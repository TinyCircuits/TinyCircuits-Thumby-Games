import thumby
import random
import math

class AlphaSprite:
    def __init__(self, width, height, data, mask):
        self.width = width
        self.height = height
        self.sprite = thumby.Sprite(width, height, data, 0, 0)
        if mask != None:
            self.mask = thumby.Sprite(width, height, mask, 0, 0)
        else:
            self.mask = None
        self.handlex = 0.5
        self.handley = 0.5
    
    def Draw(self):
        if self.mask != None:
            thumby.display.drawSpriteWithMask(self.sprite, self.mask)
        else:
            thumby.display.drawSprite(self.sprite)
        
    def SetPos(self, x, y):
        self.sprite.x = x - self.handlex * self.width
        self.sprite.y = y - self.handley * self.height
    
    def SetHandle(self, x, y):
        self.handlex = x
        self.handley = y

    def SetFrame(self, f):
        self.sprite.setFrame(f)
        self.mask.setFrame(f)
        
def DrawOnRoad(x, y, carX, corner, spr):
    if y > 1:
        return
    
    frac = math.pow(1 - y, 0.5)
    scrx = x * (1 - frac)
    centre = thumby.display.width/2 - carX + corner * (frac * frac)
    spr.SetPos(scrx + centre, thumby.display.height * (0.5 + (1 - frac) * 0.5))
    frame = min(5, int(frac * 4.5))
    if frame < 4:
        spr.SetFrame(frame)
        spr.Draw()

class Horizon:
    def __init__(self, x, y, spr):
        self.x = x
        self.y = y
        self.sprite = spr
        spr.SetHandle(0.5, 1)
        
    def Update(self, carX, corner):
        x = self.x + int(corner - carX)
        while x < -self.sprite.width:
            x = x + thumby.display.width + self.sprite.width * 2
        while x > thumby.display.width + self.sprite.width:
            x = x - (thumby.display.width + self.sprite.width * 2) 
        self.sprite.SetPos(x, self.y)

    def Draw(self):
        self.sprite.Draw()

class Road:
    def __init__(self, width):
        self.linescroll = 0
        self.roadwidth = width
        self.sceneryTime = 0.001 #a little nudge so the high lod tree shows
        treeData = bytearray([0,136,200,72,120,180,236,120,96,208,32,0,0,0,1,0,28,7,1,0,3,60,224,1,0,0,0,0,0,0,0,0,0,128,240,255,199,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20,212,42,126,152,16,0,0,0,0,0,0,0,0,1,0,128,195,254,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,96,192,192,0,0,0,0,0,0,0,0,1,6,1,135,248,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,156,224,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        treeMaskData = bytearray([136,220,252,252,252,254,254,252,248,248,240,32,0,1,3,31,63,31,7,3,63,255,255,227,1,0,0,0,0,0,0,0,128,248,255,255,255,199,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,28,254,254,255,255,254,184,16,0,0,0,0,0,0,1,3,129,195,255,255,254,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,224,240,224,224,192,0,0,0,0,0,0,1,7,15,135,255,255,248,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,156,254,252,224,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0])
        self.treeSprite = AlphaSprite(13,25, treeData, treeMaskData)
        self.treeSprite.SetHandle(0.5, 1)
        
    def Update(self):
        self.linescroll = self.linescroll + 1
        self.sceneryTime = math.fmod(self.sceneryTime + 0.05, 0.2)

    def Draw(self, carX, corner):
        lineswitchspeed = 3
        lineswitch = 3 - (self.linescroll % 4)
        col = 1
        for i in range(0, thumby.display.height/2):
            frac = float(i) / (thumby.display.height/2)
            centre = thumby.display.width/2 - carX + corner * (frac * frac)
            y = thumby.display.height - int(i)
            
            lineroadwidth = self.roadwidth * (1 - frac)
            
            left = centre - lineroadwidth
            if left > 0:
                thumby.display.drawLine(0, y, int(centre - lineroadwidth), y, col)
            right = centre + lineroadwidth
            if right < thumby.display.width:
                thumby.display.drawLine(thumby.display.width - 1, y, int(centre + lineroadwidth), y, col)
            
            for lane in range(1, 3):
                thumby.display.setPixel(int(left + (right - left) * (lane / 3)), y, 1 - col)
            
            if lineswitch <= 0:
                col = 1 - col
                lineswitch = lineswitchspeed
                lineswitchspeed -= 0.5
            lineswitch -= 1
        
        for t in range(0, 5):
            DrawOnRoad(-self.roadwidth - 5, t / 5 + self.sceneryTime, carX, corner, self.treeSprite)
            DrawOnRoad(self.roadwidth + 5, t / 5 + self.sceneryTime, carX, corner, self.treeSprite)
        
        
class Traffic:
    def __init__(self, spr, roadwidth):
        self.sprite = spr
        self.halfWidth = spr.width
        self.roadwidth = roadwidth
        self.SetOverHorizon()
        
    def SetOverHorizon(self):
        self.x = -self.roadwidth + (random.randint(0, 2) + 0.5) * (self.roadwidth * 2 / 3)
        self.y = random.uniform(-1.0, -0.5)
        self.speed = random.uniform(0.01, 0.02)

    def Update(self):
        self.y += self.speed
        if self.y > 1:
            self.SetOverHorizon()
            return True
        return False
        
    def Draw(self, carX, corner):
        DrawOnRoad(self.x, self.y, carX, corner, self.sprite)

class Game:
    def __init__(self, mode):
        self.corner = 0
        self.carX = 0.0        
        self.timeToCorner = random.randint(1, 3) * 60
        self.cornerStrength = 0
        self.score = 0
        self.scoreStr = str(self.score)

        self.framesToExtraTraffic = 60
        
        self.mode = mode
        
        carData = bytearray([0,160,112,178,116,60,38,34,34,34,34,34,34,34,34,34,36,126,180,112,160,0,0,3,3,15,5,15,5,7,5,7,7,7,7,7,5,7,5,15,7,11,3,0])
        carMaskData = bytearray([224,240,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,240,224,7,15,31,31,31,31,15,15,15,15,15,15,15,15,15,15,31,31,31,31,15,7])
        self.carSprite = AlphaSprite(22, 13, carData, carMaskData)
        self.carSprite.SetHandle(0.5, 1)
        self.carSprite.SetPos(thumby.display.width/2, thumby.display.height)
        self.carHalfWidth = self.carSprite.width/2
        
        crashData = bytearray([0,0,0,0,128,192,64,96,48,16,16,144,136,200,208,240,240,240,248,28,12,12,30,14,7,6,0,0,0,0,0,0,0,224,240,255,249,28,28,30,62,31,15,15,7,7,3,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,64,32,32,0,0,0,4,2,2,2,2,2,2,2,4,8,240,0,0,0,0,0,48,72,136,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,64,32,32,0,0,0,2,2,1,0,0,0,0,0,0,0,0,1,2,4,8,16,16,16,8,8,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,192,224,128,0,0,0,0,0,0,0,128,0,0,0,0,192,224,224,240,248,120,124,60,62,30,191,30,12,6,6,7,1,1,0,0,0,0,0,0,0,3,7,15,15,14,14,15,23,19,17,9,8,4,4,4,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,192,192,224,224,224,48,56,124,254,254,254,254,254,254,254,252,248,240,0,0,0,0,0,48,120,240,248,252,238,207,135,7,7,15,159,255,255,255,254,252,120,113,51,63,15,7,3,3,3,1,0,0,0,0,0,0,0,0,1,3,7,15,31,31,28,14,7,3,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        crashMask = bytearray([0,0,128,192,224,224,240,248,248,248,248,248,248,248,248,248,248,252,254,254,254,255,255,255,255,255,255,254,254,248,0,0,240,248,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,63,63,63,7,1,0,0,0,1,7,31,31,63,63,63,63,63,63,63,63,15,7,7,3,3,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,192,224,224,240,240,248,252,252,254,255,255,255,255,255,255,255,255,255,254,252,248,0,0,0,120,252,252,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,31,15,7,7,3,0,0,0,0,0,1,3,7,15,31,63,63,63,63,63,31,31,15,7,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,192,224,224,240,248,248,248,252,252,255,255,255,255,255,255,255,255,255,255,255,255,252,192,0,0,0,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,31,15,15,15,3,3,1,1,0,0,0,7,15,31,31,31,31,31,31,31,31,31,31,15,15,7,7,7,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,192,224,224,240,240,248,252,252,254,255,255,255,255,255,255,255,255,255,254,252,248,0,0,0,120,252,252,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,63,31,15,7,7,3,0,0,0,0,0,1,3,7,15,31,63,63,63,63,63,31,31,15,7,3,3,1,0,0,0,0,0,0,0,0,0,0,0,0])
        self.crashSprite = AlphaSprite(32, 22, crashData, crashMask)
        self.crashSprite.SetHandle(0.5, 1)
        self.crashSprite.SetPos(thumby.display.width/2, thumby.display.height)
        self.crashFrame = 0
        self.crashHeight = 0
        self.crashMom = 0
        
        trafficData = bytearray([0,128,192,120,228,226,226,226,226,226,226,226,226,228,120,192,128,0,0,7,15,5,14,7,7,4,4,4,4,7,7,14,5,15,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,224,144,144,144,144,144,144,224,128,0,0,0,0,0,0,0,0,7,12,7,7,5,5,7,15,4,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,64,64,64,128,0,0,0,0,0,0,0,0,0,0,0,6,5,7,5,5,7,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,5,5,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        trafficMaskData = bytearray([128,192,248,252,254,255,255,255,255,255,255,255,255,254,252,248,192,128,7,15,31,31,31,31,15,15,15,15,15,15,31,31,31,31,15,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,224,240,248,248,248,248,248,248,240,224,128,0,0,0,0,0,0,7,15,31,31,15,15,15,15,31,31,15,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,224,224,224,224,192,128,0,0,0,0,0,0,0,0,0,6,15,31,31,15,15,31,31,15,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,15,15,15,15,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.trafficSprite = AlphaSprite(18,25, trafficData, trafficMaskData)
        
        titleData = bytearray([0,0,192,96,48,16,24,12,4,4,140,248,112,0,0,0,0,0,0,0,0,0,8,200,8,24,24,248,112,16,16,144,192,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,96,0,0,0,31,51,32,32,48,16,24,12,6,3,0,24,60,55,16,24,12,3,0,0,61,39,1,1,56,30,3,0,16,56,31,2,3,3,30,0,0,62,51,48,24,14,3,0,28,7,3,11,14,20,30,15,0,31,19,19,30,0])
        titleMask = bytearray([0,192,224,240,120,56,60,30,14,142,254,252,248,112,128,128,0,0,128,0,0,152,220,252,220,60,252,252,252,120,184,248,248,248,160,0,0,0,0,128,0,0,0,128,128,0,128,128,128,0,0,0,128,0,192,240,240,112,0,31,63,127,115,112,120,56,60,30,15,7,27,60,127,127,63,60,31,15,3,61,127,127,47,123,127,127,63,7,120,127,63,63,7,127,127,62,62,127,127,123,62,63,15,63,63,63,15,63,63,62,63,31,63,63,63,63,63,30])
        self.titleSprite = AlphaSprite(59,15,titleData,titleMask)
        self.titleSprite.SetHandle(0.5, 0)
        self.titleSprite.SetPos(thumby.display.width/2, 0)
        
        self.horizon = []

        #no clouds in attract - fights with logo
        if self.mode != 0:
            i = 0
            for cloud in [bytearray([56,120,126,63,31,62,124,124,126,126,124,56,56]),bytearray([16,56,124,124,120,62,63,62,124,120,48,48,16]),bytearray([16,56,60,126,62,28,24,56,56,124,126,120,48])]:
                self.horizon.append(Horizon(thumby.display.width / 3 * [1, 2, 0][i], thumby.display.height/2 - i * 2, AlphaSprite(13, 7, cloud, None)))
                i = i + 1

        mountainData = bytearray([0,0,16,76,14,28,8,40,8,16,32,0,32,64,0,0])
        mountainMask = bytearray([64,112,124,126,127,126,124,124,124,120,120,112,112,112,96,64])    
        self.horizon.append(Horizon(-10, thumby.display.height/2, AlphaSprite(16, 7, mountainData, mountainMask)))

        cityData = bytearray([0,16,16,0,30,30,30,0,24,24,24,0,28,28,0,16,16,16,16,0])
        cityMask = bytearray([24,24,24,31,31,31,31,31,28,28,28,30,30,30,30,24,24,24,24,24])
        self.horizon.append(Horizon(thumby.display.width/2, thumby.display.height/2, AlphaSprite(20, 5, cityData, cityMask)))
        self.horizonOffset = 0

        self.roadwidth = 90
        
        self.traffic = []
        for t in range(0, 3):
            traf = Traffic(self.trafficSprite, self.roadwidth)
            self.traffic.append(traf)
            
        self.road = Road(self.roadwidth)
    
    def UpdateCourse(self):            
        if self.mode == 0:
            return
        
        self.timeToCorner = self.timeToCorner - 1
        if self.timeToCorner < 0:
            self.timeToCorner = random.randint(1, 3) * 60
            self.cornerStrength = random.randint(-50, 50)
        if self.cornerStrength > self.corner:
            self.corner = self.corner + 1
        if self.cornerStrength < self.corner:
            self.corner = self.corner - 1

    def UpdateDifficulty(self):
         if len(self.traffic) < 6:
             self.framesToExtraTraffic = self.framesToExtraTraffic - 1
             if self.framesToExtraTraffic < 0:
                 self.framesToExtraTraffic = 120
                 traf = Traffic(self.trafficSprite, self.roadwidth)
                 self.traffic.append(traf)
        
         if self.roadwidth > 45:
            self.roadwidth = self.roadwidth - 0.05
            self.road.roadwidth = self.roadwidth

    def StartCrash(self):
        self.mode = 2
        self.crashMom = 7

    def Update(self):
        global continueDown
        
        if self.mode == 0:
            if continueDown:
                global game
                game = Game(1)
        elif self.mode == 1:
            turnSpeed = 1
            if thumby.buttonL.pressed() or thumby.buttonB.pressed():
                self.carX = self.carX - turnSpeed
            if thumby.buttonR.pressed() or thumby.buttonA.pressed():
                self.carX = self.carX + turnSpeed
            self.carX = self.carX - self.corner * 0.02
        
        if self.mode == 2:
            if self.CrashOver():
                if continueDown:
                    global game
                    game = Game(0)
            
            self.crashFrame = self.crashFrame + 0.5
            self.crashSprite.SetFrame(int(self.crashFrame))
            self.crashMom = self.crashMom - 0.75
            self.crashHeight = self.crashHeight + self.crashMom
            if self.crashHeight < 0:
                self.crashHeight = 0
                self.crashMom = -self.crashMom * 0.7
            self.crashSprite.SetPos(thumby.display.width/2, thumby.display.height - self.crashHeight)
        
        self.road.Update()
        
        self.horizonOffset = self.horizonOffset - self.corner * 0.01
        for h in self.horizon:
            h.Update(self.carX * 1.5, self.horizonOffset)
        
        self.UpdateCourse()
        
        self.UpdateDifficulty()
        
        crash = False
        
        for t in self.traffic:
            t.roadwidth = self.roadwidth
            if t.Update() and self.mode == 1:
                self.score = self.score + 1
                self.scoreStr = str(self.score)
            if self.mode == 1 and t.y > 0.98 and abs(t.x - self.carX) < (t.halfWidth + self.carHalfWidth) * 0.6:
                self.StartCrash()
            
        self.traffic = sorted(self.traffic, key=lambda x: x.y)
      
        if self.mode == 1 and (self.carX < -self.roadwidth + self.carHalfWidth or self.carX > self.roadwidth - self.carHalfWidth):
            self.StartCrash()
      
    def CrashOver(self):
        return self.crashFrame > 16
      
    def Draw(self):
        for h in self.horizon:
            h.Draw()
        
        self.road.Draw(self.carX, self.corner)
    
        for t in self.traffic:
            t.Draw(self.carX, self.corner)
        
        if self.mode == 0:
            self.titleSprite.Draw()
        elif self.mode == 1:
            self.carSprite.Draw()
        else:
            if not self.CrashOver():
                self.crashSprite.Draw()
            else:
                thumby.display.drawFilledRectangle(0,16,thumby.display.width,10,0)
                thumby.display.drawText("GAME OVER", 10, 16, 1)
            
        if self.mode == 0:
            pass
        else:
            thumby.display.drawText(self.scoreStr, int(thumby.display.width/2 - len(self.scoreStr) * 2.5), 0, 1)
        

            
game = Game(0)

thumby.display.setFPS(30)

continueWasDown = False
continueDown = False

while(True):
    thumby.display.fill(0)
    
    down = thumby.buttonA.pressed() or thumby.buttonB.pressed()
    continueDown = False
    if not continueWasDown and down:
        continueDown = True
    continueWasDown = down
    
    game.Update()
    game.Draw()
    
    thumby.display.update()

