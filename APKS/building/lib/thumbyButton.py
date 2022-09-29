import asyncio
import pygame

class ButtonClass:
    def __init__(self, key):
        self.key = key
        self.lastState = False
        self.latchedPress = False
    
    # Returns True if the button is currently pressed, False if not.
    async def pressed(self):
        pygame.event.pump()
        await asyncio.sleep(0)
        return pygame.key.get_pressed()[self.key]
    
    # Returns True if the button was just pressed, False if not.
    def justPressed(self):
        returnVal=False
        currentState=self.pressed()
        if(self.lastState == False and currentState==True):
            returnVal = True
        if(self.latchedPress):
            returnVal = True
            self.latchedPress = False
        self.lastState = currentState
        return returnVal
    
    # Latches a button press state to be returned later through justPressed
    def update(self):
        currentState=self.pressed()
        if(self.lastState == False and currentState==True):
            self.latchedPress = True
        self.lastState = currentState
        
# Button instantiation
buttonA = ButtonClass(pygame.K_RIGHT) # Right (A) button
buttonB = ButtonClass(pygame.K_LEFT) # Left (B) button
buttonU = ButtonClass(pygame.K_w) # D-pad up
buttonD = ButtonClass(pygame.K_s) # D-pad down
buttonL = ButtonClass(pygame.K_a) # D-pad left
buttonR = ButtonClass(pygame.K_d) # D-pad right

# Returns true if any buttons are currently pressed on the thumby.
def inputPressed():
    return (buttonA.pressed() or buttonB.pressed() or buttonU.pressed() or buttonD.pressed() or buttonL.pressed() or buttonR.pressed())

# Returns true if any buttons were just pressed on the thumby.
def inputJustPressed():
    return (buttonA.justPressed() or buttonB.justPressed() or buttonU.justPressed() or buttonD.justPressed() or buttonL.justPressed() or buttonR.justPressed())

# Returns true if any dpad buttons are currently pressed on the thumby.
def dpadPressed():
    return (buttonU.pressed() or buttonD.pressed() or buttonL.pressed() or buttonR.pressed())

# Returns true if any dpad buttons were just pressed on the thumby.
def dpadJustPressed():
    return (buttonU.justPressed() or buttonD.justPressed() or buttonL.justPressed() or buttonR.justPressed())

# Returns true if either action button is pressed on the thumby.
def actionPressed():
    return (buttonA.pressed() or buttonB.pressed())

# Returns true if either action button was just pressed on the thumby.
def actionJustPressed():
    return (buttonA.justPressed() or buttonB.justPressed())