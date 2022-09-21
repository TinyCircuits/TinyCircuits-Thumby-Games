import thumby
from framebuf import FrameBuffer, MONO_VLSB

#### Sound


def playSound(playingPattern, pattern, pitch):
    thumby.audio.play(400, 5000)


def stopSound():
    thumby.audio.stop()


#### Display

dispBuffer = FrameBuffer(
    thumby.display.display.buffer,
    thumby.display.width,
    thumby.display.height,
    MONO_VLSB
)


async def render(dispWidth, dispHeight, planeBuffer):
    dispBuffer.blit(
        planeBuffer[0],
        (int(thumby.display.width) - dispWidth) >> 1,
        (int(thumby.display.height) - dispHeight) >> 1,
        min(dispWidth, thumby.display.width),
        min(dispHeight, thumby.display.height)
    )
    await thumby.display.update()


#### Key input

keymap = {}

def setKeys(keys):
    global keymap
    keymap = keys

# Get an array of keys that maps Thumby keys to CHIP-8 keys

def getKeys():
    keyboard = bytearray(16)
    if "up" in keymap:
        keyboard[keymap["up"]]    |= thumby.buttonU.pressed()
    if "down" in keymap:
        keyboard[keymap["down"]]  |= thumby.buttonD.pressed()
    if "left" in keymap:
        keyboard[keymap["left"]]  |= thumby.buttonL.pressed()
    if "right" in keymap:
        keyboard[keymap["right"]] |= thumby.buttonR.pressed()
    if "a" in keymap:
        keyboard[keymap["a"]]     |= thumby.buttonA.pressed()
    if "b" in keymap:
        keyboard[keymap["b"]]     |= thumby.buttonB.pressed()
    return keyboard

# Key combination to quit the running program

def breakCombo():
    return thumby.buttonL.pressed() and thumby.buttonA.pressed() and thumby.buttonB.pressed()
