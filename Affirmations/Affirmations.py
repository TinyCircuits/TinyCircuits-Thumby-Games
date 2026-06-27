# AFFIRMATIONS
# V0.1 Last Editted 2023-02-09
# Author: AlinaLikesCozy

# A SIMPLE DAILY AFFIRMATIONS APP. 
# DISPLAYS AND REPEATS A RANDOMLY SELECTED AFFIRMATION.
# GREAT STARTER PROJECT - PLEASE EDIT AND ENJOY <3

# Press A or B to bring up Pause Menu



import time
import thumby
import math
import machine

import random

# ADD YOUR AFFIRMATIONS HERE
# "PUT AFFIRMATION IN BETWEEN QUOTES" THEN COMMA
# NO COMMA AFTER LAST AFFIRMATION
affirmations = [
"I am worthy of love and happiness",
"I am capable of achieving my dreams",
"I choose to focus on positivity and joy",
"I am strong and resilient",
"I am grateful for all the blessings in my life",
"My thoughts and actions create my reality",
"My potential is unlimited",
"My self-confidence grows every day",
"I trust the journey of my life",
"I am surrounded by love and support",

"I choose to let go of negative thoughts and emotions",
"I am successful in all areas of my life",
"I am constantly improving and growing",
"My happiness is within reach",
"I am deserving of financial abundance",
"My relationships are fulfilling and loving",
"I am filled with energy and vitality",
"I am confident in my abilities",
"My future is bright and full of opportunities",
"I am at peace with my past",

"I am able to handle anything that comes my way",
"My hard work and determination pay off",
"I am proud of who I am and what I have accomplished",
"I am creating a life I love",
"My self-love and self-acceptance increase every day",
"I am in control of my emotions and reactions",
"I am a beacon of positivity and light",
"My mind and body are healthy",
"I am attracting abundance and prosperity",
"I am living my best life",

"I am making a positive impact on the world",
"My creativity and imagination flourish",
"I am comfortable being myself",
"I am open to new experiences and growth",
"I am full of inner peace and contentment",
"My mind is clear and focused",
"I am constantly learning and expanding my knowledge",
"I am embracing change with excitement",
"My self-esteem is high",
"I am spreading kindness and love wherever I go",

"I am surrounded by beauty and joy",
"I am proud of my unique qualities and talents",
"I am living life to the fullest",
"My heart is filled with love and compassion",
"I am confident in making decisions that align with my values",
"I am grateful for the journey of self-discovery",
"I am surrounded by abundance in all forms",
"My past experiences have made me a better person",
"I am proud of my progress and growth",
"I am a powerful and unstoppable force"
] 

# Spinning heart frames
# BITMAP: width: 9, height: 8; Heart Normal frame 1
bitmap1 = bytearray([14,31,63,126,252,126,63,29,14])
# BITMAP: width: 9, height: 8; frame 2
bitmap2 = bytearray([0,15,63,126,252,126,63,15,0])
# BITMAP: width: 9, height: 8; frame 3
bitmap3 = bytearray([0,0,31,127,252,127,31,0,0])
# BITMAP: width: 9, height: 8; frame 4
bitmap4 = bytearray([0,0,0,127,255,127,0,0,0])



# Spinning sprite heart
heartSprite = thumby.Sprite(9, 8, bitmap1)
heartAnimation = thumby.Sprite(9,8, bitmap1 + bitmap2 + bitmap3 + bitmap4 + bitmap3 + bitmap2, key = 0)


# Variables
thumby.display.setFPS(45)

i = random.randint(0,len(affirmations)-1)
x = 70
start = 0
textspeed = 15
scrolling = True
affirmation = affirmations[i]

wasPressed = False
anCounter = 0 #animation counter for tracking frame of heart
framesCounter = 0 #count the frames of FPS for the animation

while(True):
    
    ###############
    #  Scrolling  #
    ###############
    
    while(scrolling):
        t0 = time.ticks_ms()   # Get time (ms)
        
        # Reset button
        if(thumby.actionPressed() == False and wasPressed == True):
            wasPressed = False
            print("Let go button")
        
        # Pause menu interaction
        if((thumby.buttonA.pressed() == True and wasPressed == False ) or (thumby.buttonB.pressed() == True and wasPressed == False)):
            wasPressed = True
            scrolling = False
        
        bobRate = 400 # Set arbitrary bob rate (higher is slower)
        bobRange = 7  # How many pixels to move the sprite up/down (-5px ~ 5px)
    
        # Calculate number of pixels to offset sprite for bob animation
        bobOffset = math.sin(t0 / bobRate) * bobRange
        
        # Center the sprite using screen and bitmap dimensions and apply bob offset
        heartAnimation.x = int((thumby.display.width/2) - (9/2))
        heartAnimation.y = (6 + bobOffset)
        
        # Set the heart frame for spinning Animation
        heartAnimation.setFrame(anCounter)
        framesCounter += 1
        
        # Set animation frame to change every 13 frames
        if (framesCounter >= 13):
            anCounter += 1 
            framesCounter =0
        
        # Draw affirmation test
        thumby.display.fill(0) # Fill canvas to black
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        
        
        # Text scrolling moving every number of textspeed frames, advance counter
        if (len(affirmation)>12):
            thumby.display.drawText(affirmation, x, 28, 1)
            
                    
            # Start scrolling offset
            if start != textspeed:
                start += 1
            
            # Next text frame
            if (start == textspeed or start > textspeed):
                x -= 1
                
            # If position is smaller than characters in string times pixel width 6    
            if (x-1 < ((-1)*len(affirmation)*6 ) ):
                x = 70
                start = 0
                
        else:
            thumby.display.drawText(affirmation, 2, 28, 1)
            
     
        # Display the bitmap using bitmap data, position, and bitmap dimensions
        thumby.display.drawSprite(heartAnimation)
        
        # Update display
        thumby.display.update()
                       
    ##############
    # Pause Menu #
    ##############
    
    while(scrolling == False):
        print("in pause menu")
        thumby.display.fill(1)
        thumby.display.drawFilledRectangle(0, 0, thumby.display.width, 7, 0)
        thumby.display.drawText("Breathe.", 15, 0, 1)
        
        thumby.display.drawText("Would you", 11, 9, 0)
        thumby.display.drawText("like a new", 5, 17, 0)
        thumby.display.drawText("affirmation?", 2, 25, 0)
       
        thumby.display.drawText("A:Yes  B:No", 1, 33, 0) 
        thumby.display.update()
        
        # Reset press button state
        if(thumby.actionPressed() == False and wasPressed == True):
            wasPressed = False
            print("pause menu action not pressed")
            
        if(not wasPressed and thumby.buttonA.pressed() == True):
            print("pause menu A button")
            x = 70
            start = 0
            
            # Don't repeat index
            previous_i = i
            
            while (i == previous_i):
                i = random.randint(0,len(affirmations)-1)
                print("previous index:", previous_i, "; current index: ",  i)
            
            affirmation = affirmations[i]
            
            thumby.display.fill(0) 
            wasPressed = True
            scrolling = True
            
        # Reset Thumby
        elif(not wasPressed and thumby.buttonB.pressed() == True):
            print("pause menu B button")
            # Quit
            machine.reset()
        

                    
            