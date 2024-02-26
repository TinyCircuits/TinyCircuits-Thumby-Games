import thumby
import random
import time
import math
from sys import path as syspath
syspath.insert(0, '/Games/LyteBykes')
from thumbyGrayscale import display, Sprite
display.enableGrayscale()
display.setFPS(15)

# Game parameters
SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40
player_score = 0
ai_score = 0
play = True
play_to_score = 5 # Winning/losing score.  Adjust to change game length.

# Initial player and AI positions and directions
player_position = (10, SCREEN_HEIGHT // 2 + 3)
player_direction = (1, 0)  # Moving right
ai_position = (SCREEN_WIDTH - 11, SCREEN_HEIGHT // 2 + 3)
ai_direction = (-1, 0)  # Moving left

# TITLE SONG
# Define the notes as tuples (frequency, duration)
# Duration is in milliseconds
# Rests (silence) can be represented as frequency 0
notes = [
    # First part
    (587, 120),  # D5
    (0, 120),     # Rest
    (587, 120),  # D5
    (0, 30),     # Rest
    (587, 120),  # D5
    (0, 30),     # Rest
    (698, 120),  # F5
    (0, 30),     # Rest
    (784, 240),  # G5
    (0, 60),     # Rest
    (880, 120),  # A5
    (0, 30),     # Rest
    (880, 120),  # A5
    (0, 30),     # Rest
    (784, 120),  # G5
    (0, 30),     # Rest
    (698, 120),  # F5
    (0, 30),     # Rest
    (587, 120),  # D5
    (0, 30),     # Rest
    (523, 480),  # C5
    (0, 180),    # Longer rest

    # Second part - variation
    (523, 120),  # C5
    (0, 30),     # Rest
    (523, 120),  # C5
    (0, 30),     # Rest
    (523, 120),  # C5
    (0, 30),     # Rest
    (523, 120),  # C5
    (0, 30),     # Rest
    (587, 120),  # D5
    (0, 30),     # Rest
    (659, 240),  # E5
    (0, 60),     # Rest
    (698, 120),  # F5
    (0, 30),     # Rest
    (698, 120),  # F5
    (0, 30),     # Rest
    (659, 120),  # E5
    (0, 30),     # Rest
    (587, 120),  # D5
    (0, 30),     # Rest
    (523, 120),  # C5
    (0, 30),     # Rest
    (587, 480),  # D5
    (0, 180),    # Longer rest
]

# Function to play a melody
def play_melody():
    global play
    for note, duration in notes:
        if note == 0:  # Rest
            time.sleep(duration / 1000.0)
        else:
            thumby.audio.play(note, duration)
            time.sleep(duration / 1000.0)
        if thumby.inputPressed():
            play = False
            break

# Function to display the title screen
def show_title_screen():
    global play
    title = bytearray([255,1,1,1,1,1,1,1,9,25,233,9,9,249,1,1,1,1,1,1,9,25,41,73,137,17,33,65,65,33,17,137,73,169,217,169,145,137,137,137,137,137,137,9,9,137,137,137,137,137,129,249,9,233,9,9,201,73,73,73,73,73,73,121,1,1,1,1,1,1,1,255,
           255,0,0,0,0,0,0,0,0,0,255,128,128,143,136,136,136,136,136,136,136,136,136,8,248,129,190,128,128,254,1,0,0,0,0,0,0,0,0,0,0,0,255,128,128,255,0,0,0,0,0,0,0,255,128,128,157,149,149,151,144,144,144,240,0,0,0,0,0,0,0,255,
           255,0,0,252,4,4,4,228,164,68,4,20,228,4,20,36,68,132,8,16,32,64,32,16,8,132,68,36,16,8,228,4,4,4,252,64,32,16,8,132,68,36,16,8,228,4,4,4,196,68,68,68,68,68,124,0,240,24,12,132,68,68,68,68,68,68,68,108,56,0,0,255,
           255,0,0,255,0,0,0,120,72,72,48,3,4,136,112,0,0,0,1,254,0,0,0,254,1,0,0,0,0,0,255,0,0,0,224,64,132,10,17,32,64,128,0,0,255,0,0,0,57,41,41,47,32,0,224,32,163,38,44,40,41,41,41,41,41,17,3,134,252,0,0,255,
           239,168,168,171,170,170,170,170,170,170,170,170,169,168,168,168,168,168,168,171,170,170,170,171,168,168,168,168,168,168,171,170,170,42,235,136,184,161,170,170,170,170,171,168,171,170,170,170,170,170,170,170,170,170,171,168,171,170,170,170,170,170,170,170,170,170,171,169,168,184,128,255])
    display.fill(0)
    display.blit(title, 0, 0, 72, 40, -1, 0, 0)
    # display.drawText("LyteBykes", 10, 10, 1)
    # display.drawText("Press A, 5, 20, 1)
    display.update()
    while play:
        play_melody()
    reset_game()
        
    
        
def play_crash_sound(speed):
    frequency = int(random.randrange(500, 2000) * speed)  # A4 note, you can change this to get different sounds
    duration = 300  # Duration in milliseconds
    if frequency > 20:
        thumby.audio.play(frequency, duration)

# Function to reset the game state
def reset_game():
    global player_position, player_direction, ai_position, ai_direction
    player_position = (10, SCREEN_HEIGHT // 2 + 3)
    player_direction = (1, 0)
    ai_position = (SCREEN_WIDTH - 11, SCREEN_HEIGHT // 2 + 3)
    ai_direction = (-1, 0)
    display.fill(0)

def draw_player():
    display.setPixel(player_position[0], player_position[1], 1)

def draw_ai():
    display.setPixel(ai_position[0], ai_position[1], display.DARKGRAY)

def move_player():
    global player_position
    global player_direction

    # Compute the new head position
    new_position = ((player_position[0] + player_direction[0]) % SCREEN_WIDTH, (player_position[1] + player_direction[1]) % SCREEN_HEIGHT)

    # Check if player has hit a trail
    if display.getPixel(new_position[0], new_position[1]) != 0:
        return False  # Game over

    # Move the player
    player_position = new_position

    # Draw the player
    draw_player()

    return True  # Game continues

def distance(p1, p2):
    # Manhattan distance
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def ai_new_direction():
    global player_position, ai_position, ai_direction, player_score

    # Directions that the AI can move
    directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    directions.remove((-ai_direction[0], -ai_direction[1]))  # Prevent AI from reversing direction

    # Calculate new head position for each direction
    new_positions = [((ai_position[0] + d[0]) % SCREEN_WIDTH, (ai_position[1] + d[1]) % SCREEN_HEIGHT) for d in directions]

    # Remove any directions that would lead to a collision
    safe_directions = [d for d, p in zip(directions, new_positions) if display.getPixel(p[0], p[1]) == 0]
    
    # If no safe directions, return without changing direction
    if not safe_directions:
        create_explosion(*ai_position)
        # play_crash_sound()
        player_score += 1
        while particles:
            display.fill(0)
            update_particles()
            display.update()
            time.sleep(0.05)
        reset_game()
        
        return

    # If the player is close, try to move closer
    if distance(player_position, ai_position) < 10:
        if random.random() < 0.6:  # 50% chance to try to move closer
            if player_position[0] > ai_position[0] and (1, 0) in safe_directions:
                ai_direction = (1, 0)
            elif player_position[0] < ai_position[0] and (-1, 0) in safe_directions:
                ai_direction = (-1, 0)
            elif player_position[1] > ai_position[1] and (0, 1) in safe_directions:
                ai_direction = (0, 1)
            elif player_position[1] < ai_position[1] and (0, -1) in safe_directions:
                ai_direction = (0, -1)
            return

    # Otherwise, pick a random safe direction
    ai_direction = random.choice(safe_directions)

def move_ai():
    global ai_position, ai_direction

    # Compute the new head position
    new_position = ((ai_position[0] + ai_direction[0]) % SCREEN_WIDTH, (ai_position[1] + ai_direction[1]) % SCREEN_HEIGHT)

    # If the AI hits a wall or itself, or randomly, it changes direction
    if display.getPixel(new_position[0], new_position[1]) != 0 or random.random() < 0.07:  # 7% chance to change direction
        ai_new_direction()
        return True

    # Move the AI
    ai_position = new_position

    # Draw the AI
    draw_ai()

    return True  # Game continues

def control_player():
    global player_direction
    if thumby.buttonU.pressed() and player_direction != (0, 1):
        player_direction = (0, -1)
    elif thumby.buttonD.pressed() and player_direction != (0, -1):
        player_direction = (0, 1)
    elif thumby.buttonL.pressed() and player_direction != (1, 0):
        player_direction = (-1, 0)
    elif thumby.buttonR.pressed() and player_direction != (-1, 0):
        player_direction = (1, 0)


# Particles for explosion effect
particles = []

# Function to create an explosion
def create_explosion(x, y):
    global particles
    for _ in range(20):  # Create 20 particles
        vx = random.uniform(-1, 1)
        vy = random.uniform(-1, 1)
        particles.append([(x, y), (vx, vy)])

# Function to update and draw particles
def update_particles():
    global particles
    new_particles = []
    for (x, y), (vx, vy) in particles:
        # Move the particle
        x += vx
        y += vy
        # Decrease the velocity (simulates friction)
        vx *= 0.9
        vy *= 0.9
        # Determine the color based on the speed
        speed = (vx**2 + vy**2)**0.5
        play_crash_sound(speed)
        color = max(0, int(4 - speed * 4))  # Map speed in range [0, 1] to color in range [4, 0]
        # Draw the particle
        display.setPixel(int(x), int(y), color)
        # If the particle's speed is significant, keep it
        if speed > 0.1:
            new_particles.append([(x, y), (vx, vy)])
    particles = new_particles

# Winner Fireworks    
def create_fireworks(x, y):
    global particles

    # Animate a mortar shooting up to the burst point
    for mortar_y in range(SCREEN_HEIGHT, y, -2):
        display.fill(0)
        display.setPixel(x, mortar_y, 1)
        display.update()
        time.sleep(0.05)  # Short delay to animate the movement

    # Create the fireworks particles at the burst point
    for _ in range(20):  # Number of particles in the firework
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 1.5)  # Speed of the particles
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        particles.append([(x, y), (vx, vy)])

# Functions for Win/Lose Conditions    
def show_win_screen():
    global particles
    display.fill(0)
    # Create fireworks
    for _ in range(5):  # Number of fireworks bursts
        particles = []
        create_fireworks(random.randint(15, SCREEN_WIDTH - 15), random.randint(10, SCREEN_HEIGHT - 15))
        for _ in range(25):  # Duration of each burst
            display.fill(0)
            update_particles()
            display.update()
            time.sleep(0.05)
    display.fill(0)        
    display.blit(bytearray([0,0,126,0,126,0,0,14,24,240,24,14,0,252,134,134,134,252,0,254,128,128,128,254,0,0,0,0,254,128,224,128,254,0,132,134,254,134,132,0,254,24,48,96,254,0,0,126,0,126,0,0,
           0,0,1,0,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,1,0,0,0,1,0,0,1,0,1,0,0]), 10, 5, 52, 10, -1, 0, 0)
    display.drawText("Press Any", 18, 22, 1)
    display.drawText("Button", 24, 29, 1)
    display.update()
    wait_for_input()

def show_game_over_screen():
    display.fill(0)
    display.drawText("Press Any", 18, 22, 1)
    display.drawText("Button", 24, 29, 1)
    display.blit(bytearray([0,252,134,182,182,244,0,248,52,54,52,248,0,254,12,24,12,254,0,252,182,182,134,132,0,0,0,0,252,134,134,134,252,0,126,224,192,224,126,0,252,182,182,134,132,0,252,102,102,102,220,0,
           0,0,1,1,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,1,1,1,0,0,1,0,0,0,1,0]), 10, 5, 52, 10, -1, 0, 0)
    display.update()
    wait_for_input()

def wait_for_input():
    global play, particles
    while True:
        if thumby.inputPressed():
            particles = []
            play = True
            break
        time.sleep(0.1)

def reset_scores():
    global player_score, ai_score
    player_score = 0
    ai_score = 0

    

# Show the title screen
show_title_screen()
while True:
    display.setFont("/lib/font3x5.bin", 3, 5, 1)
    reset_game()
    # Main game loop
    while True:
        # Handle input
        control_player()
        move_ai()
        # Check for collisions and restart the game
        if not move_player():
            create_explosion(player_position[0], player_position[1])
            # play_crash_sound()
            ai_score += 1

            while particles:
                display.fill(0)
                update_particles()
                display.update()
                time.sleep(0.05)
            reset_game()
            break
    
        # Draw game state
        draw_player()
        draw_ai()
    
        # Update and draw particles
        update_particles()
        
        # Display Score
        display.drawText(str(player_score), 6, 0, 1)
        display.drawText(str(ai_score), 62, 0, display.DARKGRAY)
        
        if player_score >= play_to_score:
            show_win_screen()
            reset_scores()
            show_title_screen()
        elif ai_score >= play_to_score:
            show_game_over_screen()
            reset_scores()
            show_title_screen()
        
        # Refresh the screen
        display.drawRectangle(0, 6, thumby.display.width, thumby.display.height - 6, 1)
        
        display.update()
    
        # Sleep
        time.sleep(0.05)


