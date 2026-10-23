import time
import thumby
import random

# Screen is 72x40 px. Default font = 6 px per character -> max 12 chars per line.

MORSE_DICT = {
    'A': '.-',   'B': '-...', 'C': '-.-.', 'D': '-..',  'E': '.',    'F': '..-.',
    'G': '--.',  'H': '....', 'I': '..',   'J': '.---', 'K': '-.-',  'L': '.-..',
    'M': '--',   'N': '-.',   'O': '---',  'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...',  'T': '-',    'U': '..-',  'V': '...-', 'W': '.--',  'X': '-..-',
    'Y': '-.--', 'Z': '--..'
}
ALPHABET = list(MORSE_DICT.keys())

DASH_THRESHOLD_MS = 250   # press shorter than this = dot, longer = dash
TIME_LIMIT_S = 12.0       # seconds allowed to key in a letter

thumby.display.setFPS(60)


def draw_header(title):
    thumby.display.fill(0)
    thumby.display.drawText(title, 0, 0, 1)
    thumby.display.drawLine(0, 9, 71, 9, 1)


def anything_pressed():
    return (thumby.buttonA.pressed() or thumby.buttonB.pressed()
            or thumby.dpadPressed())


def wait_for_release():
    while anything_pressed():
        time.sleep(0.01)


def play_code(code, label):
    """Flash and beep a Morse sequence."""
    for ch in code:
        thumby.display.fill(0)
        thumby.display.drawText(label, 0, 0, 1)
        if ch == '.':
            thumby.display.drawFilledRectangle(33, 18, 6, 6, 1)
            ms = 100
        else:
            thumby.display.drawFilledRectangle(25, 18, 22, 6, 1)
            ms = 300
        thumby.display.update()
        thumby.audio.play(1000, ms)
        time.sleep(ms / 1000)

        thumby.display.fill(0)
        thumby.display.drawText(label, 0, 0, 1)
        thumby.display.update()
        time.sleep(0.15)


def input_morse(target_letter, show_code):
    """A = key (short press dot, long press dash). B = submit. D-pad = clear."""
    current_input = ""
    press_start = 0
    is_pressing = False

    wait_for_release()

    while True:
        thumby.display.fill(0)
        thumby.display.drawText("Find: " + target_letter, 0, 0, 1)
        if show_code:
            thumby.display.drawText("Ans: " + MORSE_DICT[target_letter], 0, 10, 1)
        # only show the last 9 symbols so it never runs off the screen
        thumby.display.drawText("In: " + current_input[-9:], 0, 20, 1)
        thumby.display.drawText("B:OK PAD:CLR", 0, 31, 1)
        thumby.display.update()

        # D-pad clears the input
        if thumby.dpadPressed():
            current_input = ""
            time.sleep(0.2)

        # A button = Morse key
        if thumby.buttonA.pressed():
            if not is_pressing:
                press_start = time.ticks_ms()
                is_pressing = True
        else:
            if is_pressing:
                duration = time.ticks_diff(time.ticks_ms(), press_start)
                is_pressing = False
                if duration < DASH_THRESHOLD_MS:
                    current_input += "."
                    thumby.audio.play(1000, 80)
                else:
                    current_input += "-"
                    thumby.audio.play(1000, 200)

        # B submits
        if thumby.buttonB.pressed():
            thumby.audio.play(600, 100)
            wait_for_release()
            return current_input


def main_menu():
    selected = 0
    wait_for_release()
    while True:
        draw_header("THUMBY MORSE")

        for i, name in enumerate(("1. LEARN", "2. PLAY")):
            y = 14 + i * 13
            if i == selected:
                thumby.display.drawFilledRectangle(4, y, 64, 11, 1)
                thumby.display.drawText(name, 8, y + 2, 0)   # dark text on lit box
            else:
                thumby.display.drawRectangle(4, y, 64, 11, 1)
                thumby.display.drawText(name, 8, y + 2, 1)

        thumby.display.update()

        if thumby.buttonU.pressed() or thumby.buttonD.pressed():
            selected = 1 - selected
            thumby.audio.play(800, 50)
            time.sleep(0.2)

        if thumby.buttonA.pressed():
            thumby.audio.play(1200, 100)
            wait_for_release()
            return selected


def learning_mode():
    idx = 0
    wait_for_release()
    while True:
        letter = ALPHABET[idx]
        code = MORSE_DICT[letter]

        draw_header("LEARN  < >")
        thumby.display.drawText("Letter: " + letter, 6, 13, 1)
        thumby.display.drawText("Morse: " + code, 6, 22, 1)
        thumby.display.drawText("A:Hear", 0, 32, 1)
        thumby.display.drawText("B:Exit", 36, 32, 1)
        thumby.display.update()

        if thumby.buttonR.pressed():
            idx = (idx + 1) % len(ALPHABET)
            time.sleep(0.15)
        elif thumby.buttonL.pressed():
            idx = (idx - 1) % len(ALPHABET)
            time.sleep(0.15)
        elif thumby.buttonA.pressed():
            wait_for_release()
            play_code(code, letter)
        elif thumby.buttonB.pressed():
            wait_for_release()
            break


def survival_game():
    score = 0
    health = 100

    while health > 0:
        target = random.choice(ALPHABET)
        correct_code = MORSE_DICT[target]

        # Show/play the pattern once, then the player has to repeat it from memory
        play_code(correct_code, "Listen: " + target)

        start_time = time.ticks_ms()
        user_code = input_morse(target, False)
        elapsed = time.ticks_diff(time.ticks_ms(), start_time) / 1000.0

        thumby.display.fill(0)
        if user_code == correct_code and elapsed < TIME_LIMIT_S:
            score += 1
            thumby.audio.play(1500, 150)
            thumby.display.drawText("CORRECT!", 12, 16, 1)
        else:
            health -= 25
            thumby.audio.play(400, 400)
            thumby.display.drawText("WRONG!", 18, 12, 1)
            thumby.display.drawText(correct_code, 0, 24, 1)
        thumby.display.update()
        time.sleep(0.8)

    # Game over screen
    wait_for_release()
    while not thumby.buttonB.pressed():
        draw_header("GAME OVER")
        thumby.display.drawText("Score: " + str(score), 12, 16, 1)
        thumby.display.drawText("B: Exit", 18, 30, 1)
        thumby.display.update()
    wait_for_release()


# Main loop
while True:
    mode = main_menu()
    if mode == 0:
        learning_mode()
    else:
        survival_game()
