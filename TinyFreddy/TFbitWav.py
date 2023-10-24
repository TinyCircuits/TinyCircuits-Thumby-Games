import time
import thumby
import math

#this is where the magic is set up
songfrequencychart = [[16,17,18,19,21,22,23,25,26,28,29,31],[33,35,37,39,41,44,46,49,52,55,58,62],[65,69,73,78,82,87,93,98,104,110,117,123],[131,139,147,156,165,175,185,196,208,220,233,247],[262,277,294,311,330,349,370,392,415,440,466,494],[523,554,587,622,659,698,740,784,831,880,932,988],[1047,1109,1175,1245,1319,1397,1480,1568,1661,1760,1865,1976],[2093,2217,2349,2489,2637,2794,2960,3136,3322,3520,3729,3951]]

tm0 = time.ticks_ms()
tm1 = tm0
songprogress = 0
songupdateprogress = 0
songloop = 0
songloopnum = 0
songlength = 1
songbeatdivisions = 3
songtempo = 240
songnotechart = [262]*songlength*songbeatdivisions

def loadPhoneRinger():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 12
    songlength = 1
    songbeatdivisions = 3
    songtempo = 240
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = songfrequencychart[5][0]
    songnotechart[1] = songfrequencychart[5][3]
    songnotechart[2] = songfrequencychart[5][7]

def loadStinger():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 1
    songlength = 1
    songbeatdivisions = 3
    songtempo = 60
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = songfrequencychart[5][8]
    songnotechart[1] = songfrequencychart[5][8]
    songnotechart[2] = songfrequencychart[5][8]
    songnotechart[2] = songfrequencychart[5][8]

def loadLaugh():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 1
    songlength = 4
    songbeatdivisions = 4
    songtempo = 80
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = 0
    songnotechart[1] = songfrequencychart[5][0]
    songnotechart[2] = songfrequencychart[4][11]
    songnotechart[3] = 0
    songnotechart[4] = songfrequencychart[5][0]
    songnotechart[5] = songfrequencychart[5][0]
    songnotechart[6] = songfrequencychart[4][11]
    songnotechart[7] = 0
    songnotechart[8] = songfrequencychart[5][0]
    songnotechart[9] = songfrequencychart[5][1]
    songnotechart[10] = 0
    songnotechart[11] = 0
    songnotechart[12] = songfrequencychart[5][1]
    songnotechart[13] = songfrequencychart[5][1]
    songnotechart[14] = 0
    songnotechart[15] = 0

def loadDeepLaugh():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 1
    songlength = 4
    songbeatdivisions = 3
    songtempo = 30
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = 0
    songnotechart[1] = songfrequencychart[3][0]
    songnotechart[2] = songfrequencychart[2][10]
    songnotechart[3] = 0
    songnotechart[4] = songfrequencychart[3][0]
    songnotechart[5] = songfrequencychart[2][10]
    songnotechart[6] = 0
    songnotechart[7] = songfrequencychart[3][0]
    songnotechart[8] = songfrequencychart[3][2]
    songnotechart[9] = 0
    songnotechart[10] = songfrequencychart[3][2]
    songnotechart[11] = songfrequencychart[3][2]

def loadDoor():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 1
    songlength = 1
    songbeatdivisions = 4
    songtempo = 180
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = songfrequencychart[3][6]
    songnotechart[1] = songfrequencychart[3][3]
    songnotechart[2] = songfrequencychart[3][0]
    songnotechart[3] = songfrequencychart[3][0]

def loadFootSteps():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 1
    songloopnum = 6
    songlength = 1
    songbeatdivisions = 2
    songtempo = 120
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = songfrequencychart[2][7]
    songnotechart[1] = 0

def loadDoorBang():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 1
    songlength = 3
    songbeatdivisions = 2
    songtempo = 40
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = 0
    songnotechart[1] = songfrequencychart[3][4]
    songnotechart[2] = 0
    songnotechart[3] = songfrequencychart[3][4]
    songnotechart[4] = 0
    songnotechart[5] = songfrequencychart[3][4]

def loadJumpScare():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 2
    songlength = 4
    songbeatdivisions = 4
    songtempo = 480
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = songfrequencychart[5][8]
    songnotechart[1] = songfrequencychart[5][5]
    songnotechart[2] = songfrequencychart[5][9]
    songnotechart[3] = songfrequencychart[5][11]
    songnotechart[4] = songfrequencychart[5][5]
    songnotechart[5] = songfrequencychart[5][9]
    songnotechart[6] = songfrequencychart[5][7]
    songnotechart[7] = songfrequencychart[5][10]
    songnotechart[8] = songfrequencychart[5][5]
    songnotechart[9] = songfrequencychart[5][8]
    songnotechart[10] = songfrequencychart[5][11]
    songnotechart[11] = songfrequencychart[5][7]
    songnotechart[12] = songfrequencychart[5][5]
    songnotechart[13] = songfrequencychart[5][8]
    songnotechart[14] = songfrequencychart[5][10]
    songnotechart[15] = songfrequencychart[5][6]

def loadGoldenJumpScare():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 0
    songloopnum = 2
    songlength = 4
    songbeatdivisions = 4
    songtempo = 480
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    songnotechart[0] = songfrequencychart[3][8]
    songnotechart[1] = songfrequencychart[3][5]
    songnotechart[2] = songfrequencychart[3][9]
    songnotechart[3] = songfrequencychart[3][11]
    songnotechart[4] = songfrequencychart[3][5]
    songnotechart[5] = songfrequencychart[3][9]
    songnotechart[6] = songfrequencychart[3][7]
    songnotechart[7] = songfrequencychart[3][10]
    songnotechart[8] = songfrequencychart[3][5]
    songnotechart[9] = songfrequencychart[3][8]
    songnotechart[10] = songfrequencychart[3][11]
    songnotechart[11] = songfrequencychart[3][7]
    songnotechart[12] = songfrequencychart[3][5]
    songnotechart[13] = songfrequencychart[3][8]
    songnotechart[14] = songfrequencychart[3][10]
    songnotechart[15] = songfrequencychart[3][6]

def loadToreador():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 1
    songloopnum = 1
    songlength = 48
    songbeatdivisions = 4
    songtempo = 120
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    #Intro
    songnotechart[0] = songfrequencychart[4][9]
    songnotechart[1] = songfrequencychart[4][10]
    songnotechart[2] = songfrequencychart[4][11]
    songnotechart[3] = songfrequencychart[5][0]
    #Stretch1
    songnotechart[4] = songfrequencychart[5][1]
    songnotechart[5] = songfrequencychart[5][1]
    songnotechart[6] = songfrequencychart[5][1]
    songnotechart[7] = songfrequencychart[5][1]
    songnotechart[8] = songfrequencychart[5][3]
    songnotechart[9] = songfrequencychart[5][3]
    songnotechart[10] = songfrequencychart[5][3]
    songnotechart[11] = songfrequencychart[5][1]
    songnotechart[12] = songfrequencychart[4][10]
    songnotechart[13] = songfrequencychart[4][10]
    songnotechart[14] = 0
    songnotechart[15] = 0
    songnotechart[16] = songfrequencychart[4][10]
    songnotechart[17] = songfrequencychart[4][10]
    songnotechart[18] = 0
    songnotechart[19] = 0
    #Stretch2
    songnotechart[20] = songfrequencychart[4][10]
    songnotechart[21] = songfrequencychart[4][10]
    songnotechart[22] = songfrequencychart[4][8]
    songnotechart[23] = songfrequencychart[4][8]
    songnotechart[24] = songfrequencychart[4][10]
    songnotechart[25] = songfrequencychart[4][10]
    songnotechart[26] = songfrequencychart[4][11]
    songnotechart[27] = songfrequencychart[4][11]
    songnotechart[28] = songfrequencychart[4][10]
    songnotechart[29] = songfrequencychart[6][1]
    songnotechart[30] = songfrequencychart[6][4]
    songnotechart[31] = songfrequencychart[6][8]
    songnotechart[32] = songfrequencychart[7][3]
    songnotechart[33] = songfrequencychart[6][11]
    songnotechart[34] = songfrequencychart[6][8]
    songnotechart[35] = songfrequencychart[6][4]
    #Stretch3
    songnotechart[36] = songfrequencychart[4][11]
    songnotechart[37] = songfrequencychart[4][11]
    songnotechart[38] = songfrequencychart[4][11]
    songnotechart[39] = songfrequencychart[4][11]
    songnotechart[40] = songfrequencychart[4][8]
    songnotechart[41] = songfrequencychart[4][8]
    songnotechart[42] = songfrequencychart[4][8]
    songnotechart[43] = songfrequencychart[5][1]
    songnotechart[44] = songfrequencychart[4][10]
    songnotechart[45] = songfrequencychart[6][1]
    songnotechart[46] = songfrequencychart[6][4]
    songnotechart[47] = songfrequencychart[6][8]
    songnotechart[48] = songfrequencychart[7][3]
    songnotechart[49] = songfrequencychart[6][11]
    songnotechart[50] = songfrequencychart[6][8]
    songnotechart[51] = songfrequencychart[6][4]
    #Stretch4
    songnotechart[52] = songfrequencychart[4][6]
    songnotechart[53] = songfrequencychart[4][6]
    songnotechart[54] = songfrequencychart[4][6]
    songnotechart[55] = songfrequencychart[4][6]
    songnotechart[56] = songfrequencychart[4][3]
    songnotechart[57] = songfrequencychart[4][3]
    songnotechart[58] = songfrequencychart[4][3]
    songnotechart[59] = songfrequencychart[4][8]
    songnotechart[60] = songfrequencychart[4][2]
    songnotechart[61] = songfrequencychart[6][1]
    songnotechart[62] = songfrequencychart[6][4]
    songnotechart[63] = songfrequencychart[6][8]
    songnotechart[64] = songfrequencychart[6][11]
    songnotechart[65] = songfrequencychart[7][1]
    songnotechart[66] = songfrequencychart[6][11]
    songnotechart[67] = songfrequencychart[6][11]
    #Stretch5
    songnotechart[68] = songfrequencychart[4][6]
    songnotechart[69] = songfrequencychart[4][6]
    songnotechart[70] = songfrequencychart[4][6]
    songnotechart[71] = songfrequencychart[4][6]
    songnotechart[72] = songfrequencychart[4][6]
    songnotechart[73] = songfrequencychart[4][6]
    songnotechart[74] = songfrequencychart[4][6]
    songnotechart[75] = songfrequencychart[4][6]
    songnotechart[76] = songfrequencychart[4][6]
    songnotechart[77] = songfrequencychart[4][6]
    songnotechart[78] = songfrequencychart[5][1]
    songnotechart[79] = songfrequencychart[5][1]
    songnotechart[80] = songfrequencychart[4][11]
    songnotechart[81] = songfrequencychart[4][11]
    songnotechart[82] = songfrequencychart[4][9]
    songnotechart[83] = songfrequencychart[4][9]
    #Stretch6
    songnotechart[84] = songfrequencychart[4][8]
    songnotechart[85] = songfrequencychart[4][8]
    songnotechart[86] = songfrequencychart[4][6]
    songnotechart[87] = songfrequencychart[4][6]
    songnotechart[88] = songfrequencychart[4][8]
    songnotechart[89] = songfrequencychart[4][8]
    songnotechart[90] = songfrequencychart[4][9]
    songnotechart[91] = songfrequencychart[4][9]
    songnotechart[92] = songfrequencychart[4][8]
    songnotechart[93] = songfrequencychart[4][8]
    songnotechart[94] = songfrequencychart[4][8]
    songnotechart[95] = songfrequencychart[4][8]
    songnotechart[96] = 0
    songnotechart[97] = 0
    songnotechart[98] = songfrequencychart[4][4]
    songnotechart[99] = 0
    #Stretch7
    songnotechart[100] = songfrequencychart[4][4]
    songnotechart[101] = songfrequencychart[4][4]
    songnotechart[102] = songfrequencychart[4][4]
    songnotechart[103] = songfrequencychart[4][4]
    songnotechart[104] = songfrequencychart[4][9]
    songnotechart[105] = songfrequencychart[4][9]
    songnotechart[106] = 0
    songnotechart[107] = 0
    songnotechart[108] = songfrequencychart[4][9]
    songnotechart[109] = songfrequencychart[4][9]
    songnotechart[110] = songfrequencychart[4][9]
    songnotechart[111] = songfrequencychart[4][9]
    songnotechart[112] = songfrequencychart[4][8]
    songnotechart[113] = songfrequencychart[4][8]
    songnotechart[114] = songfrequencychart[4][11]
    songnotechart[115] = songfrequencychart[4][11]
    #Stretch8
    songnotechart[116] = songfrequencychart[5][4]
    songnotechart[117] = songfrequencychart[5][4]
    songnotechart[118] = songfrequencychart[6][1]
    songnotechart[119] = songfrequencychart[6][4]
    songnotechart[120] = songfrequencychart[6][8]
    songnotechart[121] = songfrequencychart[6][11]
    songnotechart[122] = songfrequencychart[6][4]
    songnotechart[123] = songfrequencychart[6][8]
    songnotechart[124] = songfrequencychart[6][11]
    songnotechart[125] = songfrequencychart[7][2]
    songnotechart[126] = songfrequencychart[6][8]
    songnotechart[127] = songfrequencychart[6][11]
    songnotechart[128] = songfrequencychart[7][2]
    songnotechart[129] = songfrequencychart[7][4]
    songnotechart[130] = songfrequencychart[7][6]
    songnotechart[131] = songfrequencychart[7][6]
    #Stretch9
    songnotechart[132] = 0
    songnotechart[133] = 0
    songnotechart[134] = songfrequencychart[5][3]
    songnotechart[135] = songfrequencychart[5][4]
    songnotechart[136] = songfrequencychart[5][2]
    songnotechart[137] = songfrequencychart[5][2]
    songnotechart[138] = songfrequencychart[5][3]
    songnotechart[139] = songfrequencychart[5][3]
    songnotechart[140] = songfrequencychart[4][8]
    songnotechart[141] = songfrequencychart[4][8]
    songnotechart[142] = songfrequencychart[4][10]
    songnotechart[143] = songfrequencychart[4][10]
    songnotechart[144] = songfrequencychart[4][11]
    songnotechart[145] = songfrequencychart[4][11]
    songnotechart[146] = songfrequencychart[4][11]
    songnotechart[147] = songfrequencychart[4][11]
    #Stretch10
    songnotechart[148] = 0
    songnotechart[149] = 0
    songnotechart[150] = songfrequencychart[4][11]
    songnotechart[151] = songfrequencychart[4][10]
    songnotechart[152] = songfrequencychart[4][6]
    songnotechart[153] = songfrequencychart[4][6]
    songnotechart[154] = songfrequencychart[5][3]
    songnotechart[155] = songfrequencychart[5][3]
    songnotechart[156] = songfrequencychart[5][1]
    songnotechart[157] = songfrequencychart[5][1]
    songnotechart[158] = songfrequencychart[6][11]
    songnotechart[159] = songfrequencychart[6][10]
    songnotechart[160] = songfrequencychart[6][6]
    songnotechart[161] = songfrequencychart[6][6]
    songnotechart[162] = songfrequencychart[7][3]
    songnotechart[163] = songfrequencychart[7][3]
    #Stretch11
    songnotechart[164] = songfrequencychart[7][1]
    songnotechart[165] = songfrequencychart[7][1]
    songnotechart[166] = songfrequencychart[4][11]
    songnotechart[167] = songfrequencychart[4][10]
    songnotechart[168] = songfrequencychart[4][3]
    songnotechart[169] = songfrequencychart[4][3]
    songnotechart[170] = songfrequencychart[5][1]
    songnotechart[171] = songfrequencychart[5][1]
    songnotechart[172] = songfrequencychart[4][11]
    songnotechart[173] = songfrequencychart[4][11]
    songnotechart[174] = 0
    songnotechart[175] = 0
    songnotechart[176] = songfrequencychart[4][10]
    songnotechart[177] = songfrequencychart[4][10]
    songnotechart[178] = 0
    songnotechart[179] = 0
    #Stretch12
    songnotechart[180] = songfrequencychart[4][6]
    songnotechart[181] = songfrequencychart[4][6]
    songnotechart[182] = songfrequencychart[3][11]
    songnotechart[183] = songfrequencychart[4][0]
    songnotechart[184] = songfrequencychart[4][1]
    songnotechart[185] = songfrequencychart[4][2]
    songnotechart[186] = songfrequencychart[4][3]
    songnotechart[187] = songfrequencychart[4][4]
    songnotechart[188] = songfrequencychart[4][5]
    songnotechart[189] = songfrequencychart[4][6]
    songnotechart[190] = songfrequencychart[4][7]
    songnotechart[191] = songfrequencychart[4][8]
    
    
    #thumby.audio.play(songfrequencychart[5][0],10000)

def loadIntro():
    
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    
    #every +1 to length = 1 more beat
    songprogress = 0
    songupdateprogress = 0
    songloop = 1
    songloopnum = 1
    songlength = 16
    songbeatdivisions = 4
    songtempo = 30
    songnotechart = [262]*songlength*songbeatdivisions
    #look up a note frequency chart, and good luck
    #Stretch1
    songnotechart[0] = songfrequencychart[4][0]
    songnotechart[1] = songfrequencychart[4][0]
    songnotechart[2] = songfrequencychart[4][0]
    songnotechart[3] = songfrequencychart[4][0]
    songnotechart[4] = songfrequencychart[3][7]
    songnotechart[5] = songfrequencychart[3][7]
    songnotechart[6] = songfrequencychart[3][7]
    songnotechart[7] = songfrequencychart[3][7]
    songnotechart[8] = songfrequencychart[4][8]
    songnotechart[9] = songfrequencychart[4][8]
    songnotechart[10] = songfrequencychart[4][8]
    songnotechart[11] = songfrequencychart[4][7]
    songnotechart[12] = songfrequencychart[4][6]
    songnotechart[13] = songfrequencychart[4][5]
    songnotechart[14] = songfrequencychart[4][4]
    songnotechart[15] = songfrequencychart[4][3]
    #Stretch2
    songnotechart[16] = songfrequencychart[4][0]
    songnotechart[17] = songfrequencychart[4][0]
    songnotechart[18] = songfrequencychart[4][0]
    songnotechart[19] = songfrequencychart[4][0]
    songnotechart[20] = songfrequencychart[3][7]
    songnotechart[21] = songfrequencychart[3][7]
    songnotechart[22] = songfrequencychart[3][7]
    songnotechart[23] = songfrequencychart[3][7]
    songnotechart[24] = songfrequencychart[4][8]
    songnotechart[25] = songfrequencychart[4][8]
    songnotechart[26] = songfrequencychart[4][8]
    songnotechart[27] = songfrequencychart[4][7]
    songnotechart[28] = songfrequencychart[4][6]
    songnotechart[29] = songfrequencychart[4][5]
    songnotechart[30] = songfrequencychart[4][4]
    songnotechart[31] = songfrequencychart[4][3]
    #Stretch3
    songnotechart[32] = songfrequencychart[3][0]
    songnotechart[33] = songfrequencychart[3][0]
    songnotechart[34] = songfrequencychart[3][0]
    songnotechart[35] = songfrequencychart[3][0]
    songnotechart[36] = songfrequencychart[3][3]
    songnotechart[37] = songfrequencychart[3][3]
    songnotechart[38] = songfrequencychart[3][3]
    songnotechart[39] = songfrequencychart[3][3]
    songnotechart[40] = songfrequencychart[3][2]
    songnotechart[41] = songfrequencychart[3][3]
    songnotechart[42] = songfrequencychart[3][2]
    songnotechart[43] = songfrequencychart[3][3]
    songnotechart[44] = songfrequencychart[3][2]
    songnotechart[45] = songfrequencychart[3][2]
    songnotechart[46] = songfrequencychart[3][2]
    songnotechart[47] = songfrequencychart[3][2]
    #Stretch4
    songnotechart[48] = songfrequencychart[3][0]
    songnotechart[49] = songfrequencychart[3][0]
    songnotechart[50] = songfrequencychart[3][0]
    songnotechart[51] = songfrequencychart[3][0]
    songnotechart[52] = songfrequencychart[3][3]
    songnotechart[53] = songfrequencychart[3][3]
    songnotechart[54] = songfrequencychart[3][3]
    songnotechart[55] = songfrequencychart[3][3]
    songnotechart[56] = songfrequencychart[3][2]
    songnotechart[57] = songfrequencychart[3][3]
    songnotechart[58] = songfrequencychart[3][2]
    songnotechart[59] = songfrequencychart[3][3]
    songnotechart[60] = songfrequencychart[3][7]
    songnotechart[61] = songfrequencychart[3][7]
    songnotechart[62] = songfrequencychart[3][7]
    songnotechart[63] = songfrequencychart[3][7]

def stopsound():
    global songloopnum
    songloopnum = 0
    thumby.audio.stop()

def soundupdate():
    
    global tm0
    global tm1
    global songprogress
    global songupdateprogress
    global songloop
    global songloopnum
    global songlength
    global songbeatdivisions
    global songtempo
    global songnotechart
    global frame
        
    if(songloopnum>0):
        
        tm1 = time.ticks_ms()   # Get time (ms)
        
        # Process the song data as acurately as i know how to
        songupdateprogress = tm1-tm0
        if(songupdateprogress > (3600/songtempo)*(songbeatdivisions)):
            songprogress += 1
            if(songprogress > ((songlength*songbeatdivisions)-1)):
                songprogress = 0
                songloopnum -= 1-(songloop == 1)
            if(songnotechart[songprogress]>15):
                thumby.audio.play(songnotechart[songprogress],10000)
            else:
                thumby.audio.stop()
            tm0 = time.ticks_ms()
    else:
        thumby.audio.stop()
    
