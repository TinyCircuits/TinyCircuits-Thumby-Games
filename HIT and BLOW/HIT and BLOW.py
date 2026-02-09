import time
import thumby
import math
import random

# BITMAP: width: 38, height: 40
bm_ayane0 = bytearray([255, 63,159,175,207, 23,215, 23,215, 71,151,219, 91,189,221, 93,181,217, 89,189, 61,189,189,125,251,251,247,239,159,127,127,255,255,255,255,255,255,
255,255,255,255,248,247,232,  7, 39,208,131, 39,248,231,216,198,241,171,208,139,211, 36,211,174, 25,181, 69,169,170,212,  0,  0,  7, 31,127,255,255,
255,255,255,255,255,  7,192, 56,255,255,248,248,111,127,127,127,127,127,255,240,240,240,248, 63,192,255,  0,190,222, 97,254,193, 63,255,255,255,255,
255,255,255,255,240,207,191,  1,132,121, 11, 55,183,174,173, 77, 13,206,199,231,227,243,128,127,255,  0,190, 97, 31,252,227, 15, 30,249,231, 31,255,
255,255,255,255,127,159,227, 61,  0, 15, 63,255,255, 15,112,191,222,239,239,247,123,121,125,126, 61, 56, 31,159,207,230,246,248,248,195, 56,255,255
])
bm_mask0 = bytearray([224,240,248,252,252,252,252,252,252,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,254,252,248,240,192,192,128,  0,  0,  0,  0,
  1,  1, 15, 31,191,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,240,192,  0,
  0,  0,128,252,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,225,  1,  1,  0,
  0,  0, 31,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,224,
  0,  0,192,224,252,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,  1
])

# BITMAP: width: 72, height: 40
bm_Bingo= bytearray([234,125,106,125,106,125,234,189,234,189,234,189,234,189,234,189,234,189,239,191,240,188,255,255,224,159,120,  7, 63,127,255, 31, 15,225,192, 47,239,239,  1,252,224, 31,255,255,  0, 63,255,255,255,128,124,160,159, 63,191,191,127, 96, 17,207, 63,255,248,192, 22,182,150,218,106,106,178,208,
255,  0,  0,247,247,  0,  8,255,  4,  4,255,  3,  3,247,  7,  7,254, 15,  7,247,  6, 15,255, 15,  6,247,  7, 14,255,  0,240,  0,249,252, 14,156,  0,129,  4,255,255,255,254,253,251,248,249,251,251,247,246,241, 59,114,112,  3,  7, 14, 40,229,202,249,247,239, 12,209,197,246,  2, 99,105,220,
255,254,254,254,254,254,255,255,254,254,255,254,254,255,254,254,255,251,242,246,240,248,255,255,254,254,254, 63,135,240, 31,224,247,253,250,249,249,249,158,207,255,255,255,255,255,255,255,255,255,255,255,239,208,206,200,200,206,240,126,255,255,255,127,131,252,127,255,  0,188,193,255,126,
255,255,255, 15,243,253,253,249,131, 63,255,255,255,255,241,224,192,129,  3,129,192,224,241,127, 31,199,241,252, 63,231, 24,  3,143, 63,127,255,255,255,255,253,241,193, 97,241,243,251,251,251, 99,131,255,255,255,255,255,255,254,255,254,127,159,227,252, 63,231, 63,  1,192,243,  3,253,224,
127, 63,191,190,176,  7,127,255,255,240,199, 31, 31,231,251,253,253, 61,129,255, 63,135,241,252,255, 31,243,124, 15,224,192, 31,255,248,198, 60,249,243,199, 15, 95,159,191,190, 61,189,189, 62,191, 31, 31, 31, 15,143,143,199,227, 19,225,254,255, 15,241, 62,131,248,224,143, 63,126,241,207
])


# BITMAP: width: 17, height: 9
bm_Eye01 = bytearray([128,242,179,144,134,255,254,253,252,255,230,101, 36, 37,  6,141,250])
bm_Eye02 = bytearray([128,250,157,156,158,255,254,253,252,255,250, 61, 56, 61, 62,189,250])

# BITMAP: width: 17, height: 9
bm_Rip01 = bytearray([114,235,219,219,219,227])
bm_Rip02 = bytearray([126,239,239,239,239,255])
# Rip Animation Table: 12
tbl_Rip= [2,2,0,2,0,1,0,2,1,0,1,0,2,1,2]

# BITMAP: width: 38, height: 40
bm_BG0 = bytearray([ 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22, 29, 22,253,
120, 56,  0,248,248,248, 24,152,152,152,152, 24,152,152,152,152, 24,248,248, 24,152,152,152,152, 24,152,152,152,152, 24,248,248,248,248,  0, 56,120,255,
123,123,120,123,123,123,120,  3,123,123,123,120,123,123,123,123,120,  3,123,120,123,123,123,123,120,123,123,  3,123,120,123,123,123,123,120,123,123,  3,
239,239,239,239,239,239,239,  0,239,239,239,239,239,239,239,239,239,  0,239,239,239,239,239,239,239,239,239,  0,239,239,239,239,239,239,239,239,239,  0,
189,189,189,189,189,189,189,  0,189,189,173,165,165,165,173,189,189,  0,189,189,189,189,189,189,189,189,189,  0,189,189,173,165,165,165,173,189,189,  0
])
bm_BG1 = bytearray([246,253,246,253,240,248,240,240,224,224,224,224,128, 64,128, 96,  0,224,128,224,  0,  0, 32,128,192,224,224,224,224,240,240,248,240,252,246,253,246,253,
255,127,255,127,255,127,127,255,255,255,255,255,255,254,121,134,248,255, 62,  3,128,248,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
123,121,120,120,120,120,120,  0,121,120,121,121,123,123,120,123,123,  3,120,120,123,123,123,121,120,120,120,  1,121,121,123,121,120,121,123,123,123,  3,
239,239,239,239,239,239,239,  0,239,239,239,239,239,239,239,239,239,  0,239,239,239,239,239,239,239,239,239,  0,239,239,239,239,239,239,239,239,239,  0,
189,189,189,189,189,189,189,  0,189,189,173,165,165,165,173,189,189,  0,189,189,189,189,189,189,189,189,189,  0,189,189,173,165,165,165,173,189,189,  0 
])


# BITMAP: width: 18, height: 10
bm_Baloon0 = bytearray([  3,253,254,254,254,254,254,254,254,254,254,254,254,254,254,125,  3,255,
255,254,253,253,253,253,253,253,253,253,253,253,253,253,253,253,253,252])
# BITMAP: width: 25, height: 15
bm_Baloon1 = bytearray([  3,253,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,253,  3,255,
224,223,191,191,191,191,191,191,191,191,191,191,191,191,191,191,191,191,191,191,191,191,175,160,159])
# BITMAP: width: 36, height: 21
bm_Baloon2 = bytearray([  3,253,254,  6,  6, 62,  6,  6,254, 46, 46,254,158, 14, 14,158,158,254,254,254,222, 94, 62,254, 62,190,126,254,126,190, 14,254,252,  1,  3,255,
  0,255,255,  4,  4,151,  4, 44,255,  4,  4,255, 31, 12,204, 12, 28,255, 15, 15,252, 29,252, 15, 12,255,252,239,244,117,180,207,255,  0,  0,255,
248,247,239,236,236,236,236,238,239,236,236,239,238,236,236,236,238,239,238,236,236,238,236,236,238,239,239,239,239,237,239,239,239,236,232,231])
# BITMAP: width: 36, height: 17
bm_Baloon3 = bytearray([  1,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,  0,  1,
  0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255, 96, 64,
255,254,254,254,254,254,254,126, 62, 62,126, 62, 62,126,254,190,190, 62, 62,254,254,254, 62,190, 62,254,254,254,190, 62, 62,254,254,254,254,255])


# BITMAP: width: 17, height: 5
bm_HitBrow= bytearray([121,113, 99,113,121,255,255,127,127,127,255,255,103,107,109,107,103])


# BITMAP: width: 7, height: 11
bm_BNum0 = bytearray([  1,  0,252,252,  0,  0,  1, 28, 24,249,249, 24, 24, 28])
bm_BNum1 = bytearray([255,255,252,  0,  0,  0,255, 31, 31,159,152,152,152,159])
bm_BNum2 = bytearray([113, 48, 28,156,192,192,225, 56, 24,153,153,153,153,249])
bm_BNum3 = bytearray([249,248,220,220,  0,  0, 33, 28, 24,153,153,152, 24, 28])
bm_BNum4 = bytearray([128,128,159,159,  0,  0,  0, 63, 31,159,159, 24, 24, 56])
bm_BNum5 = bytearray([224,192,204,204, 12, 12, 28, 60, 24,153,153,152, 24, 60])
bm_BNum6 = bytearray([  1,  0,204,204,204, 12, 31,252,248,249,249,249,248,252])
bm_BNum7 = bytearray([248,248,252, 60, 12,  0,224,255,255,248,248,248,255,255])
bm_BNum8 = bytearray([ 33,  0,204,204,  0,  0, 33,124,120,121,121,120,120,124])
bm_BNum9 = bytearray([193,128,156,156,156,  0,  1,127,121,121,121,120,120,124])

# BITMAP: width: 5, height: 7
bm_SNum0 = bytearray([192,192,222,192,192])
bm_SNum1 = bytearray([255,254,192,192,255])
bm_SNum2 = bytearray([204,196,214,208,216])
bm_SNum3 = bytearray([218,218,218,192,192])
bm_SNum4 = bytearray([112,112,119, 64, 64])
bm_SNum5 = bytearray([ 88, 88, 90, 66, 70])
bm_SNum6 = bytearray([193,192,218,194,194])
bm_SNum7 = bytearray([254,254,254,192,192])
bm_SNum8 = bytearray([192,192,218,192,192])
bm_SNum9 = bytearray([208,208,214,192,224])

tbl_BigNum=[bm_BNum0,bm_BNum1,bm_BNum2,bm_BNum3,bm_BNum4,bm_BNum5,bm_BNum6,bm_BNum7,bm_BNum8,bm_BNum9]
tbl_SmallNum=[bm_SNum0,bm_SNum1,bm_SNum2,bm_SNum3,bm_SNum4,bm_SNum5,bm_SNum6,bm_SNum7,bm_SNum8,bm_SNum9]

# BITMAP: width: 38, height: 19
bm_DownFlame = bytearray([  1,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,254,  1,
  0, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63,  0,
255,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,252,255])

# BITMAP: width: 6, height: 4
bm_MyCur= bytearray([240,244,246,246,244,240])
# BITMAP: width: 7, height: 6
bm_Hart= bytearray([249,240,224,193,224,240,249])
# BITMAP: width: 8, height: 6
bm_Triangle= bytearray([207,211,220,222,220,211,207])

# Make a sprite object using bytearray (a path to binary file from 'IMPORT SPRITE' is also valid)

# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)

cnt=0

mabataki=0
RipCount=0
def_X=30
mov_X=30
Baloon_A=0
Mode=0
MyNum=[1,2,3,4]
MyNum_defY=20

Answer=[4,1,2,6]
Hit=0
Blow=0
Booking=0
Tm=0

Test=0
Record=[]
index=0
Rec_Y=0


while(1):###########################################################
    t0 = time.ticks_ms()   # Get time (ms)
    thumby.display.fill(1) # Fill canvas to white

    bobRate = 200 # Set arbitrary bob rate (higher is slower)
    bobRange = 2  # How many pixels to move the sprite up/down (-5px ~ 5px)

    # Calculate number of pixels to offset sprite for bob animation
    bobOffset = math.sin(t0 / bobRate) * bobRange

    # Center the sprite using screen and bitmap dimensions and apply bob offset
# A Button ***************************************************** A Button 
    if (thumby.buttonA.justPressed()):
        if(Mode==0):# Play Game?
            if def_X==30:
                def_X=40
                RipCount=12
                Baloon_A=1
                Mode=1
                MyNum=[1,2,3,4]
                Tm=0
                
                if (Test==0):
                    numbers=[0,1,2,3,4,5,6,7,8,9]
                    for i in range(10):
                        tmp=numbers[i]
                        R=random.randint(0,9)
                        tmp2=numbers[R]
                        numbers[R]=tmp
                        numbers[i]=tmp2
                    R=random.randint(0,5)
                    for i in range(4):
                        Answer[i]=numbers[R+i]
                    Record=[]
                
        elif(Mode==1):# Game Start
            Mode=2
            Cur=0
            Cnt02=0
            MyNum_defY=20
            MyNum_Y=40
            
        elif(Mode==2):# Hit &　Blow　Check
            if(Booking==0):
                Mode=3#  Bingo!Check
                MyNum_defY=26
                Cnt03=0
                Tm=Tm+1 # Charange Times
                if (Tm>99):
                    Tm=99
            
        elif(Mode==3)and(Cnt03>29):#  Bingo!
            if(Hit==4):
                Mode=4
                Cur_Bingo=70
                Cnt04=0
                Tm_HX=-12
                Tm_LX=-6# X Position
            else:
                Mode=2
                Cnt02=0
                MyNum_defY=20
                
        elif(Mode==4)and(Cur_Bingo==0): 
            Mode=0
            def_X=30
 

            
            

    if (mov_X<def_X):
        mov_X=mov_X+0.2
        
    if (mov_X>def_X):
        mov_X=mov_X-0.2   
# B Button ***************************************************** B Button 
    if (thumby.buttonB.justPressed()):
        if (Mode==1):
            Baloon_A=0
            def_X=30
            RipCount=8
            Mode=0
        elif(Mode==2)and(len(Record)>0):
            Mode=5 # Record Display
            index=0 #Display Record Target
            Rec_Y=0
            
        elif(Mode==3)and(Cnt03>29):
            if(Test!=2):
                Test=0
            else:
                Test=0
        elif(Mode==5):
            Mode=2 #Exit Recor Display
        else:    
            RipCount=12


    xPosition=int(mov_X)
    yPosition=int(round((thumby.display.height/2) - (32/2) + bobOffset))-2
    width=37
    height=40
    key=0
    noMirror = 0 
# L Button ***************************************************** Left Button 
    if (thumby.buttonL.justPressed()):
        if(Mode==2):
            Cur=Cur-1
            if(Cur<0):
                Cur=0
# R Button ***************************************************** Right Button 
    if (thumby.buttonR.justPressed()):
        if(Mode==2):
            Cur=Cur+1
            if(Cur>3):
                Cur=3
# **************************************************************
# D Button ***************************************************** Down Button 
    if (thumby.buttonD.justPressed()):
        if(Mode==2):
            tmp=MyNum[Cur]
            MyNum[Cur]=tmp-1
            if(MyNum[Cur]<0):
                MyNum[Cur]=9

    if (thumby.buttonD.pressed()):
        if(Mode==5):
            Rec_Y=Rec_Y-4
            if (Rec_Y-4<0):
                Rec_Y=0
                
 # U Button ***************************************************** UP Button 
    if (thumby.buttonU.justPressed()):
        if(Mode==2):
            tmp=MyNum[Cur]
            MyNum[Cur]=tmp+1
            if(MyNum[Cur]>9):
                MyNum[Cur]=0
 
    if (thumby.buttonU.pressed()):
        if(Mode==5):
            Rec_Y=Rec_Y+4
            if (Rec_Y+4>(len(Record)*16)):
                Rec_Y=(len(Record)*16)
                                              
           
                
# # Draw BackGround ************************************************************************************************************

    if(Mode!=5):# Mode5 is Record Display
        ofst=int(cnt)
        Sprite_BG0 = thumby.Sprite(38, 40, bm_BG0,ofst-76,0)
        Sprite_BG1 = thumby.Sprite(38, 40, bm_BG1,ofst-38)
        Sprite_BG2 = thumby.Sprite(38, 40, bm_BG0,ofst+0,0)
        Sprite_BG3 = thumby.Sprite(38, 40, bm_BG1,ofst+38,0)
        thumby.display.drawSprite(Sprite_BG0)
        thumby.display.drawSprite(Sprite_BG1)
        thumby.display.drawSprite(Sprite_BG2)
        thumby.display.drawSprite(Sprite_BG3)
        
    else:

        index=0
        for R_tmp in Record:
            Num_tmp1=R_tmp%10

            Ytmp=33+Rec_Y-index*14
            
            Sprite_HB = thumby.Sprite(17, 5, bm_HitBrow ,18,Ytmp)
            thumby.display.drawSprite(Sprite_HB)            
            
            Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Num_tmp1],36,Ytmp)        
            thumby.display.drawSprite(Sprite_MyN) #BloW      
            
            R_tmp=int(R_tmp/10)
            Num_tmp1=R_tmp%10
            Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Num_tmp1],24,Ytmp)       
            thumby.display.drawSprite(Sprite_MyN) #Hit
            
            R_tmp=int(R_tmp/10)
            Num_tmp1=R_tmp%10
            Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Num_tmp1],23,Ytmp-7)       
            thumby.display.drawSprite(Sprite_MyN) #Number4

            R_tmp=int(R_tmp/10)
            Num_tmp1=R_tmp%10
            Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Num_tmp1],16,Ytmp-7)       
            thumby.display.drawSprite(Sprite_MyN) #Number3

            R_tmp=int(R_tmp/10)
            Num_tmp1=R_tmp%10
            Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Num_tmp1],9,Ytmp-7)       
            thumby.display.drawSprite(Sprite_MyN) #Number2

            R_tmp=int(R_tmp/10)
            Num_tmp1=R_tmp%10
            Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Num_tmp1],2,Ytmp-7)       
            thumby.display.drawSprite(Sprite_MyN) #Number1
    
            index =index+1




# Draw girl ****************************************************
    thumby.display.blitWithMask(bm_ayane0, xPosition, yPosition, width, height, key, noMirror, noMirror, bm_mask0)

# Mabataki
    if (cnt==30)or(cnt==55)or(cnt==60):
        mabataki=6
    if mabataki>2:
        Sprite_mbt1 = thumby.Sprite(17, 8, bm_Eye02 ,xPosition+7,yPosition+12)
        thumby.display.drawSprite(Sprite_mbt1)
    if (mabataki<=2)and(mabataki>0):
        Sprite_mbt1 = thumby.Sprite(17, 8, bm_Eye01 ,xPosition+7,yPosition+12)
        thumby.display.drawSprite(Sprite_mbt1)
# Rip
    if (RipCount>0):
        RipCount=RipCount-0.25
        tmp=tbl_Rip[int(RipCount)+1]
        if (tmp==1):
            Sprite_Rip1 = thumby.Sprite(6, 6, bm_Rip01 ,xPosition+12,yPosition+20)
            thumby.display.drawSprite(Sprite_Rip1)            
        if (tmp==2):
            Sprite_Rip1 = thumby.Sprite(6, 6, bm_Rip02 ,xPosition+12,yPosition+20)
            thumby.display.drawSprite(Sprite_Rip1)            
#****************************************************************
# My number input
    if(Mode==2)or(Mode==3):
        BookFlg=[0,0,0,0]
        Booking=0
        Sprite_FRM= thumby.Sprite(38,19, bm_DownFlame ,2,MyNum_Y)
        thumby.display.drawSprite(Sprite_FRM)
        Baloon_A=0
        Sprite_Cur= thumby.Sprite(6,4, bm_MyCur ,Cur*9+4,MyNum_Y+13)
        thumby.display.drawSprite(Sprite_Cur)  
        for Num in range(4):
            for Tmp in range(4):
                if (Tmp!=Num)and(MyNum[Tmp]==MyNum[Num]): #Number Booking
                    BookFlg[Num]=1 
                    BookFlg[Tmp]=1
                    Booking=1
                    
            if ((BookFlg[Num]==0)or(Cnt02>5)):
                Sprite_MyN= thumby.Sprite(7,11, tbl_BigNum[MyNum[Num]] ,Num*9+4,MyNum_Y+2-(Cur==Num)*2)
                thumby.display.drawSprite(Sprite_MyN)  
            
        Cnt02=Cnt02+1
        if (Cnt02>30):
            Cnt02=0
            
        
        if (MyNum_Y>MyNum_defY):
            MyNum_Y=MyNum_Y-1
        if (MyNum_Y<MyNum_defY):
            MyNum_Y=MyNum_Y+1
#****************************************************************
# Check BINGO
    if(Mode==3):
        Cnt03=Cnt03+1

        if(Cnt03>0)and(Cnt03<6):
            Sprite_Bal1 = thumby.Sprite(18,10, bm_Baloon0 ,18,16)
            thumby.display.drawSprite(Sprite_Bal1) 
        elif(Cnt03>=6)and(Cnt03<9):
            Sprite_Bal1 = thumby.Sprite(25,15, bm_Baloon1 ,8,9)
            thumby.display.drawSprite(Sprite_Bal1)               
        elif(Cnt03>=9):
            Sprite_Bal1 = thumby.Sprite(36,17, bm_Baloon3 ,2,6)
            thumby.display.drawSprite(Sprite_Bal1)               

        if(Cnt03==29):            
            RipCount=8  

        if(Cnt03>=30):
            Hit=0
            Blow=0
            for Num in range(4):
                for Tmp in range(4):
                    if (MyNum[Tmp]==Answer[Num]): #Number Booking
                        if(Num==Tmp):
                            Hit=Hit+1
                        else:
                            Blow=Blow+1
            if(Hit>0):
                for i in range(0,Hit,1):
                    Sprite_HB= thumby.Sprite(7,6, bm_Hart ,4+i*8,8+(Blow==0)*3)
                    thumby.display.drawSprite(Sprite_HB)  
            if(Blow>0):
                for i in range(0,Blow,1):
                    Sprite_HB= thumby.Sprite(7,6, bm_Triangle ,4+i*8,15-(Hit==0)*4)
                    thumby.display.drawSprite(Sprite_HB)
            if(Cnt03==30):
                tmp=MyNum[0]*100000
                tmp=tmp+MyNum[1]*10000
                tmp=tmp+MyNum[2]*1000
                tmp=tmp+MyNum[3]*100
                tmp=tmp+Hit*10
                tmp=tmp+Blow
                Record.insert(0,tmp)
            Cnt03=31

                


# Baloon_A =====================================================
    if (Baloon_A>0):
        if(Baloon_A>6)and(Baloon_A<11):
            Sprite_Bal1 = thumby.Sprite(18,10, bm_Baloon0 ,18,16)
            thumby.display.drawSprite(Sprite_Bal1)    
        elif(Baloon_A>=11)and(Baloon_A<14):
            Sprite_Bal1 = thumby.Sprite(25,15, bm_Baloon1 ,10,10)
            thumby.display.drawSprite(Sprite_Bal1)   
        elif(Baloon_A>=14):
            Sprite_Bal1 = thumby.Sprite(36,21, bm_Baloon2 ,2,6)
            thumby.display.drawSprite(Sprite_Bal1)                   
        
        Baloon_A=Baloon_A+1
        if(Baloon_A>20):
            Baloon_A=20


# Bingo! ======================================================
    if (Mode==4):
        Tm_H=int(Tm/10)# 10 level
        Tm_L=Tm-Tm_H*10#  1 Level

        
        if(Cur_Bingo>0):
            Cur_Bingo=Cur_Bingo-2 #Bingo Screen X position
        Cnt04=Cnt04+1
        if(Cnt04>100):# for Charange time Display
            Tm_HX=Tm_HX+(Tm_HX<2)
            Tm_LX=Tm_LX+(Tm_LX<9)
        if(Cnt04>200):
            Cnt04=200
        Sprite_Bingo= thumby.Sprite(72,40, bm_Bingo ,Cur_Bingo,0)
        thumby.display.drawSprite(Sprite_Bingo)  
        
        Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Tm_H],Tm_HX,19)
        thumby.display.drawSprite(Sprite_MyN)        
        Sprite_MyN= thumby.Sprite(5,7, tbl_SmallNum[Tm_L],Tm_LX,19)
        thumby.display.drawSprite(Sprite_MyN)    
#===============================================================


# Test Answer Display#####
#
    if (Test==2):
        for k in range(4):
            Sprite_MyN= thumby.Sprite(7,11, tbl_BigNum[Answer[k]] ,k*9+32,0)
            thumby.display.drawSprite(Sprite_MyN) 
##########################



#Screen Update    
    thumby.display.update()
    
    if mabataki>0:
        mabataki=mabataki-1
    
    cnt=cnt+0.25
    if cnt==76:
        cnt=0
    
