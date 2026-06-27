import time
import thumby
import math
import random


# Graphics --------------------------------------------------------------

ppot_00 = bytearray([0,0,0,192,32,160,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,224,0,0,224,224,32,32,224,192,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,192,224,32,32,96,64,0,192,224,32,32,96,64,0,0,0,0,
           0,0,0,255,0,0,254,254,254,194,250,214,250,66,62,170,170,170,170,42,42,42,42,42,42,42,42,42,42,0,0,255,0,0,239,239,33,33,225,192,0,239,239,3,7,13,8,0,143,207,105,105,200,136,0,228,237,9,9,239,230,0,228,237,201,137,15,6,0,0,0,0,
           0,0,0,255,0,0,255,255,255,127,127,127,127,96,207,217,210,212,217,207,192,194,194,194,192,223,223,192,192,0,0,255,0,0,207,239,33,33,225,192,0,239,239,200,136,232,232,0,15,15,1,1,15,15,0,0,1,15,15,1,0,0,15,15,7,3,1,0,0,0,0,0,
           0,0,0,255,0,0,3,7,7,6,198,38,38,38,39,38,38,39,38,39,38,39,38,38,39,38,38,39,38,0,0,255,0,0,39,47,232,232,47,39,0,143,207,97,99,207,143,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,7,8,10,8,8,8,15,8,8,8,11,11,8,8,8,8,11,11,8,8,8,8,8,8,8,8,0,0,15,0,0,0,0,15,15,0,0,0,15,15,1,1,15,15,0,15,15,1,1,1,0,0,15,15,9,9,8,8,0,0,0,0,0,0,0,0,0,0,0])

ppot_01 = bytearray([0,0,0,192,32,160,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,224,0,0,224,224,32,32,224,192,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,192,224,32,32,96,64,0,192,224,32,32,96,64,0,0,0,0,
           0,0,0,255,0,0,254,254,254,194,250,214,250,66,62,170,170,170,170,42,42,42,42,42,42,42,42,42,42,0,0,255,0,0,239,239,33,33,225,192,0,239,239,3,7,13,8,0,143,207,105,105,200,136,0,228,237,9,9,239,230,0,228,237,201,137,15,6,0,0,0,0,
           0,0,0,255,0,0,255,255,255,127,127,127,127,96,207,217,212,210,217,207,192,194,194,198,192,223,223,192,192,0,0,255,0,0,207,239,33,33,225,192,0,239,239,200,136,232,232,0,15,15,1,1,15,15,0,0,1,15,15,1,0,0,15,15,7,3,1,0,0,0,0,0,
           0,0,0,255,0,0,3,7,7,6,198,38,38,38,39,38,38,39,38,39,38,39,38,38,39,38,38,39,38,0,0,255,0,0,39,47,232,232,47,39,0,143,207,97,99,207,143,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,7,8,10,8,8,8,15,8,8,8,11,11,8,8,8,8,11,11,8,8,8,8,8,8,8,8,0,0,15,0,0,0,0,15,15,0,0,0,15,15,1,1,15,15,0,15,15,1,1,1,0,0,15,15,9,9,8,8,0,0,0,0,0,0,0,0,0,0,0])

ppot_02 = bytearray([0,0,0,192,32,160,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,224,0,0,224,224,32,32,224,192,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,192,224,32,32,96,64,0,192,224,32,32,96,64,0,0,0,0,
           0,0,0,255,0,0,254,254,254,194,250,214,250,66,62,170,170,170,170,42,42,42,42,42,42,42,42,42,42,0,0,255,0,0,239,239,33,33,225,192,0,239,239,3,7,13,8,0,143,207,105,105,200,136,0,228,237,9,9,239,230,0,4,13,9,9,15,6,0,0,0,0,
           0,0,0,255,0,0,255,255,255,127,127,127,127,96,207,217,210,212,217,207,192,194,194,202,192,223,223,192,192,0,0,255,0,0,207,239,33,33,225,192,0,239,239,200,136,232,232,0,15,15,1,1,15,15,0,0,1,15,15,1,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,255,0,0,3,7,7,6,198,38,38,38,39,38,38,39,38,39,38,39,38,38,39,38,38,39,38,0,0,255,0,0,39,47,232,232,47,39,0,143,207,97,99,207,143,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,7,8,10,8,8,8,15,8,8,8,11,11,8,8,8,8,11,11,8,8,8,8,8,8,8,8,0,0,15,0,0,0,0,15,15,0,0,0,15,15,1,1,15,15,0,15,15,1,1,1,0,0,15,15,9,9,8,8,0,0,0,0,0,0,0,0,0,0,0])

ppot_03 = bytearray([0,0,0,192,32,160,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,32,0,0,224,0,0,224,224,32,32,224,192,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,192,224,32,32,96,64,0,192,224,32,32,96,64,0,0,0,0,
           0,0,0,255,0,0,254,254,254,194,250,214,250,66,62,170,170,170,170,42,42,42,42,42,42,42,42,42,42,0,0,255,0,0,239,239,33,33,225,192,0,239,239,3,7,13,8,0,143,207,105,105,200,136,0,228,237,9,9,239,230,0,4,13,9,9,15,6,0,0,0,0,
           0,0,0,255,0,0,255,255,255,127,127,127,127,96,207,217,212,210,217,207,192,194,194,210,192,223,223,192,192,0,0,255,0,0,207,239,33,33,225,192,0,239,239,200,136,232,232,0,15,15,1,1,15,15,0,0,1,15,15,1,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,255,0,0,3,7,7,6,198,38,38,38,39,38,38,39,38,39,38,39,38,38,39,38,38,39,38,0,0,255,0,0,39,47,232,232,47,39,0,143,207,97,99,207,143,0,224,224,32,32,224,192,0,224,224,32,32,32,32,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,7,8,10,8,8,8,15,8,8,8,11,11,8,8,8,8,11,11,8,8,8,8,8,8,8,8,0,0,15,0,0,0,0,15,15,0,0,0,15,15,1,1,15,15,0,15,15,1,1,1,0,0,15,15,9,9,8,8,0,0,0,0,0,0,0,0,0,0,0])

title = bytearray([0,0,0,192,96,48,120,216,252,252,252,254,254,254,254,252,252,252,248,248,240,224,192,0,0,0,248,236,196,236,188,252,252,124,124,252,252,252,252,248,240,224,0,0,0,240,120,220,140,220,244,252,252,252,252,252,244,236,248,0,0,
            0,120,255,253,255,254,255,255,255,3,1,1,0,0,1,1,3,255,255,255,255,255,127,255,248,0,255,255,255,255,255,255,255,120,120,252,255,255,255,255,255,231,192,0,0,7,31,63,63,127,255,255,255,252,248,248,240,192,0,0,0,
            0,0,1,7,31,63,63,127,255,255,254,254,252,252,254,254,255,255,119,125,56,29,207,195,0,0,255,255,255,255,255,255,255,248,248,188,239,199,239,123,63,31,207,192,0,252,252,252,252,252,252,255,223,143,223,119,127,31,199,192,0,
            0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,62,34,62,0,190,156,190,0,190,42,162,0,128,128,190,42,190,128,190,32,190,128,130,62,130,128,130,62,130,128,190,34,62,0,62,28,62,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,10,14,0,15,2,15,0,15,8,15,0,15,8,15,0,0,15,0,0,15,10,8,0,15,2,13,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

title_Mask = bytearray([0,0,192,224,240,248,252,252,254,254,254,255,255,255,255,254,254,254,252,252,248,240,224,192,0,248,252,254,254,254,254,254,254,254,254,254,254,254,254,252,248,240,224,0,240,248,252,254,254,254,254,254,254,254,254,254,254,254,252,248,0,
            120,255,255,255,255,255,255,255,255,255,3,3,1,1,3,3,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,192,7,31,63,127,127,255,255,255,255,255,253,253,249,241,193,0,0,
            0,1,7,31,63,127,127,255,255,255,255,255,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,254,254,254,254,254,255,255,255,255,255,255,255,255,255,231,192,
            0,0,0,0,0,0,0,0,1,1,1,3,3,3,127,127,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,127,127,127,127,1,1,1,1,1,1,1,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

intro_00 = bytearray([252,2,89,45,21,9,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,252,
            255,0,0,0,0,7,28,7,0,31,17,31,0,31,16,31,0,31,5,27,0,0,0,23,21,29,0,31,4,31,0,31,0,31,5,7,0,0,0,31,4,31,0,31,5,31,0,23,21,29,0,0,0,31,21,27,0,31,21,17,0,31,21,17,0,31,1,31,0,0,0,255,
            255,0,0,0,0,0,0,0,0,124,68,56,0,124,20,124,0,124,24,124,0,124,20,124,0,124,68,116,0,124,84,68,0,124,68,56,0,0,0,124,84,108,0,28,112,28,0,0,0,92,84,116,0,124,68,124,0,124,24,124,0,124,84,68,0,0,0,0,0,0,0,255,
            255,0,0,0,0,0,0,0,0,0,0,0,0,0,112,80,208,0,240,80,112,0,240,80,240,0,240,16,16,0,240,80,16,0,0,0,240,16,224,0,240,80,16,0,240,80,176,0,240,80,176,0,240,0,112,80,208,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
            63,64,128,128,128,128,128,128,128,128,128,128,128,128,129,129,129,128,129,128,128,128,129,128,129,128,129,129,129,128,129,129,129,128,128,128,129,129,128,128,129,129,129,128,129,129,129,128,129,128,129,128,129,128,129,129,129,128,129,128,129,128,128,128,128,160,144,168,180,154,64,63])

intro_01 = bytearray([252,2,89,45,21,9,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,252,
            255,0,0,0,0,0,0,16,0,16,0,1,31,1,0,31,4,31,0,31,21,17,0,0,0,23,21,29,0,1,31,1,0,31,21,17,0,31,21,17,0,31,5,27,0,31,0,31,1,31,0,31,17,29,0,0,0,31,0,23,21,29,0,0,0,0,0,0,0,0,0,255,
            255,0,0,124,84,108,0,124,20,108,0,124,68,124,0,124,16,108,0,124,84,68,0,124,4,124,0,0,0,124,20,124,0,124,4,124,0,124,68,56,0,0,0,28,112,28,0,124,68,124,0,124,64,124,0,0,0,124,68,68,0,124,20,124,0,124,4,124,0,0,0,255,
            255,0,0,0,0,0,0,0,0,0,0,0,0,0,240,16,240,0,240,16,240,0,16,240,16,0,0,0,240,16,240,0,240,80,240,0,240,0,240,0,240,0,240,16,208,0,240,80,240,0,16,240,16,0,240,80,16,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
            63,64,128,128,128,128,128,128,128,128,128,128,128,128,129,128,129,128,129,129,129,128,128,129,128,128,128,128,129,128,129,128,129,128,129,128,128,129,128,128,129,128,129,129,129,128,129,128,129,128,128,129,128,128,129,129,129,128,129,128,128,128,128,128,128,160,144,168,180,154,64,63])

intro_02 = bytearray([252,2,89,45,21,9,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,252,
            255,0,0,0,0,0,7,28,7,0,31,17,31,0,31,16,31,0,0,0,31,17,14,0,31,0,23,21,29,0,31,17,17,0,31,17,31,0,15,16,15,0,31,21,17,0,31,5,27,0,0,0,1,31,1,0,31,4,31,0,31,5,31,0,1,31,1,0,0,0,0,255,
            255,0,0,124,84,108,0,28,112,28,0,0,0,124,20,4,0,124,0,124,20,108,0,124,0,124,4,124,0,124,68,116,0,0,0,4,124,4,0,124,16,124,0,124,84,68,0,0,0,124,64,64,0,124,20,124,0,92,84,116,0,124,84,68,0,124,20,108,0,0,0,255,
            255,0,0,0,0,0,0,0,0,0,0,0,112,192,112,0,240,16,240,0,240,0,240,0,0,0,240,16,16,0,240,80,240,0,240,16,240,0,0,0,112,80,208,0,16,240,16,0,240,80,16,0,240,80,16,0,240,80,176,0,0,0,0,0,0,0,0,0,0,0,0,255,
            63,64,128,128,128,128,128,128,128,128,128,128,128,129,128,128,129,129,129,128,129,129,129,128,128,128,129,129,129,128,129,128,129,128,129,128,129,128,128,128,129,129,129,128,128,129,128,128,129,129,129,128,129,129,129,128,129,128,129,128,128,129,128,129,128,160,144,168,180,154,64,63])
            
intro_03 = bytearray([252,2,89,45,21,9,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,252,
            255,0,0,16,0,16,0,23,21,29,0,31,17,31,0,31,5,27,0,1,31,1,0,0,0,31,17,31,0,31,5,1,0,23,0,0,0,31,5,31,0,15,16,15,0,31,17,31,0,31,0,31,17,14,0,0,0,1,31,1,0,31,4,31,0,31,21,17,0,0,0,255,
            255,0,124,20,124,0,92,84,116,0,4,124,4,0,124,84,68,0,124,20,108,0,124,68,124,0,124,0,124,68,56,0,92,84,116,0,0,0,124,20,124,0,124,4,124,0,124,68,56,0,0,124,84,68,0,124,4,124,0,124,84,68,0,124,24,124,0,28,112,28,0,255,
            255,0,0,112,80,208,0,240,64,240,0,240,0,240,80,112,0,112,80,208,0,0,0,240,80,240,0,240,16,240,0,240,16,224,0,0,0,240,80,16,0,240,0,0,112,192,112,0,0,0,240,64,240,0,240,16,240,0,240,96,240,0,240,80,16,0,0,0,0,0,0,255,
            63,64,128,129,129,129,128,129,128,129,128,129,128,129,128,128,128,129,129,129,128,128,128,129,128,129,128,129,128,129,128,129,129,128,128,128,128,129,128,128,128,129,129,129,128,129,128,128,128,128,129,128,129,128,129,129,129,128,129,128,129,128,129,129,129,160,145,168,180,154,64,63])            
            
highScore_Img = bytearray([252,2,89,45,21,73,37,1,9,5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,252,
            255,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
            255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,255,
            255,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,0,255,
            63,64,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,160,144,128,132,162,144,168,180,154,64,63])

smallAsteroid = bytearray([0,24,36,82,106,84,44,24,0])
smallAsteroid_Mask = bytearray([24,60,126,255,255,254,126,60,24])

bigAsteroid_00 = bytearray([0,224,240,248,236,118,26,6,10,134,10,20,40,80,176,192,0,0,7,31,27,55,126,104,208,161,210,65,40,20,13,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
bigAsteroid_01 = bytearray([0,0,128,96,80,40,4,150,10,22,44,252,216,176,240,192,0,0,7,26,21,40,80,161,194,161,192,176,220,111,63,31,15,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
bigAsteroid_00_Mask = bytearray([224,240,248,252,254,255,255,255,255,255,255,254,252,248,248,240,192,7,31,63,63,127,255,255,255,255,255,255,127,63,31,15,3,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0])
bigAsteroid_01_Mask = bytearray([0,128,224,240,248,252,254,255,255,255,254,254,252,248,248,240,192,7,31,63,63,127,255,255,255,255,255,255,255,255,127,63,31,15,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0])

player_Img = bytearray([0,2,6,180,236,168,184,120,200,200,208,208,96,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0])
player_Mask = bytearray([2,7,255,254,254,252,252,252,252,252,248,248,240,96,0,1,3,3,1,1,1,3,1,1,1,1,0,0])

enemy_Img = bytearray([0,224,16,86,230,12,16,72,160,64,0,0,0,1,13,12,6,1,2,0,0,0])
enemy_Mask = bytearray([224,240,254,255,255,254,252,252,248,224,64,0,1,15,31,31,15,7,7,3,0,0])

bullet_Img = bytearray([0,8,42,62,50,58,46,28,0])
bullet_Mask = bytearray([8,62,127,127,127,127,127,62,28])

muzzle_00 = bytearray([60,126,255,255,255,255,126,60])
muzzle_01 = bytearray([0,60,126,126,126,126,60,0])
muzzle_02 = bytearray([0,0,24,60,60,24,0,0])          

shipParticle_00 = bytearray([0,4,2,0,4,6,0,4,0])
shipParticle_01 = bytearray([0,2,0,4,6,0,4,0])
shipParticle_00_Mask = bytearray([4,14,7,6,14,15,6,14,4])
shipParticle_01_Mask = bytearray([2,7,6,14,15,6,14,4])

number_00 = bytearray([31,17,31])
number_01 = bytearray([18,31,16])
number_02 = bytearray([29,21,23])
number_03 = bytearray([21,21,31])
number_04 = bytearray([7,4,31])
number_05 = bytearray([23,21,29])
number_06 = bytearray([31,21,29])
number_07 = bytearray([1,29,3])
number_08 = bytearray([31,21,31])
number_09 = bytearray([23,21,31])

shield = bytearray([0,30,60,62,60,30,0,0,28,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,34,28,0])
shield_Mask = bytearray([30,63,127,127,127,63,30,28,62,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,62,28])

puff_00 = bytearray([0,0,0,0,0,0,192,32,32,192,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0])
puff_01 = bytearray([0,0,0,0,128,96,16,16,48,32,192,0,0,0,0,0,0,0,0,1,2,2,4,4,2,1,0,0,0,0])
puff_02 = bytearray([0,192,32,24,36,4,2,2,2,10,4,4,8,240,0,0,3,4,8,8,20,32,32,32,33,18,12,2,1,0])
puff_03 = bytearray([0,0,128,152,36,36,18,12,0,8,20,34,18,12,0,0,3,4,8,9,6,0,12,18,33,18,12,0,1,0])
puff_04 = bytearray([0,0,12,18,26,4,0,0,0,4,10,18,18,12,0,0,6,9,17,10,4,0,0,0,8,20,34,18,12,0])
puff_05 = bytearray([0,0,2,6,0,0,0,0,0,0,0,6,10,12,0,0,12,20,24,0,0,0,0,0,0,16,40,16,0,0])
puff_06 = bytearray([0,2,0,0,0,0,0,0,0,0,0,0,2,4,0,0,8,16,0,0,0,0,0,0,0,0,0,0,32,0])
            
puff_00_Mask = bytearray([0,0,0,0,0,192,224,240,240,224,192,0,0,0,0,0,0,0,0,0,0,1,3,3,1,0,0,0,0,0])
puff_01_Mask = bytearray([0,0,0,128,224,240,248,248,248,240,224,192,0,0,0,0,0,0,1,3,7,7,15,15,7,3,1,0,0,0])
puff_02_Mask = bytearray([192,224,248,252,254,254,255,255,255,255,254,254,252,248,240,3,7,15,31,31,63,127,127,127,127,63,31,15,3,1])
puff_03_Mask = bytearray([0,128,216,252,254,126,63,30,12,156,62,127,63,158,12,3,7,15,31,31,15,14,30,63,127,63,30,13,3,1])
puff_04_Mask = bytearray([0,12,158,191,63,30,4,0,4,14,31,63,63,30,12,6,15,31,63,31,14,4,0,8,28,62,127,63,30,12])
puff_05_Mask = bytearray([0,2,7,15,6,0,0,0,0,0,7,15,31,30,28,14,30,62,60,56,0,0,0,0,16,56,124,56,16,0])            
puff_06_Mask = bytearray([2,7,2,0,0,0,0,0,0,0,0,2,7,14,4,8,28,56,16,0,0,0,0,0,0,0,0,32,112,32])

hit_00 = bytearray([0,0,32,4,32,80,0,0,0,1,0,0])
hit_01 = bytearray([0,32,2,32,136,0,0,0,2,0,0,0])
hit_02 = bytearray([32,1,0,0,0,0,0,4,0,0,0,0])

ppot = [ppot_00, ppot_01, ppot_02, ppot_03]
number_Sprite = [number_00, number_01, number_02, number_03, number_04, number_05, number_06, number_07, number_08, number_09]

puff        = [puff_00, puff_01, puff_02, puff_03, puff_04, puff_05, puff_06]
puff_Mask   = [puff_00_Mask, puff_01_Mask, puff_02_Mask, puff_03_Mask, puff_04_Mask, puff_05_Mask, puff_06_Mask]

hit = [hit_00, hit_01, hit_02]


# Constants --------------------------------------------------------------

CONSTANTS_Enemy_Path_Large =  [15, 14, 13, 11, 10, 8, 7, 6, 5, 4, 3, 3, 2, 2, 2, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 25, 26, 26, 26, 27, 27, 27, 27, 27, 26, 26, 26, 25, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16]
CONSTANTS_Enemy_Path_Medium = [8, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 9, 10, 10, 11, 11, 11, 11, 10, 10, 9, 9, 8, 7]
CONSTANTS_Enemy_Path_Small =  [4, 3, 3, 2, 2, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 7, 8, 8, 8, 7, 7, 6, 5]

CONSTANTS_xOffsets = [ -1, 0, 1, 0 ]
CONSTANTS_yOffsets = [ 0, -1, 0, 1 ]

CONSTANTS_BulletNone = 255
CONSTANTS_Health_Factor = 8
CONSTANTS_ScoreDistance = 96
  
CONSTANTS_Player_X = 5

DIRECTION_Up = -1
DIRECTION_None = 0
DIRECTION_Down = 1

MOTION_Slow = 0
MOTION_Fast = 1

PATH_Small = 0
PATH_Medium = 1
PATH_Large = 2

GAMESTATE_SplashScreen_Init = 1
GAMESTATE_SplashScreen = 2
GAMESTATE_TitleScreen_Init = 3
GAMESTATE_TitleScreen = 4
GAMESTATE_Game_Init = 5
GAMESTATE_Game = 6
GAMESTATE_Score_Init = 7
GAMESTATE_Score = 8

HITOBJECT_None = 0
HITOBJECT_LargeAsteroid = 1
HITOBJECT_Enemy = 2


# Classes --------------------------------------------------------------

class Rect:
    
    def __init__(self, x, y, w, h):
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Bullet:

    def __init__(self):
        
        self.sprite = thumby.Sprite(9, 7, bullet_Img)
        self.mask = thumby.Sprite(9, 7, bullet_Mask)
        
        self.muzzle_00_Sprite = thumby.Sprite(8, 8, muzzle_00)
        self.muzzle_01_Sprite = thumby.Sprite(8, 8, muzzle_01)
        self.muzzle_02_Sprite = thumby.Sprite(8, 8, muzzle_02)
        self.muzzle = [self.muzzle_00_Sprite, self.muzzle_01_Sprite, self.muzzle_02_Sprite]

        self.x = 0
        self.y = 0
        self.hitCount = 0
        self.muzzleIndex = 0
        self.hitObject = HITOBJECT_None
    
    def reset(self):
        
        self.x = -1
        self.hitCount = 0
        self.hitObject = HITOBJECT_None

    def render(self, xOffset, yOffset):

        self.sprite.x = self.x + xOffset
        self.mask.x =   self.x + xOffset
        self.sprite.y = self.y + yOffset
        self.mask.y =   self.y + yOffset

        thumby.display.drawSpriteWithMask(self.sprite, self.mask)

    def renderMuzzle(self, xOffset, yOffset):

        index = int(3 - (self.muzzleIndex / 2))
        
        self.muzzle_00_Sprite.x = self.x + xOffset
        self.muzzle_01_Sprite.x = self.x + xOffset
        self.muzzle_02_Sprite.x = self.x + xOffset
        self.muzzle_00_Sprite.y = self.y + yOffset
        self.muzzle_01_Sprite.y = self.y + yOffset
        self.muzzle_02_Sprite.y = self.y + yOffset

        thumby.display.drawSpriteWithMask(self.muzzle[index], self.muzzle[index])

    def getRect(self, margin):
        
        return Rect(self.x - margin, self.y - margin, 9 + (2 * margin), 7 + (2 * margin))


class Bullets:

    def __init__(self):
        
        self.bullets = [Bullet(), Bullet()]

    def reset(self):

        for bullet in self.bullets:
            bullet.reset()

    def getInactiveBullet(self):

        for i, bullet in enumerate(self.bullets):

            if bullet.x == -1:
                return i

        return CONSTANTS_BulletNone


class Player:

    def __init__(self):
        
        self.sprite = thumby.Sprite(14, 10, player_Img)
        self.mask = thumby.Sprite(14, 10, player_Mask)

        self.particle_00 = thumby.Sprite(8, 4, shipParticle_00)
        self.particle_01 = thumby.Sprite(8, 4, shipParticle_01)
        self.particle_00_Mask = thumby.Sprite(8, 4, shipParticle_00_Mask)
        self.particle_01_Mask = thumby.Sprite(8, 4, shipParticle_01_Mask)

        self.y = 13
        self.score = 0
        self.health = (16 * CONSTANTS_Health_Factor) - 1
        self.explodeCounter = 0
        self.direction = DIRECTION_None
        
    def updateExplosion(self):

        if self.explodeCounter > 0:

            self.explodeCounter = self.explodeCounter - 1

            if self.explodeCounter == 0:
                return True

        return False

    def reset(self):
        
        self.y = 13
        self.score = 0
        self.health = (16 * CONSTANTS_Health_Factor) - 1
        self.explodeCounter = 0
        self.direction = DIRECTION_None

    def render(self, frameCount, xOffset, yOffset):
        
        self.sprite.x = CONSTANTS_Player_X + xOffset
        self.mask.x =   CONSTANTS_Player_X + xOffset
        self.sprite.y = self.y + yOffset
        self.mask.y =   self.y + yOffset

        self.particle_00.x = CONSTANTS_Player_X - 7 + xOffset
        self.particle_01.x = CONSTANTS_Player_X - 7 + xOffset
        self.particle_00_Mask.x = CONSTANTS_Player_X - 7 + xOffset
        self.particle_01_Mask.x = CONSTANTS_Player_X - 7 + xOffset
        
        self.particle_00.y = self.y + 3 + yOffset
        self.particle_01.y = self.y + 3 + yOffset
        self.particle_00_Mask.y = self.y + 3 + yOffset
        self.particle_01_Mask.y = self.y + 3 + yOffset

        thumby.display.drawSpriteWithMask(self.sprite, self.mask)

        if frameCount % 8 < 4:
            thumby.display.drawSpriteWithMask(self.particle_00, self.particle_00_Mask)

        else:
            thumby.display.drawSpriteWithMask(self.particle_01, self.particle_01_Mask)

    def getRect(self, margin):
        
        return Rect(CONSTANTS_Player_X - margin, self.y - margin, 14 + (2 * margin), 10 + (2 * margin))


class Enemy:

    def __init__(self):
        
        self.sprite = thumby.Sprite(11, 13, enemy_Img)
        self.mask = thumby.Sprite(11, 13, enemy_Mask)
        self.x = 0
        self.y = 0
        self.active = False
        self.path = PATH_Small
        self.motion = MOTION_Slow
        self.pathCount = 0
        self.yOffset = 0
        self.explodeCounter = 0
        
    def updateExplosion(self):

        if self.explodeCounter > 0:

            self.explodeCounter = self.explodeCounter - 1

            if self.explodeCounter == 0:

                self.explodeCounter = 0
                return True

        return False

    def getActive(self):

        return self.active


    def render(self, xOffset, yOffset):

        self.sprite.x = self.x + xOffset
        self.mask.x =   self.x + xOffset
        self.sprite.y = self.y + yOffset
        self.mask.y =   self.y + yOffset
        
        thumby.display.drawSpriteWithMask(self.sprite, self.mask)

    def getRect(self, margin):
        
        return Rect(self.x - margin, self.y - margin, 11 + (2 * margin), 13 + (2 * margin))
   

class SplashScreenVars:

    def __init__(self):
        
        self.counter = 0
        self.framesPerImage = 12

    def reset(self):
        
        self.counter = 0
        
    def incCounter(self):
        
        self.counter = self.counter + 1
        if self.counter == self.framesPerImage * 4:
            self.counter = 0
        
    def imgIndex(self):
        
        return int(self.counter / self.framesPerImage)


class TitleScreenVars:

    def __init__(self):
        
        self.counter = 0
        self.introSeen = False

    def reset(self):
        
        self.counter = 0
        
    def incCounter(self):
        
        self.counter = self.counter + 1


class Star:

    def __init__(self):
        
        self.x = 0
        self.y = 0
        
    def setX(self, x):
        
        self.x = x
        
    def setY(self, y):
        
        self.y = y

    def render(self):
        
        thumby.display.setPixel(self.x, self.y, 1)


class SmallAsteroid:

    def __init__(self):
        
        self.sprite = thumby.Sprite(9, 8, smallAsteroid)
        self.mask = thumby.Sprite(9, 8, smallAsteroid_Mask)
        self.x = 0
        self.y = 0
        
    def setX(self, x):
        
        self.x = x
        
    def setY(self, y):
        
        self.y = y

    def render(self, xOffset, yOffset):

        self.sprite.x = self.x + xOffset
        self.mask.x =   self.x + xOffset
        self.sprite.y = self.y + yOffset
        self.mask.y =   self.y + yOffset
        
        thumby.display.drawSpriteWithMask(self.sprite, self.mask)
        
    def getRect(self, margin):
        return Rect(self.x - margin, self.y - margin, 9 + (2 * margin), 8 + (2 * margin))


class LargeAsteroid:

    def __init__(self):
        
        self.sprite = thumby.Sprite(17, 17, bigAsteroid_00)
        self.mask = thumby.Sprite(17, 17, bigAsteroid_00_Mask)
        self.x = 0
        self.y = 0
        self.type = 0

    def setType(self, type):
        
        self.type = type
        
        if type == 0:
            self.sprite = thumby.Sprite(17, 17, bigAsteroid_00)
            self.mask = thumby.Sprite(17, 17, bigAsteroid_00_Mask)
            
        else:
            self.sprite = thumby.Sprite(17, 17, bigAsteroid_01)
            self.mask = thumby.Sprite(17, 17, bigAsteroid_01_Mask)

    def setX(self, x):
        
        self.x = x
        
    def setY(self, y):
        
        self.y = y

    def render(self, xOffset, yOffset):

        self.sprite.x = self.x + xOffset
        self.mask.x =   self.x + xOffset
        self.sprite.y = self.y + yOffset
        self.mask.y =   self.y + yOffset
        
        thumby.display.drawSpriteWithMask(self.sprite, self.mask)
        
    def getRect_Full(self, margin):
        
        return Rect(self.x - margin, self.y - margin, 17 + (2 * margin), 17 + (2 * margin))
        
    def getRect_00(self):
        
        return Rect(self.x + 1, self.y + 6, 15, 7)
        
    def getRect_01(self):
        
        return Rect(self.x + 5, self.y + 1, 6, 15)
        
    def getRect_02(self):
        
        return Rect(self.x + 3, self.y + 3, 9, 9)
    
    
# Global Vars ----------------------------------------------------------

smallAsteroids = [SmallAsteroid(),
                  SmallAsteroid(),
                  SmallAsteroid(),
                  SmallAsteroid()]
        
largeAsteroids = [LargeAsteroid(),
                  LargeAsteroid()]

starfield = [Star(), 
             Star(),
             Star(),
             Star(),
             Star(),
             Star(),
             Star(),
             Star(),
             Star(),
             Star()]

bullets = Bullets()
player = Player()
enemies = [Enemy(), 
           Enemy(),
           Enemy()]
           
gameState = GAMESTATE_SplashScreen_Init
splashScreenVars = SplashScreenVars()
titleScreenVars = TitleScreenVars()

frameCount = 0
clearScores = 0
xOffset = 0
yOffset = 0
offsetCount = 0
gameState = GAMESTATE_SplashScreen_Init


# Game Functions ----------------------------------------------------------

def collide(rect1, rect2):

    if rect2.x >= rect1.x + rect1.w:
        return False
        
    if rect2.x + rect2.w <= rect1.x:
        return False

    if rect2.y >= rect1.y + rect1.h:
        return False
        
    if rect2.y + rect2.h <= rect1.y:
        return False

    return True


def checkBulletCollision(bullet):

    bulletRect = bullet.getRect(-1)


    # Has the bullet hit a large asteroid?

    for largeAsteroid in largeAsteroids:

        asterRect_00 = largeAsteroid.getRect_00()       # Horizontal
        asterRect_01 = largeAsteroid.getRect_01()       # Vertical
        asterRect_02 = largeAsteroid.getRect_02()       # Square

        if collide(bulletRect, asterRect_00) or collide(bulletRect, asterRect_01) or collide(bulletRect, asterRect_02):
            bullet.hitObject = HITOBJECT_LargeAsteroid
            bullet.hitCount = 1
            bullet.muzzleIndex = 0
            bullet.x = largeAsteroid.x - 4


    # Has the bullet hit an enemy?

    for enemy in enemies:

        enemyRect = enemy.getRect(-1)
        
        if enemy.active and collide(bulletRect, enemyRect):

            bullet.hitObject = HITOBJECT_Enemy
            bullet.hitCount = 1
            bullet.muzzleIndex = 0
            bullet.x = enemy.x - 4

            enemy.explodeCounter = 21
            enemy.active = False
            player.score = player.score + 5

            thumby.display.setFPS(50 + (player.score / 24))
            thumby.audio.play(3000, 50)           


def launchEnemy(enemy):

    while True:

        enemy.x = 72 + random.randint(0, 96)
        enemy.y = random.randint(0, 22)
        enemy.pathCount = random.randint(6, 11)
        enemy.motion = random.randint(0, 1)
        enemy.path = random.randint(1, 2)
        enemy.active = True

        if enemy.path == PATH_Large:
            enemy.yOffset = 0
        
        elif enemy.path == PATH_Medium:
            enemy.yOffset = random.randint(0, 9)
        
        elif enemy.path == PATH_Small:
            enemy.yOffset = random.randint(0, 19)


        enemy_Rect = enemy.getRect(-1)
        collision = False


        # Check for overlap with large asteroids ..
        
        for largeAsteroid in largeAsteroids:

            asterRect_00 = largeAsteroid.getRect_00()       # Horizontal
            asterRect_01 = largeAsteroid.getRect_01()       # Vertical
            asterRect_02 = largeAsteroid.getRect_02()       # Square

            if collide(enemy_Rect, asterRect_00) or collide(enemy_Rect, asterRect_01) or collide(enemy_Rect, asterRect_02):

                collision = True
                break


        # Check for overlap with other enemies ..
        
        if collision == False:
            
            for enemy2 in enemies:

                if enemy.x != enemy2.x or enemy.y != enemy2.y:

                    enemy_Rect2 = enemy2.getRect(2)

                    if collide(enemy_Rect, enemy_Rect2):

                        collision = True
                        break

        if collision == False:
            break                    


def launchLargeAsteroid(asteroid):

    while (True):

        asteroid.setX(72 + random.randint(0, 96))
        asteroid.setY(random.randint(0, 21))
        asteroid.type = random.randint(0, 1)

        asteroid1_Rect = asteroid.getRect_Full(0)
        collision = False

        for largeAsteroid in largeAsteroids:

            if (asteroid.x != largeAsteroid.x or asteroid.y != largeAsteroid.y):

                asteroid2_Rect = largeAsteroid.getRect_Full(4)

                if collide(asteroid1_Rect, asteroid2_Rect):

                    collision = True
                    break


        if (collision == False):
            break              


def moveRenderStarfield():

    for star in starfield:

        if (frameCount % 6 == 0):

            star.setX(star.x - 1)

            if star.x == -1:
                star.setX(72)
                star.setY(random.randint(0, 40))

        star.render()


def moveRenderSmallAsteroids(alternate, xOffset, yOffset):

    for i, smallAsteroid in enumerate(smallAsteroids):

        if (frameCount % 3 == 0):

            smallAsteroid.setX(smallAsteroid.x - 1)

            if smallAsteroid.x == -9:
                smallAsteroid.setX(72 + random.randint(0, 96))
                smallAsteroid.setY(random.randint(0, 32))

        if (alternate == False or (i % 2 == 0)):
            smallAsteroid.render(xOffset, yOffset)


def moveRenderLargeAsteroids(alternate, xOffset, yOffset):

    for i, largeAsteroid in enumerate(largeAsteroids):

        if (frameCount % 2 == 0):

            largeAsteroid.setX(largeAsteroid.x - 1)

            if largeAsteroid.x == -19:
                launchLargeAsteroid(largeAsteroid)

        if (alternate == False or (i % 2 == 0)):
            largeAsteroid.render(xOffset, yOffset)



# Splash Screen ----------------------------------------------------------

def splashScreen_Init():

    global gameState 

    splashScreenVars.reset()
    gameState = GAMESTATE_SplashScreen


def splashScreen():
    
    global gameState 
    
    splashScreenVars.incCounter()
    thumby.display.blit(ppot[splashScreenVars.imgIndex()], 0, 0, 72, 40, 0, False, False)

    if thumby.buttonA.justPressed() == True:
        gameState = GAMESTATE_TitleScreen_Init
    
    if thumby.buttonB.justPressed() == True:
        gameState = GAMESTATE_TitleScreen_Init


# Title Screen ----------------------------------------------------------

def titleScreen_Init():
    
    global gameState 

    titleScreenVars.reset()
    thumby.display.setFPS(50)

    gameState = GAMESTATE_TitleScreen
    
    for smallAsteroid in smallAsteroids:
        smallAsteroid.setX(random.randint(0, 128))
        smallAsteroid.setY(random.randint(0, 32))

    for star in starfield:
        star.setX(random.randint(0, 128))
        star.setY(random.randint(0, 32))

    for largeAsteroid in largeAsteroids:
        launchLargeAsteroid(largeAsteroid)


def titleScreen():
    
    global gameState 
    
    if titleScreenVars.counter == 0:
        moveRenderStarfield()
        moveRenderSmallAsteroids(True, 0, 0)
        moveRenderLargeAsteroids(True, 0, 0)
        thumby.display.blitWithMask(title, 5, 1, 61, 37, 0, False, False, title_Mask)

    if titleScreenVars.counter == 1:
        thumby.display.blit(intro_00, 0, 0, 72, 40, 0, False, False)

    if titleScreenVars.counter == 2:
        thumby.display.blit(intro_01, 0, 0, 72, 40, 0, False, False)

    if titleScreenVars.counter == 3:
        thumby.display.blit(intro_02, 0, 0, 72, 40, 0, False, False)

    if titleScreenVars.counter == 4:
        thumby.display.blit(intro_03, 0, 0, 72, 40, 0, False, False)

    if thumby.buttonA.justPressed() or thumby.buttonB.justPressed():
        titleScreenVars.incCounter()

    if titleScreenVars.counter == 5 or (titleScreenVars.introSeen and titleScreenVars.counter == 1):
        gameState = GAMESTATE_Game_Init
        titleScreenVars.introSeen = True
    


# Game Play ----------------------------------------------------------

def game_Init():
    
    global gameState 
    global bullets
    global player
    global offsetCount
    global xOffset
    global yOffset
    
    gameState = GAMESTATE_Game
    xOffset = 0
    yOffset = 0
    offsetCount = 0

    for smallAsteroid in smallAsteroids:
        smallAsteroid.setX(random.randint(0, 128))
        smallAsteroid.setY(random.randint(0, 32))

    for star in starfield:
        star.setX(random.randint(0, 128))
        star.setY(random.randint(0, 32))

    for largeAsteroid in largeAsteroids:
        launchLargeAsteroid(largeAsteroid)

    for enemy in enemies:
        launchEnemy(enemy)


    bullets.reset()
    player.reset()
    
    thumby.display.setFPS(50)
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)


def game():

    global gameState
    global bullets
    global player
    global offsetCount
    global xOffset
    global yOffset
    

    # Increase score based on distance travelled ..

    if frameCount % CONSTANTS_ScoreDistance == 0:
        player.score = player.score + 1

    player.y = player.y + player.direction

    if player.direction == DIRECTION_Up and player.y == -1:
        player.direction = DIRECTION_None

    if player.direction == DIRECTION_Down and player.y == 31:
        player.direction = DIRECTION_None


    # Launch a bullet if we can ..

    if thumby.buttonA.justPressed() or thumby.buttonB.justPressed() or thumby.buttonL.justPressed() or thumby.buttonR.justPressed() or thumby.buttonU.justPressed() or thumby.buttonD.justPressed():

        bulletIdx = bullets.getInactiveBullet()

        if bulletIdx != CONSTANTS_BulletNone:

            bullet = bullets.bullets[bulletIdx]

            if player.direction == DIRECTION_Up:
                player.direction = DIRECTION_Down

            elif player.direction == DIRECTION_Down:
                player.direction = DIRECTION_Up

            else:

                if player.y == -1:
                    player.direction = DIRECTION_Down

                elif player.y == 31:
                    player.direction = DIRECTION_Up

                else: 
                    if random.randint(0, 1) == 0:
                        player.direction = DIRECTION_Up
                        
                    else:
                        player.direction = DIRECTION_Down

            bullet.x = CONSTANTS_Player_X + 13
            bullet.y = player.y + 2
            bullet.muzzleIndex = 8

            thumby.audio.play(5000, 50)
            bullet.hitObject = HITOBJECT_None

    
    # Update any hit and muzzle flash counters for the bullets ..
    
    for bullet in bullets.bullets:
            
        if bullet.hitCount > 0:

            bullet.hitCount = bullet.hitCount + 1

            if bullet.hitCount > 3:
                bullet.reset()

        if  bullet.x > 0 and bullet.hitCount == 0:

            if bullet.muzzleIndex > 0:

                bullet.muzzleIndex = bullet.muzzleIndex - 1

            else:

                bullet.x = bullet.x + 4

                if bullet.x >= 72:
                    bullet.x = -1

            if bullet.x != -1:
                checkBulletCollision(bullet)

        if bullet.hitObject == HITOBJECT_LargeAsteroid:

            bullet.x = bullet.x - 1



    # Has the player hit a asteroid?

    collision = False
    playerRect = player.getRect(-1)

    for largeAsteroid in largeAsteroids:

        asteroidRect_00 = largeAsteroid.getRect_00()    # horizontal
        asteroidRect_01 = largeAsteroid.getRect_01()    # vertical
        asteroidRect_02 = largeAsteroid.getRect_02()    # square
        
        if collide(playerRect, asteroidRect_00) or collide(playerRect, asteroidRect_01) or collide(playerRect, asteroidRect_02):

            if player.health > 0:
                
                player.health = player.health - 1
                thumby.audio.play(6000, 10)
                
                if player.health == 0:
                    player.explodeCounter = 21
                    thumby.audio.play(4000, 10)       

            collision = True
            break


    if collision:

        offsetCount = offsetCount + 1

        if offsetCount > 4:
            offsetCount = 1

        xOffset = CONSTANTS_xOffsets[offsetCount - 1]
        yOffset = CONSTANTS_yOffsets[offsetCount - 1]
        
        #invert(offsetCount % 2)

    else:


        # Has the player hit an enemy ?

        for enemy in enemies:

            if enemy.getActive():

                enemyRect = enemy.getRect(-1)
                
                if collide(playerRect, enemyRect):
    
                    if player.health > 0:
                        
                        player.health = player.health - 1
                        thumby.audio.play(6000, 10)
        
                        if player.health == 0:
                            player.explodeCounter = 21
                            thumby.audio.play(4000, 10)
    
                    collision = True
                    break

        if collision:
            
            offsetCount = offsetCount + 1
    
            if offsetCount > 4:
                offsetCount = 1

            xOffset = CONSTANTS_xOffsets[offsetCount - 1]
            yOffset = CONSTANTS_yOffsets[offsetCount - 1]
            
#           invert(offsetCount % 2)

            pass

        else:
            
            offsetCount = 0
            xOffset = 0
            yOffset = 0
#           invert(false)
            pass


    # Move and render starfield  / asteroids ..

    moveRenderStarfield()
    moveRenderSmallAsteroids(False, xOffset, yOffset)
    moveRenderLargeAsteroids(False, xOffset, yOffset)


    # Move and render enemies ..

    for enemy in enemies:

        if enemy.motion == MOTION_Slow:

            if frameCount % 2 == 0:
                
                if enemy.path == PATH_Small:

                    enemy.pathCount = enemy.pathCount + 1
                    if enemy.pathCount == 24:
                        enemy.pathCount = 0

                    enemy.x = enemy.x - 1                    
                    enemy.y = CONSTANTS_Enemy_Path_Small[enemy.pathCount] + enemy.yOffset

                elif enemy.path == PATH_Medium:

                    enemy.pathCount = enemy.pathCount + 1
                    if enemy.pathCount == 36:
                        enemy.pathCount = 0

                    enemy.x = enemy.x - 1                    
                    enemy.y = CONSTANTS_Enemy_Path_Medium[enemy.pathCount] + enemy.yOffset

                elif enemy.path == PATH_Large:

                    enemy.pathCount = enemy.pathCount + 1
                    if enemy.pathCount == 70:
                        enemy.pathCount = 0

                    enemy.x = enemy.x - 1                    
                    enemy.y = CONSTANTS_Enemy_Path_Large[enemy.pathCount] + enemy.yOffset

        if enemy.motion == MOTION_Fast:

            if frameCount % 3 < 2:
                
                if enemy.path == PATH_Small:

                    enemy.pathCount = enemy.pathCount + 1
                    if enemy.pathCount == 24:
                        enemy.pathCount = 0

                    enemy.x = enemy.x - 1                    
                    enemy.y = CONSTANTS_Enemy_Path_Small[enemy.pathCount] + enemy.yOffset

                elif enemy.path == PATH_Medium:

                    enemy.pathCount = enemy.pathCount + 1
                    if enemy.pathCount == 36:
                        enemy.pathCount = 0

                    enemy.x = enemy.x - 1                    
                    enemy.y = CONSTANTS_Enemy_Path_Medium[enemy.pathCount] + enemy.yOffset

                elif enemy.path == PATH_Large:

                    enemy.pathCount = enemy.pathCount + 1
                    if enemy.pathCount == 70:
                        enemy.pathCount = 0

                    enemy.x = enemy.x - 1                    
                    enemy.y = CONSTANTS_Enemy_Path_Large[enemy.pathCount] + enemy.yOffset


        # If enemy has moved off left of screen ..

        if enemy.x == -19:
            launchEnemy(enemy)


        # Render enemy ..
        
        if enemy.getActive() or enemy.explodeCounter > 16:
            enemy.render(xOffset, yOffset)

        if enemy.explodeCounter > 0:
            thumby.display.blitWithMask(puff[int((21 - enemy.explodeCounter) / 3)], enemy.x + xOffset - 3, enemy.y + yOffset, 15, 15, 0, False, False, puff_Mask[int((21 - enemy.explodeCounter) / 3)])

        if enemy.updateExplosion():
            launchEnemy(enemy)


    # Render player ..

    if player.health > 0 or player.explodeCounter > 16:
        player.render(frameCount, xOffset, yOffset)

    if player.explodeCounter > 0:
        thumby.display.blitWithMask(puff[int((21 - player.explodeCounter) / 3)], 6, player.y + yOffset, 15, 15, 0, False, False, puff_Mask[int((21 - player.explodeCounter) / 3)])

    if player.updateExplosion():
        gameState = GAMESTATE_Score_Init


    # Render player bullets ..
    
    for bullet in bullets.bullets:
                                
        if bullet.x > 0:
                
            if bullet.muzzleIndex > 1:
                bullet.renderMuzzle(xOffset, yOffset)
                pass

            else:

                if bullet.hitCount == 0:
                    bullet.render(xOffset, yOffset)

                else:
                    thumby.display.blit(hit[bullet.hitCount - 1], bullet.x + xOffset, bullet.y - 5 + yOffset, 6, 12, 0, False, False)


    # Render the HUD ..

    thumby.display.drawFilledRectangle(51, 0, 22, 6, 0)
    health_Bar = int(player.health / CONSTANTS_Health_Factor)

    score = player.score
    digit = int(score / 10000)
    thumby.display.blit(number_Sprite[digit], 52, 0, 3, 5, 0, False, False)

    score = score - (digit * 10000)
    digit = int(score / 1000)
    thumby.display.blit(number_Sprite[digit], 56, 0, 3, 5, 0, False, False)

    score = score - (digit * 1000)
    digit = int(score / 100)
    thumby.display.blit(number_Sprite[digit], 60, 0, 3, 5, 0, False, False)

    score = score - (digit * 100)
    digit = int(score / 10)
    thumby.display.blit(number_Sprite[digit], 64, 0, 3, 5, 0, False, False)

    score = score - (digit * 10)
    thumby.display.blit(number_Sprite[score], 68, 0, 3, 5, 0, False, False)

    thumby.display.blitWithMask(shield, 44, 34, 28, 7, 0, False, False, shield_Mask)
    thumby.display.drawLine(54, 37, 54 + health_Bar, 37, 1)



# Scores ----------------------------------------------------------

def highScore_Init():
    
    global gameState 

    gameState = GAMESTATE_Score
    thumby.display.setFPS(50)


def highScore():

    global gameState
    global clearScores
    global player

    if thumby.buttonA.justPressed() or thumby.buttonB.justPressed() or thumby.buttonL.justPressed() or thumby.buttonR.justPressed() or thumby.buttonU.justPressed() or thumby.buttonD.justPressed():
        gameState = GAMESTATE_TitleScreen_Init
        
    
    score = str(player.score)
    
    while len(score) < 5:
        score = "0" +score

    thumby.display.blit(highScore_Img, 0, 0, 72, 40, 0, False, False)
    thumby.display.drawText("Score", 21, 10, 1)
    thumby.display.drawText(score, 21, 21, 1)


    
# Main Loop -------------------------------------------------------------

thumby.display.setFPS(50)
random.seed(time.ticks_us())

while (True):

    frameCount = frameCount + 1
    if frameCount > 1024:
        frameCount = 0
        
    thumby.display.fill(0) 

    if gameState == GAMESTATE_SplashScreen_Init:
        splashScreen_Init()

    if gameState == GAMESTATE_SplashScreen:
        splashScreen()

    if gameState == GAMESTATE_TitleScreen_Init:
        titleScreen_Init()

    if gameState == GAMESTATE_TitleScreen:
        titleScreen()

    if gameState == GAMESTATE_Game_Init:
        game_Init()

    if gameState == GAMESTATE_Game:
        game()

    if gameState == GAMESTATE_Score_Init:
        highScore_Init()

    if gameState == GAMESTATE_Score:
        highScore()


    thumby.display.update()

