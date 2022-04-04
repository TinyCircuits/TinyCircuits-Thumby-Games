import thumby
import random
import machine
import math
import time

"""
            ** Floppy the Flapping Bird Game **
    
    Created by: Camerin Figueroa
    
    Github: RaspberryProgramming
    Website: https://www.camscode.com/
    
    Designed for the Thumby - https://thumby.us/
    Kickstarter Page: https://www.kickstarter.com/projects/kenburns/thumby-the-tiny-playable-keychain
    
    Emulate using their handy Web IDE: https://code.thumby.us/
    
    
"""



"""
                Global Vars
"""

# Device Specific
display_dim = [72, 40] # w, h

# Default bird pos

def_bird_pos = [5, 16]

# Display Objects

"""
Example

obj = {
    "type": "bitmap" | "text" | "rectangle",
    "text" | "bitmap": bytearray | "",
    "pos": [x,y],
    "dim": [w,h]
}

"""

bird = {
    "type": "bitmap",
    "bitmap": [
        bytearray([0,112,240,240,244,108,158,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,7,7,7,6,5,5,5,5,5,3,0,0]),
        bytearray([0,192,208,216,220,220,62,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,6,7,7,6,5,5,5,5,5,3,0,0]),
        bytearray([0,128,176,184,188,188,126,254,226,92,62,62,36,56,64,128,0,
           0,3,3,3,1,6,7,7,6,5,5,5,5,5,3,0,0]),
        bytearray([0,192,208,216,220,220,62,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,6,7,7,6,5,5,5,5,5,3,0,0]),
        ],
    "pos": [def_bird_pos[0], def_bird_pos[1]],
    "dim": [17, 12],
    "frame": 0
}

# BITMAP: width: 17, height: 12
bitmap0 = bytearray([0,192,208,216,220,220,62,254,226,92,62,62,36,56,64,128,0,
           0,0,0,2,2,6,7,7,6,5,5,5,5,5,3,0,0])
# BITMAP: width: 17, height: 12
bitmap2 = bytearray([0,128,176,184,188,188,126,254,226,92,62,62,36,56,64,128,0,
           0,3,3,3,1,6,7,7,6,5,5,5,5,5,3,0,0])

score_text = {
    "type": "text",
    "text": "0",
    "pos": [display_dim[0]-18, display_dim[1]-7],
    "dim": None
}

# Dictates the space between each pipe (Should be bird's height + 2)
space_btw = bird["dim"][0] + 3


"""
                Functions
"""

def playEnd():
    """
    playEnd: Plays music at the end of the game
    """
    
    # Notes based on frequency
    endMusic = [1108, 1108]
    
    # Play each note
    for i in endMusic:
        thumby.audio.play(i, 110)
        time.sleep(0.1)
    

def drawObj(obj):
    """
    drawObj: Draws and object (Stored in dictionary format).
             Should be defined like display object above
    """
    
    # Bitmap
    if obj["type"] == "bitmap":
        # Support multiple frames to animate bitmap object
        if (type(obj["bitmap"]) == list):
            
            # If we're at the last frame, reset
            if (obj["frame"] >= len(obj["bitmap"])-1):
                obj["frame"] = 0
            else:
                # Increment frame
                obj["frame"] += 1
            
            bmp = obj["bitmap"][obj["frame"]] # Extract current bitmap frame
            
            # Display bitmap
            thumby.display.blit(bmp, obj["pos"][0], obj["pos"][1], obj["dim"][0], obj["dim"][1], -1, 0, 0)
        else:    
            
            # Display bitmap
            thumby.display.blit(obj["bitmap"], obj["pos"][0], obj["pos"][1], obj["dim"][0], obj["dim"][1], -1, 0, 0)
        
    # Rectangle
    elif obj["type"] == "rectangle":
        thumby.display.drawFilledRectangle(obj["pos"][0], obj["pos"][1], obj["dim"][0], obj["dim"][1], 1)
     
    # Text  
    elif obj["type"] == "text":
        
        thumby.display.drawFilledRectangle(obj["pos"][0], obj["pos"][1], len(obj["text"])*6, 7, 0) # Draw blank space behind text
        
        # Draw text
        thumby.display.drawText(obj["text"], obj["pos"][0], obj["pos"][1], 1)
        
    else:
        # ERROR
        thumby.display.fill(0)
        thumby.display.drawText("ERROR", 10, 15, 1)


def newPipe(x, y, w, h):
    """
    Create pipe object
    """
    
    return {
        "type": "rectangle",
        "pos": [x,y],
        "dim": [w, h]
    }

def generatePipe():
    """
    Generate set of two new pipes
    """
    y = random.randrange(0, display_dim[1]-space_btw) # Get random y height
    
    # Generate two new pipes with some space between
    top = newPipe(display_dim[0], (y-display_dim[1]), 10, 40)
    bottom = newPipe(display_dim[0], y+space_btw, 10, 40)
    
    return [top, bottom]
    
def detectCollision(obj1, obj2):
    
    """
    Detects if two objects are within a collision
    """
    
    # Generate a set of points
    
    r_point1 = [obj1["pos"][0]+obj1["dim"][0], obj1["pos"][1]+obj1["dim"][1]]
    l_point1 = [obj1["pos"][0], obj1["pos"][1]]
    r_point2 = [obj2["pos"][0]+obj2["dim"][0], obj2["pos"][1]+obj2["dim"][1]]
    l_point2 = [obj2["pos"][0], obj2["pos"][1]]

    # Check if the objects are right/left of the other
    if (r_point1[0] <= l_point2[0] or l_point1[0] >= r_point2[0]):
        return False
    
    # Check if objects are on top/below each other
    if (r_point1[1] <= l_point2[1] or l_point1[1] >= r_point2[1]):
        return False
    
    # Return True for collision
    return True
    
def startScreen():
    
    playing = True # Keeps startScreen running until b is pressed
    
    pipes = generatePipe() # Generate new pipes for animation
    
    showText = True # Determines if subtext will be shown
    
    i = 0
    
    # Text for the screen
    title = {"type":"text", "text":"Floppy", "pos":[15,0], "dim":None}
    subtext = {"type":"text", "text":"Press B", "pos":[13, 32], "dim":None}
    
    while(playing):
        
        if (thumby.buttonB.justPressed()):
            playing = False
        
        # Counter used to control elements of scene
        i += 1
        
        # Turn text on/off
        if (i%10 == 0):
            showText = not showText
        
        # Move pipes
        for p in pipes:
            p["pos"][0] -= 2
        
        # Remove old Pipes           
        if pipes[0]["pos"][0]+pipes[0]["dim"][0] < 0:
            del pipes[0]
            del pipes[0]
        
        # Add New Pipes
        if (pipes[-1]["pos"][0]+pipes[-1]["dim"][0] < display_dim[0]-26):
            pipes += generatePipe()
            

        bird["pos"][1] = int(((math.sin(i/5)+1)*14)+2) # Change bird y pos
        
        gameRender(bird, pipes, -1, []) # Render Game Scene
        
        drawObj(title) # redraw the title
        
        if (showText):
            drawObj(subtext);
                
        # Update the display
        thumby.display.update()
        
        # Render text
        
        time.sleep(0.1)

    
def gameRender(bird, pipes, score, soundQueue):
    # Rerender scene
        
    thumby.display.fill(0)
    
    drawObj(bird)
    
    for p in pipes:
        drawObj(p)
        
    # Write the score
    if (score >= 0):
        score_text["text"] = str(score)
    
        drawObj(score_text)
    
    # Update the display
    thumby.display.update()
    
    # Play sound
    
    if (len(soundQueue) > 0):
        thumby.audio.play(soundQueue[0], 110)
        del soundQueue[0]
    

def game():
    """
    
    Run the game
    
    """
    
    # Reset Position
    bird["pos"] = [def_bird_pos[0], def_bird_pos[1]]

    # Controls whether the game is over
    gameover = False
    
    soundQueue = [] # Queue for storing sound notes

    pipes = generatePipe() # Generate initial pipes
    
    steps = 0
    
    score = 0
    
    gameRender(bird, pipes, score, soundQueue)
    
    time.sleep(1)
    
    while (not gameover):
        
        # Run logic
        
        steps += 1
        
        # Move floppy up/down
        if thumby.buttonA.pressed() and bird["pos"][1] > 0: # Button was pressed so floppy goes up
            bird["pos"][1] -= 3
        else:
            # Floppy drifts down
            bird["pos"][1] += 1
        
        # Add new pipes
        if (pipes[-1]["pos"][0]+pipes[-1]["dim"][0] < display_dim[0]-26):
            pipes += generatePipe()
        
        # Move pipes
        for p in pipes:
            p["pos"][0] -= 2
        
        # Delete old pipes
        if pipes[0]["pos"][0]+pipes[0]["dim"][0] < 0:
            del pipes[0]
            del pipes[0]
            
            # Increase score and play sound
            soundQueue += [1046, 1396, 1396, 1396]
            
            score += 1
            
        
        # Detect collisions and endgame if so
        if (bird["pos"][1] > 40-bird["dim"][1]
            or detectCollision(bird, pipes[0])
            or detectCollision(bird, pipes[1])):
            
            # End Game
            gameover = True
            
        # Render the game
        gameRender(bird, pipes, score, soundQueue)
        
        # WAIT
        time.sleep(0.1)
       
    # Return the score when finished     
    return score
    
"""

                MAIN FUNCTION

"""

def main():
    
    startScreen()
    
    while (True):
        score = game()
        
        time.sleep(1)
        
        # End Screen
        
        # Clear Screen
        thumby.display.fill(0)
    
        # Render bird in new pos
        bird["pos"][1] = display_dim[1]-bird["dim"][1]
        drawObj(bird)
        
        # Render Text
        thumby.display.drawText("Game Over", 10, 3, 1)
        
        thumby.display.drawText("Score %d" % score, 10, 15, 1)
        
        thumby.display.drawText("Press B", 25, 30, 1)
        
        # Update Screen
        thumby.display.update()
        
        # Play end music
        playEnd()
        
        
        waiting = True
        
        # Loop till button is pressed
        while(waiting):
            if thumby.buttonB.justPressed():
                waiting = False
                
            # Animate bird while waiting
            drawObj(bird)
            
            thumby.display.update()
            
            time.sleep(0.1)

main() # Run Program
