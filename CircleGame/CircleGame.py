import time
import thumby
import math
import random

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(30)

random.seed(333)

# y flip, scale Thumby dimensions
wallbottom = 40
walltop = 0
wallleft = 0
wallright = 46


# BITMAP: width: 7, height: 7
bitmap1 = bytearray([28,54,99,65,99,54,28])

# BITMAP: width: 9, height: 9
bitmap2 = bytearray([16,108,130,130,1,130,130,108,16,
           0,0,0,0,1,0,0,0,0])
           
# BITMAP: width: 11, height: 11
bitmap3 = bytearray([112,216,140,6,3,1,3,6,140,216,112,
           0,0,1,3,6,4,6,3,1,0,0])

# BITMAP: width: 13, height: 13
bitmap4 = bytearray([64,176,72,164,20,10,9,10,20,164,72,176,64,
           0,1,2,4,5,9,18,9,5,4,2,1,0])
           
# BITMAP: width: 15, height: 15
bitmap5 = bytearray([192,48,8,4,2,114,1,1,1,114,2,4,8,48,192,
           1,6,8,16,32,36,68,68,68,36,32,16,8,6,1])
           
# BITMAP: width: 17, height: 17
bitmap6 = bytearray([128,112,8,4,2,242,242,1,1,1,194,194,2,4,8,112,128,
           3,28,32,64,128,140,156,60,60,60,156,140,128,64,32,28,3,
           0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0])
          
# BITMAP: width: 19, height: 19
bitmap7 = bytearray([128,112,8,4,2,194,242,249,249,249,249,249,242,210,194,132,8,112,128,
           15,112,128,0,240,249,253,255,255,127,127,255,251,251,249,240,128,112,15,
           0,0,0,1,2,2,3,7,7,4,4,7,3,3,2,1,0,0,0])
           
def Length2D(r1, r2):
    # d1 = np.linalg.norm(r1 - r2)
    diffx = float(r1[0] - r2[0])
    diffy = float(r1[1] - r2[1])
    squaresum = float(diffx * diffx + diffy * diffy);
    return math.sqrt(squaresum)

def Dot2D(r1, r2):
    return float(r1[0] * r2[0] + r1[1] * r2[1])
    
def ReflectCircle2D(r1, r2, v1, v2, m1, m2):
    length = Length2D(r1, r2)**2
    M = m1 + m2
    vdiff = [v1[0] - v2[0], v1[1] - v2[1]]
    rdiff = [r1[0] - r2[0], r1[1] - r2[1]]
    dot = Dot2D(vdiff, rdiff)
    vdeltascale = 2.0 * m2 / M * dot / length
    vdeltax = v1[0] - vdeltascale * rdiff[0]
    vdeltay = v1[1] - vdeltascale * rdiff[1]
    return [vdeltax, vdeltay]
    

class Particle:

    def __init__(self, x, y, vx, vy, radius, circleID):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        # unique identifier for circle
        self.circleID = circleID
        self.combined = None
        
    # https://en.wikipedia.org/wiki/Elastic_collision
    # see the last section on elastic sphere collisions
    def ProcessCollision(self, p2):
        # elastic delta v
        p1 = self
        # better estimation of mass here
        m1 = p1.radius**2
        m2 = p2.radius**2
        #M = m1 + m2
        r1 = [p1.x, p1.y]
        r2 = [p2.x, p2.y]
        v1 = [p1.vx, p1.vy]
        v2 = [p2.vx, p2.vy]
        u1 = ReflectCircle2D(r1, r2, v1, v2, m1, m2)
        u2 = ReflectCircle2D(r2, r1, v2, v1, m2, m1)
        momentumloss = 0.8
        p1.vx = u1[0] * momentumloss
        p1.vy = u1[1] * momentumloss
        p2.vx = u2[0] * momentumloss
        p2.vy = u2[1] * momentumloss

    def CollideAgainstAll(self, particleList):
        # process (n-1) remaining pairs of particles
        # process each particle pair only once
        bBeforeParticles = True
        for particleI in particleList:
            # skip particle pairs that are already computed this frame
            if (particleI.circleID == self.circleID):
                bBeforeParticles = False
            elif not bBeforeParticles:
                diffx = self.x - particleI.x 
                diffy = self.y - particleI.y
                distance = math.sqrt(diffx * diffx + diffy * diffy)
                if(distance < (self.radius + particleI.radius)):
                    overlap = float(-(distance - self.radius - particleI.radius) * 0.5)
                    selfpos = [float(self.x), float(self.y)]
                    particaleipos = [float(particleI.x), float(particleI.y)]
                    length = Length2D(selfpos, particaleipos)
                    if length != 0.0:
                        selfpos[0] += overlap * (selfpos[0] - particaleipos[0]) / length
                        selfpos[1] += overlap * (selfpos[1] - particaleipos[1]) / length
                        particaleipos[0] -= overlap * (selfpos[0] - particaleipos[0]) / length
                        particaleipos[1] -= overlap * (selfpos[1] - particaleipos[1]) / length
                        self.x = selfpos[0]
                        self.y = selfpos[1]
                        particleI.x = particaleipos[0]
                        particleI.y = particaleipos[1]
                    self.ProcessCollision(particleI)
                    if(particleI.radius == self.radius):
                        particleI.combined = self
                        self.combined = particleI

    def MoveParticle(self, dt):
        maxvel = 2.1
        # apply gravity
        if(self.vy < 10):
            self.vy += 0.4 * dt
        if(self.vx < -maxvel):
            self.vx = -maxvel
        if(self.vx > maxvel):
            self.vx = maxvel
        if(self.vy < -maxvel):
            self.vy = -maxvel
        if(self.vy > maxvel):
            self.vy = maxvel
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Make the Particles bounce off the walls
        if self.x - self.radius < wallleft:
            self.x = wallleft + self.radius
            self.vx = -self.vx
        if self.x + self.radius > wallright:
            self.x = wallright - self.radius
            self.vx = -self.vx
        # disable top wall
        #if self.y - self.radius < walltop:
        #    self.y = walltop + self.radius
        #    self.vy = -self.vy
        if self.y + self.radius > wallbottom:
            self.y = wallbottom - self.radius
            self.vy = -self.vy
            
    def Draw2(self):   
        right = math.ceil(self.x + self.radius)
        top = math.ceil(self.y + self.radius)
        x = math.floor(self.x - self.radius)
        y = math.floor(self.y - self.radius)
        xittr = int(x)
        while xittr < right:
            yittr = int(y)
            while yittr < top:
                x1 = self.x
                y1 = self.y
                distance = Length2D([x1, y1], [xittr, yittr])
                eps = 0.0
                if(distance <= self.radius + eps):
                    thumby.display.setPixel(xittr, yittr, 1)
                yittr += 1
            xittr += 1
            
    def Draw(self): 
        #self.Draw2()
        #return
        right = math.ceil(self.x + self.radius)
        top = math.ceil(self.y + self.radius)
        x = math.floor(self.x - self.radius)
        y = math.floor(self.y - self.radius)
        intradius = int(round(self.radius*2))
        
        bitmap = None
        
        if intradius == 7:
            bitmap = bitmap1
        elif intradius == 9:
            bitmap = bitmap2
        elif intradius == 11:
            bitmap = bitmap3
        elif intradius == 13:
            bitmap = bitmap4
        elif intradius == 15:
            bitmap = bitmap5
        elif intradius == 17:
            bitmap = bitmap6
        elif intradius == 19:
            bitmap = bitmap7    
            
        thumby.display.blit(
            bitmap, 
            int(math.floor(self.x - self.radius)), 
            int(math.floor(self.y - self.radius)), 
            intradius,
            intradius,
            0, # key
            0, # mirrorX
            0) # mirrorY
        #thumby.display.drawRectangle(int(math.floor(self.x - self.radius)), int(math.floor(self.y - self.radius)), int(self.radius*2), int(self.radius*2), 1) # (x, y, w, h, color)
        # pygame.draw.circle(screen, circle_color, position, self.radius)

ParticleList = []
clickPos = []
bHasClick = False
currentCircleID = 0
SizeArray = [ 7.0/2.0, 9.0/2.0, 11.0/2.0, 13.0/2.0, 15.0/2.0, 17.0/2.0, 19.0/2.0 ]
MaxRandomIndex = 2

thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

score = 0

cursorx = wallright / 2

nextpx = wallright + 10
nextpy = wallbottom / 4

randint = random.randint(0, MaxRandomIndex)
randomSize = SizeArray[randint]
pcurrent = Particle(cursorx, 0, 0, 5, randomSize, currentCircleID)
currentCircleID += 1

randint = random.randint(0, MaxRandomIndex)
randomSize = SizeArray[randint]
pnext = Particle(nextpx, nextpy, 0, 5, randomSize, currentCircleID)
currentCircleID += 1


collisionidxcount = 0
collisioncomputemax = 4

# Main game loop
running = True
while running:
    bHasClick = False
    thumby.display.fill(0) # Fill canvas to black
    
    # handle MOUSEBUTTONUP
    if thumby.buttonA.justPressed():
        bHasClick = True
    if thumby.buttonB.justPressed():
        bHasClick = True
            
    cursordelta = 1
    if thumby.buttonL.pressed():
        if cursorx > 0:
            cursorx -= cursordelta
    if thumby.buttonR.pressed():
        if cursorx < wallright:
            cursorx += cursordelta
            
    if (bHasClick):
        # generate circles from the first half of the list
        ParticleList.append(pcurrent)
        # prepare the next circle
        randint = random.randint(0, int(len(SizeArray)/2))
        randomSize = SizeArray[randint]
        pcurrent = pnext
        pnext = Particle(nextpx, nextpy, 0, 5, randomSize, currentCircleID)
        currentCircleID += 1
    
    for ParticleI in ParticleList:
        # simulate and accumulate velocities
        # n against n circles 
        ParticleI.CollideAgainstAll(ParticleList)
    
    # check for combined particles
    for ParticleI in ParticleList:
        if ParticleI.combined != None:
            if ParticleI.combined in ParticleList:
                ParticleList.remove(ParticleI.combined)
            ParticleList.remove(ParticleI)
            newx = ( ParticleI.combined.x + ParticleI.x ) / 2.0
            newy = ( ParticleI.combined.y + ParticleI.y ) / 2.0
            score += math.floor(ParticleI.radius)**2
            if(ParticleI.radius < SizeArray[len(SizeArray)-1]):
                p = Particle(newx, newy, 0, 0, ParticleI.radius + 1.0, currentCircleID)
                currentCircleID += 1
                ParticleList.append(p)
            break
            
    # Game over condition
    for ParticleI in ParticleList:
        if ParticleI.y < -5:
            running = False
            
        
    for ParticleI in ParticleList:
        # update position
        DeltaTime = 1
        ParticleI.MoveParticle(DeltaTime)
        # draw
        ParticleI.Draw()
        
    # draw next circle on top of cursor position
    pcurrent.x = cursorx
    pcurrent.y = 0
    pcurrent.Draw()
    
    pnext.Draw()
    
    thumby.display.drawLine(wallright, 0, wallright, wallbottom, 1)
    
    # render score
    thumby.display.drawText(str(int(score)), wallright + 4, 32, 1)

    thumby.display.update()

# game over text 
thumby.display.fill(0) # Fill canvas to black
thumby.display.drawText("Final Score", 5, 16, 1)
thumby.display.drawText(str(int(score)), 5, 24, 1)
thumby.display.update()

while True:
    if thumby.buttonA.justPressed():
        break
    if thumby.buttonB.justPressed():
        break
# Quit
thumby.reset()


