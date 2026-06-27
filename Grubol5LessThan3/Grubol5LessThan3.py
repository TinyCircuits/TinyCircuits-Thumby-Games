import thumby
import random
import time

thumby.display.setFPS(30)

# ---------------------------------------------------------
# Configuration: leagues are defined here for easy editing
# Each league is a dict with: name, seconds_per_number, numbers_options (list)
# ---------------------------------------------------------
LEAGUES = [
    {"name": "San Marino", "seconds_per_number": 5, "numbers_options": [3, 4, 5]},
    {"name": "Austria", "seconds_per_number": 3, "numbers_options": [3, 4, 5]},
    {"name": "Mongolia", "seconds_per_number": 3, "numbers_options": [5, 6, 7, 8, 9, 10]},
    {"name": "Australia", "seconds_per_number": 5, "numbers_options": [8, 9, 10, 11, 12, 13, 14, 15]},
    {"name": "Russia", "seconds_per_number": 3, "numbers_options": [12, 13, 14, 15, 16]},
    {"name": "N. Korea", "seconds_per_number": 2, "numbers_options": [15, 16, 17, 18, 20]},
]

# ---------------------------------------------------------
# Number class: represents a 3-digit enemy/warrior number
# ---------------------------------------------------------
class Number:
    def __init__(self, x):
        # Generate 3 random digits
        digits = [str(random.randint(0, 9)) for _ in range(3)]
        self.string = "".join(digits)
        self.value = int(self.string)
        self.x = x  # horizontal position in the world
        self.y = 5  # top of the screen

    def draw(self, offset):
        # Draw number shifted by camera offset
        thumby.display.drawText(self.string, self.x - offset, self.y, 1)

# ---------------------------------------------------------
# Timing helper: returns True after ms milliseconds have passed
# Uses a global fight_timer which is reset by caller when needed
# ---------------------------------------------------------
def step_wait(ms):
    global fight_timer
    now = time.ticks_ms()
    if fight_timer == 0:
        fight_timer = now
    return (now - fight_timer) > ms

# ---------------------------------------------------------
# Camera helper: center camera on the current fighting pair
# ---------------------------------------------------------
def center_camera_on_pair():
    global camera_x
    n = numbers[fight_index]
    # Center the number horizontally on the screen
    camera_x = n.x - (thumby.display.width // 2) + 8  # +8 shifts to center text width

# ---------------------------------------------------------
# Fight drawing helpers
# ---------------------------------------------------------
def fight_show_enemy():
    numbers[fight_index].draw(camera_x)

def fight_show_both():
    enemy = numbers[fight_index]
    warrior = confirmed_warriors[fight_index]
    enemy.draw(camera_x)
    thumby.display.drawText(warrior.string, enemy.x - camera_x, BOTTOM_ROW_HEIGHT, 1)

def fight_compare():
    global enemy_points, you_points, last_outcome
    enemy = numbers[fight_index]
    warrior = confirmed_warriors[fight_index]

    if enemy.value > warrior.value:
        enemy_points += 1
        last_outcome = 1  # enemy wins
    elif warrior.value > enemy.value:
        you_points += 1
        last_outcome = 2  # warrior wins
    else:
        # Draw: both get a point, both stay visible
        enemy_points += 1
        you_points += 1
        last_outcome = 0  # draw

def resolve_remaining_fights():
    global fight_index, fight_step, fight_timer

    # Continue resolving until all fights are done
    while fight_index < numbers_number:
        # Use the existing comparison logic
        fight_compare()

        fight_index += 1

    # Reset steps so results scene starts clean
    fight_step = 0
    fight_timer = 0

def fight_show_result():
    global transition
    enemy = numbers[fight_index]
    warrior = confirmed_warriors[fight_index]

    if last_outcome == 1:
        # Enemy wins: show only enemy
        enemy.draw(camera_x)
        if transition:
            thumby.audio.play(500, 60)
            transition = False
    elif last_outcome == 2:
        # Warrior wins: show only warrior
        thumby.display.drawText(warrior.string, enemy.x - camera_x, BOTTOM_ROW_HEIGHT, 1)
        if transition:
            thumby.audio.play(900, 60)
            transition = False
    else:
        # Draw: show both
        enemy.draw(camera_x)
        thumby.display.drawText(warrior.string, enemy.x - camera_x, BOTTOM_ROW_HEIGHT, 1)
        if transition:
            thumby.audio.play(700, 60)
            transition = False
        
# ---------------------------------------------------------
# Game constants and initial state
# ---------------------------------------------------------
START_X = 5
SCROLL_SPEED = 5
TIMER_BAR_LENGTH = 15
BOTTOM_ROW_HEIGHT = 28

# UI/menu state
scene = "grubol_menu"  # start at grubol_menu
league_index = 0        # which league is highlighted in the full list
league_visible_start = 0  # start index of the visible 3-line window (below header)
level_index = 0         # index inside chosen league's numbers_options when choosing level

# Gameplay state (will be initialized per level)
camera_x = 0
numbers = []
ordered_numbers = []
numbers_number = 3
current_warrior = 0  # horizontal index
selected_warrior = 0  # vertical index (for choosing warriors)
confirmed_warriors = []
seconds_to_memorise_one = 3
seconds_to_memorise_all = seconds_to_memorise_one * numbers_number
start_time = 0
transition = True # is this the first frame of the new screen? Needed to play sounds correctly
lets_skip = False

fight_index = 0
fight_step = 0
fight_timer = 0
enemy_points = 0
you_points = 0
last_outcome = 0  # 0 = draw, 1 = enemy wins, 2 = warrior wins
RESULT_WAIT = 1000  # 1 second

# ---------------------------------------------------------
# Helper: initialize a level from a league and a chosen number count
# Resets all gameplay variables so each run is fresh
# ---------------------------------------------------------
def init_level(league, chosen_numbers_count):
    global camera_x, numbers, ordered_numbers, numbers_number
    global current_warrior, selected_warrior, confirmed_warriors
    global seconds_to_memorise_one, seconds_to_memorise_all, start_time, transition
    global fight_index, fight_step, fight_timer, enemy_points, you_points, last_outcome

    camera_x = 0
    numbers = []
    ordered_numbers = []
    numbers_number = chosen_numbers_count
    current_warrior = 0
    selected_warrior = 0
    confirmed_warriors = []
    seconds_to_memorise_one = league["seconds_per_number"]
    seconds_to_memorise_all = seconds_to_memorise_one * numbers_number
    start_time = time.ticks_ms()
    transition = True

    fight_index = 0
    fight_step = 0
    fight_timer = 0
    enemy_points = 0
    you_points = 0
    last_outcome = 0

    # Create enemy numbers spaced horizontally
    for i in range(numbers_number):
        n = Number(START_X + i * (15 + 20))  # 15 = width of 3 digits, 20 = space
        numbers.append(n)

    ordered_numbers = sorted(numbers, key=lambda n: n.value)

# ---------------------------------------------------------
# Menu drawing: Leagues menu (header + 3 visible names)
# - First line is "Leagues"
# - Next three lines are movable names; when selection moves past the 3rd visible line,
#   the visible window scrolls down; when moving back up it scrolls up.
# ---------------------------------------------------------
def draw_leagues_menu():
    thumby.display.drawText("Leagues", 15, 0, 1)
    # three visible slots below header
    for i in range(3):
        idx = league_visible_start + i
        y = 13 + i * 8
        if idx < len(LEAGUES):
            name = LEAGUES[idx]["name"]
            # highlight the currently selected league
            if idx == league_index:
                thumby.display.drawText(">" + name, 0, y, 1)
            else:
                thumby.display.drawText(" " + name, 0, y, 1)
        else:
            thumby.display.drawText("", 0, y, 1)

# ---------------------------------------------------------
# Menu drawing: Choose level screen for a league
# Shows up to 3 options at a time (header "Choose level")
# Player can move up/down and pick any level with A
# ---------------------------------------------------------
def draw_choose_level_menu(league):
    thumby.display.drawText("Choose level", 0, 0, 1)
    options = league["numbers_options"]
    # We'll show up to 3 options centered under header; compute visible window
    # Keep level_index within bounds
    visible_start = max(0, min(level_index - 1, max(0, len(options) - 3)))
    for i in range(3):
        idx = visible_start + i
        y = 13 + i * 8
        if idx < len(options):
            label = str(options[idx]) + " nums"
            if idx == level_index:
                thumby.display.drawText(">" + label, 0, y, 1)
            else:
                thumby.display.drawText(" " + label, 0, y, 1)
        else:
            thumby.display.drawText("", 0, y, 1)

# ---------------------------------------------------------
# Grubol menu (intro)
# ---------------------------------------------------------
def grubol_menu():
    
    ### INSTRUCTIONS
    thumby.display.drawText("Memorise", 8, 6, 1)
    thumby.display.drawText("your", 8, 15, 1)
    thumby.display.drawText("enemies", 8, 24, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("Fight", 16, 6, 1)
    thumby.display.drawText("them", 16, 15, 1)
    thumby.display.drawText("with", 16, 24, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("their", 16, 6, 1)
    thumby.display.drawText("stronger", 8, 15, 1)
    thumby.display.drawText("countrparts", 4, 24, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    ### END OF INSTRUCTIONS
    
    # BITMAP: width: 72, height: 80
    grubol_bitmap = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,191,159,223,239,239,247,247,247,251,251,251,253,253,253,249,251,243,231,207,63,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,199,248,254,255,255,255,255,127,253,255,255,255,255,239,255,255,255,255,255,255,255,255,255,254,241,7,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,67,252,255,255,255,255,255,255,255,255,255,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,249,103,95,31,63,127,127,127,255,255,255,255,255,255,255,127,127,127,127,127,191,191,159,143,39,115,248,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,31,239,247,243,251,251,253,253,253,125,157,221,227,241,253,253,254,254,255,255,255,255,255,255,254,254,254,254,254,254,254,254,255,255,255,255,255,255,255,255,255,255,254,252,241,199,55,231,143,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,248,227,207,223,63,127,255,255,31,193,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,1,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,191,191,191,191,188,33,31,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,7,120,63,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,248,251,251,251,251,253,253,254,248,227,207,223,191,191,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,191,207,227,224,238,239,238,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,240,199,30,126,253,253,253,253,251,251,251,251,247,7,247,247,247,247,247,247,247,247,119,7,235,251,253,252,254,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,143,175,180,179,183,183,183,183,151,215,215,215,215,128,183,183,183,183,179,179,181,166,143,207,255,255,255,255,255,255,255,255,255,255,255])
    
    # BITMAP: width: 72, height: 80
    grubol_inverted_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,96,32,16,16,8,8,8,4,4,4,2,2,2,6,4,12,24,48,192,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,56,7,1,0,0,0,0,128,2,0,0,0,0,16,0,0,0,0,0,0,0,0,0,1,14,248,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,188,3,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,6,152,160,224,192,128,128,128,0,0,0,0,0,0,0,128,128,128,128,128,64,64,96,112,216,140,7,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,224,16,8,12,4,4,2,2,2,130,98,34,28,14,2,2,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,3,14,56,200,24,112,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,28,48,32,192,128,0,0,224,62,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,254,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,64,64,64,67,222,224,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,248,135,192,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,4,4,4,4,2,2,1,7,28,48,32,64,64,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,48,28,31,17,16,17,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,56,225,129,2,2,2,2,4,4,4,4,8,248,8,8,8,8,8,8,8,8,136,248,20,4,2,3,1,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,112,80,75,76,72,72,72,72,104,40,40,40,40,127,72,72,72,72,76,76,74,89,112,48,0,0,0,0,0,0,0,0,0,0,0])
    
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
    thumby.display.drawText("5 <3", 8, 2, 0)
    thumby.display.update()
    time.sleep(1.0)
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
# ---------------------------------------------------------
# Main loop
# ---------------------------------------------------------
while True:
    thumby.display.fill(0)
    
    # -------------------------
    # GRUBOL MENU
    # -------------------------
    if scene == "grubol_menu":
        grubol_menu()
        while scene == "grubol_menu":
            if thumby.buttonA.justPressed():
                scene = "leagues_menu"
    # -------------------------
    # LEAGUES MENU
    # -------------------------
    elif scene == "leagues_menu":
        # Input handling: up/down to move league_index, A to choose league -> go to choose_level
        if thumby.buttonD.justPressed():
            if league_index < len(LEAGUES) - 1:
                league_index += 1
                # If selection moved past visible window (third visible line), scroll down
                if league_index >= league_visible_start + 3:
                    league_visible_start = min(league_visible_start + 1, len(LEAGUES) - 3)
        if thumby.buttonU.justPressed():
            if league_index > 0:
                league_index -= 1
                # If selection moved above visible window, scroll up
                if league_index < league_visible_start:
                    league_visible_start = max(0, league_visible_start - 1)
        if thumby.buttonA.justPressed():
            # Enter choose level scene for selected league
            thumby.audio.play(700, 60)
            level_index = 0
            scene = "choose_level"
            thumby.inputJustPressed()  # flush input
            continue

        # Draw the menu
        draw_leagues_menu()

    # -------------------------
    # CHOOSE LEVEL SCREEN
    # -------------------------
    elif scene == "choose_level":
        league = LEAGUES[league_index]
        # Input: up/down to move level_index, A to start level, B to go back to leagues menu
        options = league["numbers_options"]
        if thumby.buttonD.justPressed():
            level_index = min(len(options) - 1, level_index + 1)
        if thumby.buttonU.justPressed():
            level_index = max(0, level_index - 1)
        if thumby.buttonB.justPressed():
            # Back to leagues menu
            scene = "leagues_menu"
            thumby.inputJustPressed()
            continue
        if thumby.buttonA.justPressed():
            # Start the chosen level
            thumby.audio.play(700, 60)
            chosen_count = options[level_index]
            init_level(league, chosen_count)
            scene = "memorise"
            thumby.inputJustPressed()
            continue

        # Draw the choose-level menu
        draw_choose_level_menu(league)

    # -------------------------
    # MEMORISE SCREEN
    # -------------------------
    elif scene == "memorise":
        # Parameters of the timer
        elapsed = time.ticks_ms() - start_time
        t = elapsed / 1000  # seconds
        remaining_ratio = max(0, 1 - (t / seconds_to_memorise_all))
        current_height = int(TIMER_BAR_LENGTH * remaining_ratio)
        if current_height == 0:
            thumby.audio.play(500, 60)
            scene = "choose_your_warriors"
            thumby.inputJustPressed()  # flush input
            continue  # skip the rest of the loop

        # Draw numbers, gaps and the timer
        for i, n in enumerate(numbers):  # n = number, i = index of the number
            n.draw(camera_x)
            thumby.display.drawFilledRectangle(0, 0, 4, current_height, 1)
            thumby.display.drawText("___", n.x - camera_x, BOTTOM_ROW_HEIGHT, 1)
        
        # Draw arrows (visual hint)
        thumby.display.drawText("<", 0, 18, 1)
        thumby.display.drawText(">", thumby.display.width - 5, 18, 1)

    # -------------------------
    # CHOOSE YOUR WARRIORS
    # -------------------------
    elif scene == "choose_your_warriors":
        # Up/Down to move selection among remaining ordered_numbers
        if thumby.buttonU.justPressed():
            thumby.audio.play(700, 60)
            selected_warrior = min(numbers_number - 1 - len(confirmed_warriors), selected_warrior + 1)
        if thumby.buttonD.justPressed():
            thumby.audio.play(700, 60)
            selected_warrior = max(0, selected_warrior - 1)
        if thumby.buttonA.justPressed():
            thumby.audio.play(500, 60)
            # pick the selected warrior from ordered_numbers
            confirmed_warriors.append(ordered_numbers.pop(selected_warrior))  # pop = extract + remove

            if current_warrior < numbers_number - 1:
                selected_warrior = max(0, selected_warrior - 1)
                current_warrior = min(numbers_number - 1, current_warrior + 1)
            else:
                scene = "fight"
                thumby.inputJustPressed()  # flush input
                continue  # skip the rest of the loop

        # Draw numbers and gaps (masked)
        for i, n in enumerate(numbers):  # n = number, i = index of the number
            thumby.display.drawText("***", n.x - camera_x, n.y, 1)
            if i == current_warrior:
                # show the currently selectable warrior (from ordered_numbers)
                if selected_warrior < len(ordered_numbers):
                    thumby.display.drawText(ordered_numbers[selected_warrior].string, n.x - camera_x, BOTTOM_ROW_HEIGHT, 1)
            if i < current_warrior:
                thumby.display.drawText(confirmed_warriors[i].string, n.x - camera_x, BOTTOM_ROW_HEIGHT, 1)
            if i > current_warrior:
                thumby.display.drawText("___", n.x - camera_x, BOTTOM_ROW_HEIGHT, 1)
        
        # Draw arrows (visual hint)
        thumby.display.drawText("<", 0, 18, 1)
        thumby.display.drawText(">", thumby.display.width - 5, 18, 1)

    # -------------------------
    # FIGHT SCENE
    # -------------------------
    elif scene == "fight":
        
        # allow skipping the fight animation
        if thumby.buttonB.justPressed():
            lets_skip = True

        # Always center camera on the current pair
        center_camera_on_pair()

        # STEP 0: show enemy only
        if fight_step == 0:
            if transition:
                thumby.audio.play(700, 60)
                transition = False
            fight_show_enemy()
            if step_wait(RESULT_WAIT):
                fight_step = 1
                fight_timer = 0
                transition = True

        # STEP 1: show both
        elif fight_step == 1:
            if transition:
                thumby.audio.play(700, 60)
                transition = False
            fight_show_both()
            if step_wait(RESULT_WAIT):
                fight_step = 2
                fight_timer = 0
                transition = True

        # STEP 2: compare (both still visible during this second)
        elif fight_step == 2:
            fight_show_both()
            if fight_timer == 0:
                fight_compare()
            if step_wait(RESULT_WAIT):
                fight_step = 3
                fight_timer = 0

        # STEP 3: show result (loser disappears), wait 1s
        elif fight_step == 3:
            fight_show_result()
            if step_wait(RESULT_WAIT):
                fight_step = 4
                fight_timer = 0
                transition = True

        # STEP 4: move to next pair or go to results
        elif fight_step == 4:
            fight_index += 1
            if fight_index >= numbers_number:
                scene = "results"
                fight_step = 0
                fight_timer = 0
            else:
                fight_step = 0
                fight_timer = 0
                
                if lets_skip:
                    lets_skip = False
                    resolve_remaining_fights()
                    scene = "results"
                    continue
        
        

    # -------------------------
    # RESULTS SCENE
    # After showing results, return to leagues menu when finished
    # -------------------------
    elif scene == "results":
        thumby.display.fill(0)

        # STEP 0: show empty labels
        if fight_step == 0:
            thumby.display.drawText("Them:   ", 5, 8, 1)
            thumby.display.drawText("You:    ", 5, 25, 1)
            if step_wait(RESULT_WAIT):
                fight_step = 1
                fight_timer = 0

        # STEP 1: reveal enemy score
        elif fight_step == 1:
            if transition:
                thumby.audio.play(700, 60)
                transition = False
            thumby.display.drawText("Them: " + str(enemy_points), 5, 8, 1)
            thumby.display.drawText("You:    ", 5, 25, 1)
            if step_wait(RESULT_WAIT):
                fight_step = 2
                fight_timer = 0
                transition = True

        # STEP 2: reveal your score
        elif fight_step == 2:
            if transition:
                thumby.audio.play(700, 60)
                transition = False
            thumby.display.drawText("Them: " + str(enemy_points), 5, 8, 1)
            thumby.display.drawText("You: " + str(you_points), 5, 25, 1)
            if step_wait(RESULT_WAIT):
                fight_step = 3
                fight_timer = 0
                transition = True

        # STEP 3: final message, then return to leagues menu
        elif fight_step == 3:
            thumby.display.fill(0)
            if you_points > enemy_points:
                if transition:
                    thumby.audio.playBlocking(700, 150)
                    thumby.audio.playBlocking(20, 50)
                    thumby.audio.playBlocking(705, 1500)
                    transition = False
                thumby.display.drawText("You win", 10, 15, 1)
            else:
                if transition:
                    thumby.audio.playBlocking(500, 300)
                    thumby.audio.playBlocking(20, 300)
                    thumby.audio.playBlocking(450, 300)
                    thumby.audio.playBlocking(20, 300)
                    thumby.audio.playBlocking(380, 1000)
                    transition = False
                thumby.display.drawText("You lose", 10, 15, 1)
            # After showing final message for a moment, go back to leagues menu
            if step_wait(RESULT_WAIT * 2):
                scene = "leagues_menu"
                # reset menu pointers so player can pick any league again
                league_index = 0
                league_visible_start = 0
                transition = True
                thumby.inputJustPressed()
                continue

    # -------------------------
    # Global input for camera scrolling (keeps original behavior)
    # -------------------------
    if thumby.buttonR.pressed():
        camera_x += SCROLL_SPEED
    if thumby.buttonL.pressed():
        if camera_x >= 0:
            camera_x -= SCROLL_SPEED


    thumby.display.update()
