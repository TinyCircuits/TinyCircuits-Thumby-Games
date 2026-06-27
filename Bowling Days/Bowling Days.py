
import thumbyButton as Btn
import thumbyGraphics as Grf
import thumbySprite as Spr 
import random
import thumbySaves as SAVE 

# BITMAP: W 42, H 24
bm_TITLE= bytearray([  1,254,242,  2,  2,  2,146, 18,  6, 76,249, 35,167, 55, 87,151, 23,247, 55,247, 16, 30,242,  2,  2,254,144,147,255, 79, 95, 95, 95,223,191,223, 95, 95, 95, 95,223, 31,
224,239,233,136,120,200,  9,  9,  8,204,143, 24, 57,248,252,127,120,121,120,249, 56, 56,255, 56, 56,255, 56, 56,191,184,184,206, 72, 72, 79, 76, 72, 75, 64, 96, 63,128,
255,255,255,193,190,163,160,160,160,167,167,160,176,159,208,208,211,208, 16,115, 94, 72, 73, 64, 96, 63,146,210,210,208,209,223,192,255,255,255,255,255,255,255,255,255])
bm_TITLEm= bytearray([254,255,255,255,255,255,255,255,255,255,254,252,248,248,248,248,248,248,248,248,255,255,255,255,255,255,255,252,240,240,224,224,224,224,192,224,224,224,224,224,224,224,
 31, 31, 31,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,
  0,  0,  0, 62,127,127,127,127,127,127,127,127,127,127, 63, 63, 63, 63,255,255,255,255,255,255,255,255,127, 63, 63, 63, 63, 63, 63,  0,  0,  0,  0,  0,  0,  0,  0,  0])

# BITMAP: W 4, H 8
bm_CHECK= bytearray([170, 85,170,213])


# BITMAP: W 11, H 13
bm_Bord_S= bytearray([255,  0, 95, 64, 67, 71, 79, 95, 63, 63, 63,255,224,239,224,224,224,224,224,224,224,224])
# BITMAP: W 39, H 6
bm_PinUp_Floor= bytearray([112,124,127,127,127,127,127,127,127, 79,115,124,127,127,127,127,127,127,127, 71,120,127,127,127,127,127,127,127,127, 71,120,127,127,127,127,127,127,127,127])

# BITMAP: W 11, H 28
bm_Pin00= bytearray([255,255,  3, 60,254,254,254, 60,  3,255,255, 63,135,240,230,205,205,205,230,240,135, 63,
  0,255,255,255,255,255,255,255,255,255,  0,252,249,243,119,119,119,119,119,115,121,124])
bm_Pin_m00= bytearray([  0,  0,252,255,255,255,255,255,252,  0,  0,192,248,255,255,255,255,255,255,255,248,192,
255,255,255,255,255,255,255,255,255,255,255,  3,  7, 15,143,143,143,143,143,143,135,131])
# BITMAP: W 11, H 25
bm_Pin01= bytearray([255,255,  1, 60,158,158,158, 60,  1,255,255, 31,195,240,251,249,249,249,251,240,195, 31,
128, 63,127,223,175,175,175,223,127, 63,128,255,255, 30,230,246,246,246,230, 30,255,255])
bm_Pin_m01= bytearray([  0,  0,254,255,255,255,255,255,254,  0,  0,224,252,255,255,255,255,255,255,255,252,224,
127,255,255,255,255,255,255,255,255,255,127,  0,  0,225,249,249,249,249,249,225,  0,  0])
# BITMAP: W 11, H 19
bm_Pin02= bytearray([255, 63,  1,140,166,166,166,140,  1, 63,255,
  1,252,255, 31,239,239,239, 31,255,252,  3,254,252, 25,203,234,234,234,203, 25,252,254])
bm_Pin_m02= bytearray([  0,192,254,255,255,255,255,255,254,192,  0,
254,255,255,255,255,255,255,255,255,255,252,  1,  3,231,247,247,247,247,247,231,  3,  1])
# BITMAP: W 14, H 28..........
bm_Pin03= bytearray([255,255,255,255,255,255,127,  3,188,190,190,126, 60,131,255,127,159,239,247,241,244,246,230,230,205,  0,254,255,
  1,254,255,255,255,255,255,255,255,255, 63,128,255,255,252,249,250,242,246,245,245,247,243,248,254,255,255,255])
bm_Pin_m03= bytearray([  0,  0,  0,  0,  0,  0,128,252,255,255,255,255,255,124,  0,128,224,240,248,254,255,255,255,255,255,255,  1,  0,
254,255,255,255,255,255,255,255,255,255,255,127,  0,  0,  3,  7,  7, 15, 15, 15, 15, 15, 15,  7,  1,  0,  0,  0])
# BITMAP: W 15, H 22
bm_Pin04= bytearray([255,255,255,255,255,127, 63, 31, 67,109, 94,222, 62, 29,195,
 31,231,251,253,254,255,255,255,255,255,254,252,  0,255,255,248,247,237,222,222,222,217,223,207,231,251,252,255,255,255])
bm_Pin_m04= bytearray([  0,  0,  0,  0,  0,128,192,224,252,254,255,255,255,254, 60,
224,248,252,254,255,255,255,255,255,255,255,255,255,  0,  0,  7, 15, 31, 63, 63, 63, 63, 63, 63, 31,  7,  3,  0,  0,  0])
# BITMAP: W 13, H 16
bm_Pin05= bytearray([127,191,223,239,239,231,227,229,214,166, 14, 29,227,224,223,163,125, 93, 93, 99,127,191,223,231,248,255])
bm_Pin_m05= bytearray([128,192,224,240,240,248,252,254,255,255,255,254, 28, 31, 63,127,255,255,255,255,255,127, 63, 31,  7,  0])
# BITMAP: W 28, H 15
bm_Pin06= bytearray([ 31,207,111,231,247,243,251,251,251,251,251,251,251,251,243,195, 11,251,115,  9, 57,132,190,190,190,190,221,193,
248,227,206,209,191,191,191,191,191,223,223,239,239,247,247,251,252,254,254,255,255,255,255,255,255,255,255,255])
bm_Pin_m06= bytearray([224,240,240,248,248,252,252,252,252,252,252,252,252,252,252,252,252,252,252,254,254,127,127,127,127,127, 62, 62,
  7, 31, 63, 63,127,127,127,127, 95, 63, 63, 31, 31, 15, 15,  7,  3,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0])
# BITMAP: W 22, H 15
bm_Pin07= bytearray([ 63,159,223,239,247,247,251,251,251,251,251,251,243,227,  9,121, 36,158,190,190,221,227,
240,239,223,190,174,177,191,191,191,223,223,239,247,251,252,254,255,255,255,255,255,255])
bm_Pin_m07= bytearray([192,224,224,240,248,248,252,252,252,252,252,252,252,252,254,254,255,127,127,127, 62, 28,
 15, 31, 63,127,127,127,127,127,127, 63, 63, 31, 15,  7,  3,  1,  0,  0,  0,  0,  0,  0])
# BITMAP: W 16, H 13
bm_Pin08= bytearray([ 31,239,119,187,187,189,125,253,249,241,233, 18,  6,190,221,227,252,251,246,235,235,235,236,239,239,247,251,252,255,255,255,255])
bm_Pin_m08= bytearray([224,240,248,252,252,254,254,254,254,254,254,255,255,127, 62, 28,  3,  7, 15, 31, 31, 31, 31, 31, 31, 15,  7,  3,  0,  0,  0,  0])

Pin_W=(11,11,11,14,15,13,28,22,16,28)
Pin_H=(28,25,19,28,22,16,15,15,13,11)

PinPtnNo=(bm_Pin00,bm_Pin01,bm_Pin02,bm_Pin03,bm_Pin04,bm_Pin05,bm_Pin06,bm_Pin07,bm_Pin08)
PinPtnmNo=(bm_Pin_m00,bm_Pin_m01,bm_Pin_m02,bm_Pin_m03,bm_Pin_m04,bm_Pin_m05,bm_Pin_m06,bm_Pin_m07,bm_Pin_m08)
PinAnim=[4,4,4,4,4,4,4,4,4,4]

PinAnim01=(0, 3,3,3,6,6,8,8)# firstNo= Mirror flg
PinAnim02=(1, 6,6,7,7,8,5,5)
PinAnim03=(1, 3,3,4,4,5,8,8)
PinAnim04=(1, 1,1,2,2,5,8,8)
PinAnim05=(0, 1,1,2,2,5,8,8)
PinAnim06=(0, 3,3,4,4,5,8,8)
PinAnim07=(0, 6,6,7,7,8,5,5)
PinAnim08=(1, 3,3,3,6,6,8,8)
PinAnimNo=(PinAnim01,PinAnim02,PinAnim03,PinAnim04,PinAnim05,PinAnim06,PinAnim07,PinAnim08)


# BITMAP: W 9, H 9
bm_TestBall= bytearray([131,125,190,126,190, 94,170, 85,131,255,255,254,254,254,254,254,255,255])
bm_TestBall_m= bytearray([124,254,255,255,255,255,255,254,124,  0,  0,  1,  1,  1,  1,  1,  0,  0])
# BITMAP: W 7, H 7
bm_TestPin= bytearray([193,156,182,170,182,156,193])
bm_TestPin_m= bytearray([ 62,127,127,127,127,127, 62])


def PinAnimSelect(DIRX):
    tmp=0
    if(DIRX<=-16):
        tmp=7
    elif(DIRX<=-12):
        tmp=6
    elif(DIRX<=-5):
        TMP=5
    elif(DIRX<=0):
        tmp=4
    elif(DIRX<=5):
        tmp=3
    elif(DIRX<=12):
        tmp=2
    elif(DIRX<=20):
        tmp=1
    return tmp

    
def ScoreCard(FrNo,ScoreDATA,TYPE):

    score=0
    SC=[]
    SCLEN=len(SCORE)-1
    if (SCLEN>=2):
        for i in range(0,int(SCLEN/2)):#----------- i is FRAME0~9
            
            if(i<9):
                flg2=-1
                if(SCLEN>=(i*2))+2:#-----Throw2 finish
                    flg2=0# [0]=Frame score is Fixed 
                    Get1=SCORE[i*2+1]
                    Get2=SCORE[i*2+2]
                    if(Get1==10):#------------------STRIKE
                        flg2=2
                        Add1=3  
                        Add2=4
                        if(i==8):#------FRAME9
                            Add1=3
                            Add2=4

                        if(SCLEN>=(i*2+Add2)):
                            
                            Get2=SCORE[i*2+Add1]
                            if(Get2!=10):#----------- Not Dobble
                                flg2=0
                                score=score+10+Get2+SCORE[i*2+Add2]
                                          
                            else:#------------------- Dobble
                                flg2=2
                                Add2=5
                                if(i==8):
                                    Add2=4#--------FRAME9 Strike FRAME10-1 STRIKE
                                if(SCLEN>=(i*2+Add2)):
                                    flg2=0
                                    Get3=SCORE[i*2+Add2]
                                    score=score+20+Get3
      
                    elif(Get1+Get2==10):#--SPARE
                        flg2=1
                        if(SCLEN>=(i*2+3)):
                            Get3=SCORE[i*2+3]
                            score=score+10+Get3
                            flg2=0
                        
                    else:
                        score=score+Get1+Get2
                        flg2=0

                if(flg2==0):
                    SC.append(score)

            else:#----------------------FRAME10
                
                flg2=0
                if(SCLEN>=20):#-------Throw2 finish
                    Get1=SCORE[19]
                    Get2=SCORE[20]

                    if(Get1 ==10 ):#-----Throw1 Strike
                        flg2=2
                        if(SCLEN>=(21)):
                            Get3=SCORE[21]    
                            flg2=0
                            score=score+10+Get2+Get3

                    elif(Get1+Get2==10):#---Spare
                        flg2=1
                        if(SCLEN>=(21)):
                            Get3=SCORE[21]    
                            flg2=0
                            score=score+10+Get3
                    else:
                        flg2=0
                        score=score+Get1+Get2
                else:
                    flg2=1
            
                if(flg2==0):
                    SC.append(score)           
            
            


    Grf.display.setFPS(30) # standardize display speed   
    flg=0
    CNT=0
    EYE_CNT=0
    if(FrNo>3):
        CNT=(FrNo-3)*21
        if(CNT>150):
            CNT=150
    if (TYPE==2):
        CNT=-10
    ofset=0
    
    while(flg==0):
        
        Grf.display.fill(1) # Fill canvas 
        if(Btn.buttonL.pressed()):
            CNT=CNT-2
            TYPE=1
            if(CNT<-10):
                CNT=-10
        if (Btn.buttonR.pressed()):
            CNT=CNT+2
            if(CNT>150):
                CNT=150

        if(Btn.buttonB.justPressed()):
            flg=1
        
        ofset=-CNT
        
        Grf.display.drawFilledRectangle(ofset, 6, 212,26, 0)
        for i in range(0,10):
            Grf.display.drawFilledRectangle(ofset+i*20+1,16, 9,7, 1)    
            Grf.display.drawFilledRectangle(ofset+i*20+11,16, 9,7, 1)    
            Grf.display.drawFilledRectangle(ofset+i*20+1,24, 19,7, 1) 
            Grf.display.drawLine(ofset+i*20,6,ofset+i*20,9, 1) 
        
            tmp2=bm_Bnum0
            tmp3=0

            if(i==9):
                tmp2=bm_Bnum1
                tmp3=3
            Sprite_Back = Spr.Sprite(5,6,tmp2,ofset+i*20+6+tmp3 ,8)#
            Grf.display.drawSprite(Sprite_Back)
            
            tmp2=Bnum_TBL[(i+1)%10]
            Sprite_Back = Spr.Sprite(5,6,tmp2,ofset+i*20+12+tmp3 ,8)#
            Grf.display.drawSprite(Sprite_Back)               
        
        Grf.display.drawFilledRectangle(ofset+201,16, 9,7, 1)  # FRAME 10  
        Grf.display.drawFilledRectangle(ofset+200,24, 10,7, 1)  
        
        j=len(SCORE)
        if (j>=2):
            Get1=0
            for i in range(1,j):
                tmp=SCORE[i]
                tmp3=5
                tmp4=6

                if(i%2==1):
                    if (tmp<=9):
                        tmpX=0
                        tmpY=1
                        tmp2=Num_TBL[tmp]
                    else:
                        tmp2=bm_STRIK
                        tmpX=8
                        tmpY=0
                        if(i==19)or(i==21): # FRAME10-1or3
                            tmpX=-2
                        tmp3=9
                        tmp4=7
                else:
                    if(SCORE[i-1]<10)and(i<20):
                        if(tmp+SCORE[i-1]<=9):
                            tmpX=10
                            tmpY=1
                            tmp2=Num_TBL[tmp] 
                        else:
                            tmp2=bm_SPEAR
                            tmpX=8
                            tmpY=0                 
                            tmp3=9
                            tmp4=7
                            
                if(i==20)or(i==21):
                    if(tmp==10):
                        tmp2=bm_STRIK
                        tmpX=-2
                        if(i==20):
                            tmpX=8
                        tmpY=0
                        tmp3=9
                        tmp4=7
                    elif((tmp+SCORE[i-1])==10):
                        tmp2=bm_SPEAR
                        tmpX=-2
                        if(i==20):
                            tmpX=8
                        tmpY=0                 
                        tmp3=9
                        tmp4=7    
                        if(i==21)and(SCORE[19]!=10):
                            tmp2=Num_TBL[tmp]
                            tmpX=0
                            tmpY=1
                            tmp3=5
                            tmp4=6                           
                        
                    else:
                        tmpX=0
                        if(i==20):
                            tmpX=10                        
                        tmpY=1
                        tmp2=Num_TBL[tmp]               
                        
                Sprite_Back = Spr.Sprite(tmp3,tmp4,tmp2,ofset+int((i+1)/2)*20-17+tmpX ,16+tmpY)#
                Grf.display.drawSprite(Sprite_Back)                       
                        
                    
        if(len(SC)>0):
            BestScore=[]
            HiScore=0
            if (SAVE.saveData.hasItem("BestScore")):
                BestScore= SAVE.saveData.getItem("BestScore")
                HiScore= int(SAVE.saveData.getItem("HiScore"))
 
            if(TYPE==2)and(SC[9]>HiScore):
                TYPE=3
                HiScore=SC[9]
                BestScore=SCORE
                
                SAVE.saveData.setItem("BestScore", BestScore)
                SAVE.saveData.save()
                SAVE.saveData.setItem("HiScore", HiScore)
                SAVE.saveData.save()

                    
            for i in range(0,len(SC)):
                tmp3=SC[i]
                for j in range(0,3):
                    tmp2=tmp3%10
                    if (tmp2!=0)or(tmp3>9):
                        Sprite_Back = Spr.Sprite(5,5,Num_TBL[tmp2],ofset+i*20+14-6*j+(i==9)*3,25)#
                        Grf.display.drawSprite(Sprite_Back)                       
                    tmp3=int(tmp3/10)
            
            if(TYPE==3)and(EYE_CNT%20<10):
                Sprite_Back = Spr.Sprite(20,8, bm_TXT_NEW , 00, 32)
                Grf.display.drawSprite(Sprite_Back)  
                Sprite_Back = Spr.Sprite(25,8, bm_TXT_BEST ,20, 32)
                Grf.display.drawSprite(Sprite_Back)  
                Sprite_Back = Spr.Sprite(27,8, bm_TXT_GAME ,45, 32)
                Grf.display.drawSprite(Sprite_Back)  
        
        
        CNT=CNT+(TYPE==2)+(TYPE==3)
        if(CNT>150):
            CNT=150
            TYPE=1
        EYE_CNT=EYE_CNT+1
        if (EYE_CNT>1000):
            EYE_CNT=0
        Grf.display.update()#-----------------------------------------------------------



# BITMAP: W 7, H 9
bm_Arrow00= bytearray([255, 63, 15,  3, 15, 63,255,255,255,255,255,255,255,255])
bm_Arrow_m00= bytearray([224,248,254,254,254,248,224,  1,  1,  1,  1,  1,  1,  1])

# BITMAP: W 19, H 6
bm_TXT_POW= bytearray([193,193,237,225,243,255,193,193,221,193,193,255,193,193,231,243,231,193,193])

# BITMAP: W 21, H 4
bm_SPIN_Meter= bytearray([113,119,115, 55,243,247,243,247,243,119, 48,183,179,183,179, 55,179,247,243,247,241])
# BITMAP: W 20, H 6
bm_TXT_SPIN= bytearray([217,209,193,197,205,255,193,193,237,225,243,255,193,193,255,193,195,247,225,193])
# BITMAP: W 7, H 4
bm_Arrow01= bytearray([255, 61,121,241,249,253,255])
bm_Arrow_m01= bytearray([  3,199,207,207, 15,  7,  3])

# BITMAP: W 36, H 38
bm_Ayane_00= bytearray([255, 63,159,175,199, 23,215, 23,215, 71,151,219, 91,187,221, 85,185,217, 89,189, 61,189,189,123,251,247,247,239,159,127,127,255,255,255,255,255,
255,255,255,255,248,247,232,  3, 43,144,131, 39,248,231,216,198,241, 39,144,135, 19, 40,211,174, 25,181, 69,169,170,212,  0,  0,  7, 31,255,255,
255,255,255,255,255,  7,192, 56,255,255,249,248,239,127,127,127,127,255,241,240,240,255,248, 63,192,255,  0,190,222, 97,254,192, 31,255,255,255,
255,255,255,199, 56,255,127,  1,248, 97, 91, 55,167,175,143, 15, 15,207,199,231,227,243,128,127,255,  0,190, 97, 31,252,227, 15, 30,248,  7,255,
255,255,255,255,254,249,254,255,192,255,255,255,255,255,192,255,254,223,239,247,251,249,253,254,253,240,255,255,255,222,230,248,252,227,220,255])
bm_Ayane_m00= bytearray([224,240,248,252,252,252,252,252,252,252,254,254,254,255,255,255,255,255,255,255,255,255,255,255,254,254,252,252,248,240,192,192,128,  0,  0,  0,
  1,  1,  1, 15, 31,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,240,  0,
  0,  0,  0,128,252,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,241,129,  0,
  0,  0,124,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,
  0,  0,  0,  3,  7,  7,  1,  0, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63, 63])
# BITMAP: W 21, H 19
bm_Ayane_01= bytearray([255,255,255,255, 15,163,107, 29, 29, 61,221, 93,171,163,  7,207,255,255,255,255,255,
255,255,  7,112, 30,232, 56,206,  8,248, 25,231, 62,222, 64,183,119,239, 95, 63,255,
255,249,254,248,254,253,252,253,253,254,254,254,249,254,255,255,254,248,248,252,255])
bm_Ayane_m01= bytearray([  0,  0,128,248,254,254,255,255,255,255,255,255,255,254,254,252,120,  0,  0,  0,  0,
  0,252,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,252,248,240,224,
  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7])
# BITMAP: W 35, H 39
bm_Ayane_02= bytearray([255,255,255, 63, 95,159,239,247,247,251,123,189,189, 61,189, 89,217,185, 85,221,187, 91,219,151, 71,215, 23,215, 23,199,175,159, 63,255,255,
 31,  7,  0,  0,212,170,169, 69,181, 25,174,211, 40, 19,135,144, 39,241,198,216,231,248, 39,131,144, 43,  3,232,247,248,255,255,255,254,255,
255, 31,192,254, 97,222,190,  0,255,192, 63,252,248,240,241,247,255, 63,191, 63, 63, 47,248,249,255,255, 56,192,  7,255,255,255,255,255,255,
248, 30,143, 99,124,159, 97, 62,  0,127,255,224, 19,227,231,199,207,142,141, 15, 46,167,183,155, 97,120, 97, 15,127,248,199, 63,255,255,255,
159,224,243,252,248,230,142,223,223,188,179,185,254,253,249,251,247,239,239,222,191,128,255,255,255,255,255,128,254,249,243,224,223,191,255])
bm_Ayane_m02= bytearray([  0,192,240,240,240,248,252,252,254,254,255,255,255,255,255,255,255,255,255,255,255,254,254,254,252,252,252,252,252,252,248,240,224,192,128,
255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255, 63, 31,  3,  3,  3,  1,
255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,128,  0,  0,  0,
255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,224,  0,
127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,112])




# BITMAP: W 5, H 4
bm_MOUSE00= bytearray([184, 52, 60, 60, 57])


# BITMAP: W 23, H 23
bm_Ball_BIG00= bytearray([255, 63,207,247,251,251,253,253,254,254,254,254,254,254,252,249, 85,171, 83,167, 79, 63,255,
128, 63,127,255,255,255,255,255,255,255,127,191,127,175, 95,170, 85,170, 85,170, 85, 42,128,
255,254,249,242,229,234,213,202,149,170,149,170,149,170,149,202,213,234,229,242,249,254,255])
bm_Ball_BIGm00= bytearray([  0,192,240,248,252,252,254,254,255,255,255,255,255,255,255,254,254,252,252,248,240,192,  0,
127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,
  0,  1,  7, 15, 31, 31, 63, 63,127,127,127,127,127,127,127, 63, 63, 31, 31, 15,  7,  1,  0])
# BITMAP: W 17, H 17
bm_Ball_BIG01= bytearray([ 31,231,251,253,253,254,254,254,254,254,252,170, 85,169, 83,167, 31,
240,203,151, 47, 87,175, 87,175, 87,171, 85,170, 85, 42,149,202,240,255,255,255,255,255,254,254,254,254,254,254,254,255,255,255,255,255])
bm_Ball_BIGm01= bytearray([224,248,252,254,254,255,255,255,255,255,255,255,254,254,252,248,224,
 15, 63,127,255,255,255,255,255,255,255,255,255,255,255,127, 63, 15,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0])

# BITMAP: W 8, H 7
bm_Ball_Small00= bytearray([227,157,190,190,190,157,131,159])
bm_Ball_Smallm00= bytearray([ 28,126,127,127,127,126,124, 96])
# BITMAP: W 6, H 5
bm_Ball_Small01= bytearray([241,238,238,238,225,239])
bm_Ball_Smallm01= bytearray([ 14, 31, 31, 31, 30, 16])
# BITMAP: W 4, H 4
bm_Ball_Small02= bytearray([249,246,246,241])
bm_Ball_Smallm02= bytearray([  6, 15, 15, 14])


# BITMAP: W 37, H 7
#bm_TXT_READY= bytearray([193,193,229,193,203,255,193,193,213,213,221,255,195,193,229,193,195,255,193,193,221,193,227,255,217,209,199,193,225,255,255,249,249,221,213,241,241])



# BITMAP: W 18, H 7
bm_FrameBack= bytearray([128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,193,227])
# BITMAP: W 26, H 6
bm_TXT_Throw= bytearray([253,224,224,237,255,224,224,253,225,255,225,225,251,253,255,225,237,225,225,255,241,239,241,239,225,225])
# BITMAP: W 16, H 6
bm_TXT_1st= bytearray([127,125, 96, 96, 96,255,255,233,233,229,231,253,224,224,109,127])
bm_TXT_2nd= bytearray([102, 98, 96, 96,104,109,255,225,225,253,227,255,225,237, 96, 96])
bm_TXT_3rd= bytearray([238,234,234,224,224,228,255,225,225,251,253,255,225,237,224,224])


# BITMAP: W 25, H 8
bm_TXT_SPARE= bytearray([198,207,223,251,115,  0,255,255, 51, 51, 30,  0,254,255, 51,255,254,  0,255,255, 27,251,238,  0,255,255,219,195])
# BITMAP: W 34, H 10
bm_TXT_STRIKE= bytearray([255,115, 97, 65,  9, 25,255,249,249,  1,  1,249,249,255,  1,  1,201,  9, 35,255,  1,  1,255,  1,  1,199, 19, 57,255,  1,  1, 73,121,255,
255,158, 14, 14, 78,207,255, 15, 15,206,206, 31,255, 31, 14,206, 15, 30,254, 15, 14, 78, 79, 30,254, 15, 14, 78,207,254,254,254,254,255])


# BITMAP: W 20, H 8
bm_TXT_NEW= bytearray([255,129,131,231,207,129,255,129,129,149,149,157,255,129,129,207,231,207,129,255])
# BITMAP: W 27, H 8
bm_TXT_GAME= bytearray([255,195,129,153,173,137,203,255,131,129,233,233,131,255,129,129,251,247,251,129,255,129,129,149,149,157,255])
# BITMAP: W 47, H 8
bm_TXT_CONTINUE= bytearray([255,195,129,153,189,153,219,255,195,129,153,189,153,195,255,129,131,231,207,129,255,253,129,129,253,255,129,129,255,129,131,231,207,129,255,193,129,159,159,193,255,129,129,149,149,157,255])
# BITMAP: W 25, H 8
bm_TXT_BEST= bytearray([255,129,129,149,149,129,139,255,129,129,149,149,157,255,147,145,149,133,141,255,253,129,129,253,255])




# BITMAP: W 5, H 6
bm_Bnum0= bytearray([127, 97, 97,127,127])
bm_Bnum1= bytearray([ 64, 65,127,127, 64])
bm_Bnum2= bytearray([115,115,121,111,103])
bm_Bnum3= bytearray([ 97,101,101,127,127])
bm_Bnum4= bytearray([ 79, 79, 72,127,127])
bm_Bnum5= bytearray([103,103,101,121,121])
bm_Bnum6= bytearray([126,127,105,121,121])
bm_Bnum7= bytearray([ 65, 65, 65,127,127])
bm_Bnum8= bytearray([127,101,101,127,127])
bm_Bnum9= bytearray([ 78,111,105,127, 95])

Bnum_TBL=[bm_Bnum0,bm_Bnum1,bm_Bnum2,bm_Bnum3,bm_Bnum4,bm_Bnum5,bm_Bnum6,bm_Bnum7,bm_Bnum8,bm_Bnum9]

# BITMAP: W 5, H 5
bm_Num0= bytearray([ 96, 96,238, 96, 96])
bm_Num1= bytearray([127,126, 96, 96,127])
bm_Num2= bytearray([228,100, 98,104,104])
bm_Num3= bytearray([110,106,106, 96, 96])
bm_Num4= bytearray([ 56, 56,187, 32, 32])
bm_Num5= bytearray([108, 44,162, 34, 34])
bm_Num6= bytearray([225,224,234,226,226])
bm_Num7= bytearray([254,254,254,224,224])
bm_Num8= bytearray([224,224,234,224,224])
bm_Num9= bytearray([233,232,234,224,240])

Num_TBL=[bm_Num0,bm_Num1,bm_Num2,bm_Num3,bm_Num4,bm_Num5,bm_Num6,bm_Num7,bm_Num8,bm_Num9]

# BITMAP: W 8, H 7
bm_SPEAR= bytearray([ 63, 31, 15, 15,  7,  3,  1,  1])
bm_STRIK= bytearray([  0, 65, 99,119,119, 99, 65,  0])


tmp=0
tmp4=0
tmp5=0
tmp6=0
SX=0#STAND_X
BallX=0
BallX0=0
BallX2=0
Pins=10
AIM=0
CNT=0
STAMINA=100
#POW=100
SPIN=0
RANE=100
AIM_DIR=0
SPIN_ADD=0
SPIN_DIR=0



#PinData=[712,72,1023,1023,544,144]
MyPin=[1, 1,1, 1,1,1, 1,1,1,1]

MyPinX=[ 0,-12,12,-25,0,25,-36,-12,12,36]
MyPinY=[ 0,18,18,36,36,36,54,54,54,54]
MyPin_DX=[0,0,0,0,0,0,0,0,0,0]
MyPin_DY=[0,0,0,0,0,0,0,0,0,0]

PinX=(0,-1,1,-2,0,2,-3,-1,1,3)
PinX2=(0,-1,1,-3,0,3,-5,-1,1,5)
pinY=(0,18,18,36,36,36,54,54,54,54)
bit=(1,2,4,8,16,32,64,128,256,512,128,256)
OtherPin=(864,712,223,207,544,233,1023,144,72)
EYE_CNT=30

STEP_Tbl=(- 2,- 3,- 3,- 2,- 1,  1,  2,  1,  1,  0,- 1,- 2,- 2,  0,  2,  4,  3,  2,  1,  1,  1,  2,  2,  3,  3,  4,  4,  4,  3,  3,  3,  2,  2,  2,  1,  1,  0)

SPIN_Effect=(0,0,0,0,0,0,0,0,0,0, 0,0,0,1,1,2,4,6,14,28,32,32,32)


FRAME=1 #FRAME
Throw=1
ef_CNT=0

MODE=10
TEST=0
flg=0
SAVE.saveData.setName("Bowling Days")

Grf.display.setFPS(60) # standardize display speed   
while (1):##################################################

 
    while (MODE==1)or(MODE==7):
        Grf.display.setFPS(40)
        if (MODE==1):
            if(Btn.buttonR.pressed())and(SX>-20):
                SX=SX-1
            if (Btn.buttonL.pressed())and(SX<20):
                SX=SX+1        
            if (Btn.buttonA.justPressed()):
                if(CNT>10):    
                    BallX0=-SX*50/15
                    BallX=BallX0
                    flg=0
                    AIM_ofset=0
                    AIM_Add=1
                    MODE=2

            if (Btn.buttonB.justPressed()):
                if(Btn.buttonD.pressed()):
                    if(TEST==0):
                        TEST=1
                    elif(TEST==1):
                        TEST=0
                    
            
            
            if (Btn.buttonU.justPressed()):

                ScoreCard(FRAME,SCORE,0)
            

            
        tmp2=int(SX/4)
        Grf.display.fill(0) # Fill canvas 

        Grf.display.drawFilledRectangle(0, 14, 72,19, 1) 
        Grf.display.drawFilledRectangle(0, 34, 72, 7, 1) 
        
        Grf.display.drawLine(26+tmp2,14,12+SX,32, 0) #Draw ROAD LINE 
        Grf.display.drawLine(26+tmp2,14,11+SX,32, 0)  
        Grf.display.drawLine(25+tmp2,14,10+SX,32, 0)          
        Grf.display.drawLine(25+tmp2,14, 9+SX,32, 0) 
        Grf.display.drawLine(44+tmp2,14,58+SX,32, 0) #Draw ROAD LINE 
        Grf.display.drawLine(44+tmp2,14,59+SX,32, 0)  
        Grf.display.drawLine(45+tmp2,14,60+SX,32, 0)          
        Grf.display.drawLine(45+tmp2,14,61+SX,32, 0)  
        Grf.display.drawLine(23+tmp2,14, 6+SX,32, 0) #Draw ROAD LINE 
        Grf.display.drawLine(22+tmp2,14, 5+SX,32, 0)          
        Grf.display.drawLine(22+tmp2,14, 4+SX,32, 0) 
        Grf.display.drawLine(47+tmp2,14,64+SX,32, 0) #Draw ROAD LINE 
        Grf.display.drawLine(48+tmp2,14,65+SX,32, 0)          
        Grf.display.drawLine(48+tmp2,14,66+SX,32, 0)            
        Grf.display.drawLine(3+tmp2,14,-39+SX,32, 0) #Draw ROAD LINE         
        Grf.display.drawLine(3+tmp2,14,-40+SX,32, 0)  
        Grf.display.drawLine(2+tmp2,14,-41+SX,32, 0)          
        Grf.display.drawLine(1+tmp2,14,-42+SX,32, 0) 
        Grf.display.drawLine(65+tmp2,14,109+SX,32, 0) #Draw ROAD LINE 
        Grf.display.drawLine(65+tmp2,14,110+SX,32, 0)  
        Grf.display.drawLine(66+tmp2,14,111+SX,32, 0)         
        Grf.display.drawLine(67+tmp2,14,112+SX,32, 0)              

        for i in range(1,6):
            Rane=i-3
            Grf.display.blit(bm_Bord_S,25+tmp2+Rane*20,0,11,13,0,0,0)   
            Grf.display.blit(bm_Bord_S,35+tmp2+Rane*20,0,11,13,0,1,0)   
            Grf.display.setPixel(35+SX+Rane*50, 28, 0)
            Grf.display.setPixel(30+SX+Rane*50, 29, 0)
            Grf.display.setPixel(25+SX+Rane*50, 30, 0)
            Grf.display.setPixel(20+SX+Rane*50, 31, 0)
            Grf.display.setPixel(40+SX+Rane*50, 29, 0)
            Grf.display.setPixel(45+SX+Rane*50, 30, 0)
            Grf.display.setPixel(50+SX+Rane*50, 31, 0)
            
            for j in range(0,10):
                PinNo=9-j # 9 to 0
                tmp3=OtherPin[i] & bit[PinNo] #PinData[Rane+2] & bit[PinNo]
                if (Rane==0):# My Rane
                    tmp3=MyPin[PinNo]
                if (tmp3!=0):#Pin is Alive
                    tmp5=1+(PinNo<6)+(PinNo<3)+(PinNo==0)
                    tmp6=32+tmp2+Rane*20
                    Grf.display.setPixel(tmp6+ PinX[PinNo]+3, tmp5, 0)#MARK
                    Grf.display.drawLine(tmp6+ PinX2[PinNo]+3,9,tmp6+ PinX2[PinNo]+3,10+(PinNo<6)+(PinNo==0), 1) #Draw Pin(Long)                

        if(MODE==7):
            tmp=int(CNT2/10)
            Y=int(CNT2/5)
            
            SPIN_DIR=SPIN_Effect[Y]*SPIN/4/Power
            BallX2=BallX2+AIM_DIR2+SPIN_DIR###### BALL Method ***********            

            X=int(35+BallX2)
            if(Y<10):
                Grf.display.blitWithMask(bm_Ball_Small00,X-4,35-Y,8,7,0,0,0,bm_Ball_Smallm00)  
                CNT2=CNT2+3             
            elif(Y<15):
                CNT2=CNT2+2            
                Grf.display.blitWithMask(bm_Ball_Small01,X-3,34-Y,6,5,0,0,0,bm_Ball_Smallm01)   
            else:
                Grf.display.blitWithMask(bm_Ball_Small02,X-2,33-Y,4,4,0,0,0,bm_Ball_Smallm02)   
                CNT2=CNT2+1
                          
        if(MODE==1):
                tmp=int(33- ef_CNT)
                if(tmp<13):
                    tmp=13
                Grf.display.blitWithMask(bm_Ayane_01 ,16,tmp,21,19,0,0,0,bm_Ayane_m01)   

                          
        Grf.display.drawFilledRectangle(0, 32, 72,1, 0)
        Grf.display.drawFilledRectangle(0, 33, 72,7, 1) #### Under SPACE  

        if(MODE==1):
                tmp=-18+int(ef_CNT*1.5)
                if(tmp>0):
                    tmp=0              
                Sprite_Back = Spr.Sprite(18,7, bm_FrameBack ,tmp, 33)
                Grf.display.drawSprite(Sprite_Back) 
                tmp2=bm_Bnum0
                if(FRAME==10):
                    tmp2=bm_Bnum1
                Sprite_Back = Spr.Sprite(5,6, tmp2 ,tmp+2, 33)#
                Grf.display.drawSprite(Sprite_Back)
                
                tmp2=Bnum_TBL[FRAME%10]
                
                Sprite_Back = Spr.Sprite(5,6, tmp2 ,tmp+9, 33)
                Grf.display.drawSprite(Sprite_Back)               
                
                tmp=48-int(ef_CNT*.5)
                if(tmp<34):
                    tmp=34              
                Sprite_Back = Spr.Sprite(26,6, bm_TXT_Throw ,41, tmp)
                Grf.display.drawSprite(Sprite_Back)  
                if(Throw==1):
                    tmp2=bm_TXT_1st
                elif(Throw==2):
                    tmp2=bm_TXT_2nd                
                else:
                    tmp2=bm_TXT_3rd
                Sprite_Back = Spr.Sprite(16,6, tmp2 ,22, tmp)# READY
                Grf.display.drawSprite(Sprite_Back)          

        ef_CNT=ef_CNT+1
        
        if(TEST==1)and(MODE==1):
            Grf.display.blitWithMask(bm_TestPin,1,1,7,7,0,0,0,bm_TestPin_m)   
        
        Grf.display.update()#-----------------------------------------------------------
        CNT=CNT+1
        if(MODE==7)and(CNT2>90):
            CNT=-20
            for i in range(0,90):
                SPIN_DIR=SPIN_Effect[int(i/5)]*SPIN/Power
                BallX=BallX+AIM_DIR+SPIN_DIR###### BALL Method 2 ***********
            
            EYE_CNT=0
            MODE=8
        
        
    while (MODE==2)or(MODE==8): ######################################################################
        Grf.display.setFPS(60)
        if(MODE!=8):
            if(Btn.buttonA.justPressed()):
                if(CNT>10):
                    CNT=1
                    AIM=AIM+AIM_ofset
                    AIM_DIR=(AIM*70/55-BallX0)/RANE
                    flg=0
                    MODE=4
            if (Btn.buttonB.justPressed()):
                ef_CNT=100
                MODE=1
            if (Btn.buttonL.pressed())and(AIM>-55):
                AIM=AIM-1
            if (Btn.buttonR.pressed())and(AIM<55):
                AIM=AIM+1
                
        ofset=0
        AIM_X=AIM
        if (AIM>35):
            ofset=35-AIM
            AIM_X=35
        if (AIM<-35):
            ofset=-(35+AIM)
            AIM_X=-35
        Grf.display.fill(0) # Fill canvas  
        Grf.display.blit(bm_PinUp_Floor,ofset-10,35,39,6,0,0,0)  
        Grf.display.drawFilledRectangle(ofset+30, 35, 10, 5, 1) 
        Grf.display.blit(bm_PinUp_Floor,ofset+41,35,39,6,0,1,0) 
        
        BallDrawFlg=0
        for j in range(0,10):
            PinNo=9-j # 9 to 0
            tmp3=MyPin[PinNo]

            BallX=BallX+AIM_DIR/10+SPIN_DIR/6
            if(MODE==8)and(BallDrawFlg==0)and((CNT*3+8)>pinY[PinNo]):
                Grf.display.blitWithMask(bm_Ball_BIG01,35+ofset+int(BallX*0.75)-8,23-CNT,17,17,0,0,0,bm_Ball_BIGm01)  #Draw Ball 
                BallDrawFlg=10


            if (tmp3!=0):# Pin is Alive *************************************::
                tmpX=int(MyPinX[PinNo]*.75)
                tmpY=9-int(MyPinY[PinNo]/6)
                
                PinPtn=bm_Pin00
                PinPtn_m=bm_Pin_m00
                PinW=11
                PinH=28
                MR=0
                
                if (MyPin[PinNo]!=1):
                    MR=PinAnimNo[PinAnim[PinNo]-1][0]# Mirror
                    tmp=abs(int(MyPin[PinNo]/4))+1
                    if (tmp>7):
                        tmp=7
                        
                    tmpAnim=PinAnim[PinNo]
                    
                    Ptn=PinAnimNo[tmpAnim][7-tmp]
                    
                    PinPtn=PinPtnNo[Ptn]
                    PinPtn_m=PinPtnmNo[Ptn]
                    PinW=Pin_W[Ptn]
                    PinH=Pin_H[Ptn]

                ofX=int(PinW/2)
                ofY=int((28-PinH)*.5)
                Grf.display.blitWithMask(PinPtn,ofset+35+tmpX-ofX,tmpY+ofY,PinW,PinH,0,MR,0,PinPtn_m)  # Draw Pin 
        
           
                if (MODE==8):
                    tmpX=MyPinX[PinNo]
                    tmpY=MyPinY[PinNo]
                    if(abs(tmpX-BallX)<13.5)and(abs(tmpY-CNT*3)<10)and(MyPin[PinNo]==1):
                        
                        # Ball VS PIN *****************************
                        
                        MyPin_DX[PinNo]=(tmpX-BallX)*Power/50+(random.randint(0,40)-20)/18+ AIM_DIR*12+SPIN/2.5
                        
                        MyPin_DY[PinNo]=(15-abs(BallX-tmpX)+random.randint(0,3)-1- SPIN/4)/3
                        if(MyPin_DY[PinNo]<0):
                            MyPin_DY[PinNo]=MyPin_DY[PinNo]/5

                        MyPin[PinNo]=-20

                        PinAnim[PinNo]=PinAnimSelect(MyPin_DX[PinNo])

                        tmp=MyPin_DX[PinNo]/(Power*0.8)
                        if(tmp>2.5):
                            tmp=2.5
                        if (tmp<-2.5):
                            tmp=-2.5
                        AIM_DIR=AIM_DIR-tmp
                        Power=Power*.75
                        SPIN=SPIN*.5

                    if(MyPin[PinNo]==1):
                        for k in range(0,10):
                            if (MyPin[k]<0):
                                tmpX=MyPinX[PinNo]
                                tmpY=MyPinY[PinNo]                                
                                tmpX2=MyPinX[k]
                                tmpY2=MyPinY[k]
                                
                                H_Range=5.2+Power*.01+(Power>80)*.1+(Power>95)*.4
                                H_Range=H_Range+abs(SPIN)*.03+(abs(SPIN>8))*.4+(random.randint(0,8)==1)
                                
                                if(abs(tmpX-tmpX2)<H_Range)  and  (tmpY>(tmpY2))and(tmpY<(tmpY2+14)):
                        
                                    # PIN VS PIN ***************************
                                    
                                    MyPin[PinNo]=-20
                                    
                                    MyPin_DX[PinNo]=((tmpX-tmpX2)*1.0+(random.randint(0,60)-30)/10+ MyPin_DX[k])*.9
                                    MyPin_DY[PinNo]=(12-abs(tmpX2-tmpX)+(random.randint(0,5))-2)*.3
                                    if(MyPin_DX[PinNo]>12):
                                        MyPin_DX[PinNo]=12
                                    if(MyPin_DX[PinNo]<-12):
                                        MyPin_DX[PinNo]=-12
                                    PinAnim[PinNo]=PinAnimSelect(MyPin_DX[PinNo])

                    MyPinX[PinNo]=MyPinX[PinNo]+int(MyPin_DX[PinNo]/5)
                    MyPinY[PinNo]=MyPinY[PinNo]+MyPin_DY[PinNo]
                    if (MyPin[PinNo]<0):
                        MyPin[PinNo]=MyPin[PinNo]+1
                        if (MyPin[PinNo]>0):
                            MyPin[PinNo]=0
            if(MODE==8)and((CNT*3+8)<0):
                Grf.display.blitWithMask(bm_Ball_BIG01,35+ofset+int(BallX*0.75)-8,23-CNT,17,17,0,0,0,bm_Ball_BIGm01)  #Draw Ball 


        if(MODE==2):#and(CNT%20<10)
                AIM_ofset=AIM_ofset + AIM_Add
                if(AIM_ofset>8):
                    AIM_Add=-1
                if(AIM_ofset<-8):
                    AIM_Add=1

                Grf.display.blitWithMask(bm_Arrow00,33+ AIM_X+int(AIM_ofset),31,7,9,0,0,0,bm_Arrow_m00)               

        if(MODE==8)and(CNT>80):
            Pins=0
            for j in range(0,10):
                if (MyPin[j]!=1):
                    MyPin[j]=0
                Pins=Pins+(MyPin[j]==1)#  Pins Count ************

           
            if(Pins==0):# No Pins (STRIKE or SPARE)
                flg=0
                if(Throw==1):
                    flg=2 #STRIKE
                elif(Throw==2):
                    flg=1#SPARE
                    if(FRAME==10)and(SCORE[19]==10):#---------- FRAME10
                        flg=2 #STRIKE
                elif(Throw==3):
                    flg=1 #SPARE
                    if(SCORE[20]==10):# Throw2 is STRIKE
                        flg=2  #STRIKE
                    elif((SCORE[19]+SCORE[20])==10):
                        flg=2  #STRIKE


            if(Pins==0)and(EYE_CNT==0):
                if(flg==2):# 10 Pins crush(STRIKE or SPARE)
                    EYE_CNT=80
                    while (EYE_CNT>0):
                        
                        tmp2=EYE_CNT-60
                        if (tmp2<0):
                            tmp2=0
                            
                        tmp3=int(4*(80-EYE_CNT)*EYE_CNT/320)
                        Grf.display.fill(1) # Fill canvas
                        for i in range(0,18) :
                            Sprite_Back = Spr.Sprite(4,8, bm_CHECK ,i*4, 0)
                            Grf.display.drawSprite(Sprite_Back)   
                        if(EYE_CNT<75):
                            Grf.display.blitWithMask(bm_Pin03,48+tmp3,20-tmp3,14,28,0,0,0,bm_Pin_m03)   
                            Grf.display.blitWithMask(bm_Pin08,48+int(tmp3*1.1),24-int(tmp3/2),16,13,0,0,0,bm_Pin_m08)  
                            Grf.display.blitWithMask(bm_Pin08,25-int(tmp3*1.1),24-int(tmp3/1.2),16,13,0,1,0,bm_Pin_m08)  
 
                            Grf.display.blitWithMask(bm_Pin07,48+int(tmp3*1.4),26-int(tmp3/3),22,15,0,0,0,bm_Pin_m07)  
                            Grf.display.blitWithMask(bm_Pin07,22-int(tmp3*1.4),26-int(tmp3/3.5),22,15,0,1,0,bm_Pin_m07)  
                            
                        Grf.display.blitWithMask(bm_Ball_BIG01,40,25-tmp3, 17,17,0,0,0,bm_Ball_BIGm01)    
                            
                        Grf.display.blitWithMask(bm_Ayane_02,-tmp2*2,2, 35,39,0,0,0,bm_Ayane_m02)       
                    
                        if(EYE_CNT%20<10):                        
                            Sprite_Back = Spr.Sprite(34,10, bm_TXT_STRIKE ,37, 10)# STRIKE
                            Grf.display.drawSprite(Sprite_Back)                           
                        
                    
                        EYE_CNT=EYE_CNT-1
                        
                        Grf.display.update()  #-----------------------------------------------------------
                                       
                #else:#          SPARE       
                elif(flg==1):#          SPARE            
                    EYE_CNT=80
                    while (EYE_CNT>0):
                        Grf.display.drawFilledRectangle(23,10,30,10, 0)    
                        if(EYE_CNT%20<10):
                            Sprite_Back = Spr.Sprite(28,8, bm_TXT_SPARE ,24, 11)# SPARE
                            Grf.display.drawSprite(Sprite_Back)    
                    
                        EYE_CNT=EYE_CNT-1
                        Grf.display.update()  #-----------------------------------------------------------
                


            flg=0
            if(FRAME<10):
                if(Throw==1):
                    Get1=10-Pins
                    if (Get1==10):# STRIKE
                        SCORE.append(10)
                        SCORE.append(0)
                        FRAME=SCORE[0]+1
                        SCORE[0]=FRAME
                        Throw=1
                        flg=1
                    else:
                        SCORE.append(Get1)
                        Throw=2
                elif(Throw==2):
                    Get1=SCORE[-1]
                    Get2=10-Get1-Pins
                    SCORE.append(Get2)
                    FRAME=SCORE[0]+1
                    SCORE[0]=FRAME
                    Throw=1
                    flg=1                 
            else:#---------------------- FRAME10
                if(Throw==1):
                    flg=0
                    Get1=10-Pins
                    SCORE.append(Get1)
                    if (Get1==10):# STRIKE
                        flg=1 # Pin Reset
                    Throw=2
                elif(Throw==2):
                    flg=0
                    Get1=SCORE[19]
                    if(Get1!=10):
                        Get2=10-Get1-Pins
                    else:
                        Get2=10-Pins
                    print(f"GET1:{Get1}")
                    print(f"GET2:{Get2}")
                    SCORE.append(Get2)
    
                    if(Pins==0):# Throw2 is STRIKE or SPARE
                        Throw=3
                        flg=1 # Pin Reset
                    else:# -------When Throw2 finished,Pin is remain.
                        if(SCORE[19]!=10):# Throw1 is not Strike
                            flg=3
                        else:#----------Throw1 is Strike. Throw2 is not Strike
                            Throw=3
                elif(Throw==3):
                    Get1=SCORE[19]
                    Get2=SCORE[20]
                    if((Get1+Get2)%10==0):
                        tmp=10-Pins
                    else:
                        tmp=10-Get2-Pins
                    print(f"GET1:{Get1}")
                    print(f"GET2:{Get2}")
                    print(f"GET3:{tmp}")
                    
                    SCORE.append(tmp)                       
                    flg=3

                    
            if (flg==3)and(EYE_CNT==0):#GameSet
                SCORE[0]=11
                SAVE.saveData.setItem("SaveDATA", SCORE)
                SAVE.saveData.save()
                ScoreCard(11,SCORE,2)

                MODE=10
                

            if (flg==1)or(flg==4):# RANE RESET
                Pins=10
                MyPin=[1, 1,1, 1,1,1, 1,1,1,1]
                MyPinX=[ 0,-12,12,-25,0,25,-36,-12,12,36]
                MyPinY=[ 0,18,18,36,36,36,54,54,54,54]
                MyPin_DX=[0,0,0,0,0,0,0,0,0,0]
                MyPin_DY=[0,0,0,0,0,0,0,0,0,0]
            CNT=0
            SX=random.randint(0,10)-10
            SPIN=0
            AIM=0
            flg=0
            ef_CNT=0
            if(MODE==8)and(EYE_CNT==0):
                if(flg!=3):
                    # When Not GAMESET 
                    SAVE.saveData.setItem("SaveDATA", SCORE)
                    SAVE.saveData.save()
                    SAVE.saveData.setItem("Throw", Throw)
                    SAVE.saveData.save()
                    SAVE.saveData.setItem("MyPin", MyPin)
                    SAVE.saveData.save()
                    ScoreCard(FRAME,SCORE,0)
                    
                MODE=1

        if(TEST==1)and(MODE==8):
            Grf.display.fill(1) # Fill canvas    
            
            for i in range(0,10):
                if (MyPin[i]!=0):
                    tmpx=int(MyPinX[i]/2)-3
                    tmpy=int(MyPinY[i]/2)-3
                    Grf.display.blitWithMask(bm_TestPin,36+tmpx,25-tmpy,7,7,0,0,0,bm_TestPin_m)                      
            tmpx=int(BallX/2)-4
            tmpy=int(CNT*3/2)-4
            Grf.display.blitWithMask(bm_TestBall,36+tmpx,25-tmpy,9,9,0,0,0,bm_TestBall_m)                   

        

        CNT=CNT+1
        if (CNT>=1000):
            CNT=0
        
        Grf.display.update()  #-----------------------------------------------------------
        
        
    while (MODE>=3)and(MODE<=5):  #####################################################################
        Grf.display.setFPS(60) 

        Grf.display.fill(1) # Fill canvas  
        for i in range(0,18) :
            Sprite_Back = Spr.Sprite(4,8, bm_CHECK ,i*4, 0)
            Grf.display.drawSprite(Sprite_Back)     

        Grf.display.blitWithMask( bm_Ayane_00,40,-4,36,38,0,0,0,bm_Ayane_m00)   
        Grf.display.blitWithMask( bm_Ball_BIG00,31,21,23,23,0,0,0,bm_Ball_BIGm00) 
        Grf.display.drawFilledRectangle(0, 32, 72,1, 0)
        Grf.display.drawFilledRectangle(0, 33, 72,7, 1) #### Under SPACE  
        
#        if(MODE==3):
#            if (Btn.buttonA.justPressed()): 
#                if(flg==1)or(CNT>10):
#                    MODE=4
#                    flg=0
#                flg=1
#            if (Btn.buttonB.justPressed()):            
#                if(flg==1):
#                    AIM_ofset=0
#                    AIM_Add=1
#                    MODE=2
#
#            if(CNT%20<10):
#                Sprite_Back = Spr.Sprite(37,7, bm_TXT_READY ,18, 33)# READY
#                Grf.display.drawSprite(Sprite_Back)
            

        
        if(MODE==4):#---Power

            PowCNT=0
            PowCNTadd=1
            if (Btn.buttonA.justPressed()):
                flg=flg# RESET justpressed
            while(MODE==4):
                Grf.display.drawFilledRectangle(0, 34, 50,5, 1)   
                Grf.display.drawFilledRectangle(21, 34, 50,5, 0)                
                Grf.display.drawFilledRectangle(22, 35, PowCNT,3, 1) #Power
            
                if (Btn.buttonA.justPressed()):            
                    if (PowCNT>2)or(flg==1):
                        Power=PowCNT+52
                        MODE=5
                        flg=0
                    flg=1
                        
                PowCNT=PowCNT+PowCNTadd
                if (PowCNT>48):
                    PowCNT=48
                    PowCNTadd=-3
                if(PowCNT<2):
                    PowCNT=21
                    PowCNTadd=1
                if(CNT%40<20):
                    Sprite_Back = Spr.Sprite(19,6, bm_TXT_POW ,1, 33)
                    Grf.display.drawSprite(Sprite_Back)
                CNT=CNT+1
                if (CNT>9):
                    flg=1
                if (CNT>=1000):
                    CNT=10
                Grf.display.update()  #--------------------------------------------------
            
        if(MODE==5):#-------------------- SPIN
            SPIN=-10
            SPINadd=1
            if(SPINadd<-1):
                SPINadd=-1
            if(SPINadd>1):
                SPINadd=1
            if (Btn.buttonA.justPressed()):
                flg=flg# RESET justpressed
            flg=0
            while(MODE==5):
                
                Grf.display.drawFilledRectangle(0, 34, 72,5, 1)       
                Sprite_Back = Spr.Sprite(21,4, bm_SPIN_Meter ,28, 35)
                Grf.display.drawSprite(Sprite_Back)            
                Grf.display.blitWithMask( bm_Arrow01,35+int(SPIN),31,7,4,0,0,0,bm_Arrow_m01) 
 
 
                if (Btn.buttonA.justPressed()):            
                    if (flg==1):
                        CNT=1
                        MODE=6
                        flg=0
                flg=1         
                
                SPIN=SPIN+SPINadd
                if (SPIN>10):
                    SPIN=10
                    SPINadd=-SPINadd

                if(SPIN<-10):
                    SPIN=-10
                    SPINadd=-SPINadd

                if(CNT%40<20):    
                    Sprite_Back = Spr.Sprite(20,6, bm_TXT_SPIN ,3, 33)
                    Grf.display.drawSprite(Sprite_Back)                
                CNT=CNT+1
                if (CNT>=1000):
                    CNT=10
                Grf.display.update()  #--------------------------------------------------
                
            
        
        CNT=CNT+1
        if (CNT>9):        
            flg=1
        if (CNT>=1000):
            CNT=10
                
        Grf.display.update()  #--------------------------------------------------
        
        
    while (MODE==6):  ######################################################################
        Grf.display.setFPS(30) 
        Grf.display.fill(1) # Fill canvas        
        for i in range(0,18) :
            Sprite_Back = Spr.Sprite(4,8, bm_CHECK ,i*4, 0)
            Grf.display.drawSprite(Sprite_Back)           
        tmp=int((CNT)/2)
        ofset=STEP_Tbl[tmp]
        ofsetB=int(CNT-20)
        if(ofsetB<0):
            ofsetB=0
        
        tmp2= 40-int(CNT/2)
        tmp3=-3+ofset
        Grf.display.blitWithMask( bm_Ayane_00,tmp2,tmp3,36,38,0,0,0,bm_Ayane_m00)   
        Grf.display.blitWithMask( bm_Ball_BIG00,30-int(CNT/2)-int(ofsetB*1.2),23+ofsetB+int(ofset/2),23,23,0,0,0,bm_Ball_BIGm00)         
        if(CNT>(len(STEP_Tbl)*1.6)):
            Sprite_Back = Spr.Sprite(5,4, bm_MOUSE00 ,tmp2+12, tmp3+22)
            Grf.display.drawSprite(Sprite_Back)
        
        Grf.display.drawFilledRectangle(0, 32, 72,1, 0)
        Grf.display.drawFilledRectangle(0, 33, 72,7, 1) #### Under SPACE  
        
        Sprite_Back = Spr.Sprite(21,4, bm_SPIN_Meter ,0, 35)
        Grf.display.drawSprite(Sprite_Back)            
        Grf.display.blitWithMask( bm_Arrow01,7+int(SPIN),32,7,4,0,0,0,bm_Arrow_m01) 
        
        Grf.display.drawFilledRectangle(23, 34, 50,5, 0)                
        Grf.display.drawFilledRectangle(24, 35, PowCNT-1,3, 1) #Power
                   
  
        CNT=CNT+1
        if (CNT>=len(STEP_Tbl)*2):
            CNT2=0
            BallX=BallX0
            BallX2=0
            AIM2=AIM*21/100+(SX/4)
            AIM_DIR2=AIM2/90
            MODE=7   
        Grf.display.update()        #--------------------------------------------------

    while (MODE==10):# TLTLE
        Grf.display.setFPS(30) # standardize display speed   
        if(CNT>80):
            CNT=80
            flg=1
        tmp=CNT
        if(tmp>40):
            tmp=40
        Grf.display.fill(1) # Fill canvas  
        for i in range(0,18) :
            Sprite_Back = Spr.Sprite(4,8, bm_CHECK ,i*4, 0)
            Grf.display.drawSprite(Sprite_Back)    
        Grf.display.blitWithMask( bm_Pin07,16,27,22,15,0,1,0,bm_Pin_m07) 
        Grf.display.blitWithMask( bm_Pin03,32,17,14,28,0,1,0,bm_Pin_m03) 
        Grf.display.    blitWithMask( bm_Pin04,57,21,15,22,0,0,0,bm_Pin_m04) 
        Grf.display.blitWithMask( bm_Ball_BIG01,43,27,17,17,0,0,0,bm_Ball_BIGm01) 
        if(CNT%10<5):
            Grf.display.blitWithMask( bm_TITLE,30+40-tmp,2, 42,24,0,0,0,bm_TITLEm )
        Grf.display.blitWithMask( bm_Ayane_02,-40+tmp,1, 35,39,0,0,0,bm_Ayane_m02) 

             
        Grf.display.update()        #--------------------------------------------------     
        if (Btn.buttonA.justPressed()):            
            if (CNT>10):
                MODE=11

        CNT=CNT+1
        Grf.display.update()        #--------------------------------------------------        
    
    while (MODE==11):# GAME SELECT
        Grf.display.setFPS(30) # standardize display speed   
    
        flg2=0
        tmpX=4# bit3( bit1= Continue/ bit2=BestScore /Bit3=New GAME)
        tmpY=0
        SCORE=[]
        tmp5=1
        tmp6=[]
        SX=random.randint(0,10)-10

        while(flg2==0):
            Grf.display.fill(1) # Fill canvas      
            for i in range(0,18) :
                Sprite_Back = Spr.Sprite(4,8, bm_CHECK ,i*4, 0)
                Grf.display.drawSprite(Sprite_Back)
            
            
            if (SAVE.saveData.hasItem("SaveDATA")):
                SCORE= (SAVE.saveData.getItem("SaveDATA"))#SCORE
                tmp5= int(SAVE.saveData.getItem("Throw"))#Throw
                tmp6= (SAVE.saveData.getItem("MyPin"))  
                if (SAVE.saveData.hasItem("BestScore")):
                    tmpX=tmpX|2#  bit1

                flg=0#if SAVEDATA is Already GameSet
                if(SCORE[0]==11):
                    flg=1

                if(flg==0):
                    tmpX=tmpX|1#  bit1
                    Sprite_Back = Spr.Sprite(47,8, bm_TXT_CONTINUE ,12, 6)
                    Grf.display.drawSprite(Sprite_Back) 
                    
                if((tmpX&2)!=0):
                    Sprite_Back = Spr.Sprite(25,8, bm_TXT_BEST ,12, 18)
                    Grf.display.drawSprite(Sprite_Back) 
                    Sprite_Back = Spr.Sprite(27,8, bm_TXT_GAME,37, 18)
                    Grf.display.drawSprite(Sprite_Back) 
                    
            Sprite_Back = Spr.Sprite(20,8, bm_TXT_NEW ,12, 26)
            Grf.display.drawSprite(Sprite_Back)                          
            Sprite_Back = Spr.Sprite(27,8, bm_TXT_GAME ,32, 26)
            Grf.display.drawSprite(Sprite_Back)                          
 
            while(((2**tmpY)&tmpX)==0):
                tmpY=tmpY+1
                if (tmpY>2):
                    tmpY=0  
    
            if (Btn.buttonU.justPressed()):       
                tmpY=tmpY-1
                if (tmpY<0):
                    tmpY=2

                while(((2**tmpY)&tmpX)==0):
                    tmpY=tmpY-1
                    if (tmpY<0):
                        tmpY=2
                
            if (Btn.buttonD.justPressed()):       
                tmpY=tmpY+1
                if (tmpY>2):
                    tmpY=0

                while(((2**tmpY)&tmpX)==0):
                    tmpY=tmpY+1
                    if (tmpY>2):
                        tmpY=0  

           
                
            Grf.display.blitWithMask(bm_TestBall,1,tmpY*10+6,9,9,0,0,0,bm_TestBall_m)      

            if (Btn.buttonA.justPressed()):            
                if (CNT>20):
                   
                    if(tmpY==1):
                        flg=1
                        SCORE=[]
                        SCORE =(SAVE.saveData.getItem("BestScore"))#SCORE
                        ScoreCard(SCORE[0],SCORE,2)
                        MODE=11
                        flg2=1
                    
                    SCORE=[1]
                    #SCORE=[10, 5,4, 7,3, 6,3, 10,0, 10,0, 6,3, 5,5, 10,0, 10,0]
                    
                    Throw=1
                    
                    MyPin=[1, 1,1, 1,1,1, 1,1,1,1]
                    #MyPin=[1, 0,0, 0,0,0, 0,0,0,0]
                    
                    MyPinX=[ 0,-12,12,-25,0,25,-36,-12,12,36]
                    MyPinY=[ 0,18,18,36,36,36,54,54,54,54]
                    
                    if (tmpY==0):
                        SCORE=[]
                        SCORE= (SAVE.saveData.getItem("SaveDATA"))#SCORE
                        Throw=tmp5
                        MyPin=tmp6
                        ScoreCard(SCORE[0],SCORE,0)
                        FRAME=SCORE[0]
                        MODE=1
                        CNT=0
                        flg2=1
                    
                    if (tmpY==2):        
                        FRAME=SCORE[0]
        
                        Get1=0
                        MODE=1
                        CNT=0
                        MyPin_DX=[0,0,0,0,0,0,0,0,0,0]
                        MyPin_DY=[0,0,0,0,0,0,0,0,0,0]
                        flg2=1
                   
 
            
            CNT=CNT+1
            Grf.display.update()        #--------------------------------------------------            
            
            
        

        
        
        
        
        
        
