# Dr. C. Dice
# Version 1.1
# By Charles "Cyndi" Cavanaugh, Ph.D.
# https://www.cyndicavanaugh.com/
import time
import thumby
import math
import random
from machine import ADC

adc = ADC(26)
charging = 38000
thumby.display.setFPS(15)
sides = 6

def center(text, y=0, width=5, height=7, spacing=1, color=1):
    x = int((72 - (width + spacing) * len(text)) / 2)
    thumby.display.setFont(f"/lib/font{width}x{height}.bin", width, height, spacing)
    thumby.display.drawText(text, x, y, color)
    
def roll(sides):
    battery=charging
    voltage=adc.read_u16()
    battery=min(battery,voltage)
    extra_rolls = battery % 256
    pre_rolls = random.randint(30, 50) + extra_rolls
    
    while(pre_rolls > 0):
        p = random.randint(1, sides)
        pre_rolls = pre_rolls - 1
    return random.randint(1, sides)


while(1):
    thumby.display.fill(0)
    center("Dice", 0)
    center("by", 8)
    center("Dr.Cavanaugh", 16)
    center("Any)continue", 32)
    thumby.display.update()
    
    while not thumby.inputJustPressed():
        thumby.display.update()
    
    choose_dice = True
    test_mode = False
    while(choose_dice):
        thumby.display.fill(0)
        center(f"^v){sides} sides", 0)
        center(f"<>)test {"on" if test_mode else "off"}", 8)
        center("A)roll!", 16)
        thumby.display.update()
        
        while not thumby.inputJustPressed():
            thumby.display.update()
            
        if(thumby.buttonU.pressed()):
            sides = sides + 1
        if(thumby.buttonR.pressed()):
            test_mode = True
        if(thumby.buttonL.pressed()):
            test_mode = False
        if(thumby.buttonD.pressed()):
            sides = max(sides - 1, 2)
        if(thumby.buttonA.pressed()):
            choose_dice = False
    
    roll_again = True
    while(roll_again):
        thumby.display.fill(0)
        center("Rolling", 16, 8, 8)
        center("Dice", 24, 8, 8)
        thumby.display.update()
        
        if test_mode:
            results = []
            rolls = 100
            for i in range(rolls):
                results.append(roll(sides))
            frequency = {}
            for items in results:
                frequency[items] = results.count(items)
            result_display = True
            side = 1
            while result_display:
                thumby.display.fill(0)
                center("Test results", 0)
                center(f"^v)side {side}", 8)
                center(f"{frequency.get(side)} times", 16)
                center(f"{rolls} rolls", 24)
                center("A)continue", 32)
                thumby.display.update()
        
                while not thumby.inputJustPressed():
                    thumby.display.update()
                    
                if(thumby.buttonU.pressed()):
                    side = min(side + 1,sides)
                if(thumby.buttonD.pressed()):
                    side = max(side - 1,1)
                if(thumby.buttonA.pressed()):
                    result_display = False
                    thumby.display.fill(0)
                    thumby.display.update()
        else:
            r = roll(sides)
            thumby.audio.play(1500, 350)
        
            thumby.display.fill(0)
            center("Dice", 0, 8, 8)
            center(str(r), 8, 8, 8)
            center(f"{sides} sides", 24)
            thumby.display.update()
        
        center("A)gain B)ack", 32)
        thumby.display.update()
        
        while not thumby.actionJustPressed():
            thumby.display.update()
            
        if(thumby.buttonB.pressed()):
            roll_again = False
            
