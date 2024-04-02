import thumby
import random
import time
import math

class GameEnvironment:
    def __init__(self):
        self.enemies = []
        self.projectiles = []
        self.player = Player(36, 20, 0.3,shipSprite, 100)
        self.lastFireTime = 0
        self.spawnThreshold = 60  # Initial spawn threshold
        self.minimumSpawnThreshold = 20  # Minimum spawn threshold
        self.spawnRateIncrease = 1
        self.gameOver = False
        self.lastCollisionCheckTime = 0
        self.collisionCheckInterval = 200  # milliseconds
        self.levelUpTarget = 100
        global startTime
        startTime = time.ticks_ms()  # Game start time, assuming this is defined globally


    def spawn_enemy(self):
        currentTime = time.ticks_ms()
        elapsedTime = currentTime - startTime
        # Decrease spawn threshold over time to increase spawn rate
        self.spawnThreshold = max(self.minimumSpawnThreshold, 
                                  self.spawnThreshold - (elapsedTime // 60000) * self.spawnRateIncrease)
        
        # Spawn logic based on adjusted spawn threshold
        if random.randint(0, self.spawnThreshold) == 0:
            # Decide the type of enemy to spawn based on the game's progression
            if random.randint(0, max(2, 50 - elapsedTime // 60000)) == 0:
                self.enemies.append(MotherShip(random.randint(10, 71), random.choice([-8, 40]), 0.03 + random.uniform(0, 0.01)))
            elif random.randint(0, max(1, 5 - elapsedTime // 60000)) == 0:
                self.enemies.append(LittleShip(random.randint(10, 71), random.choice([-8, 40]), 0.03 + random.uniform(0, 0.01)))
            else:
                self.enemies.append(TinyShip(random.randint(10, 71), random.choice([-8, 40]), 0.03 + random.uniform(0, 0.01)))


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
                
        if currentTime - self.lastCollisionCheckTime > self.collisionCheckInterval:
            self.check_collisions()  # A new method to handle all collision checks
            self.lastCollisionCheckTime = currentTime

        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y)
            enemy.render()

        # Randomly spawn new enemies, adjusted by time
        self.spawn_enemy()
            
    def check_collisions(self):
        # Move your collision check logic here, from the update method
        for enemy in self.enemies[:]:
            if enemy.check_collision_with_projectiles(self.projectiles):
                self.enemies.remove(enemy)
                self.player.gain_experience(enemy.experience)
                continue  # Enemy has been destroyed, no need to check further collision
            if enemy.check_collision_with_player(self.player):
                self.player.health -= enemy.damage
                if self.player.health <= 0:
                    # Handle game over scenario
                    displayGameOverScreen(self.player)  # Display the game over screen

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
        self.weapons = [Laser(0,0,'up')]  # Example: Starting with just the Laser weapon
        self.enemiesKilled = 0
        self.multi_projectile_level = 0
        self.chain_reaction_level = 0
        
    def fire_weapons(self, currentTime):
        projectiles = []
        for weapon in self.weapons:
            projectile = weapon.fire(currentTime, self.x + 4, self.y + 4, self.lastHorizontalDirection)
            if projectile:
                projectiles.append(projectile)
        return projectiles    
    
    def gain_experience(self, amount):
        self.experience += amount
        self.enemiesKilled += 1

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
        self.x = max(self.x, 10)  
        self.x = min(self.x, 72 - self.size/2)  
        self.y = max(self.y, 0 - self.size/2)  
        self.y = min(self.y, 40 - self.size/2)

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
                projectile.toughness -= 1
                if projectile.toughness <= 0:
                    projectile.destroy(self, projectile.x, projectile.y)
                    projectiles.remove(projectile)
                if self.toughness <= 0:
                    return True  # Return True to indicate the enemy should be removed
        return False  # Enemy survives if toughness > 0

    def check_collision_with_player(self, player):
        # Updated collision detection between enemy and player
        if (self.x < player.x + player.size) and (self.x + self.size > player.x) and \
           (self.y < player.y + player.size) and (self.y + self.size > player.y):
            return True
        return False

class TinyShip(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, bitmap=bytearray([0,18,63,18,18,0]), damage=5, toughness=1, experience=10, name='TinyShip')

class LittleShip(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, bitmap=bytearray([18,51,63,51,18,18]), damage=10, toughness=2, experience=20, name='LittleShip')

class MotherShip(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, bitmap=bytearray([136,214,162,73,73,162,214,136]), damage=20, toughness=4, experience=50, name='MotherShip')
    
    def update(self, playerX, playerY):
        super().update(playerX, playerY)  # Call the base class update
        
        # Randomly decide to spawn a TeenieShip, adjust the probability as needed
        if random.randint(0, 150) == 0:  # For example, a 1 in 21 chance each update call
            self.spawn_teenie_ship()

    def spawn_teenie_ship(self):
        # Spawn a TeenieShip at the MotherShip's current location
        teenie_ship = TeenieShip(self.x, self.y, 0.1)  # Adjust speed as needed
        global game_env
        game_env.enemies.append(teenie_ship)
        
class TeenieShip(Enemy):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed, bitmap=bytearray([7,2,2]), damage=1, toughness=1, experience=1, name='TeenieShip')




class Weapon:
    def __init__(self, fireRate, projectileDamage,projectileToughness):
        self.fireRate = fireRate
        self.projectileDamage = projectileDamage
        self.projectileToughness = projectileToughness
        self.lastFireTime = 0

    def fire(self, currentTime, x, y, direction):
        # Base fire method to be overridden by subclasses
        raise NotImplementedError("Subclass must implement abstract method")

class Laser(Weapon):
    def __init__(self, offsetx, offsety, shotDirection):
        super().__init__(1000, 1, 1)
        self.offsety = offsety  # Negative for left, positive for right
        self.offsetx = offsetx
        self.shotDirection = shotDirection
        # Direction mappings for when the ship is facing left or right
        self.direction_mappings = {
            'left': {'up': 'left', 'down': 'right', 'left': 'down', 'right': 'up'},
            'right': {'up': 'right', 'down': 'left', 'left': 'up', 'right': 'down'}
        }

    def fire(self, currentTime, x, y, shipDirection):
        if currentTime - self.lastFireTime >= self.fireRate:
            self.lastFireTime = currentTime
            # Adjust the shot direction based on the ship's direction
            final_direction = self.direction_mappings[shipDirection][self.shotDirection]
            # Calculate projectile velocity and offset based on final direction
            if final_direction == 'up':
                dx, dy = 0, -0.5
            elif final_direction == 'down':
                dx, dy = 0, 0.5
            elif final_direction == 'left':
                dx, dy = -0.5, 0
            elif final_direction == 'right':
                dx, dy = 0.5, 0
            
            # Adjust starting position of the projectile based on the offset
            projectile_x = x + self.offsetx
            projectile_y = y + self.offsety
            
            return Projectile(projectile_x, projectile_y, dx, dy, self.projectileDamage, self.projectileToughness)
        return None

class Projectile:
    def __init__(self, x, y, dx, dy, damage, toughness, generation=0):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.toughness = toughness
        self.generation = generation

    def update(self):
        self.x += self.dx
        self.y += self.dy
        return not (self.x < 10 or self.x > 72 or self.y < 0 or self.y > 40)

    def render(self):
        thumby.display.drawLine(int(self.x), int(self.y), int(self.x + max(1, 2 - self.generation)), int(self.y), 1)
        
    def destroy(self, target, x, y):
        global game_env
        if game_env.player.multi_projectile_level > 0 and (self.generation == 0 or game_env.player.chain_reaction_level >= self.generation - 1  ):
            split_count = 1 + game_env.player.multi_projectile_level  # Determine how many projectiles to split into
            angle_increment = 360 / split_count  # Calculate the angle increment
    
            for i in range(split_count):
                angle = math.radians(i * angle_increment + (split_count==2) * 90)  # Convert angle increment to radians for each projectile
                dx = math.cos(angle) * 0.5  # Calculate dx based on the angle, 0.5 is the speed factor
                dy = math.sin(angle) * 0.5  # Calculate dy based on the angle, 0.5 is the speed factor
    
                # Append the new projectile with calculated direction and increment the generation
                game_env.projectiles.append(Projectile(x, y, dx, dy, self.damage, self.toughness, self.generation + 1))

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

class IncreaseDamage(PowerUp):
    def __init__(self):
        super().__init__("Increase Damage", 2)
    
    def activate(self, player):
        for weapon in player.weapons:
            weapon.projectileDamage += 1
            
class ArmorPiercing(PowerUp):
    def __init__(self):
        super().__init__("Armour Piercing", 2)
    
    def activate(self, player):
        for weapon in player.weapons:
            weapon.projectileToughness += 1
            
class HullRepairs(PowerUp):
    def __init__(self):
        super().__init__("Hull Repair", 2)
    
    def activate(self, player):
        player.health = 100

class FasterFireRate(PowerUp):
    def __init__(self):
        super().__init__("Faster Fire Rate", 3)
    
    def activate(self, player):
        for weapon in player.weapons:
            weapon.fireRate = max(100, weapon.fireRate - 100)
            
class MultiProjectile(PowerUp):
    def __init__(self):
        super().__init__("Multi-Projectile", 3)
    
    def activate(self, player):
        player.multi_projectile_level += 1  # Increase the level each time this power-up is activated

class ChainReaction(PowerUp):
    def __init__(self):
        super().__init__("Chain Reaction", 3)
    
    def activate(self, player):
        player.chain_reaction_level += 1
        
class AddWeapon(PowerUp):
    def __init__(self):
        super().__init__("Add Weapon", 4)
    
    def activate(self, player):
        weapon_configurations = {
            1: [Laser(0, -3, 'up'), Laser(0, 2, 'up')],  # When the player has 1 weapon
            2: [Laser(0, -3, 'up'), Laser(0, 2, 'up'), Laser(0, 0, 'left')],  # When the player has 2 weapons
            3: [Laser(0, -3, 'up'), Laser(0, 2, 'up'), Laser(0, 0, 'left'), Laser(0, 0, 'right')],  # When the player has 3 weapons
            4: [Laser(0, -3, 'up'), Laser(0, 2, 'up'), Laser(0, 0, 'left'), Laser(0, 0, 'right'), Laser(0, 0, 'down')],  # When the player has 4 weapons
        }
        count = len(player.weapons)
        if count <= 4 : 
            player.weapons = weapon_configurations[count]

import random
def shuffle(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

# Function to display and select power-ups
def display_and_select_power_ups():
    all_power_ups = [MoreSpeed(), IncreaseDamage(), FasterFireRate(), AddWeapon(), ArmorPiercing(), MultiProjectile(), HullRepairs(), ChainReaction()]
    shuffle(all_power_ups)  # Use the custom shuffle function
    power_ups = all_power_ups[:3]  # Select the first three power-ups after shuffling

    selected_index = 0  # Default to first power-up in the randomized list

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
            thumby.display.fill(0)
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
    experienceBarLenth = int(10 * ((game_env.player.experience % game_env.levelUpTarget) / game_env.levelUpTarget) +1)  # Scale health to length of the bar
    thumby.display.drawFilledRectangle(3, 37-experienceBarLenth, 1, experienceBarLenth, 1)


def displayGameOverScreen(player):
    thumby.display.fill(0)  # Clear the display
    # Display game over text and stats
    thumby.display.drawText("Game Over!", 20, 10, 1)
    thumby.display.drawText("Time: " + str(getGameTime()), 10, 20, 1)
    thumby.display.drawText("Enemies: " + str(player.enemiesKilled), 10, 30, 1)
    thumby.display.update()
    while True:
        if thumby.buttonA.pressed():
                restartGame()
                break

def restartGame():
    global game_env, startTime
    startTime = time.ticks_ms()  # Reset the start time
    game_env = GameEnvironment()  # Reinitialize the game environment

# Helper function to calculate game time
def getGameTime():
    elapsedSeconds = (time.ticks_ms() - startTime) // 1000
    return f"{elapsedSeconds // 60:02}:{elapsedSeconds % 60:02}"

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
    if game_env.player.experience >= game_env.levelUpTarget:
        selected_power_up = display_and_select_power_ups()  # Pause game and select power-up
        apply_power_up(selected_power_up)  # Apply selected power-up
        game_env.player.experience = 0  # Reset experience after selecting power-up
        game_env.levelUpTarget += 50

    
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
