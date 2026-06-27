import time
import thumby
import math
import thumbyButton as buttons
from thumbyGraphics import display
import random




thumby.display.setFPS(15)
hyperspace = 0
timer = 0
x = 5
y = 20
rotation = 0
speed = 0
bullets = []
asteriods = []
explosions = []
level = 1
menu = 1
lives = 3
def createexplosion(x, y, distance):
    explosions.append([x, y, distance, random.randint(0, 360), random.randint(0, 360), random.randint(0, 360), random.randint(0, 360), random.randint(0, 360)])
def explosion():
    for e in explosions:
        if e[2] > 5:
            explosions.remove(e)
        e[2] += 1
        display.drawLine(e[0], e[1], e[0] + round(math.sin(math.radians(e[3])) * e[2]), e[1] + round(math.cos(math.radians(e[3])) * e[2]), 1)
        display.drawLine(e[0], e[1], e[0] + round(math.sin(math.radians(e[4])) * e[2]), e[1] + round(math.cos(math.radians(e[3])) * e[2]), 1)
        display.drawLine(e[0], e[1], e[0] + round(math.sin(math.radians(e[5])) * e[2]), e[1] + round(math.cos(math.radians(e[3])) * e[2]), 1)
        display.drawLine(e[0], e[1], e[0] + round(math.sin(math.radians(e[6])) * e[2]), e[1] + round(math.cos(math.radians(e[3])) * e[2]), 1)
        display.drawLine(e[0], e[1], e[0] + round(math.sin(math.radians(e[7])) * e[2]), e[1] + round(math.cos(math.radians(e[3])) * e[2]), 1)
        
def createasteriods(cool):
        for c in range(cool):
            asteriods.append([random.randint(35, 60), random.randint(5, 35), random.randint(0, 360), random.uniform(1.0, 1.5), random.randint(1, 5), random.randint(1, 4), 360])
one = 0
two = 0
three = 0

def asteriod():
    global timer
    global lives
    for p in asteriods:
        for collect in bullets:
           one = collect[0] + round(math.sin(math.radians(collect[2])) * collect[3]) - p[0]
           two = collect[1] + round(math.cos(math.radians(collect[2])) * collect[3]) - p[1]
           one = one ** 2
           two = two ** 2
           three = math.sqrt(one + two)
           one = p[2] + collect[2]
           one = one / 2
           if round(three) <= p[4]:
               if p[4] > 2:
                  if random.randint(1, 2) == 1:
                     createexplosion(p[0], p[1], 0)
                     asteriods.append([p[0], p[1] + 1, one + random.randint(-20, 20), random.uniform(1, 2.5), random.randint(1, 2), random.randint(1, 4), 360])
                     asteriods.append([p[0], p[1] + 1, one + random.randint(-20, 20), random.uniform(1, 2.5), random.randint(1, 2), random.randint(1, 4), 360])
                     asteriods.remove(p)
                  else:
                     createexplosion(p[0], p[1], 0)
                     asteriods.append([p[0], p[1] + 1, one + random.randint(-20, 20), random.uniform(1, 2.5), random.randint(1, 3), random.randint(1, 4), 360])
                     asteriods.remove(p)
                  
               else:
                  createexplosion(p[0], p[1], 0)
                  asteriods.remove(p)
        one = x - p[0]
        two = y - p[1]
        one = one ** 2
        two = two ** 2
        three = math.sqrt(one + two)
        one = p[2] + rotation
        one = one / 2
        if round(three) <= p[4] + 2:
            if timer == 10:
                timer = 0
                lives -= 1
            if p[4] > 2:
                if random.randint(1, 2) == 1:
                     createexplosion(p[0], p[1], 0)
                     asteriods.append([p[0], p[1] + 1, one + random.randint(-20, 20), random.uniform(1, 2.5), random.randint(1, 2), random.randint(1, 4), 360])
                     asteriods.append([p[0], p[1] + 1, one + random.randint(-20, 20), random.uniform(1, 2.5), random.randint(1, 2), random.randint(1, 4), 360])
                     asteriods.remove(p)
                else:
                     createexplosion(p[0], p[1], 0)
                     asteriods.append([p[0], p[1] + 1, one + random.randint(-20, 20), random.uniform(1, 2.5), random.randint(1, 3), random.randint(1, 4), 360])
                     asteriods.remove(p)
                  
            else:
                  p[2] = one + random.randint(-20, 20)
                  createexplosion(p[0], p[1], 0)
      
      
        if p[0] > 70:
            p[0] = -5
        if p[0] < -5:
            p[0] = 70
        if p[1] > 40:
            p[1] = -5
        if p[1] < -5:
           p[1] = 40
        p[6] += p[5]
        p[2] = p[2]
        p[0] = p[0] + round(math.sin(math.radians(p[2])) * p[3])
        p[1] = p[1] + round(math.cos(math.radians(p[2])) * p[3])
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] - 45)) * p[4]), p[1] + round(math.cos(math.radians(p[6] - 45)) * p[4]), p[0] + round(math.sin(math.radians(p[6])) * p[4]), p[1] + round(math.cos(math.radians(p[6])) * p[4]), 1)
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] + 45)) * p[4]), p[1] + round(math.cos(math.radians(p[6] + 45)) * p[4]), p[0] + round(math.sin(math.radians(p[6])) * p[4]), p[1] + round(math.cos(math.radians(p[6])) * p[4]), 1)
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] - 90)) * p[4]), p[1] + round(math.cos(math.radians(p[6] - 90)) * p[4]), p[0] + round(math.sin(math.radians(p[6] - 45)) * p[4]), p[1] + round(math.cos(math.radians(p[6] - 45)) * p[4]), 1)
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] + 90)) * p[4]), p[1] + round(math.cos(math.radians(p[6] + 90)) * p[4]), p[0] + round(math.sin(math.radians(p[6] + 45)) * p[4]), p[1] + round(math.cos(math.radians(p[6] + 45)) * p[4]), 1)
        
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] - 135)) * p[4]), p[1] + round(math.cos(math.radians(p[6] - 135)) * p[4]), p[0] + round(math.sin(math.radians(p[6] - 90)) * p[4]), p[1] + round(math.cos(math.radians(p[6] - 90)) * p[4]), 1)
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] + 135)) * p[4]), p[1] + round(math.cos(math.radians(p[6] + 135)) * p[4]), p[0] + round(math.sin(math.radians(p[6] + 90)) * p[4]), p[1] + round(math.cos(math.radians(p[6] + 90)) * p[4]), 1)
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] - 180)) * p[4]), p[1] + round(math.cos(math.radians(p[6] - 180)) * p[4]), p[0] + round(math.sin(math.radians(p[6] - 135)) * p[4]), p[1] + round(math.cos(math.radians(p[6] - 135)) * p[4]), 1)
        display.drawLine(p[0] + round(math.sin(math.radians(p[6] + 180)) * p[4]), p[1] + round(math.cos(math.radians(p[6] + 180)) * p[4]), p[0] + round(math.sin(math.radians(p[6] + 135)) * p[4]), p[1] + round(math.cos(math.radians(p[6] + 135)) * p[4]), 1)

def addbullet(x, y, rotation, d):
    bullets.append([x, y, rotation, d])
def bullet():
    for b in bullets:
        if b[3] > 70:
            bullets.remove(b)
        b[3] += 5
        display.setPixel(b[0] + round(math.sin(math.radians(b[2])) * b[3]), b[1] + round(math.cos(math.radians(b[2])) * b[3]), 1)


while True:
 asteriods.clear()
 explosions.clear()
 bullets.clear()
 lives = 3
 if not menu == 1:
    display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
    thumby.display.fill(0)
    lives = 3
    display.drawText(str('  game  '), 0, 0, 1)
    display.drawText(str('  OVER  '), 0, 10, 1)
    thumby.display.update()
    time.sleep(1)
 display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
 lives = 3
 while menu == 2:
    x = 5
    y = 20
    if buttons.buttonB.pressed():
        menu = 1
    if buttons.buttonA.pressed():
        menu = 1
    if buttons.buttonU.pressed():
        menu = 1
    if buttons.buttonD.pressed():
        menu = 1
    if buttons.buttonL.pressed():
        menu = 1
    if buttons.buttonR.pressed():
        menu = 1
    thumby.display.fill(0)
    lives = 3
    display.drawText(str('  game  '), 0, 0, 1)
    display.drawText(str('  OVER  '), 0, 10, 1)
    thumby.display.update()
 level = 1
 display.setFont("/lib/font8x8.bin", 8, 8, display.textSpaceWidth)
 lives = 3
 while menu == 1:
    if buttons.buttonA.pressed():
          if buttons.buttonL.pressed():
     
           if buttons.buttonR.pressed():
            thumby.display.setFPS(500)
    if buttons.buttonU.pressed():
        level += 1
    if buttons.buttonD.pressed():
        if level > 1:
            level -= 1
    thumby.display.fill(0)
    
    display.drawText(str('Asteroids'), 0, 0, 1)
    
    display.drawText(str('Press B to start'), 2, 20, 1)
    display.drawText(str(f'   {level}    '), 2, 30, 1)
    thumby.display.update()
    if buttons.buttonB.pressed():
        menu = 0
 display.setFont("/lib/font3x5.bin", 3, 5, display.textSpaceWidth)
 lives = 3
 while menu == 0:
    if hyperspace >= 75:
       hyperspace = 75
    else:
       hyperspace += 1
    
    if timer > 10:
       timer = 10
    else:
       timer += 1
    if x > 70:
        x = -5
    if x < -5:
        x = 70
    if y > 40:
        y = -5
    if y < -5:
        y = 40
    thumby.display.fill(0)
    if buttons.buttonR.pressed():
        rotation -= 10
    if buttons.buttonL.pressed():
        rotation += 10
    if rotation < 0:
        rotation = 360
    if rotation > 360:
        rotation = 0
    if buttons.buttonB.justPressed():
        if hyperspace >= 75:
            x = random.randint(1, 69)
            y = random.randint(1, 39)
            hyperspace = 0
    if buttons.buttonA.justPressed():
        addbullet(x, y, rotation, 3)
    if buttons.buttonU.pressed():
         if speed < 2:
             speed += 0.5
         
    else:
        if speed > 0:
            speed -= 0.1
        if speed < 0:
            speed += 0.1
    if buttons.buttonD.justPressed():
        if speed > 0:
            speed = 0
   
    
    
        
    x = x + round(math.sin(math.radians(rotation)) * speed)
    y = y + round(math.cos(math.radians(rotation)) * speed)
    asteriod()
    bullet()
    explosion()
    if buttons.buttonU.pressed():
        display.drawLine(x + round(math.sin(math.radians(rotation - 90)) * 1), y + round(math.cos(math.radians(rotation - 90)) * 1), x + round(math.sin(math.radians(rotation)) * -3), y + round(math.cos(math.radians(rotation)) * -3), 1)
        display.drawLine(x + round(math.sin(math.radians(rotation + 90)) * 1), y + round(math.cos(math.radians(rotation + 90)) * 1), x + round(math.sin(math.radians(rotation)) * -3), y + round(math.cos(math.radians(rotation)) * -3), 1)
    
    
    display.drawLine(x + round(math.sin(math.radians(rotation - 90)) * 2), y + round(math.cos(math.radians(rotation - 90)) * 2), x + round(math.sin(math.radians(rotation)) * -1), y + round(math.cos(math.radians(rotation)) * -1), 1)
    display.drawLine(x + round(math.sin(math.radians(rotation + 90)) * 2), y + round(math.cos(math.radians(rotation + 90)) * 2), x + round(math.sin(math.radians(rotation)) * -1), y + round(math.cos(math.radians(rotation)) * -1), 1)
    
    
    display.drawLine(x + round(math.sin(math.radians(rotation - 90)) * 2), y + round(math.cos(math.radians(rotation - 90)) * 2), x + round(math.sin(math.radians(rotation)) * 5), y + round(math.cos(math.radians(rotation)) * 5), 1)
    display.drawLine(x + round(math.sin(math.radians(rotation + 90)) * 2), y + round(math.cos(math.radians(rotation + 90)) * 2), x + round(math.sin(math.radians(rotation)) * 5), y + round(math.cos(math.radians(rotation)) * 5), 1)
    
    display.drawText(str(f'{lives}'), 0, 0, 1)
    display.drawText(str(f'{hyperspace}'), 0, 10, 1)
    thumby.display.update()
    if len(asteriods) <= 0:
        if level <= 0:
            level = 2
            menu = 1
            bullets.clear()
        bullets.clear()
        x = 5
        y = 20
        level -= 1
        createasteriods(random.randint(1, 5))
    if lives == 0:
        asteriods.clear()
        bullets.clear()
        menu = 2
