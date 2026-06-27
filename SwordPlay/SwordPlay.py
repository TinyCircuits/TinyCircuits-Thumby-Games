# Sword Play
# Written by: Ian Johnson
# Last Updated: 12 March 2024

import math
import random
import thumby
const = __import__('/Games/SwordPlay/constants')
gamepad = __import__('/Games/SwordPlay/gamepad')

__version__ = '1.0'

# -- GRAPHICS --

# BITMAP: width: 68, height: 15
BMP_TITLE_LOGO = bytearray([28,62,115,227,199,130,0,0,224,240,0,224,240,0,240,0,0,160,48,48,112,224,128,0,32,224,240,64,32,240,96,0,196,230,46,12,28,248,224,0,0,2,255,255,3,135,254,120,0,2,254,255,0,0,32,32,112,224,128,0,0,32,224,240,128,32,48,224,8,28,24,24,9,15,7,0,3,15,28,7,15,28,7,0,3,15,28,24,8,15,7,0,0,31,31,16,0,0,0,0,3,15,28,24,8,15,7,0,0,0,31,15,0,0,0,0,0,0,31,15,0,14,31,25,9,3,31,14,0,0,64,103,63,28,6,1])

SPR_ENEMY_MONSTER = thumby.Sprite(8, 8, bytearray([0,0,84,56,40,56,84,0]), key=0)
SPR_ENEMY_MUTANT = thumby.Sprite(8, 8, bytearray([0,40,186,108,68,108,186,40]), key=0)

SPR_MENU_ARROW = thumby.Sprite(6, 3, bytearray([4,6,7,7,6,4]) + bytearray([0,6,7,7,6,0]) + bytearray([0,0,7,7,0,0]), key=0)

SPR_PICKUP_HEALTH = thumby.Sprite(8, 8, bytearray([0,28,62,126,252,126,62,28]), key=0)
SPR_PICKUP_POINTS = thumby.Sprite(8, 8, bytearray([0,56,68,186,186,186,68,56]), key=0)

SPR_PLAYER = thumby.Sprite(8, 8, bytearray([0,192,240,252,254,252,240,192]) + bytearray([0,6,30,126,254,126,30,6]) + bytearray([0,16,56,56,124,124,254,254]) + bytearray([0,254,254,124,124,56,56,16]), key=0)

SPR_TUTORIAL_ARROW = thumby.Sprite(6, 6, bytearray([8,24,63,63,24,8]), key=0)

# -- DEBUG --

def debugDrawGrid():
    for y in range(const.GRID_MIN_PY, const.GRID_MAX_PY + 1, const.GRID_SIZE):
        for x in range(const.GRID_MIN_PX, const.GRID_MAX_PX + 1, const.GRID_SIZE):
            thumby.display.setPixel(x, y, 1)

def debugDrawEnemySpawnPoints(gameState):
    for x, y in gameState.getEnemySpawnPoints():
        thumby.display.drawLine(x, y - const.ENEMY_RESPAWN_OFFSET_Y, x, y + const.ENEMY_RESPAWN_OFFSET_Y, 1)

def debugDrawPickupSpawnPoints(gameState):
    for x, y in gameState.getPickupSpawnPoints():
        thumby.display.drawRectangle(x - 1, y - 1, 3, 3, 1)

# -- UTILITIES --

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def drawCenterText(text, x, y, color):
    cx = x - (thumby.display.textWidth + thumby.display.textSpaceWidth) * len(text) // 2
    thumby.display.drawText(text, cx, y, color)

def textWidth(text, textWidth = None, textSpaceWidth = None):
    if textWidth is None: textWidth = thumby.display.textWidth
    if textSpaceWidth is None: textSpaceWidth = thumby.display.textSpaceWidth
    return len(text) * (textWidth + textSpaceWidth) - textSpaceWidth

def toGridPos(px, py):
    gx = ((const.GRID_SIZE // 2) + px - const.GRID_OFFSET_X) // const.GRID_SIZE
    gy = ((const.GRID_SIZE // 2) + py - const.GRID_OFFSET_Y) // const.GRID_SIZE
    return gx, gy

def toPixelPos(gx, gy):
    px = gx * const.GRID_SIZE + const.GRID_OFFSET_X
    py = gy * const.GRID_SIZE + const.GRID_OFFSET_Y
    return px, py

def isHighScore(score):
    return score > thumby.saveData.getItem(const.SAVE_DATA_LEADER_SCORES)[-1]

# -- GENERATORS --

def genSequenceLoop(seq, rate = 1):
    while True:
        for val in seq:
            for i in range(rate):
                yield val

def genPulse(rate):
    while True:
        for i in range(rate):
            yield i == 0

# -- UI ELEMENTS --

class Menu:
    def __init__(self, items, x, y, default = 0):
        self.items = items
        self.x, self.y = x, y
        self.selectedIndex = default
        self.resetAnimation()
    
    def resetAnimation(self):
        self.__arrowSpinAnimation = genSequenceLoop((0, 0, 1, 2, 1), 4)
        self.__arrowBobbingAnimation = genSequenceLoop((0, 1, 2, 1), 5)
        
    def update(self):
        if gamepad.buttonU.justPressed():
            self.selectedIndex = (self.selectedIndex - 1) % len(self.items)
        if gamepad.buttonD.justPressed():
            self.selectedIndex = (self.selectedIndex + 1) % len(self.items)
    
    def draw(self):
        drawCenterText(self.items[self.selectedIndex], self.x, self.y, 1)
        
        bobbingOffset = next(self.__arrowBobbingAnimation)
        
        SPR_MENU_ARROW.setFrame(next(self.__arrowSpinAnimation))
        SPR_MENU_ARROW.x, SPR_MENU_ARROW.y = self.x - SPR_MENU_ARROW.width // 2, self.y - SPR_MENU_ARROW.height - 1 - bobbingOffset
        SPR_MENU_ARROW.mirrorX, SPR_MENU_ARROW.mirrorY = 0, 0
        thumby.display.drawSprite(SPR_MENU_ARROW)
        
        SPR_MENU_ARROW.y = self.y + thumby.display.textHeight + 1 + bobbingOffset
        SPR_MENU_ARROW.mirrorY = 1
        thumby.display.drawSprite(SPR_MENU_ARROW)

class HealthBar:
    def __init__(self, x, y, width, height, mob):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.mob = mob
    
    def draw(self):
        for i in range(self.mob.hpMax):
            x, y = self.x, self.y + (self.height + 1) * i
            if i < self.mob.hp:
                thumby.display.drawFilledRectangle(x, y, self.width, self.height, 1)
            else:
                thumby.display.drawRectangle(x, y, self.width, self.height, 1)

class ProgressBar:
    def __init__(self, x, y, width, height, capacity, progress = 0):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.capacity = capacity
        self.progress = progress
    
    def reset(self):
        self.progress = 0
    
    def increment(self, step = 1, rollover = False):
        self.progress += step
        if rollover:
            count = 0
            while self.progress >= self.capacity:
                self.progress -= self.capacity
                count += 1
            return count
        else:
            self.progress = min(self.progress, self.capacity)
            return 1 if (self.progress == self.capacity) else 0
    
    def draw(self):
        progressHeight = int((self.height - 2) * self.progress / self.capacity)
        thumby.display.drawRectangle(self.x, self.y, self.width, self.height, 1)
        thumby.display.drawFilledRectangle(self.x, self.y + self.height - progressHeight - 1, self.width, progressHeight, 1)

# -- GAME OBJECTS --

# Core

class GameObject:
    def __init__(self, x, y, sprite, hitSize):
        self.sprite = sprite
        self.x, self.y = x, y
        self.hitSize = hitSize
        self.visible = True
    
    def getPixelPos(self):
        return self.x, self.y
    
    def getGridPos(self):
        return toGridPos(self.x, self.y)
    
    def collidesWith(self, obj):
        if isinstance(self, Mob) and isinstance(obj, Mob):
            if self.isInvincible() or obj.isInvincible():
                return False
        return distance(self.x, self.y, obj.x, obj.y) <= self.hitSize + obj.hitSize + 0.5
    
    def update(self):
        pass
    
    def draw(self):
        if self.visible:
            self.sprite.x, self.sprite.y = self.x - self.sprite.width // 2, self.y - self.sprite.height // 2
            thumby.display.drawSprite(self.sprite)

class Mob(GameObject):
    def __init__(self, x, y, sprite, hitSize, hpMax):
        super().__init__(x, y, sprite, hitSize)
        self.hp = hpMax
        self.hpMax = hpMax
        self.invincibilityFrames = 0
    
    def update(self):
        if self.invincibilityFrames > 0:
            self.invincibilityFrames -= 1
    
    def draw(self):
        if self.invincibilityFrames % 2 == 0:
            super().draw()
    
    def isInvincible(self):
        return self.invincibilityFrames > 0
    
    def heal(self, hp = None):
        self.hp = self.hpMax if (hp is None) else min(self.hp + hp, self.hpMax)
    
    def damage(self, dmg, invincibilityFrames = 0):
        if not self.isInvincible():
            self.hp = max(self.hp - dmg, 0)
            self.invincibilityFrames = invincibilityFrames
            return True
        return False

class Enemy(Mob):
    def __init__(self, x, y, sprite, hitSize, hpMax, points, moveRate, attackDamage):
        super().__init__(x, y, sprite, hitSize, hpMax)
        self.points = points
        self.attackDamage = attackDamage
        self.targetX, self.targetY = x, y
        self.pauseMoves = 0
        self.__moveRate = moveRate
        self.__movePulse = genPulse(moveRate)
    
    def setReturnToGrid(self):
        gx, gy = self.getGridPos()
        tx, ty = toPixelPos(max(min(gx, const.GRID_WIDTH), 0), max(min(gy, const.GRID_HEIGHT), 0))
        self.__setMoveTowardsTarget(tx, ty, False)
    
    def __setNoMovement(self):
        self.pauseMoves = const.GRID_SIZE
    
    def __setRandomMove(self):
        gx, gy = self.getGridPos()
        moves = [
            move
            for move in [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
            if 0 <= gx + move[0] <= const.GRID_WIDTH and 0 <= gy + move[1] <= const.GRID_HEIGHT
        ]
        dx, dy = random.choice(moves)
        self.targetX, self.targetY = toPixelPos(gx + dx, gy + dy)
    
    def __setMoveTowardsTarget(self, targetX, targetY, clamp = True):
        gx, gy = self.getGridPos()
        tgx, tgy = toGridPos(targetX, targetY)
        dx, dy = tgx - gx, tgy - gy
        if clamp:
            dx, dy = max(min(dx, 1), -1), max(min(dy, 1), -1)
        self.targetX, self.targetY = toPixelPos(gx + dx, gy + dy)
    
    def __decideMove(self, gameState):
        raise NotImplementedError(f"class '{type(self).__name__}' must override 'Enemy.__decideMove()'")
    
    def update(self, gameState):
        super().update()
        
        if next(self.__movePulse):
            # don't move if paused
            if self.pauseMoves > 0:
                self.pauseMoves -= 1
                return
            
            # pick a new movement if reached target
            if self.x == self.targetX and self.y == self.targetY:
                self.__decideMove(gameState)
            
            # move towards target
            if self.y > self.targetY: self.y -= 1
            if self.y < self.targetY: self.y += 1
            if self.x > self.targetX: self.x -= 1
            if self.x < self.targetX: self.x += 1

class Pickup(GameObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite, const.PICKUP_HIT_SIZE)
        self.flashingAnimation = genSequenceLoop((True, False), const.PICKUP_FLASH_RATE // 2)
    
    def activateEffect(self, gameState):
        raise NotImplementedError(f"class '{type(self).__name__}' must override 'Pickup.activateEffect()'")
    
    def draw(self):
        if next(self.flashingAnimation):
            super().draw()

# Player

class Player(Mob):
    def __init__(self, x, y, direction = const.DIR_R):
        super().__init__(x, y, SPR_PLAYER, const.PLAYER_HIT_SIZE, const.PLAYER_MAX_HP)
        self.direction = direction
        self.swingingSword = False
        self.swordAngle = 0
        self.swordTargetAngle = 0
    
    def collidesWithSword(self, obj):
        if self.swingingSword:
            if isinstance(obj, Mob) and obj.isInvincible():
                return False
            if distance(self.x, self.y, obj.x, obj.y) < const.SWORD_LENGTH + obj.hitSize:
                objAngle = math.atan2(obj.y - self.y, obj.x - self.x)
                angleDiff = abs(math.radians(self.swordAngle) - objAngle)
                if angleDiff > math.pi:
                    angleDiff = 2 * math.pi - angleDiff
                return angleDiff < const.SWORD_SWING_COLLISION_TOLERANCE
        return False
    
    def swingSword(self):
        self.swingingSword = True
        if self.direction == const.DIR_U: self.swordAngle = 270 - const.SWORD_SWING_ARC // 2
        if self.direction == const.DIR_D: self.swordAngle =  90 - const.SWORD_SWING_ARC // 2
        if self.direction == const.DIR_L: self.swordAngle = 180 - const.SWORD_SWING_ARC // 2
        if self.direction == const.DIR_R: self.swordAngle =   0 - const.SWORD_SWING_ARC // 2
        self.swordTargetAngle = self.swordAngle + const.SWORD_SWING_ARC
    
    def update(self, acceptInput = True):
        super().update()
        
        if self.swingingSword:
            if self.swordAngle >= self.swordTargetAngle:
                self.swingingSword = False
            else:
                self.swordAngle += const.SWORD_SWING_SPEED
        elif acceptInput:
            # move
            if gamepad.buttonU.pressed():
                self.y -= 1
                self.direction = const.DIR_U
            if gamepad.buttonD.pressed():
                self.y += 1
                self.direction = const.DIR_D
            if gamepad.buttonL.pressed():
                self.x -= 1
                self.direction = const.DIR_L
            if gamepad.buttonR.pressed():
                self.x += 1
                self.direction = const.DIR_R
            self.x = max(min(self.x, const.GRID_MAX_PX), const.GRID_MIN_PX)
            self.y = max(min(self.y, const.GRID_MAX_PY), const.GRID_MIN_PY)
            
            # swing sword
            if gamepad.buttonA.justPressed():
                self.swingSword()
    
    def draw(self):
        # draw player
        self.sprite.setFrame(self.direction)
        super().draw()
        
        # draw sword
        if self.swingingSword:
            rad = math.radians(self.swordAngle)
            x1 = int(const.SWORD_DISTANCE * math.cos(rad)) + self.x
            y1 = int(const.SWORD_DISTANCE * math.sin(rad)) + self.y
            x2 = int(const.SWORD_LENGTH * math.cos(rad)) + self.x
            y2 = int(const.SWORD_LENGTH * math.sin(rad)) + self.y
            thumby.display.drawLine(x1, y1, x2, y2, 1)

# Enemies

class Monster(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, SPR_ENEMY_MONSTER,
            const.ENEMY_MONSTER_HIT_SIZE,
            const.ENEMY_MONSTER_HP_MAX,
            const.ENEMY_MONSTER_POINTS,
            const.ENEMY_MONSTER_MOVE_RATE,
            const.ENEMY_MONSTER_DAMAGE
        )
    
    def __decideMove(self, gameState):
        choice = random.randrange(100)
        if choice < 50:     # 50%
            self.__setRandomMove()
        elif choice < 70:   # 20%
            self.__setMoveTowardsTarget(gameState.player.x, gameState.player.y)
        else:               # 30%
            self.__setNoMovement()

class Mutant(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, SPR_ENEMY_MUTANT,
            const.ENEMY_MUTANT_HIT_SIZE,
            const.ENEMY_MUTANT_HP_MAX,
            const.ENEMY_MUTANT_POINTS,
            const.ENEMY_MUTANT_MOVE_RATE,
            const.ENEMY_MUTANT_DAMAGE
        )
    
    def __decideMove(self, gameState):
        if distance(self.x, self.y, gameState.player.x, gameState.player.y) < const.ENEMY_MUTANT_CHARGE_DIST:
            self.__setMoveTowardsTarget(gameState.player.x, gameState.player.y)
        else:
            choice = random.randrange(100)
            if choice < 60:     # 60%
                self.__setRandomMove()
            elif choice < 90:   # 30%
                self.__setMoveTowardsTarget(gameState.player.x, gameState.player.y)
            else:               # 10%
                self.__setNoMovement()

# Pickups

class HealthPickup(Pickup):
    def __init__(self, x, y):
        super().__init__(x, y, SPR_PICKUP_HEALTH)
    
    def activateEffect(self, gameState):
        gameState.player.heal(const.PICKUP_HEALTH_EFFECT)

class PointsPickup(Pickup):
    def __init__(self, x, y):
        super().__init__(x, y, SPR_PICKUP_POINTS)
    
    def activateEffect(self, gameState):
        gameState.score += const.PICKUP_POINTS_EFFECT

# -- MAIN GAMEPLAY --

class GameState:
    def __init__(self, player, enemies, pickup):
        self.player = player
        self.enemies = enemies
        self.pickup = pickup
        self.score = 0
        
        self.healthBar = HealthBar(67, 1, 4, 4, self.player)
        self.prizeProgress = ProgressBar(67, 22, 4, 17, const.KILLS_PER_PRIZE)
    
    def getEnemySpawnPoints(self):
        spawnPoints = [
            (x, y)
            for y in (const.GRID_MIN_PY - const.ENEMY_RESPAWN_OFFSET_Y, const.GRID_MAX_PY + const.ENEMY_RESPAWN_OFFSET_Y)
            for x in range(const.GRID_MIN_PX, const.GRID_MAX_PX + 1, const.GRID_SIZE)
        ]
        spawnPoints.sort(reverse = True, key = lambda pos : distance(pos[0], pos[1], self.player.x, self.player.y))
        spawnPoints = spawnPoints[:len(spawnPoints) // 2]
        return spawnPoints
    
    def respawnEnemy(self, enemy):
        enemy.x, enemy.y = random.choice(self.getEnemySpawnPoints())
        enemy.setReturnToGrid()
        enemy.invincibilityFrames = const.ENEMY_RESPAWN_OFFSET_Y * enemy.__moveRate  # invincible until back on grid
        enemy.hp = enemy.hpMax
    
    def getPickupSpawnPoints(self):
        spawnPoints = [
            toPixelPos(x, y)
            for y in (1, const.GRID_HEIGHT - 1)
            for x in (1, const.GRID_WIDTH - 1)
        ]
        spawnPoints.sort(reverse = True, key = lambda pos : distance(pos[0], pos[1], self.player.x, self.player.y))
        spawnPoints = spawnPoints[:len(spawnPoints) // 2]
        return spawnPoints
    
    def spawnPickup(self):
        x, y = random.choice(self.getPickupSpawnPoints())
        if self.player.hp == self.player.hpMax:
            self.pickup = PointsPickup(x, y)
        else:
            self.pickup = HealthPickup(x, y)
    
    def update(self):
        # update game opbjects
        self.player.update()
        for enemy in self.enemies:
            enemy.update(self)
        if self.pickup:
            self.pickup.update()
        
        # handle collisions
        if self.pickup and self.player.collidesWith(self.pickup):
            self.pickup.activateEffect(self)
            self.pickup = None
        for enemy in self.enemies:
            if self.player.collidesWithSword(enemy):
                enemy.damage(const.SWORD_DAMAGE, const.ENEMY_INVINCIBILITY_FRAMES)
                enemy.pauseMoves = int(math.ceil(const.ENEMY_INVINCIBILITY_FRAMES / enemy.__moveRate))  # pause aftertaking damage
            if self.player.collidesWith(enemy):
                self.player.damage(enemy.attackDamage, const.PLAYER_INVINCIBILITY_FRAMES)
            
            if enemy.hp <= 0:
                self.score += enemy.points
                if self.prizeProgress.increment(rollover = True):
                    self.spawnPickup()
                self.respawnEnemy(enemy)
    
    def draw(self):
        # draw game opbjects
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        if self.pickup:
            self.pickup.draw()
        
        # draw UI
        thumby.display.drawFilledRectangle(65, 0, 7, 40, 0)
        thumby.display.drawLine(65, 0, 65, 40, 1)
        self.healthBar.draw()
        self.prizeProgress.draw()

def newGameAnimation(gameState):
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    thumby.display.fill(0)
    gameState.draw()
    
    text = (' 3 ', ' 2 ', ' 1 ', 'GO!')
    w, h = textWidth(text[0], 3, 1) + 4, 9
    x, y = const.GRID_MID_PX - w // 2, 16
    for i in range(len(text) * const.FPS):
        thumby.display.drawFilledRectangle(x, y, w, h, 0)
        thumby.display.drawRectangle(x, y, w, h, 1)
        drawCenterText(text[i // const.FPS], const.GRID_MID_PX + 1, y + 2, 1)
        thumby.display.update()

def pauseGame(gameState):
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    text = 'PAUSED'
    w, h = textWidth(text, 3, 1) + 4, 9
    x, y = const.GRID_MID_PX - w // 2, 5
    thumby.display.drawFilledRectangle(x, y, w, h, 0)
    thumby.display.drawRectangle(x, y, w, h, 1)
    drawCenterText(text, const.GRID_MID_PX + 1, y + 2, 1)
    
    text = 'SCORE'
    scoreText = f"{min(gameState.score, const.SCORE_DISPLAY_CAP)}"
    w, h = max(textWidth(text, 3, 1), textWidth(scoreText, 5, 1)) + 4, 17
    x, y = const.GRID_MID_PX - w // 2, 18
    thumby.display.drawFilledRectangle(x, y, w, h, 0)
    thumby.display.drawRectangle(x, y, w, h, 1)
    drawCenterText(text, const.GRID_MID_PX + 1, y + 2, 1)
    
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    drawCenterText(scoreText, const.GRID_MID_PX + 1, y + 8, 1)
    
    gamepad.clearBuffer()
    while not gamepad.actionJustPressed():
        gamepad.update()
        thumby.display.update()

def gameOverAnimation(gameState):
    gameState.player.visible = True
    gameState.player.invincibilityFrames = 0
    gameState.player.swingingSword = False
    for enemy in gameState.enemies:
        enemy.visible = False
    gameState.pickup = None
    
    spinningAnimation = genSequenceLoop((const.DIR_U, const.DIR_R, const.DIR_D, const.DIR_L), const.GAME_OVER_ANIM_SPIN_RATE)
    for i in range(const.GAME_OVER_ANIM_DURATION):
        gameState.player.direction = next(spinningAnimation)
        
        thumby.display.fill(0)
        gameState.draw()
        thumby.display.update()

def showGameResults(gameState):
    flashingAnimation = genSequenceLoop((1, 0), const.FLASHING_TEXT_INTERVAL)
    
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    drawCenterText('SCORE', 36, 20, 1)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    drawCenterText(f"{min(gameState.score, const.SCORE_DISPLAY_CAP)}", 36, 28, 1)
    
    gamepad.clearBuffer()
    while not gamepad.actionJustPressed():
        drawCenterText('GAME OVER', 36, 4, next(flashingAnimation))
        gamepad.update()
        thumby.display.update()

def enterName():
    currentLetterIndex = 0
    nameLetters = [i for i in thumby.saveData.getItem(const.SAVE_DATA_PREV_NAME)]
    alphabet = list(map(chr, range(ord('A'), ord('Z') + 1)))  # list of A-Z
    letterChooser = Menu(alphabet, 23, 25, default = ord(nameLetters[0]) - ord('A'))
    
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("NEW", 27, 2, 1)
    thumby.display.drawText("HIGH SCORE", 6, 10, 1)
    
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
    gamepad.clearBuffer()
    while True:
        # input
        gamepad.update()
        if gamepad.buttonL.justPressed():
            currentLetterIndex = max(currentLetterIndex - 1, 0)
            letterChooser.selectedIndex = ord(nameLetters[currentLetterIndex]) - ord('A')
        if gamepad.buttonR.justPressed():
            currentLetterIndex = min(currentLetterIndex + 1, len(nameLetters) - 1)
            letterChooser.selectedIndex = ord(nameLetters[currentLetterIndex]) - ord('A')
        if gamepad.buttonA.justPressed():
            break
        
        # update & draw
        thumby.display.drawFilledRectangle(0, 19, 72, 21, 0)  # just clear the screen where the letter chooser is drawn
        for i in range(len(nameLetters)):
            x, y = 36 + ((thumby.display.textWidth + thumby.display.textSpaceWidth) * (i - 1)), 25
            if i == currentLetterIndex:
                letterChooser.x, letterChooser.y = x, y
                letterChooser.update()
                nameLetters[i] = chr(ord('A') + letterChooser.selectedIndex)
                letterChooser.draw()
            else:
                drawCenterText(nameLetters[i], x, y, 1)
        thumby.display.update()
    
    name = ''.join(nameLetters)
    thumby.saveData.setItem(const.SAVE_DATA_PREV_NAME, name)
    return name

def saveHighScore(newName, newScore):
    leaderNames = thumby.saveData.getItem(const.SAVE_DATA_LEADER_NAMES)
    leaderScores = thumby.saveData.getItem(const.SAVE_DATA_LEADER_SCORES)
    
    for i, leaderScore in enumerate(leaderScores):
        if newScore > leaderScore:
            leaderNames.insert(i, newName)
            leaderScores.insert(i, newScore)
            thumby.saveData.setItem(const.SAVE_DATA_LEADER_NAMES, leaderNames[0:3])
            thumby.saveData.setItem(const.SAVE_DATA_LEADER_SCORES, leaderScores[0:3])
            thumby.saveData.save()
            showLeaderboard(highlight = i + 1)
            return True
    return False

# -- MAIN MENU ITEMS --

def onKonamiCode():
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    thumby.display.fill(0)
    thumby.display.drawText("Sean,             ", 0,  0, 1)
    thumby.display.drawText("  Thanks for the  ", 0,  8, 1)
    thumby.display.drawText("Thumby and the    ", 0, 14, 1)
    thumby.display.drawText("idea to recreate  ", 0, 20, 1)
    thumby.display.drawText("my old game on it!", 0, 26, 1)
    thumby.display.drawText("              -Ian", 0, 34, 1)
    
    gamepad.clearBuffer()
    while not gamepad.actionJustPressed():
        gamepad.update()
        thumby.display.update()

def startGame():
    gameState = GameState(
        Player(10, 20),
        [Monster(47, 7), Monster(47, 20), Monster(47, 32), Mutant(57, 20)],
        None
    )
    
    newGameAnimation(gameState)  # makes new game less sudden
    
    # primary game loop
    gamepad.clearBuffer()
    while gameState.player.hp > 0:
        # input
        gamepad.update()
        if gamepad.buttonB.justPressed():
            pauseGame(gameState)
            continue
        
        # update
        gameState.update()
        
        # draw
        thumby.display.fill(0)
        gameState.draw()
        thumby.display.update()
    
    gameOverAnimation(gameState)  # makes game over less sudden
    showGameResults(gameState)
    if isHighScore(gameState.score):
        name = enterName()
        saveHighScore(name, gameState.score)

def showTutorial():
    pageObjects = {'id': None}
    
    def inputPage(pageObjects):
        if pageObjects['id'] != 'input':
            pageObjects.clear()
            pageObjects.update({ 'id': 'input' })
        
        thumby.display.drawText("INPUT", 0, 0, 1)
        thumby.display.drawText("Use the D-Pad", 0, 12, 1)
        thumby.display.drawText("to move around", 0, 18, 1)
        thumby.display.drawText("Pause with (B)", 0, 27, 1)
    
    def playerPage(pageObjects):
        if pageObjects['id'] != 'player':
            pageObjects.clear()
            pageObjects.update({
                'id': 'player',
                'player': Player(55, 12),
                'swordUsage': genPulse(3 * const.SWORD_SWING_ARC // const.SWORD_SWING_SPEED)
            })
        
        pageObjects['player'].update(False)
        if next(pageObjects['swordUsage']):
            pageObjects['player'].swingSword()
        
        thumby.display.drawText("PLAYER", 0, 0, 1)
        thumby.display.drawText("This is you", 0, 12, 1)
        thumby.display.drawText("Swing your", 0, 21, 1)
        thumby.display.drawText("sword with (A)", 0, 27, 1)
        pageObjects['player'].draw()
        
    def enemiesPage(pageObjects):
        if pageObjects['id'] != 'enemies':
            pageObjects.clear()
            pageObjects.update({
                'id': 'enemies',
                'enemies': [Monster(40, 5), Mutant(54, 5)],
                'animation': genSequenceLoop((-1, 1, 1, -1, 1, -1, -1, 1), 1),
                'updateRate': genPulse(4)
            })
        
        if next(pageObjects['updateRate']):
            for enemy in pageObjects['enemies']:
                enemy.x += next(pageObjects['animation'])
        
        thumby.display.drawText("ENEMIES", 0, 0, 1)
        thumby.display.drawText("These are enemies", 0, 12, 1)
        thumby.display.drawText("Avoid contact and", 0, 21, 1)
        thumby.display.drawText("defeat for points", 0, 27, 1)
        for enemy in pageObjects['enemies']:
            enemy.draw()
    
    def healthBarPage(pageObjects):
        if pageObjects['id'] != 'health':
            pageObjects.clear()
            pageObjects.update({
                'id': 'health',
                'hpBar': GameState(Player(0, 0), [], None).healthBar,
                'hpBarAnimation': genSequenceLoop((3, 2, 1, 0, 0, 0), const.FPS // 3),
                'arrowAnimation': genSequenceLoop((18, 17, 16, 17), 4)
            })
            SPR_TUTORIAL_ARROW.x, SPR_TUTORIAL_ARROW.y = 66, None
            SPR_TUTORIAL_ARROW.mirrorX, SPR_TUTORIAL_ARROW.mirrorY = 0, 1
        
        pageObjects['hpBar'].mob.hp = next(pageObjects['hpBarAnimation'])
        SPR_TUTORIAL_ARROW.y = next(pageObjects['arrowAnimation'])
        
        thumby.display.drawText("HEALTH BAR", 0, 0, 1)
        thumby.display.drawText("Lose all HP and", 0, 12, 1)
        thumby.display.drawText("it's GAME OVER", 0, 18, 1)
        pageObjects['hpBar'].draw()
        thumby.display.drawSprite(SPR_TUTORIAL_ARROW)
        if pageObjects['hpBar'].mob.hp == 0:
            thumby.display.drawText("GAME OVER", 34, 27, 1)
    
    def prizeBarPage(pageObjects):
        if pageObjects['id'] != 'prize':
            pageObjects.clear()
            pageObjects.update({
                'id': 'prize',
                'prizeBar': GameState(Player(0, 0), [], None).prizeProgress,
                'prizeBarAnimation': genSequenceLoop((0, 1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5), const.FPS // 6),
                'arrowAnimation': genSequenceLoop((13, 14, 15, 14), 4)
            })
            pageObjects['prizeBar'].capacity = 5
            SPR_TUTORIAL_ARROW.x, SPR_TUTORIAL_ARROW.y = 66, None
            SPR_TUTORIAL_ARROW.mirrorX, SPR_TUTORIAL_ARROW.mirrorY = 0, 0
        
        pageObjects['prizeBar'].progress = next(pageObjects['prizeBarAnimation'])
        SPR_TUTORIAL_ARROW.y = next(pageObjects['arrowAnimation'])
        
        thumby.display.drawText("PRIZE BAR", 0, 0, 1)
        thumby.display.drawText("Defeat enemies", 0, 15, 1)
        thumby.display.drawText("to fill it and", 0, 21, 1)
        thumby.display.drawText("earn prizes", 0, 27, 1)
        pageObjects['prizeBar'].draw()
        thumby.display.drawSprite(SPR_TUTORIAL_ARROW)
        if pageObjects['prizeBar'].progress == pageObjects['prizeBar'].capacity:
            thumby.display.drawText("PRIZE", 50, 5, 1)
    
    def prizesPage(pageObjects):
        if pageObjects['id'] != 'prizes':
            pageObjects.clear()
            pageObjects.update({
                'id': 'prizes',
                'prizes': [HealthPickup(6, 14), PointsPickup(6, 23)]
            })
        
        thumby.display.drawText("PRIZES", 0, 0, 1)
        thumby.display.drawText("Extra health", 13, 12, 1)
        thumby.display.drawText("Extra points", 13, 21, 1)
        for prize in pageObjects['prizes']:
            prize.draw()
    
    pageIndex = 0
    pages = (inputPage, playerPage, enemiesPage, healthBarPage, prizeBarPage, prizesPage)
    
    gamepad.clearBuffer()
    while True:
        # input
        prevPageIndex = pageIndex
        gamepad.update()
        if gamepad.buttonA.justPressed():
            pageIndex += 1
            if pageIndex >= len(pages):
                break
        if gamepad.buttonB.justPressed():
            break
        if gamepad.buttonL.justPressed():
            pageIndex = max(pageIndex - 1, 0)
        if gamepad.buttonR.justPressed():
            pageIndex = min(pageIndex + 1, len(pages) - 1)
        
        # update & draw
        thumby.display.fill(0)
        pages[pageIndex](pageObjects)
        
        # page indicator
        for i in range(len(pages)):
            x, y = 37 + (3 * i) - int(3 * len(pages) / 2), 38
            thumby.display.setPixel(x, y, 1)
            if i == pageIndex:
                thumby.display.drawRectangle(x - 1, y - 1, 3, 3, 1)
        
        thumby.display.update()

def showLeaderboard(highlight = 0):
    leaderboard = tuple(zip(thumby.saveData.getItem(const.SAVE_DATA_LEADER_NAMES), thumby.saveData.getItem(const.SAVE_DATA_LEADER_SCORES)))
    highlightAnimation = genSequenceLoop((True, False), const.FLASHING_TEXT_INTERVAL)
    
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    drawCenterText('HIGH SCORES', 36, 3, 1)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    
    gamepad.clearBuffer()
    while True:
        # inputs
        gamepad.update()
        if gamepad.actionJustPressed():
            break
        
        # draw
        for i, (name, score) in enumerate(leaderboard, 1):
            x, y = 6, 7 + 8 * i
            color = 0 if (i == highlight and not next(highlightAnimation)) else 1
            thumby.display.drawText(f"{i}. {name:<5} {min(score, const.SCORE_DISPLAY_CAP):>6}", x, y, color)
        thumby.display.update()

# -- MAIN MENU --

def initSaveData():
    thumby.saveData.setName(const.SAVE_NAME)
    
    # if no save data found, save defaults
    if not thumby.saveData.hasItem(const.SAVE_DATA_VERSION):
        thumby.saveData.setItem(const.SAVE_DATA_VERSION, __version__)
        thumby.saveData.setItem(const.SAVE_DATA_LEADER_NAMES, ['Ian', 'Sean', 'Errol'])
        thumby.saveData.setItem(const.SAVE_DATA_LEADER_SCORES, [1000, 500, 250])
        thumby.saveData.setItem(const.SAVE_DATA_PREV_NAME, 'AAA')
        thumby.saveData.save()

def main():
    thumby.display.setFPS(const.FPS)
    
    initSaveData()
    
    buttonHistory = gamepad.ButtonHistory(10)
    menu = Menu(['PLAY', 'TUTORIAL', 'LEADERBOARD', 'EXIT'], 36, 26)
    
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    gamepad.clearBuffer()
    while True:
        # inputs
        gamepad.update()
        buttonHistory.update()
        
        if ''.join(buttonHistory.history) == 'UUDDLRLRBA':  # konami code easter egg
            buttonHistory.history.clear()
            onKonamiCode()
            continue
        if gamepad.buttonA.justPressed():
            if menu.selectedIndex == 0:
                startGame()
            elif menu.selectedIndex == 1:
                showTutorial()
            elif menu.selectedIndex == 2:
                showLeaderboard()
            elif menu.selectedIndex == 3:
                break
            
            menu.resetAnimation()
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1) # in case font was changed
            continue
        
        # updates
        menu.update()
        
        # draw
        thumby.display.fill(0)
        thumby.display.blit(BMP_TITLE_LOGO, 2, 2, 68, 15, 0, 0, 0)
        menu.draw()
        thumby.display.update()
    
    thumby.display.fill(0)
    thumby.display.update()

main()