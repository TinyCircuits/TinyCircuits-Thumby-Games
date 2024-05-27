import random
from thumbyGraphics import display
from thumbySprite import Sprite
import thumbyButton as buttons
from thumbyAudio import audio
import time
import thumby

random.seed(time.ticks_ms())

_recent_key = None
_recent_words = set()

def simple_hash(word):
    """Generate a simple hash for a word."""
    hash_val = 0
    for char in word:
        hash_val = (hash_val * 31 + ord(char)) % 256
    return f"{hash_val:02x}"

def load_words_by_key(file_path, key):
    global _recent_key, _recent_words

    # Return cached words if the key is the same as the last requested
    if key == _recent_key:
        return _recent_words

    # Read the file to find words for the given key
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(key):
                _, words_str = line.strip().split(':', 1)
                _recent_key = key
                _recent_words = set(words_str.split(','))
                return _recent_words

    # If the key is not found, cache and return an empty set
    _recent_key = key
    _recent_words = set()
    return _recent_words

# Load words from the file
words_file_path = '/Games/Wordly/words.txt'
easy_words_file_path = '/Games/Wordly/easywords.txt'

def select_random_key():
    """Generate a random two-character key."""
    return f"{random.randint(0, 255):02x}"

def select_random_word(file_path):
    key = select_random_key()
    words_set = load_words_by_key(file_path, key)
    if words_set:
        words_list = list(words_set)  # Convert set to list
        return random.choice(words_list)
    return None

# Function to check if a word exists in the set
def is_valid_word(word):
    if not word:
        return False
    key = simple_hash(word)
    words_set = load_words_by_key(words_file_path, key)
    return word in words_set
    
# Initialize or load statistics
thumby.saveData.setName("Wordly")

stats = {
    "attempts_1": thumby.saveData.getItem("attempts_1") if thumby.saveData.hasItem("attempts_1") else 0,
    "attempts_2": thumby.saveData.getItem("attempts_2") if thumby.saveData.hasItem("attempts_2") else 0,
    "attempts_3": thumby.saveData.getItem("attempts_3") if thumby.saveData.hasItem("attempts_3") else 0,
    "attempts_4": thumby.saveData.getItem("attempts_4") if thumby.saveData.hasItem("attempts_4") else 0,
    "attempts_5": thumby.saveData.getItem("attempts_5") if thumby.saveData.hasItem("attempts_5") else 0,
    "attempts_6": thumby.saveData.getItem("attempts_6") if thumby.saveData.hasItem("attempts_6") else 0,
    "fails": thumby.saveData.getItem("fails") if thumby.saveData.hasItem("fails") else 0
}

def save_stats():
    for key in stats:
        thumby.saveData.setItem(key, stats[key])
    thumby.saveData.save()

def update_stats(attempts):
    if attempts >= 1 and attempts <= 6:
        stats[f"attempts_{attempts}"] += 1
    else:
        stats["fails"] += 1
    save_stats()

def show_stats_screen():
    display.fill(0)
    display.drawText("Stats:", 0, 0, 1)

    # Bar chart dimensions and configuration
    chart_top = 10  # Leave space for the "Stats:" text at the top
    chart_bottom = 32  # Leave space for x-axis labels and text height
    chart_height = chart_bottom - chart_top  # Calculate available height for bars
    chart_width = 58  # Width for the chart area, leaving space for the scale
    bar_spacing = 2  # Space between bars
    num_bars = len(stats)
    bar_width = (chart_width - (num_bars - 1) * bar_spacing) // num_bars
    max_value = max(stats.values())

    # Ensure we are accessing the stats in the correct order
    stat_keys = ['attempts_1', 'attempts_2', 'attempts_3', 'attempts_4', 'attempts_5', 'attempts_6', 'fails']
    labels = ["1", "2", "3", "4", "5", "6", "X"]

    # Draw y-axis with scale
    if max_value > 1:
        half_step = max_value // 2
        steps = [0, half_step, 2 * half_step]
    else:
        steps = [0, 1]

    for step in steps:
        if step <= max_value:
            y = chart_bottom - int((step / max_value) * chart_height)
            display.drawLine(5, y, 7, y, 1)
            display.drawText(str(step), 0, y - 3, 1)
    

    # Draw x-axis
    display.drawLine(7, chart_bottom, 72, chart_bottom, 1)

    for i, key in enumerate(stat_keys):
        value = stats[key]
        bar_height = int((value / max_value) * chart_height) if max_value > 0 else 0
        x = 9 + i * (bar_width + bar_spacing)  # Start bars further to the right to accommodate y-axis and scale
        y = chart_bottom - bar_height  # Y position so that bars grow upwards
        display.drawFilledRectangle(x, y, bar_width, bar_height, 1)
        display.drawText(labels[i], x + (bar_width - 4) // 2, chart_bottom + 1, 1)  # X-axis labels centered under bars
    
    display.update()

    # Wait for player input to quit
    while not buttons.buttonA.justPressed() and not buttons.buttonB.justPressed():
        buttons.buttonA.update()
        buttons.buttonB.update()




ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

MAX_TRIES = 6
WORD_LENGTH = 5
SCREEN_WIDTH = 72

# Initialize game state
tries = []
incorrect_letters = set()
current_guess = ""
selector_x = 0
selector_y = 0
view_offset = 0

# Randomly select the first letter and word
word_to_guess = select_random_word(easy_words_file_path)
print(f"Word to guess: {word_to_guess}")

# Sprites
Selector = Sprite(9, 9, bytearray([198,1,1,0,0,0,1,1,198, 0,1,1,0,0,0,1,1,0]), 0, 0)
Selector_mask = Sprite(9, 9, bytearray([199,1,1,0,0,0,1,1,199, 1,1,1,0,0,0,1,1,1]), 0, 0)

# Function to draw the current state of the game
def draw_game():
    display.fill(0)
    draw_slider()
    y = 0

    combined_list = tries + [current_guess]

    for i in range(view_offset, min(view_offset + 2, len(combined_list))):
        guess_number = i + 1
        draw_word(guess_number, combined_list[i], y * 8)
        y += 1

    draw_keyboard()
    draw_selector()
    display.update()

# Function to draw a word on the screen
def draw_word(guess_number, word, y, shownum=True):
    if(shownum):
        
        # Draw the guess number and a colon
        display.drawText(f"{guess_number}:", 0, y, 1)
        
    # Adjust x position to account for the guess number and colon
    x_offset = len(f"{guess_number}:") * 8

    for i, letter in enumerate(word[:WORD_LENGTH]):
        x = x_offset + i * 8  # Set the x position for each letter with a spacing of 8 pixels
        if len(word) > WORD_LENGTH and word[WORD_LENGTH + i] == '2':
            display.drawFilledRectangle(x - 1, y, 7, 8, 1)  # Draw filled rectangle for correct letter
            display.drawText(letter, x, y, 0)  # Draw letter in black to contrast with the filled rectangle
        elif len(word) > WORD_LENGTH and word[WORD_LENGTH + i] == '1':
            display.drawText(letter, x, y, 1)
            display.drawLine(x, y + 7, x + 5, y + 7, 1)  # Draw underline for present letter
        else:
            display.drawText(letter, x, y, 1)

# Function to draw the keyboard
def draw_keyboard():
    for row in range(3):
        for col in range(9):
            index = row * 9 + col
            if index < len(ALPHABET):
                letter = ALPHABET[index]
                if letter not in incorrect_letters:
                    display.drawText(letter, col * 8+2, 17 + row * 8, 1)

# Function to draw the selector
def draw_selector():
    Selector.x = selector_x * 8
    Selector.y = 17 + selector_y * 8
    display.drawSpriteWithMask(Selector, Selector_mask)

# Function to draw the slider
def draw_slider():
    total_rows = len(tries) + 1  # Including the current guess line even if it's empty
    if total_rows > 2:
        # Draw the scrollbar track
        display.drawLine(SCREEN_WIDTH - 2, 0, SCREEN_WIDTH - 2, 15, 1)
        
        # Calculate slider height and ensure it's at least 2 pixels
        slider_height = max(2, 15 * 2 // total_rows)
        
        # Calculate the maximum offset
        max_offset = total_rows - 2
        
        # Calculate the vertical position of the slider
        slider_y = (16 - slider_height) * view_offset // max_offset if max_offset > 0 else 0
        slider_y = min(slider_y, 15 - slider_height)  # Ensure the slider doesn't go beyond the track
        
        # Draw the slider
        display.drawFilledRectangle(SCREEN_WIDTH - 3, slider_y, 2, slider_height, 1)

        # Optional: Draw a border around the slider for better visibility
        display.drawRectangle(SCREEN_WIDTH - 4, slider_y - 1, 4, slider_height + 2, 1)


def evaluate_guess(guess):
    feedback = ["0"] * WORD_LENGTH  # Initialize feedback list with "0"
    target_letter_count = {}

    # Count occurrences of each letter in the target word
    for letter in word_to_guess:
        target_letter_count[letter] = target_letter_count.get(letter, 0) + 1

    # First pass: Identify correct letters (2)
    for i, letter in enumerate(guess):
        if letter == word_to_guess[i]:
            feedback[i] = "2"
            target_letter_count[letter] -= 1

    # Second pass: Identify correct letters in the wrong place (1)
    for i, letter in enumerate(guess):
        if feedback[i] == "0" and letter in target_letter_count and target_letter_count[letter] > 0:
            feedback[i] = "1"
            target_letter_count[letter] -= 1

    # Track incorrect letters
    for letter in set(guess):
        if all(feedback[i] == "0" for i in range(WORD_LENGTH) if guess[i] == letter):
            incorrect_letters.add(letter)

    return guess + "".join(feedback)



    
# Function to handle input and update the game state
def handle_input():
    global current_guess, selector_x, selector_y, view_offset

    combined_list_length = len(tries) + 1  # +1 to include current_guess

    if buttons.buttonL.pressed():
        if selector_x > 0:
            selector_x -= 1
        else:
            selector_x = 8  # Wrap around to the right
        time.sleep_ms(150)

    if buttons.buttonR.pressed():
        if selector_x < 8:
            selector_x += 1
        else:
            selector_x = 0  # Wrap around to the left
        time.sleep_ms(150)

    if buttons.buttonU.pressed():
        if selector_y == 0 and view_offset > 0:
            view_offset -= 1
        elif selector_y > 0:
            selector_y -= 1
        time.sleep_ms(150)

    if buttons.buttonD.pressed():
        if selector_y == 2 and view_offset + 2 < combined_list_length:
            view_offset += 1
        elif selector_y < 2:
            selector_y += 1
        time.sleep_ms(150)

    letter_index = selector_y * 9 + selector_x
    if buttons.buttonA.justPressed() and letter_index < len(ALPHABET):
        letter = ALPHABET[letter_index]
        if letter not in incorrect_letters:
            current_guess += letter
            audio.playBlocking(1000, 100)
            audio.playBlocking(1250, 100)
            view_offset = max(0, combined_list_length - 2)

    if buttons.buttonB.justPressed() and current_guess:
        current_guess = current_guess[:-1]
        audio.playBlocking(500, 50)
        view_offset = max(0, combined_list_length - 2)


        
# Initialize display
display.setFPS(30)
WORD_LENGTH = 6
# Create title with the words "thumby slowly handle wordly"
words = ["thumby000002", "slowly001022", "wordly222222"]
y_position = 10
display.fill(0)  # Clear the display
for word in words:
    draw_word(1, word, y_position, shownum=False)  # Draw each word
    y_position += 10  # Move down for the next word

WORD_LENGTH = 5

display.update()
audio.playBlocking(1000, 100)
audio.playBlocking(1250, 100)
audio.playBlocking(1500, 100)
audio.playBlocking(2000, 200)

while True:
    if buttons.buttonA.justPressed():
        break
    elif buttons.buttonB.justPressed():
        show_stats_screen()
      

audio.playBlocking(1000, 100)
audio.playBlocking(1250, 100)
audio.playBlocking(1500, 100)
audio.playBlocking(2000, 200)

# Main game loop
while True:
    handle_input()
    draw_game()
    if len(current_guess) == WORD_LENGTH:
        if is_valid_word(current_guess):
            evaluated_guess = evaluate_guess(current_guess)
            tries.append(evaluated_guess)
            if current_guess == word_to_guess:
                update_stats(len(tries))
                current_guess = ""
                draw_game()
                display.drawFilledRectangle(0, 16, 72, 24, 0)
                display.drawText("You Win!", 0, 20, 1)
                display.drawText(f"Score: {len(tries)}", 0, 30, 1)
                display.update()
                audio.playBlocking(1000, 100)
                audio.playBlocking(1250, 100)
                audio.playBlocking(1500, 100)
                audio.playBlocking(2000, 200)
                time.sleep(2)
                break
            if len(tries) >= MAX_TRIES:
                update_stats(0)  # 0 indicates failure
                draw_game()
                display.drawFilledRectangle(0, 16, 72, 24, 0)
                display.drawText("Game over!", 0, 20, 1)
                display.drawText(f"it was {word_to_guess}", 0, 30, 1)
                display.update()
                audio.playBlocking(2000, 200)
                time.sleep(2)
                break
            audio.playBlocking(1500, 100)
            current_guess = ""
            if len(tries) > 2:
                view_offset = len(tries) - 2
        else:
            display.drawFilledRectangle(0, 16, 72, 24, 0)
            display.drawText("Unlisted", 0, 24, 1)
            display.drawText("word", 0, 32, 1)
            display.update()
            audio.playBlocking(2000, 100)
            audio.playBlocking(1000, 100)
            audio.playBlocking(1500, 100)
            audio.playBlocking(1000, 100)
            audio.playBlocking(1250, 100)
            audio.playBlocking(1000, 200)
            time.sleep(1)
            current_guess = ""

show_stats_screen()
