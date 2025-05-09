FPS = 30 # Video frame rate
RES = (72,40) # Video resolution
SCROLL = 6 # Message scroll speed

from sys import path
loc = "/Games/Fireplace/"
path += [loc]
from thumbyGrayscale import display, Sprite, buttonA
display.enableGrayscale()

# Scroll the message
message = """Pull up a seat by the fire, weary traveller, and rest your tired feet.
\n Take a moment to hear the crackle and let the charred air fill slow breaths..."""
txt = [""]
for line in message.split("\n"):
    for word in line.split(" "):
        if len(txt[-1]) + len(word) >= 12:
            txt += [""]
        txt[-1] += (" " if txt[-1] else "") + word
    txt += [""]
display.setFPS(SCROLL)
h = 39
while h > -len(txt)*10:
    h -= 1
    for ln, line in enumerate(txt):
        display.drawText(line, 0, h+10*ln, 1)
    display.update()
    display.fill(0)
    if buttonA.justPressed():
        display.calibrate()

# Play the video
t = 0
display.setFPS(FPS)
video = Sprite(RES[0], RES[1], (loc+"vid.BIT.bin", loc+"vid.SHD.bin"), 0, 0)
while True:
    video.setFrame(t)
    display.drawSprite(video)
    display.update()
    t += 1
    if buttonA.justPressed():
        display.calibrate()