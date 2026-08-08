import thumby
import sys
import time
import select

thumby.display.setFPS(30)
#cursor
cx, cy = 36.0, 20.0
scroll_offset = 0
visible_lines = 5

history = []
current_req = None

page_lines = ["Press A to", "type a search"]
page_links = {}

keyboard = [
    ['q','w','e','r','t','y','u','i','o','p'],
    ['a','s','d','f','g','h','j','k','l','_'], 
    ['z','x','c','v','b','n','m','.','/','<'], 
    ['h','t','t','p',':','/','/','E','N','T']  
]

#debounce
btn_prev = {"U": False, "D": False, "L": False, "R": False, "A": False, "B": False}

def get_btn_clicks():

    global btn_prev
    clicks = {}
    for name, btn in [("U", thumby.buttonU), ("D", thumby.buttonD), ("L", thumby.buttonL), ("R", thumby.buttonR), ("A", thumby.buttonA), ("B", thumby.buttonB)]:
        pres = btn.pressed()
        clicks[name] = pres and not btn_prev[name]
        btn_prev[name] = pres
    return clicks

def open_keyboard():

    search_query = ""
    kx, ky = 0, 0
    
    while thumby.buttonA.pressed(): time.sleep(0.01)
    
    while True:
        thumby.display.fill(0)
        thumby.display.drawText("SEARCH", 0, 0, 1)
        thumby.display.drawText(search_query[-12:], 0, 9, 1)
        thumby.display.drawLine(0, 17, 72, 17, 1)
        
        start_row = ky
        if ky == len(keyboard) - 1:
            start_row = ky - 1
            
        draw_y = 20
        for y_offset in range(2):
            grid_y = start_row + y_offset
            if grid_y < len(keyboard):
                for x in range(10):
                    char = keyboard[grid_y][x]
                    if grid_y == ky and x == kx:
                        thumby.display.drawFilledRectangle(x*7, draw_y-1, 7, 9, 1)
                        thumby.display.drawText(char, x*7+1, draw_y, 0)
                    else:
                        thumby.display.drawText(char, x*7+1, draw_y, 1)
            draw_y += 10
        thumby.display.update()
        
        clicks = get_btn_clicks()
        if clicks["U"]: ky = max(0, ky - 1)
        elif clicks["D"]: ky = min(len(keyboard)-1, ky + 1)
        elif clicks["L"]: kx = max(0, kx - 1)
        elif clicks["R"]: kx = min(9, kx + 1)
        elif clicks["A"]:
            selected = keyboard[ky][kx]
            if selected == '<': search_query = search_query[:-1]
            elif selected == '_': search_query += " "
            elif selected in ['E', 'N', 'T']:
                if len(search_query) > 0:
                    return search_query
            else:
                search_query += selected
        elif clicks["B"]:
            return ""

poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

def check_serial_data():
    """Non-blocking check for incoming text frames from the host."""
    global page_lines, page_links, scroll_offset
    
    if poll_obj.poll(0):
        line = sys.stdin.readline().strip()
        if line.startswith("RESET"):
            page_lines = []
            page_links = {}
            scroll_offset = 0
        elif line.startswith("T:"):
            page_lines.append(line[2:])
        elif line.startswith("L:"):
            last_idx = len(page_lines) - 1
            if last_idx >= 0:
                page_links[last_idx] = line[2:]

def main_loop():
    global cx, cy, scroll_offset, page_lines, page_links, history, current_req
    
    while True:
        check_serial_data()
        #cursor nav
        speed = 1.3
        if thumby.buttonU.pressed(): cy = max(0.0, cy - speed)
        if thumby.buttonD.pressed(): cy = min(39.0, cy + speed)
        if thumby.buttonL.pressed(): cx = max(0.0, cx - speed)
        if thumby.buttonR.pressed(): cx = min(71.0, cx + speed)
        #scroll
        if cy >= 38.0 and (scroll_offset + visible_lines) < len(page_lines):
            scroll_offset += 1
            cy = 34.0
        elif cy <= 1.0 and scroll_offset > 0:
            scroll_offset -= 1
            cy = 5.0
            #render
        thumby.display.fill(0)
        
        for i in range(visible_lines):
            line_idx = i + scroll_offset
            if line_idx < len(page_lines):
                y_pos = i * 8
                text = page_lines[line_idx]
                
                is_link = line_idx in page_links
                hovering_line = (int(cy) // 8 == i)
                
                if is_link and hovering_line:
                    thumby.display.drawText(f">{text[:11]}", 0, y_pos, 1)
                else:
                    thumby.display.drawText(text[:12], 0, y_pos, 1)
                    
        url_hover = (cy < 5)
        if url_hover:
            thumby.display.drawFilledRectangle(0, 0, 72, 8, 1)
            thumby.display.drawText("Search", 18, 1, 0)
            
        if not url_hover:
            ix, iy = int(cx), int(cy)
            thumby.display.drawLine(ix - 1, iy, ix + 1, iy, 1)
            thumby.display.drawLine(ix, iy - 1, ix, iy + 1, 1)
            thumby.display.setPixel(ix, iy, 0)
            
        thumby.display.update()
        
        clicks = get_btn_clicks()
        
        if clicks["A"]:
            if url_hover:
                query = open_keyboard()
                if query:
                    if current_req is not None:
                        history.append(current_req)
                    
                    current_req = f"SEARCH:{query}"
                    page_lines = ["Loading...", "Fooding"]
                    page_links = {}
                    scroll_offset = 0
                    print(current_req)
            else:
                clicked_visible_idx = int(cy) // 8
                clicked_actual_idx = clicked_visible_idx + scroll_offset
                if clicked_actual_idx in page_links:
                    target_url = page_links[clicked_actual_idx]
                    
                    if current_req is not None:
                        history.append(current_req)
                        
                    current_req = f"GET:{target_url}"
                    page_lines = ["Loading...", "Fooding"]
                    page_links = {}
                    scroll_offset = 0
                    print(current_req)
                    
        #backward B
        elif clicks["B"]:
            if len(history) > 0:
                current_req = history.pop()
                page_lines = ["Loading back", "Fooding"]
                page_links = {}
                scroll_offset = 0
                print(current_req)
            else:
                current_req = None
                page_lines = ["Press A top", "type a search", "-----------------"]
                page_links = {}
                scroll_offset = 0
#shield
try:
    main_loop()
except Exception as e:
    thumby.display.fill(0)
    thumby.display.drawText("CRASH SHIELD", 2, 0, 1)
    thumby.display.drawText(str(e)[:12], 0, 12, 1)
    thumby.display.update()
    while True: pass
