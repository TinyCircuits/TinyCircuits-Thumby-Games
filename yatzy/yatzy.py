"""
Yatzy micropython game for Thumby
License - MIT
Code: SHDWWZRD
Art: VAMPIRICS
version:
0.3 BETA
-fixed bug where New High Score screen showed p2 scores twice if player 2 won
1.0 - 4/18/2022
-Public Release
"""

import thumby, random, gc, os

#images
cup_images = (# width, height 14, 24
(0x03, 0xa9, 0x54, 0xaa, 0xea, 0xea, 0x6a, 
0x6a, 0x6a, 0xea, 0xea, 0xf4, 0xf9, 0x03, 0x80, 0x2a, 0x55, 0xea, 0xff, 0xff, 0xf0, 
0xf7, 0xf0, 0xff, 0xff, 0xff, 0x7f, 0x00, 0xff, 0xff, 0xfe, 0xfc, 0xfd, 0xfd, 0xfd, 
0xfd, 0xfd, 0xfd, 0xfd, 0xfc, 0xfe, 0xff, 
),(# FRAME 2/4pl
0x03, 0xa9, 0x54, 0xaa, 0xea, 0xea, 0xea, 
0x6a, 0xea, 0xea, 0xea, 0xf4, 0xf9, 0x03, 0x80, 0x2a, 0x55, 0xea, 0xff, 0xff, 0xf6, 
0xf0, 0xf7, 0xff, 0xff, 0xff, 0x7f, 0x00, 0xff, 0xff, 0xfe, 0xfc, 0xfd, 0xfd, 0xfd, 
0xfd, 0xfd, 0xfd, 0xfd, 0xfc, 0xfe, 0xff, 
),(# FRAME 3/4
0x03, 0xa9, 0x54, 0xaa, 0xea, 0xea, 0x6a, 
0x6a, 0x6a, 0xea, 0xea, 0xf4, 0xf9, 0x03, 0x80, 0x2a, 0x55, 0xea, 0xff, 0xff, 0xf1, 
0xf5, 0xf4, 0xff, 0xff, 0xff, 0x7f, 0x00, 0xff, 0xff, 0xfe, 0xfc, 0xfd, 0xfd, 0xfd, 
0xfd, 0xfd, 0xfd, 0xfd, 0xfc, 0xfe, 0xff, 
),(# FRAME 4/4
0x03, 0xa9, 0x54, 0xaa, 0xea, 0xea, 0x6a, 
0x6a, 0xea, 0xea, 0xea, 0xf4, 0xf9, 0x03, 0x80, 0x2a, 0x55, 0xea, 0xff, 0xff, 0xf7, 
0xf5, 0xfa, 0xff, 0xff, 0xff, 0x7f, 0x00, 0xff, 0xff, 0xfe, 0xfc, 0xfd, 0xfd, 0xfd, 
0xfd, 0xfd, 0xfd, 0xfd, 0xfc, 0xfe, 0xff, )
)
dice_images = (# width, height 12, 12
(0x00, 0xfe, 0xfe, 0xfe, 0xfe, 0x9e, 
0x9e, 0xfe, 0xfe, 0xfe, 0xfe, 0x00, 0xf0, 0xf7, 0xf7, 0xf7, 0xf7, 0xf7, 
0xf7, 0xf7, 0xf7, 0xf7, 0xf7, 0xf0, 
),(# FRAME 2/6
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0xfe, 
0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0x00, 0xf0, 0xf7, 0xf7, 0xf7, 0xf7, 0xf7, 
0xf7, 0xf7, 0xf4, 0xf4, 0xf7, 0xf0, 
),(# FRAME 3/6
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0x9e, 
0x9e, 0xfe, 0xfe, 0xfe, 0xfe, 0x00, 0xf0, 0xf7, 0xf7, 0xf7, 0xf7, 0xf7, 
0xf7, 0xf7, 0xf4, 0xf4, 0xf7, 0xf0, 
),(# FRAME 4/6
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0xfe, 
0xfe, 0xfe, 0xf2, 0xf2, 0xfe, 0x00, 0xf0, 0xf7, 0xf4, 0xf4, 0xf7, 0xf7, 
0xf7, 0xf7, 0xf4, 0xf4, 0xf7, 0xf0, 
),(# FRAME 5/6
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0x9e, 
0x9e, 0xfe, 0xf2, 0xf2, 0xfe, 0x00, 0xf0, 0xf7, 0xf4, 0xf4, 0xf7, 0xf7, 
0xf7, 0xf7, 0xf4, 0xf4, 0xf7, 0xf0, 
),(# FRAME 6/6
0x00, 0xfe, 0x92, 0x92, 0xfe, 0xfe, 
0xfe, 0xfe, 0x92, 0x92, 0xfe, 0x00, 0x00, 0x07, 0x04, 0x04, 0x07, 0x07, 
0x07, 0x07, 0x04, 0x04, 0x07, 0x00, )
)
locked_dice_images = (# width, height 12, 12
(0x00, 0x00, 0x00, 0x00, 0x00, 0x60, 
0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
),(# FRAME 2/6
0x00, 0x00, 0x0c, 0x0c, 0x00, 0x00, 
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 
),(# FRAME 3/6
0x00, 0x00, 0x0c, 0x0c, 0x00, 0x60, 
0x60, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 
),(# FRAME 4/6
0x00, 0x00, 0x0c, 0x0c, 0x00, 0x00, 
0x00, 0x00, 0x0c, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 
0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 
),(# FRAME 5/6
0x00, 0x00, 0x0c, 0x0c, 0x00, 0x60, 
0x60, 0x00, 0x0c, 0x0c, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 
0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 
),(# FRAME 6/6
0x00, 0x00, 0x6c, 0x6c, 0x00, 0x00, 
0x00, 0x00, 0x6c, 0x6c, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 
0x00, 0x00, 0x03, 0x03, 0x00, 0x00, )
)
arrow_plus_mask = (# width, height 7, 8
(0x8f, 0xa7, 0xb3, 0xbb, 0xb3, 0xa7, 0x8f, ),
(0x00, 0x20, 0x30, 0x38, 0x30, 0x20, 0x00, ),
(0x80, 0xbe, 0x9c, 0xc9, 0xe3, 0xff, 0xff, ),
(0x00, 0x3e, 0x1c, 0x08, 0x00, 0x00, 0x00, ),
(0xf8, 0xf2, 0xe6, 0xee, 0xe6, 0xf2, 0xf8, ),
(0x00, 0x02, 0x06, 0x0e, 0x06, 0x02, 0x00, ),
(0xff, 0xff, 0xe3, 0xc9, 0x9c, 0xbe, 0x80, ),
(0x00, 0x00, 0x00, 0x08, 0x1c, 0x3e, 0x00, ),
)
ScoreSheetElements_images = (# width, height 12, 12
(0x00, 0xfe, 0xfe, 0xfe, 0xfe, 0x9e, 
0x9e, 0xfe, 0xfe, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x07, 0x07, 0x07, 0x07, 
0x07, 0x07, 0x07, 0x07, 0x07, 0x00, 
),(# FRAME 2/14
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0xfe, 
0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x07, 0x07, 0x07, 0x07, 
0x07, 0x07, 0x04, 0x04, 0x07, 0x00, 
),(# FRAME 3/14
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0x9e, 
0x9e, 0xfe, 0xfe, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x07, 0x07, 0x07, 0x07, 
0x07, 0x07, 0x04, 0x04, 0x07, 0x00, 
),(# FRAME 4/14
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0xfe, 
0xfe, 0xfe, 0xf2, 0xf2, 0xfe, 0x00, 0x00, 0x07, 0x04, 0x04, 0x07, 0x07, 
0x07, 0x07, 0x04, 0x04, 0x07, 0x00, 
),(# FRAME 5/14
0x00, 0xfe, 0xf2, 0xf2, 0xfe, 0x9e, 
0x9e, 0xfe, 0xf2, 0xf2, 0xfe, 0x00, 0x00, 0x07, 0x04, 0x04, 0x07, 0x07, 
0x07, 0x07, 0x04, 0x04, 0x07, 0x00, 
),(# FRAME 6/14
0x00, 0xfe, 0x92, 0x92, 0xfe, 0xfe, 
0xfe, 0xfe, 0x92, 0x92, 0xfe, 0x00, 0x00, 0x07, 0x04, 0x04, 0x07, 0x07, 
0x07, 0x07, 0x04, 0x04, 0x07, 0x00, 
),(# FRAME 7/14
0x00, 0xfe, 0x72, 0x52, 0x02, 0xfe, 
0x22, 0xde, 0x22, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x06, 0x06, 0x06, 0x07, 
0x06, 0x07, 0x06, 0x07, 0x07, 0x00, 
),(# FRAME 8/14
0x00, 0xfe, 0xc2, 0xce, 0x02, 0xfe, 
0x22, 0xde, 0x22, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x07, 0x07, 0x06, 0x07, 
0x06, 0x07, 0x06, 0x07, 0x07, 0x00, 
),(# FRAME 9/14
0x00, 0xfe, 0x1e, 0xce, 0xc6, 0x02, 
0xc6, 0xce, 0x1e, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x06, 0x07, 0x07, 0x06, 
0x06, 0x06, 0x06, 0x07, 0x07, 0x00, 
),(# FRAME 10/14
0x00, 0xfe, 0x7e, 0x2e, 0x0e, 0x8e, 
0x0e, 0xfe, 0xfe, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x06, 0x06, 0x07, 0x07, 
0x07, 0x07, 0x07, 0x07, 0x07, 0x00, 
),(# FRAME 11/14
0x00, 0xfe, 0x7e, 0x3e, 0x1e, 0x8a, 
0xc2, 0xe2, 0xc2, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x06, 0x06, 0x07, 0x07, 
0x07, 0x07, 0x07, 0x07, 0x07, 0x00, 
),(# FRAME 12/14
0x00, 0xfe, 0xfe, 0xf6, 0xf2, 0x9a, 
0x82, 0xe6, 0xfe, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x07, 0x07, 0x07, 0x06, 
0x06, 0x07, 0x07, 0x07, 0x07, 0x00, 
),(# FRAME 13/14
0x00, 0xfe, 0x46, 0x52, 0x12, 0xfe, 
0x22, 0xde, 0x22, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x06, 0x06, 0x07, 0x07, 
0x06, 0x07, 0x06, 0x07, 0x07, 0x00, 
),(# FRAME 14/14
0x00, 0xfe, 0x02, 0x52, 0x26, 0xfe, 
0x46, 0x52, 0x12, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x06, 0x06, 0x07, 0x07, 
0x06, 0x06, 0x07, 0x07, 0x07, 0x00, 
),(# FRAME 15/14
0x00, 0xfe, 0x02, 0x52, 0x26, 0xfe, 
0x46, 0x52, 0x12, 0xfe, 0xfe, 0x00, 0x00, 0x07, 0x06, 0x06, 0x07, 0x07, 
0x06, 0x06, 0x07, 0x07, 0x07, 0x00, )
)
MenuButtonImages = (# width, height 16, 16
(0x01, 0xfc, 0xfe, 0xfe, 0xfe, 0xfe, 0x7e, 0x3e, 
0x7e, 0xfe, 0xfe, 0xfe, 0xfe, 0xfc, 0x01, 0xff, 0xc0, 0x9f, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbe, 
0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0x9f, 0xc0, 0xff, 
),
(# FRAME 2/5
0x01, 0xfc, 0xf6, 0xe2, 0xf6, 0xfe, 0xfe, 0xfe, 
0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfc, 0x01, 0xff, 0xc0, 0x9f, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 0xbf, 
0xbf, 0xbf, 0xb7, 0xa3, 0xb7, 0x9f, 0xc0, 0xff, 
),
(# FRAME 3/5
0x01, 0xfc, 0xce, 0xce, 0x02, 0x02, 0xce, 0xce, 
0xce, 0x02, 0x02, 0xce, 0xce, 0xfc, 0x01, 0xff, 0xc0, 0x9f, 0xb9, 0xb9, 0xa0, 0xa0, 0xb9, 0xb9, 
0xb9, 0xa0, 0xa0, 0xb9, 0xb9, 0x9f, 0xc0, 0xff, 
),
(# FRAME 4/5
0x01, 0xfc, 0xf6, 0xe2, 0xc6, 0x8e, 0x1e, 0x3e, 
0x1e, 0x8e, 0xc6, 0xe2, 0xf6, 0xfc, 0x01, 0xff, 0xc0, 0x9f, 0xb7, 0xa3, 0xb1, 0xb8, 0xbc, 0xbe, 
0xbc, 0xb8, 0xb1, 0xa3, 0xb7, 0x9f, 0xc0, 0xff, 
),
(# FRAME 5/5
0x01, 0xfc, 0x02, 0xfa, 0x22, 0x22, 0x22, 0x22, 
0x3a, 0x3a, 0x3a, 0xfa, 0x06, 0xfc, 0x01, 0xff, 0xc0, 0x9f, 0xa0, 0xaf, 0xa8, 0xa8, 0xa8, 0xa8, 
0xa8, 0xa8, 0xa8, 0xaf, 0xa0, 0x9f, 0xc0, 0xff, )
)
next_player_panel_image = (# width, height 41, 21
0x00, 0xfc, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0x06, 0xde, 0xbe, 0x7e, 0x06, 0xfe, 0x06, 0xb6, 0xb6, 0xf6, 0xf6, 0xfe, 
0xe6, 0x5e, 0xbe, 0x5e, 0xe6, 0xfe, 0xf6, 0xf6, 0x06, 0xf6, 0xf6, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfe, 0xfc, 0x00, 0x00, 0xff, 0xff, 0x07, 0xb7, 0xb7, 0xb7, 0xcf, 0xff, 0x04, 0xff, 0xff, 0xff, 0xfc, 0xff, 0x04, 0xb5, 0xb5, 0xb5, 0x05, 0xff, 
0xe4, 0xdf, 0x3f, 0xdf, 0xe4, 0xff, 0x07, 0xb7, 0xb4, 0xf7, 0xf7, 0xff, 0x07, 0xb7, 0x37, 0xb7, 0xcf, 0xff, 0xff, 0x00, 0xe0, 0xe7, 0xef, 0xec, 0xef, 0xef, 0xef, 0xef, 0xef, 0xec, 0xed, 0xed, 0xed, 0xed, 0xef, 0xec, 0xef, 0xef, 0xef, 0xec, 0xef, 
0xef, 0xef, 0xec, 0xef, 0xef, 0xef, 0xec, 0xed, 0xed, 0xed, 0xed, 0xef, 0xec, 0xef, 0xef, 0xee, 0xed, 0xef, 0xe7, 0xe0,
)

#global functions
def getCamSmoothMove(distance:int):
    off = abs(distance)
    if (off >= 40):
        if(distance < 0):
            off = -20
        else:
            off = 20
    elif (off >= 4):
        off = int(distance / 2)
    elif (off > 0):
        if(distance < 0):
            off = -1
        else:
            off = 1
    else:
        off = 0
    return off
    
def drawSprite( inspr, x:int, y:int, width:int, height:int, key=-1, frame = 0, masked = False):
    sprite = []
    if(globals().get('ImageFile') is not None and type(inspr)==ImageFile):
        if(inspr.masked):
            masked = True
            sprite.append(inspr.maskedBitmap)
        sprite.append(inspr.bitmap)
    elif(type(inspr[0]) == tuple):#animated sprite data
        if(masked):#masked
            sprite.append(bytearray(inspr[2*frame]))
            sprite.append(bytearray(inspr[2*frame+1]))
        else:#not masked
            sprite.append(bytearray(inspr[frame]))
    else:#not animated can not be masked
        sprite.append(bytearray(inspr))          

    if(masked):
        thumby.display.blit(sprite[0], x, y, width, height, 1,0,0)
        thumby.display.blit(sprite[1], x, y, width, height, 0,0,0)
    else:
        thumby.display.blit(sprite[0], x, y, width, height, key,0,0)
        
#ImageFile Class
class ImageFile:
    
    def __init__(self, _w, _h, _bitmapSource, _waitFrame, _masked=False, _startFrame=0, _setLastFrame=0, _loop=True):
        global FPS
        self.bitmapSource = _bitmapSource
        self.bitmapByteCount = _w*(_h//8)
        if(_h%8):
            self.bitmapByteCount+=_w
        self.lastFrame = _setLastFrame+_startFrame
        self.loop = _loop
        self.masked =_masked
        self.startFrame = _startFrame
        self.currentFrame = _startFrame
        self.bitmap = bytearray(self.bitmapByteCount)
        self.animationComplete = False
        if(_setLastFrame==0):#then it is set by the size of the imagefile
            self.lastFrame = os.stat(self.bitmapSource)[6] // self.bitmapByteCount
        self.tick=0
        self.nframe=_waitFrame
        if(_masked):
            self.maskedBitmap = bytearray(self.bitmapByteCount)
            if(_setLastFrame==0):#then it is set by the size of the imagefile
                self.lastFrame = os.stat(self.bitmapSource)[6] // (self.bitmapByteCount*2)
        self.loadImage()
        
    def nextFrame(self):
        if self.animationComplete == False:
            self.tick+=1
            if(self.tick % self.nframe == 0):
                self.currentFrame+=1;
                if self.currentFrame >= self.lastFrame:
                    self.currentFrame = self.startFrame
                    if self.loop == False:
                        self.animationComplete = True
                self.loadImage()
                
    def startAnimation(self):
        self.animationComplete = False
            
    def setFrame(self,_frame:int):
        if(_frame >= self.startFrame and _frame < self.lastFrame and _frame != self.currentFrame):
            self.currentFrame = _frame
            self.loadImage()
        self.animationComplete = False
    
    def loadImage(self):
        if(self.masked):
            offset=self.bitmapByteCount*(2*self.currentFrame)
            f = open(self.bitmapSource,'rb')
            f.seek(offset)
            f.readinto(self.bitmap)
            offset=self.bitmapByteCount*(2*self.currentFrame+1)
            f.seek(offset)
            f.readinto(self.maskedBitmap)
            f.close()
        else:
            offset=self.bitmapByteCount*self.currentFrame
            f = open(self.bitmapSource,'rb')
            f.seek(offset)
            f.readinto(self.bitmap)
            f.close()
            
fs_images = ImageFile(72, 40, "/Games/yatzy/fs_images.bin",0);#file set frames non animated non masked


#classes
class Player:
    def __init__(self, _x:int, _y:int, _id):
        self.x = _x
        self.y = _y
        self.id = _id
        self.scores = [-1 for _ in range(0,13)]
        self.remainingPlays = 13
        self.bonus_yatzy = 0
        self.active = False
        
    def reset(self):
        for i in range(0,13):
            self.scores[i] = -1
        self.remainingPlays = 13
        self.bonus_yatzy = 0
        self.active = False
        
    def addPlayer(self):
        self.active = True
        
    def saveData(self):
        result = ""
        for _score in self.scores :
            result = result + str(_score) + " "
        result = result + str(self.remainingPlays) + " " + str(self.bonus_yatzy) + " "
        return result
        
    def loadData(self,_s0,_s1,_s2,_s3,_s4,_s5,_s6,_s7,_s8,_s9,_s10,_s11,_s12,_rp,_by):
        self.scores[0] = int(_s0)
        self.scores[1] = int(_s1)
        self.scores[2] = int(_s2)
        self.scores[3] = int(_s3)
        self.scores[4] = int(_s4)
        self.scores[5] = int(_s5)
        self.scores[6] = int(_s6)
        self.scores[7] = int(_s7)
        self.scores[8] = int(_s8)
        self.scores[9] = int(_s9)
        self.scores[10] = int(_s10)
        self.scores[11] = int(_s11)
        self.scores[12] = int(_s12)
        self.remainingPlays = int(_rp)
        self.bonus_yatzy = int(_by)
        self.active = True
        
    def currentScore(self):
        # Maps any -1 scores to 0 before totaling
        s = [0 if x < 0 else x for x in self.scores]
        # Returns sum of map. Includes 35 bonus calculation if upper section >= 63
        return (sum(s)+(self.bonus_yatzy*100) if sum(s[0:6]) < 63 else sum(s) + 35 + (self.bonus_yatzy*100))
    
    def hasBonus(self):
        s = [0 if x < 0 else x for x in self.scores]
        if sum(s[0:6]) >= 63 :
            return 35
        return 0
        
    def setScore(self, _id):
        #add 100 if a bonus yahtzy
        if self.scores[12] == 50 : #have one yatzy already
            if game.count(1) == 5 or game.count(2) == 5 or game.count(3) == 5 or game.count(4) == 5 or game.count(5) == 5 or game.count(6) == 5 :
                self.bonus_yatzy+=1;
        self.scores[_id] = game.calculateHand(_id)
        self.remainingPlays-=1

    def draw(self):#draw player score at x:y centered and the tab
        if self.active :#only active players are drawn
            offset = 0
            if game.activePlayer==self.id : # we are the active player
                offset = 1
            thumby.display.drawFilledRectangle(self.x-17,self.y-2+offset,34,10,1)
            score = self.currentScore()
            toffset = -2
            if score>10 :
                toffset-=3
            if score>100 :
                toffset-=3
            if score>1000 :
                toffset-=3
            thumby.display.drawText(str(self.currentScore()),self.x+toffset,self.y,0)
        
class Die:
    """Holds sprite of a 6-sided die"""
    def __init__(self, _id, _x, _y):
        self.x = _x
        self.y = _y
        self.id = _id
        self.target_y = 24
        self.value = random.randint(1,6)
        self.locked = False
        self.active = False # has not been rolled yet
        
    def reset(self):
        self.locked = False
        self.active = False
        
    def initRoll(self):#throw the die off the top of the screen so it will roll its way onto the screen
        if self.locked == False :
            self.y = -12-self.id*12
            self.active = True
    
    def isObjectSelectable(self):#id die is active then it is selectable
        return self.active
        
    def select(self):#die was selected
        #if cup still has more rolls then we need to toggle lock on this die
        if game.selectableObjects[0].rolls_left > 0 :
            self.toggleLock()
        #else we could show an alert that the player is out of rolls
        
    def toggleLock(self):
        if self.locked :
            self.locked = False
        else:
            self.locked = True
            
    def isRolling(self):
        if self.y < 24 :
            return True
            
    def tick(self):
        #move the die
        if self.y<self.target_y :
            self.y=self.y+getCamSmoothMove(self.target_y-self.y)
            #if die is moving then roll the face
            self.value = random.randint(1,6)
        
    def draw(self):
        #draw the die on the dicepanel
        if self.active :
            if(self.locked):
                drawSprite(locked_dice_images,self.x+game.dicePanel.x,self.y+game.dicePanel.y+2,12,12,-1,self.value-1,False)
            else :
                drawSprite(dice_images,self.x+game.dicePanel.x,self.y+game.dicePanel.y,12,12,-1,self.value-1,False)
         
class ScoreBoardElement:
    #scoreboard element are selectable elements that are viewable on the scoreboard Panel
    def __init__(self, _id):
        # id 13 is top bonus and id 14 is bonus yahtzees, they can never be selected but will be viewable
        self.id = _id
        if self.id < 6 : #
            self.x = 4+17*self.id
        elif self.id == 13 : #
            self.x = 4+17*6
        elif self.id == 14 : 
            self.x = 4+17*14
        else : 
            self.x = 4+17*(self.id+1)
        self.y = 18
        if self.id<13 :
            self.selectable = True
        else : 
            self.selectable = False
    
    def isObjectSelectable(self):#id die is active then it is selectable
        return self.selectable
        
    def select(self):#selectable scoreboard element was selected
        if game.selectableObjects[1].active : #if dice have been rolled 
            if game.players[game.activePlayer].scores[self.id] < 0: #if score does not exist on the player yet then get the total and place on scoresheet
                game.players[game.activePlayer].setScore(self.id)
                game.nextPlayer()
        
    def tick(self):#no ticks  
        return 0
        
    def draw(self):#draw the element on the scoreboard panel and the tentative score under the element - if active player has locked in a score here then draw the lock element and the locked score
        if self.id == 13 :
            drawSprite(ScoreSheetElements_images,self.x+game.scoreBoardPanel.x,self.y,12,12,-1,self.id,False)
            thumby.display.drawText(str(game.players[game.activePlayer].hasBonus()),self.x+game.scoreBoardPanel.x,self.y+13,0)
        elif self.id == 14 :
            drawSprite(ScoreSheetElements_images,self.x+game.scoreBoardPanel.x,self.y,12,12,-1,self.id,False)
            thumby.display.drawText(str(game.players[game.activePlayer].bonus_yatzy*100),self.x+game.scoreBoardPanel.x,self.y+13,0)
        elif game.players[game.activePlayer].scores[self.id] >= 0 : #score set for this location
            drawSprite(ScoreSheetElements_images,self.x+game.scoreBoardPanel.x,self.y,12,12,-1,self.id,False)
            thumby.display.drawText(str(game.players[game.activePlayer].scores[self.id]),self.x+game.scoreBoardPanel.x,self.y+13,0)
        else :
            pos_score = 0
            if game.selectableObjects[1].active :
                pos_score = game.calculateHand(self.id)
            thumby.display.drawFilledRectangle(self.x+game.scoreBoardPanel.x-2,self.y-2,16,24,0)
            drawSprite(ScoreSheetElements_images,self.x+game.scoreBoardPanel.x,self.y,12,12,-1,self.id,False)
            thumby.display.drawText(str(pos_score),self.x+game.scoreBoardPanel.x,self.y+13,1)
            
class DicePanel:
    #scoreboard panel and dice panel - panels can move onto and off the viewable window
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.target_x = _x
        self.target_y = _y
        
    def reset(self):
        self.y = 0
        self.target_y = 0
     
    def moveOffScreen(self):
        self.target_y = 40
        
    def moveOnScreen(self):
        self.target_y = 0
            
    def tick(self):#panel must alwys try to get to the target x and y coords
        if self.y<self.target_y :
            self.y=self.y+getCamSmoothMove(self.target_y-self.y)
        if self.y>self.target_y :
            self.y=self.y+getCamSmoothMove(self.target_y-self.y)
        if self.x<self.target_x :
            self.x=self.x+getCamSmoothMove(self.target_x-self.x)
        if self.x>self.target_x :
            self.x=self.x+getCamSmoothMove(self.target_x-self.x)
        
    def draw(self):#draw the panel
        fs_images.setFrame(3)#dicec panel image
        drawSprite(fs_images, self.x,self.y,72,40,-1,0,False)

class ScoreBoardPanel:
    #scoreboard panel and dice panel - panels can move onto and off the viewable window
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.target_x = _x
        self.target_y = _y
        
    def reset(self):
        self.x=0
        self.target_x=0
        
    def tick(self):#panel must alwys try to get to the target x and y coords
        if self.y<self.target_y :
            self.y=self.y+getCamSmoothMove(self.target_y-self.y)
        if self.y>self.target_y :
            self.y=self.y+getCamSmoothMove(self.target_y-self.y)
        if self.x<self.target_x :
            self.x=self.x+getCamSmoothMove(self.target_x-self.x)
        if self.x>self.target_x :
            self.x=self.x+getCamSmoothMove(self.target_x-self.x)
        #if cursor is not at 6 when scoreboard panel is on screen then we need to move the panel
        
    def draw(self):#draw the panel
        thumby.display.drawFilledRectangle(self.x,self.y,262,31,1)
        thumby.display.drawRectangle(self.x,self.y,262,31,0)
        
class Cup:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y  
        self.rolls_left = 0
        self.offset = 2
        self.direction = -1
        
    def reset(self):
        self.rolls_left = 3
        
    def isObjectSelectable(self):#id die is active then it is selectable
        return True
        
    def select(self):#cup was selected
        if self.rolls_left > 0 :#roll all dice not locked
            self.rolls_left -= 1
            for i in range(1,6):#dice
                game.selectableObjects[i].initRoll()
        #else alert player is out of rolls
        
    def tick(self):#cup does not ever move
        if(game.counter%2 == 0):
            self.offset += self.direction
            if self.offset == 2:
                self.direction = -1
            elif self.offset == 0:
                self.direction = 1
        
    def draw(self):#draw the cup on the dice panel
        if game.cursor.cursor_on == 0 and self.rolls_left > 0 and game.areDiceRolling() == False:
            drawSprite(cup_images,self.x+self.offset,self.y+game.dicePanel.y,14,18,-1,self.rolls_left,False)
        else :
            drawSprite(cup_images,self.x,self.y+game.dicePanel.y,14,18,-1,self.rolls_left,False)
        
class Cursor:
    #can only point at objects that are selectable which includes selectable object that do nothin just so the screen can look at something
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.cursor_on = 0
        self.offset = 0
        self.direction = 1
        
    def reset(self):
        self.cursor_on = 0
        
    def tick(self):
        if(game.counter%2 == 0):
            self.offset += self.direction
            if self.offset == 2:
                self.direction = -1
            elif self.offset == 0:
                self.direction = 1
                
    def nextDicePanelObject(self):#move to the next selectable object
        if(self.cursor_on>=6) : #we are currently on the scoreboard we need to switch to dicepanel
            self.cursor_on = 0
            game.dicePanel.moveOnScreen()
        else: # we are on the dice panel
            self.cursor_on += 1
            if self.cursor_on >= 6 :
                self.cursor_on = 0
        #check to see if the object is currently selectable
        while game.selectableObjects[self.cursor_on].isObjectSelectable() == False:
            self.cursor_on += 1
            if self.cursor_on >= 6 :
                self.cursor_on = 0
                
    def nextScoreBoardObject(self):#move to the next selectable object
        if(self.cursor_on<=5) : #we are currently on the dice panel we need to switch to scoreboardpanel
            game.dicePanel.moveOffScreen()
            self.cursor_on = 6
        else:
            self.cursor_on += 1
            if self.cursor_on >= 19 :
                self.cursor_on = 6
        #check to see if the object is currently selectable
        while game.selectableObjects[self.cursor_on].isObjectSelectable() == False:
            self.cursor_on += 1
            if self.cursor_on >= 19 :
                self.cursor_on = 6
        game.scoreBoardPanel.target_x = -1*(game.selectableObjects[self.cursor_on].x-4)
        if game.scoreBoardPanel.target_x < -190 : 
            game.scoreBoardPanel.target_x = -190
        
    def select(self):#select the object the cursor is on
        game.selectableObjects[self.cursor_on].select()
        
    def draw(self):#draw the cursor icon
        if self.cursor_on >= 6 : #on scoreboardpanel arrow points down to scoreboard element
            drawSprite(arrow_plus_mask,game.selectableObjects[self.cursor_on].x+game.scoreBoardPanel.x+2,game.selectableObjects[self.cursor_on].y+self.offset-8,7,7,-1,2,True)
        elif self.cursor_on == 0 : #on dicepanel arrow point right at cup
            drawSprite(arrow_plus_mask,game.selectableObjects[self.cursor_on].x+self.offset-8,game.selectableObjects[self.cursor_on].y+game.dicePanel.y+4,7,7,-1,1,True)
        else : #on dice panel arrow points down at die
            drawSprite(arrow_plus_mask,game.selectableObjects[self.cursor_on].x+2,game.selectableObjects[self.cursor_on].y+game.dicePanel.y+self.offset-8,7,7,-1,2,True)
            
class MainMenuButton:
    def __init__(self, _x, _y, _id):
        self.x = _x
        self.y = _y  
        self.id = _id
        self.target_x = _x
        self.target_y = _y
        
    def rotate(self):
        #4 buttons - 26,23 -> 6,28 -> 26,40 -> 46,28
        #5 buttons - 26,23 -> 6,28 -> 16,40 -> 36,40 -> 46,28
        if self.target_x == 26 and self.target_y == 23 :
            self.target_x = 6
            self.target_y = 28
        elif self.target_x == 6 and self.target_y == 28 :
            if game.menuButtonCount == 4 :
                self.target_x = 26
            else :
                self.target_x = 16
            self.target_y = 40
        elif self.target_x == 16 and self.target_y == 40 :
            self.target_x = 36
            self.target_y = 40
        elif self.target_x == 26 and self.target_y == 40 :
            self.target_x = 46
            self.target_y = 28
        elif self.target_x == 36 and self.target_y == 40 :
            self.target_x = 46
            self.target_y = 28
        elif self.target_x == 46 and self.target_y == 28 :
            self.target_x = 26
            self.target_y = 23
        
    def tick(self):
        if self.y<self.target_y :
            self.y=self.y+getCamSmoothMove(self.target_y-self.y)
        if self.y>self.target_y :
            self.y=self.y+getCamSmoothMove(self.target_y-self.y)
        if self.x<self.target_x :
            self.x=self.x+getCamSmoothMove(self.target_x-self.x)
        if self.x>self.target_x :
            self.x=self.x+getCamSmoothMove(self.target_x-self.x)
        
    def draw(self):#draw the cup on the dice panel
        drawSprite(MenuButtonImages,self.x,self.y,16,16,-1,self.id,False)
        
class NextPlayerPanel:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.target_x = _x
        self.target_y = _y
        self.active = False
        
    def start(self):
        self.x = -72
        self.target_x = 15
        self.active = True
        game.startCounter =  game.counter
            
    def tick(self):#panel must alwys try to get to the target x and y coords
        if self.active :
            if self.x<self.target_x :
                self.x=self.x+getCamSmoothMove(self.target_x-self.x)
            if self.x>self.target_x :
                self.x=self.x+getCamSmoothMove(self.target_x-self.x)
            if self.x == 15 :
                #count for 3 secs
                if (game.counter-game.startCounter) % (game.FPS*2) == 0 :
                    self.target_x = 72
            if self.x == 72 :
                self.active = False
                
    def draw(self):#draw the panel
        drawSprite(next_player_panel_image,self.x,self.y,41,21,-1,0,False)
    
class HighScoreTable:
    def __init__(self):
        self.highScores = [0 for _ in range(0,5)]
        self.load()
        
    def isNewHighScore(self, _score):
        # start with the lowest score and move up, if score passwed in is higher then move the current score 
        new_score_position = 0;# no new high score
        for i in range(4, -1, -1) :
            if int(_score) > int(self.highScores[i]) : # new score is higher than current score
                if(i!=4) :
                    self.highScores[i+1] = self.highScores[i]
                    self.highScores[i] = _score
                    new_score_position = i+1
        if  new_score_position > 0 :#there is a new highscore
            self.saveHighScores()
        return new_score_position
        
    def load(self):
        try:
            self.highScores = open("/Games/yatzy/scores.sav", "r").read().split()
        except OSError:
            file = open("/Games/yatzy/scores.sav", "w")
            file.write(""+str(self.highScores[0])+" "+str(self.highScores[1])+" "+str(self.highScores[2])+" "+str(self.highScores[3])+" "+str(self.highScores[4])+" ")
            file.close()
            self.highScores = open("/Games/yatzy/scores.sav", "r").read().split()
        
    def saveHighScores(self):
        file = open("/Games/yatzy/scores.sav", "w")
        file.write(""+str(self.highScores[0])+" "+str(self.highScores[1])+" "+str(self.highScores[2])+" "+str(self.highScores[3])+" "+str(self.highScores[4])+" ")
        file.close()
        
    def draw(self):#draw the high scores table
        fs_images.setFrame(2)#high score bg
        drawSprite(fs_images, 0, 0, 72, 40,-1)
        for i in range(0,5) :
            thumby.display.drawText(str((i+1)),34,1+i*8,1)
            thumby.display.drawText(str(self.highScores[i]),int(56-(len(str(self.highScores[i]))/2*6)),1+i*8,1)
        
class Game:
    def NeoRetroSplashScreen(self):
        fs_images.setFrame(0)#neo retro logo
        drawSprite(fs_images, 0, 0, 72, 40,-1)
        if(self.startCounter==0):
            self.startCounter = 1
        if(self.counter-self.startCounter>self.FPS*3 or thumby.inputJustPressed() == True):
            self.gameState=10
            self.startCounter=0
        
    def TitleScreen(self):
        fs_images.setFrame(1)#title images
        drawSprite(fs_images, 0, 0, 72, 40,-1)
        for i in range(0,self.menuButtonCount):
            self.menuButtons[i].tick()
            self.menuButtons[i].draw()
        #draw the menu here
        if (thumby.dpadJustPressed() == True):
            #rotate the menu buttons
            for i in range(0,self.menuButtonCount):
                self.menuButtons[i].rotate()
            self.menuButtonOn+= 1
            if self.menuButtonOn > (self.menuButtonCount-1) :
                self.menuButtonOn = 0
        if (thumby.actionJustPressed() == True):
            if self.menuButtonOn == 0 :
                self.resetGame();
                self.players[0].addPlayer() 
                self.activePlayers=1
                self.gameState = 50
            elif self.menuButtonOn == 1 :
                self.resetGame();
                self.players[0].addPlayer() 
                self.players[1].addPlayer() 
                self.activePlayers=2
                self.gameState = 50
            elif self.menuButtonOn == 2 :
                self.gameState = 20
            elif self.menuButtonOn == 3 :
                thumby.reset();
            elif self.menuButtonOn == 4 : #load game
                self.loadGame()
                
    def ScoresScreen(self):
        self.highScoreTable.draw()
        if (thumby.actionJustPressed() == True):
            self.gameState = 10
            self.resetMainMenu()
        
    def GameOverScreen(self):# shows which player won with the ability to cycle through each players scoresheet
        #tick all objects
        self.scoreBoardPanel.tick()
        self.cursor.tick()
        for i in range(len(self.selectableObjects)):
            self.selectableObjects[i].tick()
            
        #draw all objects
        self.scoreBoardPanel.draw()
        for i in range(6,19):#scoreboard elements
            self.selectableObjects[i].draw()
        for i in range(0,2):#scoreboard elements
            self.nonSelectableScoreBoardElements[i].draw()
        self.players[0].draw()
        self.players[1].draw()
        self.cursor.draw()
        
        if (self.counter-self.startCounter) % 15 == 0 :
            if self.drawResult :
                self.drawResult = False
            else:
                self.drawResult = True
        if self.drawResult :
            if game.activePlayers>1 : # two player game who won
                if game.winningPlayer == 1 :
                    #have winning player plaque flashing over where the cursor goes
                    thumby.display.drawFilledRectangle(2,0,32,9,0)
                    thumby.display.drawText("WON",9,1,1)
                    thumby.display.drawFilledRectangle(37,0,32,9,0)
                    thumby.display.drawText("LOST",42,1,1)
                else : 
                    #have winning player plaque flashing over where the cursor goes
                    thumby.display.drawFilledRectangle(2,0,32,9,0)
                    thumby.display.drawText("LOST",9,1,1)
                    thumby.display.drawFilledRectangle(37,0,32,9,0)
                    thumby.display.drawText("WON",42,1,1)
            else:
                thumby.display.drawFilledRectangle(2,0,68,9,0)
                thumby.display.drawText("GAME OVER",9,1,1)
            
        if (thumby.buttonU.justPressed() == True):
            self.cursor.nextScoreBoardObject()
        elif (thumby.buttonD.justPressed() == True):
            if self.isp1newhighscore > 0 or self.isp2newhighscore > 0 :#go to new high score screen
                self.gameState = 70
            else:
                self.gameState = 10
                self.resetMainMenu()
        elif (thumby.actionJustPressed() == True):
            self.activePlayer+= 1
            if self.activePlayer >= self.activePlayers :
                self.activePlayer = 0 
                
    def NewHighScoreScreen(self) :
        fs_images.setFrame(4)#title images
        drawSprite(fs_images, 0, 0, 72, 40,-1)
        #show the new high scores and their position
        if self.isp1newhighscore>0 : #player 1 had a new highscore
            thumby.display.drawText(str((self.isp1newhighscore)),24,17,0)
            thumby.display.drawText(str(self.highScoreTable.highScores[(self.isp1newhighscore-1)]),int(46-(len(str(self.highScoreTable.highScores[(self.isp1newhighscore-1)]))/2*6)),17,0)
        if self.isp2newhighscore>0 : #player 2 had a new highscore
            thumby.display.drawText(str((self.isp2newhighscore)),24,27,0)
            thumby.display.drawText(str(self.highScoreTable.highScores[(self.isp2newhighscore-1)]),int(46-(len(str(self.highScoreTable.highScores[(self.isp2newhighscore-1)]))/2*6)),27,0)
        if thumby.actionJustPressed() == True :
            self.gameState = 10
            self.resetMainMenu()
                
    def GameScreen(self):
        #tick all objects
        self.scoreBoardPanel.tick()
        self.dicePanel.tick()
        self.cursor.tick()
        self.nextPlayerPanel.tick()
        for i in range(len(self.selectableObjects)):
            self.selectableObjects[i].tick()
            
        #draw all objects
        if self.dicePanel.y>0 :
            self.scoreBoardPanel.draw()
            for i in range(6,19):#scoreboard elements
                self.selectableObjects[i].draw()
            for i in range(0,2):#scoreboard elements
                self.nonSelectableScoreBoardElements[i].draw()
            self.players[0].draw()
            self.players[1].draw()
        if self.dicePanel.y<40 :
            self.dicePanel.draw()
            for i in range(0,6):#cup and dice
                self.selectableObjects[i].draw()
        self.cursor.draw()
        self.nextPlayerPanel.draw()
        
        #look for key press events
        if self.areDiceRolling() == False :
            if (thumby.actionJustPressed() == True):
                self.cursor.select()
            if (thumby.buttonU.justPressed() == True):
                self.cursor.nextScoreBoardObject()
            if (thumby.buttonD.justPressed() == True):
                self.cursor.nextDicePanelObject()
        
        
    # at class creation time, the above functions are 'local' names
    # so can be assigned to a dictionary, but remain unbound
    state_map = {0: NeoRetroSplashScreen, 10: TitleScreen, 20:ScoresScreen, 50:GameScreen, 60:GameOverScreen, 70:NewHighScoreScreen}
            
    def __init__(self):
        self.FPS = 30
        self.gameState = 0
        self.counter=0
        self.startCounter=0
        self.drawResult = True
        thumby.display.setFPS(self.FPS)
        self.dicePanel = DicePanel(0,0)
        self.scoreBoardPanel = ScoreBoardPanel(0,9)
        self.nextPlayerPanel = NextPlayerPanel(-72,10)
        self.players = []
        for i in range(0, 2):#18,53
            self.players.append(Player(18+35*i,1,i))
        self.activePlayer = 0
        self.activePlayers = 0
        self.winningPlayer = 0
        self.cursor = Cursor(0,0)
        self.selectableObjects = []#cup, 5 dice, 13 scoreboard elements
        self.selectableObjects.append(Cup(29,2))
        for i in range(0,5):
            self.selectableObjects.append(Die(i,4+(13*i),23))
        for i in range(0,13):
            self.selectableObjects.append(ScoreBoardElement(i))
        self.nonSelectableScoreBoardElements = []
        for i in range(13,15):
            self.nonSelectableScoreBoardElements.append(ScoreBoardElement(i))
        self.menuButtons = []
        self.menuButtonCount = 4
        if self.isSavedGame() : 
            self.menuButtonCount = 5
        #26,23 - 46,28 - 26,50 - 6,28
        if self.menuButtonCount == 4 :
            self.menuButtons.append(MainMenuButton(26,23,0))
            self.menuButtons.append(MainMenuButton(46,28,1))
            self.menuButtons.append(MainMenuButton(26,40,2))
            self.menuButtons.append(MainMenuButton(6,28,3))
            self.menuButtonOn=0
        else :
            self.menuButtons.append(MainMenuButton(26,23,4))
            self.menuButtons.append(MainMenuButton(46,28,0))
            self.menuButtons.append(MainMenuButton(36,40,1))
            self.menuButtons.append(MainMenuButton(16,40,2))
            self.menuButtons.append(MainMenuButton(6,28,3))
            self.menuButtonOn=4
        self.highScoreTable = HighScoreTable()
        self.isp1newhighscore = 0
        self.isp2newhighscore = 0
        #check to see if we have a saved game
        
    def resetMainMenu(self):
        for i in range((self.menuButtonCount-1), -1, -1) :
            del self.menuButtons[i]
        self.menuButtonCount = 4
        #26,23 - 46,28 - 26,50 - 6,28
        self.menuButtons.append(MainMenuButton(26,23,0))
        self.menuButtons.append(MainMenuButton(46,28,1))
        self.menuButtons.append(MainMenuButton(26,40,2))
        self.menuButtons.append(MainMenuButton(6,28,3))
        self.menuButtonOn=0
            
    def isSavedGame(self):
        try:
            st = os.stat("/Games/yatzy/game.sav")
        except OSError:
            return False
        return True
        
    def loadGame(self):
        try:
            file = open("/Games/yatzy/game.sav", "r").read().split()
        except OSError:
            return False
        # space separated 
        self.resetGame()
        self.activePlayer = int(file[0])
        self.activePlayers = int(file[1])
        self.players[0].addPlayer() 
        self.players[0].loadData(file[2],file[3],file[4],file[5],file[6],file[7],file[8],file[9],file[10],file[11],file[12],file[13],file[14],file[15],file[16])
        if self.activePlayers > 1 :
            self.players[1].addPlayer() 
            self.players[1].loadData(file[17],file[18],file[19],file[20],file[21],file[22],file[23],file[24],file[25],file[26],file[27],file[28],file[29],file[30],file[31])
        self.gameState = 50
        self.deleteSaveGame()

    def saveGame(self):
        file = open("/Games/yatzy/game.sav", "w")
        save_data = str(self.activePlayer) + " " + str(self.activePlayers) + " "
        save_data += self.players[0].saveData()
        if self.activePlayers > 1 :
            save_data += self.players[1].saveData()
        file.write(save_data)
        file.close()
        
    def deleteSaveGame(self):
        os.remove("/Games/yatzy/game.sav")
        
    def areDiceRolling(self):
        for i in range(1,6):#dice
            rolling = self.selectableObjects[i].isRolling()
            if rolling :
                return True
        return False
        
    
    def resetGame(self):
        self.cursor.reset();
        self.dicePanel.reset()
        for i in range(0,6):#cup dice
            self.selectableObjects[i].reset()
        self.players[0].reset() 
        self.players[1].reset() 
        self.isp1newhighscore = False
        self.isp2newhighscore = False
        self.winningPlayer = 0
        self.counter=0
        
    def update(self):
        self.counter+=1
        if self.gameState in self.state_map:
            self.state_map[self.gameState](self)
            
    def nextPlayer(self):#move to the next player
        self.activePlayer+= 1
        if self.activePlayer >= self.activePlayers :
           self.activePlayer = 0 
        if self.activePlayers > 1 :
            self.nextPlayerPanel.start()
        #if activePlayer has no more turns left then the game is over
        if self.players[self.activePlayer].remainingPlays == 0 : #game over
            self.deleteSaveGame()
            self.gameState = 60;
            self.startCounter=0
            self.winningPlayer = 1
            #determine winning player
            if self.activePlayers>1 : # two player game who won
                if self.players[0].currentScore() > self.players[1].currentScore() :
                    self.winningPlayer = 1
                    self.isp1newhighscore = self.highScoreTable.isNewHighScore(self.players[0].currentScore())
                    self.isp2newhighscore = self.highScoreTable.isNewHighScore(self.players[1].currentScore())
                else:
                    self.winningPlayer = 2
                    self.isp2newhighscore = self.highScoreTable.isNewHighScore(self.players[1].currentScore())
                    self.isp1newhighscore = self.highScoreTable.isNewHighScore(self.players[0].currentScore())
            else:
                self.isp1newhighscore = self.highScoreTable.isNewHighScore(self.players[0].currentScore())
        else : 
            self.cursor.reset() #move the cursor back to the cup
            self.scoreBoardPanel.reset()
            self.dicePanel.moveOnScreen()
            self.selectableObjects[0].reset() #reset cup rolls to 3
            for i in range(1,6):
                self.selectableObjects[i].reset()
            self.saveGame()
            
    def count(self, _number) :
        val = 0;
        for i in range(1,6):
            if self.selectableObjects[i].value == _number :
                val+= 1
        return val

    def isa(self, _number) :
        for i in range(1,6):
            if self.selectableObjects[i].value == _number :
                return True
        return False;

    def sumHand(self) :
        val = 0;
        for i in range(1,6):
            val += self.selectableObjects[i].value;
        return val

    def calculateHand(self, selection) :
        score = 0;
        if selection == 0 : #ones
            for i in range(1,6):
                if (self.selectableObjects[i].value == 1) :
                    score += 1
        elif selection == 1 : #twos
            for i in range(1,6):
                if (self.selectableObjects[i].value == 2) :
                    score += 2
        elif selection == 2 : #threes
            for i in range(1,6):
                if (self.selectableObjects[i].value == 3) :
                    score += 3
        elif selection == 3 : #fours
            for i in range(1,6):
                if (self.selectableObjects[i].value == 4) :
                    score += 4
        elif selection == 4 : #fives
            for i in range(1,6):
                if (self.selectableObjects[i].value == 5) :
                    score += 5
        elif selection == 5 : #sixes
            for i in range(1,6):
                if (self.selectableObjects[i].value == 6) :
                    score += 6
        elif selection == 6 : #three of a kind
            if self.count(1) >= 3 or self.count(2) >= 3 or self.count(3) >= 3 or self. count(4) >= 3 or self.count(5) >= 3 or self.count(6) >= 3 :
                score += self.sumHand()
        elif selection == 7 : #four of a kind
            if self.count(1) >= 4 or self.count(2) >= 4 or self.count(3) >= 4 or self. count(4) >= 4 or self.count(5) >= 4 or self.count(6) >= 4 :
                score += self.sumHand()
        elif selection == 8 : #full house
            for i in range(1,7):
                if (self.count(i) == 3) :
                    for t in range(1,7):
                        if (self.count(t) == 2 and t != i) :
                            score += 25
        elif selection == 9 : #small straight
            if (self.isa(3) == True and self.isa(4) == True and self.isa(5) == True and self.isa(6) == True) :
                score += 30;
            elif (self.isa(1) == True and self.isa(2) == True and self.isa(3) == True and self.isa(4) == True) :
                score += 30;
            elif (self.isa(2) == True and self.isa(3) == True and self.isa(4) == True and self.isa(5) == True) :
                score += 30;
        elif selection == 10 : #large straight
            if (self.isa(2) == True and self.isa(3) == True and self.isa(4) == True and self.isa(5) == True and self.isa(6) == True) :
                score += 40
            elif (self.isa(1) == True and self.isa(2) == True and self.isa(3) == True and self.isa(4) == True and self.isa(5) == True) :
                score += 40
        elif selection == 11 : #chance
            score += self.sumHand()
        elif selection == 12 : #five of a kind
            if self.count(1) >= 5 or self.count(2) >= 5 or self.count(3) >= 5 or self.count(4) >= 5 or self.count(5) >= 5 or self.count(6) >= 5 :
                score += 50
        return score;

     
game = Game()
# Main game loop
while(True):
    thumby.display.fill(0)
    game.update()
    if(game.counter%game.FPS==0):
        gc.collect()
        print(gc.mem_free())
    thumby.display.update()