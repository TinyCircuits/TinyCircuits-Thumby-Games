import thumby
import random
import time

class GameEnvironment:
    def __init__(self):
        self.enemies = []
        self.projectiles = []
        self.player = Player(36, 20, 0.3,shipSprite, 100)
        self.lastFireTime = 0
        self.fireRate = 1000  # milliseconds
        self.spawn_enemy()  # Initial enemy spawn

    def spawn_enemy(self):
        if random.randint(0, 1) == 0:  # Top or bottom
            x = random.randint(10, 71)  # Adjusted to start after the toolbar
            y = -8 if random.randint(0, 1) == 0 else 40
        else:  # Left or right
            x = -8 if random.randint(0, 1) == 0 else 72
            y = random.randint(0, 39)
        
        if random.randint(0, 1) == 0:
            self.enemies.append(LittleShip(x, y, 0.03 + random.uniform(0, 0.01)))
        else:
            self.enemies.append(TinyShip(x, y, 0.03 + random.uniform(0, 0.01)))

    def update(self, currentTime):
        # Player movement and firing
        self.player.update()
        # Fire all weapons that are ready and add their projectiles to the game
        new_projectiles = self.player.fire_weapons(currentTime)
        self.projectiles.extend(new_projectiles)

        # Update and render projectiles
        for projectile in self.projectiles[:]:
            if not projectile.update():
                self.projectiles.remove(projectile)
            else:
                projectile.render()

        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y)
            enemy.render()
            # Check collision with projectiles
            if enemy.check_collision_with_projectiles(self.projectiles):
                self.enemies.remove(enemy)
                self.player.gain_experience(enemy.experience)
                continue  # Enemy has been destroyed, no need to check further collision
            # Check collision with player
            if enemy.check_collision_with_player(self.player):
                self.player.health -= enemy.damage  # Directly reduce player health on collision
                if self.player.health <= 0:
                    # Handle game over scenario
                    print("Game Over!")  # Placeholder for actual game over handling
                #self.enemies.remove(enemy)  # Optionally remove the enemy on collision


        # Randomly spawn new enemies
        if random.randint(0, 60) == 0:
            self.spawn_enemy()

class Player:
    def __init__(self, x, y, speed, bitmap, health):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.bitmap = bitmap
        self.size = len(bitmap)
        self.lastHorizontalDirection = 'right'
        self.experience = 0
        # Initialize the player with a list of weapons
        self.weapons = [Laser()]  # Example: Starting with just the Laser weapon
        
    def fire_weapons(self, currentTime):
        projectiles = []
        for weapon in self.weapons:
            projectile = weapon.fire(currentTime, self.x + 4, self.y + 4, self.lastHorizontalDirection)
            if projectile:
                projectiles.append(projectile)
        return projectiles    
    
    def gain_experience(self, amount):
        self.experience += amount

    def update(self):
        if thumby.buttonU.pressed():
            self.y -= self.speed
        if thumby.buttonD.pressed():
            self.y += self.speed
        if thumby.buttonL.pressed():
            self.x -= self.speed
            self.lastHorizontalDirection = 'left'
        if thumby.buttonR.pressed():
            self.x += self.speed
            self.lastHorizontalDirection = 'right'
        self.x = max(self.x, 10)  # Prevent player from entering the toolbar area

    def render(self):
        thumby.display.blit(self.bitmap, int(self.x), int(self.y), self.size, self.size, 0, self.lastHorizontalDirection == 'left', 0)

class Enemy:
    def __init__(self, x, y, speed, bitmap, damage, toughness, experience, name='Enemy'):
        self.x = x
        self.y = y
        self.speed = speed
        self.bitmap = bitmap
        self.damage = damage
        self.toughness = toughness
        self.name = name
        self.size = len(bitmap)
        self.experience = experience

    def update(self, playerX, playerY):
        dx = playerX - self.x
        dy = playerY - self.y
        self.x += self.speed if dx > 0 else -self.speed if dx < 0 else 0
        self.y += self.speed if dy > 0 else -self.speed if dy < 0 else 0

    def render(self):
        global game_env
        if self.x > 10:
            thumby.display.blit(self.bitmap, int(self.x), int(self.y), self.size, self.size, 0, self.x > game_env.player.x, 0)

    def check_collision_with_projectiles(self, projectiles):
        for projectile in projectiles:
            if (self.x < projectile.x + 1) and (self.x + self.size > projectile.x) and \
               (self.y < projectile.y + 1) and (self.y + self.size > projectile.y):
                self.toughness -= projectile.damage  # Subtract projectile damage from enemy toughness
                projectiles.remove(projectile)
                if self.toughness <= 0:
                    return True  # Return True to indicate the enemy should be removed
        return False  # Enemy survives if toughness > 0

    def check_collision_with_player(self, player):
        # Assuming player's sprite can be approximated as a square for collision detection
        player_size = 8  # This assumes the player sprite is 8x8 pixels
        # Updated collision detection between enemy and player
        if (self.x < player.x + player.size) and (self.x + self.size > player.x) and \
           (self.y < player.y + player.size) and (self.y + self.size > player.y):
            return True
        return False

class TinyShip(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, bitmap=bytearray([0,18,63,18,18,0]), damage=1, toughness=1, experience=10, name='TinyShip')

class LittleShip(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, bitmap=bytearray([18,51,63,51,18,18]), damage=4, toughness=2, experience=20, name='LittleShip')


class Weapon:
    def __init__(self, fireRate, projectileDamage):
        self.fireRate = fireRate  # Time between shots in milliseconds
        self.projectileDamage = projectileDamage
        self.lastFireTime = 0

    def fire(self, currentTime, x, y, direction):
        if currentTime - self.lastFireTime >= self.fireRate:
            projVel = -0.5 if direction == 'left' else 0.5
            self.lastFireTime = currentTime
            return Projectile(x, y, projVel, 0, self.projectileDamage)
        return None

class Laser(Weapon):
    def __init__(self):
        super().__init__(1000, 1)  # Example: Laser fires every 0.5 seconds with 1 damage

class Projectile:
    def __init__(self, x, y, dx, dy, damage):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage

    def update(self):
        self.x += self.dx
        self.y += self.dy
        return not (self.x < 10 or self.x > 72 or self.y < 0 or self.y > 40)

    def render(self):
        thumby.display.drawLine(int(self.x), int(self.y), int(self.x+2), int(self.y), 1)

class PowerUp:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity
    
    def activate(self, player):
        pass  # To be overridden by subclasses

class MoreSpeed(PowerUp):
    def __init__(self):
        super().__init__("Increase Speed", 1)
    
    def activate(self, player):
        player.speed += 0.3
        print(f"{self.name} activated!")

class IncreaseDamage(PowerUp):
    def __init__(self):
        super().__init__("Increase Damage", 2)
    
    def activate(self, player):
        for weapon in player.weapons:
            weapon.projectileDamage += 1
        print(f"{self.name} activated!")

class FasterFireRate(PowerUp):
    def __init__(self):
        super().__init__("Faster Fire Rate", 3)
    
    def activate(self, player):
        for weapon in player.weapons:
            weapon.fireRate = max(100, weapon.fireRate - 100)
        print(f"{self.name} activated!")


# Function to display and select power-ups
def display_and_select_power_ups():
    power_ups = [MoreSpeed(), IncreaseDamage(), FasterFireRate()]
    selected_index = 0  # Default to first power-up

    # Display power-up selection menu
    while True:
        thumby.display.fill(0)  # Clear display

        # Display each power-up option
        for i, power_up in enumerate(power_ups):
            if i == selected_index:
                # Highlight selected power-up
                thumby.display.drawText(">", 0, i * 10, 1)
            thumby.display.drawText(power_up.name, 6, i * 10, 1)

        thumby.display.update()

        # Navigation
        if thumby.buttonU.pressed():
            selected_index = (selected_index - 1) % len(power_ups)
        elif thumby.buttonD.pressed():
            selected_index = (selected_index + 1) % len(power_ups)
        elif thumby.buttonA.pressed():
            break  # Confirm selection

        time.sleep(0.1)  # Debounce buttons

    return power_ups[selected_index]

# Function to apply the selected power-up
def apply_power_up(power_up):
    global game_env
    # This is a placeholder for applying the selected power-up
    # You would add logic here based on the selected index
    print("Applying power-up:", power_up)
    power_up.activate(game_env.player)

# Helper function to draw the toolbar
def updateToolbarDynamic():
    global game_env, startTime
    # Calculate elapsed time
    elapsedSeconds = (time.ticks_ms() - startTime) // 1000
    minutes = elapsedSeconds // 60
    seconds = elapsedSeconds % 60

    # Display time counter
    thumby.display.drawText(f"{minutes:02}", 1, 9, 1)
    thumby.display.drawText(f"{seconds:02}", 1, 14, 1)
    # Draw health bar line
    healthBarLength = int(10 * (game_env.player.health / 100))  # Scale health to length of the bar
    thumby.display.drawFilledRectangle(4, 37-healthBarLength, 2, healthBarLength, 1)
    experienceBarLenth = int(10 * ((game_env.player.experience % 100) / 100) +1)  # Scale health to length of the bar
    thumby.display.drawFilledRectangle(3, 37-experienceBarLenth, 1, experienceBarLenth, 1)


# Game start time
startTime = time.ticks_ms()
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

# Game variables
# BITMAP: width: 8, height: 8
shipSprite = bytearray([24,219,255,126,126,90,90,66])
# Initialize game environment
game_env = GameEnvironment()

# Toolbar BITMAP: width: 10, height: 40
toolbar = bytearray([255,1,121,165,165,165,197,121,1,255,
           255,0,0,0,0,0,0,0,0,255,
           255,0,96,240,224,224,240,96,0,255,
           255,0,252,4,5,5,4,252,0,255,
           255,128,191,160,160,160,160,191,128,255])

# Game loop setup
thumby.display.setFPS(60)
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
lastToolbarUpdateTime = time.ticks_ms()

#initalize screen:
# Draw the toolbar
thumby.display.blit(toolbar, 0, 0, 10, 40, 0, 0, 0)
updateToolbarDynamic()

while True:
    currentTime = time.ticks_ms()
    
    # Check for power-up selection
    if game_env.player.experience >= 100:
        selected_power_up = display_and_select_power_ups()  # Pause game and select power-up
        apply_power_up(selected_power_up)  # Apply selected power-up
        game_env.player.experience = 0  # Reset experience after selecting power-up

    
    thumby.display.drawFilledRectangle(10, 0, 62, 40, 0)  # Clear game area
    game_env.update(currentTime)
    game_env.player.render()

    # Draw the toolbar
    thumby.display.blit(toolbar, 0, 0, 10, 40, 0, 0, 0)

    if currentTime - lastToolbarUpdateTime >= 1000:
        thumby.display.drawFilledRectangle(2, 10, 6, 10, 0)
        thumby.display.drawFilledRectangle(4, 27, 2, 10, 0)
        updateToolbarDynamic()
        lastToolbarUpdateTime = currentTime  # Update the last update time

    thumby.display.update()
