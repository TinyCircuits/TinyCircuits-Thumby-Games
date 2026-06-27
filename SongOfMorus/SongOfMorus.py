import time
import thumby
import math
import random

musicTitle =[4/12,9/12,12/12,9/12,7/12,9/12,1+2/12,9/12,
            4/12,9/12,1+2/12,9/12,7/12,9/12,1+2/12,1+4/12,
            4/12,9/12,12/12,9/12,7/12,9/12,1+4/12,9/12,
            1+4/12,1+2/12,9/12,1+2/12,1+4/12,9/12,1+9/12,9/12
            ]
# == cover
# BITMAP: width: 72, height: 40
coverTitle = bytearray([0,0,0,0,0,0,0,248,252,252,254,255,255,127,63,63,63,127,127,127,126,126,124,48,0,128,192,192,224,224,192,192,128,0,0,248,252,248,248,240,192,0,0,0,0,248,252,248,0,192,248,252,254,127,63,63,63,127,127,255,255,126,48,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,7,15,31,31,63,63,60,56,56,56,120,248,240,240,224,28,127,255,255,199,131,131,193,243,127,62,0,63,255,255,255,127,7,15,28,56,112,255,255,255,0,127,255,255,128,0,0,12,156,252,252,252,248,240,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,192,224,224,224,192,1,15,15,14,14,14,140,204,238,239,207,7,3,0,0,0,1,129,129,1,1,0,120,252,204,200,123,35,252,254,46,12,0,0,0,0,1,1,0,0,1,3,7,7,7,7,3,1,1,131,199,199,224,224,224,224,192,128,128,0,0,0,
           0,0,0,192,252,255,255,255,63,63,126,248,240,248,252,30,15,143,255,255,255,0,48,252,254,255,31,15,15,7,6,14,252,248,0,254,255,254,254,62,14,14,30,28,28,0,254,254,254,252,248,0,0,0,254,254,64,0,31,63,127,127,255,231,231,231,231,199,195,128,0,0,
           0,252,255,255,127,63,15,1,0,0,0,1,1,1,0,0,0,7,15,31,15,0,0,1,3,7,6,6,6,6,6,7,3,0,0,0,15,31,3,0,0,0,0,0,0,0,1,3,7,7,15,12,14,7,7,3,0,0,0,24,56,56,112,224,224,241,247,255,255,255,127,124])

# BITMAP: width: 80, height: 40
coverSong = bytearray([0,0,0,0,0,0,0,0,0,128,224,224,0,128,224,248,126,120,96,96,96,192,192,192,208,240,240,56,223,31,15,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,127,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,1,15,31,190,63,56,48,120,248,240,240,248,128,0,0,
           0,140,252,248,240,120,124,190,159,207,231,247,119,103,65,0,126,255,255,255,254,0,127,127,127,3,248,255,0,0,0,0,0,0,0,128,0,0,96,254,252,240,224,192,0,0,0,0,128,241,231,207,31,127,255,255,255,1,0,0,0,0,0,0,0,0,0,224,62,0,199,255,254,248,3,255,255,191,16,0,
           1,127,255,255,225,30,127,251,231,31,127,125,0,255,255,223,152,119,207,95,95,192,255,255,0,6,14,192,240,192,0,0,0,0,128,31,247,227,248,200,128,145,193,243,255,254,252,255,255,243,225,241,129,16,0,129,231,231,240,240,0,0,0,0,0,0,142,3,0,156,159,199,227,241,252,127,31,25,8,0,
           2,7,7,15,15,159,124,249,240,224,0,0,0,255,3,253,253,158,174,62,253,253,3,255,0,254,255,127,127,191,254,240,192,0,253,248,225,159,63,127,255,255,255,255,191,251,191,191,191,255,255,255,255,255,255,255,127,63,207,239,0,0,192,240,252,190,127,127,31,31,21,3,1,1,0,0,0,0,0,0,
           0,0,0,0,224,255,126,31,7,1,0,0,252,255,0,255,255,231,106,223,255,255,0,255,128,15,15,15,14,14,15,15,15,15,15,15,15,15,15,6,4,1,3,3,55,7,135,199,103,103,51,51,17,1,60,126,126,255,255,250,248,222,191,191,199,225,209,128,192,192,192,224,112,48,12,0,0,0,0,0])

# BITMAP: width: 80, height: 40
coverDemon = bytearray([192,0,0,248,255,31,135,243,199,159,62,126,63,15,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,255,252,240,0,0,0,1,3,7,31,127,255,252,224,224,224,224,240,0,0,0,0,0,0,0,0,128,192,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           1,3,14,31,127,252,241,231,223,191,127,254,252,248,248,224,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,24,127,255,127,31,0,0,0,0,0,128,192,224,243,121,193,255,255,7,225,240,240,248,220,158,95,71,203,135,135,7,15,14,12,28,252,254,255,224,112,0,0,0,0,0,0,0,0,
           0,0,0,0,1,1,1,3,7,255,255,248,129,131,7,15,15,15,0,0,0,0,0,0,0,0,192,224,224,224,240,160,192,0,0,0,224,248,128,255,254,18,199,247,251,252,255,191,255,255,254,15,183,155,7,31,223,239,246,250,56,12,5,1,193,227,240,248,255,127,63,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,12,11,127,127,252,250,250,250,242,244,229,224,203,159,124,248,248,248,255,255,255,231,255,127,126,126,190,255,255,127,15,7,56,63,127,255,241,249,255,255,255,255,0,127,255,255,252,255,31,3,0,0,136,176,188,191,191,191,191,63,126,120,120,120,240,248,252,192,192,128,128,
           128,128,248,240,192,224,224,240,254,254,253,126,191,159,223,231,241,253,126,126,62,58,22,254,252,141,1,3,3,2,6,6,15,15,15,7,1,0,0,128,128,224,224,240,120,60,13,30,30,126,126,252,252,249,250,224,192,196,132,34,65,0,0,4,5,13,9,9,17,17,3,3,2,6,126,13,193,241,231,207])

# BITMAP: width: 16, height: 16
bmpSong = [bytearray([120,252,28,236,244,240,120,120,248,248,254,126,110,206,136,240,
           96,96,112,27,255,255,116,116,119,71,119,244,252,55,96,96]),
           bytearray([120,252,28,236,244,240,120,120,248,248,254,126,110,206,136,240,
           48,48,56,11,127,255,244,116,119,71,247,244,124,15,48,48]),
           bytearray([240,136,200,110,254,254,254,248,120,248,248,240,236,28,252,120,
           96,96,119,29,254,255,119,118,117,71,119,119,123,100,6,6]),
           bytearray([0,0,0,128,128,128,128,128,128,128,128,0,0,0,0,0,
           206,224,31,115,123,251,251,27,123,115,123,123,120,102,16,48])
           ]
spriteSong = []
for i in range(4):
    spriteSong.append(thumby.Sprite(16,16,bmpSong[i]))
# BITMAP: width: 16, height: 16
bmpDemon = [bytearray([0,128,135,254,248,188,124,252,252,252,252,254,127,188,120,96,
           96,96,113,27,255,223,92,92,95,95,95,220,252,55,96,96]),
           bytearray([0,128,135,254,248,188,124,252,252,252,252,254,127,188,120,96,
           48,48,57,11,127,223,220,92,95,95,223,220,124,15,56,48]),
           bytearray([96,120,252,127,254,252,252,252,124,252,252,248,254,199,64,0,
           96,96,119,29,254,223,95,94,93,95,95,95,121,100,6,6])
           ]
spriteDemon = []
for i in range(3):
    spriteDemon.append(thumby.Sprite(16,16,bmpDemon[i],0,0,-1,1))
# == bullet
# BITMAP: width: 8, height: 8
bmpBulletA = bytearray([24,102,66,129,129,66,102,24])
spriteBulletA = thumby.Sprite(8,8,bmpBulletA, 0,0,0)
# BITMAP: width: 8, height: 8
bmpBulletA2 = bytearray([255,231,195,129,129,195,231,255])
spriteBulletA2 = thumby.Sprite(8,8,bmpBulletA2, 0,0,1)
# BITMAP: width: 8, height: 8
bmpBulletB = bytearray([231,153,189,126,126,189,153,231])
spriteBulletB = thumby.Sprite(8,8,bmpBulletB, 0,0,1)
# BITMAP: width: 8, height: 8
bmpBulletB2 = bytearray([0,24,60,126,126,60,24,0])
spriteBulletB2 = thumby.Sprite(8,8,bmpBulletB2, 0,0,0)
# BITMAP: width: 8, height: 5
bmpFulu = bytearray([10,14,10,14,10,10,14,0])
spriteFulu = thumby.Sprite(8,5,bmpFulu, 0,0,-1)
# BITMAP: width: 8, height: 8
bmpExplode = bytearray([128,160,136,144,194,248,48,62])
spriteExplode = [
        thumby.Sprite(8,8,bmpExplode, 0,0,0),
        thumby.Sprite(8,8,bmpExplode, 0,0,0,1),
        thumby.Sprite(8,8,bmpExplode, 0,0,0,0,1),
        thumby.Sprite(8,8,bmpExplode, 0,0,0,1,1)
    ]
# BITMAP: width: 3, height: 3
bmpHeart = bytearray([3,6,3])
spriteHeart = thumby.Sprite(8,5,bmpHeart,0,0,0)

# BITMAP: width: 3, height: 2
bmpDown = bytearray([1,3,1])
spriteDown = thumby.Sprite(3,2,bmpDown)
           
thumby.display.setFPS(60)

page = 0
frame = 0

@micropython.viper
def draw( sprtptr:ptr8, x:int, y:int, width:int, height:int, offset:ptr8, scroll:int, cut:int):
    xStart=int(x)
    yStart=int(y)
    ptr = ptr8(thumby.display.display.buffer)
    screenWidth = int(thumby.display.width)
    screenHeight = int(thumby.display.height)
        
    yFirst=0-yStart
    blitHeight=height
    if yFirst<0:
        yFirst=0
    if yStart+height>screenHeight:
        blitHeight = screenHeight-yStart
        
    xFirst=0-xStart
    blitWidth=width
    if xFirst<0:
        xFirst=0
    if xStart+width>screenWidth:
        blitWidth = screenWidth-xStart
        
    y=yFirst
    while y < blitHeight:
        x=xFirst
        o=0
        if cut<=2 :
            o = offset[(y+scroll)%screenHeight]-128;
            o = o >>cut
        while x < blitWidth:
            tx = x +o
            if(sprtptr[(y >> 3) * width + tx] & (1 << (y & 0x07))):
                ptr[((yStart+y) >> 3) * screenWidth + xStart+x] |= 1 << ((yStart+y) & 0x07)
            else:
                ptr[((yStart+y) >> 3) * screenWidth + xStart+x] &= 0xff ^ (1 << ((yStart+y) & 0x07))
            x+=1
        y+=1


def initGame():
    global bullets, explodes, fulus, songY, demonY, demonTY, demonTI, songHit, demonHit, score, hp
    bullets = []
    explodes = []
    fulus = []
    songY = 20
    demonY = 20
    demonTY = 20
    demonTI = 0
    songHit = 0
    demonHit = 0
    score = 0
    hp = 3

initGame()

def switchPage(num):
    global page, frame
    page = num
    if page == 0 or page ==2:
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        frame = 0
    elif page == 1:
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        frame = -120
        initGame()
switchPage(0)
wave = bytearray([int(0)] *40)
for i in range(40):
    wave[i] = int(round(3*math.sin(3.14*i/20)+128))
        
def pageCover():
    global page , frame, wave
    if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
        thumby.audio.playBlocking(int(256*math.pow(2,1+4/12)),150)
        thumby.audio.playBlocking(int(256*math.pow(2,1+7/12)),150)
        thumby.audio.playBlocking(int(256*math.pow(2,1+9/12)),150)
        switchPage(1)
        return
    
    thumby.display.fill(0) # Fill canvas to blac
    if frame < 150:
        
        thumby.display.drawText("Made by", 0,2, 1)
        thumby.display.drawText("@SunnyChow", 0, 16, 1)
        thumby.display.drawText(" TheGuy", 0, 24, 1)
    elif frame < 300:
        draw(coverSong, int((frame-150)/(150/8))-8, 0,80,40,wave,frame,int((frame-150)/20))

    elif frame < 480:
        draw(coverDemon, -int((frame-300)/(150/8)), 0,80,40,wave,frame,int((frame-300)/20))

    else :
        draw(coverTitle, 0, 0,72,40,wave,frame,int((frame-480)/20))
        if frame > 720 and frame%120<60:
            thumby.display.drawFilledRectangle(0, 22, 72, 18, 0)
            thumby.display.drawText("Press button" , 1,25, 1)
            thumby.display.drawText("to start" , 12,33, 1)
            
    
    if frame%15 == 0:
        i = math.floor(frame/15)
        if i < len(musicTitle) and musicTitle[i]!= 0:
            thumby.audio.play(int(256*math.pow(2,musicTitle[i])),150)
            
    
    frame += 1

def pageGame():
    
    global frame , page 
    global songY , demonY, demonTY
    global songHit , demonHit 
    global score, hp
    # control
    if hp<=0:
        if frame==1:
            thumby.audio.playBlocking(int(256*math.pow(2,1)),150)
            thumby.audio.playBlocking(int(256*math.pow(2,0)),150)
        if frame>120:
            switchPage(2)
            return
    elif frame<0:
        0
    else:
        if thumby.buttonU.pressed() :
            if songY>8:
                songY-=1
        if thumby.buttonD.pressed() :
            if songY<32:
                songY+=1
                
                    
        if math.fabs(demonTY-demonY)<0.5:
            demonTY = random.randrange(8,40-8)
        else:
            demonY+=math.copysign(0.3,demonTY-demonY)
        
        if frame%90 == 0 :
             fulus.append([10, songY,0])
             rnd = random.random()*min(3,1.5+score/10)
             if rnd>2:
                bullets.append([62, demonY,-.4,-0.1,0])
                bullets.append([62, demonY,-.4,0.1,0])
             elif rnd>1:
                bullets.append([62, demonY-3,-.4,0,0])
                bullets.append([62, demonY+3,-.4,0,0])
             else:
                bullets.append([62, demonY,-.4,0,0])
        
        for b in bullets:
            b[0] +=b[2]
            b[1] +=b[3]
            b[4]+=1
            
            if songHit==0 and b[0]<14 and b[0]>2 and b[1]<songY+6 and b[1]>songY-6 :
                explodes.append([ b[0],  b[1],0])
                bullets.remove(b)
                songHit=60
                thumby.audio.play(2000,50)
                hp-=1
                if hp ==0:
                    frame = 0
                
            
            if b[4]>240:
                bullets.remove(b)
                
        for b in fulus:
            b[0]+=2
            b[2]+=1
            
            if b[0]<69 and b[0]>59 and b[1]<demonY+5 and b[1]>demonY-5 :
                explodes.append([ b[0],  b[1],0])
                fulus.remove(b)
                demonHit=30
                thumby.audio.play(400,50)
                score+=1
            
            if b[2]>60:
                fulus.remove(b)
    
    frBool = frame%10<5
    thumby.display.fill(0) 
        
    if hp ==0 :
        if frame <60: 
            sp = spriteSong[2]
        else:
            sp = spriteSong[3]
    elif songHit>0:
        songHit-=1
        sp = spriteSong[2]
    elif frBool:
        sp = spriteSong[0]
    else:
        sp = spriteSong[1]
    
    sp.x = 0
    if frame<0:
       sp.x  = frame/6
    sp.y = int(songY-8)
    thumby.display.drawSprite(sp)
    if demonHit>0:
        demonHit-=1
        sp = spriteDemon[2]
    elif frBool:
        sp = spriteDemon[0]
    else:
        sp = spriteDemon[1]
    sp.x = 56
    if frame<0:
       sp.x += -frame/6
    sp.y = int(demonY-8)
    thumby.display.drawSprite(sp)
    
    for b in bullets:
        if frBool:
            sp1 = spriteBulletA
            sp2 = spriteBulletA2
        else:
            sp1 = spriteBulletB
            sp2 =spriteBulletB2
            
        sp1.x = sp2.x = int(b[0])-4
        sp1.y = sp2.y = int(b[1])-4
        thumby.display.drawSprite(sp1)
        thumby.display.drawSprite(sp2)
            
    for b in fulus:
        sp1 = spriteFulu
        sp1.x = int(b[0])-6
        sp1.y = int(b[1])-2
        thumby.display.drawSprite(sp1)
            
    for h in range(hp):
        spriteHeart.x = h*4
        thumby.display.drawSprite(spriteHeart)
    
    for e in explodes:
        spriteExplode[0].x = spriteExplode[2].x =  e[0]-7
        spriteExplode[1].x = spriteExplode[3].x =  e[0]
        spriteExplode[0].y = spriteExplode[1].y =  e[1]-7
        spriteExplode[2].y = spriteExplode[3].y =  e[1]
        for e2 in spriteExplode:
            thumby.display.drawSprite(e2)
        
        e[2]+=1
        if e[2]>6:
            explodes.remove(e)
     
    thumby.display.drawText( '%0*d' % (4, score), 56, 0, 1)
    frame += 1
    
def pageOver():
    global frame, score 
    thumby.display.fill(0) 
    thumby.display.drawText("Game Over", 10, 12, 1)
    if frame>60:
        thumby.display.drawText( '%0*d' % (4, score), 24, 20, 1)
    
    if frame>120:
        spriteDown.x = 69
        if frame%60<30:
            spriteDown.y = 37
        else:
            spriteDown.y = 36
        thumby.display.drawSprite(spriteDown)
        if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
            switchPage(0)
            return
    
        
    frame += 1
    

while(1):
    if page ==0:
        pageCover()
    elif page ==1:
        pageGame()
    elif page ==2:
        pageOver()
    else:
        thumby.display.drawText("Song", 22, 6, 1)
        thumby.display.drawText("of Morus", 14, 14, 1)
    thumby.display.update()
    
