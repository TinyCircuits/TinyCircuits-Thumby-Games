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
        self.maxspawnThreshold = 80  # Initial spawn threshold
        self.minimumSpawnThreshold = 20  # Minimum spawn threshold
        self.spawnRateIncrease = 10
        self.gameOver = False
        self.lastCollisionCheckTime = 0
        self.collisionCheckInterval = 200  # milliseconds
        self.levelUpTarget = 100
        self.powerUp = None
        global startTime
        global elapsedTime
        startTime = time.ticks_ms()  # Game start time, assuming this is defined globally
        
        self.enemy_types = {
            'TinyShip': {'class': TinyShip, 'min_time': 0, 'max_time': 2, 'rarity': 2},
            'LittleShip': {'class': LittleShip, 'min_time': 0, 'max_time': 3, 'rarity': 10},
            'BigShip': {'class': BigShip, 'min_time': 1, 'max_time': 10, 'rarity': 20},
            'FastShip': {'class': FastShip, 'min_time': 2, 'max_time': 10, 'rarity': 15},
            'GunShip': {'class': GunShip, 'min_time': 3, 'max_time': 20, 'rarity': 25},
            'MotherShip': {'class': MotherShip, 'min_time': 2, 'max_time': 20, 'rarity': 50},
            'SuperMotherShip': {'class': SuperMotherShip, 'min_time': 4, 'max_time': 100, 'rarity': 100}
        }


    def spawn_enemy(self):
        spawnThreshold = max(self.minimumSpawnThreshold, 
                                  self.maxspawnThreshold - (elapsedTime // 60000) * self.spawnRateIncrease)
    
        if random.randint(0, spawnThreshold) == 0:
            possible_enemies = [(data['class'], 1.0 / data['rarity']) for name, data in self.enemy_types.items()
                        if elapsedTime >= data['min_time'] * 60000 and elapsedTime <= data['max_time'] * 60000]
            if possible_enemies:
                enemy_class = weighted_random_choice(possible_enemies)
                enemy = enemy_class(random.randint(10, 71), random.choice([-8, 40]))
                minutes_past_five = max(0, (elapsedTime - 300000) // 60000)
                if minutes_past_five > 0:
                    additional_damage = 3 * minutes_past_five
                    additional_toughness = 3 * minutes_past_five
                    enemy.damage += additional_damage
                    enemy.toughness += additional_toughness
                self.enemies.append(enemy)


    def spawn_power_up(self):
        if not self.powerUp and random.randint(0, 2000) == 0:
            speed = 0.2
            y, dy = (0, speed) if random.choice([True, False]) else (40, -speed)
            dx = math.cos(random.uniform(-math.pi / 4, math.pi / 4)) * speed
            x = random.randint(15, 67)
            self.powerUp = PowerUpItem(x, y, dx, dy)

            
    def update(self):
        # Player movement and firing
        self.player.update()
        # Fire all weapons that are ready and add their projectiles to the game
        new_projectiles = self.player.fire_weapons()
        self.projectiles.extend(new_projectiles)

        # Update and render projectiles
        for projectile in self.projectiles[:]:
            if not projectile.update():
                self.projectiles.remove(projectile)
            else:
                projectile.render()
                
        if elapsedTime - self.lastCollisionCheckTime > self.collisionCheckInterval:
            self.check_collisions()  # A new method to handle all collision checks
            self.lastCollisionCheckTime = elapsedTime

        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y)
            enemy.render()
            
        if self.powerUp:
            self.powerUp.update()
            if self.powerUp.active:
                self.powerUp.render()
            else:
                self.powerUp = None  # Remove the power-up if it's not active

        # Randomly spawn new enemies, adjusted by time
        self.spawn_enemy()
        
        self.spawn_power_up()
            
    def check_collisions(self):
        # Move your collision check logic here, from the update method
        for enemy in self.enemies[:]:
            if enemy.check_collision_with_projectiles(self.projectiles):
                self.enemies.remove(enemy)
                self.player.gain_experience(enemy.experience)
                continue  # Enemy has been destroyed, no need to check further collision
            if enemy.check_collision_with_shields(self.player.shields):
                self.enemies.remove(enemy)
                self.player.gain_experience(enemy.experience)
                continue  # Enemy has been destroyed, no need to check further collision
            if enemy.check_collision_with_player(self.player):
                self.player.health -= enemy.damage
                if self.player.health <= 0:
                    # Handle game over scenario
                    displayGameOverScreen(self.player)  # Display the game over screen
        if self.powerUp and self.powerUp.active:
            if self.player.x < self.powerUp.x + 2 and self.player.x + self.player.size > self.powerUp.x and \
               self.player.y < self.powerUp.y + 2 and self.player.y + self.player.size > self.powerUp.y:
                self.powerUp.active = False  # Deactivate the power-up
                selected_power_up = display_and_select_power_ups()
                apply_power_up(selected_power_up)

class Player:
    def __init__(self, x, y, speed, bitmap, health):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.bitmap = bitmap
        self.size = len(bitmap)
        self.rad = self.size / 2
        self.lastHorizontalDirection = 'right'
        self.experience = 0
        # Initialize the player with a list of weapons
        self.weapons = [Laser(0,0,'up')]  # Example: Starting with just the Laser weapon
        self.shields = []
        self.enemiesKilled = 0
        self.multi_projectile_level = 0
        self.chain_reaction_level = 0
        
    def fire_weapons(self):
        projectiles = []
        for weapon in self.weapons:
            projectile = weapon.fire(self.x + 4, self.y + 4, self.lastHorizontalDirection)
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
        for shield in self.shields[:]:
            shield.update()
            shield.render()

    def render(self):
        thumby.display.blit(self.bitmap, int(self.x), int(self.y), self.size, self.size, 0, self.lastHorizontalDirection == 'left', 0)

class Enemy:
    base_speed = 0.03  # Default base speed for all enemies
    lastDirectionUpdateTime = 0
    
    def __init__(self, x, y, bitmap, damage, toughness, experience, name='Enemy'):
        self.x = x
        self.y = y
        speed = self.base_speed + random.uniform(0, 0.01)  # Add random speed variation here
        self.speed = speed
        self.bitmap = bitmap
        self.damage = damage
        self.toughness = toughness
        self.name = name
        self.size = len(bitmap)
        self.rad = self.size / 2
        self.experience = experience
        self.dx = 0
        self.dy = 0

    def update(self, playerX, playerY):
        currentTime = time.ticks_ms()  # Get the current time in milliseconds
        # Update direction only every 200ms
        if currentTime - Enemy.lastDirectionUpdateTime > 400:
            # Calculate direction from enemy center to player center
            dx = (playerX + game_env.player.rad) - (self.x + self.rad)
            dy = (playerY + game_env.player.rad) - (self.y + self.rad)
            self.lastDirectionUpdateTime = currentTime  # Update the last direction update time
        # Update position every time
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
        
    def check_collision_with_shields(self, shields):
        for shield in shields:
            if (self.x < shield.x + 1) and (self.x + self.size > shield.x) and \
               (self.y < shield.y + 1) and (self.y + self.size > shield.y):
                self.toughness -= shield.damage
                if self.toughness <= 0:
                    return True  # Collision detected
        return False

class TinyShip(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, bitmap=bytearray([0,18,63,18,18,0]), damage=5, toughness=1, experience=10, name='TinyShip')

class LittleShip(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, bitmap=bytearray([18,51,63,51,18,18]), damage=10, toughness=2, experience=20, name='LittleShip')
        
class BigShip(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, bitmap=bytearray([36,102,126,126,219,219,219,66]), damage=15, toughness=5, experience=30, name='BigShip')

class MotherShip(Enemy):
    base_speed = 0.01  # Override base speed for MotherShip

    def __init__(self, x, y):
        super().__init__(x, y, bitmap=bytearray([136,214,162,73,73,162,214,136]), damage=20, toughness=4, experience=50, name='MotherShip')
        
    def update(self, playerX, playerY):
        super().update(playerX, playerY)  # Call the base class update
        
        # Randomly decide to spawn a TeenieShip, adjust the probability as needed
        if random.randint(0, 150) == 0:  # For example, a 1 in 21 chance each update call
            self.spawn_teenie_ship()

    def spawn_teenie_ship(self):
        # Spawn a TeenieShip at the MotherShip's current location
        teenie_ship = TeenieShip(self.x, self.y)  
        global game_env
        game_env.enemies.append(teenie_ship)
        
class SuperMotherShip(MotherShip):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Override specific properties after calling the parent's __init__
        self.bitmap=bytearray([36,255,126,60,165,255,189,129])
        self.size = len(self.bitmap)
        self.damage = 50
        self.toughness = 10
        self.experience = 100
        self.name = 'SuperMotherShip'
        # Adjust the base_speed directly since it's a class attribute
        SuperMotherShip.base_speed = 0.03
        
class FastShip(Enemy):
    base_speed = 0.15
    def __init__(self, x, y):
        super().__init__(x, y, bitmap=bytearray([15,6,6,6]), damage=2, toughness=2, experience=5, name='FastShip')
        
class GunShip(Enemy):
    base_speed = 0.03
    def __init__(self, x, y):
        super().__init__(x, y, bitmap=bytearray([73,127,62,20,20,20,20]), damage=5, toughness=4, experience=10, name='GunShip')


class TeenieShip(Enemy):
    base_speed = 0.1
    def __init__(self, x, y):
        super().__init__(x, y, bitmap=bytearray([7,2,2]), damage=1, toughness=1, experience=1, name='TeenieShip')




class Weapon:
    def __init__(self, fireRate, projectileDamage,projectileToughness):
        self.fireRate = fireRate
        self.projectileDamage = projectileDamage
        self.projectileToughness = projectileToughness
        self.lastFireTime = 0

    def fire(self, x, y, direction):
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

    def fire(self, x, y, shipDirection):
        global elapsedTime
        if elapsedTime - self.lastFireTime >= self.fireRate:
            self.lastFireTime = elapsedTime
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
        if game_env.player.multi_projectile_level > 0 and (self.generation == 0 or game_env.player.chain_reaction_level >= self.generation  ):
            split_count = 1 + game_env.player.multi_projectile_level  # Determine how many projectiles to split into
            angle_increment = 360 / split_count  # Calculate the angle increment
    
            for i in range(split_count):
                angle = math.radians(i * angle_increment + (split_count==2) * 90)  # Convert angle increment to radians for each projectile
                dx = math.cos(angle) * 0.5  # Calculate dx based on the angle, 0.5 is the speed factor
                dy = math.sin(angle) * 0.5  # Calculate dy based on the angle, 0.5 is the speed factor
    
                # Append the new projectile with calculated direction and increment the generation
                game_env.projectiles.append(Projectile(x, y, dx, dy, self.damage, self.toughness, self.generation + 1))

class RotatingShield:
    def __init__(self, player, radius=10, rotation_speed=0.05, damage=1):
        self.player = player
        self.radius = radius
        self.angle = 0
        self.damage = damage
        self.rotation_speed = rotation_speed

    def update(self):
        # Update the angle to rotate the shield
        self.angle += self.rotation_speed
        # Calculate the shield's new position
        self.x = self.player.x + self.player.size/2 + math.cos(self.angle) * self.radius
        self.y = self.player.y + self.player.size/2 + math.sin(self.angle) * self.radius

    def render(self):
        # Render the shield at its current position
        if self.x > 10:
            thumby.display.setPixel(int(self.x), int(self.y), 1)

class PowerUp:
    def __init__(self, name, rarity):
        self.name = name
        self.rarity = rarity
    
    def activate(self, player):
        pass  # To be overridden by subclasses

class MoreSpeed(PowerUp):
    def __init__(self):
        super().__init__("Increase Speed", 2)
    
    def activate(self, player):
        player.speed += 0.1

class IncreaseDamage(PowerUp):
    def __init__(self):
        super().__init__("Increase Damage", 1)
    
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
        super().__init__("Hull Repair", 1)
    
    def activate(self, player):
        player.health = 100

class FasterFireRate(PowerUp):
    def __init__(self):
        super().__init__("Faster Fire Rate", 1)
    
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
        
class RotatingShieldPowerUp(PowerUp):
    def __init__(self):
        super().__init__("Rotating Shield", 3)

    def activate(self, player):
        # Attach a rotating shield to the player
        player.shields.append(RotatingShield(player))
        
class AddWeapon(PowerUp):
    def __init__(self):
        super().__init__("Add Weapon", 3)
    
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

class PowerUpItem:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.active = True  # Indicates whether the power-up is active

    def update(self):
        # Move the power-up based on its velocity
        self.x += self.dx
        self.y += self.dy
        # Check if the power-up has moved off-screen
        if self.x < 10 or self.x > 72 or self.y < 0 or self.y > 40:
            self.active = False

    def render(self):
        if self.active:
            # Get the current time in milliseconds
            current_time = time.ticks_ms()
            
            # Check if the current time modulo some number results in a value that meets our condition for flashing
            if current_time // 50 % 2 == 0:  # This will toggle the visibility every 250 milliseconds
                # Draw a 2x2 square for the power-up
                thumby.display.drawRectangle(int(self.x), int(self.y), 2, 2, 1)



import random
def shuffle(lst):
    for i in range(len(lst) - 1, 0, -1):
        j = random.randint(0, i)
        lst[i], lst[j] = lst[j], lst[i]

def weighted_random_choice(choices):
    total_weight = sum(weight for _, weight in choices)
    random_num = random.uniform(0, total_weight)
    upto = 0
    for choice, weight in choices:
        if upto + weight >= random_num:
            return choice
        upto += weight

# Function to display and select power-ups
def display_and_select_power_ups():
    all_power_ups = [MoreSpeed(), IncreaseDamage(), FasterFireRate(), AddWeapon(), ArmorPiercing(), MultiProjectile(), HullRepairs(), ChainReaction(), RotatingShieldPowerUp()]
    # Convert power-ups to (power-up, weight) pairs based on rarity
    power_up_weights = [(power_up, 4 - power_up.rarity) for power_up in all_power_ups]
    
    # Select three unique power-ups based on their weights
    selected_power_ups = []
    for _ in range(3):
        choice = weighted_random_choice(power_up_weights)
        selected_power_ups.append(choice)
        # Remove the chosen power-up from the list of weights to ensure it's not selected again
        power_up_weights = [pw for pw in power_up_weights if pw[0] != choice]

    selected_index = 0  # Default to first power-up in the selected list


    # Display power-up selection menu
    while True:
        thumby.display.fill(0)  # Clear display

        # Display each power-up option
        for i, power_up in enumerate(selected_power_ups):
            if i == selected_index:
                # Highlight selected power-up
                thumby.display.drawText(">", 0, i * 10, 1)
            thumby.display.drawText(power_up.name, 6, i * 10, 1)

        thumby.display.update()

        # Navigation
        if thumby.buttonU.pressed():
            selected_index = (selected_index - 1) % len(selected_power_ups)
        elif thumby.buttonD.pressed():
            selected_index = (selected_index + 1) % len(selected_power_ups)
        elif thumby.buttonA.pressed():
            thumby.display.fill(0)
            break  # Confirm selection

        time.sleep(0.1)  # Debounce buttons

    return selected_power_ups[selected_index]


# Function to apply the selected power-up
def apply_power_up(power_up):
    global game_env
    power_up.activate(game_env.player)

# Helper function to draw the toolbar
def updateToolbarDynamic():
    global game_env, startTime, elapsedTime
    # Calculate elapsed time
    elapsedSeconds = (elapsedTime) // 1000
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
random.seed(startTime)
currentTime = time.ticks_ms()
elapsedTime = currentTime - startTime
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
           
# BITMAP: width: 72, height: 40
title = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,96,48,48,56,252,186,141,236,220,252,30,30,151,140,236,236,140,23,30,44,92,156,220,31,24,252,60,62,24,48,224,192,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,128,224,160,240,216,216,232,180,236,254,126,115,117,63,60,56,56,48,56,124,195,193,97,49,31,147,103,147,238,14,15,234,17,43,193,7,57,49,65,193,119,60,56,56,56,60,63,114,117,183,254,254,254,220,248,248,224,128,128,0,0,0,0,0,0,
           0,0,8,4,6,7,7,7,3,3,3,3,113,124,127,15,1,0,0,0,0,0,0,0,0,0,0,0,3,14,250,0,255,132,200,15,5,5,143,17,192,127,129,227,63,23,1,0,0,0,0,0,0,0,0,0,0,0,3,127,127,121,1,3,3,3,7,7,7,6,12,8,
           0,0,0,0,0,0,0,0,0,0,0,128,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,252,189,255,255,1,127,127,194,255,223,252,255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,96,60,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,39,31,15,8,12,12,15,31,31,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,15,248,0,0,0,0,0,0])

TITLE_PAGE = 0
GAME_LOOP = 1
gameState = TITLE_PAGE  # Initial state
# Game loop setup
thumby.display.setFPS(60)
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
lastToolbarUpdateTime = time.ticks_ms()

#initalize screen:
# Draw the toolbar
thumby.display.blit(toolbar, 0, 0, 10, 40, 0, 0, 0)
updateToolbarDynamic()

# Timing for flashing text
textFlashInterval = 500  # Time in milliseconds
lastFlashTime = time.ticks_ms()
textVisible = True

# Star settings
numStars = 10
stars = [{'x': random.randint(0, 71), 'y': random.randint(0, 39)} for _ in range(numStars)]

# Setup display
thumby.display.setFPS(60)
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

def update_stars():
    for star in stars:
        star['y'] -= 1  # Move star up
        if star['y'] < 0:
            star['x'] = random.randint(0, 71)
            star['y'] = 39
            
            
soundTrack = [
    (262, 75),  # C4 - Starting the rhythm
    (330, 75),  # E4 - Upbeat and lively
    (392, 75),  # G4 - Keeping the energy high
    (330, 75),  # E4 - Return to maintain rhythm
    (440, 75),  # A4 - Lift the melody
    (392, 75),  # G4 - Step down in scale
    (440, 75),  # A4 - Back up
    (494, 75),  # B4 - Peak of the sequence
    (440, 75),  # A4 - Back down to start the loop
    (392, 75),  # G4 - Further down
    (330, 75),  # E4 - Return to earlier upbeat tone
    (262, 75),  # C4 - Close the loop with base note
    (330, 75),  # E4 - Start again to maintain energy
    (392, 75),  # G4 - Continue the loop
    (440, 75),  # A4 - Keep energy before restarting loop
    (494, 75),  # B4 - Hit the peak again for loop closure
]

currentNote = 0  # Index of the current note to play
lastNoteTime = time.ticks_ms()  # Time when the last note was played
noteInterval = 200  # Time between notes in ms

# Function to play a sequence of sounds non-blocking
def playSoundtrack():
    global currentNote, lastNoteTime
    currentTime = time.ticks_ms()
    if currentNote >= len(soundTrack):
        currentNote = 0  # Reset to loop the soundtrack
    if soundTrack[currentNote] is None:
        lastNoteTime = currentTime + 150  # Set time for rest duration
        currentNote += 1
    elif currentTime - lastNoteTime >= noteInterval:
        note = soundTrack[currentNote]
        thumby.audio.play(note[0], note[1])
        lastNoteTime = currentTime
        currentNote += 1


while True:
    
    if gameState == TITLE_PAGE:
        # Clear display
        thumby.display.fill(0)
        
        # Update stars position
        update_stars()

        # Draw the title
        thumby.display.blit(title, 0, 0, 72, 40, -1, 0, 0)
        
        # Handle flashing text
        currentTime = time.ticks_ms()
        if currentTime - lastFlashTime > textFlashInterval:
            textVisible = not textVisible
            lastFlashTime = currentTime
        
        if textVisible:
            thumby.display.drawText("Press", 3, 24, 1)
            thumby.display.drawText("A", 3, 30, 1)
        
        # Draw stars
        for star in stars:
            thumby.display.setPixel(star['x'], star['y'], 1)
        
        playSoundtrack()  # This plays the music non-blockingly
        
        # Update the display
        thumby.display.update()
        
        if thumby.buttonA.pressed():
            gameState = GAME_LOOP
            thumby.display.fill(0)
            time.sleep(0.3)
            
    elif gameState == GAME_LOOP:
    
        currentTime = time.ticks_ms()
        elapsedTime = currentTime - startTime
        
        # Check for power-up selection
        if game_env.player.experience >= game_env.levelUpTarget:
            selected_power_up = display_and_select_power_ups()  # Pause game and select power-up
            apply_power_up(selected_power_up)  # Apply selected power-up
            game_env.player.experience = 0  # Reset experience after selecting power-up
            game_env.levelUpTarget += 50
    
        
        thumby.display.drawFilledRectangle(10, 0, 62, 40, 0)  # Clear game area
        game_env.update()
        game_env.player.render()
    
        # Draw the toolbar
        thumby.display.blit(toolbar, 0, 0, 10, 40, 0, 0, 0)
    
        if currentTime - lastToolbarUpdateTime >= 1000:
            thumby.display.drawFilledRectangle(1, 10, 7, 10, 0)
            thumby.display.drawFilledRectangle(4, 27, 2, 10, 0)
            updateToolbarDynamic()
            lastToolbarUpdateTime = currentTime  # Update the last update time
    
        thumby.display.update()
