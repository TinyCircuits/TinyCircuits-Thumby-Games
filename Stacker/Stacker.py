# Stacker

# Can you manage to stack all the blocks?

# Written by Jason Ngo
# Last edited 01/21/2022
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
from thumbyAudio import audio
from thumbyButton import actionJustPressed, buttonA, buttonB, buttonD, buttonU
from thumbyGraphics import display
import utime

VERSION = "1.0.0"

EASY = 0
MEDIUM = 1
HARD = 2

C4 = 261.63
D4 = 293.66
E4 = 329.63
F4 = 349.23
G4 = 392.00
A4 = 440.00
B4 = 493.88
C5 = 523.25
D5 = 587.33
E5 = 659.25
F5 = 698.46
G5 = 783.99
A5 = 880.00
B5 = 987.77
C6 = 1046.50
NOTES = [C4, D4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5, A5, B5, C6]

class Vector2:
    x: float
    y: float

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
    size: Vector2
    speed: float
    position: Vector2

    def __init__(self, size: Vector2, initialPos: Vector2, initialSpeed: float):
        self.size = size
        self.speed = initialSpeed
        self.position = Vector2(initialPos.x, initialPos.y)

    @micropython.native
    def move(self):
        self.position += Vector2(self.speed, 0)

    @micropython.native
    def bounce(self):
        self.speed *= -1

    @micropython.native
    def draw(self):
        display.drawFilledRectangle(
            int(self.position.x - self.size.x / 2),
            int(self.position.y - self.size.y),
            int(self.size.x),
            int(self.size.y),
            1)

    @micropython.native
    def update(self):
        self.draw()
        if self.speed == 0:
            return
        self.move()
        if (self.position.x - self.size.x / 2) < 0 or \
            (self.position.x + self.size.x / 2) > display.width:
            self.bounce()

    @micropython.native
    def trim(self, other: 'Line') -> 'Line':
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
    score: int

    def __init__(self):
        self.score = 0
        display.setFont("/lib/font3x5.bin", 3, 5, 0)

    @micropython.native
    def addScore(self, amount: int):
        self.score += amount

    @micropython.native
    def reset(self):
        self.score = 0

    @micropython.native
    def draw(self):
        display.drawFilledRectangle(0, display.height - 8 , display.width, 8, 1)
        display.drawText(f"Score:{self.score}", 2, display.height - 7, 0)

class Game:
    difficulty: input
    maxFPS: int
    running: bool
    lines: list[Line]
    scoreboard: Scoreboard
    wonGame: bool

    def __init__(self):
        self.difficulty = MEDIUM
        self.maxFPS = 60
        self.running = False
        self.lines = []
        self.scoreboard = Scoreboard()

    @micropython.native
    def titleScreen(self):
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
        self.titleScreen()
        self.chooseDifficulty()
        self.startGameplay()
        while self.restart():
            self.chooseDifficulty()
            self.startGameplay()

    @micropython.native
    def startGameplay(self) -> bool:
        self.lines.clear()
        self.wonGame = False
        self.scoreboard.reset()
        t0: int = utime.ticks_us()
        self.running = True
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

        while self.running:
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
        currentLine: Line = self.lines[-1]
        newSpeed: float = abs(currentLine.speed)
        if self.difficulty == EASY:
            newSpeed += 0.025
        elif self.difficulty == MEDIUM:
            newSpeed += 0.035
        elif self.difficulty == HARD:
            newSpeed += 0.05
        currentLine.speed = 0
        newLine: Line
        if len(self.lines) > 1:
            newLine = currentLine.trim(self.lines[-2])
            newLine.speed = newSpeed
        else:
            newPos: Vector2 = currentLine.position - Vector2(0, currentLine.size.y)
            newLine = Line(currentLine.size, newPos, newSpeed)
        audio.play(int(NOTES[min(len(self.lines) - 1, len(NOTES) - 1)]), 1000)
        self.lines.append(newLine)
        if newLine.position.y <= 0:
            self.wonGame = True
            self.running = False
        if newLine.size.x < 1:
            self.running = False
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
    Game().run()
    display.setFont("/lib/font5x7.bin", 5, 7, 1)


main()