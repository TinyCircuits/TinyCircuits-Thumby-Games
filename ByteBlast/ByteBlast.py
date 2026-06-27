from thumby import Sprite
from thumby import display
from thumby import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR
from thumby import audio
import random
import time
import math
import sys

# Game constants
FPS = 60
FONT_PATH = "/lib/font3x5.bin"
FONT_WIDTH = 3
FONT_HEIGHT = 5
FONT_SPACING = 1
BOARD_DIMENSIONS_PX = 40 # The game board is 40x40 pixels

# UI layout constants
DIVIDER_LINE_X = 40
SCORE_TEXT_POS = (44, 3)
SCORE_VALUE_POS = (44, 10)
QUEUE_START_POS = (45, 20)
QUEUE_SPACING_X = 8
QUEUE_SPACING_Y = 7
GAMEOVER_NEW_TEXT_POS = (44, 18)
GAMEOVER_NEWGAME_POS = (44, 25)
GAMEOVER_EXIT_POS = (44, 32)
TITLE_START_TEXT_POS = (0, 33)
TITLE_WIDTH = 70
TITLE_HEIGHT = 30
TITLE_BORDER_LEFT_X = 0
TITLE_BORDER_TOP_Y = 0
TITLE_BORDER_RIGHT_X = 71
TITLE_BORDER_Y_BOTTOM = 30
TITLE_BOTTOM_LINE_X2 = 72

# Placed BITMAP checkerboard pattern: width: 5, height: 5
PLACED_BIT_MAP_A = bytearray([10, 21, 10, 21, 10])
PLACED_BIT_MAP_B = bytearray([21, 10, 21, 10, 21])


# Title Screen  BITMAP: width: 70, height: 30
TITLE_BIT_MAP = bytearray([255,255,255,255,255,1,1,57,57,57,57,57,57,135,135,255,255,225,225,159,159,127,127,159,159,225,225,255,255,249,249,249,249,1,1,249,249,249,249,255,255,1,1,153,153,153,153,249,249,249,249,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,192,192,207,207,207,207,207,207,240,240,255,255,255,255,255,255,192,192,255,255,255,255,255,255,255,255,255,255,192,192,255,255,255,255,255,255,192,192,207,207,207,207,207,207,207,207,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,0,0,60,60,60,60,60,195,195,255,255,0,0,255,255,255,255,255,255,255,255,255,63,63,3,3,60,60,3,3,63,63,255,255,255,0,0,60,60,60,60,60,60,60,255,255,252,252,252,252,0,0,252,252,252,252,255,255,255,
           63,63,63,63,63,63,63,63,63,63,63,0,0,15,15,15,15,15,48,48,63,63,0,0,15,15,15,15,15,15,15,63,63,0,0,63,63,63,63,63,63,0,0,63,63,63,15,15,15,15,15,15,15,0,0,63,63,63,63,63,63,0,0,63,63,63,63,63,63,63])

# Game Over BITMAP: width: 40, height: 40
GAME_OVER_BIT_MAP = bytearray([255,225,253,253,253,255,63,191,191,191,191,63,255,255,63,191,191,191,63,255,255,63,63,255,63,63,255,255,63,191,191,191,191,255,255,253,253,253,225,255,
           255,255,255,255,255,255,0,127,119,119,119,6,255,255,0,247,247,247,0,255,255,0,254,248,254,0,255,255,0,123,123,123,127,255,255,255,255,255,255,255,
           255,255,255,255,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,239,255,255,255,255,255,
           255,255,255,255,255,255,0,254,254,254,254,0,255,255,224,143,63,143,224,255,255,0,238,238,238,254,255,255,0,222,158,45,243,255,255,255,255,255,255,255,
           255,135,191,191,191,255,254,254,254,254,254,254,255,255,255,255,254,255,255,255,255,254,254,254,254,254,255,255,254,255,255,255,254,255,255,191,191,191,135,255])

TETROMINOES = {
    "I2": [(0, 0), (0, 1)],
    "I3": [(-1, 0), (0, 0), (1, 0)],
    "L3": [(0, 1), (0, 0), (1, 0)],
    "I": [(-2, 0), (-1, 0), (0, 0), (1, 0)],
    "O": [(0, -1), (1, -1), (0, 0), (1, 0)],
    "T": [(0, -1), (-1, 0), (0, 0), (1, 0)],
    "S": [(0, -1), (1, -1), (-1, 0), (0, 0)],
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],
    "J": [(-1, -1), (-1, 0), (0, 0), (1, 0)],
    "L": [(1, -1), (-1, 0), (0, 0), (1, 0)],
    "N": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "F": [(0, -1), (1, -1), (-1, 0), (0, 0), (0, 1)],
    "P": [(-1, -1), (0, -1), (1, -1), (-1, 0), (0, 0)],
    "W": [(-1, 1), (-1, 0), (0, 0), (0, -1), (1, -1)],
    "Y": [(0, -1), (-1, 0), (0, 0), (1, 0), (0, 1)],
    "Z5": [(-1, -1), (0, -1), (0, 0), (0, 1), (1, 1)],
    "L5": [(-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)],
    "U": [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)],
}


# Split pools to allow for piece rarity
POOL_3 = ["I2", "I3", "L3"]
POOL_4 = [
    "I",
    "O",
    "T",
    "S",
    "Z",
    "J",
    "L",
    "N",
]
POOL_5 = ["F", "P", "W", "Y", "Z5", "L5", "U"]


class Game:
    BLOCK_SIZE_PX = 5
    BOARD_DIMENSION = 8

    START_POSITION = (3, 3)
    QUEUE_LENGTH = 3

    # Piece rarity
    COMMON_PIECE_CHANCE = 0.7
    UNCOMMON_PIECE_CHANCE = 0.88

    # Scoring
    BASE_LINE_SCORE = 5
    LINE_SCORE_EXP_MULTIPLIER = 1.2
    TURN_SCORE_MULTIPLIER_OFFSET = 1
    MIN_TURN_SCORE_MULTIPLIER = 1
    
    def __init__(self):
        self.board = [[False for _ in range(Game.BOARD_DIMENSION)] for _ in range(Game.BOARD_DIMENSION)]
        self.score = 0
        self.turn_count = 0
        self.game_over = False

        # 2 patterns 1 for each of the alternating patterns
        self.brick_sprite = Sprite(
            Game.BLOCK_SIZE_PX, Game.BLOCK_SIZE_PX, PLACED_BIT_MAP_A + PLACED_BIT_MAP_B
        )
        self.piece = self.get_random_piece()
        self.position = Game.START_POSITION
        self.queue = [self.get_random_piece() for _ in range(Game.QUEUE_LENGTH)]

    def reset(self):
        self.board = [[False for _ in range(Game.BOARD_DIMENSION)] for _ in range(Game.BOARD_DIMENSION)]
        self.score = 0
        self.turn_count = 0
        self.game_over = False
        self.piece = self.get_random_piece()
        self.position = Game.START_POSITION
        self.queue = [self.get_random_piece() for _ in range(Game.QUEUE_LENGTH)]

    def draw_board(self):
        for row in range(Game.BOARD_DIMENSION):
            for col in range(Game.BOARD_DIMENSION):
                if self.board[row][col]:
                    # alternate between the block patterns to create checkerboard
                    if (row + col) % 2 == 0:
                        self.brick_sprite.setFrame(0)
                    else:
                        self.brick_sprite.setFrame(1)

                    # Col is X, Row is Y
                    self.brick_sprite.x = col * Game.BLOCK_SIZE_PX
                    self.brick_sprite.y = row * Game.BLOCK_SIZE_PX
                    display.drawSprite(self.brick_sprite)

    def draw_current_piece(self):
        for dx, dy in self.piece:
            # Calculate actual screen position
            x = (self.position[0] + dx) * Game.BLOCK_SIZE_PX
            y = (self.position[1] + dy) * Game.BLOCK_SIZE_PX
            display.drawRectangle(x, y, Game.BLOCK_SIZE_PX, Game.BLOCK_SIZE_PX, 1)

    @staticmethod
    def draw_queue_piece(piece, position):
        QUEUE_PIECE_BLOCK_SIZE = 3
        for dx, dy in piece:
            # Calculate actual screen position
            x = position[0] + (dx * QUEUE_PIECE_BLOCK_SIZE)
            y = position[1] + (dy * QUEUE_PIECE_BLOCK_SIZE)
            display.drawRectangle(x, y, QUEUE_PIECE_BLOCK_SIZE, QUEUE_PIECE_BLOCK_SIZE, 1)

    def rotate_piece(self, clock_wise):
        if clock_wise:
            new_shape = [(-dy, dx) for dx, dy in self.piece]
        else:
            new_shape = [(dy, -dx) for dx, dy in self.piece]

        if self.is_in_bounds(self.position[0], self.position[1], new_shape):
            self.piece = new_shape

    def move_piece(self, x_change, y_change):
        new_x = self.position[0] + x_change
        new_y = self.position[1] + y_change

        if self.is_in_bounds(new_x, new_y, self.piece):
            self.position = (new_x, new_y)

    def is_in_bounds(self, col, row, shape):
        # Check if the move results in the piece being out of bound
        for dx, dy in shape:
            new_col = col + dx
            new_row = row + dy
            # Check grid boundaries
            if new_col < 0 or new_col >= Game.BOARD_DIMENSION or new_row < 0 or new_row >= Game.BOARD_DIMENSION:
                return False

        return True

    def piece_can_be_placed(self):
        for dx, dy in self.piece:
            x = self.position[0] + dx
            y = self.position[1] + dy

            if self.board[y][x]:
                return False

        return True

    def place_piece(self):
        if not self.piece_can_be_placed():
            return

        self.turn_count += 1

        for dx, dy in self.piece:
            x = self.position[0] + dx
            y = self.position[1] + dy

            self.board[y][x] = True

        self.score_board()

        # move to next piece in queue
        self.piece = self.queue.pop(0)
        self.queue.append(self.get_random_piece())

        self.check_game_over()
        self.position = Game.START_POSITION

        # if game over pause so players can see there final board
        if self.game_over:
            self.dun_dun_dunnnn()

    def score_board(self):
        # Audio for line clear
        BASE_CLEAR_FREQ = 440
        CLEAR_FREQ_MULTIPLIER = 1.06
        CLEAR_FREQ_SEMITONE_STEP = 2
        CLEAR_SOUND_DURATION = 250

        row_scored = [True for _ in range(Game.BOARD_DIMENSION)]
        col_scored = [True for _ in range(Game.BOARD_DIMENSION)]

        for x in range(Game.BOARD_DIMENSION):
            for y in range(Game.BOARD_DIMENSION):
                # if they are true the entire row/col they are a full linessddw
                col_scored[x] = col_scored[x] and self.board[x][y]
                row_scored[y] = row_scored[y] and self.board[x][y]

        # count total lines scored for cleaner code
        total_lines_scored = sum(row_scored) + sum(col_scored)

        # exit early if no lines scored
        if total_lines_scored == 0:
            return

        # calculate score
        line_score = total_lines_scored * Game.BASE_LINE_SCORE * (Game.LINE_SCORE_EXP_MULTIPLIER**total_lines_scored)
        # give them a reward for longer sessions (doesn't activate until 10 moves)
        turn_multiplier = max(math.log(self.turn_count) - Game.TURN_SCORE_MULTIPLIER_OFFSET, Game.MIN_TURN_SCORE_MULTIPLIER)
        self.score += int(line_score * turn_multiplier)

        # clear the scored lines and make a sound for every line cleared
        # the sounds start at a middle c (261 and go up one note every clear

        lines_cleared = 0
        for y, full in enumerate(row_scored):
            if full:
                audio.playBlocking(int(BASE_CLEAR_FREQ * CLEAR_FREQ_MULTIPLIER ** (CLEAR_FREQ_SEMITONE_STEP * lines_cleared)), CLEAR_SOUND_DURATION)
                for x in range(Game.BOARD_DIMENSION):
                    self.board[x][y] = False

                lines_cleared += 1

        # clear the scored columns
        for x, full in enumerate(col_scored):
            if full:
                audio.playBlocking(int(BASE_CLEAR_FREQ * CLEAR_FREQ_MULTIPLIER ** (CLEAR_FREQ_SEMITONE_STEP * lines_cleared)), CLEAR_SOUND_DURATION)
                for y in range(Game.BOARD_DIMENSION):
                    self.board[x][y] = False

                lines_cleared += 1

    def check_game_over(self):
        # loop over game board with piece in all 4 directions until a viable place spot is found
        NUM_ROTATIONS = 4
        starting_piece = self.piece
        starting_position = self.position

        has_valid_move = False

        for i in range(NUM_ROTATIONS):
            for x in range(Game.BOARD_DIMENSION):
                for y in range(Game.BOARD_DIMENSION):
                    if not self.is_in_bounds(x, y, self.piece):
                        continue

                    self.position = (x, y)
                    if self.piece_can_be_placed():
                        has_valid_move = True
                        break

                if has_valid_move:
                    break

            if has_valid_move:
                break

            # rotate piece
            self.piece = [(-dy, dx) for dx, dy in self.piece]

        # reset to earlier version
        self.piece = starting_piece
        self.position = starting_position

        self.game_over = not has_valid_move

    @staticmethod
    def get_random_piece():
        rand = random.random()
        # pick a random from the pools
        if rand < Game.COMMON_PIECE_CHANCE:  # common (classic piece)
            key = random.choice(POOL_4)
        elif rand < Game.UNCOMMON_PIECE_CHANCE:  # uncommon (small pieces)
            key = random.choice(POOL_3)
        else:  # rare (large pieces)
            key = random.choice(POOL_5)

        return TETROMINOES[key]

    @staticmethod
    def dun_dun_dunnnn():
        # plays the classic dun_dun_dunnnn sound effect
        DB5_FREQ = 553 # Db5
        DUN_DUR_SHORT = 150
        DUN_PAUSE = 0.05
        AB4_FREQ = 415 # Ab4
        F4_FREQ = 349 # F4
        DUN_DUR_LONG = 1000
        audio.playBlocking(DB5_FREQ, DUN_DUR_SHORT)
        time.sleep(DUN_PAUSE)
        audio.playBlocking(AB4_FREQ, DUN_DUR_SHORT)
        time.sleep(DUN_PAUSE)
        audio.playBlocking(F4_FREQ, DUN_DUR_LONG)


game = Game()
display.setFPS(FPS)
display.setFont(FONT_PATH, FONT_WIDTH, FONT_HEIGHT, FONT_SPACING)

game_over_screen = Sprite(BOARD_DIMENSIONS_PX, BOARD_DIMENSIONS_PX, GAME_OVER_BIT_MAP, 0, 0)
title_screen = Sprite(TITLE_WIDTH, TITLE_HEIGHT, TITLE_BIT_MAP, 1, 0)

# title screen
game_started = False

while not game_started:
    display.fill(0)

    display.drawSprite(title_screen)
    # add extra line to seperate title
    display.drawLine(TITLE_BORDER_LEFT_X, TITLE_BORDER_TOP_Y, TITLE_BORDER_LEFT_X, TITLE_BORDER_Y_BOTTOM, 1)
    display.drawLine(TITLE_BORDER_RIGHT_X, TITLE_BORDER_TOP_Y, TITLE_BORDER_RIGHT_X, TITLE_BORDER_Y_BOTTOM, 1)
    display.drawLine(TITLE_BORDER_LEFT_X, TITLE_BORDER_Y_BOTTOM, TITLE_BOTTOM_LINE_X2, TITLE_BORDER_Y_BOTTOM, 1)

    display.drawText("Start: A | Exit: B", *TITLE_START_TEXT_POS, 1)

    if buttonA.justPressed():
        game_started = True

    if buttonB.justPressed():
        sys.exit()

    display.update()


while game_started:
    # clear screen
    display.fill(0)

    # divider line (board takes up 40*40)
    display.drawLine(DIVIDER_LINE_X, 0, DIVIDER_LINE_X, BOARD_DIMENSIONS_PX, 1)

    # Draw Scoreboard
    display.drawText("Score", *SCORE_TEXT_POS, 1)
    display.drawText(f"{game.score}", *SCORE_VALUE_POS, 1)

    if not game.game_over:
        # draw game
        game.draw_board()
        game.draw_current_piece()

        # Draw queue pieces with diagonal spacing
        for i, piece in enumerate(game.queue):
            game.draw_queue_piece(piece, (QUEUE_START_POS[0] + i * QUEUE_SPACING_X, QUEUE_START_POS[1] + i * QUEUE_SPACING_Y))

        # handle input
        if buttonA.justPressed():
            game.place_piece()

        if buttonB.justPressed():
            game.rotate_piece(clock_wise=False)

        if buttonU.justPressed():
            game.move_piece(0, -1)

        if buttonD.justPressed():
            game.move_piece(0, 1)

        if buttonL.justPressed():
            game.move_piece(-1, 0)

        if buttonR.justPressed():
            game.move_piece(1, 0)

    # show game over screen
    else:
        display.drawSprite(game_over_screen)

        # in place of queue section
        display.drawText("New", *GAMEOVER_NEW_TEXT_POS, 1)
        display.drawText("Game: A", *GAMEOVER_NEWGAME_POS, 1)
        display.drawText("Exit: B", *GAMEOVER_EXIT_POS, 1)

        if buttonA.justPressed():
            game.reset()

        if buttonB.justPressed():
            break

    display.update()
