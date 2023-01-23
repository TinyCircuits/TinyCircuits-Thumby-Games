# Stacker

# Can you manage to stack all the blocks?

# Written by Jason Ngo
# Last edited 01/22/2022
"""
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details. You should have received a copy of the GNU General Public License along with this
program. If not, see <https://www.gnu.org/licenses/>.
"""

from machine import idle
import math
import random
from thumbyButton import actionJustPressed, buttonA, buttonB, buttonD, buttonU
from thumbyGraphics import display
import utime

VERSION = "1.1.0"

# Difficulty levels
EASY = 0
"""Easy difficulty level; widest starting line and slowest movement speed."""
MEDIUM = 1
"""Medium difficulty level; medium starting line and medium movement speed."""
HARD = 2
"""Hard difficulty level; smallest starting line and fastest movement speed."""


class Vector2:
    """Vectors in 2D space contain two properties: and x and a y."""
    x: float
    """The vector's x component."""
    y: float
    """The vector's y component."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector2') -> 'Vector2':
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Vector2(x, y)

    def __mul__(self, factor: float) -> 'Vector2':
        x: float = self.x * factor
        y: float = self.y * factor
        return Vector2(x, y)

    def __pow__(self, factor: float) -> 'Vector2':
        x: float = self.x ** factor
        y: float = self.y ** factor
        return Vector2(x, y)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        x: float = self.x - other.x
        y: float = self.y - other.y
        return Vector2(x, y)

    def __truediv__(self, factor: float) -> 'Vector2':
        x: float = self.x / factor
        y: float = self.y / factor
        return Vector2(x, y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Line:
    """Moving line of blocks that stack on top of one another."""
    size: Vector2
    """The size of the line in pixels."""
    speed: float
    """The speed of the line in pixels per frame."""
    position: Vector2
    """The current position of the line in pixels."""

    def __init__(self, size: Vector2, initialPos: Vector2, initialSpeed: float):
        self.size = size
        self.speed = initialSpeed
        self.position = Vector2(initialPos.x, initialPos.y)

    @micropython.native
    def move(self):
        """Translate the line by the amount of its speed."""
        self.position += Vector2(self.speed, 0)

    @micropython.native
    def bounce(self):
        """Invert the movement direction of the line."""
        self.speed *= -1

    @micropython.native
    def draw(self):
        """Draw the line of blocks itself."""
        display.drawFilledRectangle(
            int(self.position.x - self.size.x / 2),
            int(self.position.y - self.size.y),
            int(self.size.x),
            int(self.size.y),
            1)

    @micropython.native
    def update(self):
        """Draw the line and handle movement logic."""
        self.draw()
        if self.speed == 0:
            return
        self.move()
        if (self.position.x - self.size.x / 2) < 0 or \
            (self.position.x + self.size.x / 2) > display.width:
            self.bounce()

    @micropython.native
    def trim(self, other: 'Line') -> 'Line':
        """Snip off parts of the line that overhang the other line.
        
        Parameters:
        ----------
        other: Line
            The line to trim against.
        """
        newLine = Line(Vector2(0, 0), Vector2(0, 0), self.speed)
        selfLeft: float = self.position.x - self.size.x / 2
        selfRight: float = self.position.x + self.size.x / 2
        otherLeft: float = other.position.x - other.size.x / 2
        otherRight: float = other.position.x + other.size.x / 2
        left: float = selfLeft
        right: float = selfRight
        if selfLeft < otherLeft:
            left = otherLeft
        elif selfRight > otherRight:
            right = otherRight
        newLine = Line(Vector2(right - left, self.size.y), Vector2(left + (right - left) / 2, self.position.y - self.size.y), self.speed)
        return newLine


class Scoreboard:
    """Displays the player's score."""
    score: int
    """The player's current score."""

    def __init__(self):
        self.score = 0
        display.setFont("/lib/font3x5.bin", 3, 5, 0)

    @micropython.native
    def addScore(self, amount: int):
        """Add to the player's score.
        
        Parameters
        ----------
        amount : int
            The amount to add to the score.
        """
        self.score += amount

    @micropython.native
    def reset(self):
        """Reset the player's score to 0."""
        self.score = 0

    @micropython.native
    def draw(self):
        """Draw the scoreboard."""
        display.drawFilledRectangle(0, display.height - 8 , display.width, 8, 1)
        display.drawText(f"Score:{self.score}", 2, display.height - 7, 0)

class Game:
    """The main game class."""
    difficulty: int
    """The game's current difficulty."""
    maxFPS: int
    """The maximum frames per second the game will run at."""
    playing: bool
    """Whether the player is currently in-game."""
    lines: list[Line]
    """A list containing all the stacked lines in the active game session (including the currently moving one)."""
    scoreboard: Scoreboard
    """The game scoreboard object."""
    wonGame: bool
    """Whether the player has won the game."""

    def __init__(self):
        self.difficulty = MEDIUM
        self.maxFPS = 60
        self.playing = False
        self.lines = []
        self.scoreboard = Scoreboard()

    @micropython.native
    def titleScreen(self):
        """Display the title screen."""
        display.fill(0)
        display.setFont("/lib/font8x8.bin", 8, 8, 1)
        display.drawText("Stacker", 5, 4, 1)
        display.drawLine(6, 12, display.width - 7, 12, 1)
        display.setFont("/lib/font5x7.bin", 5, 7, 1)
        display.drawText("Press A/B", 8, 16 , 1)
        display.drawText("to Start", 8, 28, 1)
        display.update()
        while not actionJustPressed():
            idle()

    @micropython.native
    def chooseDifficulty(self):
        """Display and choose from the difficulty selection screen."""
        display.blit(bytearray([31, 14, 4]), 1, 16, 3, 5, 0, 0, 0)
        while True:
            display.fill(0)
            display.setFont("/lib/font5x7.bin", 5, 7, 1)
            display.drawText("Easy", 8, 4, 1)
            display.drawText("Medium", 8, 16, 1)
            display.drawText("Hard", 8, 28, 1)
            if self.difficulty == MEDIUM:
                display.blit(bytearray([127, 62, 28, 8]), 1, 16, 4, 7, 0, 0, 0)
                if buttonU.justPressed():
                    self.difficulty = EASY
                elif buttonD.justPressed():
                    self.difficulty = HARD
            elif self.difficulty == EASY:
                display.blit(bytearray([127, 62, 28, 8]), 1, 4, 4, 7, 0, 0, 0)
                if buttonD.justPressed():
                    self.difficulty = MEDIUM
            elif self.difficulty == HARD:
                display.blit(bytearray([127, 62, 28, 8]), 1, 28, 4, 7, 0, 0, 0)
                if buttonU.justPressed():
                    self.difficulty = MEDIUM
            display.update()
            if actionJustPressed():
                break
        
    @micropython.native
    def restart(self) -> bool:
        """Restart the game.

        Returns
        -------
        bool
            True if the game was restarted, False if the game was exited.
        """
        while True:
            display.fill(0)
            display.setFont("/lib/font8x8.bin", 8, 8, 1)
            display.drawText("YOU WON!" if self.wonGame else "YOU LOSE!", 2 if self.wonGame else 1, 4, 1)
            display.drawLine(1, 12, display.width - 1, 12, 1)
            if self.wonGame:
                display.setFont("/lib/font5x7.bin", 5, 7, 1)
                display.drawText(f"Score: {self.scoreboard.score}", 1, 16, 1)
            display.setFont("/lib/font3x5.bin", 3, 5, 1)
            display.drawText("A to restart", 8, 27 , 1)
            display.drawText("B to exit", 8, 33, 1)
            display.update()
            if buttonA.pressed():
                return True
            elif buttonB.pressed():
                return False


    @micropython.native
    def run(self):
        """Run the game."""
        self.titleScreen()
        self.chooseDifficulty()
        self.startGameplay()
        while self.restart():
            self.chooseDifficulty()
            self.startGameplay()

    @micropython.native
    def startGameplay(self) -> bool:
        """Start the gameplay loop.

        Returns
        -------
        bool
            True if the player won the game, False if the player lost the game.
        """
        self.lines.clear()
        self.wonGame = False
        self.scoreboard.reset()
        t0: int = utime.ticks_us()
        self.playing = True
        lineWidth: float
        lineSpeed: float
        if self.difficulty == EASY:
            lineWidth = 16
            lineSpeed = 0.1
        elif self.difficulty == MEDIUM:
            lineWidth = 12
            lineSpeed = 0.15
        elif self.difficulty == HARD:
            lineWidth = 8
            lineSpeed = 0.25
        firstLine = Line(Vector2(lineWidth, 2), Vector2(display.width / 2, display.height - 8), lineSpeed)
        self.lines.append(firstLine)

        # Main loop
        while self.playing:
            display.fill(0)
            for line in self.lines:
                line.update()
            self.scoreboard.draw()
            display.update()
            if actionJustPressed():
                self.place()
            while utime.ticks_diff(utime.ticks_us(), t0) < 1_000_000 / self.maxFPS:
                idle()  

    @micropython.native
    def place(self):
        """Place a new line on the stack."""
        currentLine: Line = self.lines[-1]
        newSpeed: float = abs(currentLine.speed)
        if self.difficulty == EASY:
            newSpeed += 0.025
        elif self.difficulty == MEDIUM:
            newSpeed += 0.035
        elif self.difficulty == HARD:
            newSpeed += 0.05
        # Choose a random starting direction
        newSpeed *= random.choice([-1, 1])
        currentLine.speed = 0
        newLine: Line
        # Only trim if there are two or more stacked lines
        if len(self.lines) > 1:
            newLine = currentLine.trim(self.lines[-2])
            newLine.speed = newSpeed
        else:
            newPos: Vector2 = currentLine.position - Vector2(0, currentLine.size.y)
            newLine = Line(currentLine.size, newPos, newSpeed)
        self.lines.append(newLine)
        # Set win condition if the line reaches the top of the screen
        if newLine.position.y <= 0:
            self.wonGame = True
            self.playing = False
        # Set lose condition if the line is too small
        if newLine.size.x < 0.5:
            self.playing = False
        else:
            score: int = 0
            if self.difficulty == EASY:
                score = 100
            elif self.difficulty == MEDIUM:
                score = 200
            elif self.difficulty == HARD:
                score = 300
            score *= (newLine.size.x / currentLine.size.x) * len(self.lines)
            score = math.ceil(round(score, -2))
            self.scoreboard.addScore(score)
        utime.sleep(1)


@micropython.native
def main():
    """Main function."""
    Game().run()
    display.setFont("/lib/font5x7.bin", 5, 7, 1)


main()