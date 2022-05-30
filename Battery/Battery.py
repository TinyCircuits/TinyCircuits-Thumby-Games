#Battery charge level indicator by @AyreGuitar 30/5/2022
#
#Based on code posted by:
#@JasonTC from Discord channel https://discord.com/channels/898292107289190461/898292174410612787/972253183814541342
#@TPReal from Discord channel https://discord.com/channels/898292107289190461/898292174410612787/975659380232060978 
#
#v1.2.1
#Changelog:
#Better initial calibration values
#Smoother icon changes - doesn't flick between 2 states if voltage near threshold level
#
#Disclaimer:
#Use at your own risk, no warranties or guarantees

import thumby
from machine import ADC

adc = ADC(26)

#40000 Maybe an OK value (for plugged in and charging)?
#40000 too high, says Not charging when connected
#roughly calibrated on hi brightness - feel free to calibrate yourself
charging = 38000
#level_0 = 32000 #~70min shuts off never used
level_1 = 33700 #~45min
level_2 = 34300 #~30min
level_3 = 35400 #~15min

# BITMAP: width: 11, height: 5
batt0 = bytearray([31,17,17,17,17,17,17,17,17,27,14])
batt1 = bytearray([31,31,31,31,17,17,17,17,17,27,14])
batt2 = bytearray([31,31,31,31,31,31,31,17,17,27,14])
batt3 = bytearray([31,31,31,31,31,31,31,31,31,31,14])
charg = bytearray([31,31,27,27,9,0,18,27,27,31,14])
emula = bytearray([31,21,17,0,31,2,31,0,31,16,31])

iconx = 61
icony = 0
iconw = 11
iconh = 5
b=charging

thumby.display.setFPS(5)
while (not thumby.buttonA.pressed()):
    thumby.display.fill(0)
    in_emu=not hasattr(thumby.display.display,"cs")
    if (in_emu):
        thumby.display.blit(emula,iconx,icony,iconw,iconh,-1,0,0)
    else:
        v=adc.read_u16()
        b=min(b,v)
        if (v > charging):
            thumby.display.blit(charg,iconx,icony,iconw,iconh,-1,0,0)
            b=v
        else:
            if (b > level_3):
                thumby.display.blit(batt3,iconx,icony,iconw,iconh,-1,0,0)
            elif (b > level_2):
                thumby.display.blit(batt2,iconx,icony,iconw,iconh,-1,0,0)
            elif (b > level_1):
                thumby.display.blit(batt1,iconx,icony,iconw,iconh,-1,0,0)
            else:
                thumby.display.blit(batt0,iconx,icony,iconw,iconh,-1,0,0)
        if (thumby.buttonB.pressed()):
            thumby.display.drawText("v=%d" % b, 0, 0, 1)
    thumby.display.update() 
