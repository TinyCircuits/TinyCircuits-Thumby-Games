import gc
gc.enable()
import time
import thumby
import math
import random
import math
import ujson
import sys
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, TextForScroller, Item, Monster, AttackMove
from funcLib import thingAquired, printMon, showOptions, showMonInfo, tameMon, save


def buy(itemList, player):
    if len(player.inventory) >= player.maxHelditems:
        thingAquired("Your", "inventory", "is already", "full!", 2, 0, 0)
    else:
        thingAquired("Everything", "is on", "sale for 10", "Tiny Coins!", 1, 0, 0)
        bottomScreenText = "Tiny Coins: " + str(player.playerBlock['money'])
        curSelect = 0
        tempSelect = curSelect
        optionList = []
        i = 0
        for items in itemList:
            i = i+1
            optionList.append(str(i) + ". " + itemList[i-1])
        while curSelect < 11:
            bottomScreenText = "TinyCoins:" + str(player.playerBlock['money'])
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect == 31:
                if player.playerBlock['money'] > 9:
                    if tempSelect < 0:
                        tempSelect += 6
                    newItem = Item("GenHeal", 1)
                    if itemList[tempSelect] == "Crystals":
                        tempSelect = 14
                    newItem.getItem(1, tempSelect)
                    player.inventory.append(newItem)
                    player.playerBlock['money'] -= 10 
                    thingAquired("You", "purchased", newItem.name, "", 1,0,0)
                else:
                    thingAquired("You", "don't have", "enough", "Tiny Coins!", 1,0,0)
            elif curSelect == 30:
                pass
            elif curSelect > 11:
                curSelect = tempSelect
            thumby.display.update()
    thumby.display.fill(0)


def sell(player):
    if len(player.inventory) <= 0:
        thingAquired("You", "don't have", "anything", "to sell!", 2, 0, 0)
    else:
        thingAquired("I will", "buy any", "item for 5", "Tiny Coins!", 1, 0, 0)
        bottomScreenText = "Tiny Coins: " + str(player.playerBlock['money'])
        curSelect = 0
        tempSelect = curSelect
        optionList = []
        i = 0
        for items in player.inventory:
            i = i+1
            optionList.append(str(i) + ". " + items.name)
        while curSelect < 11:
            bottomScreenText = "TinyCoins:" + str(player.playerBlock['money'])
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect ==  31:
                itemName = player.inventory[tempSelect].name
                player.inventory.pop(tempSelect)
                player.playerBlock['money'] += 5
                thingAquired("You sold", itemName, "for 5", "Tiny Coins!", 1, 0, 0)
            elif curSelect == 30:
                pass
            elif curSelect > 11:
                curSelect = tempSelect
            thumby.display.update()
    thumby.display.fill(0)


def stayBring(player, sOrB):
    tempPlayer = Player()
    try:
        tempPlayer = loadGame("campfire")
    except:
        pass
    tempPlayer.playerBlock['friendMax'] = 4
    
    if sOrB == 0:
        stay(player, tempPlayer)
    if sOrB == 1:
        bring(player, tempPlayer)
    if sOrB == 2:
        release(tempPlayer)
    save(tempPlayer, "campfire")    
    del tempPlayer

def bring(player, tempPlayer):
    if len(tempPlayer.friends) > 0 and len(tempPlayer.friends) <= tempPlayer.playerBlock['friendMax'] and len(player.friends) < player.playerBlock['friendMax']:
        takeWith = showMonInfo(tempPlayer, 0, 0, 1)
        if takeWith == 1:
            tameMon(player, tempPlayer.friends[0], tempPlayer.friends[0].statBlock)
            tempPlayer.friends.pop(0)
        tempPlayer.playerBlock['name'] = "Campfire"
    elif len(tempPlayer.friends) == 0:
        thingAquired("There aren't", "any", "monsters", "at the camp!", 2, 0, 0)
    else:
        thingAquired("You have", "too many", "monsters", "leave one!", 2, 0, 0)

    
def stay(player, tempPlayer):
    if len(tempPlayer.friends) < (tempPlayer.playerBlock['friendMax']-1) and len(player.friends) > 1:
        stayBehind = showMonInfo(player, 0, 0, 2)
        if stayBehind == 1:
            tameMon(tempPlayer, player.friends[0], player.friends[0].statBlock)
            player.friends.pop(0)
    elif len(player.friends) < 2:
        thingAquired("You need", "to keep", "at least", "one monster!", 2, 0, 0)
    else:
        stayBehind = showMonInfo(player, 0, 0, 2)
        if stayBehind == 1:
            tameMon(tempPlayer, player.friends[0], player.friends[0].statBlock)
            player.friends.pop(0)
        while(len(tempPlayer.friends) == tempPlayer.playerBlock['friendMax']):
            thingAquired("The Camp", "is full!", "Take a", "monster!", 2, 0, 0)
            bring(player, tempPlayer)


def release(tempPlayer):
    if len(tempPlayer.friends) > 0:
        release = showMonInfo(tempPlayer, 0, 0, 3)
        if release == 1:
            tempPlayer.friends.pop(0)
    elif len(tempPlayer.friends) == 0:
        thingAquired("There aren't", "any", "monsters", "at the camp!", 2, 0, 0)

def drawCharScreen(chair, player):
    myScroller = TextForScroller(chair.scollerTxt)
    # BITMAP: width: 20, height: 8
    BG = bytearray([96,80,72,72,80,80,96,0,0,16,40,36,36,36,40,40,40,48,0,0]) 
    
    '''#36x29
    bytearray([0,0,48,40,36,44,40,40,48,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,96,80,80,80,72,72,88,80,112,32,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
            0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])'''
    background = thumby.Sprite(20, 8, BG)  
    background.x = 0
    background.y = 2
    curSelect = 1
    tempSelect = curSelect
    cancelCheck = 0
    spriteCtr = 0
    bgCtr = 0
    c0 = time.ticks_ms()
    while cancelCheck != 1:
        thumby.display.fill(0)
        thumby.display.drawSprite(background)
        t0 = time.ticks_ms()
        bottomScreenText = ""
        tempSelect = curSelect
        curSelect = showOptions(chair.optionList, curSelect, bottomScreenText, 36, 1)
        if curSelect == 28 or curSelect == 29:
            curSelect = tempSelect
        if curSelect == 30:
            cancelCheck = 1
        if curSelect == 31:
            curSelect = tempSelect
            if chair.optionList[curSelect] == "Buy":
                buy(chair.items2Sell, player)
            elif chair.optionList[curSelect] == "Sell":
                sell(player)
            elif chair.optionList[curSelect] == "Leave":
                stayBring(player, 0)
            elif chair.optionList[curSelect] == "Bring":
                stayBring(player, 1)
            elif chair.optionList[curSelect] == "Spar":
                pass
            elif chair.optionList[curSelect] == "Let Go":
                stayBring(player, 2)
            elif chair.optionList[curSelect] == "Bye":
                cancelCheck = 1
            
                
        thumby.display.drawFilledRectangle(0, 30, 72, 10, 0)    
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 31, 1)
        thumby.display.drawSpriteWithMask(chair.sprite[0], chair.sprite[1])
        thumby.display.drawRectangle(0, 0, 36, 30, 1)
        thumby.display.update()
        if t0 - c0 > 300:
            c0 = time.ticks_ms()
            spriteCtr += 1
            chair.sprite[0].setFrame(spriteCtr)
            chair.sprite[1].setFrame(spriteCtr)
            bgCtr += 1
            if bgCtr == 3:
                background.x -= 1
                bgCtr = 0
                if background.x < -22:
                    background.x = 36
    return 0


def loadGame(name="campfire"):
    gc.collect()
    tempPlayer = Player()
    f = open('/Games/Tiny_Monster_Trainer/Curtain/'+name+'.ujson')
    bigJson = ujson.load(f)
    tempPlayer.playerBlock = bigJson[0]['player'].copy()
    if bigJson[0]['items'] != [{}]:
        for x in range(0, len(bigJson[0]['items'][0])):
            tempPlayer.inventory.append(Item(bigJson[0]['items'][0]['item' + str(x)]['name'],
                                            bigJson[0]['items'][0]['item' + str(x)]['key'],
                                            bigJson[0]['items'][0]['item' + str(x)]['bonus']))
    for x in range(0, len(bigJson[0]['monsterInfo'][0])):
        tempMon = Monster()
        tempMon.statBlock = bigJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat'].copy()
        tempMon.bodyBlock = bigJson[0]['monsterInfo'][1]['mon' + str(x) + 'body'].copy()
        tempMon.mutateSeed = bigJson[0]['monsterInfo'][3]['mon' + str(x) + 'mutate'].copy()
        try:
            tempMon.bonusStats = bigJson[0]['monsterInfo'][4]['mon' + str(x) + 'bonus'].copy() 
        except:
            pass
        for y in range(0, len(bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])): 
            tempAttackMove = AttackMove(bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['name'], 
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['numUses'],
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['baseDamage'],
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['magic'],
                                        bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['moveElementType'])
            tempAttackMove.currentUses = bigJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['currentUses']
            tempMon.attackList.append(tempAttackMove) 
        tempMon.attackList = tempMon.attackList.copy()
        tempPlayer.friends.append(tempMon)
        tempPlayer.friends = tempPlayer.friends.copy()
    f.close()
    del bigJson
    return tempPlayer


class Character:
    def __init__(self):
        self.playerBlock = {'name' : "Campfire",
                        'trainerLevel' : 1,
                        'friendMax' : 2,
                        'inspire' : 0}
        self.friends = []
        self.items2Sell = []
        self.optionList = []
        self.sprite = []
        self.scollerTxt =""
        #self.spar = 0

        
        
    def getCharacter(self, who):
        # BITMAP: width: 36, height: 29 = All Character sprites
        if who == 0:
            frame1 = bytearray([0,0,0,0,0,0,0,192,112,24,12,4,2,2,130,2,132,230,2,194,130,2,134,6,4,12,24,224,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,255,1,0,0,0,0,126,251,247,227,231,255,159,123,247,226,231,254,0,0,128,255,0,0,0,0,0,0,0,0,
                        0,0,0,0,112,144,32,33,25,142,128,64,33,7,15,159,251,247,182,186,31,15,195,96,56,12,7,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,1,3,2,2,28,6,2,18,11,7,7,12,27,12,7,7,11,19,6,24,0,0,0,0,0,0,0,0,0,0,0])
            frame2 = bytearray([0,0,0,0,0,0,0,192,112,24,12,4,2,2,2,130,196,102,130,194,130,2,134,6,4,24,48,192,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,255,1,0,0,0,192,254,251,247,227,231,255,159,123,246,227,231,62,0,0,240,31,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,128,64,33,25,142,128,64,33,7,15,159,251,247,182,154,15,135,97,48,24,15,3,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,3,2,2,2,2,28,6,2,18,11,7,7,12,27,12,7,7,11,19,6,24,0,0,0,0,0,0,0,0,0,0,0])
            frameM1 = bytearray([0,0,0,0,0,0,0,192,240,248,252,252,254,254,254,254,252,254,254,254,254,254,254,254,252,252,248,224,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,0,0,0,0,0,0,0,0,
                        0,0,0,0,112,240,224,225,249,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,15,7,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,1,3,3,3,31,31,31,31,31,31,31,31,31,31,31,31,31,31,30,24,0,0,0,0,0,0,0,0,0,0,0])
            frameM2 = bytearray([0,0,0,0,0,0,0,192,240,248,252,252,254,254,254,254,252,254,254,254,254,254,254,254,252,248,240,192,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,128,192,225,249,255,255,255,255,255,255,255,255,255,255,255,255,255,127,63,31,15,3,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,3,3,3,3,3,31,31,31,31,31,31,31,31,31,31,31,31,31,31,30,24,0,0,0,0,0,0,0,0,0,0,0])

            if random.randint(0,2) == 1:
                self.items2Sell = ["Crystals"]
            else:
                self.items2Sell = ["Stickers", "Vitamins", "Helium", "Pillows", "Stardust", "Tinfoil"]
            self.optionList = ["Buy", "Sell", "Bye"]
            self.scollerTxt ="Greetings! I'm Bean, the traveling merchant! Would you like to Buy, Sell, or Spar?"
            self.playerBlock['name'] = "Bean"
            self.playerBlock['trainerLevel'] = 80
            
        elif who == -1:
            frame1 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,128,240,30,2,243,1,0,31,48,224,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,31,112,192,143,24,32,32,11,132,192,115,15,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        16,16,16,16,24,24,24,24,28,30,31,31,31,27,25,25,17,17,25,25,27,31,31,31,30,28,24,24,24,24,24,16,16,16,16,16])
            frame2 =  bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,32,48,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,224,56,4,198,3,0,56,225,3,14,248,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,30,115,192,128,19,48,48,24,135,192,112,15,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        16,16,16,16,24,24,24,24,28,30,31,31,31,27,25,25,17,17,25,25,27,31,31,31,30,28,24,24,24,24,24,16,16,16,16,16])
            frameM1 = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,128,240,254,254,255,255,255,255,240,224,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,31,127,255,255,255,255,255,255,255,255,127,15,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        16,16,16,16,24,24,24,24,28,30,31,31,31,31,31,31,31,31,31,31,31,31,31,31,30,28,24,24,24,24,24,16,16,16,16,16])
            frameM2 =  bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,224,240,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,0,224,248,252,254,255,255,255,255,255,254,248,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        0,0,0,0,0,0,0,0,0,0,0,30,127,255,255,255,255,255,255,255,255,127,15,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        16,16,16,16,24,24,24,24,28,30,31,31,31,31,31,31,31,31,31,31,31,31,31,31,30,28,24,24,24,24,24,16,16,16,16,16])
            self.optionList = ["Leave", "Bring", "Let Go", "Bye"]
            self.scollerTxt ="You are at your camp. Would you like to leave a monster, or bring one with you?"
        
        sprite = thumby.Sprite(36, 29, frame1 + frame2)
        sprite.x = 0
        sprite.y = 1
        spriteM = thumby.Sprite(36, 29, frameM1 + frameM2)
        self.sprite = [sprite, spriteM]
