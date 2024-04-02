import thumby

class Enemy:
    def __init__(self, x, y, speed, bitmap, name='Enemy'):
        self.x = x
        self.y = y
        self.speed = speed
        self.bitmap = bitmap
        self.name = name

    def update(self, playerX, playerY):
        # playerX and playerY are converted to fixed-point before being passed here
        dx = playerX - self.x
        dy = playerY - self.y
        # Replace math.copysign with direct comparisons and arithmetic
        self.x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
        self.y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

class TinyShip(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, bitmap=bytearray([8,30,8,8,30,8]), name='TinyShip')


class Projectile:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def update(self):
        # Move the projectile
        self.x += self.dx
        self.y += self.dy

        # Return False if the projectile goes off-screen (for cleanup)
        return not (self.x < 10 or self.x > 72 or self.y < 0 or self.y > 40)


import random

# List to hold enemies
enemies = []

# Function to spawn a new enemy, ensuring they appear within the adjusted gameplay area
def spawn_enemy():
    if random.randint(0, 1) == 0:  # Top or bottom
        x = random.randint(10, 71)  # Adjusted to start after the toolbar
        y = -8 if random.randint(0, 1) == 0 else 40
    else:  # Left or right, but shifted to the right of the toolbar
        x = -8 if random.randint(0, 1) == 0 else 72
        y = random.randint(0, 39)
    
    enemies.append(TinyShip(x, y, enemySpeed + random.uniform(0, 0.01)))

    
import time

# Player health
playerHealth = 100

# Game start time
startTime = time.ticks_ms()
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

# Helper function to draw the toolbar
def updateToolbarDynamic():
    global playerHealth, startTime
    # Calculate elapsed time
    elapsedSeconds = (time.ticks_ms() - startTime) // 1000
    minutes = elapsedSeconds // 60
    seconds = elapsedSeconds % 60

    # Display time counter
    thumby.display.drawText(f"{minutes:02}", 1, 9, 1)
    thumby.display.drawText(f"{seconds:02}", 1, 14, 1)
    # Draw health bar line
    healthBarLength = int(10 * (playerHealth / 100))  # Scale health to length of the bar
    thumby.display.drawFilledRectangle(4, 27, 2, healthBarLength, 1)


# Game variables
shipSprite = bytearray([96,127,56,254,254,56,127,96])
# BITMAP: width: 8, height: 8
shipSpriteRight = bytearray([24,219,255,126,126,90,90,66])
# BITMAP: width: 8, height: 8
shipSpriteLeft =  bytearray([66,90,90,126,126,255,219,24])

# Toolbar BITMAP: width: 10, height: 40
toolbar = bytearray([255,1,121,165,165,165,197,121,1,255,
           255,0,0,0,0,0,0,0,0,255,
           255,0,96,240,224,224,240,96,0,255,
           255,0,252,4,5,5,4,252,0,255,
           255,128,191,160,160,160,160,191,128,255])

# BITMAP: width: 8, height: 8
enemy1 = bytearray([0,16,60,16,16,60,16,0])

thumby.display.setFPS(60)

# Player starting position
playerX = 36
playerY = 20

playerSpeed = 0.3

enemySpeed = 0.03
# Game loop
# Initial enemy spawn
spawn_enemy()
# Keep track of the last update time for the toolbar
lastToolbarUpdateTime = time.ticks_ms()

# Initialize projectile list and firing variables
projectiles = []
fireRate = 1000  # milliseconds
lastFireTime = 0

# Initialize the last direction the ship moved horizontally
lastHorizontalDirection = 'right'


while True:
    currentTime = time.ticks_ms()
    thumby.display.drawFilledRectangle(10, 0, 62, 40, 0)
    # Player movement
    if thumby.buttonU.pressed():
        playerY -= playerSpeed
    if thumby.buttonD.pressed():
        playerY += playerSpeed
    if thumby.buttonL.pressed():
        playerX -= playerSpeed
        lastHorizontalDirection = 'left'
    if thumby.buttonR.pressed():
        playerX += playerSpeed
        lastHorizontalDirection = 'right'


    # Display the player's ship
    if lastHorizontalDirection == 'right':
        thumby.display.blit(shipSpriteRight, int(playerX), int(playerY), 8, 8, 0, 0, 0)
    else:  # Last movement was left
        thumby.display.blit(shipSpriteLeft, int(playerX), int(playerY), 8, 8, 0, 0, 0)
    
    # Handle firing
    if currentTime - lastFireTime >= fireRate:
        projVel = -0.5
        if lastHorizontalDirection == 'right': projVel = projVel * -1
        projectiles.append(Projectile(playerX + 4, playerY + 4, projVel, 0))
        lastFireTime = currentTime
    
    # Update and render projectiles
    for projectile in projectiles[:]:
        projectile.update()
        thumby.display.drawLine(int(projectile.x), int(projectile.y), int(projectile.x+2), int(projectile.y), 1)  # Render as a line
        if not projectile.update():  # Remove off-screen projectiles
            projectiles.remove(projectile)
    
    # Collision detection for projectiles and enemies
    for projectile in projectiles:
        for enemy in enemies[:]:  # Copy list for safe removal
            if abs(projectile.x - enemy.x - 3) < 3 and abs(projectile.y - enemy.y - 3) < 3:  # Simple collision check
                enemies.remove(enemy)  # Remove the enemy
                try:
                    projectiles.remove(projectile)  # Remove the projectile
                except ValueError:
                    pass  # In case the projectile was already removed

    # Update and display each enemy
    for enemy in enemies:
        enemy.update(playerX, playerY)
        if(int(enemy.x)>10):
            thumby.display.blit(enemy.bitmap, int(enemy.x) , int(enemy.y), 6, 6, 0, 0, 0)
        if abs(playerX + 4 - enemy.x - 3) < 4 and abs(playerY + 4 - enemy.y - 3) < 4:  # Simple collision check
            playerHealth -= 1
    # Randomly spawn new enemies
    if random.randint(0, 60) == 0:
        spawn_enemy()

    # Ensure player doesn't move into the toolbar area
    playerX = max(playerX, 10)  # Prevent player from entering the toolbar area

    # Draw the toolbar
    thumby.display.blit(toolbar, 0, 0, 10, 40, 0, 0, 0)

    if currentTime - lastToolbarUpdateTime >= 1000:
        thumby.display.drawFilledRectangle(2, 10, 6, 10, 0)
        thumby.display.drawFilledRectangle(4, 27, 2, 10, 0)
        updateToolbarDynamic()
        lastToolbarUpdateTime = currentTime  # Update the last update time

    # Update the display
    thumby.display.update()



