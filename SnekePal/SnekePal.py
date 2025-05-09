from sys import path as syspath  # NOQA
syspath.insert(0, '/Games/SnekePal')  # NOQA

from time import sleep
import gc
import random

from thumbyGrayscale import display, Sprite
from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR

# BITMAP: width: 72, height: 40
bmpIntro = [bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 96, 240, 176, 147, 255, 240, 224, 160, 128, 152, 126, 126, 254, 195, 131, 3, 0, 0, 0, 254, 254, 252, 252, 224, 128, 255, 255, 254, 0, 0, 254, 254, 206, 206, 206, 206, 14, 4, 0, 0, 30, 254, 254, 252, 240, 120, 60, 30, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 8, 8, 255, 27, 24, 8, 8, 15, 7, 0, 192, 195, 231, 127, 126, 60, 0, 255, 255, 255, 3, 15, 63, 127, 127, 1, 0, 0, 127, 127, 113, 113, 113, 113, 112, 224, 32, 0, 0, 63, 127, 63, 15, 63, 124, 248, 112, 64, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 252, 20, 20, 28, 0, 248, 16, 16, 0, 112, 168, 168, 176, 0, 144, 168, 168, 200, 0, 112, 168, 168, 176, 0, 248, 8, 8, 240, 0, 8, 252, 8, 8, 0, 144, 168, 168, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]), bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                                                                                                                                                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 96, 46, 0, 8, 0, 64, 0, 32, 2, 128, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 16, 0, 0, 0, 1, 6, 0, 0, 0, 0, 0, 0, 0, 210, 14, 0, 0, 254, 1, 1, 30, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                                                                                                                                                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 208, 0, 7, 16, 16, 1, 0, 5, 0, 0, 32, 128, 0, 0, 64, 0, 0, 128, 128, 68, 8, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 145, 144, 32, 0, 63, 64, 0, 80, 0, 32, 2, 128, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                                                                                                                                                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                                                                                                                                                                                                                                            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])]

# BITMAP: width: 72, height: 40
bmpTitle = [bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 192, 192, 192, 192, 224, 192, 248, 204, 198, 194, 195, 193, 193, 193, 195, 194, 194, 198, 196, 204, 200, 200, 200, 200, 200, 200, 200, 200, 200, 204, 196, 196, 196, 134, 134, 134, 130, 2, 3, 3, 2, 2, 6, 12, 24, 16, 32, 96, 192, 128, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 240, 0, 124, 255, 227, 248, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 127, 31, 15, 3, 15, 63, 255, 224, 240, 252, 254, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 254, 252, 248, 224, 224, 224, 224, 224, 224, 224, 224, 225, 226, 236, 248, 224, 128, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 127, 192, 31, 243, 3, 3, 131, 129, 129, 1, 1, 129, 129, 129, 0, 0, 0, 0, 0, 0, 0, 0, 1, 7, 15, 15, 31, 63, 63, 127, 127, 127, 255, 255, 255, 255, 255, 255, 255, 127, 127, 63, 31, 15, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 24, 51, 100, 200, 209, 241, 113, 176, 120, 153, 25, 105, 209, 144, 148, 86, 86, 80, 16, 16, 80, 80, 80, 208, 144, 80, 72, 40, 24, 14, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 64, 48, 24, 7, 1, 0,
                       0, 0, 0, 0, 0, 0, 192, 0, 240, 248, 248, 248, 248, 248, 254, 120, 31, 7, 0, 0, 255, 128, 63, 224, 128, 0, 0, 1, 3, 2, 2, 1, 1, 129, 129, 193, 64, 96, 96, 192, 192, 128, 128, 128, 128, 128, 128, 128, 192, 64, 64, 64, 64, 64, 32, 32, 32, 16, 16, 8, 8, 4, 6, 254, 1, 0, 0, 0, 0, 0, 0, 0]), bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 3, 2, 6, 4, 4, 4, 4, 4, 4, 4, 6, 2, 2, 2, 3, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 3, 6, 12, 24, 16, 48, 96, 192, 128, 0, 0, 0, 0, 0,
                                                                                                                                                                                                                                                                                                                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 240, 248, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 3, 6, 28, 112, 192,
                                                                                                                                                                                                                                                                                                                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 127, 255, 224, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 255,
                                                                                                                                                                                                                                                                                                                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15, 31, 60, 120, 112, 32, 0, 0, 192, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 192, 96, 56, 14, 3,
                                                                                                                                                                                                                                                                                                                                 0, 0, 0, 0, 0, 0, 192, 224, 0, 0, 0, 0, 0, 8, 6, 7, 0, 0, 0, 0, 255, 255, 192, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 128, 128, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 254, 3, 1, 0, 0, 0, 0, 0])]

# BITMAP: width: 128, height: 32
bmpFont = bytearray([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 60, 126, 66, 66, 126, 60, 0, 0, 0, 68, 126, 126, 64, 0, 0, 0, 100, 114, 114, 94, 94, 76, 0, 0, 66, 74, 74, 126, 126, 52, 0, 0, 60, 38, 34, 126, 126, 32, 0, 0, 46, 78, 74, 122, 122, 48, 0, 0, 60, 126, 74, 74, 122, 48, 0, 0, 2, 98, 114, 122, 14, 6, 0, 0, 52, 74, 74, 126, 126, 52, 0, 0, 12, 82, 82, 126, 126, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 124, 18, 18, 126, 126, 124, 0, 0, 126, 126, 74, 74, 126, 52, 0, 0, 60, 126, 66, 66, 102, 36, 0, 0, 126, 66, 66, 126, 126, 60, 0, 0, 126, 126, 74, 74, 74, 66, 0, 0, 126, 126, 18, 18, 18, 2, 0, 0, 60, 126, 66, 82, 118, 116, 0, 0, 126, 8, 8, 8, 126, 126, 0, 0, 0, 66, 126, 126, 66, 0, 0, 0, 48, 112, 66, 126, 62, 2, 0, 0, 126, 126, 24, 60, 102, 66, 0, 0, 126, 126, 64, 64, 64, 64, 0, 0, 126, 12, 24, 12, 126, 126, 0, 0, 126, 12, 24, 48, 126, 126, 0, 0, 60, 126, 66, 66, 126, 60, 0,
                     0, 126, 126, 18, 18, 30, 12, 0, 0, 60, 126, 66, 82, 34, 92, 0, 0, 126, 126, 18, 50, 94, 76, 0, 0, 36, 78, 74, 122, 122, 48, 0, 0, 2, 2, 126, 126, 2, 2, 0, 0, 62, 64, 64, 96, 126, 62, 0, 0, 30, 32, 64, 96, 62, 30, 0, 0, 126, 48, 24, 48, 126, 126, 0, 0, 98, 52, 24, 28, 38, 66, 0, 0, 6, 14, 120, 120, 14, 6, 0, 0, 98, 114, 122, 94, 78, 70, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

# BITMAP: width: 63, height: 24
bmpLetters = [bytearray([252, 128, 191, 63, 63, 13, 9, 15, 6, 0, 252, 128, 63, 63, 9, 15, 6, 0, 0, 0, 252, 128, 63, 63, 6, 0, 0, 0, 0, 0, 252, 0, 63, 0, 0, 0, 0, 0, 24, 240, 134, 63, 63, 0, 0, 0, 24, 48, 38, 239, 137, 63, 63, 0, 24, 48, 38, 47, 237, 137, 191, 63, 63,
                         248, 128, 190, 63, 63, 237, 137, 63, 62, 0, 248, 128, 190, 191, 137, 63, 62, 0, 0, 0, 248, 128, 190, 63, 62, 0, 0, 0, 0, 0, 252, 0, 63, 0, 0, 0, 0, 0, 248, 128, 190, 63, 62, 0, 0, 0, 248, 128, 62, 255, 137, 63, 62, 0, 248, 128, 62, 63, 237, 137, 191, 63, 62,
                         252, 128, 191, 191, 191, 160, 160, 32, 32, 0, 252, 128, 191, 191, 160, 32, 32, 0, 0, 0, 252, 128, 191, 63, 32, 0, 0, 0, 0, 0, 252, 0, 63, 0, 0, 0, 0, 0, 128, 188, 160, 63, 63, 0, 0, 0, 128, 128, 160, 188, 160, 63, 63, 0, 128, 128, 160, 160, 188, 160, 191, 63, 63]), bytearray([252, 254, 192, 64, 0, 22, 22, 0, 0, 0, 252, 254, 64, 0, 22, 0, 0, 0, 0, 0, 252, 254, 64, 0, 0, 0, 0, 0, 0, 0, 252, 126, 0, 0, 0, 0, 0, 0, 24, 252, 248, 64, 0, 0, 0, 0, 24, 60, 56, 240, 246, 64, 0, 0, 24, 60, 56, 48, 246, 246, 192, 64, 0,
                                                                                                                                                                                                                                                                                                              248, 252, 192, 64, 0, 246, 246, 64, 0, 0, 248, 252, 192, 192, 246, 64, 0, 0, 0, 0, 248, 252, 192, 64, 0, 0, 0, 0, 0, 0, 252, 126, 0, 0, 0, 0, 0, 0, 248, 252, 192, 64, 0, 0, 0, 0, 248, 252, 64, 192, 246, 64, 0, 0, 248, 252, 64, 0, 246, 246, 192, 64, 0,
                                                                                                                                                                                                                                                                                                              252, 254, 192, 192, 192, 192, 192, 64, 0, 0, 252, 254, 192, 192, 192, 64, 0, 0, 0, 0, 252, 254, 192, 64, 0, 0, 0, 0, 0, 0, 252, 126, 0, 0, 0, 0, 0, 0, 128, 252, 222, 64, 0, 0, 0, 0, 128, 192, 192, 220, 222, 64, 0, 0, 128, 192, 192, 192, 220, 222, 192, 64, 0])]
sprLetter = Sprite(9, 8, bmpLetters)

display.blit(bmpIntro, 0, 0, 72, 40, -1, 0, 0)
display.update()

sleep(2)

display.fill(0)
display.update()

sleep(0.5)

letterSpin = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1, 0, 1, 1, 0]

display.setFPS(20)

display.blit(bmpTitle, 0, 0, 72, 40, -1, 0, 0)
display.update()

frame = 0
while True:
    frame += 1
    random.random()

    if buttonA.justPressed():
        break

    for i in range(3):
        animFrame = min(len(letterSpin)-1, (frame + (2-i)*3) % 60)
        sprLetter.x = 0
        sprLetter.y = 0 + i * 10
        sprLetter.setFrame(i*7 + letterSpin[animFrame])
        display.drawSprite(sprLetter)

    display.update()


def drawTextRow(index, text, foreground, background):

    o = 72*index

    textLen = len(text)

    bufBW = display.buffer
    bufGS = display.shading

    fvBW = 0xff if (foreground & 1) else 0
    fvGS = 0xff if (foreground & 2) else 0
    bvBW = 0xff if (background & 1) else 0
    bvGS = 0xff if (background & 2) else 0

    for _ in range((72 - textLen * 8) // 2):
        bufBW[o] = bvBW
        bufGS[o] = bvGS
        o += 1

    for i in range(textLen):
        fontO = (ord(text[i])-ord(' '))*8
        for _ in range(8):
            fontF = bmpFont[fontO]
            fontB = 255 - fontF

            bufBW[o] = (fontF & fvBW) | (fontB & bvBW)
            bufGS[o] = (fontF & fvGS) | (fontB & bvGS)

            fontO += 1
            o += 1

    for _ in range((72*(index+1)) - o):
        bufBW[o] = bvBW
        bufGS[o] = bvGS
        o += 1


options = ["NEBULA", "ENIGMA", "TWIN", "WHIRL", "MAZE"]

for i in range(len(options)):
    drawTextRow(i, options[i], 3, 0)

while not buttonD.justPressed():
    display.update()

drawTextRow(0, options[0], 1, 2)

optionIndex = 0
while True:
    if buttonD.justPressed():
        drawTextRow(optionIndex, options[optionIndex], 3, 0)
        optionIndex = (optionIndex + 1) % len(options)
        drawTextRow(optionIndex, options[optionIndex], 1, 2)
    if buttonU.justPressed():
        drawTextRow(optionIndex, options[optionIndex], 3, 0)
        optionIndex = (optionIndex + len(options) - 1) % len(options)
        drawTextRow(optionIndex, options[optionIndex], 1, 2)

    display.update()

    if buttonA.justPressed():
        break

display.fill(0)
drawTextRow(optionIndex, options[optionIndex], 1, 0)
display.update()

maps = {
    "NEBULA": [
        "..................",
        "..................",
        "..................",
        "..................",
        "..................",
        "..................",
        "..................",
        "..................",
        "..................",
        "..................",
    ],
    "ENIGMA": [
        "xxxxxxxxxxxxxxxxxx",
        "x................x",
        "x................x",
        "x................x",
        "x................x",
        "x................x",
        "x................x",
        "x................x",
        "x................x",
        "xxxxxxxxxxxxxxxxxx",
    ],
    "TWIN": [
        "..................",
        "..................",
        "..................",
        "....x........x....",
        "....x........x....",
        "....x........x....",
        "....x........x....",
        "....x........x....",
        "..................",
        "..................",
    ],
    "WHIRL": [
        "....x.............",
        "....x.............",
        "........xxxxxxxxxx",
        "..................",
        "..................",
        "..................",
        "..................",
        "xxxxxxxxxx........",
        ".............x....",
        ".............x....",
    ],
    "MAZE": [
        "x.x.x.x.x.x.x.x.x.",
        "..................",
        ".x.x.x.x.x.x.x.x.x",
        "..................",
        "x.x.x.x.x.x.x.x.x.",
        "..................",
        ".x.x.x.x.x.x.x.x.x",
        "..................",
        "x.x.x.x.x.x.x.x.x.",
        "..................",
    ],
}

MAP_COLS = const(18)
MAP_ROWS = const(10)
TILE_SIZE = 4

TILE_EMPTY = const(0)
TILE_SNEK = const(1)
TILE_WALL = const(2)
TILE_BODY = const(3)
TILE_FOOD = const(7)

DIR_R = const(0)
DIR_D = const(1)
DIR_L = const(2)
DIR_U = const(3)


def dirNext(dir, p):
    x, y = p
    if dir == DIR_R:
        return ((x+1) % MAP_COLS, y)
    if dir == DIR_L:
        return ((x+MAP_COLS-1) % MAP_COLS, y)
    if dir == DIR_D:
        return (x, (y+1) % MAP_ROWS)
    if dir == DIR_U:
        return (x, (y+MAP_ROWS-1) % MAP_ROWS)


mapTiles = [TILE_EMPTY] * (MAP_COLS * MAP_ROWS)

while True:

    display.setFPS(60)

    mapData = maps[options[optionIndex]]
    for y in range(10):
        for x in range(18):
            display.drawFilledRectangle(
                x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE, 1)
            display.update()
            c = mapData[y][x]
            if c == 'x':
                mapTiles[y*MAP_COLS+x] = TILE_WALL
            else:
                mapTiles[y*MAP_COLS+x] = TILE_EMPTY
            display.drawFilledRectangle(
                x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE, mapTiles[y*MAP_COLS+x])

    display.update()
    sleep(0.5)

    snekX, snekY = 0, 0
    while True:
        snekX = random.randrange(18)
        snekY = random.randrange(10)
        tile = mapTiles[snekY*MAP_COLS+snekX]
        if tile == TILE_EMPTY:
            mapTiles[snekY*MAP_COLS+snekX] = TILE_SNEK
            display.drawFilledRectangle(
                snekX*TILE_SIZE, snekY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SNEK)
            display.update()
            break

    sleep(0.5)

    foodX, foodY = 0, 0

    def spawnFood():
        global foodX, foodY
        attempts = 0
        while attempts < 100:
            attempts += 1
            foodX = random.randrange(18)
            foodY = random.randrange(10)
            tile = mapTiles[foodY*MAP_COLS+foodX]
            if tile == TILE_EMPTY:
                mapTiles[foodY*MAP_COLS+foodX] = TILE_FOOD
                display.drawRectangle(
                    foodX*TILE_SIZE, foodY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_FOOD & 0b11)
                return
        options = []
        for y in range(10):
            for x in range(18):
                tile = mapTiles[foodY*MAP_COLS+foodX]
                if tile == TILE_EMPTY:
                    options.append((x, y))
        if len(options) > 0:
            foodX, foodY = options[random.randrange(len(options))]
            mapTiles[foodY*MAP_COLS+foodX] = TILE_FOOD
            display.drawRectangle(
                foodX*TILE_SIZE, foodY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_FOOD & 0b11)

    spawnFood()
    display.update()

    snekDir = DIR_R
    while True:
        if buttonR.justPressed():
            snekDir = DIR_R
            break
        if buttonD.justPressed():
            snekDir = DIR_D
            break
        if buttonL.justPressed():
            snekDir = DIR_L
            break
        if buttonU.justPressed():
            snekDir = DIR_U
            break

    display.setFPS(5)
    display.update()

    body = []
    score = 0
    gc.collect()
    while True:
        if buttonR.justPressed() and snekDir != DIR_L:
            snekDir = DIR_R
        elif buttonD.justPressed() and snekDir != DIR_U:
            snekDir = DIR_D
        elif buttonL.justPressed() and snekDir != DIR_R:
            snekDir = DIR_L
        elif buttonU.justPressed() and snekDir != DIR_D:
            snekDir = DIR_U

        nextX, nextY = dirNext(snekDir, (snekX, snekY))
        nextTile = mapTiles[nextY*MAP_COLS+nextX]

        if nextTile == TILE_FOOD:
            score += 1
            body.append((snekX, snekY))
            spawnFood()

        elif nextTile != TILE_EMPTY:
            display.drawFilledRectangle(
                snekX*TILE_SIZE, snekY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_BODY)
            break

        if len(body) > 0:
            tailX, tailY = body[0]
            mapTiles[tailY*MAP_COLS+tailX] = TILE_EMPTY
            display.drawFilledRectangle(
                tailX*TILE_SIZE, tailY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_EMPTY)
            del body[0]

            bodyX, bodyY = snekX, snekY
            body.append((bodyX, bodyY))
            mapTiles[bodyY*MAP_COLS+bodyX] = TILE_BODY
            display.drawFilledRectangle(
                bodyX*TILE_SIZE, bodyY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_BODY)
        else:
            mapTiles[snekY*MAP_COLS+snekX] = TILE_EMPTY
            display.drawFilledRectangle(
                snekX*TILE_SIZE, snekY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_EMPTY)

        snekX, snekY = nextX, nextY
        mapTiles[snekY*MAP_COLS+snekX] = TILE_SNEK
        display.drawFilledRectangle(
            snekX*TILE_SIZE, snekY*TILE_SIZE, TILE_SIZE, TILE_SIZE, TILE_SNEK)

        display.update()

    sleep(1)

    display.setFPS(5)
    for i in range(10):
        drawTextRow(1, "GAME OVER"[0:i]+" "*(9-i), 0, 1)
        display.update()

    display.setFPS(max(10, score/2))
    for i in range(score):
        drawTextRow(3, "SCORE "+str(i), 0, 3)
        display.update()

    sleep(0.5)
    drawTextRow(3, "SCORE "+str(score), 0, 1)
    display.update()

    display.setFPS(10)
    while not buttonA.justPressed():
        display.update()
