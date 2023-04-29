import thumby
import random
import time
import math
from collections import namedtuple, deque

from sys import path
path.append("/Games/Aliens")



from game_classes import (
    Star,
    Ship,
    Missile,
    BasicAlien,
    Explosion,
    MissileHUD,
    Logo,
)

MAX_STARS = 10
MAX_MISSILES = 3
MAX_ALIENS = 3
MIN_ALIEN_TIME = 500
MIN_STAR_TIME = 1000
MIN_RESTART_TIME = 4000

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)
thumby.saveData.setName("alieninvaders")

missile_hud = MissileHUD()
logo = Logo()

setup = True

def get_high_score():
    high_score = 0
    if thumby.saveData.hasItem("high_score"):
        high_score = int(thumby.saveData.getItem("high_score"))
    return high_score
    
def set_high_score(score):
    thumby.saveData.setItem("high_score", score)
    thumby.saveData.save()
    
    
def get_alien(num, alien_pool):
    if num < 5:
        new_alien = alien_pool[0].pop()
        if num == 0:
            new_alien.initialize(
                x=random.randint(0, thumby.display.width - new_alien.sprite.width),
                y=-new_alien.sprite.height,
                s=random.randint(50, 100),
                mf=lambda x, y: (x, y+1),
            )
        elif num == 1:
            if random.randint(0,1):
                new_alien.initialize(
                    x=-new_alien.sprite.width,
                    y=random.randint(int(thumby.display.height/2), thumby.display.height - new_alien.sprite.height),
                    s=random.randint(50, 100),
                    mf=lambda x, y: (x+1, y),
                )
            else:
                new_alien.initialize(
                    x=thumby.display.width,
                    y=random.randint(int(thumby.display.height/2), thumby.display.height - new_alien.sprite.height),
                    s=random.randint(50, 100),
                    mf=lambda x, y: (x-1, y),
                )
        elif num == 2:
            if random.randint(0,1):
                new_alien.initialize(
                    x=random.randint(0, int(thumby.display.width/3)),
                    y=-new_alien.sprite.height,
                    s=random.randint(50, 100),
                    mf=lambda x, y: (x+1, y+1),
                )
            else:
                new_alien.initialize(
                    x=random.randint(int(thumby.display.width*(2/3)), thumby.display.width - new_alien.sprite.width),
                    y=-new_alien.sprite.height,
                    s=random.randint(50, 100),
                    mf=lambda x, y: (x-1, y+1),
                )
        elif num == 3:
                new_alien.initialize(
                    x=random.randint(0, thumby.display.width - new_alien.sprite.width),
                    y=-new_alien.sprite.height,
                    s=random.randint(50, 100),
                    mf=lambda x, y: (new_alien.centerx + new_alien.amplitude*math.sin(6*math.pi*(1/thumby.display.height)*y), y+1),
                )
        else:
            if random.randint(0,1):
                new_alien.initialize(
                    x=-new_alien.sprite.width,
                    y=random.randint(int(thumby.display.height/2), thumby.display.height - new_alien.sprite.height),
                    s=random.randint(50, 100),
                    mf=lambda x, y: (x+1, new_alien.centery + new_alien.amplitude*math.sin(6*math.pi*(1/thumby.display.width)*x))
                )
            else:
                new_alien.initialize(
                    x=thumby.display.width,
                    y=random.randint(int(thumby.display.height/2), thumby.display.height - new_alien.sprite.height),
                    s=random.randint(50, 100),
                    mf=lambda x, y: (x-1, new_alien.centery + new_alien.amplitude*math.sin(6*math.pi*(1/thumby.display.width)*x)),
                )
            
        new_alien.alive = True
        return new_alien
        
        
while(1):
    
    if setup:
        game_over = False
        score = 0
        old_high_score = get_high_score()
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        star_list = []
        missile_list = []
        alien_list = []
        explosion_list = []
        star_queue = deque((), MAX_STARS)
        alien_pool = {}
        explosion_queue = deque((), 3)
        
        # Create a list of initial stars
        for _ in range(MAX_STARS):
            star_list.append(Star(
                random.randint(2,4),
                random.randint(0, thumby.display.width),
                random.randint(0, thumby.display.height),
            )
        )
                
        # Create a pool of alien sprites
        for alien_type in (0,):
            alien_pool[alien_type] = []
            for _ in range(MAX_ALIENS):
                alien_pool[alien_type].append(BasicAlien())
                
        for _ in range(3):
            explosion_queue.append(Explosion())
        
        alien_timer = time.ticks_add(time.ticks_ms(), MIN_ALIEN_TIME)
        star_timer = time.ticks_add(time.ticks_ms(), MIN_STAR_TIME)
        restart_wait = 0
        
        ship = Ship(MAX_MISSILES)
        setup = False
    
        # Show logo
        while(1):
            logo.update(time.ticks_ms())
            thumby.display.fill(0)
            thumby.display.drawSprite(logo.sprite)
            thumby.display.update()
            if thumby.buttonA.pressed():
                thumby.display.fill(0)
                # Flush justPressed to prevent firing missile at start of game
                thumby.buttonA.justPressed()
                break
            if thumby.buttonB.pressed():
                thumby.reset()
        
    
    t0 = time.ticks_ms()
    
    # Check for collisions
    for alien in alien_list:
        if ship.alive and alien.collides_with(ship.sprite):
            ship.explosion_sprite.x = ship.sprite.x
            ship.explosion_sprite.y = ship.sprite.y
            ship.alive = False
            restart_wait = time.ticks_add(t0, MIN_RESTART_TIME)
            if score > old_high_score:
                set_high_score(score)
            if explosion_queue:
                explosion_list.append(explosion_queue.popleft().place(ship.sprite.x, ship.sprite.y))
        for missile in missile_list:
            if alien.collides_with(missile.sprite):
                alien.alive, missile.alive = False, False
                score += alien.score()
                if explosion_queue:
                    explosion_list.append(explosion_queue.popleft().place(alien.sprite.x-1, alien.sprite.y-1))
                
    if time.ticks_diff(star_timer, t0) < 0:
    # Possibly add a star to the star list
        if len(star_list) < MAX_STARS and not random.randint(0,10):
            new_star = star_queue.popleft()
            new_star.sprite.x = random.randint(0, thumby.display.width)
            new_star.sprite.y = 0
            star_list.append(new_star)
            star_timer = time.ticks_add(time.ticks_ms(), MIN_STAR_TIME)
        
    if time.ticks_diff(alien_timer, t0) < 0:
        # Possibly spawn an alien
        if len(alien_list) < MAX_ALIENS and random.randint(0, 50) == 0:
            alien_list.append(get_alien(random.randint(0, min(4, score//100)), alien_pool))
            # alien_list.append(get_alien(4, alien_pool))
            alien_timer = time.ticks_add(time.ticks_ms(), MIN_ALIEN_TIME)
        
    # Fill screen with black
    thumby.display.fill(0)
    

    # Draw all stars and move them to their next position
    for star in star_list:
        thumby.display.drawSprite(star.sprite)
        star.move(t0)
       
    # Draw and move missiles
    for missile in missile_list:
        thumby.display.drawSprite(missile.sprite)
        missile.move(t0)
        
    # Draw and move aliens
    for alien in alien_list:
        thumby.display.drawSprite(alien.sprite)
        alien.move(t0)   
        
    # Draw and update explosions
    for explosion in explosion_list:
        thumby.display.drawSprite(explosion.sprite)
        explosion.update(t0)
        
    explosion_list.sort()
    
    while explosion_list and explosion_list[-1].done:
        explosion_queue.append(explosion_list.pop())
      
    if ship.alive:
        # Move the ship 
        ship.move(
            thumby.buttonL.pressed(),
            thumby.buttonR.pressed(),
            thumby.buttonU.pressed(),
            thumby.buttonD.pressed(),
            t0,
        )
        thumby.display.drawSprite(ship.sprite)
        
        # Fire missiles
        if thumby.buttonA.justPressed():
            missile_list.extend(ship.fire(Missile.fire_direction.forward))
        if thumby.buttonB.justPressed():
            missile_list.extend(ship.fire(Missile.fire_direction.side))
    elif game_over or len(explosion_list) == 0:
        game_over = True
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText("GAME", int(thumby.display.width/2) - 12, int(thumby.display.height/2) - 17, 1)
        thumby.display.drawText("OVER", int(thumby.display.width/2) - 12, int(thumby.display.height/2) - 9, 1)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText("HI SCORE", int(thumby.display.width/2) - 12, int(thumby.display.height/2), 1)
        thumby.display.drawText(str(max(old_high_score, score)), int(thumby.display.width/2) - 12, int(thumby.display.height/2) + 7, 1)
        if score > old_high_score:
            thumby.display.drawText("NEW!", int(thumby.display.width/2) - 12 - 18, int(thumby.display.height/2), 1)
            
        if time.ticks_diff(restart_wait, t0) <= 0:
            setup = True

    # Sort the list of stars by vertical position
    star_list.sort()
    
    # Pop all stars from the list that have fallen off the bottom of the screen
    # Place sprites back in pool
    while star_list and star_list[-1].sprite.y > thumby.display.height:
        star_queue.append(star_list.pop())
        
    # Sort the list of active missiles by out of bounds status
    missile_list.sort()
    
    # Return all out of bounds missiles to the ship's queue
    while missile_list and (missile_list[-1].out_of_bounds() or not missile_list[-1].alive):
        ship.missile_queue.append(missile_list.pop())
        
    missile_hud.update(len(ship.missile_queue))
    thumby.display.drawSprite(missile_hud.sprite)
    
    alien_list.sort()
    
    # Return all out of bounds aliens to the alien pool
    while alien_list and (alien_list[-1].out_of_bounds() or not alien_list[-1].alive):
        # Subtract from score if alien got across screen
        if ship.alive and alien_list[-1].alive:
            score -= alien_list[-1].score()
        alien_pool[0].append(alien_list.pop())
        
    # Draw score
    thumby.display.drawText(str(score), 0, int(thumby.display.height - 5), 1)
        
    # Draw frame
    thumby.display.update()
        