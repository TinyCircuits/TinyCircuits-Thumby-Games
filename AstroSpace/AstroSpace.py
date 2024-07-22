import thumby
import time
import random
thumby.display.setFPS(60)

# Constants
WIDTH, HEIGHT = 72, 40  # Thumby screen size
PLAYER_WIDTH, PLAYER_HEIGHT = 8, 8

bitmap5 = bytearray([0,0,0,0,4,34,0,0,0,0,4,0,64,1,0,0,0,0,0,0,0,0,2,64,0,0,0,0,64,0,1,0,0,0,0,64,0,1,0,0,8,0,0,0,64,4,0,0,0,0,8,0,0,0,0,16,0,0,1,0,16,0,4,0,0,0,1,0,16,0,0,0,
           0,1,0,6,0,0,128,0,0,0,2,0,0,0,0,0,0,0,0,128,0,0,0,0,0,4,0,0,0,0,0,0,0,4,0,0,16,0,0,4,0,0,0,0,0,0,0,128,0,0,0,0,0,0,0,64,0,0,4,0,0,128,0,0,8,0,0,0,0,0,32,0,
           0,0,0,8,0,0,0,0,64,0,0,0,0,0,0,2,0,0,0,32,0,0,0,0,0,0,128,0,0,0,2,0,0,128,0,32,0,0,0,4,0,0,32,0,0,0,8,0,0,0,0,64,0,0,0,0,0,32,0,0,0,0,16,0,2,0,0,8,0,0,0,0,
           128,0,0,0,1,16,0,0,0,4,0,0,0,0,1,0,32,0,0,8,0,0,1,0,0,2,0,0,136,0,0,0,64,2,0,0,32,0,8,0,0,0,2,0,0,0,0,0,0,32,0,0,0,0,16,0,0,2,0,0,64,0,0,0,4,0,64,0,0,0,0,0,
           128,0,128,2,128,0,128,8,0,0,128,1,0,0,145,0,128,128,4,128,0,144,0,0,1,128,16,128,128,0,136,0,128,0,0,64,130,128,0,128,128,0,128,145,0,0,0,0,0,8,1,0,0,0,0,128,16,0,0,2,0,32,0,0,0,0,0,32,0,0,0,0])

# Player class
class Player:
    def __init__(self):
        self.health = 3
        self.x = WIDTH // 2 - PLAYER_WIDTH // 2
        self.y = HEIGHT - PLAYER_HEIGHT
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.vel = 1.5
        self.heart = bytearray([6,9,18,9,6])
        self.image = bytearray([112,220,178,210,178,210,188,112])  # Load your bitmap

    def move(self):
        if thumby.buttonL.pressed():
            self.x -= self.vel
        if thumby.buttonR.pressed():
            self.x += self.vel
        if thumby.buttonU.pressed():
            self.y -= self.vel/4*3
        if thumby.buttonD.pressed():
            self.y += self.vel/4*3
        self.x = max(0, min(WIDTH - self.width, self.x))
        self.y = max(0, min(HEIGHT - self.height, self.y))


    def draw(self,score):
        for x in range(self.health):
            y = x//9
            thumby.display.blit(self.heart, 67-(x*6)+(54*y), 1+y*6, 5, 5, 0, 0, 0)

        thumby.display.blit(self.image, int(self.x), int(self.y), 8, 8, 0, 0, 0)

# Asteroid class
class Asteroid:
    def __init__(self):
        self.asteroids = []
        self.image = bitmap3 = bytearray([14,30,31,15,6])
        self.speed = 0.75

    def add(self):
        self.asteroids.append([random.randint(0, WIDTH-5), -5])
    
    def move(self,player,score):
        for item in self.asteroids:
            item[1] += self.speed
            if item[1] >= HEIGHT:
                self.asteroids.remove(item)
                score += 5
            if check_collision(player,item):
                self.asteroids.remove(item)
                player.health -= 1
        return score

    def draw(self):
        for x, y in self.asteroids:
            thumby.display.blit(self.image, int(x), int(y), 5, 5, 0,0,0)

class Heart:
    def __init__(self):
        self.hearts = []
        self.image = bytearray([6,9,18,9,6])
        self.speed = 0.75

    def add(self):
        self.hearts.append([random.randint(0, WIDTH-5), -5])
    
    def move(self,player):
        for item in self.hearts:
            item[1] += self.speed
            if item[1] >= HEIGHT:
                self.hearts.remove(item)
            if check_collision(player,item):
                self.hearts.remove(item)
                player.health += 1
            
            
                

    def draw(self):
        for x, y in self.hearts:
            thumby.display.blit(self.image, int(x), int(y), 5, 5, 0,0,0)

def check_collision(a, b):
    return (a.x < b[0] + 5 and
            a.x + a.width > b[0] and
            a.y < b[1] + 5 and
            a.y + a.height > b[1])
score = 0

# Main game function
def main():
    global score
    player = Player()
    asteroid = Asteroid()
    heart = Heart()
    asteroid.add()
    speed = 400
    speed1 = 10000
    
    tick = time.ticks_ms()
    tick1 = time.ticks_ms()
    tick2 = time.ticks_ms()
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        
    while True:
        if time.ticks_ms() - tick >= speed:
            asteroid.add()
            tick = time.ticks_ms()
        if time.ticks_ms() - tick1 >= 5000:
            heart.add()
            tick1 = time.ticks_ms()
        if time.ticks_ms() - tick2 >= speed1:
            speed = speed-speed/8
            speed1 = speed1-speed1/16
            tick2 = time.ticks_ms()
        
        # Handle input
        player.move()

        # Update game state
        score = asteroid.move(player,score)
        heart.move(player)

        # Draw everything
          
        thumby.display.drawSprite(thumby.Sprite(72, 40, bitmap5, 0, 0))
        thumby.display.drawText(str(score), 0, 1, 1)
        player.draw(score)
        asteroid.draw()
        heart.draw()
        
        thumby.display.update()
        if player.health <= 0:
            break


while True:
    

    while not thumby.actionPressed():
        thumby.display.drawSprite(thumby.Sprite(72, 40, bitmap5, 0, 0))
        thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
        thumby.display.drawText('Astro', 13, 3, 1)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText('Space', 20, 12, 1)
        if(time.ticks_ms() % 1000 < 500):
            thumby.display.drawFilledRectangle(0, 31, 72, 9, 0)
            thumby.display.drawText("Press A/B", 9, 32, 1)
        else:
            thumby.display.drawFilledRectangle(0, 31, 72, 9, 1)
            thumby.display.drawText("Press A/B", 9, 32, 0)
        thumby.display.update()
        
    break


if __name__ == "__main__":
    main()
    
thumby.saveData.setName('AstroSpace')
if thumby.saveData.hasItem('score'):
    highscore = thumby.saveData.getItem('score')
else:
    highscore = score
    thumby.saveData.setItem('score', score)
    thumby.saveData.save()
if score > highscore:
    highscore = score
    thumby.saveData.setItem('score', score)
    thumby.saveData.save()
    
while True:
    
    select = 1
    while not thumby.actionPressed():
        thumby.display.fill(0)
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        thumby.display.drawText(str(score), 0, 1, 1)
        thumby.display.drawText('High', 55,1,1)
        thumby.display.drawText('Score',53,7,1)
        thumby.display.drawText(str(highscore),53,13,1)


        thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)

        thumby.display.drawText(' You ', 11, 3, 1)
        thumby.display.drawText('Died', 16, 12, 1)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        if select == 1:
            thumby.display.drawText("  Again<", 7, 24, 1)
            thumby.display.drawText("   End", 7, 32, 1)
        else:
            thumby.display.drawText("  Again", 7, 24, 1)
            thumby.display.drawText("   End<", 7, 32, 1)
        if thumby.buttonU.pressed():
            select = 1
        elif thumby.buttonD.pressed():
            select = 0
        thumby.display.update()
    
    if select == 0:
        thumby.reset()
    else:
        score = 0
        main()
        
    
