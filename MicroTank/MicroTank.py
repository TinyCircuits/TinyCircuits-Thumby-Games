import time
import thumby
import math
import random

TANK_SPEED = .2
TANK_ROTATE_SPEED = .02
TANK_RADIUS = 3
TURRET_LEN = 2
BULLET_VELOCITY = .4
LEVEL_COUNT = 10

thumby.display.setFPS(60)
thumby.saveData.setName("MicroTank")

# BITMAP: width: 7, height: 5
arrowBitmap = bytearray([0,2,4,8,4,2,0])

class Game:
    def __init__(self, level=1, lives=3):
        self.player = None
        self.walls = []
        self.enemies = []
        self.currentLevel = level
        self.lives = lives
        self.timeKilled = None
        self.paused = False
        
    def loadLevel(self, level):
        if level == 1:
            self.walls = [
                Wall(thumby.display.width//4 - 5, thumby.display.height//2, 3, thumby.display.width//2),
                Wall(2*thumby.display.width//3 - 5, thumby.display.height//2 - 8, 3, 16)
            ]
            self.player = Tank(TANK_RADIUS + 4, thumby.display.height - TANK_RADIUS - 4, -.5*math.pi, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[(3*thumby.display.width//4 + 10, thumby.display.height//2)])    
            ]
        elif level == 2:
            self.walls = [
                Wall(thumby.display.width//4, thumby.display.height//4 + 3, 5, thumby.display.height//2 - 6),
                Wall(3*thumby.display.width//4 - 5, thumby.display.height//4 + 3, 5, thumby.display.height//2 - 6)
            ]
            self.player = Tank(TANK_RADIUS + 4, thumby.display.height//2, 0, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height//2),
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height - TANK_RADIUS - 4),
                    (thumby.display.width//2, thumby.display.height - TANK_RADIUS - 4),
                    (thumby.display.width//2, TANK_RADIUS + 4),
                    (thumby.display.width - TANK_RADIUS - 4, TANK_RADIUS + 4)
                ])
            ]
        elif level == 3:
            self.walls = [
                Wall(thumby.display.width//2 - 5, thumby.display.height//2 - 5, 10, 10)
            ]
            self.player = Tank(thumby.display.width//4, thumby.display.height//2, 0, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (thumby.display.width - TANK_RADIUS - 4, TANK_RADIUS + 4),
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height - TANK_RADIUS - 4)
                ]),
                Tank(0, 0, 0, patrol=[
                    (3*thumby.display.width//4, thumby.display.height - TANK_RADIUS - 4),
                    (3*thumby.display.width//4, TANK_RADIUS + 4)
                ])
            ]
        elif level == 4:
            self.walls = [
                Wall(0, thumby.display.height//2 - 3, 25, 6),
                Wall(thumby.display.width - 25, thumby.display.height//2 - 3, 25, 6)
            ]
            self.player = Tank(TANK_RADIUS + 4, thumby.display.height//4, 0, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (TANK_RADIUS + 4, 3*thumby.display.height//4),
                    (thumby.display.width - TANK_RADIUS - 4, 3*thumby.display.height//4),
                    (thumby.display.width//2, 3*thumby.display.height//4),
                    (thumby.display.width//2, thumby.display.height//4),
                    (thumby.display.width//2, 3*thumby.display.height//4)
                ])
            ]
        elif level == 5:
            self.walls = [
                Wall(0, 4*TANK_RADIUS, 4*TANK_RADIUS, thumby.display.height - 8*TANK_RADIUS),
                Wall(thumby.display.width//2 - 2*TANK_RADIUS, 4*TANK_RADIUS, 4*TANK_RADIUS, thumby.display.height - 8*TANK_RADIUS),
                Wall(thumby.display.width - 4*TANK_RADIUS, 4*TANK_RADIUS, 4*TANK_RADIUS, thumby.display.height - 8*TANK_RADIUS)
            ]
            self.player = Tank(2*thumby.display.width//3, thumby.display.height - TANK_RADIUS - 3, -3*math.pi/4, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (thumby.display.width//3, TANK_RADIUS + 3),
                    (2*thumby.display.width//3, TANK_RADIUS + 3),
                    (2*thumby.display.width//3, thumby.display.height - TANK_RADIUS - 3),
                    (thumby.display.width//3, thumby.display.height - TANK_RADIUS - 3)
                ])
            ]
        elif level == 6:
            self.walls = [
                Wall(12, thumby.display.height//3 - 1, thumby.display.width - 12, 3),
                Wall(0, 2*thumby.display.height//3 - 1, thumby.display.width - 12, 3)
            ]
            self.player = Tank(thumby.display.width//2, thumby.display.height//2, 0, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (thumby.display.width - TANK_RADIUS - 4, TANK_RADIUS + 4),
                    (TANK_RADIUS + 4, TANK_RADIUS + 4),
                    (TANK_RADIUS + 4, thumby.display.height//2),
                    (thumby.display.width//2 - TANK_RADIUS, thumby.display.height//2),
                    (TANK_RADIUS + 4, thumby.display.height//2),
                    (TANK_RADIUS + 4, TANK_RADIUS + 4)
                ]),
                Tank(0, 0, 0, patrol=[
                    (TANK_RADIUS + 4, thumby.display.height - TANK_RADIUS - 4),
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height - TANK_RADIUS - 4),
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height//2),
                    (thumby.display.width//2 + TANK_RADIUS, thumby.display.height//2),
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height//2),
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height - TANK_RADIUS - 4),
                ])
            ]
        elif level == 7:
            self.walls = [
                Wall(thumby.display.width//4 - 1, 0, 3, thumby.display.height - 12),
                Wall(thumby.display.width//2 - 1, 12, 3, thumby.display.height - 12),
                Wall(3*thumby.display.width//4 - 1, 0, 3, thumby.display.height - 12)
            ]
            self.player = Tank(thumby.display.width//8, TANK_RADIUS + 4, math.pi/2, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (3*thumby.display.width//8, thumby.display.height - TANK_RADIUS - 4),
                    (3*thumby.display.width//8, TANK_RADIUS + 4)
                ]),
                Tank(0, 0, 0, patrol=[
                    (5*thumby.display.width//8, TANK_RADIUS + 4),
                    (5*thumby.display.width//8, thumby.display.height - TANK_RADIUS - 4)
                ]),
                Tank(0, 0, 0, patrol=[
                    (7*thumby.display.width//8, thumby.display.height - TANK_RADIUS - 4),
                    (7*thumby.display.width//8, TANK_RADIUS + 4)
                ])
            ]
        elif level == 8:
            self.walls = [
                Wall(4*TANK_RADIUS, 4*TANK_RADIUS, 8, 8),
                Wall(thumby.display.width - 4*TANK_RADIUS - 8, thumby.display.height - 4*TANK_RADIUS - 8, 8, 8)
            ]
            self.player = Tank(TANK_RADIUS + 4, TANK_RADIUS + 4, math.pi/4, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height - TANK_RADIUS - 4),
                    (TANK_RADIUS + 4, thumby.display.height - TANK_RADIUS - 4),
                    (thumby.display.width - TANK_RADIUS - 4, TANK_RADIUS + 4)
                ])    
            ]
        elif level == 9:
            self.walls = [
                Wall(thumby.display.width//2 - 1, 12, 3, thumby.display.height - 24),
                Wall(12, thumby.display.height//2 - 1, thumby.display.width - 24, 3)
            ]
            self.player = Tank(thumby.display.width//2 + TANK_RADIUS + 4, thumby.display.height//2 - TANK_RADIUS - 4, math.pi/-4, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (TANK_RADIUS + 4, thumby.display.height - TANK_RADIUS - 4),
                    (TANK_RADIUS + 4, TANK_RADIUS + 4),
                    (thumby.display.width - TANK_RADIUS - 4, TANK_RADIUS + 4),
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height - TANK_RADIUS - 4)
                ]),
                Tank(0, 0, 0, patrol=[
                    (thumby.display.width - TANK_RADIUS - 4, thumby.display.height - TANK_RADIUS - 4),
                    (TANK_RADIUS + 4, thumby.display.height - TANK_RADIUS - 4),
                    (TANK_RADIUS + 4, TANK_RADIUS + 4),
                    (thumby.display.width - TANK_RADIUS - 4, TANK_RADIUS + 4),
                ])
            ]
        elif level == 10:
            self.walls = [
                Wall(12, 12, thumby.display.width//2 - 18, 3),
                Wall(thumby.display.width//2 + 6, 12, thumby.display.width//2 - 18, 3),
                Wall(12, thumby.display.height//2 + 6, thumby.display.width//2 - 18, 3),
                Wall(thumby.display.width//2 + 6, thumby.display.height//2 + 6, thumby.display.width//2 - 18, 3)
            ]
            self.player = Tank(thumby.display.width - TANK_RADIUS - 3, thumby.display.height - TANK_RADIUS - 3, math.pi, 2, 2)
            self.enemies = [
                Tank(0, 0, 0, patrol=[
                    (thumby.display.width//2, thumby.display.height//2)
                ]),
                Tank(0, 0, 0, patrol=[
                    (TANK_RADIUS + 3, TANK_RADIUS + 3),
                    (thumby.display.width - TANK_RADIUS - 3, TANK_RADIUS + 3),
                    (thumby.display.width - TANK_RADIUS - 3, thumby.display.height - TANK_RADIUS - 3),
                    (TANK_RADIUS + 3, thumby.display.height - TANK_RADIUS - 3)
                ])
            ]

class Wall:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def draw(self):
        thumby.display.drawFilledRectangle(self.x, self.y, self.w, self.h, 1)

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vx = BULLET_VELOCITY * math.cos(angle)
        self.vy = BULLET_VELOCITY * math.sin(angle)
        self.bounces = 0
        
    def draw(self):
        thumby.display.setPixel(int(self.x), int(self.y), 1)
        

class Tank:
    def __init__(self, x, y, angle, maxBullets=1, maxBounces=1, patrol=[]):
        if len(patrol) == 1:
            x, y = patrol[0]
            nextX, nextY = patrol[0]
        elif len(patrol):
            x, y = patrol[0]
            nextX, nextY = patrol[1]
            angle = math.atan2(nextY - y, nextX - x)
        self.x = x
        self.y = y
        self.angle = angle
        self.turretX = x
        self.turretY = y
        self.bullets = []
        self.hasLOS = False
        self.lockingOn = False
        self.patrol = patrol
        self.stop = 0
        self.maxBullets = maxBullets
        self.maxBounces = maxBounces
        self.dead = False
        
    def draw(self):
        if self.dead:
            return
        if self.x == game.player.x and self.y == game.player.y:
            flipY = self.y <= TANK_RADIUS + TURRET_LEN + 5
            if not flipY:
                arrowSprite = thumby.Sprite(7, 5, arrowBitmap, self.x - 3, self.y - (TANK_RADIUS + TURRET_LEN + 5), -1)
            else:
                arrowSprite = thumby.Sprite(7, 5, arrowBitmap, self.x - 3, self.y + (TANK_RADIUS + TURRET_LEN + 2), -1, 0, 1)
            thumby.display.drawSprite(arrowSprite)
        tCos = math.cos(self.angle)
        tSin = math.sin(self.angle)
        turretX1 = int(self.x + TANK_RADIUS*tCos)
        turretY1 = int(self.y + TANK_RADIUS*tSin)
        self.turretX = turretX2 = int(self.x + (TANK_RADIUS + TURRET_LEN)*tCos)
        self.turretY = turretY2 = int(self.y + (TANK_RADIUS + TURRET_LEN)*tSin)
        
        topLeftCos = TANK_RADIUS * math.cos(self.angle - math.pi/4)
        topLeftSin = TANK_RADIUS * math.sin(self.angle - math.pi/4)
        
        x1 = int(self.x + topLeftCos)
        y1 = int(self.y + topLeftSin)
        
        x2 = int(self.x - topLeftSin)
        y2 = int(self.y + topLeftCos)
        
        x3 = int(self.x + topLeftSin)
        y3 = int(self.y - topLeftCos)
        
        x4 = int(self.x - topLeftCos)
        y4 = int(self.y - topLeftSin)
        
        thumby.display.drawLine(x1, y1, x2, y2, 1)
        thumby.display.drawLine(x2, y2, x4, y4, 1)
        thumby.display.drawLine(x4, y4, x3, y3, 1)
        thumby.display.drawLine(x3, y3, x1, y1, 1)
        thumby.display.drawLine(turretX1, turretY1, turretX2, turretY2, 1)
    
    def fire(self):
        if len(self.bullets) < self.maxBullets:
            self.bullets.append(Bullet(self.turretX, self.turretY, self.angle))
            thumby.audio.play(300, 200)
            
    def move(self, speed):
        newX = self.x + speed*math.cos(self.angle)
        newY = self.y + speed*math.sin(self.angle)
        newX = max(TANK_RADIUS+1, newX)
        newX = min(thumby.display.width-TANK_RADIUS-1, newX)
        newY = max(TANK_RADIUS+1, newY)
        newY = min(thumby.display.height-TANK_RADIUS-1, newY)
        for wall in game.walls:
            if (newX+TANK_RADIUS >= wall.x and newX-TANK_RADIUS <= wall.x + wall.w 
            and newY+TANK_RADIUS >= wall.y and newY - TANK_RADIUS <= wall.y + wall.h):
                if self.x+TANK_RADIUS < wall.x or self.x-TANK_RADIUS > wall.x + wall.w:
                    newX = self.x
                elif self.y+TANK_RADIUS < wall.y or self.y-TANK_RADIUS > wall.y + wall.h:
                    newY = self.y
        for enemy in game.enemies:
            if (self.x != enemy.x and self.y != enemy.y and abs(newX - enemy.x) < TANK_RADIUS*2
            and abs(newY - enemy.y) < TANK_RADIUS*2):
                if self.x+TANK_RADIUS < enemy.x+TANK_RADIUS or self.x-TANK_RADIUS > enemy.x-TANK_RADIUS:
                    newX = self.x
                if self.y+TANK_RADIUS < enemy.y+TANK_RADIUS or self.y-TANK_RADIUS > enemy.y-TANK_RADIUS:
                    newY = self.y
        self.x = newX
        self.y = newY
        
    def rotate(self, speed):
        self.angle += speed
    
    def tick(self):
        self.updateBullets()

    def updateBullets(self):
        newBullets = []
        for bullet in self.bullets:
            newX = bullet.x + bullet.vx
            if newX <= 1 or newX >= thumby.display.width-1:
                bullet.vx = -1 * bullet.vx
                newX = bullet.x + bullet.vx
                bullet.bounces += 1
                thumby.audio.play(1000, 50)
            newY = bullet.y + bullet.vy
            if newY <= 1 or newY >= thumby.display.height-1:
                bullet.vy = -1 * bullet.vy
                newY = bullet.y + bullet.vy
                bullet.bounces += 1
                thumby.audio.play(1000, 50)
            for wall in game.walls:
                if newX >= wall.x and newX <= wall.x + wall.w and newY >= wall.y and newY <= wall.y + wall.h:
                    if bullet.x < wall.x or bullet.x > wall.x + wall.w:
                        bullet.vx = -1 * bullet.vx
                        newX = bullet.x + bullet.vx
                    elif bullet.y < wall.y or bullet.y > wall.y + wall.h:
                        bullet.vy = -1 * bullet.vy
                        newY = bullet.y + bullet.vy
                    bullet.bounces += 1
                    thumby.audio.play(1000, 50)
            bullet.x = newX
            bullet.y = newY
            hit = False
            if bullet.x <= game.player.x+TANK_RADIUS and bullet.x >= game.player.x-TANK_RADIUS and bullet.y <= game.player.y+TANK_RADIUS and bullet.y >= game.player.y-TANK_RADIUS:
                hit = True
                game.player.dead = True
                game.timeKilled = time.ticks_ms()
                thumby.audio.play(800, 200)
            for enemy in game.enemies:
                if not enemy.dead and bullet.x <= enemy.x+TANK_RADIUS and bullet.x >= enemy.x-TANK_RADIUS and bullet.y <= enemy.y+TANK_RADIUS and bullet.y >= enemy.y-TANK_RADIUS:
                    hit = True
                    enemy.dead = True
                    thumby.audio.play(1200, 200)
            if bullet.bounces < self.maxBounces and not hit:
                newBullets.append(bullet)
        self.bullets = newBullets

    def testLOS(self):
        if self.dead:
            return
        angle = math.atan2(game.player.y - self.y, game.player.x - self.x)
        stepX = 2*math.cos(angle)
        stepY = 2*math.sin(angle)
        x, y = self.x, self.y
        while (self.x <= x <= game.player.x or self.x >= x >= game.player.x) and (self.y <= y <= game.player.y or self.y >= y >= game.player.y):
            for wall in game.walls:
                if x >= wall.x and x <= wall.x + wall.w and y >= wall.y and y <= wall.y + wall.h:
                    self.hasLOS = False
                    return
            x += stepX
            y += stepY
        self.hasLOS = True
        return
    
    def ai(self):
        self.updateBullets()
        if self.dead:
            return
        if self.hasLOS and not self.lockingOn:
            self.lockingOn = random.random() <= .04
        if self.hasLOS and self.lockingOn:
            angle = math.atan2(game.player.y - self.y, game.player.x - self.x)
            diff = (angle - self.angle + math.pi) % (2*math.pi) - math.pi
            if abs(diff) <= TANK_ROTATE_SPEED:
                self.angle = angle
                self.fire()
            else:
                if diff > 0:
                    self.rotate(TANK_ROTATE_SPEED)
                else:
                    self.rotate(TANK_ROTATE_SPEED * -1)
        else:
            self.lockingOn = False
            stopX, stopY = self.patrol[self.stop]
            if abs(self.x - stopX) <= TANK_SPEED and abs(self.y - stopY) <= TANK_SPEED:
                self.x = stopX
                self.y = stopY
                self.stop = (self.stop + 1) % len(self.patrol)
            else:
                angle = math.atan2(stopY - self.y, stopX - self.x)
                diff = (angle - self.angle + math.pi) % (2*math.pi) - math.pi
                if abs(diff) <= TANK_ROTATE_SPEED:
                    self.angle = angle
                    self.move(TANK_SPEED)
                else:
                    if diff > 0:
                        self.rotate(TANK_ROTATE_SPEED)
                    else:
                        self.rotate(TANK_ROTATE_SPEED * -1)


def cleanup():
    newEnemies = []
    for enemy in game.enemies:
        if not enemy.dead or len(enemy.bullets):
            newEnemies.append(enemy)
    game.enemies = newEnemies

def gameLoop():
    frame = 0
    while(1):
        t0 = time.ticks_ms()   # Get time (ms)
        if game.player.dead:
            if t0 - game.timeKilled > 1000:
                game.lives -= 1
                return
            continue
        thumby.display.fill(0) # Fill canvas to black
        if game.paused:
            thumby.display.drawText("-Paused-", 12, thumby.display.height // 2 - 3, 1)
            thumby.display.update()
            if thumby.buttonB.justPressed() or thumby.buttonA.justPressed():
                game.paused = False
            continue
        cleanup()
        if not len(game.enemies):
            game.currentLevel += 1
            return
        
        # control
        if thumby.buttonB.justPressed():
            game.paused = True
            continue
        if thumby.buttonL.pressed():
            game.player.rotate(TANK_ROTATE_SPEED * -1)
        elif thumby.buttonR.pressed():
            game.player.rotate(TANK_ROTATE_SPEED)
        if thumby.buttonU.pressed():
            game.player.move(TANK_SPEED)
        elif thumby.buttonD.pressed():
            game.player.move(TANK_SPEED * -1)
        
        game.player.tick()
        
        if len(game.enemies):
            enemyToTest = game.enemies[frame % len(game.enemies)]
            enemyToTest.testLOS()
        for enemy in game.enemies:
            enemy.ai()
    
        if thumby.buttonA.justPressed():
            game.player.fire()
        
        # drawing
        for wall in game.walls:
            wall.draw()
        game.player.draw()
        for enemy in game.enemies:
            enemy.draw()
            for bullet in enemy.bullets:
                bullet.draw()
        for bullet in game.player.bullets:
            bullet.draw()
        thumby.display.drawRectangle(0, 0, thumby.display.width, thumby.display.height, 1)
        thumby.display.update()
        frame += 1
        
# BITMAP: width: 8, height: 8
heartBitmap = bytearray([30,63,126,252,252,126,63,30])

def gameControlLoop():
    tEntered = time.ticks_ms()
    while(1):
        t = time.ticks_ms()
        thumby.buttonA.justPressed()
        thumby.display.fill(0)
        if game.lives <= 0:
            thumby.display.drawText("Game over :(", 1, thumby.display.height//2 - 3, 1)
            if t - tEntered > 3000:
                return
        elif game.currentLevel > LEVEL_COUNT:
            result = (tEntered - runStart) / 1000
            best = float("inf")
            if thumby.saveData.hasItem("best"):
                best = float(thumby.saveData.getItem("best"))
            if result < best:
                best = result
                thumby.saveData.setItem("best", best)
            thumby.saveData.save()
            thumby.display.drawText("You win!", 0, 0, 1)
            thumby.display.drawText(f"{result:.2f} sec", 0, 8, 1)
            thumby.display.drawText("Best:", 0, 18, 1)
            thumby.display.drawText(f"{best:.2f} sec", 0, 26, 1)
            if t - tEntered > 5000:
                return
        else:
            thumby.display.drawText(f"Level {game.currentLevel}", 14, 8, 1)
            for i in range(game.lives):
                heart = thumby.Sprite(8, 8, heartBitmap, 21+(i*10), 20, 0)
                thumby.display.drawSprite(heart)
        thumby.display.update()
        if t - tEntered > 3000:
            game.loadLevel(game.currentLevel)
            gameLoop()
            tEntered = time.ticks_ms()

# BITMAP: width: 72, height: 20
titleBitmap = bytearray([15,225,226,225,239,224,239,224,239,233,233,233,224,239,225,225,225,224,15,9,9,15,0,0,0,128,224,224,240,224,128,0,0,0,0,0,0,224,224,224,224,224,224,192,128,0,0,224,224,224,224,224,224,224,0,96,224,224,224,224,224,224,224,0,224,224,224,224,224,224,0,0,
           0,3,3,3,0,128,128,255,255,255,255,128,128,128,0,3,3,3,0,128,128,192,240,252,255,127,119,115,127,255,255,254,248,224,128,128,0,128,128,255,255,255,135,143,31,63,126,252,248,255,255,255,0,0,0,0,128,255,255,255,255,188,190,127,255,243,225,192,128,128,128,0,
           0,0,0,0,0,3,3,3,3,3,3,3,3,3,0,0,0,0,3,3,3,3,3,3,3,0,0,0,0,3,3,3,3,3,3,3,0,3,3,3,3,3,3,3,0,0,0,0,1,3,3,3,0,0,0,3,3,3,3,3,3,3,3,0,0,1,3,3,3,3,3,0])
# BITMAP: width: 16, height: 4
versionBitmap = bytearray([6,8,6,0,0,9,15,8,0,8,0,15,9,15,0,0])

while(1):
    t = time.ticks_ms()
    if thumby.buttonA.justPressed():
        random.seed(t)
        game = Game()
        runStart = t
        gameControlLoop()
    thumby.display.fill(0)
    title = thumby.Sprite(72, 20, titleBitmap, 0, 0, 0)
    thumby.display.drawSprite(title)
    if t % 2000 < 1000:
        thumby.display.drawText("A to start", 7, 24, 1)
    version = thumby.Sprite(16, 4, versionBitmap, thumby.display.width - 16, thumby.display.height - 4, 0)
    thumby.display.drawSprite(version)
    thumby.display.update()
    
