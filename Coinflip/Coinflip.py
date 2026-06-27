import random
import thumby
import math
# 40x40 for 16 frames
coin = thumby.Sprite(40,40, "/Games/Coinflip/coin.bin", 10, 0, 0)
coinside = random.randrange(2)

thumby.display.setFPS(6)
thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
index = 0
rounds = 0
while(1):
    thumby.display.fill(0)
    if (index-rounds) == 16 and coinside == 0 or (index-rounds) == 24 and coinside == 1:
        thumby.display.drawText("A", 0, 0, 1)
        thumby.display.drawText("g", 0, 7, 1)
        thumby.display.drawText("a", 0, 14, 1)
        thumby.display.drawText("i", 0, 21, 1)
        thumby.display.drawText("n", 0, 28, 1)
        thumby.display.drawText("A:Y", 52, 12, 1)
        thumby.display.drawText("B:N", 52, 20, 1)
        if thumby.buttonB.justPressed():
            thumby.reset()
        if thumby.buttonA.justPressed():
            if (index-rounds) == 16:
                rounds += 16
            if (index-rounds) == 24:
                rounds += 24
            coinside = random.randrange(2)
    else:    
        index += 1
    
    coin.setFrame(index)
    thumby.display.drawSprite(coin)
    thumby.display.update()