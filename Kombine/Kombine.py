import math
import random
import thumby

BOARD_SIZE = 4
LETTER_WIDTH = 5
LETTER_HEIGHT = 7
BIG_TILES_FROM = 2
ASCII_UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Board:
    def __init__(self):
        self.board = None
        self.score = None
        self.old_board = None
        self.empty_cells = None

        self.size = BOARD_SIZE
        self.pixel_size = thumby.display.height
        self.cell_pixel_size = int(self.pixel_size / self.size)

        self.generate_new_board()

    def generate_new_board(self):
        self.board = []
        self.score = 0
        self.empty_cells = set()

        for row in range(self.size):
            col_array = []
            for col in range(self.size):
                col_array.append(0)
                self.empty_cells.add((row, col))
            self.board.append(col_array)

        self.add_to_random_place()
        self.add_to_random_place()

    def _get_dx_dy_by_direction(self, direction):
        dx, dy = 0, 0

        if direction == thumby.buttonR:
            dx = 1
        elif direction == thumby.buttonL:
            dx = -1
        elif direction == thumby.buttonU:
            dy = -1
        elif direction == thumby.buttonD:
            dy = 1

        return dx, dy

    def _is_cell_can_merge(self, row, col):
        checks = [-1, 1]
        row_values = [self.board[row + check][col] for check in checks if 0 <= row + check < self.size]
        col_values = [self.board[row][col + check] for check in checks if 0 <= col + check < self.size]
        return self.board[row][col] in (row_values + col_values)

    def _check_board_finished(self):
        for row in range(self.size):
            for col in range(self.size):
                if self._is_cell_can_merge(row, col):
                    return False
        return True

    def _get_new_tile_value(self):
        if self.size ** 2 - len(self.empty_cells) <= BIG_TILES_FROM:
            return 2
        return random.randint(1, 2) * 2

    def add_to_random_place(self):
        if not len(self.empty_cells):
            return

        rand = random.randint(0, len(self.empty_cells) - 1)
        cell = list(self.empty_cells)[rand]
        self.empty_cells.remove(cell)

        row, col = cell
        self.board[row][col] = self._get_new_tile_value()

    def _move_cell(self, row, col, direction):
        dx, dy = self._get_dx_dy_by_direction(direction)
        merged = False
        changed = False

        while self.board[row][col] and row >= -dy and col >= -dx and (
                not self.board[row + dy][col + dx]
                or
                self.board[row][col] == self.board[row + dy][col + dx]
        ):
            changed = True
            if not merged or (merged and not self.board[row + dy][col + dx]):
                if not merged and self.board[row][col] == self.board[row + dy][col + dx]:
                    self.score += self.board[row][col] * 2
                    merged = True

                self.board[row + dy][col + dx] += self.board[row][col]
                self.board[row][col] = 0

                if 0 <= row + dy < self.size and 0 <= col + dx < self.size:
                    self.empty_cells.add((row, col))

                try:
                    self.empty_cells.remove((row + dy, col + dx))
                except:
                    pass

            row += dy
            col += dx

        return changed

    def move(self, direction):
        changed = False
        self.old_board = [[cell for cell in row] for row in self.board]

        for line in range(self.size):
            indexes = range(self.size)
            if direction in [thumby.buttonD, thumby.buttonR]:
                indexes = list(reversed(indexes))

            for index in indexes[1:]:
                row, col = (index, line) if direction in [thumby.buttonU, thumby.buttonD] else (line, index)

                try:
                    changed = self._move_cell(row, col, direction) or changed
                except IndexError:
                    changed = True

        if not changed:
            return False

        self.draw_transition(direction)

        self.add_to_random_place()
        self._draw_score()
        if not len(self.empty_cells) and self._check_board_finished():
            self._draw_game_over()

        return True

    def _draw_text_middle_right(self, text, y, color):
        middle_gap = int((thumby.display.width - self.pixel_size - LETTER_WIDTH * len(text)) / 2)
        thumby.display.drawText(text, self.pixel_size + middle_gap - 2, y, color)

    def _draw_score(self):
        thumby.display.drawFilledRectangle(self.pixel_size, 0, thumby.display.width - self.pixel_size, 15, 0)
        self._draw_text_middle_right(str(self.score), 5, 1)

    def _draw_game_over(self):
        self._draw_text_middle_right("Over", thumby.display.height - LETTER_HEIGHT - 3, 1)
        self._draw_text_middle_right("Game", thumby.display.height - (LETTER_HEIGHT * 2) - 6, 1)

    def _draw_line(self, line_place, horizontal=False):
        pixel_place = line_place * self.cell_pixel_size

        if horizontal:
            x1, y1 = pixel_place, 0
            x2, y2 = pixel_place, self.pixel_size - 1
        else:
            x1, y1 = 0, pixel_place
            x2, y2 = self.pixel_size - 1, pixel_place

        thumby.display.drawLine(x1, y1, x2, y2, 1)

    def _fill_cell(self, row, col, color, offset_x=0, offset_y=0):
        reduce_from_row = 1 if row < self.size - 1 else 2
        reduce_from_col = 1 if col < self.size - 1 else 2

        thumby.display.drawFilledRectangle(col * self.cell_pixel_size + 1 + offset_x,
                                           row * self.cell_pixel_size + 1 + offset_y,
                                           self.cell_pixel_size - reduce_from_col,
                                           self.cell_pixel_size - reduce_from_row,
                                           color)

    def _offset_restrict(self, offset, index):
        if offset > 0:
            return min((self.size - 1 - index) * self.cell_pixel_size, offset)
        return max(index * -self.cell_pixel_size, offset)

    def _draw_cell(self, row, col, board=None, offset_x=0, offset_y=0):
        board = board or self.board
        if not board[row][col]:
            return

        reduce_from_row = 0 if row < self.size - 1 else 1
        reduce_from_col = 0 if col < self.size - 1 else 1

        offset_x = self._offset_restrict(offset_x, col)
        offset_y = self._offset_restrict(offset_y, row)

        self._fill_cell(row, col, 1, offset_x, offset_y)
        val = int(math.log(board[row][col], 2))
        thumby.display.drawText(ASCII_UPPERCASE[val - 1],
                                col * self.cell_pixel_size + 3 - reduce_from_col + offset_x,
                                row * self.cell_pixel_size + 2 - reduce_from_row + offset_y,
                                0)

    def draw_board_outline(self):
        thumby.display.drawFilledRectangle(0, 0, self.pixel_size, self.pixel_size, 0)
        thumby.display.drawRectangle(0, 0, self.pixel_size, self.pixel_size, 1)
        for i in range(self.size):
            self._draw_line(i)
            self._draw_line(i, horizontal=True)

    def _get_first_instance_line(self, line, direction, board=None):
        board = board or self.board

        indexes = range(self.size)
        if direction in [thumby.buttonU, thumby.buttonL]:
            indexes = list(reversed(indexes))

        for index in indexes:
            val = board[index][line] if direction in [thumby.buttonU, thumby.buttonD] else board[line][index]
            if val:
                return index

    def _get_first_instance_all_lines(self, direction, board=None):
        board = board or self.board
        positions = []

        for line in range(self.size):
            positions.append(self._get_first_instance_line(line, direction, board))
        return positions

    def _draw_line_transition(self, row, col, direction, transition):
        dx, dy = self._get_dx_dy_by_direction(direction)

        self._draw_cell(row, col, board=self.old_board, offset_x=dx * transition, offset_y=dy * transition)
        ix, iy = dx, dy
        while (dy and 0 <= row + iy < self.size) or (dx and 0 <= col + ix < self.size):
            self._draw_cell(row + iy, col + ix, board=self.old_board, offset_x=dx * transition, offset_y=dy * transition)
            ix, iy = ix + dx, iy + dy

    def draw_transition(self, direction):
        old_positions = self._get_first_instance_all_lines(direction, self.old_board)
        new_positions = self._get_first_instance_all_lines(direction, self.board)
        transitions = [None if old_positions[i] is None or new_positions[i] is None else abs(
            old_positions[i] - new_positions[i]) * self.cell_pixel_size for i in range(self.size)]
        current = [t for t in transitions]

        while len([line for line in current if line and line > 0]):
            self.draw_board_outline()
            for line in range(self.size):
                if transitions[line] is not None:
                    transition = transitions[line] - current[line]
                    if direction in [thumby.buttonU, thumby.buttonD]:
                        row, col = old_positions[line], line
                    else:
                        row, col = line, old_positions[line]
                    self._draw_line_transition(row, col, direction, transition)
                    current[line] = max(current[line] - 5, 0)
            thumby.display.update()

    def draw(self):
        self.draw_board_outline()

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col]:
                    self._draw_cell(row, col)
                else:
                    self._fill_cell(row, col, 0)


# Set the FPS (without this call, the default fps is 30)
all_arrow = [thumby.buttonL, thumby.buttonR, thumby.buttonU, thumby.buttonD]
thumby.display.setFPS(60)
game = Board()

while 1:
    for arrow in all_arrow:
        if arrow.justPressed():
            game.move(arrow)

    game.draw()
    thumby.display.update()
