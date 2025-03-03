# Magic Eight Ball for Thumby
# A fortune-telling game with immersive animations

import thumby
import time
import random
import math

# Initialize the display
thumby.display.setFPS(30)
thumby.display.fill(0)

# Game states
STATE_START = 0
STATE_SHAKE = 1
STATE_FORTUNE = 2

# Current game state
current_state = STATE_START

# List of possible fortunes
fortunes = [
    "IT IS\nCERTAIN",
    "IT IS\nDECIDEDLY\nSO",
    "WITHOUT A\nDOUBT",
    "YES\nDEFINITELY",
    "YOU MAY\nRELY ON IT",
    "AS I SEE\nIT, YES",
    "MOST\nLIKELY",
    "OUTLOOK\nGOOD",
    "YES",
    "SIGNS POINT\nTO YES",
    "REPLY HAZY\nTRY AGAIN",
    "ASK AGAIN\nLATER",
    "BETTER NOT\nTELL YOU\nNOW",
    "CANNOT\nPREDICT\nNOW",
    "CONCENTRATE\nAND ASK\nAGAIN",
    "DON'T\nCOUNT\nON IT",
    "MY REPLY\nIS NO",
    "MY SOURCES\nSAY NO",
    "OUTLOOK NOT\nSO GOOD",
    "VERY\nDOUBTFUL"
]

# Current fortune and previous fortune
current_fortune = ""
previous_fortune = ""

# Animation variables
shake_frames = 0
shake_counter = 0
fade_counter = 0
noise_level = 0
bubble_positions = []

# Draw the start screen
def draw_start_screen():
    # Draw eight ball border to make it look like we're looking through the window
    thumby.display.drawRectangle(0, 0, 72, 40, 1)
    thumby.display.drawRectangle(1, 1, 70, 38, 1)
    
    # Draw title text
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    thumby.display.drawText("MAGIC", 18, 5, 1)
    thumby.display.drawText("EIGHT BALL", 8, 15, 1)
    
    # Draw the number 8 with a simple background (using lines instead of a triangle)
    thumby.display.drawLine(28, 30, 50, 30, 1)
    thumby.display.drawLine(28, 30, 39, 18, 1)
    thumby.display.drawLine(50, 30, 39, 18, 1)
    #thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.drawText("8", 37, 22, 1)
    
    # Draw instructions
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.drawText("A/B to shake", 12, 32, 1)

# Draw the fortune with word wrapping
def draw_fortune(text, alpha=1.0):
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    lines = text.split('\n')
    y = max(0, (40 - len(lines) * 10) // 2)
    
    for line in lines:
        x = max(0, (72 - len(line) * 6) // 2)
        
        # Only draw the text if random value is less than alpha (for fade effect)
        if random.random() < alpha:
            thumby.display.drawText(line, x, y, 1)
        y += 10

# Create bubble effect
def initialize_bubbles():
    global bubble_positions
    bubble_positions = []
    
    # Create random bubbles
    for _ in range(10):
        x = random.randint(5, 67)
        y = random.randint(5, 35)
        size = random.randint(1, 3)
        speed = random.uniform(0.2, 0.8)
        bubble_positions.append([x, y, size, speed])

# Update and draw bubbles
def update_bubbles():
    global bubble_positions
    
    for i, bubble in enumerate(bubble_positions):
        # Move bubble up
        bubble[1] -= bubble[3]
        
        # If bubble goes off screen, reset at bottom
        if bubble[1] < -5:
            bubble[0] = random.randint(5, 67)
            bubble[1] = 45
            
        # Draw bubble
        thumby.display.drawFilledRectangle(int(bubble[0]), int(bubble[1]), bubble[2], bubble[2], 1)
        
        # Update in the list
        bubble_positions[i] = bubble

# Generate random noise pattern for shaking effect
def generate_noise(intensity):
    for y in range(0, 40, 2):
        for x in range(0, 72, 2):
            if random.random() < intensity / 10.0:
                thumby.display.setPixel(x, y, 1)

# Shake animation - simulates the fluid becoming cloudy and bubbling
def animate_shake():
    global shake_frames, shake_counter, bubble_positions, noise_level
    
    shake_frames += 1
    
    # Draw the eight ball window border
    thumby.display.drawRectangle(0, 0, 72, 40, 1)
    
    # Calculate noise intensity - increases then decreases
    if shake_frames < 30:
        noise_level = min(10, shake_frames // 3)
    else:
        noise_level = max(0, 10 - (shake_frames - 30) // 3)
    
    # Generate noise pattern with current intensity
    generate_noise(noise_level)
    
    # Update and draw bubbles
    update_bubbles()
    
    # Occasionally show the previous fortune fading out
    if shake_frames < 30 and previous_fortune and random.random() < 0.3:
        fade_alpha = max(0, 1.0 - (shake_frames / 30.0))
        draw_fortune(previous_fortune, fade_alpha)
    
    # Shake the screen slightly
    shake_offset = random.randint(-2, 2)
    thumby.display.drawLine(0, 0 + shake_offset, 71, 0 + shake_offset, 1)
    thumby.display.drawLine(0, 39 + shake_offset, 71, 39 + shake_offset, 1)
    
    # Check if shake animation is complete
    if shake_frames >= 60:
        return True
    return False

# Animate the fortune appearing from the cloudy fluid
def animate_fortune_reveal():
    global fade_counter
    
    fade_counter += 1
    
    # Draw the eight ball window border
    thumby.display.drawRectangle(0, 0, 72, 40, 1)
    
    # Calculate fade-in alpha
    alpha = min(1.0, fade_counter / 30.0)
    
    # Generate decreasing noise as the text becomes clearer
    noise_intensity = max(0, 10 - fade_counter // 3)
    generate_noise(noise_intensity)
    
    # Update and draw bubbles (they continue throughout)
    update_bubbles()
    
    # Draw the fortune with current alpha
    draw_fortune(current_fortune, alpha)
    
    # Check if fade animation is complete
    if fade_counter >= 30:
        return True
    return False

# Initialize the game
initialize_bubbles()

# Main game loop
while True:
    thumby.display.fill(0)
    
    # Handle button inputs
    if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
        if current_state == STATE_START or current_state == STATE_FORTUNE:
            current_state = STATE_SHAKE
            shake_frames = 0
            shake_counter = 0
            # Store previous fortune before selecting a new one
            previous_fortune = current_fortune
            # Select a random fortune
            current_fortune = random.choice(fortunes)
            # Reset bubbles for shake animation
            initialize_bubbles()
    
    # Update and render based on current state
    if current_state == STATE_START:
        draw_start_screen()
    
    elif current_state == STATE_SHAKE:
        # Run shake animation
        if animate_shake():
            current_state = STATE_FORTUNE
            fade_counter = 0
    
    elif current_state == STATE_FORTUNE:
        # Run fortune transition animation or show fortune
        if fade_counter < 30:
            animate_fortune_reveal()
        else:
            # Draw the eight ball window border
            thumby.display.drawRectangle(0, 0, 72, 40, 1)
            # Draw fully revealed fortune
            draw_fortune(current_fortune)
            # Still show some occasional bubbles
            update_bubbles()
    
    # Update the display
    thumby.display.update()