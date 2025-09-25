from thumbyHardware import swL, swR, swU, swD, swA, swB

class ButtonState:
    def __init__(self, pin):
        self.pin = pin
        self.clearBuffer()
    
    @micropython.native
    def clearBuffer(self):
        self.__pressed = False
        self.__justPressed = None
        
    @micropython.native
    def update(self):
        pressed = False if self.pin.value() == 1 else True
        self.__justPressed = pressed and not self.__pressed and self.__justPressed is not None
        self.__pressed = pressed
    
    @micropython.native
    def pressed(self):
        return self.__pressed
    
    @micropython.native
    def justPressed(self):
        return self.__justPressed

buttonA = ButtonState(swA) # Left (A) button
buttonB = ButtonState(swB) # Right (B) button
buttonU = ButtonState(swU) # D-pad up
buttonD = ButtonState(swD) # D-pad down
buttonL = ButtonState(swL) # D-pad left
buttonR = ButtonState(swR) # D-pad right

@micropython.native
def clearBuffer():
    buttonA.clearBuffer()
    buttonB.clearBuffer()
    buttonU.clearBuffer()
    buttonD.clearBuffer()
    buttonL.clearBuffer()
    buttonR.clearBuffer()

@micropython.native
def update():
    buttonA.update()
    buttonB.update()
    buttonU.update()
    buttonD.update()
    buttonL.update()
    buttonR.update()

# Returns true if any buttons are currently pressed on the thumby.
@micropython.native
def inputPressed():
    return (buttonA.pressed() or buttonB.pressed() or buttonU.pressed() or buttonD.pressed() or buttonL.pressed() or buttonR.pressed())

# Returns true if any buttons were just pressed on the thumby.
@micropython.native
def inputJustPressed():
    return (buttonA.justPressed() or buttonB.justPressed() or buttonU.justPressed() or buttonD.justPressed() or buttonL.justPressed() or buttonR.justPressed())

# Returns true if any dpad buttons are currently pressed on the thumby.
@micropython.native
def dpadPressed():
    return (buttonU.pressed() or buttonD.pressed() or buttonL.pressed() or buttonR.pressed())

# Returns true if any dpad buttons were just pressed on the thumby.
@micropython.native
def dpadJustPressed():
    return (buttonU.justPressed() or buttonD.justPressed() or buttonL.justPressed() or buttonR.justPressed())

# Returns true if either action button is pressed on the thumby.
@micropython.native
def actionPressed():
    return (buttonA.pressed() or buttonB.pressed())

# Returns true if either action button was just pressed on the thumby.
@micropython.native
def actionJustPressed():
    return (buttonA.justPressed() or buttonB.justPressed())

class ButtonHistory:
    def __init__(self, depth):
        self.depth = depth
        self.history = []
    
    def update(self):
        if buttonA.justPressed(): self.history.append('A')
        if buttonB.justPressed(): self.history.append('B')
        if buttonU.justPressed(): self.history.append('U')
        if buttonD.justPressed(): self.history.append('D')
        if buttonL.justPressed(): self.history.append('L')
        if buttonR.justPressed(): self.history.append('R')
        self.history = self.history[-self.depth:]
