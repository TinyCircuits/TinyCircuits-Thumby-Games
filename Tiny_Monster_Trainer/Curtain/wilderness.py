import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys 
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Map, Monster, Tile, RoamingMonster, TextForScroller, Item, AttackMove, NPC
from funcLib import thingAquired, battleStartAnimation, printMon, drawArrows, showOptions, popItOff, buttonInput, noDupAtk, giveName, tameMon, switchActiveMon, save, showMonInfo
#import micropython


def worldRangeCheck(test):
    if test >= 19:
        test = test - 25
    if test <= -19:
        test = test + 25
    return test


def mapChangeCheck(player, worldMap, worldRoom):
    if worldMap.floor[player.currentPos].isObjectHere == 2:
        if player.currentPos == 4:
            player.position[player.currentPos] = 0
            player.currentPos = 31
            player.position[player.currentPos] = 1
            worldRoom = worldRoom - 5
            worldRoom = worldRangeCheck(worldRoom)
        elif player.currentPos == 40:
            player.position[player.currentPos] = 0
            player.currentPos = 13
            player.position[player.currentPos] = 1
            worldRoom = worldRoom + 5
            worldRoom = worldRangeCheck(worldRoom)
        elif player.currentPos == 26:
            player.position[player.currentPos] = 0
            player.currentPos = 19
            player.position[player.currentPos] = 1
            worldRoom = worldRoom + 1
            worldRoom = worldRangeCheck(worldRoom)
        elif player.currentPos == 18:
            player.position[player.currentPos] = 0
            player.currentPos = 25
            player.position[player.currentPos] = 1
            worldRoom = worldRangeCheck(worldRoom)
            worldRoom = worldRoom - 1
    worldMap.displayMap()
    return worldRoom

    
def noDupAtk(currentAttackList):
    checkingTotal = 0
    listRangeCheck = 0
    for attacksKnown in currentAttackList:
        checkingTotal = checkingTotal + 1
    for i in range(0, checkingTotal):
        for n in range(0, checkingTotal):
            if i <= (i - listRangeCheck):
                if (currentAttackList[i].name == currentAttackList[n].name) and (i != n):
                    currentAttackList.pop(n)
                    listRangeCheck = listRangeCheck + 1


def autoSwitchMon(playerInfo):
    if playerInfo.friends[0].statBlock['currentHealth'] < 1:
        x = 0
        for monsters in playerInfo.friends:
            if playerInfo.friends[x].statBlock['currentHealth'] > 0:
                switchActiveMon(playerInfo, playerInfo.friends[0], playerInfo.friends[x], x)
            x = x + 1
        if playerInfo.friends[0].statBlock['currentHealth'] > 0:
            thingAquired(playerInfo.friends[0].statBlock['given_name'], "is now", "your active", "monster!", 2)


def playerInformation(playerInfo):
    thumby.display.fill(0)
    waiting = True
    back = 0
    while(back < 29):
        if back == 0:
            thumby.display.drawText(playerInfo.playerBlock['name'], 1, 1 ,1)
            thumby.display.blit(bytearray(playerInfo.sprite), 60, 27, 8, 8, 0, 0, 0)
            thumby.display.drawText("Lvl: " + str(playerInfo.playerBlock['trainerLevel']), 1, 10, 1)
            thumby.display.drawText("Exp: " + str(playerInfo.playerBlock['experience']), 1, 19, 1)
            thumby.display.drawText("Mons: " + str(len(playerInfo.friends)) + "/" + str(playerInfo.playerBlock['friendMax']), 1, 28, 1)
            thumby.display.update()
            back = buttonInput(back)
            if back > 29:
                waiting = False
            else:
                back = 0


def displayItems(playerInfo):
    thumby.display.fill(0)
    curSelect = 0
    tempSelect = curSelect
    cancelCheck = 0
    optionList = []
    i = 0
    for items in playerInfo.inventory:
        i = i+1
        optionList.append(str(i) + ". " + items.name)
    x = len(optionList)
    if x > 0:
        while curSelect < 11:
            bottomScreenText = ("CurHP:" + str(playerInfo.friends[0].statBlock['currentHealth']))
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect ==  31:
                playerInfo.inventory[tempSelect].doAction(playerInfo.friends[0])
                thingAquired(playerInfo.playerBlock['name'],
                "gave", playerInfo.friends[0].statBlock['given_name'],
                playerInfo.inventory[tempSelect].name, 2)
                playerInfo.inventory.pop(tempSelect)
            elif curSelect == 30:
                pass
            elif curSelect > 11:
                curSelect = tempSelect
            thumby.display.update()
    else:
        pass


def trainActiveMon(myMonStats, monsterBody):
    #gc.collect()
    thumby.display.fill(0)
    healthAmtTxt = (str(myMonStats['Health']) + '/' + str(myMonStats['maxHealth']))
    agileAmtTxt = (str(myMonStats['Agility']) + '/' + str(myMonStats['maxAgility']))
    strengthAmtTxt = (str(myMonStats['Strength']) + '/' + str(myMonStats['maxStrength']))
    enduranceAmtTxt = (str(myMonStats['Endurance']) + '/' + str(myMonStats['maxEndurance']))
    mystAmtTxt = (str(myMonStats['Mysticism']) + '/' + str(myMonStats['maxMysticism'])) 
    tinfoilAmtTxt = (str(myMonStats['Tinfoil']) + '/' + str(myMonStats['maxTinfoil']))
    trainingPointsTxt = ("TP: " + str(myMonStats['trainingPoints']))
    statNameList = ["Health", "Agility", "Strength", "Endurance", "Mysticism", "Tinfoil"]
    statNumsList = [healthAmtTxt, agileAmtTxt, strengthAmtTxt, enduranceAmtTxt, mystAmtTxt, tinfoilAmtTxt]
    goBack = 0
    currentSelect = 1
    tempSelect = currentSelect
    while goBack != 1:
        if currentSelect > 6 - 2 :
            currentSelect = currentSelect - 6
        if currentSelect < -6 + 2:
            currentSelect = currentSelect + 6
        thumby.display.fill(0)
        thingAquired(statNameList[currentSelect], statNumsList[currentSelect], trainingPointsTxt, myMonStats['given_name'], 0, 1)
        drawArrows(1, 1, -1, -1)
        tempSelect = currentSelect
        currentSelect = buttonInput(currentSelect)
        if currentSelect == 28 or currentSelect == 29:
            currentSelect = tempSelect
        elif currentSelect == 30: 
            goBack = 1
        elif currentSelect == 31:
            currentSelect = tempSelect
            if myMonStats['trainingPoints'] > 0:
                if statNameList[currentSelect] == "Health" and myMonStats['Health'] < myMonStats['maxHealth']: 
                    myMonStats['Health'] = myMonStats['Health'] + 1
                    myMonStats['currentHealth'] = myMonStats['Health']
                    trainJumpRope(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "health!", 2) 
                elif statNameList[currentSelect] == "Agility" and myMonStats['Agility'] < myMonStats['maxAgility']: 
                    myMonStats['Agility'] = myMonStats['Agility'] + 1
                    trainJumpRope(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "agility!", 2)
                elif statNameList[currentSelect] == "Strength" and myMonStats['Strength'] < myMonStats['maxStrength']: 
                    myMonStats['Strength'] = myMonStats['Strength'] + 1
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "strength!", 2)
                elif statNameList[currentSelect] == "Endurance"  and myMonStats['Endurance'] < myMonStats['maxEndurance']: 
                    myMonStats['Endurance'] = myMonStats['Endurance'] + 1
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "endurance", 2)
                elif statNameList[currentSelect] == "Mysticism" and myMonStats['Mysticism'] < myMonStats['maxMysticism']: 
                    myMonStats['Mysticism'] = myMonStats['Mysticism'] + 1
                    trainCandles(monsterBody)
                    thingAquired(myMonStats['given_name'], "practiced", "their", "mysticism", 2)
                elif statNameList[currentSelect] == "Tinfoil" and myMonStats['Tinfoil'] < myMonStats['maxTinfoil']: 
                    myMonStats['Tinfoil'] = myMonStats['Tinfoil'] + 1
                    trainCandles(monsterBody)
                    thingAquired(myMonStats['given_name'], "polished", "their", "tinfoil", 2)
                else:
                    thingAquired("Stat is", "already", "maxed out", "", 2)
                    myMonStats['trainingPoints'] = myMonStats['trainingPoints'] + 1
                myMonStats['trainingPoints'] = myMonStats['trainingPoints'] - 1
            else:
                thingAquired("Not", "Enough", "Trainer", "Points", 2)
            thumby.display.update()
            goBack = 1
        thumby.display.update()


def inspireActive(playerBlock, myMonStats, monsterBonus):
    if playerBlock['inspire'] > 0: 
        inspireOpt = ["Dancing", "Flexing", "Running", "Meditation", "Origami", "Nevermind"]
        sOrNo = ""
        if playerBlock['inspire'] > 1 :
            sOrNo = 's'
        thingAquired("You can", "do " + str(playerBlock['inspire']), "act"+sOrNo + " of", "insperation!", 2, 0, 0)
        goBack = 0
        curSelect = 1
        while(goBack != 1):
            tempSelect = curSelect
            curSelect = showOptions(inspireOpt, curSelect, "Inspire By")
            if curSelect == 30:
                curSelect = 1
                goBack = 1
            if curSelect == 31:
                curSelect = tempSelect
                if inspireOpt[curSelect] == inspireOpt[0]:
                    myMonStats['maxAgility'] = myMonStats['maxAgility'] + 1
                elif inspireOpt[curSelect] == inspireOpt[1]:
                    myMonStats['maxStrength'] = myMonStats['maxStrength'] + 1
                elif inspireOpt[curSelect] == inspireOpt[2]:
                    myMonStats['maxEndurance'] = myMonStats['maxEndurance'] + 1
                elif inspireOpt[curSelect] == inspireOpt[3]:
                    myMonStats['maxMysticism'] = myMonStats['maxTinfoil'] + 1
                elif inspireOpt[curSelect] == inspireOpt[4]:
                    myMonStats['maxTinfoil'] = myMonStats['maxTinfoil'] + 1    
                else: #"Nevermind"
                    break
                thingAquired(myMonStats['given_name'], "was inspired", "by your", inspireOpt[curSelect], 2)
                myMonStats['maxHealth'] = myMonStats['maxHealth'] + 1
                myMonStats['trainingPoints'] = myMonStats['trainingPoints'] + 2
                monsterBonus['trained'] = monsterBonus['trained'] + 1
                playerBlock['inspire'] = playerBlock['inspire'] - 1
                goBack = 1
            thumby.display.update() 
    else:
        thingAquired("Level up", "to", "inspire", myMonStats['given_name'], 2, 0, 0)


def myMonSubMenu(playerInfo):
    goBack = 0
    curSelect = 1
    extraMenu = 1
    optionList = ["Info / Swap", "Train", "Learn Attack", "Give Name", "Mutate", "Back", "Inspire"]
    while(goBack != 1):
        thumby.display.fill(0)
        if curSelect == 28 or curSelect == 29:
            curSelect = tempSelect
        tempSelect = curSelect
        if playerInfo.playerBlock['inspire'] == 0 and extraMenu == 1:
            optionList.pop(6)
            extraMenu = 0
        curSelect = showOptions(optionList, curSelect, "My Friends")
        if curSelect == 31:
            curSelect = tempSelect
            if optionList[curSelect] == optionList[0]:
                showMonInfo(playerInfo)
            if optionList[curSelect] == optionList[1]:
                trainActiveMon(playerInfo.friends[0].statBlock, playerInfo.friends[0].bodyBlock)
            if optionList[curSelect] == optionList[2]:
                trainAnAttackMove(playerInfo.friends[0].attackList, playerInfo.friends[0].statBlock, playerInfo.friends[0].keyList)
                while len(playerInfo.friends[0].attackList) > 5:
                    popItOff(playerInfo.friends[0].attackList, "moves! Please forget one!")
            if optionList[curSelect] == optionList[3]:
                playerInfo.friends[0].statBlock['given_name'] = giveName(playerInfo.friends[0].statBlock['given_name'])
            if optionList[curSelect] == optionList[4]:
                mutateMon(playerInfo.friends[0])
            if optionList[curSelect] == optionList[5]:
                curSelect = 1
                goBack = 1
            if extraMenu == 1:
                if optionList[curSelect] == optionList[6]:
                    if playerInfo.friends[0].bonusStats['trained'] < 20:
                        inspireActive(playerInfo.playerBlock, playerInfo.friends[0].statBlock, playerInfo.friends[0].bonusStats)   
                    else:
                        thingAquired(playerInfo.friends[0].statBlock['giveName'], "is already", "full of", "insperation!", 2, 0, 0)
        if curSelect == 30:
            curSelect = 1
            goBack = 1
        thumby.display.update()


def optionScreen(playerInfo):
    if(thumby.buttonB.pressed() == True):
        while(thumby.buttonB.pressed() == True):
            pass
        thumby.display.fill(0)
        #gc.collect()
        curSelect = 1
        tempSelect = curSelect
        cancelCheck = 0
        optionList = ["My Info", "My Monsters", "Items", "Save", "Back"]
        while cancelCheck != 1:
            bottomScreenText = ("CurHP:" + str(playerInfo.friends[0].statBlock['currentHealth']))
            if curSelect == 28 or curSelect == 29:
                curSelect = tempSelect
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect == 31:
                curSelect = tempSelect
                if optionList[curSelect] == optionList[0]:
                    playerInformation(playerInfo)
                if optionList[curSelect] == optionList[1]:
                    myMonSubMenu(playerInfo)
                if optionList[curSelect] == optionList[2]:
                    displayItems(playerInfo)
                if optionList[curSelect] == optionList[3]:
                    save(playerInfo)
                    thingAquired("","Game","Saved","", 0, 1, 0)
                    thumby.display.drawRectangle(15, 7, 41, 22, 1)
                    thumby.display.update()
                    time.sleep(1.5)
                if optionList[curSelect] == optionList[4]: 
                    cancelCheck = 1
            if curSelect == 30:
                cancelCheck = 1
                thumby.display.fill(0)
            thumby.display.update()


def mutateMon(self):
    if self.statBlock['trainingPoints'] > 4:
        tempBody = self.bodyBlock.copy()
        if self.mutateSeed[1] < 4:
            random.seed(self.mutateSeed[0] + (self.mutateSeed[1] * 100))
            mutation = random.randint(1, 5)
            if mutation > 2 :
                mutation = random.randint(4, 8) 
                if mutation == 0 or mutation > 3 :
                  self.statBlock['max' + self.keyList[mutation]] = self.statBlock['max' + self.keyList[mutation]] + 10
            else:
                if (random.randint(1,3)) != 1:
                    self.makeMonBody()
                if self.statBlock['Type2'] == "":
                    self.statBlock['Type2'] = self.makeType()
                    myAttack = AttackMove()
                    randoNum = random.randint(1,4)
                    myAttack.getAnAttackMove(randoNum, self.statBlock['Type2'])
                    self.attackList.append(myAttack)
                    noDupAtk(self.attackList)
                elif self.statBlock['Type3'] == "":
                    self.statBlock['Type3'] = self.makeType()
                    myAttack = AttackMove()
                    randoNum = random.randint(1,4)
                    myAttack.getAnAttackMove(randoNum, self.statBlock['Type3'])
                    noDupAtk(self.attackList)
                self.statBlock['maxHealth'] = self.statBlock['maxHealth'] + 10
                for mutateX in range(4, 9):
                    self.statBlock['max' + self.keyList[mutateX]] = self.statBlock['max' + self.keyList[mutateX]] + 2
            self.mutateSeed[1] = self.mutateSeed[1] + 1
            self.statBlock['trainingPoints'] = self.statBlock['trainingPoints'] - 5 
            gc.collect()
            mutateAnimation(tempBody, self.bodyBlock)
            thingAquired(self.statBlock['given_name'], "has", "mutated!", "", 2)
        else:
            thingAquired(self.statBlock['given_name'], "is unable to", "mutate", "again", 2)
    else:
        howManyPoints = self.statBlock['trainingPoints']
        thingAquired(self.statBlock['given_name'], ("needs " + str(5 - howManyPoints) + " more"), "Training", "Points", 2)


def trainAnAttackMove(attackList, statBlock, keyList):
        #gc.collect()
        howManyTypes = 0
        newAttack = AttackMove()
        attacksKnown = len(attackList)
        attackLearned = 0
        noAttacksToLearn = 0
        if statBlock['trainingPoints'] >= 3:
            for x in range(1,4):
                if statBlock[keyList[x]] != "":
                    howManyTypes = howManyTypes + 1
            while(attackLearned != 1):
                learnFromType = random.randint(1,howManyTypes)
                selectionNumber = random.randint(1, 4)
                newAttack.getAnAttackMove(selectionNumber, statBlock[keyList[learnFromType]])
                attackList.append(newAttack)
                noDupAtk(attackList)
                checkKnownAttacks = len(attackList)
                if attacksKnown != checkKnownAttacks:
                    attackLearned = 1
                    thingAquired(statBlock['given_name'], "learned", attackList[-1].name, "", 2)
                    statBlock['trainingPoints'] = statBlock['trainingPoints'] - 3
                    break
                noAttacksToLearn = noAttacksToLearn  + 1
                if noAttacksToLearn == 30:
                    thingAquired(statBlock['given_name'], "did not", "learn a", "new attack", 2)
                    break
        else:
            howManyPoints = statBlock['trainingPoints'] 
            thingAquired(statBlock['given_name'], ("needs " + str(3 - howManyPoints) + " more"), "Training", "Points", 2)


def makeWorld(wSeed):
    gc.collect()
    thingAquired("", "Generating", "World","", 0)
    random.seed(wSeed) 
    worldList = []
    for i in range(0 , 25): # world size
        newMap = Map()
        newMap.procGenMap()
        worldList.append(newMap)
    return worldList


def findAnItem(playerInv, maxItems):
    #gc.collect()
    newItem = Item("GenHeal", 1)
    newItem.getItem()
    playerInv.append(newItem)
    thingAquired("You", "found", newItem.name, "", 2)
    if maxItems <= len(playerInv):
        popItOff(playerInv, "items! Please lose one.")


def printExciteLines(randoNum, randoNum2, randoNum3):
    thumby.display.drawLine(6+randoNum, 6+randoNum2, 18+randoNum3, 12, 1)
    thumby.display.drawLine(6+randoNum, 6+randoNum2+1, 18+randoNum3, 12+1, 1)
    thumby.display.drawLine(6+randoNum2, 18+randoNum, 18+randoNum3, 20, 1)
    thumby.display.drawLine(6+randoNum2, 18+randoNum+1, 18+randoNum3, 20+1, 1)
    thumby.display.drawLine(6+randoNum3, 30+randoNum2, 18+randoNum, 28, 1)
    thumby.display.drawLine(6+randoNum3, 30+randoNum2+1, 18+randoNum, 28+1, 1)
    thumby.display.drawLine(72-6-randoNum3, 6-randoNum2, 72-18-randoNum, 12, 1)
    thumby.display.drawLine(72-6-randoNum3, 6-randoNum2+1, 72-18-randoNum, 12+1, 1)
    thumby.display.drawLine(72-6-randoNum2, 18-randoNum, 72-18-randoNum3, 20, 1)
    thumby.display.drawLine(72-6-randoNum2, 18-randoNum+1, 72-18-randoNum3, 20+1, 1)
    thumby.display.drawLine(72-6-randoNum, 30-randoNum3, 72-18-randoNum2, 28, 1)
    thumby.display.drawLine(72-6-randoNum, 30-randoNum3+1, 72-18-randoNum2, 28+1, 1)


def mutateAnimation(tempBody, monsterBody):
    gc.collect()
    random.seed(time.ticks_ms())
    t0 = 0
    ct0 = time.ticks_ms()
    # BITMAP: width: 20, height: 30
    f = open('/Games/Tiny_Monster_Trainer/Curtain/Other.ujson')
    images = ujson.load(f)
    
    while(t0 - ct0 < 6000):
        t0 = time.ticks_ms()
        randoNumber = random.randint(-1,1)
        randoNumber2 = random.randint(-1,1)
        randoNumber3 = random.randint(-1,1)
    
        thumby.display.fill(0)
        printExciteLines(randoNumber, randoNumber2, randoNumber3)
        
        if t0 - ct0 > 3000:
            thumby.display.blit(bytearray(images["poppy"]), 15+randoNumber2, 1 + randoNumber3, 20, 30, 0, 0, 0)
            thumby.display.blit(bytearray(images["poppy"]), 72-37+randoNumber2, 1 + randoNumber3, 20, 30, 0, 1, 0)
        if t0 - ct0 < 3000:
            if (t0 - ct0) % 3 == 0 and t0 - ct0 > 2300:
                printMon(monsterBody, 25+randoNumber2, 8, 0)
            else:
                printMon(tempBody, 25, 8, 0)
        if t0 - ct0 > 3000:
            printMon(monsterBody, 25+randoNumber2, 8+randoNumber, 0)
        thumby.display.update()
        

def extraTrain(activeMonster, fighter):
    extraTPChance = random.randint(0,12)
    if extraTPChance < 2:
        etp = [0,1,1,1,2,2,3,5]
        extraTPChance = random.randint(0, 7)
        if etp[extraTPChance] > 0 and  fighter == 1:
            thingAquired(activeMonster, "fought", "hard & got", str(etp[extraTPChance]) + " extra TP!", 2, 0, 0)
        if etp[extraTPChance] > 0 and fighter == 0:
            thingAquired(activeMonster, "got " + str(etp[extraTPChance]) + " TP", "by watching", " & learning!", 2, 0, 0)
        return etp[extraTPChance]
    else:
        return 0

def trainAnimation(monsterBody):
    f = open('/Games/Tiny_Monster_Trainer/Curtain/Other.ujson')
    images = ujson.load(f)
    t0 = 0
    ct0 = time.ticks_ms()
    while(t0 - ct0 < 3000):
        t0 = time.ticks_ms()
        bobRate = 250
        bobRange = 5
        bobOffset = math.sin(t0 / bobRate) * bobRange
        thumby.display.fill(0)
        printMon(monsterBody, 26, 12, 0)
        thumby.display.blit(bytearray(images["barbell"]), 21, math.floor(5+bobOffset), 30, 9, 0, 0, 0)
        thumby.display.drawLine(0, 39, 72, 39, 1)
        thumby.display.update()
    f.close()
    del images

def trainJumpRope(monsterBody):
    thumby.display.setFPS(60)
    handle = bytearray([12,30,22,26,30,22,26,30,22,12])     # BITMAP: width: 10, height: 6
    tempbobOffset = 0
    bobOffset = 0
    t0 = 0
    ct0 = time.ticks_ms()
    while(t0 - ct0 < 3000):
        t0 = time.ticks_ms()
        tempbobOffset = bobOffset
        bobOffset = math.sin(t0 / 250) * 5
        bobOffset2 = math.sin(t0 / 225) * 1
        if round(bobOffset) < -3 or round(bobOffset) > 3:
            transp = 1
        elif bobOffset > tempbobOffset:
            transp = 1
        else:
            transp = 0
        thumby.display.fill(0)
        thumby.display.drawLine(15, round(22+bobOffset2), 28, round(22+(bobOffset*3)), 1)
        thumby.display.drawLine(16, round(22+bobOffset2), 29, round(22+(bobOffset*3)), 1)        
        thumby.display.drawLine(57, round(22+bobOffset2), 44, round(22+(bobOffset*3)), 1)
        thumby.display.drawLine(56, round(22+bobOffset2), 43, round(22+(bobOffset*3)), 1)
        thumby.display.drawLine(29,round(22+(bobOffset*3)), 43, round(22+(bobOffset*3)-1), transp)
        thumby.display.drawLine(29,round(22+(bobOffset*3)-1), 43, round(22+(bobOffset*3)), transp)
        thumby.display.blit(handle, 6, round(20+bobOffset2), 10, 6, 0, 0, 1)
        thumby.display.blit(handle, 57, round(20+bobOffset2), 10, 6, 0, 0, 0)
        printMon(monsterBody, 26, round(8 - bobOffset), 0)
        thumby.display.drawLine(0, 39, 72, 39, 1)
        thumby.display.update()

def trainCandles(monsterBody):
    # BITMAP: width: 7, height: 7
    flame1 = bytearray([0,56,70,84,104,48,0])
    flame2 = bytearray([0,56,69,84,106,48,0])
    flame3 = bytearray([0,48,72,68,106,48,0])
    flame4 = bytearray([0,48,72,84,104,49,0])
    flame5 = bytearray([0,48,72,84,104,48,0])
    flame6 = bytearray([0,48,72,84,106,48,0])
    flame7 = bytearray([16,40,96,81,106,20,8])
    #BITMAP: width: 9, height: 14
    wax = bytearray([0,0,254,2,3,2,254,0,0,32,48,63,48,48,48,63,48,32])
    smoke1 = bytearray([0,120,204,230,50,18,145,112,32,0,0,3,7,37,25,1,0,0])
    smoke2 = bytearray([0,120,204,196,64,66,66,64,132,0,0,1,7,37,21,21,9,0])
    smoke3 = bytearray([0,124,195,225,177,144,224,0,0,0,0,0,1,50,28,0,0,0])         
    
    flame = thumby.Sprite(7, 7, flame1+flame2+flame3+flame5+flame6, 11, 18)
    candle = thumby.Sprite(9, 14, wax, 10, 25)
    smoke = thumby.Sprite(9, 14, smoke2+smoke2+smoke2+smoke1+smoke1+smoke1+smoke3+smoke3+smoke3, 9, 3)
    flame2 = thumby.Sprite(7, 7, flame1+flame2+flame3+flame5+flame6, 72-11-8, 18)
    candle2 = thumby.Sprite(9, 14, wax, 72-20, 25)
    smoke2 = thumby.Sprite(9, 14, smoke2+smoke2+smoke2+smoke1+smoke1+smoke1+smoke3+smoke3+smoke3, 72-19, 3)
    
    # Set the FPS (without this call, the default fps is 30)
    thumby.display.setFPS(10)
    flameCtr = 0
    smokeCtr = random.randint(0, 1)
    smoke2.mirrorX = 1
    t0 = 0
    ct0 = time.ticks_ms()
    while(t0 - ct0 < 3000):
        t0 = time.ticks_ms()   # Get time (ms)
        thumby.display.fill(0) # Fill canvas to black
    
        mirrorOrNo = random.randint(0, 1)
        flameCtr = random.randint(0, 5)
        flameCtr2 = random.randint(0, 5)
        smokeCtr += 1
        if(smokeCtr >= 8): # There are 6 frames in the list, in the placement 0-5
            smokeCtr = 0
        flame.mirrorX = mirrorOrNo
        flame.setFrame(flameCtr)
        smoke.setFrame(smokeCtr)
        flame2.mirrorX = mirrorOrNo
        flame2.setFrame(flameCtr2)
        smoke2.setFrame(smokeCtr)
        thumby.display.drawSprite(flame)
        thumby.display.drawSprite(smoke)
        thumby.display.drawSprite(candle)
        thumby.display.drawSprite(flame2)
        thumby.display.drawSprite(smoke2)
        thumby.display.drawSprite(candle2)
        printMon(monsterBody, 26, 12, 0)
        thumby.display.drawLine(0, 39, 72, 39, 1)
        thumby.display.update()


def loadGame():
    gc.collect()
    tempPlayer = Player()
    f = open('/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson')
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


def makeRandomStats(monToStat, trainerLevel):
    random.seed(time.ticks_ms())
    tempMon = monToStat
    tempMon.statBlock = tempMon.statBlock.copy()
    genStat = tempMon.makeStat
    tempMon.bonusStats = {'trained' : 0}    
    tempMon.statBlock['Health'] = genStat(0) + random.randint(0, trainerLevel) 
    if tempMon.statBlock['Health'] > tempMon.statBlock['maxHealth']:
        tempMon.statBlock['Health'] = tempMon.statBlock['maxHealth']
    tempMon.statBlock['currentHealth'] = tempMon.statBlock['Health']
    for x in range (4,9):
        tempMon.statBlock[tempMon.keyList[x]] = genStat(0) + random.randint(0, trainerLevel)
        if tempMon.statBlock[tempMon.keyList[x]] > tempMon.statBlock['max' + tempMon.keyList[x]]:
            tempMon.statBlock[tempMon.keyList[x]] = tempMon.statBlock['max' + tempMon.keyList[x]]
    return tempMon

    
def makeRandomMon(roomElm):
    gc.collect()
    random.seed(time.ticks_ms())
    spawnType = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal", "asdf"]
    f = open('/Games/Tiny_Monster_Trainer/Curtain/here_be_monsters.ujson')
    monsterJson = ujson.load(f)
    tempMon = Monster()
    numberOfMons = len(monsterJson[0]['monsterInfo'][0])
    while(1):
        randomNumber = random.randint(0,numberOfMons-1)
        #micropython.mem_info()
        if (monsterJson[0]['monsterInfo'][0]['mon' + str(randomNumber) + 'stat']['Type1'] == spawnType[roomElm] 
            or monsterJson[0]['monsterInfo'][0]['mon' + str(randomNumber) + 'stat']['Type2'] == spawnType[roomElm] 
            or monsterJson[0]['monsterInfo'][0]['mon' + str(randomNumber) + 'stat']['Type3'] == spawnType[roomElm]):
            tempMon = Monster()
            tempMon.statBlock = monsterJson[0]['monsterInfo'][0]['mon' + str(randomNumber) + 'stat'].copy()
            tempMon.bodyBlock = monsterJson[0]['monsterInfo'][1]['mon' + str(randomNumber) + 'body'].copy()
            tempMon.mutateSeed = monsterJson[0]['monsterInfo'][2]['mon' + str(randomNumber) + 'mutate'].copy()
            f.close()
            del monsterJson
            tempMon = makeRandomStats(tempMon, 0)
            tempMon = makeRandomStats(tempMon, 0)
            newMonAtk = AttackMove()
            newMonAtk.getAnAttackMove(random.randint(1,3), "Default")
            tempMon.attackList.append(newMonAtk)
            newMonAtk = AttackMove()
            newMonAtk.getAnAttackMove(random.randint(1,4), tempMon.statBlock['Type1'])
            tempMon.attackList.append(newMonAtk)
            newMonAtk = AttackMove()
            if tempMon.statBlock['Type2'] != "":
                newMonAtk.getAnAttackMove(random.randint(1,4), tempMon.statBlock['Type2'])
            else:
                newMonAtk.getAnAttackMove(random.randint(1,4), tempMon.statBlock['Type1'])
            tempMon.attackList.append(newMonAtk)
            noDupAtk(tempMon.attackList)
            del newMonAtk
            return tempMon


def loss(curMon):
    curMon.statBlock['currentHealth'] = curMon.statBlock['Health']
    for attacks in range(0, len(curMon.attackList)):
        curMon.attackList[attacks-1].currentUses = curMon.attackList[attacks-1].numUses
    if curMon.statBlock['trainingPoints'] >= 0:
        curMon.statBlock['trainingPoints'] = curMon.statBlock['trainingPoints'] - 1
    thingAquired(curMon.statBlock['given_name'], "is", "Disheartened", "TP lost", 2)
    # else print that no TP left to lose


def toBtl(myGuy, nme):
    gc.collect()
    from battle import Battle 
    btl = Battle()
    battle=1
        
    btl.setBattle(myGuy, nme)
    myScroller = TextForScroller(btl.battleBlock['textScroll'])
        
    curSelect = 1
    prevSelect = 1
    while(battle == 1):
        victory = 0
        prevSelect = curSelect
        curSelect = btl.drawScreen(myScroller, myGuy, nme, curSelect, prevSelect)

        btl.battleBlock['myB4hp'] = myGuy.friends[0].statBlock['currentHealth'] - 0
        btl.battleBlock['nmeB4hp'] = nme.friends[0].statBlock['currentHealth'] - 0

        if btl.battleBlock['curAtkSlct'] != 15:
            agileTie = random.randint(-2,1)
            if (myGuy.friends[0].statBlock['Agility'] + myGuy.playerBlock['trainerLevel'] + agileTie) >= (nme.friends[0].statBlock['Agility'] + nme.playerBlock['trainerLevel']):
                btl.npcAtkSel(nme.friends[0].attackList)
                btl.battleBlock['whoFirst'] = 0
                btl.battleCrunch(myGuy.friends[0], nme.friends[0], btl.battleBlock['curAtkSlct'], btl.battleBlock['nmeAtkSlct'], btl.battleBlock['myTL'], btl.battleBlock['nmeTL']) 
            else:
                btl.npcAtkSel(nme.friends[0].attackList)
                btl.battleBlock['whoFirst'] = 1
                btl.battleCrunch(nme.friends[0], myGuy.friends[0], btl.battleBlock['nmeAtkSlct'], btl.battleBlock['curAtkSlct'], btl.battleBlock['nmeTL'], btl.battleBlock['myTL'])

            if myGuy.friends[0].statBlock['currentHealth'] == 0 and myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].currentUses == 0:
                btl.battleBlock['myText'] = "ZzZz..."
            
            btl.attackAnimation(myGuy.friends[0].bodyBlock,
                                    nme.friends[0].bodyBlock,
                                    myGuy.friends[0].statBlock['currentHealth'],
                                    nme.friends[0].statBlock['currentHealth'],
                                    myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].moveElementType,
                                    nme.friends[0].attackList[btl.battleBlock['nmeAtkSlct']].moveElementType)
            
            btl.battleBlock['whoFirst'] = 0
            btl.battleBlock['prvAtkSlct'] = btl.battleBlock['curAtkSlct']
            btl.damageTxt(myGuy, nme)
            if myScroller.scrollingText != btl.battleBlock['textScroll']:
                myScroller = TextForScroller(btl.battleBlock['textScroll'])
                myScroller.scroller = 0
        btl.battleBlock['curAtkSlct'] = 15

        autoSwitchMon(nme)
        autoSwitchMon(myGuy)
        if myGuy.friends[activeMon].statBlock['currentHealth'] == 0:
            battle = 0
            battleStartAnimation(0)
            loss(myGuy.friends[random.randint(0, len(myGuy.friends) - 1)])
        if nme.friends[activeMon].statBlock['currentHealth'] == 0:
            battle = 0
            victory = 1

        thumby.display.update() 
        if btl.battleBlock['othrOpt'] == 1:
            if len(myGuy.inventory) > 0:
                for things in range(0, len(myGuy.inventory)):
                    if myGuy.inventory[things-1].name == "Crystals":
                        if (random.randint(0,20) + myGuy.inventory[things-1].bonus + math.ceil(myGuy.playerBlock['trainerLevel']/10)) > 15: 
                            thingAquired(npcMon.statBlock['name'], "was", "Tamed!", "Yay!", 3)
                            tameMon(myGuy, npcMon)
                            myGuy.friends[-1].statBlock['currentHealth'] = myGuy.friends[-1].statBlock['Health']
                            myGuy.inventory.pop(things-1)
                            battle = 0
                            break
                        else:
                            thingAquired("Crystal", "Used,", "Not", "Tamed", 2)
                            myGuy.inventory.pop(things-1)
                            break
                    elif things == len(myGuy.inventory):
                        thingAquired("You don't", "have any", "Taming", "Crystals", 2) 
            else:
                thingAquired("You don't", "have any", "Taming", "Crystals", 2)
            btl.battleBlock['othrOpt'] = 0
        if btl.battleBlock['othrOpt'] == 2:
            battle = 0
            btl.battleBlock['othrOpt'] = 0
        if victory == 1:
            battle = 0
            
    del btl
    if victory == 1:        
        battleStartAnimation(0)
        myGuy.levelUpCheck()
        if len(myGuy.friends) > 1:
            if random.randint(0,15) < 2: 
                obsTP = random.randint(2, len(myGuy.friends)) - 1
                extraTP = extraTrain(myGuy.friends[obsTP].statBlock['given_name'], 0)
                myGuy.friends[obsTP].statBlock['trainingPoints'] = myGuy.friends[obsTP].statBlock['trainingPoints'] + extraTP
        extraTP = extraTrain(myGuy.friends[0].statBlock['given_name'], 1)
        myGuy.friends[0].statBlock['trainingPoints'] = myGuy.friends[0].statBlock['trainingPoints'] + 1 + extraTP
        if len(myGuy.inventory) < myGuy.maxHelditems:
            randoNum = random.randint(1,10)
            if randoNum > 2:
                findAnItem(myGuy.inventory, myGuy.maxHelditems)
    else:
       battleStartAnimation(0) 
    del sys.modules["battle"]


## Setting up the game ##

world=[]
myGuy = Player()
myGuy = loadGame()
world = makeWorld(myGuy.playerBlock['worldSeed'])

nmeNPC = NPC()
npcMon = Monster()
activeMon = 0
room = 13 
tempRoom = room
npcMonRoaming = RoamingMonster()
monsterMovement = 0
battle = 0
victory = 0
tempPlayerPos = myGuy.currentPos


###variables needed if save is old 11-18-22
for x in range(0, len(myGuy.friends)): 
    try:
        if myGuy.friends[x].bonusStats['item'] >= 0:
            pass
    except:
        myGuy.friends[x].bonusStats = {'item' : 0, 'trained' : 0}
    try:
        if myGuy.playerBlock['inspire'] >= 0:
            pass
    except:
        myGuy.playerBlock['inspire'] = 0


## Pretty much the game after this point :D ##

while(1):
    gc.collect()
    #micropython.mem_info()
    
    chkDone = 0
    while(battle != 1):
        allUnique = 0
        nameChanged = 1
        while(allUnique != 1 and chkDone < 6): # need to make sure that all given names are different for multiplayer battles
            for x in range(len(myGuy.friends)):
                for y in range(len(myGuy.friends)):
                    if myGuy.friends[x].statBlock['given_name'] == myGuy.friends[y].statBlock['given_name'] and x != y:
                        nameChanged = 1
                        thingAquired("Monsters", "need", "unique", "names", 2, 0, 0)
                        myGuy.friends[y].statBlock['given_name'] = giveName(myGuy.friends[y].statBlock['given_name'])
            if nameChanged == 1:
                nameChanged = 0
                allUnique = 1
            chkDone = chkDone + 1
        if len(myGuy.friends) > myGuy.playerBlock['friendMax']:
            popItOff(myGuy.friends, "monsters, please let one go!")

        thumby.display.fill(0)
        room = mapChangeCheck(myGuy, world[room], room)
        if tempRoom != room:
            npcMonRoaming.removeMonster()
            npcMonRoaming.placeMonster(world[room])
            tempRoom = room
            monsterMovement = random.randint(0,2)
        myGuy.movePlayer(world[room], npcMonRoaming, monsterMovement)
        if myGuy.currentPos != tempPlayerPos:
            npcMonRoaming.moveMonster(myGuy.currentPos, world[room], monsterMovement)
        tempPlayerPos = myGuy.currentPos
        npcMonRoaming.drawMonster()
        optionScreen(myGuy)
        thumby.display.update()
        
        if myGuy.currentPos == npcMonRoaming.currentPos:
            npcMonRoaming.removeMonster()
            battle = 1
            battleStartAnimation(1)
            
    npcMon = makeRandomMon(world[room].elementType)
    nmeNPC.playerBlock['trainerLevel'] = random.randint(myGuy.playerBlock['trainerLevel'] - 3, myGuy.playerBlock['trainerLevel'] + 3) + random.randint(-2, 2)
    if nmeNPC.playerBlock['trainerLevel'] < 0:
        nmeNPC.playerBlock['trainerLevel'] = 0
    battleMon = makeRandomStats(npcMon, random.randint(0, nmeNPC.playerBlock['trainerLevel']))
    nmeNPC.friends.append(battleMon)
    toBtl(myGuy, nmeNPC)
    nmeNPC.friends.pop(-1)
    battle = 0
