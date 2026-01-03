# stream_json.py - Generic streaming JSON parser for memory-constrained devices
# Reads JSON files line-by-line without loading entire file into memory

from gc import collect

def extract_str(line, key):
    """Extract string value from a JSON line like: "key": "value"
    Returns the value string or None if not found"""
    k = f'"{key}"'
    i = line.find(k)
    if i < 0: return None
    i = line.find(':', i) + 1
    while i < len(line) and line[i] in ' \t': i += 1
    if i >= len(line) or line[i] != '"': return None
    j = i + 1
    while j < len(line) and not (line[j] == '"' and line[j-1] != '\\'): j += 1
    return line[i+1:j] if j < len(line) else None

def read_field(filepath, field, max_lines=10):
    """Read a top-level string field from JSON file using streaming
    Searches first max_lines lines for the field"""
    try:
        with open(filepath, 'r') as f:
            for _ in range(max_lines):
                line = f.readline()
                if not line: break
                v = extract_str(line, field)
                if v: return v
    except: pass
    return None

def read_fields(filepath, fields, max_lines=10):
    """Read multiple top-level string fields from JSON file
    Returns dict with field names as keys"""
    result = {f: None for f in fields}
    found = 0
    try:
        with open(filepath, 'r') as f:
            for _ in range(max_lines):
                line = f.readline()
                if not line: break
                for field in fields:
                    if result[field] is None:
                        v = extract_str(line, field)
                        if v:
                            result[field] = v
                            found += 1
                            if found == len(fields): return result
    except: pass
    return result

def _find_array_start(f, array_name):
    """Find file position after array '[' for given array name
    Returns position or -1. File handle must be open."""
    target = f'"{array_name}"'
    while True:
        line = f.readline()
        if not line: return -1
        if target in line:
            bracket_pos = line.find('[')
            if bracket_pos >= 0:
                return f.tell() - len(line) + bracket_pos + 1
            pos = f.tell()
            line = f.readline()
            if not line: return -1
            bracket_pos = line.find('[')
            if bracket_pos >= 0:
                return pos + bracket_pos + 1
            return -1

def count_array(filepath, array_name):
    """Count objects in named array using streaming - no full file load"""
    try:
        with open(filepath, 'r') as f:
            arr_pos = _find_array_start(f, array_name)
            if arr_pos < 0: return 0
            f.seek(arr_pos)
            count, depth = 0, 0
            while True:
                line = f.readline()
                if not line: break
                for c in line:
                    if c == '{': depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0: count += 1
                    elif c == ']' and depth == 0:
                        return count
            return count
    except: return 0

def get_array_object(filepath, array_name, idx):
    """Get object at index from named array using streaming
    Returns parsed object dict or None"""
    try:
        with open(filepath, 'r') as f:
            arr_pos = _find_array_start(f, array_name)
            if arr_pos < 0: return None
            f.seek(arr_pos)
            depth, count = 0, 0
            obj_start, obj_end = -1, -1
            while True:
                pos = f.tell()
                line = f.readline()
                if not line: break
                for i, c in enumerate(line):
                    if c == '{':
                        if depth == 0 and count == idx:
                            obj_start = pos + i
                        depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            if count == idx:
                                obj_end = pos + i + 1
                                break
                            count += 1
                    elif c == ']' and depth == 0:
                        return None
                if obj_end > 0: break
            if obj_start < 0 or obj_end < 0: return None
            f.seek(obj_start)
            obj_str = f.read(obj_end - obj_start)
            import json
            result = json.loads(obj_str)
            collect()
            return result
    except: pass
    return None
