import thumby
import urandom
import time

thumby.display.setFPS(30)

keyboard = [
    list("QWERTYUIOP"),
    list("ASDFGHJKL"),
    list("ZXCVBNM")
]

KEY_W = 12
KEY_H = 16
SPACING = 2

# BITMAP: width: 72, height: 40
up_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,192,248,56,56,12,12,56,56,248,192,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,192,248,56,60,15,7,7,1,0,0,0,0,0,0,1,7,7,15,60,56,248,192,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,14,15,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,3,15,14,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
           
# BITMAP: width: 72, height: 40
down_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,112,240,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,240,112,112,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,31,28,60,240,224,224,128,0,0,0,0,0,0,128,224,224,240,60,28,31,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,31,28,28,48,48,28,28,31,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
           
# BITMAP: width: 72, height: 40
left_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,224,224,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,224,224,248,56,62,14,15,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,127,115,243,192,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,7,7,31,28,124,112,240,192,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# BITMAP: width: 72, height: 40
right_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,224,224,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,15,14,62,56,248,224,224,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,192,243,115,127,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,192,240,112,124,28,31,7,7,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# BITMAP: width: 72, height: 40
a_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

arrowUpSprite = thumby.Sprite(72, 40, up_bitmap)
arrowDownSprite = thumby.Sprite(72, 40, down_bitmap)
arrowLeftSprite = thumby.Sprite(72, 40, left_bitmap)
arrowRightSprite = thumby.Sprite(72, 40, right_bitmap)
buttonASprite = thumby.Sprite(72, 40, a_bitmap)

# Starting selection
sel_row = 0
sel_col = 0

# Camera position
camX = 0
camY = 0

# Menu controls
menu_active = True
digit_left = 0
digit_right = 0
selected_digit = 1 # 0 = left, 1 = right
tutorialMode = True

words = [
    "QWE", #0
    "QAW",
    "QEW",
    "SEQ",
    "DEAQ",
    "QWXD",
    "SEXS",
    "WEZD",
    "XDXD",
    "XEAZXESWEZ", #9
    "CASE",
    "DESC",
    "WAXED",
    "CAVES",
    "SAVED",
    "WAVES",
    "SCARE",
    "CEASE",
    "CZESC",
    "QEACWDQXAW", #19
    "FREAD",
    "SEEFS",
    "WEARS",
    "FEARZ",
    "READX",
    "ZERCE",
    "QEESV",
    "VEAFE",
    "RZECZ",
    "RZVWFECQXF", #29
    "TEARS",
    "BETSA",
    "DEGREE",
    "EAGER",
    "BADDEST",
    "SWABZ",
    "WAGES",
    "SETTER",
    "GRACZE",
    "BSTXVQGXWV", #39
    "NEARER",
    "SHEARS",
    "RHYTHQ",
    "VEXERS",
    "REHAB",
    "READY",
    "HYENA",
    "WHENQY",
    "CHARACZ",
    "NSHXQNZYDT", #49
    "FRERES",
    "GAFFES",
    "GERERAS",
    "REVES",
    "BANGER",
    "EXERCER",
    "GRAVE",
    "NETTES",
    "CENSE",
    "RASCENDANT", #59
    "MUETS",
    "FAMUZ",
    "RUXAXZ",
    "BRANDJYX",
    "MAJEUR",
    "MENENT",
    "RAVABAR",
    "NEWJERSEY",
    "MATEMATYCZNY",
    "URDADMFUNXER", #69
    "QXJZYFRC",
    "FANTASMA",
    "BENVEDERE",
    "DURAREBBE",
    "MAREMMASANTA",
    "SBUCCARE",
    "AVENAEQC",
    "SARACEN",
    "MURMURANTE",
    "TRASTEVERE", #79
    "CHILIPEPPER"
    "PAMPUCHY",
    "PANZARELLA",
    "SHENANIGANS",
    "ZDRAVSTVUJTE",
    "NIESZCZESCIE",
    "RONALDINHO",
    "GRUBOLE",
    "MUSINILIPONA",
    "CHIZHIYIHENG", #89
    "ELOKESZULET",
    "KERESZTENY",
    "FUGGETLENUL",
    "TITKOSUGYNOK",
    "GYURUKURA",
    "EGESZSEGUGYI",
    "SZEMELYISEG",
    "ABCDEFGHIJKL",
    "MNOPQRSTUVW",
    "XYZ"
    ]


def get_key_position(r, c):
    """Return the world-space (x,y) of the top-left corner of a key."""
    row = keyboard[r]
    row_width = len(row) * (KEY_W + SPACING)

    # Base centered X
    x = -(row_width // 2)

    # Apply row-specific horizontal offsets
    if r == 2:  # third row (Z row)
        x -= (KEY_W + SPACING) // 2   # shift left by half a key

    # Add column offset
    x += c * (KEY_W + SPACING)

    # Vertical position
    y = r * (KEY_H + SPACING)

    return x, y

def update_camera():
    global camX, camY
    
    if tutorialMode:
        # Center camera on selected key
        kx, ky = get_key_position(sel_row, sel_col)
        camX = kx + KEY_W//2 - 72//2
        camY = ky + KEY_H//2 - 40//2
    
    # Keyboard bounding box in world space
    minX = -100
    maxX = 300
    minY = -100
    maxY = 300
    
    camX = max(minX, min(maxX, camX))
    camY = max(minY, min(maxY, camY))


def draw_keyboard():
    if not keyboardVisible:
        return  # Skip drawing entirely

    for r, row in enumerate(keyboard):
        for c, letter in enumerate(row):
            kx, ky = get_key_position(r, c)

            # Convert world ’ screen
            sx = int(kx - camX)
            sy = int(ky - camY)

            # Draw key box
            thumby.display.drawRectangle(sx, sy, KEY_W, KEY_H, 1)

            # Highlight selected key
            if tutorialMode and r == sel_row and c == sel_col:
                thumby.display.drawRectangle(sx-2, sy-2, KEY_W+4, KEY_H+4, 1)

            # Draw letter centered
            thumby.display.drawText(letter, sx + KEY_W//2 - 3, sy + KEY_H//2 - 3, 1)

def teleport_random():
    global sel_row, sel_col
    sel_row = urandom.getrandbits(8) % len(keyboard)
    sel_col = urandom.getrandbits(8) % len(keyboard[sel_row])

def flash_sprite(sprite):
    # Clear screen
    thumby.display.fill(0)

    # Draw sprite at (0,0) because it's full-screen
    thumby.display.drawSprite(sprite)
    thumby.display.update()

    # Hold for 0.2 seconds
    time.sleep(0.2)

def draw_menu():
    thumby.display.fill(0)

    # Use a larger builtin font

    thumby.display.drawText("Lvl (00-99)", 5, 2, 1)
    
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)

    # Center of screen
    x_center = 72 // 2
    y_center = 40 // 2

    # Digit positions (closer together)
    left_x  = x_center - 10
    right_x = x_center + 2
    digit_y = y_center - 4

    # Draw digits in large font
    thumby.display.drawText(str(digit_left),  left_x,  digit_y, 1)
    thumby.display.drawText(str(digit_right), right_x, digit_y, 1)

    # Restore default font for the rest of the game
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    # on the right
    thumby.display.drawText(str(digit_left),  left_x + 30,  digit_y + 2, 1)
    thumby.display.drawText(str((digit_right + 1) % 10), left_x + 38, digit_y + 2, 1)
    
    # underneath
    thumby.display.drawText(str((digit_left + 1) % 10),  left_x + 4,  digit_y + 14, 1)
    thumby.display.drawText(str(digit_right), left_x + 12, digit_y + 14, 1)
    
    # underneath to the right
    thumby.display.drawText(str((digit_left + 1) % 10),  left_x + 30,  digit_y + 14, 1)
    thumby.display.drawText(str((digit_right + 1) % 10), left_x + 38, digit_y + 14, 1)
    
    thumby.display.update()
    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)


def show_level_number(level_number):
    global tutorialMode
    
    thumby.display.fill(0)

    text = "Level " + str(level_number)
    x = (72 - len(text)*6) // 2   # center horizontally
    y = 40//2 - 4                 # center vertically

    thumby.display.drawText(text, x, y, 1)
    thumby.display.update()
    time.sleep(0.5)  # hold for 0.5s
    thumby.display.fill(0)
    
    text = "Password:"
    x = (72 - len(text)*6) // 2   # center horizontally
    y = 40//2 - 4                 # center vertically
    thumby.display.drawText(text, x, y, 1)
    thumby.display.update()
    time.sleep(0.5)  # hold for 0.5s
    thumby.display.fill(0)
    
    text = words[level_number]
    x = (72 - len(text)*6) // 2   # center horizontally
    y = 40//2 - 4                 # center vertically
    thumby.display.drawText(text, x, y, 1)
    thumby.display.update()
    
    while not thumby.buttonA.justPressed():
        continue
    
    if not tutorialMode or level_number == 2: # level 2 is the first obligatory blind level
        probs = 0.2
        if urandom.getrandbits(8) < int(probs * 256) or level_number == 2:
            thumby.display.fill(0)
            thumby.display.update()
            
            text = "Try blind?"
            x = (72 - len(text)*6) // 2   # center horizontally
            y = 40//2 - 4                 # center vertically
            thumby.display.drawText(text, x, y, 1)
            thumby.display.update()
            time.sleep(0.5)  # hold for 0.5s
            thumby.display.fill(0)
            
            while not thumby.buttonA.justPressed():
                continue



def run_menu():
    global menu_active, digit_left, digit_right

    while menu_active:
        draw_menu()

        # UP/DOWN ’ change left digit
        if thumby.buttonU.justPressed():
            digit_left = (digit_left - 1) % 10

        if thumby.buttonD.justPressed():
            digit_left = (digit_left + 1) % 10

        # LEFT/RIGHT ’ change right digit
        if thumby.buttonL.justPressed():
            digit_right = (digit_right - 1) % 10

        if thumby.buttonR.justPressed():
            digit_right = (digit_right + 1) % 10

        # A starts the game
        if thumby.buttonA.justPressed():
            menu_active = False
            return

def run_intro():
        
    ### INSTRUCTIONS
    thumby.display.drawText("Arrows", 10, 2, 1)
    thumby.display.drawText("to move", 10, 11, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("A to", 10, 2, 1)
    thumby.display.drawText("press", 10, 11, 1)
    thumby.display.drawText("key", 10, 20, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("B to", 10, 2, 1)
    thumby.display.drawText("show/hide", 10, 11, 1)
    thumby.display.drawText("keyboard", 10, 20, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    ### END OF INSTRUCTIONS
    
    # BITMAP: width: 72, height: 80
    grubol_bitmap = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,159,223,207,231,247,247,251,123,121,125,125,125,125,125,125,125,125,125,125,125,253,249,243,247,231,207,159,63,127,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,195,249,252,63,223,231,247,251,253,254,254,254,127,255,255,255,255,255,255,255,255,255,255,255,254,254,252,253,251,243,231,223,62,252,243,207,63,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,254,63,231,249,254,255,255,255,255,255,255,255,223,191,191,255,255,255,255,251,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,255,255,252,1,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,192,4,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,192,127,63,135,248,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,191,159,192,206,221,179,55,103,111,239,239,239,239,239,239,239,239,239,207,223,223,223,223,223,223,223,95,47,175,175,199,199,199,179,57,120,253,254,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,191,159,207,231,243,251,253,252,255,255,255,255,255,255,255,255,255,255,255,254,254,252,253,253,253,253,253,253,253,253,253,253,253,254,254,254,255,255,255,255,255,255,255,255,255,255,254,252,249,243,231,207,
           255,255,255,255,255,255,255,255,255,255,127,159,207,231,247,249,253,12,254,127,143,255,15,239,239,239,255,15,255,127,143,255,15,111,111,47,143,255,127,143,239,207,63,255,255,255,127,15,159,127,255,15,239,111,111,15,255,255,15,239,239,223,31,255,255,255,255,255,255,255,255,255,
           255,255,255,255,63,159,199,243,249,254,255,255,255,255,255,255,255,192,248,250,199,255,192,222,222,223,255,192,254,255,255,255,192,222,222,221,193,255,248,231,223,207,240,255,207,227,240,247,247,192,255,192,248,242,231,239,223,255,192,223,207,239,224,255,255,255,255,255,255,255,255,255,
           143,243,249,252,255,255,251,251,251,3,251,251,251,255,3,123,103,15,255,255,255,127,15,227,227,15,255,255,251,227,15,255,63,135,243,255,3,123,123,251,255,3,255,255,255,255,3,255,255,255,255,3,123,123,251,255,3,123,59,179,135,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,224,255,255,255,255,224,254,248,243,231,255,227,248,253,253,253,248,227,255,255,255,252,241,252,255,255,255,240,247,247,247,255,240,247,247,247,255,240,247,247,247,255,240,247,247,247,255,240,254,252,249,243,255,255,255,255,255,255,255,255,255,255,255])
    
    # BITMAP: width: 72, height: 80
    grubol_inverted_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,96,32,48,24,8,8,4,132,134,130,130,130,130,130,130,130,130,130,130,130,2,6,12,8,24,48,96,192,128,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,60,6,3,192,32,24,8,4,2,1,1,1,128,0,0,0,0,0,0,0,0,0,0,0,1,1,3,2,4,12,24,32,193,3,12,48,192,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,1,192,24,6,1,0,0,0,0,0,0,0,32,64,64,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,0,3,254,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,251,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,63,128,192,120,7,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,64,96,63,49,34,76,200,152,144,16,16,16,16,16,16,16,16,16,48,32,32,32,32,32,32,32,160,208,80,80,56,56,56,76,198,135,2,1,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,96,48,24,12,4,2,3,0,0,0,0,0,0,0,0,0,0,0,1,1,3,2,2,2,2,2,2,2,2,2,2,2,1,1,1,0,0,0,0,0,0,0,0,0,0,1,3,6,12,24,48,
           0,0,0,0,0,0,0,0,0,0,128,96,48,24,8,6,2,243,1,128,112,0,240,16,16,16,0,240,0,128,112,0,240,144,144,208,112,0,128,112,16,48,192,0,0,0,128,240,96,128,0,240,16,144,144,240,0,0,240,16,16,32,224,0,0,0,0,0,0,0,0,0,
           0,0,0,0,192,96,56,12,6,1,0,0,0,0,0,0,0,63,7,5,56,0,63,33,33,32,0,63,1,0,0,0,63,33,33,34,62,0,7,24,32,48,15,0,48,28,15,8,8,63,0,63,7,13,24,16,32,0,63,32,48,16,31,0,0,0,0,0,0,0,0,0,
           112,12,6,3,0,0,4,4,4,252,4,4,4,0,252,132,152,240,0,0,0,128,240,28,28,240,0,0,4,28,240,0,192,120,12,0,252,132,132,4,0,252,0,0,0,0,252,0,0,0,0,252,132,132,4,0,252,132,196,76,120,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,31,0,0,0,0,31,1,7,12,24,0,28,7,2,2,2,7,28,0,0,0,3,14,3,0,0,0,15,8,8,8,0,15,8,8,8,0,15,8,8,8,0,15,8,8,8,0,15,1,3,6,12,0,0,0,0,0,0,0,0,0,0,0])
    
    for i in range(41):
        grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_bitmap, 0, 0-40+i)
        
        thumby.display.fill(0)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.update()
        time.sleep(0.02)
    
    time.sleep(0.5)
    thumby.display.drawText("Grubol", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("4", 18, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Key", 4, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("board", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Travel", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("ler", 4, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press", 2, 2, 0)
    thumby.display.drawText("A to", 2, 11, 0)
    thumby.display.drawText("start", 2, 20, 0)
    thumby.display.update()
    time.sleep(0.5)
    grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_inverted_bitmap, 0, 0)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press", 2, 2, 1)
    thumby.display.drawText("A to", 2, 11, 1)
    thumby.display.drawText("start", 2, 20, 1)
    thumby.display.update()
    time.sleep(0.5)
    
    while not thumby.buttonA.justPressed():
        continue
    
##################################################

run_intro()
run_menu()

chosen_level = digit_left * 10 + digit_right
show_level_number(chosen_level)

# Keyboard visibility toggle
tutorialMode = chosen_level < 2 # only for levels 0 and 1
keyboardVisible = tutorialMode

targetWord = words[chosen_level]      # Save the first one
typed = ""                 # What the player has typed so far

while True:
    # Toggle keyboard visibility
    if thumby.buttonB.justPressed():
        keyboardVisible = not keyboardVisible

    update_camera()

    thumby.display.fill(0)
    draw_keyboard()
    if not keyboardVisible:
        thumby.display.drawText(targetWord, 1, 2, 1)
    thumby.display.update()

    # Input handling (still works even when keyboard is invisible)
    if thumby.buttonU.justPressed():
        if not (tutorialMode) and keyboardVisible:
            # Move camera only
            camY -= 10
        else:
            flash_sprite(arrowUpSprite)
            
            if sel_row > 0:
                sel_row -= 1
                sel_col = min(sel_col, len(keyboard[sel_row]) - 1)
            else:
                teleport_random()
    
    if thumby.buttonD.justPressed():
        if not (tutorialMode) and keyboardVisible:
            # Move camera only
            camY += 10
        else:
            flash_sprite(arrowDownSprite)
            
            if sel_row < len(keyboard) - 1:
                sel_row += 1
                sel_col = min(sel_col, len(keyboard[sel_row]) - 1)
            else:
                teleport_random()
    
    if thumby.buttonL.justPressed():
        if not (tutorialMode) and keyboardVisible:
            # Move camera only
            camX -= 10
        else:
            flash_sprite(arrowLeftSprite)
            
            if sel_col > 0:
                sel_col -= 1
            else:
                teleport_random()
    
    if thumby.buttonR.justPressed():
        if not (tutorialMode) and keyboardVisible:
            # Move camera only
            camX += 10
        else:
            flash_sprite(arrowRightSprite)
            
            if sel_col < len(keyboard[sel_row]) - 1:
                sel_col += 1
            else:
                teleport_random()

    if thumby.buttonA.justPressed():
        if tutorialMode or not keyboardVisible:
            thumby.audio.play(1000, 50) # short beep
            flash_sprite(buttonASprite)
            
            letter = keyboard[sel_row][sel_col]
            typed += letter
        
            if typed == targetWord:
                # Level complete ’ next level
                chosen_level = (chosen_level + 1) % len(words)
                targetWord = words[chosen_level]
                typed = ""
                sel_row = 0
                sel_col = 0
            
                # Reset tutorial mode and keyboard visibility
                tutorialMode = chosen_level < 2
                keyboardVisible = tutorialMode
            
                # Show intro again
                show_level_number(chosen_level)
            
            elif len(typed) == len(targetWord):
                # Wrong ’ restart same level
                
                # Show "Try again"
                thumby.display.fill(0)
                msg = "Try again!"
                x = (72 - len(msg)*6) // 2
                y = 40//2 - 4
                thumby.display.drawText(msg, x, y, 1)
                thumby.display.update()
                time.sleep(1.0)
                
                typed = ""
                sel_row = 0
                sel_col = 0
            
                # Reset tutorial mode and keyboard visibility
                tutorialMode = chosen_level < 2
                keyboardVisible = tutorialMode
            
                # Show intro again
                show_level_number(chosen_level)


