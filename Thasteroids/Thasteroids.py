# Author: PanduhBeer
# version number: 1.0
import thumby
import math
import random
from sys import path
import time
path.append("/Games/Thasteroids")


# Constants
SPACESHIP_SIZE = 3
ASTEROID_SIZE = 4
PROJECTILE_SIZE = 1
MAX_BIG_ASTEROIDS = 2
MAX_SMALL_ASTEROIDS = 3
MAX_PROJECTILES = 5
PROJECTILE_SPEED = 1
SCORE_INCREMENT = 10
FRAME_RATE = 20


def save_high_score(high_score, filename="/Games/Thasteroids/high_score.txt"):
    with open(filename, "w") as f:
        f.write(str(high_score))

def load_high_score(filename="/Games/Thasteroids/high_score.txt"):
    try:
        with open(filename, "r") as f:
            high_score = f.read()
            return int(high_score)
    except:
        print("error loading file")
        save_high_score(0, filename)
        return 0
        
    print(high_score)


# Helper functions
def wrap_coordinates(x, y):
    return x % 72, y % 40

def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
class Spaceship:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.vx = 0
        self.vy = 0
        self.thrust = 0.1
        self.drag = 0.01

    def update(self):
        if thumby.buttonU.pressed():
            self.vx += math.cos(math.radians(self.angle)) * self.thrust
            self.vy += math.sin(math.radians(self.angle)) * self.thrust
        
        self.x += self.vx
        self.y += self.vy
        self.x, self.y = wrap_coordinates(self.x, self.y)

        # Apply drag
        self.vx *= (1 - self.drag)
        self.vy *= (1 - self.drag)


    def draw(self):
        x1, y1 = self.x + math.cos(math.radians(self.angle)) * SPACESHIP_SIZE, self.y + math.sin(math.radians(self.angle)) * SPACESHIP_SIZE
        x2, y2 = self.x + math.cos(math.radians(self.angle + 130)) * SPACESHIP_SIZE, self.y + math.sin(math.radians(self.angle + 130)) * SPACESHIP_SIZE
        x3, y3 = self.x + math.cos(math.radians(self.angle + 230)) * SPACESHIP_SIZE, self.y + math.sin(math.radians(self.angle + 230)) * SPACESHIP_SIZE
    
        coords = [(x1, y1), (x2, y2), (x3, y3)]
    
        for i in range(len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[(i + 1) % len(coords)]
    
            wrapped_x1, wrapped_y1 = wrap_coordinates(x1, y1)
            wrapped_x2, wrapped_y2 = wrap_coordinates(x2, y2)
    
            if abs(x1 - x2) < 72 / 2 and abs(y1 - y2) < 40 / 2:
                thumby.display.drawLine(int(x1), int(y1), int(x2), int(y2), 1)
            
            if abs(wrapped_x1 - wrapped_x2) < 72 / 2 and abs(wrapped_y1 - wrapped_y2) < 40 / 2:
                thumby.display.drawLine(int(wrapped_x1), int(wrapped_y1), int(wrapped_x2), int(wrapped_y2), 1)

        # Add thrust pixel
        if thumby.buttonU.pressed():
            x_thrust, y_thrust = self.x + math.cos(math.radians(self.angle + 180)) * SPACESHIP_SIZE, self.y + math.sin(math.radians(self.angle + 180)) * SPACESHIP_SIZE
            wrapped_x_thrust, wrapped_y_thrust = wrap_coordinates(x_thrust, y_thrust)
            thumby.display.setPixel(int(wrapped_x_thrust), int(wrapped_y_thrust), 1)


    def teleport(self):
        self.x = random.randint(0, 72)
        self.y = random.randint(0, 40)

    def check_teleport(self):
        if thumby.buttonB.justPressed():
            self.teleport()



class Asteroid:
    def __init__(self, x, y, size, angle, num_vertices=6):
        self.x = x
        self.y = y
        self.size = size
        self.angle = angle
        self.speed = 0.4
        self.divisible = True
        self.vertices = self.generate_vertices(num_vertices)
        
    def generate_vertices(self, num_vertices):
        vertices = []
        for i in range(num_vertices):
            angle = (360 / num_vertices) * i + random.uniform(-20, 20)
            x_offset = math.cos(math.radians(angle)) * self.size
            y_offset = math.sin(math.radians(angle)) * self.size
            vertices.append((x_offset, y_offset))
        return vertices

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.x, self.y = wrap_coordinates(self.x, self.y)

    
    def draw(self):
        for i in range(len(self.vertices)):
            x1, y1 = self.x + self.vertices[i][0], self.y + self.vertices[i][1]
            x2, y2 = self.x + self.vertices[(i + 1) % len(self.vertices)][0], self.y + self.vertices[(i + 1) % len(self.vertices)][1]
    
            wrapped_x1, wrapped_y1 = wrap_coordinates(x1, y1)
            wrapped_x2, wrapped_y2 = wrap_coordinates(x2, y2)
    
            draw_horizontal_line = abs(wrapped_x1 - wrapped_x2) < 72 / 2
            draw_vertical_line = abs(wrapped_y1 - wrapped_y2) < 40 / 2
    
            if draw_horizontal_line and draw_vertical_line:
                thumby.display.drawLine(int(wrapped_x1), int(wrapped_y1), int(wrapped_x2), int(wrapped_y2), 1)
            elif draw_horizontal_line:
                if wrapped_y1 > wrapped_y2:
                    thumby.display.drawLine(int(wrapped_x1), int(wrapped_y1 - 40), int(wrapped_x2), int(wrapped_y2), 1)
                else:
                    thumby.display.drawLine(int(wrapped_x1), int(wrapped_y1 + 40), int(wrapped_x2), int(wrapped_y2), 1)
            elif draw_vertical_line:
                if wrapped_x1 > wrapped_x2:
                    thumby.display.drawLine(int(wrapped_x1 - 72), int(wrapped_y1), int(wrapped_x2), int(wrapped_y2), 1)
                else:
                    thumby.display.drawLine(int(wrapped_x1 + 72), int(wrapped_y1), int(wrapped_x2), int(wrapped_y2), 1)


class SmallAsteroid(Asteroid):
    def __init__(self, x, y, size, angle, num_vertices=6):
        super().__init__(x, y, size, angle, num_vertices)
        self.speed = random.uniform(0.5, 1)
        self.divisible = False  # Set 'divisible' to False for SmallAsteroid
        

class Projectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 2

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        if 0 <= self.x < 72 and 0 <= self.y < 40:
            thumby.display.setPixel(int(self.x), int(self.y), 1)
    
    def off_screen(self):
        return self.x < 0 or self.x >= 72 or self.y < 0 or self.y >= 40


# Add a new class for FlyingSaucer
class FlyingSaucer:
    def __init__(self):
        self.x = random.choice([0, 72])
        self.y = random.choice([random.randint(2, 12), random.randint(28, 38)])
        self.speed = random.uniform(0.5, 1)
        self.direction = random.choice([-1, 1])
        self.size = 8
        self.alive = True
        self.b_array = bytearray([2,5,7,5,5,7,5,2])

    def update(self):
        self.x += self.direction * self.speed
        if self.x < 0 or self.x > 72:
            self.alive = False

    def draw(self):
        if self.alive:
            wrapped_x, wrapped_y = wrap_coordinates(self.x, self.y)
            # thumby.display.drawFilledRectangle(int(wrapped_x - self.size // 2), int(wrapped_y - self.size // 2), self.size, 3, 1)
            thumby.display.blit(self.b_array, int(wrapped_x - self.size // 2), int(wrapped_y - self.size // 2), 8, 3, 0, 0, 0)
            
            
class SaucerProjectile:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * PROJECTILE_SPEED
        self.y -= math.sin(math.radians(self.angle)) * PROJECTILE_SPEED

    def draw(self):
        thumby.display.setPixel(int(self.x), int(self.y), 1)

    def off_screen(self):
        return self.x < 0 or self.x > 72 or self.y < 0 or self.y > 40
      

def draw_pixel_burst(x, y, num_pixels=8):
    for _ in range(num_pixels):
        angle = random.randint(0, 360)
        distance = random.randint(1, 3)
        px = int(x + math.cos(math.radians(angle)) * distance)
        py = int(y + math.sin(math.radians(angle)) * distance)
        thumby.display.setPixel(px, py, 1)

        
# Load the high score
high_score = load_high_score()
titlescreen = True

while True:
    while titlescreen:
        titlescreen = True
        title_img = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,8,54,8,8,0,0,0,0,0,0,0,0,0,0,0,0,
           0,2,5,61,65,61,5,2,0,62,65,54,20,54,65,62,0,60,66,41,66,60,0,46,81,85,69,58,0,2,5,61,65,61,5,2,0,62,65,85,85,42,0,62,65,53,53,73,118,0,62,65,93,65,62,0,62,65,62,0,127,65,73,34,28,0,46,81,85,69,58,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,4,4,27,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0])
        thumby.display.fill(0)
        thumby.display.blit(title_img, 0, 0, 72, 40, -1, 0, 0)
            
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("Press A", 22, 25, 1)
        thumby.display.update()
        time.sleep(0.1)
        if thumby.buttonA.justPressed():
            titlescreen = False
            instructions = True
    
    
    while instructions:
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("Fire: 'A'", 5, 2, 1)
        thumby.display.drawText("Turn: 'L'/'R'", 5, 12, 1)
        thumby.display.drawText("Thrust: 'Up'", 5, 22, 1)
        thumby.display.drawText("Warp: 'B'", 5, 32, 1)
        thumby.display.update()
    
        if thumby.buttonA.justPressed():
            spaceship = Spaceship(72 // 2, 40 // 2, 0)
            asteroids = []
            projectiles = []
            saucer_projectiles = []
            score = 0
            thumby.display.setFPS(FRAME_RATE)
            instructions = False
            game_over = False

    saucer_spawn_interval = 10 * FRAME_RATE  # Spawn a saucer every 10 seconds
    saucer_spawn_counter = 0
    flying_saucer = None    
    
    while not game_over:
        thumby.display.fill(0)
        spaceship.update()
        spaceship.check_teleport()
        spaceship.draw()
        
        
        # Update saucer_spawn_counter and spawn FlyingSaucer if needed
        saucer_spawn_counter += 1
        if saucer_spawn_counter >= saucer_spawn_interval:
            if flying_saucer is None or not flying_saucer.alive:
                flying_saucer = FlyingSaucer()
                saucer_spawn_counter = 0
    
        # Update and draw FlyingSaucer if it exists
        if flying_saucer is not None:
            flying_saucer.update()
            flying_saucer.draw()

            # Check if the saucer has fired a projectile
            if not hasattr(flying_saucer, 'has_fired'):
                flying_saucer.has_fired = False

            # If the saucer hasn't fired a projectile, make it shoot one towards the player
            if not flying_saucer.has_fired and 0 <= flying_saucer.x <= 72 and 0 <= flying_saucer.y <= 40:
                offsetx = random.choice([-6, -5, -4 -3, 3, 4, 5, 6])
                offsety = random.choice([-6, -5, -4 -3, 3, 4, 5, 6])
                dx = (spaceship.x + offsetx) - flying_saucer.x
                dy = (spaceship.y + offsety) - flying_saucer.y
                angle_to_player = math.degrees(math.atan2(-dy, dx))
                saucer_projectile = SaucerProjectile(flying_saucer.x, flying_saucer.y, angle_to_player)
                saucer_projectiles.append(saucer_projectile)
                flying_saucer.has_fired = True
        
    
        colliding_projectiles = []
        for projectile in projectiles:
            projectile.update()
            projectile.draw()
            
            
            if flying_saucer is not None and flying_saucer.alive:
                if distance(projectile.x, projectile.y, flying_saucer.x, flying_saucer.y) <= flying_saucer.size + PROJECTILE_SIZE:
                    flying_saucer.alive = False
                    draw_pixel_burst(flying_saucer.x, flying_saucer.y)  # Draw pixel burst
                    colliding_projectiles.append(projectile)
                    score += SCORE_INCREMENT * 5  # Extra points for shooting down a saucer
                
            
            for asteroid in asteroids:
                if distance(projectile.x, projectile.y, asteroid.x, asteroid.y) <= ASTEROID_SIZE + PROJECTILE_SIZE:
                    asteroids.remove(asteroid)
                    colliding_projectiles.append(projectile)
                    score += SCORE_INCREMENT
    
                    # Spawn new smaller asteroids if the asteroid is divisible
                    if asteroid.divisible:  # Check if the asteroid is divisible
                        new_asteroid_count = random.randint(2, 3)
                        for _ in range(new_asteroid_count):
                            new_angle = random.randint(0, 360)
                            new_size = asteroid.size * 0.5
                            offset = new_size + PROJECTILE_SIZE + 3  # Add an extra 3 for safety margin
                            small_asteroid = SmallAsteroid(
                                asteroid.x + math.cos(math.radians(new_angle)) * offset,
                                asteroid.y + math.sin(math.radians(new_angle)) * offset,
                                new_size,
                                new_angle
                            )
                            if num_small_asteroids < MAX_SMALL_ASTEROIDS:
                                asteroids.append(small_asteroid)
                                
        # Update and draw saucer projectiles
        for saucer_projectile in saucer_projectiles:
            saucer_projectile.update()
            saucer_projectile.draw()

            # Check if the saucer projectile has hit the player
            if distance(spaceship.x, spaceship.y, saucer_projectile.x, saucer_projectile.y) <= SPACESHIP_SIZE + PROJECTILE_SIZE:
                game_over = True
                game_over_screen = True
                break

            # Remove the saucer projectile if it's off-screen
            if saucer_projectile.off_screen():
                saucer_projectiles.remove(saucer_projectile)

        
        for asteroid in asteroids:
            asteroid.update()
            asteroid.draw()
            
            
        thumby.display.drawText("Score: " + str(score), 0, 0, 1)
    
        if thumby.buttonA.justPressed():
            if len(projectiles) < MAX_PROJECTILES:
                projectiles.append(Projectile(spaceship.x, spaceship.y, spaceship.angle))
    
        if thumby.buttonL.pressed():
            # Rotate the spaceship counterclockwise
            spaceship.angle -= 10
    
        if thumby.buttonR.pressed():
            # Rotate the spaceship clockwise
            spaceship.angle += 10
    
        colliding_projectiles = []
        for projectile in projectiles:
            for asteroid in asteroids:
                if distance(projectile.x, projectile.y, asteroid.x, asteroid.y) <= ASTEROID_SIZE + PROJECTILE_SIZE:
                    asteroids.remove(asteroid)
                    colliding_projectiles.append(projectile)
                    score += SCORE_INCREMENT
                    break
        
        projectiles = [p for p in projectiles if p not in colliding_projectiles and not p.off_screen()]
    
    
        num_big_asteroids = sum(1 for asteroid in asteroids if asteroid.divisible)
        num_small_asteroids = len(asteroids) - num_big_asteroids
        
        if num_big_asteroids < MAX_BIG_ASTEROIDS:
            angle = random.randint(0, 360)
            edge = random.choice(["top", "bottom", "left", "right"])
    
            offset = ASTEROID_SIZE / 2

            if edge == "top":
                x = random.randint(0, 72)
                y = -offset
            elif edge == "bottom":
                x = random.randint(0, 72)
                y = 40 + offset
            elif edge == "left":
                x = -offset
                y = random.randint(0, 40)
            else:  # edge == "right"
                x = 72 + offset
                y = random.randint(0, 40)
            asteroids.append(Asteroid(x, y, ASTEROID_SIZE, angle))
            
        for asteroid in asteroids:
            if distance(spaceship.x, spaceship.y, asteroid.x, asteroid.y) <= ASTEROID_SIZE + SPACESHIP_SIZE:
                game_over = True
                game_over_screen = True
                
        # Check for collisions between the spaceship and the flying saucer
        if flying_saucer is not None and flying_saucer.alive:
            if distance(spaceship.x, spaceship.y, flying_saucer.x, flying_saucer.y) <= SPACESHIP_SIZE + (flying_saucer.size / 2):
                game_over = True
                game_over_screen = True
                
        thumby.display.update()
        
        if score > high_score:
            high_score = score
            save_high_score(high_score)  # Save the new high score to the file
    
    while game_over_screen:
        game_over_screen = True
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("Game Over", 10, 5, 1)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("Score: " + str(score), 10, 18, 1)
        thumby.display.drawText("Press B", 10, 28, 1)
        thumby.display.update()
        time.sleep(0.1)
        if thumby.buttonB.justPressed():
            game_over_screen = False
            high_score_screen = True
            
    while high_score_screen:
        high_score_screen = True
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("High Score", 10, 5, 1)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("Score: " + str(high_score), 10, 18, 1)
        thumby.display.drawText("Press B", 10, 28, 1)
        thumby.display.update()
        time.sleep(0.1)
        if thumby.buttonB.justPressed():
            high_score_screen = False
            titlescreen = True
