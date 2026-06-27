#FNAF
import thumby
import random
thumby.display.setFont("/lib/font5x7.bin",5,7,1)
thumby.display.drawText("Loading...",0,0,1)
#plushies(12x16)(Cis14x16)
bit_F = bytearray([0,24,136,120,95,127,223,255,248,232,24,0,
           112,126,125,125,125,125,189,94,191,111,15,6])
bit_B = bytearray([0,24,188,248,240,190,127,190,192,0,0,0,
           0,14,111,255,255,126,125,126,127,254,236,96])
bit_C = bytearray([0,0,192,0,112,120,92,125,126,222,250,112,0,0,
           39,125,127,125,103,120,127,127,126,127,223,175,119,7])
bit_P = bytearray([131,207,255,126,92,248,216,252,254,254,14,6,
           112,118,119,127,127,126,127,255,255,111,78,6])
bit_G = bytearray([0,0,0,64,248,160,179,160,128,0,0,0,
           2,3,67,112,121,96,0,0,0,48,48,0])
rand = random.randint(0,12)
if(rand == 12):
    thumby.display.blit(bit_G,30,23,12,16,0,0,0)
elif((rand%4)==0):
    thumby.display.blit(bit_F,30,23,12,16,0,0,0)
elif((rand%4)==1):
    thumby.display.blit(bit_B,30,23,12,16,0,0,0)
elif((rand%4)==2):
    thumby.display.blit(bit_C,30,23,14,16,0,0,0)
else:
    thumby.display.blit(bit_P,30,23,12,16,0,0,0)
thumby.display.update()
import sys
sys.path.insert(0, '/Games/TinyFreddy')
import TFcameras
import math
import time
import micropython
import polysynth
import midi
import mml
micropython.mem_info(1)
gamestate = "title1"
thumby.display.setFPS(60)
freddydifficulty = 0
bonniedifficulty = 0
chicadifficulty = 0
foxydifficulty = 0
goldendifficulty = 0
animAI = [0,0,0,0,0]
rand = 0
night = 1
staticmode = 1
audiomode = 0
fadepower = 0
settings = [staticmode, audiomode]
EMULATOR = 0
try:
    import emulator
    EMULATOR = 1
    night = 2
    audiomode = 1
except ImportError:
    thumby.saveData.setName("TinyFreddy")
    if(thumby.saveData.hasItem("progress")):
        night = thumby.saveData.getItem("progress")
    else:
        night = 1
        thumby.saveData.setItem("progress", 1)
        thumby.saveData.save()
    if(thumby.saveData.hasItem("staticmode")):
        settings[0] = thumby.saveData.getItem("staticmode")
    else:
        thumby.saveData.setItem("staticmode", settings[0])
        thumby.saveData.save()
    if(thumby.saveData.hasItem("audiomode")):
        settings[1] = thumby.saveData.getItem("audiomode")
    else:
        thumby.saveData.setItem("audiomode", settings[1])
        thumby.saveData.save()
staticmode = settings[0]
audiomode = settings[1]
def fader(power):
    length = 0
    while(length < 360):
        x = (length%18)*4+4*(math.floor(length/18)%4)
        y = math.floor(length/36)*4
        thumby.display.drawFilledRectangle(x,y,4,4,0)
        length += math.floor(pow(power,1.1))
def sfx(ID):
    if(ID == 0):
        text = "!c0@t140@n4c4.c.c.c.c.c"
    if(ID == 1):
        text = "!c0@t140@n3c5..c..c"
    if(ID == 2):
        text = "!c0@t100@n4c6b5.c6cb5.c6c#-.c#-"
    if(ID == 3):
        text = "!c0@t70@n4c5b4.c5cb4.c5c#-..c#-"
    if(ID == 4):
        text = "!c0@t480@n4g#6fabfaga#fg#bgfg#a#f#"
    if(ID == 5):
        text = "!c0@t480@n4g#4fabfaga#fg#bgfg#a#f#"
    return mml.load(text)
def title(warning):
    global night
    spr_office = thumby.Sprite(72,40,"/Games/TinyFreddy/Title.bin",0,0)
    menu = 1
    selection = 0
    selectiony = 0
    selectionynext = 0
    thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
    frame = 0
    nextstate = "title1"
    global staticmode
    global audiomode
    polysynth.configure()
    if(audiomode == 1):
        song = midi.load(open("/Games/TinyFreddy/Music/Title.mid", "rb"),mute=[1])
    else:
        song = midi.load(open("/Games/TinyFreddy/Music/Title.mid", "rb"))
    polysynth.play(song, loop=True)
    while(nextstate == "title1"):
        fade = 1
        fadepower = 1
        while(menu == 1):
            if((selectiony == selectionynext)&(fade == 0)):
                if(thumby.buttonD.justPressed()):
                    selection += (selection < 6)
                if(thumby.buttonU.justPressed()):
                    selection -= (selection > 0)
            if(selection == 0):
                selectionynext = 0
            elif(selection == 1):
                selectionynext = 40
            elif(selection == 2):
                selectionynext = 48
            elif(selection == 3):
                selectionynext = 56
            elif(selection == 4):
                selectionynext = 64
            elif(selection == 5):
                selectionynext = 72
            elif(selection == 6):
                selectionynext = 80
            if(selectiony<selectionynext):
                selectiony += 3
                if(selectiony>selectionynext):
                    selectiony = selectionynext
            elif(selectiony>selectionynext):
                selectiony -= 3
                if(selectiony<selectionynext):
                    selectiony = selectionynext
            if(thumby.buttonA.justPressed()):
                fade = 2
            frame += 1
            frame = frame % 30030
            thumby.display.fill(0)
            rand = random.randint(0,30)
            if(rand<28):
                spr_office.setFrame(0)
            else:
                spr_office.setFrame(rand-27)
            thumby.display.drawSprite(spr_office)
            thumby.display.setFont("/lib/font5x7.bin",5,7,1)
            if(selectiony>39):
                thumby.display.drawText(">",0,17,1)
            thumby.display.drawText("Five",0,0-selectiony,1)
            thumby.display.drawText("Nights",0,8-selectiony,1)
            thumby.display.drawText("At",0,16-selectiony,1)
            thumby.display.drawText("Freddys",0,24-selectiony,1)
            thumby.display.drawText("New",6,57-selectiony,1)
            thumby.display.drawText("Cont:"+str(night),6,65-selectiony,1)
            thumby.display.drawText("Night6",6,73-selectiony,1)
            thumby.display.drawText("Custom",6,81-selectiony,1)
            thumby.display.drawText("Option",6,89-selectiony,1)
            thumby.display.drawText("Exit",6,97-selectiony,1)
            TFcameras.static(frame,staticmode)
            if(fade == 1):
                fadepower += 1
                if(fadepower < 9):
                    fader(fadepower)
                else:
                    fade = 0
            
            if(fade == 2):
                fadepower -= 1
                if(fadepower > 1):
                    fader(fadepower)
                else:
                    if(selection == 6):
                        menu = 0
                        nextstate = "exit"
                    elif(selection == 1):
                        night = 1
                        nextstate = "game"
                        menu = 0
                    elif(selection == 4):
                        nextstate = "game"
                        menu = 2
                    elif(selection == 2):
                        nextstate = "game"
                        menu = 0
                    elif(selection == 3):
                        night = 6
                        nextstate = "game"
                        menu = 0
                    elif(selection == 5):
                        nextstate = "title1"
                        menu = 3
            
            thumby.display.update()
        
        if(selection == 1):
            menu = 0
            moveleft = 72
            night = 1
            fade = 1
            fadepower = 1
            spr_office.setFrame(4)
            while(menu == 0):
                thumby.display.drawSprite(spr_office)
                if(fade == 0):
                    if(thumby.buttonA.justPressed()):
                        fade = 2
                    if(thumby.buttonB.justPressed()):
                        menu = 1
                        nextstate = "title1"
                frame += 1
                frame % 30030
                if(fade == 1):
                    fadepower += 1
                    if(fadepower < 9):
                        fader(fadepower)
                    else:
                        fade = 0
                if(fade == 2):
                    fadepower -= 1
                    if(fadepower > 1):
                        fader(fadepower)
                    else:
                        menu = 1
                        nextstate = "game"
                thumby.display.update()
        if(menu == 2):
            global freddydifficulty
            global bonniedifficulty
            global chicadifficulty
            global foxydifficulty
            global goldendifficulty
            global animAI
            night = 7
            # BITMAP: width: 16, height: 16
            bit_0 = bytearray([0,0,12,140,248,216,124,254,223,255,254,252,248,252,12,0,
                240,224,224,243,155,219,251,251,251,223,221,255,241,240,24,240])
            # BITMAP: width: 16, height: 16
            bit_1 = bytearray([0,0,0,224,247,255,251,248,191,247,48,64,0,0,0,0,
                224,224,224,39,239,255,251,251,251,243,243,243,227,224,192,128])
            # BITMAP: width: 16, height: 16
            bit_2 = bytearray([0,0,0,224,240,89,90,255,95,90,249,240,224,0,0,0,
                252,252,248,119,239,223,217,209,209,217,223,239,231,224,224,192])
            # BITMAP: width: 16, height: 16
            bit_3 = bytearray([255,255,255,255,128,222,156,156,254,188,248,252,158,31,255,255,
                255,255,255,247,241,255,183,178,243,251,79,227,227,195,255,255])
            # BITMAP: width: 16, height: 16
            bit_4 = bytearray([14,10,236,248,56,188,59,252,255,63,188,56,248,236,10,14,
                0,0,111,223,254,222,254,211,211,254,222,254,223,111,0,0])
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            selection = 0
            while(menu == 2):
                if(thumby.buttonR.justPressed()):
                    selection += (selection < 3)
                if(thumby.buttonL.justPressed()):
                    selection -= (selection > -1)
                if(thumby.buttonU.justPressed()):
                    animAI[selection+5*(selection == -1)] += (animAI[selection+5*(selection == -1)]<20)-20*(animAI[selection+5*(selection == -1)]==20)
                if(thumby.buttonD.justPressed()):
                    animAI[selection+5*(selection == -1)] -= (animAI[selection+5*(selection == -1)]>0)-20*(animAI[selection+5*(selection == -1)]==0)
                freddydifficulty = animAI[0]
                bonniedifficulty = animAI[1]
                chicadifficulty = animAI[2]
                foxydifficulty = animAI[3]
                goldendifficulty = animAI[4]
                if(thumby.buttonA.justPressed()):
                    menu = 0
                    nextstate = "game"
                if(thumby.buttonB.justPressed()):
                    menu = 1
                    nextstate = "title1"
                thumby.display.fill(0)
                if(selection == -1):
                    thumby.display.blit(bit_4,1,6,16,16,-1,0,0)
                else:
                    thumby.display.blit(bit_0,1,6,16,16,-1,0,0)
                thumby.display.blit(bit_1,19,6,16,16,-1,0,0)
                thumby.display.blit(bit_2,37,6,16,16,-1,0,0)
                thumby.display.blit(bit_3,55,6,16,16,-1,0,0)
                thumby.display.drawText("Custom Night",12,0,1)
                thumby.display.drawText("Fred",1,23,1)
                if(selection == -1):
                    thumby.display.drawText(str(goldendifficulty),5,29,1)
                else:
                    thumby.display.drawText(str(freddydifficulty),5,29,1)
                thumby.display.drawText("Bonn",19,23,1)
                thumby.display.drawText(str(bonniedifficulty),23,29,1)
                thumby.display.drawText("Chic",37,23,1)
                thumby.display.drawText(str(chicadifficulty),41,29,1)
                thumby.display.drawText("Foxy",55,23,1)
                thumby.display.drawText(str(foxydifficulty),59,29,1)
                if(selection == -1):
                    thumby.display.drawText("<  >",1,29,1)
                else:
                    thumby.display.drawText("<  >",1+(18*selection),29,1)
                thumby.display.drawText("A:Start B:Back",8,35,1)
                thumby.display.update()
        if(menu == 3):
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            selection = 0
            while(menu == 3):
                audiomode
                staticmode
                frame += 1
                if(thumby.buttonD.justPressed()):
                    selection += (selection < 1)
                if(thumby.buttonU.justPressed()):
                    selection -= (selection > 0)
                if(thumby.buttonA.justPressed()):
                    if(selection == 0):
                        staticmode = not(staticmode)
                        settings[0] = staticmode
                    if(selection == 1):
                        audiomode = not(audiomode)
                        settings[1] = audiomode
                if(thumby.buttonB.justPressed()):
                    menu = 1
                thumby.display.fill(0)
                thumby.display.drawText(">",0,0+(6*selection),1)
                if(staticmode == 0):
                    thumby.display.drawText("Static: Old",4,0,1)
                else:
                    thumby.display.drawText("Static: New",4,0,1)
                if(audiomode == 0):
                    thumby.display.drawText("Audio: Poly",4,6,1)
                else:
                    thumby.display.drawText("Audio: Mono",4,6,1)
                TFcameras.static(frame,staticmode)
                thumby.display.update()
            if(menu == 1):
                thumby.display.fill(0)
                thumby.display.drawText("Loading changes",0,0,1)
                thumby.display.update()
                thumby.saveData.setItem("staticmode", staticmode)
                thumby.saveData.save()
                thumby.saveData.setItem("audiomode", audiomode)
                thumby.saveData.save()
    polysynth.stop()
    return nextstate
def phonecall(ID):
    state = 0
    # BITMAP: width: 14, height: 30
    bit_0 = bytearray([252,2,169,85,169,85,169,85,2,252,8,16,96,128,
           0,1,2,2,2,2,2,6,249,0,0,0,0,255,
           192,32,144,80,144,80,144,88,39,192,0,0,128,127,
           15,16,42,37,42,37,42,37,16,15,4,2,1,0])
    # BITMAP: width: 9, height: 10
    bit_1 = bytearray([252,2,1,0,252,2,0,120,132,
           0,1,2,0,0,1,0,0,0])
    if(audiomode == 0):
        polysynth.configure([polysynth.SQUARE, polysynth.NOISE])
        song = midi.load(open("/Games/TinyFreddy/Music/PhoneRinger.mid", "rb"), reserve={1:[1]})
    else:
        polysynth.configure()
        song = midi.load(open("/Games/TinyFreddy/Music/PhoneRinger.mid", "rb"), mute=[1])
    polysynth.play(song, loop=True)
    frame = 0
    thumby.buttonA.justPressed()
    skip = 1
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    while(1):
        frame += 1
        thumby.display.fill(0)
        thumby.display.blit(bit_0, 58, 6, 14, 30, 0, 0, 0)
        if((frame%60)<30):
            thumby.display.blit(bit_1, 48, 6, 9, 10, 0, 0, 0)
        thumby.display.drawText("Answer: A",0,12,1)
        thumby.display.drawText("Mute: B",0,18,1)
        thumby.display.update()
        if(thumby.buttonA.justPressed()):
            skip = 0
            break
        if(thumby.buttonB.justPressed()):
            break
    if(skip == 0):
        if(ID == 1):
            text = [["Hello, hello",
                    "hello? Uh, I'm",
                    "the old",
                    "security",
                    "guard, here to",
                    "help you out."],
                    ["Consider this",
                    "your guide to",
                    "a workweek at",
                    "Freddy's! huh?",
                    "Yeah, not the",
                    "best name."],
                    ["First off, the",
                    "animatronics",
                    "are going to",
                    "try stuffing",
                    "you into a",
                    "freddy suit."],
                    ["What you think",
                    "are ghosts is",
                    "actually just",
                    "a programming",
                    "error, don't",
                    "worry too much."],
                    ["Anyway, here's",
                    "how to stop",
                    "them from, uh,",
                    "hurting you,",
                    "at least what",
                    "i know."],
                    ["Firstly: doors",
                    "The A button",
                    "on your remote",
                    "works doors,",
                    "The B button",
                    "works lights"],
                    ["Next: cameras",
                    "The V button",
                    "turns on the",
                    "cameras.",
                    "< and > change",
                    "the camera #"],
                    ["",
                    "Hold A in",
                    "order to use",
                    "the more",
                    "detailed map",
                    ""],
                    ["And uh, I",
                    "think that's",
                    "it for the",
                    "options you",
                    "have to help",
                    "yourself out."],
                    ["Remember, ALL",
                    "electronics,",
                    "including the",
                    "cameras waste",
                    "power. Don't",
                    "overuse them!"],
                    ["",
                    "I hope to",
                    "speak to you",
                    "tommorow!",
                    "",
                    ""]]
        if(ID == 2):
            text = [["He-Hey!",
                    "night 2 huh?",
                    "Most guards",
                    "get cold feet",
                    "and quit. I",
                    "envy them..."],
                    ["Look, by now",
                    "you know the",
                    "truth, I'm",
                    "not allowed",
                    "to talk and",
                    "i'm sorry..."],
                    ["... anyway",
                    "the bots will",
                    "start moving",
                    "quicker",
                    "tonight, so",
                    "get ready."],
                    ["Never forget",
                    "about your",
                    "lights.",
                    "Bonnie and",
                    "Chica are",
                    "programmed..."],
                    ["to check into",
                    "staff rooms",
                    "before entry",
                    "to see if",
                    "they're",
                    "needed there."],
                    ["The lights",
                    "are the last",
                    "thing to",
                    "catch them",
                    "before,",
                    "well..."],
                    ["Oh yeah, and",
                    "foxy doesn't",
                    "like being",
                    "watched. If",
                    "the cam light",
                    "blinks, he..."],
                    ["... seems to",
                    "get nervous,",
                    "as if he does",
                    "not want to",
                    "reveal his",
                    "attack."],
                    ["Freddy",
                    "himself never",
                    "comes off",
                    "stage often,",
                    "so i'll talk",
                    "Fred tommorow."],
                    ["Anyway, thats",
                    "the cast. I",
                    "wish you the",
                    "best of luck.",
                    "goodnight!",
                    ""]]
        if(ID == 3):
            text = [["Hi man!",
                    "night 3! I",
                    "said I",
                    "would talk",
                    "about freddy",
                    "Now, right?"],
                    ["He also hates",
                    "being watched",
                    "like foxy,",
                    "but he seems",
                    "more aware of",
                    "which cam..."],
                    ["Which camera",
                    "you look at.",
                    "it might be",
                    "the small",
                    "click sound",
                    "they make."],
                    ["He seems to",
                    "be the most",
                    "aware of the",
                    "group, he",
                    "almost never",
                    "goes back."],
                    ["... try not",
                    "to let him",
                    "get into",
                    "the corner",
                    "of the hall.",
                    ""],
                    ["I don't",
                    "think your",
                    "door lights",
                    "will catch",
                    "him. he's",
                    "too quick."],
                    ["Your doors",
                    "will always",
                    "protect you,",
                    "don't worry",
                    "about it",
                    "too much."],
                    ["Hey, have",
                    "you ever",
                    "seen one of",
                    "these shows?",
                    "I hear they",
                    "were the..."],
                    ["talk of the",
                    "town in their",
                    "time. sadly,",
                    "it lead to a",
                    "child losing",
                    "their head."],
                    ["It's been",
                    "dubbed the",
                    "bite of 87.",
                    "they had to",
                    "rework the",
                    "restaurant..."],
                    ["Just to",
                    "get the news",
                    "off their",
                    "back.",
                    "Actually,",
                    "the news..."],
                    ["Boosted their",
                    "guest size",
                    "by the boat-",
                    "load. at",
                    "least until",
                    "the five kids..."],
                    ["... I've",
                    "talked for",
                    "too long,",
                    "sorry. Catch",
                    "you on the",
                    "flipside!"]]
        if(ID == 4):
            text = [["Hey there,",
                    "night 4.",
                    "Most guards",
                    "don't last",
                    "this long. I",
                    "mean, uh..."],
                    ["Tonight,",
                    "things are",
                    "gonna get",
                    "real... so",
                    "get",
                    "comfortable."],
                    ["If you keep",
                    "your cool,",
                    "you should be",
                    "fine, I",
                    "wouldn't",
                    "worry."],
                    ["Hey, I have",
                    "an idea, what",
                    "if you played",
                    "dead? like,",
                    "went limp?",
                    ""],
                    ["There's a",
                    "chance they",
                    "would see you",
                    "as a suit",
                    "rather than a",
                    "endoskeleton."],
                    ["Then again,",
                    "they might",
                    "stuff an endo",
                    "into you...",
                    "that would be",
                    "worse huh?"],
                    ["... The",
                    "restaurant",
                    "owner",
                    "contacted me,",
                    "said that I",
                    "would be..."],
                    ["fired if I",
                    "kept making",
                    "these. I'm",
                    "okay with it",
                    "as long as",
                    "you're safe."],
                    ["Doesn't hit",
                    "my consience",
                    "well to",
                    "leave you",
                    "without help.",
                    ""],
                    ["",
                    "",
                    "Have a good",
                    "night pal!",
                    "",
                    ""]]
        if(ID == 5):
            text = [["Hello? are",
                    "you getting",
                    "this? I uh...",
                    "I need you",
                    "to hear this.",
                    "Please..."],
                    ["I'm glad I",
                    "recorded these",
                    "messages, well,",
                    "when I did.",
                    "Not sure how",
                    "to say this..."],
                    ["Uh, hey, could",
                    "you check on",
                    "those suits,",
                    "in the back-",
                    "room? I uh...",
                    ""],
                    ["",
                    "I think I left",
                    "something",
                    "PERSONAL in",
                    "there...",
                    ""],
                    ["",
                    "something very",
                    "important to",
                    "ME... if you",
                    "get me, huh?",
                    ""],
                    ["That, an uh...",
                    "oh god, I'm",
                    "curious,",
                    "what's in all",
                    "those empty",
                    "heads, y'know?"],
                    ["...",
                    "uh...",
                    "...",
                    "...",
                    "oh no...",
                    "..."],
                    ["",
                    "",
                    "Huh?",
                    "Willia-",
                    "",
                    ""]]
            #polysynth.configure()
            #if(audiomode == 1):
            #    song = midi.load(open("/Games/TinyFreddy/Music/Toreador.mid", "rb"),mute=[1])
            #else:
            #    song = midi.load(open("/Games/TinyFreddy/Music/Toreador.mid", "rb"))
            #polysynth.play(song, loop=True)
            #polysynth.stop()
            #spr_office = thumby.Sprite(72,40,"/Games/TinyFreddy/Title.bin",0,0)
            #spr_office.setFrame(5)
        i = 0
        while(i<len(text)):
            thumby.display.fill(0)
            thumby.display.blit(bit_0, 58, 6, 14, 30, 0, 0, 0)
            thumby.display.drawText(text[i][0],0,0,1)
            thumby.display.drawText(text[i][1],0,6,1)
            thumby.display.drawText(text[i][2],0,12,1)
            thumby.display.drawText(text[i][3],0,18,1)
            thumby.display.drawText(text[i][4],0,24,1)
            thumby.display.drawText(text[i][5],0,30,1)
            thumby.display.update()
            if(thumby.buttonA.justPressed()):
                i += 1
            if(thumby.buttonB.justPressed()):
                break
    polysynth.stop()
#This is where the FNAF begins
def game():
    global night
    global staticmode
    global audiomode
    spr_office = thumby.Sprite(100,40,"/Games/TinyFreddy/Office.bin",0,0)
    thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
    done = 300
    rand = random.randint(0,12)
    while(done > 0):
        done -= 1
        thumby.display.fill(0)
        if(rand == 12):
            thumby.display.blit(bit_G, 30, 24, 12, 16, 0, 0, 0)
        elif((rand%4)==0):
            thumby.display.blit(bit_F, 30, 24, 12, 16, 0, 0, 0)
        elif((rand%4)==1):
            thumby.display.blit(bit_B, 30, 24, 12, 16, 0, 0, 0)
        elif((rand%4)==2):
            thumby.display.blit(bit_C, 30, 24, 14, 16, 0, 0, 0)
        else:
            thumby.display.blit(bit_P, 30, 24, 12, 16, 0, 0, 0)
        if(done < 298):
            thumby.display.drawText("Night "+str(night),4,16,1)
        if(done > 292):
            if(done > 297):
                thumby.display.drawFilledRectangle(0, 18, 72, 2, 1)
                thumby.display.drawLine(0, 21, 72, 21, 1)
            else:
                length = 3
                while(length>0):
                    thumby.display.drawFilledRectangle(0,random.randint(0,39),72,random.randint(1,3),1)
                    length -= 1
        thumby.display.update()
    if(night<6):
        phonecall(night)
    # BITMAP: width: 6, height: 6
    bit_0 = bytearray([0,25,63,59,32,0])
    # BITMAP: width: 6, height: 6
    bit_1 = bytearray([14,6,36,60,46,0])
    spr_fan = thumby.Sprite(6,6,bit_0+bit_1,0,0)
    spr_doors = thumby.Sprite(10,39,"/Games/TinyFreddy/Images/doors.bin",0,0,0)
    spr_doorsw = thumby.Sprite(10,39,"/Games/TinyFreddy/Images/doors.bin",0,0,1)
    # BITMAP: width: 8, height: 17
    bit_0 = bytearray([255,237,242,250,196,180,232,240,
               255,255,255,255,127,127,63,31,
               1,1,0,0,0,0,0,0])
    # BITMAP: width: 8, height: 17
    bit_1 = bytearray([255,237,18,154,100,20,232,240,
               255,7,128,128,64,71,63,31,
               1,1,0,0,0,0,0,0])
    spr_litWindowL = thumby.Sprite(8,17,bit_0+bit_1,10,10)
    # BITMAP: width: 8, height: 17
    bit_0 = bytearray([240,200,68,132,226,194,177,255,
               31,63,127,127,255,255,255,255,
               0,0,0,0,0,0,1,1])
    # BITMAP: width: 8, height: 17
    bit_1 = bytearray([240,168,244,84,254,86,241,255,
               31,34,87,101,209,165,87,255,
               0,0,0,0,0,0,1,1])
    spr_litWindowR = thumby.Sprite(8,17,bit_0+bit_1,10,10)
    spr_camup = thumby.Sprite(72,40,'/Games/TinyFreddy/CamFlip.bin',0,0,0)
    done = 300
    cam = 0
    camto = [[4,8,1,8],
            [0,2,3,10],
            [8,10,5,1],
            [1,5,4,6],
            [3,7,0,7],
            [2,9,8,3],
            [1,3,7,9],
            [6,4,0,4],
            [5,0,2,0],
            [10,6,10,5],
            [9,1,9,2]]
    freevar = [0,0,0,0,0]
    hud = 1
    hudy = 0
    scrollx = 0
    leftDoorLit = 0
    rightDoorLit = 0
    leftDoorClosed = 0
    lDoorClosedFrame = 0
    rDoorClosedFrame = 0
    rightDoorClosed = 0
    camUp = 0
    camMode = 0
    camstate = 0
    frame = 0
    am = 0
    power = 99
    powerusage = 0
    powerout = 0
    freddylocation = 0
    bonnielocation = 0
    chicalocation = 0
    foxylocation = 0
    global freddydifficulty
    global bonniedifficulty
    global chicadifficulty
    global foxydifficulty
    global goldendifficulty
    global animAI
    goldenappear = 0
    goldendelay = 0
    bstinger = 0
    cstinger = 0
    bt0a = time.ticks_ms()
    bt0b = bt0a
    bdelay = -1
    ct0a = bt0a
    ct0b = bt0a
    cdelay = -1
    ft0a = bt0a
    ft0b = bt0a
    fdelay = -1
    fmoving = 0
    freddycamnums = [0,1,10,9,6,7]
    drawFreddy = 0
    pt0a = bt0a
    pt0b = bt0a
    pdelay = -1
    foxydrain = 0
    foxyframe = 0
    foxytimer = 1000
    rsclocka = bt0a
    rsclockb = bt0a
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    t0a = time.ticks_ms()
    t0b = t0a
    t0 = 0
    tpa = time.ticks_ms()
    tpb = time.ticks_ms()
    tpc = 0
    tp = 0
    fail = 0
    jumpnum = 0
    maxloop = 0
    if(night != 7):
        if(night == 1):
            animAI = [0,0,0,0,0]
        if(night == 2):
            animAI = [0,3,1,1,0]
        if(night == 3):
            animAI = [0,0,5,2,0]
        if(night == 4):
            animAI = [1,2,4,6,0]
        if(night == 5):
            animAI = [3,5,7,5,1]
        if(night == 6):
            animAI = [4,10,12,16,4]
        freddydifficulty = animAI[0]
        bonniedifficulty = animAI[1]
        chicadifficulty = animAI[2]
        foxydifficulty = animAI[3]
        goldendifficulty = animAI[4]
    polysynth.configure()
    if(audiomode == 0):
        foxySong = midi.load(open("/Games/TinyFreddy/Music/FoxySong.mid", "rb"), reserve={0:[]})
        jukeBoxSong = midi.load(open("/Games/TinyFreddy/Music/JukeBox.mid", "rb"), reserve={0:[]})
        metroidReferenceSong = midi.load(open("/Games/TinyFreddy/Music/MetroidReference.mid", "rb"), reserve={0:[]})
    while((am != 6)&(fail == 0)):
        t0b = time.ticks_ms()
        t0 = t0b-t0a
        #animatronicLocker
        if(power > -1):
            bt0a = time.ticks_ms()
            if(bonnielocation < 7):
                if((bt0a-bt0b)>=4970):
                    if(random.randint(1,20)<(bonniedifficulty+1)):
                        if((bonnielocation == 0)|(bonnielocation == 1)|(bonnielocation == 3)):
                            bonnielocation += random.randint(1,2)
                        elif((bonnielocation == 2)|(bonnielocation == 5)):
                            bonnielocation += random.randint(0,1)
                            bonnielocation -= (bonnielocation==2)
                        elif(bonnielocation == 4):
                            bonnielocation += random.randint(0,1)
                            bonnielocation += (bonnielocation==5)-(bonnielocation==4)
                        elif(bonnielocation == 6):
                            if(leftDoorClosed):
                                bonnielocation = 1
                            else:
                                bonnielocation = 7
                                bdelay = camUp
                            bstinger = 0
                    bt0a = time.ticks_ms()
                    bt0b = time.ticks_ms()
            else:
                if(bdelay == 0)&(camUp == 1):
                    bdelay = 1
                    bt0b = time.ticks_ms()
                if(bdelay == 1)&(camUp == 0):
                    jumpnum = 0
                    fail = 1
                if((bt0a-bt0b)>=30000):
                    jumpnum = 0
                    fail = 1
            ct0a = time.ticks_ms()
            if(chicalocation < 7):
                if((ct0a-ct0b)>=4980):
                    if(random.randint(1,20)<(chicadifficulty+1)):
                        if(chicalocation == 0):
                            chicalocation += 1
                        elif((chicalocation == 1)|(chicalocation == 2)):
                            chicalocation += random.randint(1,2)
                        elif((chicalocation == 3)|(chicalocation == 5)):
                            chicalocation += random.randint(0,1)
                            chicalocation -= (chicalocation==3)
                        elif(chicalocation == 4):
                            chicalocation += random.randint(0,1)
                            chicalocation -= (chicalocation==4)*3
                        elif(chicalocation == 6):
                            if(rightDoorClosed):
                                chicalocation = 4
                            else:
                                chicalocation = 7
                                cdelay = camUp
                            cstinger = 0
                    ct0a = time.ticks_ms()
                    ct0b = time.ticks_ms()
            else:
                if(cdelay == 0)&(camUp == 1):
                    cdelay = 1
                    ct0b = time.ticks_ms()
                if(cdelay == 1)&(camUp == 0):
                    jumpnum = 1
                    fail = 1
                if((ct0a-ct0b)>=30000):
                    jumpnum = 1
                    fail = 1
            ft0a = time.ticks_ms()
            if((ft0a-ft0b)>=3520):
                if(random.randint(1,20)<(freddydifficulty+1)):
                    if((freddylocation < 5)):
                        fmoving = 1
                        fdelay = time.ticks_ms()
                    elif(freddylocation == 5):
                        if((rightDoorClosed)|((not(camUp < 2))&(cam == 7))|(camUp < 2)):
                            if(random.randint(0,14) == 0):
                                freddylocation = 4
                        else:
                            freddylocation = 6
                    elif(freddylocation == 6):
                        if(camUp == 0):
                            if(random.randint(0,1)==1):
                                jumpnum = 2
                                fail = 1
                ft0a = time.ticks_ms()
                ft0b = time.ticks_ms()
            if(fmoving == 1):
                if((freddycamnums[freddylocation] == cam)&(camUp > 0)):
                    fdelay = time.ticks_ms()
                else:
                    if((ft0a-fdelay) >= (11000-(freddydifficulty*500))):
                        freddylocation += 1
                        fmoving = 0
                        polysynth.play(sfx(3))
            pt0a = time.ticks_ms()
            if(not(camUp == 0)):
                foxytimer = random.randint(1000,16000)
                pdelay = time.ticks_ms()
            if(foxylocation < 3):
                if((pt0a-pt0b)>=5010):
                    if(((pt0a - pdelay)>foxytimer)):
                        if(random.randint(1,20)<(foxydifficulty+1)):
                            foxylocation += 1
                            if(foxylocation == 3):
                                foxyframe = 0
                    pt0a = time.ticks_ms()
                    pt0b = time.ticks_ms()
            else:
                if(((pt0a-pt0b)>=30000)&(foxyframe == 0)):
                    foxyframe = 1
            if(goldenappear == 1):
                gt0a = time.ticks_ms()
                if(EMULATOR == 1):
                    if((gt0a - goldendelay)>=5500-(4000*(goldendifficulty/20))):
                        jumpnum = 5
                        fail = 1
                else:
                    if((gt0a - goldendelay)>=5000-(4000*(goldendifficulty/20))):
                        jumpnum = 5
                        fail = 1
        else:
            # BITMAP: width: 8, height: 8
            bit_0 = bytearray([0,66,172,106,55,106,172,66])
            if(powerout == 0):
                powerout = 1
                maxloop = 0
                ft0b = time.ticks_ms()
                freddylocation = 0
            ft0a = time.ticks_ms()
            if(freddylocation == 0):
                if((ft0a-ft0b)>=5000):
                    ft0b = time.ticks_ms()
                    maxloop += 1
                    if((random.randint(0,3) == 0)|(maxloop > 2)):
                        freddylocation = 1
                        if(audiomode == 1):
                            song = midi.load(open("/Games/TinyFreddy/Music/Toreador.mid", "rb"),mute=[1])
                        else:
                            song = midi.load(open("/Games/TinyFreddy/Music/Toreador.mid", "rb"))
                        polysynth.play(song)
                        maxloop = 0
            if(freddylocation == 1):
                fmoving += 1
                if(fmoving > 19):
                    fmoving = 0
                if(fmoving < 10):
                    drawFreddy = 1
                else:
                    drawFreddy = 0
                if((ft0a-ft0b)>=5000):
                    maxloop += 1
                    ft0b = time.ticks_ms()
                    if((random.randint(0,3) == 0)|(maxloop > 2)):
                        freddylocation = 2
                        polysynth.stop()
            if(freddylocation == 2):
                if((ft0a-ft0b)>=2000):
                    ft0b = time.ticks_ms()
                    if(random.randint(0,4) == 0):
                        jumpnum = 4
                        fail = 1
            
        if(camMode == 0):
            if((thumby.buttonD.justPressed())):
                camUp = (camUp==0)
                if(camUp == 0):
                    camstate = random.randint(0,99)
                    if((random.randint(0,100)<(goldendifficulty*2))|(goldenappear == 2)):
                        goldenappear = 1-(goldenappear == 2)
                        goldendelay = time.ticks_ms()
                        if(goldenappear == 1):
                            x = 1
                            polysynth.play(sfx(2))
                leftDoorLit = 0
                rightDoorLit = 0
            if(thumby.buttonU.justPressed()):
                hud = (hud+1)%2
        
        if(hudy < 6)and(hud == 1):
            hudy += 1
        
        if(hudy > 0)and(hud == 0):
            hudy -= 1
        
        if(camUp == 0):
            scrollx += ((thumby.buttonR.pressed())&(scrollx<28))-((thumby.buttonL.pressed())&(scrollx>0))
            thumby.buttonR.justPressed()
            thumby.buttonL.justPressed()
            if(power > -1):
                if(thumby.buttonA.justPressed()):
                    if(scrollx<15):
                        leftDoorClosed = ((leftDoorClosed+1)%2)
                        polysynth.playnote(0,42,polysynth.instrument(rise=-4,length=400))
                    else:
                        rightDoorClosed = ((rightDoorClosed+1)%2)
                        polysynth.playnote(0,42,polysynth.instrument(rise=-4,length=400))
                if(thumby.buttonB.justPressed()):
                    if(scrollx<15):
                        leftDoorLit = ((leftDoorLit+1)%2)
                        rightDoorLit = 0
                    else:
                        rightDoorLit = ((rightDoorLit+1)%2)
                        leftDoorLit = 0
            
        else:
            camMode = 0
            if(thumby.buttonA.pressed()):
                camMode = 1
            prevCam = cam
            if(camMode == 1):
                if(thumby.buttonU.justPressed()):
                    cam = camto[cam][0]
                
                if(thumby.buttonL.justPressed()):
                    cam = camto[cam][1]
                
                if(thumby.buttonD.justPressed()):
                    cam = camto[cam][2]
                
                if(thumby.buttonR.justPressed()):
                    cam = camto[cam][3]
            else:
                if(thumby.buttonL.justPressed()):
                    cam -= 1
                    if(cam < 0):
                        cam = 10
                if(thumby.buttonR.justPressed()):
                    cam += 1
                    if(cam > 10):
                        cam = 0
            if(cam == 9)&(cam != prevCam):
                if(freddylocation == 3):
                    x = 3
                elif(chicalocation == 3):
                    x = 3
        if(power < 0):
            leftDoorLit = 0
            rightDoorLit = 0
            leftDoorClosed = 0
            rightDoorClosed = 0
            camUp = 0
            hud = 0
        
        powerusage = (leftDoorLit|rightDoorLit)+(leftDoorClosed)+(rightDoorClosed)+(camUp>0)
        
        tpb = time.ticks_ms()
        tpc = (tpb-tpa)
        tpa = time.ticks_ms()
        tp += tpc*(powerusage+1)
        if(tp >= 8600):
            power -= 1
            tpb = tpa
            tp = 0
        #Draw
        thumby.display.fill(0)
        if(((foxylocation == 3)&(camUp == 2))|(foxyframe > 0)):
            if(camUp == 2):
                foxyframe += (cam == 3)
            else:
                foxyframe += 1
            if(foxyframe == 3):
                x = 3
                polysynth.play(sfx(0))
            if(foxyframe > 30):
                if(leftDoorClosed == 0):
                    jumpnum = 3
                    fail = 1
                if(foxyframe == 31):
                    x = 3
                    polysynth.play(sfx(1))
                if(foxyframe>60):
                    foxylocation = 0
                    power -= 1+(5*foxydrain)
                    foxyframe = 0
                    foxydrain += 1
            if(foxyframe < 31):
                camstate = foxyframe
        if(camUp != 2):
            if(power < 0):
                if(freddylocation < 2):
                    spr_office.setFrame(1)
                    spr_office.x = -scrollx
                    thumby.display.drawSprite(spr_office)
                    thumby.display.drawSprite(spr_fan)
                    if(drawFreddy):
                        thumby.display.blit(bit_0,6-scrollx,12,8,8,-1,0,0)
            else:
                spr_office.setFrame(0)
                spr_office.x = -scrollx
                thumby.display.drawSprite(spr_office)
                spr_fan.setFrame((thumby.Sprite.getFrame(spr_fan))+1)
                thumby.display.drawSprite(spr_fan)
            spr_litWindowL.x = 16-scrollx
            spr_litWindowL.y = 8
            spr_litWindowR.x = 76-scrollx
            spr_litWindowR.y = 8
            spr_doors.y = 1
            spr_doorsw.y = 1
            spr_fan.x = 53-scrollx
            spr_fan.y = 14
            if(random.randint(0,5)>0)&(leftDoorLit == 1):
                spr_doors.x = 5-scrollx
                if(bonnielocation == 6):
                    spr_doors.setFrame(19)
                    spr_litWindowL.setFrame(1)
                    if(bstinger == 0):
                        polysynth.playnote(0, 80, polysynth.instrument(length=500))
                        bstinger = 1
                else:  
                    spr_doors.setFrame(18)
                    spr_litWindowL.setFrame(0)
                thumby.display.drawSprite(spr_doors)
                thumby.display.drawSprite(spr_litWindowL)
            if(random.randint(0,5)>0)&(rightDoorLit == 1):
                spr_doors.x = 86-scrollx
                spr_doors.setFrame(20)
                if(chicalocation == 6):
                    spr_litWindowR.setFrame(1)
                    if(cstinger == 0):
                        polysynth.playnote(0, 80, polysynth.instrument(length=500))
                        cstinger = 1
                else:
                    spr_litWindowR.setFrame(0)
                thumby.display.drawSprite(spr_doors)
                thumby.display.drawSprite(spr_litWindowR)
            if(leftDoorClosed == 1):
                spr_doors.x = 5-scrollx
                spr_doorsw.x = 5-scrollx
                if(lDoorClosedFrame<8):
                    lDoorClosedFrame += 1
                spr_doors.setFrame(lDoorClosedFrame)
                thumby.display.drawSprite(spr_doors)
                spr_doorsw.setFrame(lDoorClosedFrame+9)
                thumby.display.drawSprite(spr_doorsw)
            elif(lDoorClosedFrame>0):
                lDoorClosedFrame -= 1
                spr_doors.x = 5-scrollx
                spr_doorsw.x = 5-scrollx
                spr_doors.setFrame(lDoorClosedFrame)
                thumby.display.drawSprite(spr_doors)
                spr_doorsw.setFrame(lDoorClosedFrame+9)
                thumby.display.drawSprite(spr_doorsw)
            if(rightDoorClosed == 1):
                spr_doors.x = 86-scrollx
                spr_doorsw.x = 86-scrollx
                spr_doors.mirrorX = 1
                spr_doorsw.mirrorX = 1
                if(rDoorClosedFrame<8):
                    rDoorClosedFrame += 1
                spr_doors.setFrame(rDoorClosedFrame)
                thumby.display.drawSprite(spr_doors)
                spr_doorsw.setFrame(rDoorClosedFrame+9)
                thumby.display.drawSprite(spr_doorsw)
                spr_doors.mirrorX = 0
                spr_doorsw.mirrorX = 0
            elif(rDoorClosedFrame>0):
                rDoorClosedFrame -= 1
                spr_doors.x = 86-scrollx
                spr_doorsw.x = 86-scrollx
                spr_doors.mirrorX = 1
                spr_doorsw.mirrorX = 1
                spr_doors.setFrame(rDoorClosedFrame)
                thumby.display.drawSprite(spr_doors)
                spr_doorsw.setFrame(rDoorClosedFrame+9)
                thumby.display.drawSprite(spr_doorsw)
                spr_doors.mirrorX = 0
                spr_doorsw.mirrorX = 0
            if(goldenappear == 1):
                # BITMAP: width: 25, height: 24
                bit_0 = bytearray([0,0,0,0,0,0,140,122,252,60,60,143,203,123,56,48,192,128,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,48,253,255,143,255,83,0,8,0,72,131,7,12,12,128,0,0,0,0,
                        48,16,48,48,48,254,239,227,224,255,239,224,224,120,227,247,247,247,225,238,233,251,112,112,32])
                thumby.display.blit(bit_0,37-scrollx,16,25,24,0,0,0)
                # BITMAP: width: 25, height: 24
                bit_0 = bytearray([255,255,255,255,255,255,191,251,253,63,63,143,203,123,60,55,255,191,255,255,255,255,255,255,255,
                       255,255,255,255,255,253,124,253,255,143,255,83,0,8,0,72,131,7,15,15,151,255,255,255,255,
                       191,159,191,63,63,255,239,227,224,255,239,224,224,120,227,247,247,247,229,238,233,251,123,127,255])
                thumby.display.blit(bit_0,37-scrollx,16,25,24,1,0,0)
                if(random.randint(0,7)==0):
                    if(random.randint(0,3)==0):
                        spr_jumpscare = thumby.Sprite(72,40,"/Games/TinyFreddy/Jumpscares.bin",0,0)
                        spr_jumpscare.setFrame(96+random.randint(0,3))
                        thumby.display.drawSprite(spr_jumpscare)
                    else:
                        thumby.display.fill(0)
                        thumby.display.drawText("ITS ME",random.randint(0,47),random.randint(0,35),1)
                    thumby.display.update()
                    thumby.display.update()
                    thumby.display.update()
            if(camUp == 1):
                freevar[0] == thumby.Sprite.getFrame(spr_camup)
                if(thumby.Sprite.getFrame(spr_camup)<6):
                    spr_camup.setFrame((thumby.Sprite.getFrame(spr_camup))+1)
                    thumby.display.drawSprite(spr_camup)
                    spr_camup.key = 1
                    spr_camup.setFrame(thumby.Sprite.getFrame(spr_camup)+7)
                    thumby.display.drawSprite(spr_camup)
                    spr_camup.key = 0
                    spr_camup.setFrame((thumby.Sprite.getFrame(spr_camup))-7)
                if(thumby.Sprite.getFrame(spr_camup) == 6):
                    camUp = 2
            elif(thumby.Sprite.getFrame(spr_camup)>0):
                spr_camup.setFrame((thumby.Sprite.getFrame(spr_camup))-1)
                thumby.display.drawSprite(spr_camup)
                spr_camup.key = 1
                spr_camup.setFrame(thumby.Sprite.getFrame(spr_camup)+7)
                thumby.display.drawSprite(spr_camup)
                spr_camup.key = 0
                spr_camup.setFrame((thumby.Sprite.getFrame(spr_camup))-7)
        else:
            if(goldenappear == 1):
                goldenappear = 2
                if((fail == 1)&(jumpnum == 5)):
                    fail = 0
            TFcameras.getcamera(cam,camstate,freddylocation,bonnielocation,chicalocation,foxylocation)
            TFcameras.static(frame,staticmode)
            TFcameras.camMap(cam,camMode)
        #GUI
        thumby.display.drawFilledRectangle(53,0,20,hudy,0)
        thumby.display.drawFilledRectangle(0,0,12,hudy,0)
        ampre = am
        am = math.floor(t0/70000)
        if(ampre != am):
            if(night == 1):
                if(am == 1):
                    animAI = [0,0,0,0,0]
                if(am == 2):
                    animAI = [0,1,0,0,0]
                if(am == 3):
                    animAI = [0,2,1,1,0]
                if(am == 4):
                    animAI = [0,3,2,2,0]
                if(am == 5):
                    animAI = [0,3,2,2,0]
            if(night == 2):
                if(am == 1):
                    animAI = [0,3,1,1,0]
                if(am == 2):
                    animAI = [0,4,1,1,0]
                if(am == 3):
                    animAI = [0,5,2,2,0]
                if(am == 4):
                    animAI = [0,6,3,3,0]
                if(am == 5):
                    animAI = [0,6,3,3,0]
            if(night == 3):
                if(am == 1):
                    animAI = [0,0,5,2,0]
                if(am == 2):
                    animAI = [1,1,5,2,0]
                if(am == 3):
                    animAI = [1,2,6,3,0]
                if(am == 4):
                    animAI = [1,3,7,4,0]
                if(am == 5):
                    animAI = [2,3,7,4,0]
            if(night == 4):
                if(am == 1):
                    animAI = [1,2,4,6,0]
                if(am == 2):
                    animAI = [random.randint(1,2),3,5,6,0]
                if(am == 3):
                    animAI = [2,4,6,7,0]
                if(am == 4):
                    animAI = [2,5,6,8,0]
                if(am == 5):
                    animAI = [random.randint(2,3),5,6,8,0]
            if(night == 5):
                if(am == 1):
                    animAI = [2,5,7,5,1]
                if(am == 2):
                    animAI = [3,6,7,5,1]
                if(am == 3):
                    animAI = [3,7,8,6,1]
                if(am == 4):
                    animAI = [4,8,9,7,1]
                if(am == 5):
                    animAI = [4,8,9,7,1]
            if(night == 6):
                if(am == 1):
                    animAI = [4,10,12,16,4]
                if(am == 2):
                    animAI = [5,11,12,16,4]
                if(am == 3):
                    animAI = [5,12,13,17,4]
                if(am == 4):
                    animAI = [6,13,14,18,4]
                if(am == 5):
                    animAI = [6,13,14,18,4]
            if(night == 7):
                if(random.randint(0,15) == 0):
                    animAI[0] += (animAI[0]<20)
                if(random.randint(0,15) == 0):
                    animAI[1] += (animAI[1]<20)
                if(random.randint(0,15) == 0):
                    animAI[2] += (animAI[2]<20)
                if(random.randint(0,15) == 0):
                    animAI[3] += (animAI[3]<20)
                if(random.randint(0,31) == 0):
                    animAI[4] += (animAI[4]<20)
            freddydifficulty = animAI[0]
            bonniedifficulty = animAI[1]
            chicadifficulty = animAI[2]
            foxydifficulty = animAI[3]
            goldendifficulty = animAI[4]
        if(hud == 1)|(hudy > 0):
            string = power
            if(power>9):
                string = str(power)+"%"
            else:
                if(power>-1):
                    string = "0"+str(power)+"%"
                else:
                    string = "00%"
            thumby.display.drawText(string,0,-6+hudy,1)
            if(am == 0):
                string = "12:AM"
            else:
                string = str(am)+":AM"
            thumby.display.drawText(string,57-4*(am == 0),-6+hudy,1)
            thumby.display.drawLine(0,hudy,8,hudy,0)
            for freevar[0] in range(0,(powerusage*2)+1,2):
                thumby.display.setPixel(freevar[0],hudy,1)
        frame += 1
        frame = frame % 30030
        if((powerout == 0)&(audiomode == 0)):
            rsclocka = time.ticks_ms()
            if((rsclocka-rsclockb)>=30000):
                rand = random.randint(0,5)
                if(rand<3):
                    polysynth.playnote(1, 55+rand*25, polysynth.instrument(rise=-5+10*(rand<0), length=2000))
                elif(rand == 3):
                    polysynth.play(foxySong)
                elif(rand == 4):
                    polysynth.play(jukeBoxSong)
                else:
                    polysynth.play(metroidReferenceSong)
                rsclockb = rsclocka
        thumby.display.update()
    polysynth.stop()
    if(fail == 1):
        if(jumpnum == 4):
            done = 41
        else:
            done = 56
        frame = 0
        framestart = [0,10,25,53,73,95]
        framelimit = [9,14,27,20,21,0]
        spr_jumpscare = thumby.Sprite(72,40,"/Games/TinyFreddy/Jumpscares.bin",0,0)
        if(jumpnum == 5):
            x = 0
            polysynth.play(sfx(5),loop=True)
        else:
            x = 0
            polysynth.play(sfx(4),loop=True)
        while(done > 0):
            done -= 1
            t0b = time.ticks_ms()
            t0 = t0b-t0a
            am = math.floor(t0/70000)
            if(am == 6):
                done = 0
            frame += 0.5
            if(frame > framelimit[jumpnum]):
                if(jumpnum == 3):
                    frame -= 0.5
                else:
                    frame = 0
            thumby.display.fill(0)
            spr_jumpscare.setFrame(round(frame+framestart[jumpnum]))
            thumby.display.drawSprite(spr_jumpscare)
            thumby.display.update()
        if(am != 6):
            fail = 2
            polysynth.stop()
    if(am == 6):
        done = 600
        thumby.display.setFont("/lib/font8x8.bin", 8, 8, 1)
        if(EMULATOR == 0):
            if(night != 7):
                thumby.saveData.setItem("progress", night+1-(night>4))
                thumby.saveData.save()
        while(done > 0):
            done -= 1
            thumby.display.fill(0)
            if(done > 420):
                thumby.display.drawText("5:AM",18,16,1)
            elif(done > 300):
                thumby.display.drawText("5",18,16-int((done-420)/2),1)
                thumby.display.drawText("6",18,16-int((done-300)/2),1)
                thumby.display.drawText(":AM",27,16,1)
            else:
                thumby.display.drawText("6:AM",18,16,1)
            thumby.display.update()
    
    if(fail == 2):
        done = 300
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
        spr_office = thumby.Sprite(72,40,"/Games/TinyFreddy/Title.bin",0,0)
        spr_office.setFrame(5)
        while(done > 0):
            done -= 1
            thumby.display.fill(0)
            thumby.display.drawSprite(spr_office)
            thumby.display.drawText("Game Over",38,35,1)
            thumby.display.update()
    
    if((fail == 2)|(night > 4)):
        if(fail == 0):
            thumby.buttonA.justPressed()
            thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
            spr_office = thumby.Sprite(72,40,"/Games/TinyFreddy/Title.bin",0,0)
            spr_office.setFrame(6)
            if(audiomode == 1):
                song = midi.load(open("/Games/TinyFreddy/Music/Toreador.mid", "rb"),mute=[1])
            else:
                song = midi.load(open("/Games/TinyFreddy/Music/Toreador.mid", "rb"))
            polysynth.play(song)
            y = 0
            yscroll = 0
            while(done == 0):
                if(thumby.buttonA.justPressed()):
                    if(yscroll != 40):
                        y = 40
                    else:
                        done = 1
                if(y>yscroll):
                    yscroll += 1
                thumby.display.fill(0)
                if(night == 5):
                    thumby.display.drawText("Good job, sport!",4,0-yscroll,1)
                    thumby.display.drawText("See you next week",2,6-yscroll,1)
                    thumby.display.drawText("Payment: $120",10,19-yscroll,1)
                if(night == 6):
                    thumby.display.drawText("Good job, sport!",4,0-yscroll,1)
                    thumby.display.drawText("You've earned some",0,6-yscroll,1)
                    thumby.display.drawText("overtime!",0,12-yscroll,1)
                    thumby.display.drawText("Payment: $120+50c",3,19-yscroll,1)
                if(night == 7):
                    thumby.display.drawText("Notice:Termination",0,0-yscroll,1)
                    thumby.display.drawText("You're fired!",6,7-yscroll,1)
                    thumby.display.drawText("Reason: tampering",2,15-yscroll,1)
                    thumby.display.drawText("with things, odor",2,21-yscroll,1)
                spr_office.y = 40-yscroll
                thumby.display.drawSprite(spr_office)
                thumby.display.drawFilledRectangle(44, 74-yscroll, 30, 6, 0)
                thumby.display.drawText("THE END",45,75-yscroll,1)
                thumby.display.update()
        
        return "title0"
    else:
        night += 1
        return "game"

while(gamestate != "exit"):
    if(gamestate == "game"):
        gamestate = game()
    elif(gamestate == "title0"):
        gamestate = title(0)
    elif(gamestate == "title1"):
        gamestate = title(1)
