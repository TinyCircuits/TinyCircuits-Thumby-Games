## Script Loading and Level Progression ##

from monsters import *
import gc
from utils import *
from machine import Pin, freq
from array import array
_buf = array('l', [0, 0, 0, 0, 0, 0, 0, 0])
bA = Pin(27, Pin.IN, Pin.PULL_UP).value
bR = Pin(5, Pin.IN, Pin.PULL_UP).value

w = None # World
_loaded = None
_last_feed = "[_","_","_","_","_]"
def _load_world(tape, mons, world, feed):
    global _loaded, _last_feed
    if _loaded != world:
        global w
        tape.feed = None
        mons.ticks = None
        w = None
        gc.collect()
        with open(f"/Games/Umby&Glow/world{world}.py") as fp:
            exec(fp.read())
        try:
            gc.collect()
            with open(f"/Games/Umby&Glow/mons{world}.py") as fp:
                exec(fp.read())
        except OSError:
            pass
        gc.collect()
        _loaded = world
    tape.feed = eval(feed)
    split = feed.split(',')
    # Reset any offscreen background changes
    if split[0] != _last_feed[0]:
        start = tape.bx[0]
        for i in range(start+72, start+144):
            tape.redraw_tape(0, i, tape.feed[0], None)
    if split[1] != _last_feed[1] or split[2] != _last_feed[2]:
        start = tape.midx[0]
        for i in range(start+72, start+144):
            tape.redraw_tape(1, i, tape.feed[1], tape.feed[2])
    _last_feed = split

def _script():
    with open("/Games/Umby&Glow/script.txt") as fp:
        for line in fp:
            if line and line[0] != "#" and line[0] != "\n":
                dist, _, ev_str = line.partition(",")
                yield int(dist), ev_str.strip()

def get_chapters():
    pos = -145
    for dist, ev in _script():
        pos += dist
        if ev.startswith('"CHAPTER~') or ev.startswith('"~'):
            yield (eval(ev), pos)

_line = _script()
_next_at, _next_event = next(_line)
state = [_next_at] # Last event for save state

def _load_lvl(tape, mons, ev):
    _load_world(tape, mons, ev[0], ev[1])
    tape.spawner = ev[2]
    for plyr in tape.players:
        plyr.space = ev[3] & 1
    tape.cam_shake = ev[3] >> 1

def story_jump(tape, mons, start, lobby):
    global _next_event, _next_at
    # Scan script finding the starting position
    if _next_at <= start:
        lvl = None
        for dist, _next_event in _line:
            state[0] = _next_at
            _next_at += dist
            if _next_event[0] == "(":
                lvl = _next_event
            if _next_at > start:
                break
        if lvl:
            _load_lvl(tape, mons, eval(lvl))

    # Reset the tape data to match the new details
    tape.reset(start)
    if lobby:
        # Fill the visible tape with the starting platform
        for i in range(start, start+72):
            tape.redraw_tape(2, i, pattern_room, pattern_fill)
        tape.write(1, "THAT WAY!", start//2+19, 26)
        tape.write(1, "------>", start//2+37, 32)
        tape.write(2, "Go Glow!^", start+1, 5)
        tape.write(2, "Go Umby!@", start+1, 40)

_dialog_queue = []
_pos = _dialog_c = 0
_active_battle = -1
_speaking = False

@micropython.native
def add_dialog(tape, dialog):
    char = dialog[0]
    pos = 1 if char == '^' else 2 if char == '@' else 3 if char == '|' else 0
    if char == '|':
        dialog = dialog[1:]
    if pos: # Worm dialog or overlay
        # Split the text into lines that fit on screen.
        lines = [""]
        for word in dialog.split(' '):
            if (int(len(lines[-1])) + int(len(word)) + 1)*4 > 72:
                lines.append("")
            lines[-1] += (" " if lines[-1] else "") + word
        # Queue up each 2 lines of dialog
        while lines:
            line = lines.pop(0)
            if lines:
                line += " " + lines.pop(0)
            _dialog_queue.append((pos, line))
    else: # Narration
        tape.message(0, dialog, 1)

@micropython.native
def story_events(tape, mons, coop_px, autotxt, outbuf, inbuf):
    global _dialog_c, _next_event, _next_at, _active_battle, _pos, _speaking
    outbuf[14] = ((1 if not _speaking or autotxt else 0) |
        (2 if _active_battle >= 0 else 0))
    if tape.player and tape.player.mode > 200:
        # Respawning
        if _speaking and not autotxt:
            tape.clear_overlay()
            tape.player.revive()
        else:
            return
    # Update current dialog queue
    if _active_battle >= 0:
        autotxt = True
    if _dialog_c > 0:
        if _dialog_c == 1 and not autotxt and (bA() and bR()):
            ali = 10 if _pos==3 else 0
            n = ">>" if _dialog_queue else "XX"
            tape.write(3, n, 65, 18-ali)
            tape.write(3, n, 65, 27+ali)
            return
        _dialog_c -= 1
        if _dialog_c == 0:
            tape.clear_overlay()
            _speaking = False
    if _dialog_queue and _dialog_c == 0:
        _pos, text = _dialog_queue.pop(0)
        tape.message(_pos%3, text, 3)
        _dialog_c = (60 + len(text)*3) // (1 if autotxt else 2)
        _speaking = True
        outbuf[14] = ((1 if not _speaking or autotxt else 0) |
        (2 if _active_battle >= 0 else 0))
    if mons.reactions:
        add_dialog(tape, mons.reactions.pop(0))
    # Script event check
    if _active_battle >= 0:
        if mons.is_alive(_active_battle):
            return # Active boss battle
        _active_battle = -1
    posx = tape.x[0]
    pos = posx if posx > coop_px else coop_px # Furthest of both players
    if pos >= _next_at:
        state[0] = _next_at
        event = eval(_next_event)
        if isinstance(event, tuple):
            _load_lvl(tape, mons, event)
        elif isinstance(event, str):
            if inbuf[14] & 2:
                return
            add_dialog(tape, event)
        elif event: # Monsters
            if posx < _next_at:
                return # Wait to reach spawn position
            bat = mons.add(event, posx+144, 32)
            if event in boss_types:
                _active_battle = bat
        dist, _next_event = next(_line)
        _next_at += dist