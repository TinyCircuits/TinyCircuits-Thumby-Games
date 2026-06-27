# -------------------------
# Constants (tiny)
# -------------------------
SCREEN_W = 72
SCREEN_H = 40
CHAR_W = 6
CHAR_H = 8

CARD_W = 20
CARD_H = 24
CENTER_X = 36
CENTER_Y = 20
CARD_Y = CENTER_X - 0  # temporary; will be set properly below

# fix CARD_Y consistent with original
CARD_Y = CENTER_Y - CARD_H // 2 - 2

LEFT_WORD_1 = "White"
LEFT_WORD_2 = "Black"

# -------------------------
# Gameplay (lazy, optimized flash)
# -------------------------
def run_game():
    import thumby as _th
    import time as _time
    import random as _random

    # local constants
    SW = SCREEN_W
    SH = SCREEN_H
    CW = CHAR_W
    CH = CHAR_H
    cX = CENTER_X
    cY = CENTER_Y
    cW = CARD_W
    cH = CARD_H
    cYpos = CARD_Y

    def shuffle_inplace(lst):
        try:
            _random.shuffle(lst)
        except Exception:
            for i in range(len(lst) - 1, 0, -1):
                j = _random.randint(0, i)
                lst[i], lst[j] = lst[j], lst[i]

    def new_deck():
        deck = [0] * 26 + [1] * 26
        shuffle_inplace(deck)
        return deck

    # vertical word + labels
    def draw_vertical_word(word, x, invert=False):
        total_h = len(word) * CH
        y0 = (SH - total_h) // 2
        if invert:
            _th.display.drawFilledRectangle(x, y0, CW, total_h, 1)
            color = 0
        else:
            color = 1
        for i, c in enumerate(word):
            _th.display.drawText(c, x, y0 + i * CH, color)

    def draw_vertical_words():
        left_word = LEFT_WORD_1
        total_h = len(left_word) * CH
        y0 = (SH - total_h) // 2
        _th.display.drawFilledRectangle(0, y0, CW, total_h, 1)
        for i, c in enumerate(left_word):
            _th.display.drawText(c, 0, y0 + i * CH, 0)
        right_word = LEFT_WORD_2
        total_h = len(right_word) * CH
        y0 = (SH - total_h) // 2
        for i, c in enumerate(right_word):
            _th.display.drawText(c, SW - CW, y0 + i * CH, 1)

    def draw_vertical_letters():
        screen_height = SH
        char_height = CH
        card_x = cX - cW // 2
        card_w = cW
        left_word = LEFT_WORD_1
        total_word_height = len(left_word) * char_height
        vertical_offset = (screen_height - total_word_height) // 2
        letter_y = vertical_offset + (total_word_height - char_height) // 2
        left_letter_x = (0 + card_x) // 2
        _th.display.drawText("B", left_letter_x, letter_y, 1)
        right_word_x = SW - CW
        card_right_x = card_x + card_w
        right_letter_x = ((card_right_x + right_word_x) // 2) - 2
        _th.display.drawText("A", right_letter_x, letter_y, 1)

    def draw_vertical_labels():
        draw_vertical_words()
        draw_vertical_letters()

    # card drawing
    def draw_card_back_scaled(width, cards_left=None):
        _th.display.fill(0)
        x = cX - width // 2
        y = cYpos
        _th.display.drawRectangle(x, y, width, cH, 1)
        if width > 2:
            for xx in range(x + 1, x + width - 1):
                for yy in range(y + 1, y + cH - 1):
                    # diagonal stripe pattern using xor
                    if ((xx + yy) % 4) < 2:
                        _th.display.setPixel(xx, yy, 1)
        draw_vertical_labels()
        if cards_left is not None:
            ct = str(cards_left)
            xp = max(0, (SW - len(ct) * 6) // 2)
            _th.display.drawText(ct, xp, 32, 1)
        _th.display.update()

    def draw_card_front_scaled(width, color, cards_left=None):
        _th.display.fill(0)
        x = cX - width // 2
        y = cYpos
        _th.display.drawRectangle(x, y, width, cH, 1)
        if width > 2:
            _th.display.drawFilledRectangle(x + 1, y + 1, width - 2, cH - 2, color)
        draw_vertical_labels()
        if cards_left is not None:
            ct = str(cards_left)
            xp = max(0, (SW - len(ct) * 6) // 2)
            _th.display.drawText(ct, xp, 32, 1)
        _th.display.update()

    def flip_back_to_front_fast(color, cards_left):
        for w in range(cW, 1, -2):
            draw_card_back_scaled(w, cards_left)
            _time.sleep(0.02)
        for w in range(2, cW + 1, 2):
            draw_card_front_scaled(w, color, cards_left)
            _time.sleep(0.02)

    def flip_front_to_back_fast(color, cards_left):
        for w in range(cW, 1, -2):
            draw_card_front_scaled(w, color, cards_left)
            _time.sleep(0.02)
        for w in range(2, cW + 1, 2):
            draw_card_back_scaled(w, cards_left)
            _time.sleep(0.02)

    # FAST flash screen helper
    def flash_screen_fast(duration=0.15):
        buf = _th.display.display.buffer
        for i in range(len(buf)):
            buf[i] ^= 0xFF
        _th.display.update()
        _time.sleep(duration)
        for i in range(len(buf)):
            buf[i] ^= 0xFF
        _th.display.update()

    # -------------------------
    # Main game loop
    # -------------------------
    deck = new_deck()
    score = 0
    current_card = deck.pop() if deck else None
    draw_card_back_scaled(cW, cards_left=len(deck) + 1)
    menu_index = 0

    while True:
        if current_card is None:
            # in-game menu
            if _th.buttonU.justPressed():
                menu_index = 0
            if _th.buttonD.justPressed():
                menu_index = 1

            _th.display.fill(0)
            draw_vertical_words()
            st = str(score)
            sx = (SW - len(st) * 6) // 2
            _th.display.drawText(st, sx, 4, 1)

            again = "Again"
            quitstr = "Quit"
            ax = (SW - len(again) * 6) // 2
            qx = (SW - len(quitstr) * 6) // 2
            if menu_index == 0:
                _th.display.drawText(">", ax - 8, 16, 1)
            if menu_index == 1:
                _th.display.drawText(">", qx - 8, 26, 1)
            _th.display.drawText(again, ax, 16, 1)
            _th.display.drawText(quitstr, qx, 26, 1)
            _th.display.update()

            if _th.buttonA.justPressed():
                if menu_index == 0:
                    deck = new_deck()
                    score = 0
                    current_card = deck.pop()
                    menu_index = 0
                    draw_card_back_scaled(cW, cards_left=len(deck) + 1)
                    continue
                if menu_index == 1:
                    return "quit"
            continue

        # guess input
        guess_black = None
        if _th.buttonA.justPressed():
            guess_black = True
        elif _th.buttonB.justPressed():
            guess_black = False

        if guess_black is not None:
            flip_back_to_front_fast(current_card, cards_left=len(deck) + 1)
            _time.sleep(0.2)

            if (guess_black and current_card == 0) or ((not guess_black) and current_card == 1):
                score += 1
                try:
                    _th.audio.play(400, 100)
                except Exception:
                    pass
            else:
                try:
                    _th.audio.play(150, 200)
                except Exception:
                    pass
                # fast flash for incorrect guess
                flash_screen_fast(0.15)

            if deck:
                next_card = deck.pop()
                flip_front_to_back_fast(current_card, cards_left=len(deck) + 1)
                current_card = next_card
            else:
                current_card = None

        _time.sleep(0.01)
