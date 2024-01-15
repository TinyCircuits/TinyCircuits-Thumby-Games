import thumby
import time
import random
from sys import path
path.append("/Games/Clucker")
import fonthandler


# Game constants
SCREEN_WIDTH = thumby.display.width
SCREEN_HEIGHT = thumby.display.height
CHICKEN_SIZE = 3
CAR_HEIGHT = 4
LANE_HEIGHT = 10
MAX_LEVELS = 10 # Make evenly divisible by 2
LANES = [(6, 12), (13, 19), (22, 28), (29, 35)]  # y coordinates of the lanes

thumby.display.setFPS(15)

# Initialize save data
thumby.saveData.setName("Clucker")
if thumby.saveData.hasItem("highscore"):
    high_score = int(thumby.saveData.getItem("highscore"))
else:
    high_score = 0
    
    
# Function to play cluck and squawk sounds
def play_cluck():
    thumby.audio.play(800, 20)
    
def play_squawk():
    thumby.audio.play(1000, 20)
    time.sleep(0.1)
    thumby.audio.play(1350, 60)
    time.sleep(0.02)
    thumby.audio.play(1700, 150)
    time.sleep(0.05)
    thumby.audio.play(1400, 100)
    time.sleep(0.1)
    
    
# 30 x 30 pixels
right_sprite = bytearray([255,255,255,255,255,255,255,255,255,255,63,223,95,63,31,207,111,111,47,31,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,63,207,247,251,252,252,142,6,22,142,124,156,234,103,55,23,151,215,239,255,255,255,255,255,
           255,255,255,255,255,255,248,225,207,159,159,63,63,63,63,63,152,199,15,216,212,212,211,239,255,255,255,255,255,255,
           63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,62,61,60,62,63,63,63,63,63,63,63,63,63,63,63])
down_sprite = bytearray([255,255,255,255,255,255,255,255,255,127,127,63,63,191,191,191,127,127,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,127,7,1,248,254,255,255,255,255,159,15,15,79,158,253,243,3,139,155,39,127,255,255,255,255,
           255,255,255,255,252,249,251,250,128,121,141,182,198,198,198,141,29,243,7,251,252,248,240,243,247,248,255,255,255,255,
           63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,62,63,63,63,63,63,63,63,63,63,63,63,63])
left_sprite = bytearray([255,255,255,255,255,255,255,255,255,255,255,31,207,111,31,63,63,63,63,127,127,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,253,114,10,10,134,252,120,134,127,63,63,127,255,254,254,252,225,7,255,255,255,255,255,255,
           255,255,255,255,255,253,250,250,250,251,57,21,142,143,220,26,24,156,207,15,247,251,252,255,255,255,255,255,255,255,
           63,63,63,63,63,63,63,63,63,63,62,61,61,61,60,62,63,62,62,63,63,63,63,63,63,63,63,63,63,63])
up_sprite = bytearray([255,255,255,255,255,255,255,255,255,255,255,63,223,63,127,255,255,255,127,127,191,127,255,255,255,255,255,255,255,255,
           255,255,255,255,135,59,115,67,7,207,247,120,179,46,44,88,216,216,219,236,231,192,23,55,167,207,255,255,255,255,
           255,255,255,255,255,249,246,244,240,243,239,222,188,188,124,126,127,63,63,191,159,199,224,248,255,255,255,255,255,255,
           63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63,63])

lines = bytearray([127,127,255,255,255,247,246,253,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,251,253,254,255,127,191,255,
           255,255,127,191,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,238,219,187,251])

game_over_image = bytearray([0,252,134,182,182,244,0,248,52,54,52,248,0,254,12,24,12,254,0,252,182,182,134,132,0,0,0,0,252,134,134,134,252,0,126,224,192,224,126,0,252,182,182,134,132,0,252,102,102,102,220,0,
           0,0,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,1,0,0,0,1,0])
           
win_image = bytearray([0,0,126,0,126,0,0,14,24,240,24,14,0,252,134,134,134,252,0,254,128,128,128,254,0,0,0,0,254,128,224,128,254,0,132,134,254,134,132,0,254,24,48,96,254,0,0,126,0,126,0,0,
            0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0])
            
notes_1 = [

    (523, 250),  # C5
    (587, 250),  # D5
    (659, 250),  # E5
    (698, 250),  # F5

    (523, 250),  # C5
    (587, 250),  # D5
    (659, 250),  # E5
    (587, 250),  # D5

    (698, 250),  # F5
    (784, 250),  # G5
    (880, 250),  # A5
    (784, 250),  # G5
    
    (880, 250),  # A5
    (784, 250),  # G5
    (698, 250),  # F5
    (587, 250),  # D5

    (523, 250),  # C5
    (587, 250),  # D5
    (659, 250),  # E5
    (587, 250),  # D5

    (523, 250),  # C5
    (587, 250),  # D5
    (659, 250),  # E5
    (698, 250),  # F5

    (880, 250),  # A5
    (784, 250),  # G5
    (698, 250),  # E5
    (587, 250),  # D5
    
    (523, 1000), # C5
]


# Player class
class Chicken:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = CHICKEN_SIZE
        self.height = CHICKEN_SIZE
        self.img = bytearray([3,6,2])
        self.leftright = 0
    
    # Draw player
    def draw(self):
        thumby.display.blit(self.img, self.x, self.y, self.width, self.height, 0, self.leftright, 0)
        
    # Movement
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Prevent moving out of the screen
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))
        
        # Random clucking chance each time the chicken moves
        if random.random() < 0.3: # 30% chance to cluck
            play_cluck()



class Car:
    def __init__(self, x, y, speed, direction):
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction
        self.max_width = 16  # Maximum vehicle width
        

        self.sprites = [
            {'bitmap': bytearray([6,9,15,9,9,6]), 'width': 6, 'height': 4}, 
            {'bitmap': bytearray([6,9,15,15,9,9,9,15]), 'width': 8, 'height': 4},
            {'bitmap': bytearray([6,9,15,6,15,15,15,15,15,15,15,15]), 'width': 12, 'height': 4},
            {'bitmap': bytearray([6,9,15,6,15,15,15,15,15,15,15,15,15,15,15,15]), 'width': 16, 'height': 4}
        ]
        
        
        self.sprite = random.choice(self.sprites)  # Randomly select a sprite

    def draw(self):
        if self.direction == -1:
            thumby.display.blit(self.sprite['bitmap'], self.x, self.y, self.sprite['width'], self.sprite['height'], 0, 0, 0)
        else:  # If the car is moving to the right, mirror the sprite
            thumby.display.blit(self.sprite['bitmap'], self.x, self.y, self.sprite['width'], self.sprite['height'], 0, 1, 0)


    def move(self):
        self.x += self.speed * self.direction
        # Adjust car reset conditions to account for maximum car width
        if self.direction == -1 and self.x + self.max_width < 0:
            self.reset()
        elif self.direction == 1 and self.x > SCREEN_WIDTH:
            self.reset()

    def reset(self):
        if self.direction == -1:
            self.x = SCREEN_WIDTH + self.max_width
        else:
            self.x = -self.max_width

# Function to play a melody
def play_melody(notes):
    for note, duration in notes:
        if note == 0:  # Rest
            time.sleep(duration / 1000.0)
        else:
            thumby.audio.play(note, duration)
            time.sleep(duration / 1000.0)
        if thumby.inputPressed():
            break


# Function to draw dotted line
def drawDottedLine(y):
    for x in range(0, SCREEN_WIDTH, 4):
        thumby.display.drawLine(x, y, x+2, y, 1)

# Function to create levels
def initialize_level(level):
    cars = []
    # maximum car width
    max_width = 16
    # determine direction for each pair of lanes for first 5 levels
    if level <= 5:
        # First two lanes go in a random direction
        first_pair_direction = random.choice([-1, 1])
        # Second two lanes go in the opposite direction
        second_pair_direction = -first_pair_direction
        directions = [first_pair_direction, first_pair_direction, second_pair_direction, second_pair_direction]
    else:
        # For higher levels, directions are randomized for each lane
        directions = [random.choice([-1, 1]) for _ in range(4)]
    # for each lane
    for index, lane in enumerate(LANES):
        direction = directions[index]
        speed = random.choice(range(1, level+1))  # Random speed for this lane
        # calculate number of cars and spacing
        if speed > 5:
            num_cars = 1
        elif speed > 3:
            num_cars = random.randint(1, 2)
        else:
            num_cars = random.randint(1, 3)
        spacing = (SCREEN_WIDTH - num_cars * max_width) // (num_cars + 1)
        # add cars to the lane
        for i in range(num_cars):
            x = spacing * (i + 1) + max_width * i
            y = (lane[0] + lane[1] - CAR_HEIGHT) // 2  # Center cars vertically in lane
            cars.append(Car(x, y, speed, direction))
    return cars

def draw_score(score, high_score):
    fh.write_white(f"Score: {score} High: {high_score}", 0 , 0)

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-0.5, 0.5)  # Horizontal velocity
        self.vy = random.uniform(-1.3, 0.2)  # Vertical velocity (upwards)
        self.lifespan = 30  # Number of frames the particle will live

    def update(self, y):
        # Update position
        self.x += self.vx
        self.y += self.vy

        # Apply gravity
        self.vy += 0.1

        # Destroy landed particles
        if self.y > y + 2:
            self.lifespan = 0

    def draw(self):
        if self.lifespan > 0:
            thumby.display.setPixel(int(self.x), int(self.y), 1)

    def is_alive(self):
        return self.lifespan > 0

# List to hold particles
particles = []

# Function to create particles
def create_particles(x, y, count=20):
    for _ in range(count):
        particles.append(Particle(x, y))    


# Game initialization
fh = fonthandler.FontHandler()
thumby.display.fill(0)
level = 1
score = 0
chicken = Chicken(SCREEN_WIDTH // 2, SCREEN_HEIGHT - CHICKEN_SIZE)
cars = initialize_level(level)

# Title Screen
def draw_title(): # 72 x 40
    title_image = bytearray([0,0,255,255,255,0,255,0,0,0,0,219,0,0,0,0,255,0,255,255,255,255,255,255,255,191,183,239,255,255,127,135,155,203,199,195,217,141,141,69,227,255,255,255,255,223,239,247,255,255,255,255,255,255,0,255,0,0,0,0,109,0,0,0,0,255,0,255,255,255,0,0,
           0,0,255,255,255,0,255,0,0,0,0,182,0,0,0,0,255,0,255,255,251,251,255,255,255,255,255,7,121,254,255,255,255,241,224,226,241,15,243,253,12,134,130,114,250,253,255,255,119,219,221,223,255,255,0,255,0,0,0,0,219,0,0,0,0,255,0,255,255,255,0,0,
           0,0,255,255,255,0,63,128,128,128,128,173,0,0,0,128,63,0,127,127,127,127,123,61,191,63,127,127,60,185,51,115,103,39,167,167,135,179,152,1,123,58,186,58,125,127,63,191,63,126,61,191,191,191,128,191,128,0,0,0,182,128,128,128,128,63,0,255,255,255,0,0,
           0,0,255,255,0,254,255,255,3,3,3,3,1,0,255,255,255,0,0,0,0,0,0,255,255,255,0,0,255,255,255,0,254,255,255,3,3,3,3,1,0,255,255,255,240,240,255,191,31,0,255,255,255,227,227,227,67,1,0,255,255,255,243,243,255,191,30,64,255,255,0,0,
           0,0,255,255,224,15,159,63,56,56,56,184,16,0,31,63,191,56,184,184,184,144,192,207,159,191,184,184,191,159,207,224,207,159,191,184,184,184,184,144,192,159,191,159,193,193,159,191,159,192,159,191,191,184,56,184,56,16,0,31,191,31,1,1,31,191,31,192,255,255,0,0])
    thumby.display.fill(0)
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.blit(title_image, 0, 0, 72, 40, -1, 0, 0)
    thumby.display.update()
    while True:
        play_melody(notes_1)
        if thumby.inputPressed():
            break
        time.sleep(0.1)

# Draw title screen and wait for a button press to start the game
draw_title()

game_over = False

# Main game loop
while(True):
    if not game_over:
        # Handle button inputs
        if(thumby.buttonL.pressed()):
            chicken.move(-1, 0)
            chicken.leftright = 0
        if(thumby.buttonR.pressed()):
            chicken.move(1, 0)
            chicken.leftright = 1
        if(thumby.buttonU.pressed()):
            chicken.move(0, -1)
        if(thumby.buttonD.pressed()):
            chicken.move(0, 1)

    # Draw game state
    thumby.display.fill(0)

    # Draw lanes
    thumby.display.drawLine(0, 5, SCREEN_WIDTH, 5, 1)
    thumby.display.drawLine(0, 35, SCREEN_WIDTH, 35, 1)
    thumby.display.drawLine(0, 19, SCREEN_WIDTH, 19, 1)
    thumby.display.drawLine(0, 21, SCREEN_WIDTH, 21, 1)
    
    # Draw dotted line in the middle
    drawDottedLine(12)
    drawDottedLine(28)

    # Draw score
    draw_score(score, high_score)
    
    particles = [particle for particle in particles if particle.is_alive()]

    for car in cars:
        car.draw()
        car.move()
    if not game_over:
        chicken.draw()
    # Update and draw particles in game loop
    for particle in particles:
        particle.update(chicken.y)
        particle.draw()
    thumby.display.update()

    # Check for collision with cars
    for car in cars:
        if not game_over:
            if (chicken.x < car.x + car.sprite['width'] and chicken.x + chicken.width > car.x and
                chicken.y < car.y + car.sprite['height'] and chicken.y + chicken.height > car.y):
                play_squawk()
                create_particles(chicken.x, chicken.y)
                game_over = True
                # game over
            
    if game_over and not particles:
        game_over = False
        thumby.display.fill(0)
        thumby.display.blit(game_over_image, 10, 10, 52, 10, -1, 0, 0)
        thumby.display.drawText("SCORE: " + str(score), 21, 24, 1)
        thumby.display.update()
        time.sleep(2)
        print('Game Over! Score: ', score)
        if score > high_score:
            high_score = score
            thumby.saveData.setItem("highscore", high_score)
            thumby.saveData.save()
        draw_title()
        level = 1
        score = 0
        chicken = Chicken(SCREEN_WIDTH // 2 - 2, SCREEN_HEIGHT - CHICKEN_SIZE)
        cars = initialize_level(level)

    # Check if chicken reached top
    if chicken.y <= 3:
        level += 1
        score += 1
        chicken.y = SCREEN_HEIGHT - CHICKEN_SIZE
        chicken.x = SCREEN_WIDTH // 2 - 2
        if level <= MAX_LEVELS:
            cars = initialize_level(level)
            if level == MAX_LEVELS / 2 + 1:
                thumby.display.fill(1)
                thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
                thumby.display.drawText("HALFWAY", 5, 5, 0)
                thumby.display.drawText("THERE!", 10, 15, 0)
                thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
                thumby.display.drawText("SCORE: " + str(score), 21, 30, 0)
                thumby.display.update()
                time.sleep(2)
            else:
                thumby.display.fill(0)
                thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
                thumby.display.drawText("YOU MADE IT!", 13, 10, 1)
                thumby.display.drawText("SCORE: " + str(score), 21, 20, 1)
                thumby.display.update()
                time.sleep(2)
        else:
            # Win Condition Met
            # Array of bitmaps for each rotation frame
            bitmaps = [down_sprite, left_sprite, up_sprite, right_sprite]
            
            frames = 21
            counter = 0
            animating = True
            while animating:
                if counter < frames:
                    for bitmap in bitmaps:
                        thumby.display.fill(1)
                        # Display the bitmap
                        thumby.display.blit(bitmap, 21, 3, 30, 30, -1, 0, 0)
                        if bitmap == right_sprite:
                            thumby.display.blit(lines, 20, 9, 32, 16, 1, 0, 0)
                        thumby.display.update()
                        counter += 1
                        thumby.audio.play(200 * counter, 20)
                        # Delay for animation speed
                        time.sleep(0.1)
                else:
                    animating = False
                    time.sleep(2)

                    
            thumby.display.fill(0)
            thumby.display.blit(win_image, 10, 9, 52, 10, -1, 0, 0)
            thumby.display.drawText("Score: " + str(score), 19, 24, 1)
            thumby.display.update()
            time.sleep(2)
            print('You won! Score: ', score)
            if score > high_score:
                high_score = score
                thumby.saveData.setItem("highscore", high_score)
                thumby.saveData.save()
            level = 1
            score = 0
            chicken = Chicken(SCREEN_WIDTH // 2 - 2, SCREEN_HEIGHT - CHICKEN_SIZE)
            cars = initialize_level(level)
            draw_title()
            game_over = False
            thumby.display.update()

    time.sleep(0.1)
    