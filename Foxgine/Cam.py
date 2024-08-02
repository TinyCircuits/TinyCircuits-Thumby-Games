from math import *

class Cam:
    def __init__(self, pos=(0, 0, 0), rot=(0, 0)):
        self.pos = list(pos)
        self.rot = list(rot)
        self.style = 0
        self.yVel = 0
        self.falling = 0
        self.lastPos = [0,0,0]

    def update(self, dt, buttons, objects):
        s = dt * 10
        
        self.lastPos = self.pos[:]
        
        if self.style == 0:
            x, y = s * sin(self.rot[1]), s * cos(self.rot[1])
            if buttons.buttonU.pressed():
                self.pos[0] += x
                self.pos[2] += y
            if buttons.buttonD.pressed():
                self.pos[0] -= x
                self.pos[2] -= y
            if buttons.buttonL.pressed():
                self.pos[0] -= y
                self.pos[2] += x
            if buttons.buttonR.pressed():
                self.pos[0] += y
                self.pos[2] -= x

        elif self.style == 1:
            if buttons.buttonR.pressed():
                self.rot[1] += 0.05
            if buttons.buttonL.pressed():
                self.rot[1] -= 0.05
            if buttons.buttonU.pressed():
                self.rot[0] += 0.05
            if buttons.buttonD.pressed():
                self.rot[0] -= 0.05
        
        if buttons.buttonA.justPressed() and self.falling <= 1:
            print("Jump initiated!")
            self.yVel = 0.8
        
        self.yVel -= 0.1
        self.pos[1] += self.yVel

        if buttons.buttonB.justPressed():
            self.style = (self.style + 1) % 2
        
        self.falling += 1
        
        if self.pos[1] <= 1:
            self.falling = 0
            self.yVel = 0
            self.pos[1] = 1
        
        print(self.lastPos, self.pos)
    
    def changeToLast(self):
        self.pos = self.lastPos
        if self.falling > 0:
            self.yVel = 0
            self.falling = 0
        print("Success!")