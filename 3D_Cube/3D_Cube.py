#----------------------------------------------------------------------#
#---------------------------3D Cube------------------------------------#
#----------------------------------------------------------------------#
#------------------------YouTube-3DSage--------------------------------#
#----------------------------------------------------------------------#

import thumby

#screen width height
SW  =72
SH  =40
SW2 =36
SH2 =20

T_Sin = [0,9,18,27,36,45,54,62,71,80,89,98,106,115,124,133,141,150,158,167,175,
183,192,200,208,216,224,232,240,248,256,264,271,279,286,294,301,308,315,322,329,
336,343,349,356,362,368,374,380,386,392,398,403,409,414,419,424,429,434,439,443,
448,452,456,460,464,468,471,475,478,481,484,487,490,492,495,497,499,501,503,504,
506,507,508,509,510,511,511,512,512,512,512,512,511,511,510,509,508,507,506,504,
503,501,499,497,495,492,490,487,484,481,478,475,471,468,464,460,456,452,448,443,
439,434,429,424,419,414,409,403,398,392,386,380,374,368,362,356,349,343,336,329,
322,315,308,301,294,286,279,271,264,256,248,240,232,224,216,208,200,192,183,175,
167,158,150,141,133,124,115,106,98,89,80,71,62,54,45,36,27,18,9,0,
-9,-18,-27,-36,-45,-54,-62,-71,-80,-89,-98,-106,-115,-124,-133,-141,-150,-158,-167,-175,
-183,-192,-200,-208,-216,-224,-232,-240,-248,-256,-264,-271,-279,-286,-294,-301,-308,-315,-322,-329,
-336,-343,-349,-356,-362,-368,-374,-380,-386,-392,-398,-403,-409,-414,-419,-424,-429,-434,-439,-443,
-448,-452,-456,-460,-464,-468,-471,-475,-478,-481,-484,-487,-490,-492,-495,-497,-499,-501,-503,-504,
-506,-507,-508,-509,-510,-511,-511,-512,-512,-512,-512,-512,-511,-511,-510,-509,-508,-507,-506,-504,
-503,-501,-499,-497,-495,-492,-490,-487,-484,-481,-478,-475,-471,-468,-464,-460,-456,-452,-448,-443,
-439,-434,-429,-424,-419,-414,-409,-403,-398,-392,-386,-380,-374,-368,-362,-356,-349,-343,-336,-329,
-322,-315,-308,-301,-294,-286,-279,-271,-264,-256,-248,-240,-232,-224,-216,-208,-200,-192,-183,-175,
-167,-158,-150,-141,-133,-124,-115,-106,-98,-89,-80,-71,-62,-54,-45,-36,-27,-18,-9]
 
T_Cos = [512,512,512,511,511,510,509,508,507,506,504,503,501,499,497,495,492,490,487,484,481,
478,475,471,468,464,460,456,452,448,443,439,434,429,424,419,414,409,403,398,392,
386,380,374,368,362,356,349,343,336,329,322,315,308,301,294,286,279,271,264,256,
248,240,232,224,216,208,200,192,183,175,167,158,150,141,133,124,115,106,98,89,
80,71,62,54,45,36,27,18,9,0,-9,-18,-27,-36,-45,-54,-62,-71,-80,-89,
-98,-106,-115,-124,-133,-141,-150,-158,-167,-175,-183,-192,-200,-208,-216,-224,-232,-240,-248,-256,
-264,-271,-279,-286,-294,-301,-308,-315,-322,-329,-336,-343,-349,-356,-362,-368,-374,-380,-386,-392,
-398,-403,-409,-414,-419,-424,-429,-434,-439,-443,-448,-452,-456,-460,-464,-468,-471,-475,-478,-481,
-484,-487,-490,-492,-495,-497,-499,-501,-503,-504,-506,-507,-508,-509,-510,-511,-511,-512,-512,-512,
-512,-512,-511,-511,-510,-509,-508,-507,-506,-504,-503,-501,-499,-497,-495,-492,-490,-487,-484,-481,
-478,-475,-471,-468,-464,-460,-456,-452,-448,-443,-439,-434,-429,-424,-419,-414,-409,-403,-398,-392,
-386,-380,-374,-368,-362,-356,-349,-343,-336,-329,-322,-315,-308,-301,-294,-286,-279,-271,-264,-256,
-248,-240,-232,-224,-216,-208,-200,-192,-183,-175,-167,-158,-150,-141,-133,-124,-115,-106,-98,-89,
-80,-71,-62,-54,-45,-36,-27,-18,-9,0,9,18,27,36,45,54,62,71,80,89,
98,106,115,124,133,141,150,158,167,175,183,192,200,208,216,224,232,240,248,256,
264,271,279,286,294,301,308,315,322,329,336,343,349,356,362,368,374,380,386,392,
398,403,409,414,419,424,429,434,439,443,448,452,456,460,464,468,471,475,478,481,
484,487,490,492,495,497,499,501,503,504,506,507,508,509,510,511,511,512,512]

#cube vertices
cbx=[-12,-12, 12, 12,  -12,-12, 12, 12]
cby=[-12, 12, 12,-12,  -12, 12, 12,-12]
cbz=[ 12, 12, 12, 12,  -12,-12,-12,-12]
#pyramid
cpx=[-12,  0,  0, 12,  -12,  0,  0, 12]
cpy=[-12, 12, 12,-12,  -12, 12, 12,-12]
cpz=[ 12,  0,  0, 12,  -12,  0,  0,-12]

#rotation
rot=0 
#hold vertex screen position
hvx=[0,0,0,0,0,0,0,0]
hvy=[0,0,0,0,0,0,0,0]
#rotation speed
rs=1 
#invert
inv=1
#freese
frz=0
#pyramid
prd=0

#draw cube
def drawCube():
    #camera z
    cz=36 
    #update rotation
    global rot,rs,inv,frz
    if(frz==0):
        rot+=rs
        if(rot>359): rot-=360
    #sin cos
    TC=T_Cos[rot]
    TS=T_Sin[rot]
    #8 verticies
    for x in range(8): 
        #load point
        if prd==1:
            vx=cpx[x]
            vy=cpy[x]
            vz=cpz[x]
        else:
            vx=cbx[x]
            vy=cby[x]
            vz=cbz[x]            
        #rotate on y
        a=vx*TC-vy*TS
        b=vy*TC+vx*TS 
        vx=a>>9 
        vy=b>>9 
        #rotate on y
        a=vx*TC-vz*TS
        b=vz*TC+vx*TS 
        vx=a>>9 
        vz=b>>9
        #depth
        d=(1024*12)/(vz+cz)
        vx=(int(vx*d)>>9)+SW2 
        vy=(int(vy*d)>>9)+SH2+1
        #draw 
        if(vz+cz>0 and vx>0 and vx<SW and vy>0 and vy<SH):
            hvx[x]=vx
            hvy[x]=vy
    #front square
    thumby.display.drawLine(hvx[0],hvy[0], hvx[1],hvy[1], inv)
    thumby.display.drawLine(hvx[1],hvy[1], hvx[2],hvy[2], inv)
    thumby.display.drawLine(hvx[2],hvy[2], hvx[3],hvy[3], inv)
    thumby.display.drawLine(hvx[3],hvy[3], hvx[0],hvy[0], inv)
    #back square
    thumby.display.drawLine(hvx[4],hvy[4], hvx[5],hvy[5], inv)
    thumby.display.drawLine(hvx[5],hvy[5], hvx[6],hvy[6], inv)
    thumby.display.drawLine(hvx[6],hvy[6], hvx[7],hvy[7], inv)
    thumby.display.drawLine(hvx[7],hvy[7], hvx[4],hvy[4], inv)
    #corners
    thumby.display.drawLine(hvx[0],hvy[0], hvx[4],hvy[4], inv)
    thumby.display.drawLine(hvx[1],hvy[1], hvx[5],hvy[5], inv)
    thumby.display.drawLine(hvx[2],hvy[2], hvx[6],hvy[6], inv)
    thumby.display.drawLine(hvx[3],hvy[3], hvx[7],hvy[7], inv)
    
# Set the FPS (without this call, the default fps is 30)
thumby.display.setFPS(60)
#timer
tm=0

while(1):
    #info screen
    if tm<200:
        tm+=1
        thumby.display.fill(0) # Fill canvas to black
        thumby.display.drawText("By:3DSage", 2, 2, 1)
        thumby.display.drawText("Up:Speed",  2,12, 1)
        thumby.display.drawText("A :Invert",  2,22, 1)
        thumby.display.drawText("B :Freeze",  2,32, 1)
        thumby.display.update()
    else:
        thumby.display.fill(1-inv) # Fill canvas to black    
        #speed
        if thumby.buttonU.pressed(): rs=7
        else: rs=1
        #invert
        if thumby.buttonA.pressed(): inv=0; #top red button
        else: inv=1
        #freeze rotation
        if thumby.buttonB.pressed(): frz=1
        else: frz=0
        if thumby.buttonD.pressed(): prd=1
        else: prd=0        
        
        drawCube()
        thumby.display.update()
    
    
    
