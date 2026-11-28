# Thumby 4x4 grid with 2x1 selector, piece queue, centered panel, 4-way rotation
# Improved diamond pixel pattern (8x8 inner area) and elimination mechanic
import time
import random
import thumby

# Screen
SCREEN_W = 72
SCREEN_H = 40

# Grid configuration
GRID_COLS = 4
GRID_ROWS = 4
CELL_SIZE = 10  # requested size

GRID_X = 0
GRID_W = GRID_COLS * CELL_SIZE  # 40
GRID_Y = (SCREEN_H - (GRID_ROWS * CELL_SIZE)) // 2

# Right panel (area used to show active piece and next piece)
PANEL_X = GRID_X + GRID_W
PANEL_W = SCREEN_W - PANEL_X

# Game state
# board stores -1 for empty, or pattern id (0=cross, 1=rect, 2=diamond, 3=three-lines)
boards = [
    [[-1 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
]

boards_covered = [
    [[False for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    for _ in [1, 2, 3]
]

current_floor_index = 0 # 0 for 1st floor, 1 for 2nd, 2 for 3rd
available_spaces = 16
available_spaces_old = 16
warning_sound_played = False

# Selector anchor on-board coordinates (when a piece is being moved on the board)
sel_x = GRID_COLS - 1
sel_y = 0
# rotation: 0..3 clockwise
# 0 = vertical, second tile below (anchor is top)
# 1 = horizontal, second tile to the right (anchor is left)
# 2 = vertical, second tile above (anchor is bottom)
# 3 = horizontal, second tile to the left (anchor is right)
sel_rotation = 0

# Piece queue and active moving piece
# patterns: 0 = cross (big X), 1 = small 2x2 filled rect, 2 = diamond (rotated square), 3 = three horizontal lines
# pieces are lists of pattern ids, length 2 (default) or 3 (introduced at level >= 5)
active_piece = [0, 1]
next_piece = [2, 3]

# When a piece is moved from the panel to the board area, this holds the piece being moved.
moving_piece = None  # None or list like [a, b] or [a, b, c]

piece_on_panel = True  # starts in the right panel (active shown in panel)
changing_floors_locked = False

UNVEIL_DURATION_MS = 10 * 1000  # 10 seconds
unveiled_floor = -1
unveil_end_time = 0
dwarfless = False
diet_mode = None  # None, or 0..4 for the 5 diet/chill modes

TIME_ATTACK_DURATION_S = 40
time_attack = False
time_attack_seconds_left = TIME_ATTACK_DURATION_S
time_attack_start_time = 0

# Scoring system
points = 0
dosh = 0
combo = 0
level = 1

list_of_upgrades = [
    True, #lvl 0
    True, #lvl 1
    False, #rotation_enabled
    False, #combos_enabled
    False, #dwarfs_enabled
    False, #second_floor_enabled
    False, #repeated choice
    False, #neighbours_swap_enabled
    False, # in a triple tile the middle one is a joker (white tile)
    #with probability equals 0.05
    False, #remove_field_enabled
    False, #third_floor_enabled (level 10)
    False, #empties whole floor
    False, #uncovering_enabled
    ]
    
available_upgrades = [1, 2, 3, 4, 5]
remaining_upgrades = [6, 7, 8, 9, 10, 11, 12]

'''
To do:
- Diet game modes
- levels by 1.5 again (and not by 1.05)
- test on Thumby (esp. time attack)
'''


# Blink
BLINK_MS = 500
_last_blink = time.ticks_ms()
_cursor_visible = True
_dwarf_cursor_visible = True

# Movement repeat
_last_move = 0
MOVE_DELAY = 160  # ms

# A long-press detection to open dwarf market
A_down_time = None
A_hold_reported = False
HOLD_THRESHOLD_MS = 1000  # threshold to consider "held" (adjustable)

# ===============
# ==== Music ====
# ===============
NOTES = {
    "C2": 65.41,
    "D2": 73.42,
    "E2": 82.41,
    "F2": 87.31,
    "G2": 98.00,
    "A2": 110.00,
    "B2": 123.47,
    
    "C3": 130.81,
    "D3": 146.83,
    "E3": 164.81,
    "F3": 174.61,
    "G3": 196.00,
    "A3": 220.00,
    "B3": 246.94,

    "C4": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,

    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
    "F5": 698.46,
    "G5": 783.99,
    "A5": 880.00,
    "B5": 987.77
}

def play_note(note_name, duration_ms=20):
    freq = int(NOTES[note_name])
    thumby.audio.play(freq, int(duration_ms))
    
def play_pair_sound():
    play_note("C3")

def play_triplet_sound():
    play_note("C4", 50)
    time.sleep_ms(100)
    play_note("C4", 50)

def play_warning_sound():
    play_note("G3", 150)
    time.sleep_ms(170)
    play_note("E3", 300)

def play_level_sound(base_time=150):
    pause_time = base_time + 20
    
    play_note("E3", base_time/2)
    time.sleep_ms(pause_time)
    play_note("C4", base_time/2)
    time.sleep_ms(pause_time)
    play_note("G4", base_time/2)
    time.sleep_ms(pause_time)
    
    play_note("F3", base_time/2)
    time.sleep_ms(pause_time)
    play_note("D4", base_time)
    time.sleep_ms(pause_time)
    play_note("G4", base_time)
    time.sleep_ms(pause_time)
    
    play_note("C5", 2 * base_time)

def play_game_over_sound(base_time = 150):
    pause_time = base_time + 20
    
    play_note("E3", base_time/2)
    time.sleep_ms(pause_time)
    play_note("E3", base_time/2)
    time.sleep_ms(pause_time)
    play_note("E3", base_time/2)
    time.sleep_ms(pause_time)
    play_note("E3", base_time/2)
    time.sleep_ms(pause_time)
    
    play_note("B3", base_time/2)
    time.sleep_ms(pause_time)
    play_note("G3", base_time/2)
    time.sleep_ms(pause_time)
    play_note("E3", base_time/2)
    time.sleep_ms(pause_time)
    

# ============================================================
# DIRTY-REGION RENDER STATE
# ============================================================
# Each board cell is tracked independently. This lets the renderer repaint
# only the tiles whose pixels may have become stale.
dirty_grids = [
    [[True for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
]
panel_dirty = True
dosh_dirty = True
timer_dirty = True
overlay_dirty = True
force_full_redraw = True

def invalidate_grid_coords(coords, floor):
    """Mark the supplied valid board coordinates for repaint."""
    for x, y in coords:
        if 0 <= x < GRID_COLS and 0 <= y < GRID_ROWS:
            dirty_grids[floor][y][x] = True

def invalidate_all_grid():
    """Mark every board tile dirty."""
    for y in range(GRID_ROWS):
        row = dirty_grids[current_floor_index][y]
        for x in range(GRID_COLS):
            row[x] = True

def invalidate_panel():
    """Mark the right-hand piece panel for repaint."""
    global panel_dirty
    panel_dirty = True

def invalidate_dosh():
    """Mark the score/currency text area for repaint."""
    global dosh_dirty
    dosh_dirty = True

def invalidate_overlay():
    """Mark the moving-piece/selector overlay for repaint."""
    global overlay_dirty
    overlay_dirty = True

def invalidate_all():
    """Invalidate the complete gameplay scene after an overlay screen."""
    global force_full_redraw, panel_dirty, dosh_dirty, timer_dirty, overlay_dirty
    force_full_redraw = True
    panel_dirty = True
    dosh_dirty = True
    timer_dirty = True
    overlay_dirty = True
    invalidate_all_grid()

# ============================================================
# SYMBOL BITMAPS (8×8)
# ============================================================

crossBitmap = [
    1,0,0,0,0,0,0,1,
    0,1,0,0,0,0,1,0,
    0,0,1,0,0,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,1,0,0,1,0,0,
    0,1,0,0,0,0,1,0,
    1,0,0,0,0,0,0,1
]

rectBitmap = [
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
]

diamondBitmap = [
    0,0,0,1,1,0,0,0,
    0,0,1,0,0,1,0,0,
    0,1,0,0,0,0,1,0,
    1,0,0,0,0,0,0,1,
    1,0,0,0,0,0,0,1,
    0,1,0,0,0,0,1,0,
    0,0,1,0,0,1,0,0,
    0,0,0,1,1,0,0,0
]

threeLinesBitmap = [
    0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0,
    1,1,1,1,1,1,1,1,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
]

semicolonDBitmap = [
    0,0,0,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,1,0,1,0,1,0,0,
    0,0,0,1,0,0,1,0,
    0,0,0,1,0,0,1,0,
    0,1,0,1,0,1,0,0,
    0,1,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0
]

plusBitmap = [
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,1,1,0,0,0
]

sadFaceBitmap = [
    0,0,0,0,0,0,0,0,
    0,1,1,0,0,0,1,0,
    0,1,1,0,0,1,0,0,
    0,0,0,0,1,0,0,0,
    0,0,0,0,1,0,0,0,
    0,1,1,0,0,1,0,0,
    0,1,1,0,0,0,1,0,
    0,0,0,0,0,0,0,0
]

circlesBitmap = [
    0,0,0,1,1,1,0,0,
    0,1,1,0,0,0,1,0,
    1,0,0,1,1,0,1,0,
    1,0,1,0,0,1,0,1,
    1,0,1,0,0,1,0,1,
    0,1,0,1,1,0,0,1,
    0,1,0,0,0,1,1,0,
    0,0,1,1,1,0,0,0
]

glassBitmap = [
    0,0,0,0,0,0,0,0,
    0,1,0,0,1,0,1,0,
    0,1,0,1,0,0,1,0,
    0,1,0,0,0,0,1,0,
    0,0,1,0,0,1,0,0,
    0,0,1,0,0,1,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0
]

spiralBitmap = [
    0,0,0,0,0,0,0,0,
    0,1,1,0,0,0,0,0,
    0,1,0,1,0,0,0,0,
    0,0,1,0,0,0,0,0,
    1,1,0,1,0,1,0,0,
    0,0,0,0,1,0,1,0,
    0,0,0,1,0,1,0,0,
    0,0,0,1,0,0,0,0
]

grubolBitmap = [
    0,0,0,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,0,0,0,1,0,0,
    0,0,0,0,0,0,0,0,
    0,0,1,0,0,0,0,0,
    0,0,0,1,1,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0
]

tileBorderBitmap = [
        1,1,1,1,1,1,1,1,1,1,
        1,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,0,1,
        1,0,0,0,0,0,0,0,0,1,
        1,1,1,1,1,1,1,1,1,1
    ]

jokerBitmap = [
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,1,1
]

twoSpacesLeftBitmap = [
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,1,0,
    0,0,0,0,0,0,0,0
]

oneSpaceLeftBitmap = [
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,
    0,0,0,0,1,0,1,0,
    0,0,0,0,0,0,0,0
]

coveredBitmap = [
    0,0,0,0,0,0,0,0,
    0,0,1,0,0,1,0,0,
    0,1,0,1,1,0,1,0,
    0,0,0,1,0,0,1,0,
    0,0,1,0,0,1,0,0,
    0,0,0,0,0,0,0,0,
    0,0,1,0,0,1,0,0,
    0,0,0,0,0,0,0,0
]

list_of_pattern_bitmaps = [
    crossBitmap,
    rectBitmap,
    diamondBitmap,
    threeLinesBitmap,
    semicolonDBitmap,
    plusBitmap,
    sadFaceBitmap,
    circlesBitmap,
    glassBitmap,
    spiralBitmap,
    grubolBitmap
    ]
    
def correct_bitmap(bitmap, width, height):
    # bitmap -> 2D [y][x]
    pixels = []
    for i in range(0, len(bitmap), width):
        pixels.append(bitmap[i:i+width])

    packed = bytearray()
    blocks = (height + 7) // 8  # number of 8-pixel vertical blocks

    for block in range(blocks):
        for x in range(width):
            byte = 0
            for bit_index in range(8):
                y = block * 8 + bit_index
                if y < height and pixels[y][x]:
                    byte |= (1 << bit_index)  # bit 0 = top row of this block
            packed.append(byte)

    return packed
    
def correct_bitmaps():
    global list_of_pattern_bitmaps, tileBorderBitmap, jokerBitmap
    global twoSpacesLeftBitmap, oneSpaceLeftBitmap, coveredBitmap
    
    list_of_pattern_bitmaps = [correct_bitmap(x, 8, 8) for x in list_of_pattern_bitmaps]
        
    tileBorderBitmap = correct_bitmap(tileBorderBitmap, 10, 10)
    jokerBitmap = correct_bitmap(jokerBitmap, 8, 8)
    twoSpacesLeftBitmap = correct_bitmap(twoSpacesLeftBitmap, 8, 8)
    oneSpaceLeftBitmap = correct_bitmap(oneSpaceLeftBitmap, 8, 8)
    coveredBitmap = correct_bitmap(coveredBitmap, 8, 8)

def just_pressed(btn):
    try:
        return btn.justPressed()
    except AttributeError:
        return btn.pressed()

def handle_input(now):
    global sel_x, sel_y, _last_move, changing_floors_locked
    global moving_piece, active_piece, next_piece
    global moving_piece, piece_on_panel, sel_rotation
    global overlay_dirty
    global A_down_time, A_hold_reported
    global level, points
    global available_spaces, available_spaces_old
    global warning_sound_played
    
    if piece_on_panel:
        # L moves the active piece onto the board.
        if just_pressed(thumby.buttonL) or thumby.buttonL.pressed():
            # move active piece into moving_piece
            moving_piece = list(active_piece)
        
            # Move next -> active, then generate a fresh next piece.
            active_piece = list(next_piece)
            next_piece = pick_random_piece()
        
            sel_x = GRID_COLS - 1
            sel_y = 0
            clamp_selector()
        
            piece_on_panel = False
        
            # Panel changed immediately; repaint it this frame.
            invalidate_panel()
        
            # The moving piece will be drawn over these cells.
            invalidate_grid_coords(
                get_selector_touched_tiles(
                    sel_x, sel_y, sel_rotation, moving=True
                ),
                current_floor_index
            )
            invalidate_overlay()
            
            time.sleep_ms(140)
            visual_changed = True

        # A opens dwarf market on panel (only after upgrade).
        # list_of_upgrades[4] = dwarfs_enabled
        if (just_pressed(thumby.buttonA) or thumby.buttonA.pressed()) and list_of_upgrades[4] and not dwarfless:
            # Open dwarf market view. Wait until market closes.
            show_dwarf_market()
            # After returning from market, force a redraw of UI
            invalidate_all()
            # Small delay to avoid immediate re-trigger
            time.sleep_ms(120)
            visual_changed = True
        
        # U/D change floors on panel
        if thumby.buttonU.pressed():
            change_floors("U")
        elif thumby.buttonD.pressed():
            change_floors("D")
        
    else:
        # Save the old footprint before changing selector position.
        old_sel_coords = set(
            get_selector_touched_tiles(
                sel_x, sel_y, sel_rotation, moving=True
            )
        )

        moved = False

        if thumby.buttonU.pressed():
            if time.ticks_diff(now, _last_move) > MOVE_DELAY:
                sel_y -= 1
                _last_move = now
                moved = True
            
        elif thumby.buttonD.pressed():
            if time.ticks_diff(now, _last_move) > MOVE_DELAY:
                sel_y += 1
                _last_move = now
                moved = True

        elif thumby.buttonL.pressed():
            if time.ticks_diff(now, _last_move) > MOVE_DELAY:
                sel_x -= 1
                _last_move = now
                moved = True

        elif thumby.buttonR.pressed():
            if time.ticks_diff(now, _last_move) > MOVE_DELAY:
                sel_x += 1
                _last_move = now
                moved = True

        else:
            _last_move = 0

        clamp_selector()

        if moved:
            new_sel_coords = set(
                get_selector_touched_tiles(
                    sel_x, sel_y, sel_rotation, moving=True
                )
            )
            # Restores old preview + paints new preview underneath.
            invalidate_grid_coords(old_sel_coords | new_sel_coords, current_floor_index)
            invalidate_overlay()
            visual_changed = True

        # B rotates selector clockwise.
        # list_of_upgrades[2] = rotation_enabled
        if list_of_upgrades[2] and just_pressed(thumby.buttonB):
            changing_floors_locked = True
            
            old_rot_coords = set(
                get_selector_touched_tiles(
                    sel_x, sel_y, sel_rotation, moving=True
                )
            )

            rotate_selector_clockwise()

            new_rot_coords = set(
                get_selector_touched_tiles(
                    sel_x, sel_y, sel_rotation, moving=True
                )
            )

            invalidate_grid_coords(old_rot_coords | new_rot_coords, current_floor_index)
            invalidate_overlay()
            time.sleep_ms(120)
            visual_changed = True
            changing_floors_locked = False

        #A-pressing handling
        
        #Button just went down
        if thumby.buttonA.justPressed():
            A_down_time = time.ticks_ms()
            A_hold_reported = False
            changing_floors_locked = True
    
        # Button is being held
        if A_down_time is not None and thumby.buttonA.pressed():
            duration = time.ticks_diff(time.ticks_ms(), A_down_time)
    
            # Threshold crossed → report "held" immediately
            if duration >= HOLD_THRESHOLD_MS and not A_hold_reported:
                A_hold_reported = True
                
                # list_of_upgrades[4] = dwarfs_enabled
                if list_of_upgrades[4] and not dwarfless:
                    # Open dwarf market view. Wait until market closes.
                    changing_floors_locked = False
                    show_dwarf_market()
                    # After returning from market, force a redraw of UI
                    invalidate_all()
                    # Small delay to avoid immediate re-trigger
                    time.sleep_ms(120)
                    visual_changed = True 
    
        # Button released
        if A_down_time is not None and not thumby.buttonA.pressed():
            # If threshold was NOT crossed → it's a short press
            if not A_hold_reported:
                
                if place_moving_piece_at(sel_x, sel_y, sel_rotation):
                    select_new_cover()
                    # Level-up check
                    if not time_attack and diet_mode is None:
                        while points >= get_level_threshold(level):
                            level += 1
                            show_level_upgrade(level)
                    
                    update_available_spaces_counter()
                    if available_spaces == 0:
                        if time_attack or diet_mode is not None:
                            show_time_attack_game_over()
                            return
                        else:
                            show_game_over()
                    
                    if available_spaces != available_spaces_old:
                        # refresh whole grid if the counter has changed
                        invalidate_all_grid()
                        available_spaces_old = available_spaces
                    
                    piece_on_panel = True
                    overlay_dirty = False
                    sel_rotation = 0
                    clamp_selector()
                    warning_sound_played = False
    
                    # The board changed via place_moving_piece_at().
                    # The panel queue was already updated when the piece was
                    # first taken from the panel, but the selector has now
                    # returned to the panel.
                    invalidate_panel()
                    visual_changed = True
                else:
                    time.sleep_ms(120)
    
            # Reset state
            A_down_time = None
            A_hold_reported = False
            changing_floors_locked = False
            
    # Optional board clear with L+R+A.
    if (
        thumby.buttonL.pressed()
        and thumby.buttonR.pressed()
        and thumby.buttonA.pressed()
    ):
        clear_boards()
        time.sleep_ms(200)
        visual_changed = True

# Drawing helpers
def draw_tile_border(px, py):
    thumby.display.blit(tileBorderBitmap, px, py, 10, 10, -1, 0, 0)

def draw_tile(cx, cy, pattern):
    global warning_sound_played
    
    px = GRID_X + cx * CELL_SIZE
    py = GRID_Y + cy * CELL_SIZE
    draw_tile_border(px, py)
    if pattern is not None and pattern >= 0:
        if level < 12: # without covering
            draw_pattern_in_tile_at(px, py, pattern)
        else:
            is_unveiled = (current_floor_index == unveiled_floor and unveil_end_time != 0)
            if boards_covered[current_floor_index][cy][cx] and not is_unveiled:
                draw_pattern_in_tile_at(px, py, 88) # 88 = coveredBitmap
            else:
                draw_pattern_in_tile_at(px, py, pattern)
                    
    elif pattern is None:
        if 4 < available_spaces <= 8:
            draw_pattern_in_tile_at(px, py, 92) # 92 = twoSpacesLeftBitmap
        elif available_spaces <= 4:
            draw_pattern_in_tile_at(px, py, 91) # 91 = oneSpaceLeftBitmap
            if piece_on_panel and not warning_sound_played:
                play_warning_sound()
                warning_sound_played = True

def get_pattern_bitmap(pattern):
    if pattern == 99: # joker
        return jokerBitmap
    elif pattern == 92: # two spaces left
        return twoSpacesLeftBitmap
    elif pattern == 91: # one space left
        return oneSpaceLeftBitmap
    elif pattern == 88: # covered
        return coveredBitmap
    return list_of_pattern_bitmaps[pattern]

def draw_pattern_in_tile_at(px, py, pattern):
    # px, py are top-left pixel coords of the tile (including border)
    # inner drawable area is 8x8 at px+1..px+8, py+1..py+8
    
    patternBitmap = get_pattern_bitmap(pattern)
    
    thumby.display.blit(patternBitmap, px + 1, py + 1, 8, 8, -1, 0, 0)
    

def draw_panel_tile_at(px, py, pattern):
    draw_tile_border(px, py)
    if pattern is not None and pattern >= 0:
        draw_pattern_in_tile_at(px, py, pattern)

def draw_selector_rect_from_rotation(x, y, rotation, visible, length=2):
    if not visible:
        return
    # compute bounding rectangle for the piece based on rotation and length
    px = GRID_X + x * CELL_SIZE
    py = GRID_Y + y * CELL_SIZE

    if rotation == 0:
        w = CELL_SIZE
        h = CELL_SIZE * length
        rx = px
        ry = py
    elif rotation == 1:
        w = CELL_SIZE * length
        h = CELL_SIZE
        rx = px
        ry = py
    elif rotation == 2:
        w = CELL_SIZE
        h = CELL_SIZE * length
        rx = px
        ry = py - CELL_SIZE * (length - 1)
    else:  # rotation == 3
        w = CELL_SIZE * length
        h = CELL_SIZE
        rx = px - CELL_SIZE * (length - 1)
        ry = py

    # Outer rectangle border around the combined area
    thumby.display.drawLine(rx, ry, rx + w - 1, ry, 1)
    thumby.display.drawLine(rx, ry, rx, ry + h - 1, 1)
    thumby.display.drawLine(rx, ry + h - 1, rx + w - 1, ry + h - 1, 1)
    thumby.display.drawLine(rx + w - 1, ry, rx + w - 1, ry + h - 1, 1)

    # inner inset border for clearer highlight
    if w > 2 and h > 2:
        thumby.display.drawLine(rx + 1, ry + 1, rx + w - 2, ry + 1, 1)
        thumby.display.drawLine(rx + 1, ry + 1, rx + 1, ry + h - 2, 1)
        thumby.display.drawLine(rx + 1, ry + h - 2, rx + w - 2, ry + h - 2, 1)
        thumby.display.drawLine(rx + w - 2, ry + 1, rx + w - 2, ry + h - 2, 1)


def draw_selector_panel(visible, length=2):
    if not visible:
        return
    # center both pieces horizontally in the panel with even spacing between:
    gap = (PANEL_W - 2 * CELL_SIZE) // 3
    left_px = PANEL_X + gap
    right_px = left_px + CELL_SIZE + gap
    top_py = GRID_Y

    # outer rectangle around the left (active) stacked tiles (visual selector)
    w = CELL_SIZE
    h = CELL_SIZE * length
    
    thumby.display.drawLine(left_px, top_py, left_px + w - 1, top_py, 1)
    thumby.display.drawLine(left_px, top_py, left_px, top_py + h - 1, 1)
    thumby.display.drawLine(left_px, top_py + h - 1, left_px + w - 1, top_py + h - 1, 1)
    thumby.display.drawLine(left_px + w - 1, top_py, left_px + w - 1, top_py + h - 1, 1)
    if w > 2 and h > 2:
        thumby.display.drawLine(left_px + 1, top_py + 1, left_px + w - 2, top_py + 1, 1)
        thumby.display.drawLine(left_px + 1, top_py + 1, left_px + 1, top_py + h - 2, 1)
        thumby.display.drawLine(left_px + 1, top_py + h - 2, left_px + w - 2, top_py + h - 2, 1)
        thumby.display.drawLine(left_px + w - 2, top_py + 1, left_px + w - 2, top_py + h - 2, 1)

def clear_boards(show_intro=True, open_menu=True):
    global boards, dirty_grids, points, dosh, combo, level
    global dwarfless, time_attack, diet_mode, changing_floors_locked
    global unveiled_floor, unveil_end_time
    global active_piece, next_piece
    global moving_piece, piece_on_panel
    global sel_x, sel_y, sel_rotation
    global _cursor_visible, _last_blink
    global _last_move, A_down_time, A_hold_reported
    global list_of_upgrades, available_upgrades, remaining_upgrades
    global current_floor_index
    global available_spaces, available_spaces_old
    global warning_sound_played

    # Boards and scoring
    boards = [
        [[-1 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    ]
    dirty_grids = [
        [[True for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
    ]
    current_floor_index = 0
    available_spaces = 16
    available_spaces_old = 16
    points = 0
    dosh = 0
    combo = 0
    level = 1

    dwarfless = False
    time_attack = False
    diet_mode = None
    changing_floors_locked = False
    unveiled_floor = -1
    unveil_end_time = 0

    # Upgrades
    list_of_upgrades = [
        True,
        True,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
        False,
    ]
    available_upgrades = [1, 2, 3, 4, 5]
    remaining_upgrades = [6, 7, 8, 9, 10, 11, 12]

    # Piece queue
    active_piece = pick_random_piece()
    next_piece = pick_random_piece()
    moving_piece = None
    piece_on_panel = True

    # Selector
    sel_x = GRID_COLS - 1
    sel_y = 0
    sel_rotation = 0

    # Blink + input states
    _cursor_visible = True
    _last_blink = time.ticks_ms()
    _last_move = 0
    A_down_time = None
    A_hold_reported = False
    warning_sound_played = False

    # Redraw everything
    invalidate_all()
    thumby.display.fill(0)
    thumby.display.update()
    if show_intro:
        grubol_menu()
    if open_menu:
        show_main_menu()


def get_piece_coords_from_anchor(x, y, rotation, length=2):
    """
    Return list of coords for a piece anchored at (x,y) with given rotation.
    length is number of tiles (2 or 3).
    Anchor is the first tile in the list (same convention as before).
    rotation: 0=vertical down, 1=horizontal right, 2=vertical up, 3=horizontal left
    """
    coords = []
    if rotation == 0:  # vertical down
        for i in range(length):
            coords.append((x, y + i))
    elif rotation == 1:  # horizontal right
        for i in range(length):
            coords.append((x + i, y))
    elif rotation == 2:  # vertical up
        for i in range(length):
            coords.append((x, y - i))
    else:  # rotation == 3 horizontal left
        for i in range(length):
            coords.append((x - i, y))
    return coords


def clamp_selector():
    global sel_x, sel_y, sel_rotation
    # ensure both tiles are within bounds
    if sel_x < 0: sel_x = 0
    if sel_x > GRID_COLS - 1: sel_x = GRID_COLS - 1
    if sel_y < 0:
        sel_y = 0
        change_floors("U")
    if sel_y > GRID_ROWS - 1:
        sel_y = GRID_ROWS - 1
        change_floors("D")

    length = len(moving_piece) if moving_piece is not None else len(active_piece)
    coords = get_piece_coords_from_anchor(sel_x, sel_y, sel_rotation, length)

    # if any coord out of bounds, try to shift anchor to make it fit
    for _ in range(4):
        bad = False
        for (cx, cy) in coords:
            if cx < 0:
                sel_x += 1
                bad = True
            if cx >= GRID_COLS:
                sel_x -= 1
                bad = True
            if cy < 0:
                sel_y += 1
                change_floors("U")
                bad = True
            if cy >= GRID_ROWS:
                sel_y -= 1
                change_floors("D")
                bad = True
        if not bad:
            break
        length = len(moving_piece) if moving_piece is not None else len(active_piece)
        coords = get_piece_coords_from_anchor(sel_x, sel_y, sel_rotation, length)


    # final clamp to absolute bounds
    if sel_x < 0: sel_x = 0
    if sel_x > GRID_COLS - 1: sel_x = GRID_COLS - 1
    if sel_y < 0: sel_y = 0
    if sel_y > GRID_ROWS - 1: sel_y = GRID_ROWS - 1

def rotate_selector_clockwise():
    global sel_rotation
    sel_rotation = (sel_rotation - 1) % 4
    clamp_selector()

def get_shapes():
    # shapes: 0=cross, 1=rect, 2=diamond, 3=three-lines, ...
    if time_attack:
        return [0, 1, 2, 3, 4, 5, 6]
    if diet_mode is not None:
        if diet_mode == 0:          # Utopia chill: 4 symbols
            return [0, 1, 2, 3]
        elif diet_mode in (1, 2):   # Total chill, Netflix & chill: 6 symbols
            return [0, 1, 2, 3, 4, 5]
        else:                       # Red hot chill, Endless winter chill: 11 symbols
            return [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    shapes = [0, 1, 2] #lvl 1
    if level >= 2: shapes.append(3)
    if level >= 3: shapes.append(4)
    if level >= 4: shapes.append(5)
    # level 5 => triple tiles
    if level >= 6: shapes.append(6)
    if level >= 7: shapes.append(7)
    if level >= 8: shapes.append(8)
    if level >= 9: shapes.append(9)
    if level >= 10: shapes.append(10)
    # later levels => not related to shapes
    return shapes

def pick_random_piece():
    """
    Return a list of pattern ids. Before level 5 always length 2.
    At level >= 5: with probability 0.5 return length 3, otherwise length 2.
    Ensure adjacent tiles in the same piece can be the same or different;
    keep the previous rule that in a 2-length piece the two are different.
    For 3-length pieces we allow any combination but avoid all three equal
    to keep variety (optional; you can remove that check if you prefer).
    """
    shapes = get_shapes()
    # decide length
    length = 2
    if diet_mode is not None:
        if diet_mode in (2, 3):     # Netflix & chill, Red hot chill: 2 or 3
            if random.random() < 0.5:
                length = 3
        elif diet_mode == 4:        # Endless winter chill: only 3-square pieces
            length = 3
    elif level >= 5 and not time_attack:
        rand_num = random.random()
        if rand_num < 0.5:
            length = 3
        else:
            if level >= 11 and rand_num < 0.75:
                length = 3

    if length == 2:
        a = random.choice(shapes)
        b = random.choice(shapes)
        while b == a:
            b = random.choice(shapes)
        return [a, b]
    else:
        # length == 3
        a = random.choice(shapes)
        b = random.choice(shapes)
        c = random.choice(shapes)
        # optional: avoid all three equal to keep variety
        while a == b or a == c or b == c:
            while b == a or b == c:
                b = random.choice(shapes)
            while c == a:
                c = random.choice(shapes)
        
        if list_of_upgrades[8]: # if joker enabled
            if random.random() < 0.05: # probability of joker
                b = 99 # joker pattern
        return [a, b, c]


def can_place_at(x, y, rotation, length=None, floor=10):
    # length None -> infer from moving_piece if available, else default 2
    if length is None:
        if moving_piece is not None:
            length = len(moving_piece)
        else:
            length = 2
    
    coords = get_piece_coords_from_anchor(x, y, rotation, length)
    for (cx, cy) in coords:
        if cx < 0 or cx >= GRID_COLS or cy < 0 or cy >= GRID_ROWS:
            return False
        if boards[floor][cy][cx] != -1:
            return False
    return True

def place_moving_piece_at(x, y, rotation):
    global moving_piece

    if moving_piece is None:
        return False

    length = len(moving_piece)

    if not can_place_at(x, y, rotation, length, current_floor_index):
        return False

    coords = get_piece_coords_from_anchor(x, y, rotation, length)

    # Place each tile of the moving piece onto the board
    for (px, py), pattern in zip(coords, moving_piece):
        boards[current_floor_index][py][px] = pattern

    # After placing, run elimination mechanic for each placed square.
    to_clear = set()

    def flood_collect(sx, sy):
        """Return set of connected coords (orthogonal) with same symbol."""
        symbol = boards[current_floor_index][sy][sx]
        if symbol == -1:
            return set()
        if symbol == 99: # 99 = joker
            return_set = set()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = sx + dx, sy + dy
                if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                    return_set.add((nx, ny))
            return return_set

        stack = [(sx, sy)]
        visited = set()

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue

            visited.add((cx, cy))

            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                    if boards[current_floor_index][ny][nx] in [symbol, 99] and (nx, ny) not in visited:
                        # 99 = joker
                        stack.append((nx, ny))

        return visited

    # collect groups for each placed tile
    for (px, py) in coords:
        group = flood_collect(px, py)
        if 2 <= len(group) <= 4:
            to_clear.update(group)

    for cx, cy in to_clear:
        boards[current_floor_index][cy][cx] = -1

    changed = set(coords)
    changed.update(to_clear)
    invalidate_grid_coords(changed, current_floor_index)
    
    to_clear = list(dict.fromkeys(to_clear)) #removes duplicates
    cleared_count = len(to_clear)
    apply_scoring(cleared_count)

    moving_piece = None
    return True

def show_level_upgrade(level):
    global visual_changed
    global list_of_upgrades, available_upgrades, remaining_upgrades
    global dosh

    list_of_upgrades_details = [ #exclamation, description
            ["", "", 0], #lvl 0
            ["", "", 0], #lvl 1
            ["Not bad!", "Rotation\n\nAllows you to rotate pieces with B-button.", 0], #lvl 2
            ["Alright!", "Combo\n\nAllows you to score more points when tiles are removed in a series.", 0], #lvl 3
            ["Sweet!", "Dwarf market\n\nAllows you to open dwarf market by holding A.", 0], #lvl 4
            ["Nice!", "Second floor\n\nAllows you to put tiles on two floors. Allows you to switch floors by going up or down the board.", 50], #lvl 5
            ["Good!", "Repeating dwarf\n\nAllows you to exchange the current tile to a new random one for $20.", 25], #lvl 6
            ["Very good!", "Swapping dwarf\n\nAllows you to swap two neigh\nbouring fields for $50.", 40], #lvl 7
            ["Grand!", "Joker\n\nMakes a joker (white square) appear in the middle of 5% of triple tiles.", 100], #lvl 8
            ["Fantastic!", "Removing dwarf\n\nAllows you to make a field empty for $100.", 50], #lvl 9
            ["Brilliant!", "Third floor\n\nAllows you to put tiles on three floors. Allows you to switch floors by going up or down the board.", 350], #350 lvl 10
            ["Superb!", "Clean dwarf\n\nAllows you to make a whole floor empty for $1000.", 100], #lvl 11
            ["Wonderful!", "Unveiling dwarf\n\nAllows you to uncover a whole floor for 10s for $10 x current level (e.g. $120 for level 12).", 150], #lvl 12
            ["Marvellous!", "", 0], #lvl 13
            ["Mental!", "", 0], #lvl 14
            ["Wow!", "", 0]
        ]
            
    if level >= 5:
        if 6 <= level <= 12 and len(remaining_upgrades) > 0:
            new_upgrade = random.choice(remaining_upgrades)
            remaining_upgrades.remove(new_upgrade)
            available_upgrades.append(new_upgrade)

        possible_outcomes = []
        # Check all unlocked upgrades that have not been bought yet
        for x in available_upgrades:
            if not list_of_upgrades[x]:
                # Third floor (10) cannot be proposed without second floor (5)
                if x == 10 and not list_of_upgrades[5]:
                    continue
                # Dwarfs (6, 7, 9, 11, 12) cannot be proposed without dwarf market (4)
                if x in [6, 7, 9, 11, 12] and not list_of_upgrades[4]:
                    continue
                possible_outcomes.append(x)

        if len(possible_outcomes) > 0:
            final_outcome = random.choice(possible_outcomes)
    else:
        final_outcome = level
        possible_outcomes = [final_outcome]
        if dwarfless and level == 4:
            possible_outcomes = []
            list_of_upgrades[final_outcome] = True
            # True because we don't want it to be available
            # as an upgrade. And we'll set all dwarfs to be true too:
            for x in [6, 7, 9, 11, 12]: list_of_upgrades[x] = True
            
            
        
    def buy():
        global list_of_upgrades, dosh
        global boards
        
        if dosh - list_of_upgrades_details[final_outcome][2] >= 0:
            list_of_upgrades[final_outcome] = True
            dosh -= list_of_upgrades_details[final_outcome][2]
            
            if final_outcome in [5, 10]:
            # adding a second or third floor
                boards.append(
                    [[-1 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
                )
                
                dirty_grids.append(
                    [[True for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]
                )
                
        else: # if you're poor
            show_scrolling_menu(
                "You've got:", "$ " + str(dosh),
                "Earn a bit more and come back later.",
                decline,
                decline
            )
            

    def decline():
        global list_of_upgrades
        list_of_upgrades[final_outcome] = False
    
    if level < len(list_of_upgrades_details):
        exclamation_text = list_of_upgrades_details[level][0]
    else:
        exclamation_text = ""
    
    level_text = "Level " + str(level)
    
    if len(possible_outcomes) > 0:
        description_text = list_of_upgrades_details[final_outcome][1]
        cost_text = str(list_of_upgrades_details[final_outcome][2])
        compound_description_text = description_text + "\n\nA Buy for $" + cost_text + "\nB Decline"

        show_scrolling_menu(
            exclamation_text, level_text,
            compound_description_text, buy, decline
        )
    else:
        def just_continue():
            return
        
        list_of_funny_lines = [
            "Still hungry for more?",
            "Haven't you got enough yet?",
            "You ain't gunna stop, are you?",
            "Kmon, mate, this game ain't worth it...",
            "Where are we heading?",
            "Haven't you any housework to do or summat?",
            "Are you ready?",
            "Run, Forrest, run!",
            "This is not the greatest game in the world, no.",
            "Meanwhile your friends: ...",
            "Shall you pass?",
            "Keep up, moth- -the- -cracker!"
            ]
        
        compound_description_text = random.choice(list_of_funny_lines)
        if level == 15:
            compound_description_text = "\nFlipping heck!"
        elif level == 16:
            compound_description_text = "\nBloody hell!"
        elif level == 17:
            compound_description_text = "\nFucking hell!"
        elif level == 18:
            compound_description_text = "\nBruv, are you a human?"
        elif level == 19:
            compound_description_text = "\nKollektivet sang about you... In the song 'Not human'"
        elif level == 20:
            compound_description_text = "\nYou're the god of this game, mate"
        
        show_scrolling_menu(
            exclamation_text, level_text,
            compound_description_text, just_continue, just_continue
        )
        
    
    # The upgrade screen uses the full display, so restore
    # the main-game scene when it returns.
    invalidate_all()
    visual_changed = True

def show_game_over():

    def buy():
        clear_boards()

    def decline():
        return

    menu_text = (
        "Oh blast... But hey...! Let's have another go, we'll make it to level " +
        str(level + 1) +
        " this time!"
    )
    show_scrolling_menu("You've run", "out of space", menu_text, buy, decline)

def update_available_spaces_counter():
    global available_spaces, available_spaces_old
    
    counter = 0
    
    for floor in range(len(boards)):
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                for rot in (0,1,2,3):
                    if can_place_at(x, y, rot, length=3, floor=floor):
                        counter += 1
                        if counter > 8:
                        # we don't need to count more
                        # because it doesn't matter
                            available_spaces = counter
                            return
    
    available_spaces = counter

def draw_grid_tile(x, y):
    """Draw exactly one board cell."""
    val = boards[current_floor_index][y][x]
    px = GRID_X + x * CELL_SIZE
    py = GRID_Y + y * CELL_SIZE

    # Clearing first guarantees that stale preview/selector pixels disappear.
    thumby.display.drawFilledRectangle(px, py, CELL_SIZE, CELL_SIZE, 0)
    draw_tile(x, y, None if val == -1 else val)


def draw_dirty_grid():
    """Redraw dirty board cells and return the coordinates actually repainted."""
    repainted = set()

    for y in range(GRID_ROWS):
        row = dirty_grids[current_floor_index][y]
        for x in range(GRID_COLS):
            if row[x]:
                draw_grid_tile(x, y)
                row[x] = False
                repainted.add((x, y))

    return repainted


def get_panel_piece_rect():
    gap = (PANEL_W - 2 * CELL_SIZE) // 3
    left_px = PANEL_X + gap
    right_px = left_px + CELL_SIZE + gap
    top_py = GRID_Y
    return left_px, right_px, top_py

def clear_third_row(left_px, right_px):
    third_y = GRID_Y + 2 * CELL_SIZE
    
    # Active piece third row
    if len(active_piece) >= 3:
        draw_panel_tile_at(left_px, third_y, active_piece[2])
    else:
        thumby.display.drawFilledRectangle(left_px, third_y, CELL_SIZE, CELL_SIZE, 0)
    
    # Next piece third row
    if len(next_piece) >= 3:
        draw_panel_tile_at(right_px, third_y, next_piece[2])
    else:
        thumby.display.drawFilledRectangle(right_px, third_y, CELL_SIZE, CELL_SIZE, 0)

def draw_floor_indicator():
    # Three vertical segments, 1px wide, 3px tall each
    # Positioned between active and next piece tiles
    gap = (PANEL_W - 2 * CELL_SIZE) // 3
    left_px = PANEL_X + 2 * gap
    right_px = left_px + CELL_SIZE + gap
    mid_x = (left_px + right_px) // 2  # center between tiles

    #base_y = GRID_Y + CELL_SIZE // 2  # vertically centered
    base_y = 2 * CELL_SIZE - 5  # vertically centered

    # Draw segments from bottom to top
    segments = current_floor_index + 1  # 0→1 segment, 1→2, 2→3

    for i in range(segments):
        seg_y = base_y - (i * 6)
        thumby.display.drawLine(mid_x, seg_y, mid_x, seg_y + 3, 1)


def draw_panel_contents():
    """Repaint only the panel's piece/selector area, not the whole screen."""
    left_px, right_px, top_py = get_panel_piece_rect()

    # Clear the small panel-piece region first.
    thumby.display.drawFilledRectangle(
        PANEL_X, top_py, PANEL_W, CELL_SIZE * 2, 0
    )

    # Active piece (stacked vertically in the left panel column)
    for i, pattern in enumerate(active_piece):
        draw_panel_tile_at(left_px, top_py + i * CELL_SIZE, pattern)
    
    # Next piece (stacked vertically in the right panel column)
    for i, pattern in enumerate(next_piece):
        draw_panel_tile_at(right_px, top_py + i * CELL_SIZE, pattern)

    if not time_attack:
        clear_third_row(left_px, right_px)
    draw_floor_indicator()

    # Panel selector.
    if piece_on_panel:
        draw_selector_panel(_cursor_visible, length=len(active_piece))


def draw_dosh():
    # Only erase the tiny text area that contains the value.
    thumby.display.drawFilledRectangle(
        PANEL_X, SCREEN_H - 7, PANEL_W, 7, 0
    )
    dosh_text = "S " + str(dosh)
    thumby.display.drawText(dosh_text, PANEL_X + 2, SCREEN_H - 5, 1)

def draw_time_left():
    thumby.display.drawFilledRectangle(
        PANEL_X, SCREEN_H - 14, PANEL_W, 7, 0
    )
    time_text = str(time_attack_seconds_left)
    thumby.display.drawText(time_text, PANEL_X + 2, SCREEN_H - 12, 1)

def get_selector_touched_tiles(x, y, rotation, moving):
    """
    Return all grid tiles whose pixels can be affected by the active preview
    and selector outline. For moving pieces, use the current moving_piece length
    if available; otherwise assume length 2.
    """
    coords = []
    try:
        length = 2
        if moving and moving_piece is not None:
            length = len(moving_piece)
        piece_coords = get_piece_coords_from_anchor(x, y, rotation, length)
    except Exception:
        return coords

    for cx, cy in piece_coords:
        if 0 <= cx < GRID_COLS and 0 <= cy < GRID_ROWS:
            coords.append((cx, cy))

    return coords


def draw_moving_piece_and_selector():
    # No moving piece → nothing to draw
    if moving_piece is None:
        return

    length = len(moving_piece)
    coords = get_piece_coords_from_anchor(sel_x, sel_y, sel_rotation, length)

    # Draw each tile of the moving piece
    for (cx, cy), pattern in zip(coords, moving_piece):
        if not (0 <= cx < GRID_COLS and 0 <= cy < GRID_ROWS):
            continue

        px = GRID_X + cx * CELL_SIZE
        py = GRID_Y + cy * CELL_SIZE

        # The board tile has already been repainted underneath.
        # Draw the moving piece as an overlay.
        draw_tile_border(px, py)
        draw_pattern_in_tile_at(px, py, pattern)

    # Draw selector rectangle sized for 2×1 or 3×1 piece
    draw_selector_rect_from_rotation(
        sel_x,
        sel_y,
        sel_rotation,
        _cursor_visible,
        length
    )


def render_frame(full=False):
    """
    Incremental renderer.

    `full=True` is only used for the first frame / scene restoration.
    Normal frames repaint only dirty board cells and small UI regions.
    """
    global force_full_redraw, panel_dirty, dosh_dirty, timer_dirty, overlay_dirty

    if full or force_full_redraw:
        thumby.display.fill(0)
        invalidate_all_grid()
        panel_dirty = True
        dosh_dirty = True
        timer_dirty = True
        overlay_dirty = True
        force_full_redraw = False

    # 1. Restore/repaint only board cells that actually became dirty.
    repainted_grid = draw_dirty_grid()

    # 2. Panel contents only change when the queue or panel cursor changes.
    if panel_dirty:
        draw_panel_contents()
        panel_dirty = False

    # 3. Currency text only changes after scoring/reset.
    if dosh_dirty:
        draw_dosh()
        dosh_dirty = False

    if time_attack and timer_dirty:
        draw_time_left()
        timer_dirty = False

    # 4. The moving overlay is redrawn only when it moved/blinked/changed,
    #    or when one of the underlying cells had to be repainted.
    if not piece_on_panel and moving_piece is not None:
        current_overlay = set(
            get_selector_touched_tiles(
                sel_x, sel_y, sel_rotation, moving=True
            )
        )
        if overlay_dirty or current_overlay.intersection(repainted_grid):
            draw_moving_piece_and_selector()
            overlay_dirty = False

    thumby.display.update()

def handle_blinking(now, for_dwarf=False):
    global _cursor_visible, _last_blink, BLINK_MS, visual_changed
    global piece_on_panel
    global sel_x, sel_y, sel_rotation, moving_piece
    global _dwarf_cursor_visible
    global unveiled_floor, unveil_end_time
    
    if time.ticks_diff(now, _last_blink) >= BLINK_MS:
        _cursor_visible = not _cursor_visible
        _last_blink = now
        visual_changed = True
        
        if for_dwarf:
            _cursor_visible = True
            _dwarf_cursor_visible = not _dwarf_cursor_visible
    
        if piece_on_panel:
            invalidate_panel()
        else:
            # Selector outline lives on the current moving-piece footprint.
            invalidate_grid_coords(
                get_selector_touched_tiles(
                    sel_x, sel_y, sel_rotation, True #moving_piece is not None
                ),
                current_floor_index
            )
            invalidate_overlay()
    
    if unveil_end_time != 0 and time.ticks_diff(now, unveil_end_time) >= 0:
            unveiled_floor = -1
            unveil_end_time = 0
            invalidate_all_grid()

def get_level_threshold(lvl):
    # Level 1 → 2: 3 points
    # Level 2 → 3: 6 points
    # Level 3 → 4: 15 points
    # Level 4 → 5: 25 points
    # Level 5 → 6: 40 points
    # Level 6 → 7: 60 points (1.5 × previous)
    
    new_lvl = lvl + 1
    
    if new_lvl == 2:
        return 3
    elif new_lvl == 3:
        return 8
    elif new_lvl == 4:
        return 24
    elif new_lvl == 5:
        return 55
    elif new_lvl == 6:
        return 80
    else:
        # new_lvl >= 7
        return int(get_level_threshold(lvl - 1) * 1.5)

def apply_scoring(cleared_count):
    global points, dosh, combo, level

    if cleared_count <= 1:
        # No scoring, no combo
        combo = 0
        return
    elif cleared_count == 2:
        play_pair_sound()
    else:
        play_triplet_sound()

    # Base points
    base = cleared_count - 1

    # Combo system active from level 3+ or in Time Attack
    if level >= 3 or time_attack or diet_mode is not None:
        bonus = combo
    else:
        bonus = 0

    gained = base + bonus

    points += gained
    dosh += gained
    invalidate_dosh()

    # Update combo
    if level >= 3 or time_attack or diet_mode is not None:
        combo += 1
        if combo > 5: # limiting combo to 5
            combo = 5
    else:
        combo = 0

def _text_pixel_width(text, font_char_width):
    return len(text) * font_char_width

def draw_down_triangle():
    # Draw a small filled downward triangle centered in the reserved area
    cx = SCREEN_W // 2
    # triangle rows (top -> bottom)
    top = SCREEN_H - 5   # top row of triangle
    mid = SCREEN_H - 4
    bot = SCREEN_H - 3   # tip of triangle
    # top row (two pixels)
    thumby.display.setPixel(cx - 1, top, 1)
    thumby.display.setPixel(cx + 1, top, 1)
    # middle row (one pixel centered)
    thumby.display.setPixel(cx, mid, 1)
    # bottom row (tip)
    thumby.display.setPixel(cx, bot, 1)

def show_scrolling_menu(title, subtitle, menu_text, on_buy, on_decline):
    """
    Shared scrolling menu for upgrade screens.

    title: string (e.g., "Good!")
    subtitle: string (e.g., "Level 2")
    menu_text: string with explicit newlines to preserve paragraphs
    on_buy: callable executed when user presses A after scrolling to end
    on_decline: callable executed when user presses B after scrolling to end
    """
    # Use the 5x7 font for the upgrade screens
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

    # --- Centered title ---
    title_w = len(title) * 6
    title_x = max(0, (SCREEN_W - title_w) // 2)
    title_y = max(0, (SCREEN_H - 7) // 2) - 8
    
    subtitle_w = len(subtitle) * 6
    subtitle_x = max(0, (SCREEN_W - subtitle_w) // 2)
    subtitle_y = max(0, (SCREEN_H - 7) // 2)

    # Show title and wait for A to continue (same as original)
    thumby.display.fill(0)
    thumby.display.drawText(title, title_x, title_y, 1)
    thumby.display.drawText(subtitle, subtitle_x, subtitle_y, 1)
    thumby.display.update()
    if "Level" in subtitle:
        time.sleep_ms(500)
        play_level_sound()
    
    if "out of space" in subtitle:
        time.sleep_ms(500)
        play_game_over_sound()
    
    while True:
        thumby.display.fill(0)
        thumby.display.drawText(title, title_x, title_y, 1)
        thumby.display.drawText(subtitle, subtitle_x, subtitle_y, 1)
        thumby.display.update()

        if just_pressed(thumby.buttonA):
            time.sleep_ms(120)
            break
        time.sleep_ms(30)

    # Layout parameters (shared)
    margin = 5
    max_text_width = SCREEN_W - margin * 2
    font_char_width = 6
    line_height = 8  # 7 px font height + 1 px spacing

    # Build wrapped lines preserving paragraph breaks
    paragraphs = menu_text.split("\n")
    wrapped_lines = []
    for p in paragraphs:
        if p.strip() == "":
            wrapped_lines.append(("", margin))
            continue
        words = p.split()
        cur = words[0] if words else ""
        for w in words[1:]:
            candidate = cur + " " + w
            if len(candidate) * font_char_width <= max_text_width:
                cur = candidate
            else:
                wrapped_lines.append((cur, margin))
                cur = w
        wrapped_lines.append((cur, margin))

    # Stack lines top-down and compute positions
    lines_with_pos = []
    y = 2
    for text, x in wrapped_lines:
        lines_with_pos.append((text, x, y))
        y += line_height

    content_top = lines_with_pos[0][2] if lines_with_pos else 0
    content_bottom = lines_with_pos[-1][2] + line_height if lines_with_pos else 0
    content_height = content_bottom - content_top

    reserved_height = 5
    content_area_height = SCREEN_H - reserved_height

    # Scrolling setup (in pixels)
    scroll = 0
    max_scroll = max(0, content_height - content_area_height)
    scroll_step = int(line_height * 2.7)

    # Main menu loop with scrolling and selection
    while True:
        thumby.display.fill(0)

        for text, x, base_y in lines_with_pos:
            y_on_screen = base_y - scroll
            if -line_height < y_on_screen < content_area_height:
                thumby.display.drawText(text, x, y_on_screen, 1)

        if scroll < max_scroll:
            thumby.display.drawFilledRectangle(0, SCREEN_H - 8, SCREEN_W, 8, 0)
            draw_down_triangle()

        thumby.display.update()

        # Scroll down
        if just_pressed(thumby.buttonD):
            if scroll < max_scroll:
                scroll = min(max_scroll, scroll + scroll_step)
                time.sleep_ms(120)
        
        #Scroll down down down
        if just_pressed(thumby.buttonR):
            scroll = max_scroll
            time.sleep_ms(120)

        # Scroll up
        if just_pressed(thumby.buttonU):
            if scroll > 0:
                scroll = max(0, scroll - scroll_step)
                time.sleep_ms(120)

        if scroll == max_scroll:
            # Buy (A) or Decline (B)
            if just_pressed(thumby.buttonA):
                on_buy()
                time.sleep_ms(120)
                break

            if just_pressed(thumby.buttonB):
                on_decline()
                time.sleep_ms(120)
                break

        time.sleep_ms(30)

    # Restore the small font used by the main game
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

def wrap_menu_item(text, max_chars=10):
    """Wrap a menu label onto multiple lines (10 chars fits after '> ' on 72px with 5x7 font)."""
    words = text.split()
    if not words:
        return [""]
    lines = []
    cur = ""
    for w in words:
        if cur == "":
            while len(w) > max_chars:
                lines.append(w[:max_chars])
                w = w[max_chars:]
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur += " " + w
        else:
            lines.append(cur)
            while len(w) > max_chars:
                lines.append(w[:max_chars])
                w = w[max_chars:]
            cur = w
    if cur != "":
        lines.append(cur)
    return lines


def show_menu(items, allow_back=True, cursor=0, title=None, blank_lines=False):
    """
    Shared scrollable menu with line wrapping.
    Returns the selected item index on A, or -1 on B (if allow_back is True).
    """
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

    # Build wrapped display lines and track each item's start/end line index
    display_lines = []  # (item_idx, text, is_first_line)
    item_ranges = []    # (start_line, end_line)

    for idx, item in enumerate(items):
        wrapped = wrap_menu_item(item)
        start_line = len(display_lines)
        for line_i, line_text in enumerate(wrapped):
            display_lines.append((idx, line_text, line_i == 0))
        end_line = len(display_lines) - 1
        item_ranges.append((start_line, end_line))
        if blank_lines and idx < len(items) - 1:
            display_lines.append((-1, "", False))

    row_h = 9
    start_row = 3 if title is not None else 0
    visible_rows = int(SCREEN_H // row_h) - start_row
    top_line = 0

    # Ensure initial cursor is visible
    if item_ranges:
        s, e = item_ranges[cursor]
        if e >= top_line + visible_rows:
            top_line = e - visible_rows + 1

    while True:
        thumby.display.fill(0)

        if title is not None:
            title_x = max(0, (SCREEN_W - len(title) * 6) // 2)
            thumby.display.drawText(title, title_x, 0, 1)

        for i in range(visible_rows):
            line_idx = top_line + i
            if line_idx >= len(display_lines):
                break
            item_idx, text, is_first = display_lines[line_idx]
            if item_idx == -1:
                continue
            prefix = "> " if (is_first and item_idx == cursor) else "  "
            thumby.display.drawText(prefix + text, 0, (i + start_row) * row_h, 1)

        thumby.display.update()

        if just_pressed(thumby.buttonU):
            if cursor > 0:
                cursor -= 1
                start_line, _ = item_ranges[cursor]
                if start_line < top_line:
                    top_line = start_line
            time.sleep_ms(120)

        if just_pressed(thumby.buttonD):
            if cursor < len(items) - 1:
                cursor += 1
                _, end_line = item_ranges[cursor]
                if end_line >= top_line + visible_rows:
                    top_line = end_line - visible_rows + 1
            time.sleep_ms(120)

        if just_pressed(thumby.buttonA) or just_pressed(thumby.buttonR):
            time.sleep_ms(120)
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            return cursor

        if allow_back and (just_pressed(thumby.buttonB) or just_pressed(thumby.buttonL)):
            time.sleep_ms(120)
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            return -1

        time.sleep_ms(30)


# --- Dwarf market view -----------------------------------------------------
def show_dwarf_market():
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

    dwarfs = []
    dwarfs_names = [
        "","","","","","",
        "Repeating",
        "Swapping",
        "", # joker
        "Removing",
        "", # third floor
        "Clean",
        "Unveiling"
    ]

    for x in [6, 7, 9, 11, 12]: #which upgrades are dwarfs
        if list_of_upgrades[x]:
            dwarfs.append(dwarfs_names[x])

    # If no dwarfs -> show simple static screen
    if len(dwarfs) == 0:
        while True:
            thumby.display.fill(0)
            thumby.display.drawText("> Soon...", 0, 0, 1)
            thumby.display.update()

            if just_pressed(thumby.buttonB):
                time.sleep_ms(120)
                thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
                return
    
    if level >= 19:
        while True:
            thumby.display.fill(0)
            thumby.display.drawText("> Striking", 0, 0, 1)
            thumby.display.drawText("...", 50, 7, 1)
            thumby.display.update()

            if just_pressed(thumby.buttonB):
                time.sleep_ms(120)
                thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
                return

            time.sleep_ms(30)

    selected = show_menu(dwarfs, allow_back=True)
    if selected != -1:
        upgrade_index = dwarfs_names.index(dwarfs[selected])
        show_dwarf_description(upgrade_index)

# ---------------------------------------------------------
# Grubol menu (intro)
# ---------------------------------------------------------
def grubol_menu():
    
    ### INSTRUCTIONS
    thumby.display.drawText("Match", 8, 6, 1)
    thumby.display.drawText("tiles", 8, 15, 1)
    thumby.display.drawText("with A", 8, 24, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("Buy", 8, 6, 1)
    thumby.display.drawText("upgrades", 8, 15, 1)
    thumby.display.drawText("to win", 8, 24, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    ### END OF INSTRUCTIONS
    
    # BITMAP: width: 72, height: 80
    grubol_bitmap = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,191,191,191,191,191,191,191,63,127,127,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,7,243,249,254,254,254,255,247,127,255,255,255,239,255,255,255,255,254,248,227,15,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,191,191,191,191,176,175,159,63,127,127,255,255,255,254,254,255,255,255,255,255,255,255,127,31,192,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,207,231,251,251,251,251,251,251,243,103,31,159,239,231,243,249,252,254,255,255,255,255,255,255,255,255,255,255,255,255,254,254,254,252,253,253,253,253,253,253,253,252,254,254,252,243,135,63,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,223,223,232,227,231,207,31,127,143,231,243,252,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,248,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,253,253,253,253,253,252,226,136,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,15,224,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,4,241,239,223,63,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,191,191,223,207,199,195,89,222,222,193,
           239,239,239,223,223,223,223,223,223,223,223,223,223,223,223,223,191,191,191,191,191,191,191,63,63,63,63,63,31,127,124,1,127,255,255,254,124,189,205,241,251,251,251,247,247,247,247,119,55,151,199,231,231,247,243,251,253,253,126,126,63,223,231,247,251,249,253,254,254,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,131,184,190,190,191,191,191,191,191,159,223,111,143,197,225,241,228,239,207,63,127,127,191,159,231,243,249,252,253,253,253,253,253,253,253,254,254,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,252,243,247,231,207,223,223,223,220,220,193,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
    
    # BITMAP: width: 72, height: 80
    grubol_inverted_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,64,64,64,64,64,64,64,192,128,128,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,248,12,6,1,1,1,0,8,128,0,0,0,16,0,0,0,0,1,7,28,240,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,64,64,64,64,79,80,96,192,128,128,0,0,0,1,1,0,0,0,0,0,0,0,128,224,63,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,48,24,4,4,4,4,4,4,12,152,224,96,16,24,12,6,3,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,3,2,2,2,2,2,2,2,3,1,1,3,12,120,192,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,32,32,23,28,24,48,224,128,112,24,12,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,2,2,2,2,3,29,119,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,240,31,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,251,14,16,32,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,64,64,32,48,56,60,166,33,33,62,
           16,16,16,32,32,32,32,32,32,32,32,32,32,32,32,32,64,64,64,64,64,64,64,192,192,192,192,192,224,128,131,254,128,0,0,1,131,66,50,14,4,4,4,8,8,8,8,136,200,104,56,24,24,8,12,4,2,2,129,129,192,32,24,8,4,6,2,1,1,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,124,71,65,65,64,64,64,64,64,96,32,144,112,58,30,14,27,16,48,192,128,128,64,96,24,12,6,3,2,2,2,2,2,2,2,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,3,12,8,24,48,32,32,32,35,35,62,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    for i in range(41):
        grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_bitmap, 0, 0-40+i)
        
        thumby.display.fill(0)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.update()
        time.sleep(0.02)
    
    time.sleep(0.5)
    thumby.display.drawText("Grubol 7", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Grubol 7", 2, 2, 0)
    thumby.display.drawText("PieRog", 8, 11, 0)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press A", 4, 5, 0)
    #thumby.display.drawText("to start", 2, 11, 0)
    thumby.display.drawText("to start", 2, 14, 0)
    thumby.display.update()
    time.sleep(0.5)
    grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_inverted_bitmap, 0, 0)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press A", 4, 5, 1)
    #thumby.display.drawText("to start", 2, 11, 1)
    thumby.display.drawText("to start", 2, 14, 1)
    thumby.display.update()
    time.sleep(0.5)
    while True:
        if just_pressed(thumby.buttonA):
            break

# --- Main menu -------------------------------------------------------------
def show_main_menu():
    
    # Structure
    '''
    Classic
    Non-classic
    
    -- Classic
    ---- Beginner
    ---- Expert (start from lvl 4)
    ---- Cheater ($9999 from start)
    
    -- Non-classic
    Dwarfless
    Time attack 0:40 (7 symbols)
    Diet
    
    ---- Diet
    Utopia chill (only 2-square pieces, 4 symbols)
    Total chill (only 2-square pieces, 7 symbols)
    Netflix & chill (7 symbols)
    Red hot chill (11 symbols)
    Endless winter chill (only 3-square pieces, 11 symbols)
    '''

    global level, points, dosh
    global dwarfless
    
    root_items = ["Classic", "Bonus"]
    classic_items = ["Beginner", "Expert", "Cheater"]
    bonus_items = ["Dwarfless", "Time attack", "Diet"]
    diet_items = [
        "Utopia chill",
        "Total chill",
        "Netflix & chill",
        "Red hot chill",
        "Endless winter chill"
    ]

    root_cursor = 0
    while True:
        choice = show_menu(
            root_items,
            allow_back=False,
            cursor=root_cursor,
            title="Game modes",
            blank_lines=True
        )
        root_cursor = choice

        if choice == 0:  # Classic
            classic_cursor = 0
            while True:
                c_choice = show_menu(classic_items, allow_back=True, cursor=classic_cursor, blank_lines=True)
                if c_choice == -1:  # B -> back to root
                    break
                classic_cursor = c_choice
                if c_choice == 0:   # Beginner -> launch game
                    return
                elif c_choice == 1: # Expert
                    level = 4
                    points = get_level_threshold(3)
                    dosh = 25
                    list_of_upgrades[2] = True  # Rotation
                    list_of_upgrades[3] = True  # Combo
                    list_of_upgrades[4] = True  # Dwarf market
                    return
                elif c_choice == 2: # Cheater
                    dosh = 9999
                    return

        elif choice == 1:  # Bonus
            bonus_cursor = 0
            while True:
                b_choice = show_menu(bonus_items, allow_back=True, cursor=bonus_cursor, blank_lines=True)
                if b_choice == -1:  # B -> back to root
                    break
                bonus_cursor = b_choice
                if b_choice == 0:   # Dwarfless
                    dwarfless = True
                    return
                elif b_choice == 1: # Time attack
                    start_time_attack()
                    return
                elif b_choice == 2: # Diet
                    diet_cursor = 0
                    while True:
                        d_choice = show_menu(diet_items, allow_back=True, cursor=diet_cursor, blank_lines=True)
                        if d_choice == -1:  # B -> back to Bonus
                            break
                        diet_cursor = d_choice
                        start_diet(d_choice)
                        return

def show_dwarf_description(upgrade_index):
    dwarf_description = ""
    
    def not_enough_dosh():
        show_scrolling_menu(
            "You've got:", "$ " + str(dosh),
            "Earn a bit more and come back later.",
            decline,
            decline
        )
            
    
    def decline():
        return
    
    if upgrade_index == 6:
        dwarf_name = "Repeating"
        description_text = """
        If you hire him, your current tile
        will get replaced by a new one.
        The new one will be assigned randomly.
        """
        cost = 20
        
        def buy():
            global dosh
            if dosh >= cost:
                dosh -= cost
                apply_repeating_dwarf()
            else: # if you're poor
                not_enough_dosh()
                
    elif upgrade_index == 7:
        dwarf_name = "Swapping"
        description_text = """
        If you hire him, you will select one of
        the fields, press A to select it,
        then you'll press up/ down/ left/ right
        to swap it with its up/ down/ left/ right neighbour.
        """
        cost = 50
        
        def buy():
            global dosh
            if dosh >= cost:
                dosh -= cost
                apply_swapping_dwarf(cost)
            else: # if you're poor
                not_enough_dosh()
    
    elif upgrade_index == 9:
        dwarf_name = "Removing"
        description_text = """
        If you hire him, you will select one of
        the fields by pressing A.
        The field will become empty.
        """
        cost = 100
        
        def buy():
            global dosh
            if dosh >= cost:
                dosh -= cost
                apply_removing_dwarf(cost)
            else: # if you're poor
                not_enough_dosh()
    
    elif upgrade_index == 11:
        dwarf_name = "Clean"
        description_text = """
        If you hire him, all the fields
        on the current floor
        will become empty.
        """
        cost = 1000
        
        def buy():
            global dosh
            if dosh >= cost:
                dosh -= cost
                apply_clean_dwarf()
            else: # if you're poor
                not_enough_dosh()
    
    elif upgrade_index == 12:
        dwarf_name = "Unveiling"
        description_text = """
        If you hire him, all the fields
        on the current floor will be
        uncovered for a moment.
        """
        cost = 10 * level

        def buy():
            global dosh
            if dosh >= cost:
                dosh -= cost
                apply_unveiling_dwarf()
            else: # if you're poor
                not_enough_dosh()
    
    cost_text = str(cost)
    compound_description_text = description_text + "\n\nA Buy for $" + cost_text + "\nB Decline"
    show_scrolling_menu(
        dwarf_name, "dwarf",
        compound_description_text,
        buy,
        decline
    )
                
def apply_repeating_dwarf():
    global active_piece, moving_piece
    if piece_on_panel:
        active_piece = pick_random_piece()
    else:
        moving_piece = pick_random_piece()

def select_one_field():
    # Draw board
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            draw_tile(x, y, boards[current_floor_index][y][x])

    # Draw panel using your existing code
    draw_panel_contents()
    
    draw_dosh()
    
    # Draw selector highlight (1x1)
    draw_selector_rect_from_rotation(sel_x, sel_y, 0, _dwarf_cursor_visible, length=1)
    
    thumby.display.update()

    handle_basic_selector_movement()
    handle_blinking(time.ticks_ms(), for_dwarf=True)

def select_new_cover():
    global boards_covered
    
    if level < 12: # without covering
        return
    else:
        if level == 12:
            p = 0.01
        elif level == 13:
            p = 0.02
        elif level == 14:
            p = 0.05
        elif level == 15:
            p = 0.1
        elif level == 16:
            p = 0.3
        elif level == 17:
            p = 0.5
        else: # level >= 18
            p = 1
        
        for z in range(3):
            if z == unveiled_floor and unveil_end_time != 0:
                """
                boards_covered[unveiled_floor] stays untouched
                while the unveiling dwarf's effect is active,
                so the exact same coverage returns
                when the timer runs out.
                """
                continue
            for y in range(GRID_ROWS):
                for x in range(GRID_COLS):
                    rand_num = random.random()
                    
                    if rand_num < p:
                        boards_covered[z][y][x] = True
                    else:
                        boards_covered[z][y][x] = False
        invalidate_all_grid()
        return
        
def apply_swapping_dwarf(cost):
    """
    Lets the player select a tile on the current floor and swap it with a neighbour.
    Uses A to select, then U/D/L/R to choose swap direction.
    Works even if neighbour or selected tile is empty (-1).
    """

    global sel_x, sel_y, overlay_dirty
    global dosh, _dwarf_cursor_visible
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    invalidate_overlay()

    # --- STEP 1: SELECT TILE ---
    selecting = True
    while selecting:
        thumby.display.fill(0)

        select_one_field()
        
        if thumby.buttonB.justPressed(): # cancel
            dosh += cost
            return
            
        if just_pressed(thumby.buttonA):
            selecting = False

        time.sleep_ms(50)

    sx, sy = sel_x, sel_y

    # --- STEP 2: WAIT FOR DIRECTION TO SWAP ---
    waiting_for_direction = True
    while waiting_for_direction:
        thumby.display.fill(0)

        # Draw board
        for y in range(GRID_ROWS):
            for x in range(GRID_COLS):
                draw_tile(x, y, boards[current_floor_index][y][x])

        # Draw panel
        draw_panel_contents()
        
        draw_dosh()

        # Highlight selected tile
        draw_selector_rect_from_rotation(sx, sy, 0, True, length=1)

        thumby.display.update()

        dx = dy = 0
        if thumby.buttonB.justPressed(): # cancel
            dosh += cost
            waiting_for_direction = False
        elif thumby.buttonU.justPressed():
            dy = -1
        elif thumby.buttonD.justPressed():
            dy = 1
        elif thumby.buttonL.justPressed():
            dx = -1
        elif thumby.buttonR.justPressed():
            dx = 1

        if dx != 0 or dy != 0:
            nx = sx + dx
            ny = sy + dy

            if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                # Swap tiles
                boards[current_floor_index][sy][sx], boards[current_floor_index][ny][nx] = \
                    boards[current_floor_index][ny][nx], boards[current_floor_index][sy][sx]

                invalidate_grid_coords([(sx, sy), (nx, ny)], current_floor_index)
                overlay_dirty = True

            waiting_for_direction = False

        time.sleep_ms(50)

    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    clamp_selector()
    invalidate_overlay()
    
def apply_removing_dwarf(cost):
    global dosh, boards
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    invalidate_overlay()
    
    chosen = False

    while not chosen:
        thumby.display.fill(0)

        select_one_field()
        
        if thumby.buttonB.justPressed(): # cancel
            dosh += cost
            chosen = True

        if just_pressed(thumby.buttonA):
            sx, sy = sel_x, sel_y
            
            boards[current_floor_index][sy][sx] = -1 # -1 = empty
        
            chosen = True

        time.sleep_ms(50)

    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    clamp_selector()
    invalidate_overlay()

def apply_clean_dwarf():
    global boards
    global available_spaces, available_spaces_old
    
    boards[current_floor_index] = [[-1] * 4 for _ in range(4)]
    
    available_spaces = 16
    available_spaces_old = 16
    invalidate_all_grid()

def apply_unveiling_dwarf():
    global unveiled_floor, unveil_end_time

    unveiled_floor = current_floor_index
    unveil_end_time = time.ticks_add(time.ticks_ms(), UNVEIL_DURATION_MS)
    invalidate_all_grid()
    
def handle_basic_selector_movement():
    global sel_x, sel_y

    if thumby.buttonU.pressed():
        sel_y -= 1
    elif thumby.buttonD.pressed():
        sel_y += 1
    elif thumby.buttonL.pressed():
        sel_x -= 1
    elif thumby.buttonR.pressed():
        sel_x += 1

    # clamp inside board
    if sel_x < 0: sel_x = 0
    if sel_x >= GRID_COLS: sel_x = GRID_COLS - 1
    if sel_y < 0:
        sel_y = 0
        change_floors("U")
    if sel_y >= GRID_ROWS:
        sel_y = GRID_ROWS - 1
        change_floors("D")


def change_floors(direction):
    global current_floor_index, changing_floors_locked
    
    if changing_floors_locked:
        return

    if direction == "U":
        if current_floor_index < len(boards) - 1:
            current_floor_index += 1
            invalidate_all()

    elif direction == "D":
        if current_floor_index > 0:
            current_floor_index -= 1
            invalidate_all()

def start_time_attack():
    global time_attack, time_attack_seconds_left, time_attack_start_time
    global timer_dirty, active_piece, next_piece

    clear_boards(show_intro=False, open_menu=False)
    time_attack = True
    list_of_upgrades[2] = True  # Rotation
    list_of_upgrades[3] = True  # Combo

    # Regenerate starting pieces using Time Attack's 6 symbols and 2-tile rule
    active_piece = pick_random_piece()
    next_piece = pick_random_piece()

    time_attack_seconds_left = TIME_ATTACK_DURATION_S
    time_attack_start_time = time.ticks_ms()
    timer_dirty = True


def handle_time_attack(now):
    global time_attack_seconds_left, timer_dirty

    elapsed = time.ticks_diff(now, time_attack_start_time)
    new_seconds = max(0, TIME_ATTACK_DURATION_S - (elapsed // 1000))

    if new_seconds != time_attack_seconds_left:
        time_attack_seconds_left = new_seconds
        timer_dirty = True
        if time_attack_seconds_left == 0:
            render_frame()
            time.sleep_ms(300)
            show_time_attack_game_over()


def show_time_attack_game_over():
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)

    thumby.display.fill(0)
    if time_attack:
        thumby.display.drawText("Score: $ " + str(dosh), 0, 4, 1)
    else:
        thumby.display.drawText("Score: $" + str(dosh), 0, 4, 1)
    thumby.display.drawText("A Play again", 0, 18, 1)
    thumby.display.drawText("B Main menu", 0, 28, 1)
    thumby.display.update()
    time.sleep(1.0)

    # Wait for any held A/B release before accepting input
    if not time_attack:
        play_game_over_sound()
    while thumby.buttonA.pressed() or thumby.buttonB.pressed():
        time.sleep_ms(30)
    just_pressed(thumby.buttonA)
    just_pressed(thumby.buttonB)

    while True:
        if just_pressed(thumby.buttonA):
            time.sleep_ms(120)
            if time_attack:
                start_time_attack()
            else:
                start_diet(diet_mode)
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            invalidate_all()
            render_frame(full=True)
            return

        if just_pressed(thumby.buttonB):
            time.sleep_ms(120)
            clear_boards(show_intro=True, open_menu=True)
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            invalidate_all()
            render_frame(full=True)
            return

        time.sleep_ms(30)

def start_diet(mode):
    global diet_mode, active_piece, next_piece

    clear_boards(show_intro=False, open_menu=False)
    diet_mode = mode
    list_of_upgrades[2] = True  # Rotation
    list_of_upgrades[3] = True  # Combo

    # Regenerate starting pieces using the chosen diet mode's rules
    active_piece = pick_random_piece()
    next_piece = pick_random_piece()

def main():
    global _last_blink, _cursor_visible, sel_x, sel_y, _last_move
    global active_piece, next_piece
    global moving_piece, piece_on_panel, sel_rotation
    global panel_dirty, dosh_dirty, overlay_dirty
    global A_down_time, A_hold_reported

    # Initial queue (ensure different shapes in each piece).
    active_piece = pick_random_piece()
    next_piece = pick_random_piece()

    moving_piece = None
    piece_on_panel = True
    sel_rotation = 0
    
    correct_bitmaps()
    
    grubol_menu()
    show_main_menu()

    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

    # First frame is the only normal-game full-screen clear.
    render_frame(full=True)

    while True:
        now = time.ticks_ms()
        visual_changed = False
        
        handle_blinking(now)
        handle_input(now)
        if time_attack:
            handle_time_attack(now)

        # Even when there was no explicit state change, the blink state may
        # have dirtied the small cursor region. render_frame() therefore
        # checks the dirty flags rather than relying on this boolean.
        render_frame()
        time.sleep_ms(30)


main()