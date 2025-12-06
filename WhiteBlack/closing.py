# opening.py  -- opening animations (fast, buffer-based)
import thumby
import time

# constants replicated (small)
SCREEN_W = 72
SCREEN_H = 40
CHAR_W = 6
CHAR_H = 8
LEFT_WORD_1 = "White"
LEFT_WORD_2 = "Black"

# -------------------------
# Closing animation (lazy) - REPLACEMENT
# -------------------------
def run_closing():
    # local draw helper (keeps this function self-contained & small in RAM)
    def draw_vertical_word_local(word, x, invert=False):
        total_h = len(word) * CHAR_H
        y0 = (SCREEN_H - total_h) // 2
        if invert:
            thumby.display.drawFilledRectangle(x, y0, CHAR_W, total_h, 1)
            color = 0
        else:
            color = 1
        for i, c in enumerate(word):
            thumby.display.drawText(c, x, y0 + i * CHAR_H, color)

    # local fast in-out cycle (matches opening animate_second_cycle)
    def animate_cycle():
        white_x = 0
        black_x = SCREEN_W - CHAR_W

        target_white_x = (SCREEN_W - (2 * CHAR_W)) // 2
        target_black_x = target_white_x + CHAR_W

        steps_in = abs(target_white_x - white_x)
        buf = thumby.display.display.buffer

        # SLIDE IN (fast, accumulate white on left, keep right black)
        for _ in range(steps_in):
            thumby.display.fill(0)

            # accumulate left-white region from 0..(white_x+CHAR_W)
            white_fill_end = white_x + CHAR_W
            if white_fill_end > 0:
                left = 0
                right = min(white_fill_end, SCREEN_W)
                for row in range(0, SCREEN_H, 8):
                    row_base = (row // 8) * SCREEN_W
                    # write bytes for left..right
                    for xx in range(left, right):
                        buf[row_base + xx] = 0xFF

            # restore right-black region from black_x..SCREEN_W
            black_restore_start = black_x
            if black_restore_start < SCREEN_W:
                left = max(black_restore_start, 0)
                right = SCREEN_W
                for row in range(0, SCREEN_H, 8):
                    row_base = (row // 8) * SCREEN_W
                    for xx in range(left, right):
                        buf[row_base + xx] = 0x00

            # draw both words (white inverted; black normal)
            draw_vertical_word_local(LEFT_WORD_1, white_x, invert=True)
            draw_vertical_word_local(LEFT_WORD_2, black_x, invert=False)

            thumby.display.update()

            white_x += 1
            black_x -= 1

            time.sleep(0.005)

        # FINAL CENTER FRAME
        thumby.display.fill(0)
        for row in range(0, SCREEN_H, 8):
            row_base = (row // 8) * SCREEN_W
            # fill left up to target_white_x + CHAR_W
            for xx in range(0, target_white_x + CHAR_W):
                buf[row_base + xx] = 0xFF

        draw_vertical_word_local(LEFT_WORD_1, target_white_x, invert=True)
        draw_vertical_word_local(LEFT_WORD_2, target_black_x, invert=False)
        thumby.display.update()
        time.sleep(0.05)

        # SLIDE OUT (fast, keep left white and right black during retreat)
        steps_out = steps_in
        # start white_x, black_x at center positions for outward motion
        white_x = target_white_x
        black_x = target_black_x

        for _ in range(steps_out):
            thumby.display.fill(0)

            # left should remain white from 0..(white_x+CHAR_W)
            white_fill_end = white_x + CHAR_W
            if white_fill_end > 0:
                left = 0
                right = min(white_fill_end, SCREEN_W)
                for row in range(0, SCREEN_H, 8):
                    row_base = (row // 8) * SCREEN_W
                    for xx in range(left, right):
                        buf[row_base + xx] = 0xFF

            # right should remain black from black_x..SCREEN_W
            black_restore_start = black_x
            if black_restore_start < SCREEN_W:
                left = max(black_restore_start, 0)
                right = SCREEN_W
                for row in range(0, SCREEN_H, 8):
                    row_base = (row // 8) * SCREEN_W
                    for xx in range(left, right):
                        buf[row_base + xx] = 0x00

            draw_vertical_word_local(LEFT_WORD_1, white_x, invert=True)
            draw_vertical_word_local(LEFT_WORD_2, black_x, invert=False)

            thumby.display.update()

            white_x -= 1
            black_x += 1

            time.sleep(0.005)

        # FINAL OUTER FRAME (words at edges)
        thumby.display.fill(0)
        for row in range(0, SCREEN_H, 8):
            row_base = (row // 8) * SCREEN_W
            for xx in range(0, CHAR_W):
                buf[row_base + xx] = 0xFF
        draw_vertical_word_local(LEFT_WORD_1, 0, invert=True)
        draw_vertical_word_local(LEFT_WORD_2, SCREEN_W - CHAR_W, invert=False)
        thumby.display.update()

    # --- Run first cycle (in->out)
    animate_cycle()

    # --- Reveal the 3 lines (same positions / timing as original)
    thumby.display.drawText("buyme", CHAR_W + 4, 5, 1)
    thumby.display.update()
    time.sleep(0.25)

    thumby.display.drawText("acoffee", CHAR_W + 4, 5 + CHAR_H + 2, 1)
    thumby.display.update()
    time.sleep(0.25)

    thumby.display.drawText("/gea3w6orn", CHAR_W, 5 + (CHAR_H + 2) * 2, 1)
    thumby.display.update()

    # --- Wait for user confirmation
    while not thumby.buttonA.justPressed():
        time.sleep(0.01)

    # --- Second full cycle (in->out) BEFORE returning to menu
    animate_cycle()