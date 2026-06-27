import thumby
import random
import time

# Initialize the display
thumby.display.setFPS(30)
thumby.display.fill(0)

# Game configuration - change this title to customize your card app
APP_TITLE = "Oblique Strategies"

# Constants
SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40
SCROLL_DELAY = 8  # Frames between scrolling action
SCROLL_SPEED = 1  # Pixels to scroll per action
FADE_STEPS = 8    # Number of steps in the fade animation

TITLE_BG = 0
TITLE_FG = 1

CARD_BG = 1
CARD_FG = 0

SMALL_FONT = "/lib/font3x5.bin"
SMALL_FONT_WIDTH = 3
SMALL_FONT_HEIGHT = 5

BIG_FONT = "/lib/font5x7.bin"
BIG_FONT_WIDTH = 5
BIG_FONT_HEIGHT = 7

FONT_SPACING = 1

LINE_HEIGHT = BIG_FONT_HEIGHT + 1
MAX_VISIBLE_LINES = SCREEN_HEIGHT // LINE_HEIGHT

phrases = [
    "Abandon normal instruments",
    "Accept advice",
    "Accretion",
    "A line has two sides",
    "Allow an easement (an easement is the abandonment of a stricture)",
    "Are there sections? Consider transitions",
    "Ask people to work against their better judgment",
    "Ask your body",
    "Assemble some of the instruments in a group and treat the group",
    "Balance the consistency principle with the inconsistency principle",
    "Be dirty",
    "Breathe more deeply",
    "Bridges -build -burn",
    "Cascades",
    "Change instrument roles",
    "Change nothing and continue with immaculate consistency",
    "Children's voices -speaking -singing",
    "Cluster analysis",
    "Consider different fading systems",
    "Consult other sources -promising -unpromising",
    "Convert a melodic element into a rhythmic element",
    "Courage!",
    "Cut a vital connection",
    "Decorate, decorate",
    "Define an area as `safe` and use it as an anchor",
    "Destroy -nothing -the most important thing",
    "Discard an axiom",
    "Disconnect from desire",
    "Discover the recipes you are using and abandon them",
    "Distorting time",
    "Do nothing for as long as possible",
    "Don't be afraid of things because they're easy to do",
    "Don't be frightened of cliches",
    "Don't be frightened to display your talents",
    "Don't break the silence",
    "Don't stress one thing more than another",
    "Do something boring",
    "Do the washing up",
    "Do the words need changing?",
    "Do we need holes?",
    "Emphasize differences",
    "Emphasize repetitions",
    "Emphasize the flaws",
    "Faced with a choice, do both",
    "Feedback recordings into an acoustic situation",
    "Fill every beat with something",
    "Get your neck massaged",
    "Ghost echoes",
    "Give the game away",
    "Give way to your worst impulse",
    "Go slowly all the way round the outside",
    "Honor thy error as a hidden intention",
    "How would you have done it?",
    "Humanize something free of error",
    "Imagine the music as a moving chain or caterpillar",
    "Imagine the music as a set of disconnected events",
    "Infinitesimal gradations",
    "Intentions -credibility of -nobility of -humility of",
    "Into the impossible",
    "Is it finished?",
    "Is there something missing?",
    "Is the tuning appropriate?",
    "Just carry on",
    "Left channel, right channel, center channel",
    "Listen in total darkness, or in a very large room, very quietly",
    "Listen to the quiet voice",
    "Look at a very small object; look at its center",
    "Look at the order in which you do things",
    "Look closely at the most embarrassing details and amplify them",
    "Lowest common denominator check -single beat -single note -single riff",
    "Make a blank valuable by putting it in an exquisite frame",
    "Make an exhaustive list of everything you might do and do the last thing on the list",
    "Make a sudden, destructive, unpredictable action; incorporate",
    "Mechanicalize something idiosyncratic",
    "Mute and continue",
    "Only one element of each kind",
    "(Organic) machinery",
    "Overtly resist change",
    "Put in earplugs",
    "Remember those quiet evenings",
    "Remove ambiguities and convert to specifics",
    "Remove specifics and convert to ambiguities",
    "Repetition is a form of change",
    "Reverse",
    "Shortcircuit: (example: a man eating peas with the idea that they will improve his virility shovels them straight into his lap)",
    "Shut the door and listen from outside",
    "Simple subtraction",
    "Spectrum analysis",
    "Take a break",
    "Take away the elements in order of apparent non-importance",
    "Tape your mouth",
    "The inconsistency principle",
    "The tape is now the music",
    "Think of the radio",
    "Tidy up",
    "Trust in the you of now",
    "Turn it upside down",
    "Twist the spine",
    "Use an old idea",
    "Use an unacceptable color",
    "Use fewer notes",
    "Use filters",
    "Use 'unqualified' people",
    "Water",
    "What are you really thinking about just now?",
    "What is the reality of the situation?",
    "What mistakes did you make last time?",
    "What would your closest friend do?",
    "What wouldn't you do?",
    "Work at a different speed",
    "You are an engineer",
    "You can only make one dot at a time",
    "You don't have to be ashamed of using your own ideas"
]

# App state
current_phrase = ""
scroll_position = 0
scroll_counter = 0
lines = []
total_height = 0
needs_scrolling = False
is_fading = False
fade_step = 0
fade_in = False  # False for fade out, True for fade in
show_title_screen = True

def line_width(line: str) -> int:
    return len(line) * (BIG_FONT_WIDTH + FONT_SPACING)

def make_lines(text: str) -> tuple[list[str], int]:
    words = text.split(' ')
    lines = []
    current_line = ""
    
    total_width = 0
    lines: list[str] = []
    for word in words:
        test_line = current_line + word + " "
        if line_width(test_line) <= SCREEN_WIDTH:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            total_width = max(total_width, line_width(current_line.strip()))
            current_line = word + " "
    
    if current_line:  # Add the last line
        lines.append(current_line.strip())
        total_width = max(total_width, line_width(current_line.strip()))
    
    return (lines, total_width)

def draw_title_screen():
    thumby.display.fill(TITLE_BG)
    
    # Draw the app title centered (normal size, black text)
    thumby.display.setFont(BIG_FONT, BIG_FONT_WIDTH, BIG_FONT_HEIGHT, FONT_SPACING)
    title_lines, title_width = make_lines(APP_TITLE)
    title_x = max(1, (SCREEN_WIDTH - title_width) // 2)
    current_y = 1
    for line in title_lines:
        thumby.display.drawText(line, title_x, current_y, TITLE_FG)
        current_y += BIG_FONT_HEIGHT + 1
    
    # Draw decorative line
    current_y += 1
    thumby.display.drawLine(5, current_y, SCREEN_WIDTH - 5, current_y, TITLE_FG)
    
    # Draw instructions in smaller text
    thumby.display.setFont(SMALL_FONT, SMALL_FONT_WIDTH, SMALL_FONT_HEIGHT, FONT_SPACING)
    current_y += 3
    thumby.display.drawText("CONTROLS:", 13, current_y, TITLE_FG)
    current_y += SMALL_FONT_HEIGHT + 2
    thumby.display.drawText("A/B: New Card", 8, current_y, TITLE_FG)
    current_y += SMALL_FONT_HEIGHT + 2
    thumby.display.drawText("U/D: Scroll", 11, current_y, TITLE_FG)
    
    thumby.display.update()

def start_fade_transition():
    global is_fading, fade_step, fade_in
    is_fading = True
    fade_step = 0
    fade_in = False  # Start with fade out


def select_random_phrase():
    global current_phrase, scroll_position, scroll_counter, lines, total_height, total_width, needs_scrolling
    
    current_phrase = random.choice(phrases)
    scroll_position = 0
    scroll_counter = 0
    
    # Split the phrase into lines to fit screen width    
    lines, total_width = make_lines(current_phrase)
    
    total_height = len(lines) * LINE_HEIGHT
    needs_scrolling = total_height > (MAX_VISIBLE_LINES * LINE_HEIGHT)

def update():
    global scroll_position, scroll_counter, is_fading, fade_step, fade_in, show_title_screen
    
    # Handle title screen
    if show_title_screen:
        if any([thumby.buttonA.justPressed(), thumby.buttonB.justPressed(),
                thumby.buttonU.justPressed(), thumby.buttonD.justPressed()]):
            show_title_screen = False
            start_fade_transition()
            fade_in = True  # Skip fade out, just fade in the first card
        return
        
    # Handle fade transition
    if is_fading:
        fade_step += 1
        if fade_step >= FADE_STEPS:
            fade_step = 0
            if fade_in:
                # Fade in complete
                is_fading = False
            else:
                # Fade out complete, select new phrase and start fade in
                fade_in = True
                select_random_phrase()
        return
    
    # Check for button presses
    if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
        start_fade_transition()
        return
    
    if thumby.buttonU.pressed() and needs_scrolling and scroll_position > 0:
        scroll_position -= SCROLL_SPEED
    
    if thumby.buttonD.pressed() and needs_scrolling and scroll_position < max(0, total_height - (MAX_VISIBLE_LINES * LINE_HEIGHT)):
        scroll_position += SCROLL_SPEED
    
    # Auto-scroll if needed
    if needs_scrolling:
        scroll_counter += 1
        if scroll_counter >= SCROLL_DELAY:
            scroll_counter = 0
            scroll_position += SCROLL_SPEED
            
            # Loop the scrolling
            if scroll_position >= total_height:
                scroll_position = -MAX_VISIBLE_LINES * LINE_HEIGHT

def draw():
    # Handle title screen
    if show_title_screen:
        draw_title_screen()
        return
        
    thumby.display.fill(CARD_BG) 
    
    if is_fading:
        # Draw fading effect
        intensity = fade_step / FADE_STEPS
        if not fade_in:
            # Fading out (to black)
            fill_value = CARD_FG
            pattern_value = round(intensity * 100)
        else:
            # Fading in (from black)
            fill_value = CARD_FG
            pattern_value = round((1 - intensity) * 100)
            
        thumby.display.fill(1 - fill_value)  # Fill opposite of our fade color
        
        # Create a dithering pattern for the fade effect
        for y in range(SCREEN_HEIGHT):
            for x in range(SCREEN_WIDTH):
                if (x + y) % 4 == 0 and random.randint(0, 100) < pattern_value:
                    thumby.display.setPixel(x, y, fill_value)
                    
    else:
        vertical_offset = 0
        if not needs_scrolling and total_height < SCREEN_HEIGHT:
            vertical_offset = (SCREEN_HEIGHT - total_height) // 2
            
        # Draw visible lines of text 
        visible_start = scroll_position // LINE_HEIGHT
        visible_offset = scroll_position % LINE_HEIGHT
        
        text_x = max(1, (SCREEN_WIDTH - total_width) // 2)
        thumby.display.setFont(BIG_FONT, BIG_FONT_WIDTH, BIG_FONT_HEIGHT, FONT_SPACING)
        for i in range(visible_start, min(len(lines), visible_start + MAX_VISIBLE_LINES + 1)):
            y = (i - visible_start) * LINE_HEIGHT - visible_offset + vertical_offset
            if 0 <= y < SCREEN_HEIGHT:
                thumby.display.drawText(lines[i], text_x, y, CARD_FG)  
        
        # Draw scrollbar if needed
        if needs_scrolling:
            scrollbar_height = max(3, (MAX_VISIBLE_LINES * LINE_HEIGHT) * MAX_VISIBLE_LINES * LINE_HEIGHT // total_height)
            scrollbar_position = min(SCREEN_HEIGHT - scrollbar_height - 1, 
                                  (scroll_position * (SCREEN_HEIGHT - scrollbar_height - 2) // 
                                  max(1, total_height - MAX_VISIBLE_LINES * LINE_HEIGHT)))
            
            thumby.display.drawRectangle(SCREEN_WIDTH - 3, scrollbar_position, 2, scrollbar_height, CARD_FG)
    
    thumby.display.update()

# Initialize with a random phrase
select_random_phrase()

# Main app loop
while True:
    update()
    draw()
    time.sleep(1/30)  # Cap at 30 FPS