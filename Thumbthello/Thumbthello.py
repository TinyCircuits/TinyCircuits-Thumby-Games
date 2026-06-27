import time

try:
    import thumby

    display = thumby.display

    buttonA = thumby.buttonA
    buttonB = thumby.buttonB
    buttonU = thumby.buttonU
    buttonD = thumby.buttonD
    buttonL = thumby.buttonL
    buttonR = thumby.buttonR

except:

    from thumbyGraphics import display

    from thumbyButton import (
        buttonA,
        buttonB,
        buttonU,
        buttonD,
        buttonL,
        buttonR
    )

EMPTY = 0
BLACK = 1
WHITE = 2

board = []
cursor_x = 2
cursor_y = 3

message = "Your turn"
game_over = False
intro_screen = True

dirs = [
    (-1,-1), (-1,0), (-1,1),
    (0,-1),          (0,1),
    (1,-1),  (1,0),  (1,1)
]

weights = [
    [90,-20,15,10,10,15,-20,90],
    [-20,-35,-5,-5,-5,-5,-35,-20],
    [15,-5,10,3,3,10,-5,15],
    [10,-5,3,2,2,3,-5,10],
    [10,-5,3,2,2,3,-5,10],
    [15,-5,10,3,3,10,-5,15],
    [-20,-35,-5,-5,-5,-5,-35,-20],
    [90,-20,15,10,10,15,-20,90]
]


def reset():

    global board
    global cursor_x
    global cursor_y
    global game_over
    global message

    board = [[EMPTY for _ in range(8)] for _ in range(8)]

    board[3][3] = WHITE
    board[3][4] = BLACK
    board[4][3] = BLACK
    board[4][4] = WHITE

    cursor_x = 2
    cursor_y = 3

    game_over = False
    message = "Your turn"


def inside(y, x):
    return 0 <= y < 8 and 0 <= x < 8


def opponent(player):

    if player == BLACK:
        return WHITE

    return BLACK


def flips(y, x, player):

    if not inside(y, x):
        return []

    if board[y][x] != EMPTY:
        return []

    enemy = opponent(player)
    result = []

    for dy, dx in dirs:

        cy = y + dy
        cx = x + dx

        line_cells = []

        while inside(cy, cx) and board[cy][cx] == enemy:
            line_cells.append((cy, cx))
            cy += dy
            cx += dx

        if inside(cy, cx) and board[cy][cx] == player and len(line_cells) > 0:
            result += line_cells

    return result


def legal_moves(player):

    moves = []

    for y in range(8):
        for x in range(8):

            f = flips(y, x, player)

            if len(f) > 0:
                moves.append((y, x, f))

    return moves


def make_move(y, x, player, f):

    board[y][x] = player

    for fy, fx in f:
        board[fy][fx] = player


def score():

    black = 0
    white = 0

    for row in board:
        for cell in row:

            if cell == BLACK:
                black += 1

            elif cell == WHITE:
                white += 1

    return black, white


def finish_game():

    global game_over
    global message

    game_over = True

    b, w = score()

    if b > w:
        message = "You win"
    elif w > b:
        message = "CPU wins"
    else:
        message = "Draw"


def cpu_move():

    global message

    moves = legal_moves(WHITE)

    if len(moves) == 0:

        if len(legal_moves(BLACK)) == 0:
            finish_game()
        else:
            message = "CPU pass"

        return

    best = moves[0]
    best_score = -9999

    for move in moves:

        y, x, f = move

        s = weights[y][x] + len(f) * 8

        if s > best_score:
            best_score = s
            best = move

    y, x, f = best
    make_move(y, x, WHITE, f)

    if len(legal_moves(BLACK)) == 0:

        if len(legal_moves(WHITE)) == 0:
            finish_game()
        else:
            message = "You pass"
            draw()
            time.sleep(0.5)
            cpu_move()

    else:
        message = "Your turn"


def draw_disc(cx, cy, player):

    left = cx - 2
    top = cy - 2

    if player == WHITE:
        display.drawFilledRectangle(left, top, 5, 5, 1)

    elif player == BLACK:
        display.drawRectangle(left, top, 5, 5, 1)

        display.setPixel(left + 1, top + 1, 0)
        display.setPixel(left + 2, top + 1, 0)
        display.setPixel(left + 3, top + 1, 0)

        display.setPixel(left + 1, top + 2, 0)
        display.setPixel(left + 2, top + 2, 0)
        display.setPixel(left + 3, top + 2, 0)

        display.setPixel(left + 1, top + 3, 0)
        display.setPixel(left + 2, top + 3, 0)
        display.setPixel(left + 3, top + 3, 0)


def draw_intro_token(x, y, player):

    if player == WHITE:

        display.drawFilledRectangle(x, y, 7, 7, 1)

    else:

        display.drawRectangle(x, y, 7, 7, 1)

        display.setPixel(x + 2, y + 2, 0)
        display.setPixel(x + 3, y + 2, 0)
        display.setPixel(x + 4, y + 2, 0)

        display.setPixel(x + 2, y + 3, 0)
        display.setPixel(x + 3, y + 3, 0)
        display.setPixel(x + 4, y + 3, 0)

        display.setPixel(x + 2, y + 4, 0)
        display.setPixel(x + 3, y + 4, 0)
        display.setPixel(x + 4, y + 4, 0)


def draw_intro():

    display.fill(0)

    ticks = time.ticks_ms()
    frame = int(ticks / 400) % 4
    blink = int(ticks / 500) % 2

    display.drawRectangle(0, 0, 72, 40, 1)
    display.drawRectangle(2, 2, 68, 36, 1)

    display.drawText("THUMBTHELLO", 4, 5, 1)

    display.drawLine(18, 20, 53, 20, 1)
    display.drawLine(18, 21, 53, 21, 1)

    if frame == 0:
        draw_intro_token(19, 16, BLACK)
        draw_intro_token(33, 16, WHITE)
        draw_intro_token(47, 16, BLACK)

    elif frame == 1:
        draw_intro_token(19, 16, BLACK)
        draw_intro_token(33, 16, BLACK)
        draw_intro_token(47, 16, WHITE)

    elif frame == 2:
        draw_intro_token(19, 16, WHITE)
        draw_intro_token(33, 16, BLACK)
        draw_intro_token(47, 16, WHITE)

    else:
        draw_intro_token(19, 16, BLACK)
        draw_intro_token(33, 16, WHITE)
        draw_intro_token(47, 16, WHITE)

    if frame == 0:
        display.setPixel(10, 17, 1)
        display.setPixel(61, 24, 1)

    elif frame == 1:
        display.setPixel(12, 15, 1)
        display.setPixel(59, 26, 1)

    elif frame == 2:
        display.setPixel(14, 13, 1)
        display.setPixel(57, 28, 1)

    else:
        display.setPixel(16, 15, 1)
        display.setPixel(55, 26, 1)

    if blink == 0:
        display.drawText("A START", 15, 30, 1)

    display.update()


def draw():

    display.fill(0)

    ox = 0
    oy = 0
    size = 5

    for y in range(9):
        display.drawLine(
            ox,
            oy + y * size,
            ox + 8 * size,
            oy + y * size,
            1
        )

    for x in range(9):
        display.drawLine(
            ox + x * size,
            oy,
            ox + x * size,
            oy + 8 * size,
            1
        )

    for y in range(8):
        for x in range(8):
            cell = board[y][x]

            if cell != EMPTY:
                draw_disc(
                    ox + x * size + 2,
                    oy + y * size + 2,
                    cell
                )

    cx = ox + cursor_x * size
    cy = oy + cursor_y * size

    display.drawLine(cx, cy, cx + 5, cy + 5, 1)
    display.drawLine(cx + 5, cy, cx, cy + 5, 1)

    blink = int(time.ticks_ms() / 300) % 2

    if blink == 0:
        display.drawFilledRectangle(cx, cy, 2, 2, 1)
        display.drawFilledRectangle(cx + 4, cy, 2, 2, 1)
        display.drawFilledRectangle(cx, cy + 4, 2, 2, 1)
        display.drawFilledRectangle(cx + 4, cy + 4, 2, 2, 1)

    b, w = score()

    display.drawText("B" + str(b), 45, 0, 1)
    display.drawText("W" + str(w), 45, 8, 1)

    display.drawText(message[:9], 43, 22, 1)

    if game_over:
        display.drawText("B reset", 43, 31, 1)

    display.update()


def handle_input():

    global cursor_x
    global cursor_y
    global message
    global intro_screen

    if intro_screen:

        if buttonA.justPressed():
            reset()
            intro_screen = False
            time.sleep(0.2)

        return

    if buttonL.justPressed():
        if cursor_x > 0:
            cursor_x -= 1

    if buttonR.justPressed():
        if cursor_x < 7:
            cursor_x += 1

    if buttonU.justPressed():
        if cursor_y > 0:
            cursor_y -= 1

    if buttonD.justPressed():
        if cursor_y < 7:
            cursor_y += 1

    if buttonB.justPressed():
        reset()
        intro_screen = True
        time.sleep(0.2)

    if buttonA.justPressed():

        if not game_over:

            f = flips(cursor_y, cursor_x, BLACK)

            if len(f) == 0:
                message = "Bad move"

            else:
                make_move(cursor_y, cursor_x, BLACK, f)
                draw()
                time.sleep(0.3)
                cpu_move()


reset()

while True:

    handle_input()

    if intro_screen:
        draw_intro()
    else:
        draw()

    time.sleep(0.03)