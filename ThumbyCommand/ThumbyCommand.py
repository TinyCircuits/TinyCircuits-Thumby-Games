# Thumby command game
# Written by Daniel Spångberg

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import thumby
import random
import math
import gc

# width: 5, height: 5
missile_LD = bytearray([0,0,4,3,2])
missile_RD = bytearray([2,3,4,0,0])
missile_D = bytearray([0,3,6,3,0])
explosion_anim = [bytearray([0,0,4,0,0]),
                    bytearray([0,10,4,10,0]),
                    bytearray([10,27,4,27,10]),
                    bytearray([10,17,0,17,10])]
explosion_anim_rate=60*2
city_sprites = [bytearray([28,16,24,28,16]),
                bytearray([28,16,31,24,28]),
                bytearray([30,28,0,30,24])]

# width: 5, height: 12
nuke_anim = [bytearray([0,0,0,0,0,0,0,12,0,0]),
                bytearray([0,0,0,0,0,0,2,14,2,0]),
                bytearray([0,0,0,0,0,0,3,15,3,0]),
                bytearray([128,192,192,192,128,0,1,15,1,0]),
                bytearray([192,224,224,224,192,0,9,15,9,0]),
                bytearray([96,240,240,240,96,0,8,15,8,0]),
                bytearray([48,120,248,120,48,8,12,15,12,8]),
                bytearray([24,60,252,60,24,12,14,15,14,12]),
                bytearray([12,30,254,30,12,0,15,15,15,0]),
                bytearray([6,15,255,15,6,0,1,15,1,0]),
                bytearray([6,138,255,133,6,0,0,0,0,0]),
                bytearray([4,138,87,133,2,0,0,0,0,0]),
                bytearray([0,2,80,5,0,0,0,0,0,0])]
nuke_anim_rate=60*3
                
# width: 5, height: 5
crosshair = bytearray([4,4,27,4,4])

w=thumby.display.width
h=thumby.display.height

# Crosshair coordinate
cx=int(w/2)
cy=int(h/2)

thumby.display.fill(0)
thumby.display.update()
thumby.display.setFPS(60)


cities=[]
missiles=[]
explosions=[]
nukes=[]

max_missiles=10
# Missile probability
missile_P=0.001
# Min/Max missile speed
missile_speed=(0.3,2)
# Relative missile speed
missile_speed_rel=2./60

max_explosions=5


def draw_scene():
    thumby.display.fill(0)
    # Draw cities
    for city_x,city_type in cities:
           thumby.display.blit(city_sprites[city_type],city_x,h-5,5,5,0,0,0)
    # Draw missiles
    for missile in missiles:
        dx=missile[3]-missile[0]
        dy=h-1-missile[1]
        idlen=1./math.sqrt(dx*dx+dy*dy)
        dx*=idlen
        if dx<-0.5:
            thumby.display.blit(missile_LD,int(missile[0]),int(missile[1]),5,5,0,0,0)
        elif dx>0.5:
            thumby.display.blit(missile_RD,int(missile[0]),int(missile[1]),5,5,0,0,0)
        else:
            thumby.display.blit(missile_D,int(missile[0]),int(missile[1]),5,5,0,0,0)
    # Draw nukes
    for nuke in nukes:
        frame=int(nuke[2]*len(nuke_anim)/nuke_anim_rate)
        thumby.display.blit(nuke_anim[frame],int(nuke[0]),h-12,5,12,-1,0,0)

    # Draw crosshair
    thumby.display.blit(crosshair,cx,cy,5,5,-1,0,0)
    
    # Draw explosions
    for explosion in explosions:
        frame=int(explosion[2]*len(explosion_anim)/explosion_anim_rate)
        thumby.display.blit(explosion_anim[frame],int(explosion[0]),int(explosion[1]),5,5,0,0,0)

    thumby.display.update()

def update_game():
    global missile_P
    
    # Add more missiles?
    if len(missiles)<max_missiles:
        if random.random()<missile_P:
            city_target=int(len(cities)*random.random())
            city_x=cities[city_target][0]
            # x, y, speed, coordinate target
            new_missile=[w*random.random(),0,missile_speed[0]+(missile_speed[1]-missile_speed[0])*random.random(),city_x]
            missiles.append(new_missile)
    # Move missiles
    for missile in missiles:
        dx=missile[3]-missile[0]
        dy=h-1-missile[1]
        idlen=missile_speed_rel/math.sqrt(dx*dx+dy*dy)
        missile[0]+=dx*idlen*missile[2]
        missile[1]+=dy*idlen*missile[2]

    # Update explosion animations (if we get to the end, remove the explosion)
    explosions_to_remove=[]
    for explosion in explosions:
        explosion[2]+=1
        if explosion[2]>=explosion_anim_rate:
            explosions_to_remove.append(explosion)
    
    for e in explosions_to_remove:
        if e in explosions:
            explosions.remove(e)

    # Update nuke animations (if we get to the end, remove the nuke, and the city)
    nukes_to_remove=[]
    cities_to_remove=[]
    for nuke in nukes:
        nuke[2]+=1
        if nuke[2]>=nuke_anim_rate:
            nukes_to_remove.append(nuke)
            # Remove the city
            cities_to_remove.append(nuke[1])
            
    for n in nukes_to_remove:
        if n in nukes:
            nukes.remove(n)
    
    for c in cities_to_remove:
        if c in cities:
            cities.remove(c)

    # Check missile - city collision
    missiles_to_remove=[]
    for missile in missiles:
        for city in cities:
            m_x=missile[0]
            m_y=missile[1]
            c_x=city[0]
            c_y=h-1
            dx=m_x-c_x
            dy=m_y-c_y
            d2=dx*dx+dy*dy
            if d2<25:
                # Collision - remove the missile and add a nuke
                nukes.append([c_x,city,0])
                missiles_to_remove.append(missile)
                thumby.audio.play(300,250)
                
    # Remove missiles that did not hit a city (because it was already blown up)
    for missile in missiles:
        m_y=missile[1]
        if m_y>h-3:
            missiles_to_remove.append(missile)


    # Check missile - explosion collision
    for missile in missiles:
        for explosion in explosions:
            if explosion[2]>explosion_anim_rate*0.5:
                m_x=missile[0]
                m_y=missile[1]
                e_x=explosion[0]
                e_y=explosion[1]
                dx=m_x-e_x
                dy=m_y-e_y
                d2=dx*dx+dy*dy
                if d2<25:
                    # Collision - remove the missile
                    missiles_to_remove.append(missile)
                    thumby.audio.play(400,250)
        

    for m in missiles_to_remove:
        if m in missiles:
            missiles.remove(m)


    if thumby.buttonU.pressed():
        global cy
        cy-=1
        if cy<0:
            cy=0
            
    if thumby.buttonD.pressed():
        global cy
        cy+=1
        if cy>h-6:
            cy=h-6

    if thumby.buttonL.pressed():
        global cx
        cx-=1
        if cx<0:
            cx=0

    if thumby.buttonR.pressed():
        global cx
        cx+=1
        if cx>w-6:
            cx=w-6
            
    if thumby.buttonA.justPressed():
        global cx,cy
        if len(explosions)<max_explosions:
            explosions.append([cx,cy,0])
            thumby.audio.play(500,250)
            

    # Increase the number of missiles
    missile_P+=0.00001/60
    if missile_P>0.01:
        missile_P=0.01



random.seed()

play_again=True
while play_again:
    # Missile probability
    missile_P=0.001
    missiles=[]
    explosions=[]
    nukes=[]
    # X-coordinates of cities, city type
    for i in range(5):
        cities.append((int(random.random()*w),int(random.random()*len(city_sprites))))

    thumby.display.fill(0)
    thumby.display.update()
    thumby.display.drawText("Thumby",int((w-6*5)/2),int((h-7)/2)-10,1)
    thumby.display.drawText("Command",int((w-7*5)/2),int((h-7)/2),1)
    thumby.display.drawText("Press A",int((w-7*5)/2),int((h-7)/2)+10,1)
    thumby.display.update()
    
    while True:
        if thumby.buttonA.justPressed():
            break
    
    while len(cities)>0:
        draw_scene()
        update_game()
    
    
    
    thumby.display.fill(0)
    thumby.display.update()
    thumby.display.drawText("Game Over",int((w-9*5)/2),int((h-7)/2)-10,1)
    thumby.display.drawText("A - play",int((w-8*5)/2),int((h-7)/2),1)
    thumby.display.drawText("B - exit",int((w-8*5)/2),int((h-7)/2)+10,1)
    thumby.display.update()
    while True:
        if thumby.buttonA.justPressed():
            play_again=True
            break
        if thumby.buttonB.justPressed():
            play_again=False
            break






