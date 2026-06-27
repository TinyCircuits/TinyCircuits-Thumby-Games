import thumby
import random
import time
import math
from collections import namedtuple, deque

from sys import path
path.append("/Games/AlienInvasion")

from game_classes import (
    Star,
    Ship,
    Missile,
    BasicAlien,
    Explosion,
    MissileHUD,
    Logo,
    BossAlien,
    BossState,
    AudioMixer,
    BEEP_SOUND,
    FIRE_MISSILE_SOUND,
    TRACTOR_BEAM_SOUND,
    GAME_OVER_SOUND,
    explosion_sound,
)


MAX_STARS = 10
MAX_MISSILES = 3
MAX_ALIENS = 3
MAX_EXPLOSIONS = 4
MIN_ALIEN_TIME = 500
MIN_STAR_TIME = 1000
MIN_RESTART_TIME = 3000
BOSS_SCORE_INTERVAL = 200
ABDUCTED_FIRE_DELAY = 4

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)
thumby.saveData.setName("alieninvaders")

missile_hud = MissileHUD()
logo = Logo()
mixer = AudioMixer(MAX_EXPLOSIONS + MAX_MISSILES)

setup = True

def show_logo():
    """Show the logo until the game is started or thumby reset"""
    # clear input buffers
    thumby.buttonL.justPressed()
    thumby.buttonR.justPressed()
    thumby.buttonA.justPressed()
    thumby.buttonB.justPressed()
    
    while (1):
        t0 = time.ticks_ms()
        if logo.update(t0):
            mixer.play_sound(BEEP_SOUND)
        if thumby.actionJustPressed():
            if logo.current_option == Logo.option.exit:
                thumby.reset()
            elif logo.current_option == Logo.option.start:
                mixer.play_sound(BEEP_SOUND)
                break
            elif logo.current_option == Logo.option.audio:
                thumby.audio.setEnabled(not thumby.audio.enabled)
                mixer.play_sound(BEEP_SOUND)
            elif logo.current_option == Logo.option.clear_hs and not logo.cleared_hs:
                mixer.play_sound(BEEP_SOUND)
                thumby.saveData.setItem("high_score", 0)
                thumby.saveData.save()
                logo.cleared_hs = True
        mixer.update(t0)
            

def get_high_score():
    high_score = 0
    if thumby.saveData.hasItem("high_score"):
        high_score = int(thumby.saveData.getItem("high_score"))
    return high_score
    
def check_and_set_high_score(score, old_high_score):
    if score > old_high_score:
        thumby.saveData.setItem("high_score", score)
        thumby.saveData.save()
        logo.cleared_hs = False
    
def get_alien(num, alien_pool):
    """Get and initialize an alien from the pool"""
    
    if num < 1 or len(alien_pool) < 1:
        return None
    new_alien = alien_pool.pop()
    if num == 1:
        new_alien.initialize(
            x=random.randint(0, thumby.display.width - new_alien.sprite.width),
            y=-new_alien.sprite.height,
            s=random.randint(50, 100),
            mf=lambda x, y: (x, y+1),
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
    elif num == 4:
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
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        star_list = []
        missile_list = []
        alien_list = []
        explosion_list = []
        star_queue = deque((), MAX_STARS)
        alien_pool = []
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
        for _ in range(MAX_ALIENS):
            alien_pool.append(BasicAlien())
                
        # Create a pool of explosion sprites
        for _ in range(MAX_EXPLOSIONS):
            explosion_queue.append(Explosion())
        
        alien_timer = time.ticks_add(time.ticks_ms(), MIN_ALIEN_TIME)
        star_timer = time.ticks_add(time.ticks_ms(), MIN_STAR_TIME)
        restart_wait = 0
        
        ship = Ship(MAX_MISSILES, ABDUCTED_FIRE_DELAY)
        boss_alien = BossAlien(ship)
        
        show_logo()
        old_high_score = get_high_score()
        
        setup = False


    t0 = time.ticks_ms()
    
    if boss_alien.countdown <= 0:
        boss_alien.initialize(BOSS_SCORE_INTERVAL)
    
    if boss_alien.state < BossAlien.boss_state.abduct:
        # Check for basic alien collisions
        for alien in alien_list:
            if ship.alive and alien.collides_with(ship.sprite):
                ship.alive = False
                mixer.play_sound(explosion_sound())
                if explosion_queue:
                    explosion_list.append(explosion_queue.popleft().place(ship.sprite.x, ship.sprite.y))
            for missile in missile_list:
                if alien.collides_with(missile.sprite):
                    alien.alive, missile.alive = False, False
                    mixer.play_sound(explosion_sound())
                    if not boss_alien.state:
                        score += alien.score()
                        boss_alien.countdown -= alien.score()
                    if explosion_queue:
                        explosion_list.append(explosion_queue.popleft().place(alien.sprite.x-1, alien.sprite.y-1))
                        
    if boss_alien.state == BossAlien.boss_state.beam_down and not mixer.static_sound and not game_over:
        mixer.play_static_sound(TRACTOR_BEAM_SOUND)
        
    if mixer.static_sound and boss_alien.state in (BossAlien.boss_state.inactive, BossAlien.boss_state.move, boss_alien.boss_state.exit):
        mixer.stop_static_sound()
           
    if boss_alien.state:  # "inactive" state is 0
        # Check for collisions
        if boss_alien.collides_with(ship.sprite) and ship.alive and not boss_alien.state >= BossAlien.boss_state.abduct:
            ship.alive = False
            mixer.play_sound(explosion_sound())
            if explosion_queue:
                explosion_list.append(explosion_queue.popleft().place(ship.sprite.x, ship.sprite.y))
        for missile in missile_list:
            if boss_alien.collides_with(missile.sprite):
                missile.alive = False
                boss_alien.health -= 1
                mixer.play_sound(explosion_sound())
                if explosion_queue and boss_alien.health > 0:
                    explosion_list.append(explosion_queue.popleft().place(missile.sprite.x-2, missile.sprite.y-2))
            if boss_alien.health <= 0:
                mixer.play_sound(explosion_sound())
                if explosion_queue:
                    explosion_list.append(explosion_queue.popleft().place(boss_alien.sprite.x, boss_alien.sprite.y-2))
                boss_alien.state = BossAlien.boss_state.inactive
                boss_alien.kill_count += 1
                score += 100
                ship.abducted_fire_delay = ABDUCTED_FIRE_DELAY
                break

        # Abduct the ship!        
        if boss_alien.beam_collides_with_ship() and boss_alien.health > 0:
            boss_alien.state = BossAlien.boss_state.abduct
                
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
        alien_timer = time.ticks_add(time.ticks_ms(), MIN_ALIEN_TIME)
        if boss_alien.kill_count and len(alien_list) < MAX_ALIENS and random.randint(0, 1) == 0:
            new_alien = get_alien(random.randint(1, min(5, boss_alien.kill_count)), alien_pool)
            if new_alien:
                alien_list.append(new_alien)
    
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
        
    # Draw and move boss alien and it's abdution beam
    if boss_alien.state:
        thumby.display.drawSprite(boss_alien.sprite)
        thumby.display.drawLine(0, 0, 0, (boss_alien.health-1)*2+1, 1)
        for active_beam in filter(lambda x: x.active, boss_alien.beam_segments):
            thumby.display.drawSprite(active_beam.sprite)
        
        boss_alien.move(t0)
      
    if ship.alive:
        if not boss_alien.state >= BossAlien.boss_state.abduct:
            # Move the ship
            ship.move(
                thumby.buttonL.pressed(),
                thumby.buttonR.pressed(),
                thumby.buttonU.pressed(),
                thumby.buttonD.pressed(),
                t0,
            )
            # Fire missiles
            if thumby.buttonA.justPressed():
                if new_missile := ship.fire(Missile.fire_direction.forward):
                    mixer.play_sound(FIRE_MISSILE_SOUND)
                    missile_list.extend(new_missile)
            if thumby.buttonB.justPressed():
                if new_missiles := ship.fire(Missile.fire_direction.side):
                    mixer.play_sound(FIRE_MISSILE_SOUND)
                    missile_list.extend(new_missiles)
                
        if boss_alien.state == BossAlien.boss_state.abduct:
            # Fire one missile for every ABDUCTED_FIRE_DELAY+1 button presses
            if thumby.buttonA.justPressed():
                if ship.abducted_fire_delay:
                    ship.abducted_fire_delay -= 1
                else:
                    missile_list.extend(ship.fire(Missile.fire_direction.forward))
                    ship.abducted_fire_delay = ABDUCTED_FIRE_DELAY
            
            # Bar representing missile delay
            thumby.display.drawLine(
                thumby.display.width-1,
                thumby.display.height - missile_hud.sprite.height - 2,
                thumby.display.width-1,
                thumby.display.height - missile_hud.sprite.height - 2*ship.abducted_fire_delay - 4,
                1,
            )   
                
        thumby.display.drawSprite(ship.sprite)

    
    elif game_over or len(explosion_list) == 0:
        if not game_over:
            game_over = True
            mixer.stop_static_sound()
            mixer.play_sound(GAME_OVER_SOUND)
            check_and_set_high_score(score, old_high_score)
            restart_wait = time.ticks_add(t0, MIN_RESTART_TIME)
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
            
    # Sort the list of explosions by done status
    explosion_list.sort()
    
    # Put all finished explosions back in the queue
    while explosion_list and explosion_list[-1].done:
        explosion_queue.append(explosion_list.pop())

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
        if ship.alive and alien_list[-1].alive and not boss_alien.state:
            score = max(score - alien_list[-1].score(), 0)
        alien_pool.append(alien_list.pop())
        
    # Draw score
    thumby.display.drawText(str(score), 0, int(thumby.display.height - 5), 1)
    
    # Play
    mixer.update(t0)
        
    # Draw frame
    thumby.display.update()

