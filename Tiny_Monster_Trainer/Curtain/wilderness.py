import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys 
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Map, Monster, Tile, RoamingMonster, TextForScroller, Item, AttackMove
from funcLib import thingAquired, battleStartAnimation, printMon, drawArrows, showOptions, popItOff, buttonInput, noDupAtk, giveName, tameMon, switchActiveMon, save, showMonInfo
#import micropython


#player3_sprite = [0,46,251,127,123,255,46,0]
#blob_sprite = [56,124,124,54,62,116,124,56]
#head0_sprite = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
#           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

 
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


def typeAsNum(moveType):
    typeList = ["", "Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    typeNumber = 0
    for i in range(0,12):
        if moveType == typeList[i]:
            typeNumber = i
    return typeNumber
        

def attackAnimation(playerBod, nmeBod, attackIsPlayer, missFlag, amountOfDmg, playerHP, nmeHP, atkTxt, attackType = ""):
    # BITMAP: width: 8, height: 8
    sidewaySkull = bytearray([0,42,62,119,127,107,107,62]) # ethereal
    darkness = bytearray([0,36,66,8,16,66,36,0]) # darkness
    maybeFireball = bytearray([20,42,62,99,69,89,99,62]) # fire
    maybeWaterball = bytearray([16,68,16,40,68,76,56,0]) # water
    windBlow = bytearray([68,85,85,34,8,138,170,68]) # wind
    rock = bytearray([20,65,28,42,66,86,36,56]) # earth
    punch =  bytearray([189,165,36,116,148,180,132,120])  # physical
    spiral = bytearray([124,130,57,69,149,153,66,60]) # mind
    fourFlowers = bytearray([32,82,37,2,64,164,74,4]) # light
    heart = bytearray([28,62,126,252,252,126,62,28]) # cute
    arrow = bytearray([4,60,39,114,90,78,120,0]) # mystic
    basic = bytearray([56,108,130,162,138,154,130,124]) #basic
    
    BoltArray = [basic, rock, windBlow, maybeWaterball, maybeFireball, fourFlowers, darkness, heart, spiral, punch, arrow, sidewaySkull]
    attackTypeNum = typeAsNum(attackType)
    
    nmeAfterDmg = nmeHP - amountOfDmg
    playerAfterDmg = playerHP - amountOfDmg
    combatText = ""
    
    t0 = 0
    ct0 = time.ticks_ms()
    bobRate = 250
    bobRange = 5
    animateX = 0
    
    thumby.display.setFPS(40)
    while(t0 - ct0 < 4000):
        t0 = time.ticks_ms()
        bobOffset = math.sin(t0 / bobRate) * bobRange
        if(t0 - ct0 >= 4000):
            combatText = ""
        playerX = 8
        nmeX = 42
        y = 0
        nmeY = 0
        if (t0 - ct0 >= 2000) and (t0 - ct0 <= 3000) and attackIsPlayer == 1:
            y = 5
        elif (t0 - ct0 >= 2000) and (t0 - ct0 <= 3000) and attackIsPlayer == 0:
            nmeY = 5
        thumby.display.fill(0) 
        printMon(playerBod, playerX + y, 1, 0)
        printMon(nmeBod, nmeX - nmeY, 1, 1)
        thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
        thumby.display.drawText(str(playerHP), 2, 30, 0)
        thumby.display.drawText(str(nmeHP), 72 - len(str(nmeHP) * 7), 30, 0)
        thumby.display.drawText(combatText, math.ceil(((72-(len(combatText))*6))/2)+1, 30, 0)
        if missFlag == 1 and (t0 - ct0) > 2000 and (t0 - ct0 <= 3500) and attackIsPlayer == 1: # player misses
            combatText = atkTxt
        if missFlag == 0 and (t0 - ct0) > 2000 and (t0 - ct0 <= 4000) and attackIsPlayer == 1: # player hits
            thumby.display.blit(BoltArray[attackTypeNum], (30 + animateX), math.floor(10+bobOffset), 8, 8, 0, 0, 0) #, flippy, 0)
            nmeHP = nmeAfterDmg
            combatText = atkTxt
        if missFlag == 1 and (t0 - ct0) > 2000 and (t0 - ct0 <= 3500) and attackIsPlayer == 0: # nme misses
            thumby.display.drawText("Miss", 25, 30, 0)
            combatText = "Miss"
        if missFlag == 0 and (t0 - ct0) > 2000 and (t0 - ct0 <= 4000) and attackIsPlayer == 0: # nme hits
            thumby.display.blit(BoltArray[attackTypeNum], (36 - animateX), math.floor(10+bobOffset), 8, 8, 0, 1, 0) #, flippy, 0)
            combatText = atkTxt
            playerHP = playerAfterDmg
        thumby.display.update()
        y = 0
        nmeY = 0
        if (t0 - ct0) % 2 == 0 and (t0 - ct0) > 2000:
            animateX = animateX + 1


def isTypeWeak(mon1Type, mon2Type): 
    typeList = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    offsetList = ["Fire", "Earth", "Wind", "Water", "Mind", "Light", "Darkness",
                "Cute", "Ethereal", "Physical", "Mystical"]
    x = 0
    bonus = 0
    if mon1Type != "":
        while mon1Type != offsetList[x]:
            x = x + 1
        if mon2Type == typeList[x]:
            bonus = 1
    return bonus
    

def isTypeStrong(mon1Type, mon2Type): 
    typeList = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    offsetList = ["Wind", "Water", "Fire", "Earth", "Darkness", "Cute", "Mind",
                "Light", "Mystical", "Ethereal", "Physical"]
    x = 0
    bonus = 0
    if mon1Type != "":
        while mon1Type != typeList[x]:
            x = x + 1
        if mon2Type == offsetList[x]:
            bonus = 1
    return bonus


def attack(attackMon, defenceMon, activeAttack, attackTrainLevel=0, defTrainLevel=0): 
    
    if activeAttack.magic == 1:
        dodgeBonus = defenceMon.statBlock['Tinfoil'] + random.randint(-1, 5)
        attackAmnt = attackMon.statBlock['Mysticism'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2) 
        defence =  defTrainLevel + dodgeBonus
    else:
        dodgeBonus = defenceMon.statBlock['Endurance'] + random.randint(-1, 5)
        attackAmnt = attackMon.statBlock['Strength'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2)
        defence = defTrainLevel + dodgeBonus
    hp2 = defenceMon.statBlock['currentHealth']
    dodge = defenceMon.statBlock['Agility'] + dodgeBonus 
    damage = 0
    hit = 1
    atkTypeBonus = 1
    defTypeBonus = 1
    if (dodge + random.randint(-abs(attackTrainLevel),(100 - defTrainLevel)))+200 > (90 - defTrainLevel)+200: # check for dodge
        glanceCheck = random.randint(-20, 20)
        if ((math.ceil(attackAmnt/2) + attackMon.statBlock['Agility']) + glanceCheck + attackMon.bonusStats['trained']) >= dodge+defTrainLevel: # check for glance
            hit = 2
        else:
            hit = 0
    if hit > 0:
        for x in range(1,3):
            atkTypeBonus = isTypeStrong(activeAttack.moveElementType, defenceMon.statBlock[defenceMon.keyList[x]]) + atkTypeBonus
        for x in range(1,3):
            defTypeBonus = isTypeWeak(defenceMon.statBlock[defenceMon.keyList[x]], activeAttack.moveElementType) + defTypeBonus
        damage = math.ceil((attackAmnt * atkTypeBonus)/3) - math.ceil((defence * defTypeBonus)/3)
        if damage <= 0:
            damage = 1
        else:
            damage = math.ceil(damage/hit)
    if hit == 1:
        piz = [0,0,0,0,1,1,1,2,3]
        paz = random.randint(0,8)
        damage = damage + piz[paz]
    hp2 = hp2 - damage
    if hp2 < 0:
        hp2 = 0
    defenceMon.statBlock['currentHealth'] = hp2
    if hit == 1:
        return "Hit!"
    elif hit == 2:
        return "Glance"
    else: # hit == 0:
        return "Miss"  
        

def afterAttackSelect(attackingMon, atkChoice, defMon, playerTrainLevel, npcTrainLevel, attackIsPlayer):
    scrollText = ""
    hpBeforeDmg = defMon.statBlock['currentHealth']
    attackText = attack(attackingMon, defMon, attackingMon.attackList[atkChoice], playerTrainLevel, npcTrainLevel)
    amntOfDmg = hpBeforeDmg - defMon.statBlock['currentHealth'] 
    if amntOfDmg >= 1:
        if attackIsPlayer == 1:
            attackAnimation(attackingMon.bodyBlock, defMon.bodyBlock, attackIsPlayer, 0, amntOfDmg, attackingMon.statBlock['currentHealth'], hpBeforeDmg, attackText, attackingMon.attackList[atkChoice].moveElementType)
            scrollText = (attackingMon.statBlock['given_name'] + " did " + str(amntOfDmg) + " points of damage!")
        else:
            attackAnimation(defMon.bodyBlock, attackingMon.bodyBlock, attackIsPlayer, 0, amntOfDmg, hpBeforeDmg, attackingMon.statBlock['currentHealth'], attackText, attackingMon.attackList[atkChoice].moveElementType)
    else:
        if attackIsPlayer == 1:
            attackAnimation(attackingMon.bodyBlock, defMon.bodyBlock, attackIsPlayer, 1, amntOfDmg, attackingMon.statBlock['currentHealth'], hpBeforeDmg, attackText)
            scrollText = (attackingMon.statBlock['given_name'] + "'s " + attackingMon.attackList[atkChoice].name + " attack missed!" )
        else: 
            attackAnimation(defMon.bodyBlock, attackingMon.bodyBlock, attackIsPlayer, 1, amntOfDmg, hpBeforeDmg, attackingMon.statBlock['currentHealth'], attackText)
    return scrollText


def attackOptionMenu(monInfo):  
    currentSelect = 1
    tempSelect = currentSelect
    playerOptionList = []
    
    for attacksKnown in range(0, len(monInfo)):
        playerOptionList.append(monInfo[attacksKnown].name)
        
    while(currentSelect < 29):
        thumby.display.fill(0)
        tempSelect = currentSelect
        if currentSelect == len(monInfo):
            currentSelect = currentSelect - 1
        if currentSelect == -abs(len(monInfo)):
            currentSelect = currentSelect + 1
        currentSelect = showOptions(playerOptionList, currentSelect, "Stamina: " + str(monInfo[currentSelect].currentUses))
        thumby.display.update()
        if currentSelect == 31:
            return tempSelect 
        elif currentSelect == 30:
            return 30 
        elif currentSelect == 28 or currentSelect == 29:
            currentSelect = tempSelect
    
    
def battleScreen(playerMon, nmeMon, playerTrainLevel, npcTrainLevel):
    #print("Hi, you are in a fight!")
    myScroller = TextForScroller(playerMon.statBlock['given_name'] + " has entered into battle with a roaming " + nmeMon.statBlock['name'] + "!")
    currentSelect = 1
    tempSelect = currentSelect
    options = ["Info", "Atk", "Run", "Tame", "Swap"] 
    while((playerMon.statBlock['currentHealth'] >= 1) and (nmeMon.statBlock['currentHealth'] >= 1)):
        thumby.display.fill(0)
        tempSelect = currentSelect
        currentSelect = showOptions(options, currentSelect, "", 47)
        thumby.display.drawFilledRectangle(0, 31, 72, 10, 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 31, 1)
        if currentSelect == 31: 
            currentSelect = tempSelect
            if options[currentSelect] == "Atk": 
                selectCheck = attackOptionMenu(playerMon.attackList)
                if selectCheck < 30:
                    if playerMon.attackList[selectCheck].currentUses <= 0:
                        playerMon.statBlock['currentHealth'] = math.floor(playerMon.statBlock['currentHealth'] * 0.7)
                        thingAquired(playerMon.statBlock['given_name'], "is out of", "stamina", "HP lost", 2)
                        if playerMon.statBlock['currentHealth'] <= 0:
                            return 
                    agileTie = 0
                    if (playerMon.statBlock['Agility'] + playerTrainLevel) == (nmeMon.statBlock['Agility'] + npcTrainLevel):
                        agileTie = random.randint(-2,1)
                    if (playerMon.statBlock['Agility'] + playerTrainLevel + agileTie) >= (nmeMon.statBlock['Agility'] + npcTrainLevel):
                        myScroller = TextForScroller(afterAttackSelect(playerMon, selectCheck, nmeMon, playerTrainLevel, npcTrainLevel, 1))
                        if npcMon.statBlock['currentHealth'] <= 0:
                            playerMon.attackList[selectCheck].currentUses = playerMon.attackList[selectCheck].currentUses -1
                            if playerMon.attackList[selectCheck].currentUses < 0:
                                playerMon.attackList[selectCheck].currentUses = 0
                            return 1 
                        junk = afterAttackSelect(nmeMon, (len(nmeMon.attackList) -1), playerMon, npcTrainLevel, playerTrainLevel, 0) 
                        del junk
                    else:
                        junk = afterAttackSelect(nmeMon, (len(nmeMon.attackList) -1), playerMon, npcTrainLevel, playerTrainLevel, 0)
                        del junk
                        if playerMon.statBlock['currentHealth'] <= 0:
                            return 0 
                        myScroller = TextForScroller(afterAttackSelect(playerMon, selectCheck, nmeMon, playerTrainLevel, npcTrainLevel, 1))
                    playerMon.attackList[selectCheck].currentUses = playerMon.attackList[selectCheck].currentUses -1
                    if playerMon.attackList[selectCheck].currentUses < 0:
                        playerMon.attackList[selectCheck].currentUses = 0
                    if npcMon.statBlock['currentHealth'] <= 0:
                        return 1 
            elif options[currentSelect] == "Run": 
                nmeMon.statBlock['currentHealth'] = 0
            elif options[currentSelect] == "Tame": 
                return 2 
            elif options[currentSelect] == "Info": 
                tempPlayer = Player()
                tempPlayer.friends.append(nmeMon)
                tempPlayer.friends.append(playerMon)
                showMonInfo(tempPlayer, 0 , 1)
                del tempPlayer
            elif options[currentSelect] == "Swap":
                return 4 
            else: 
                pass
        if currentSelect == 30 or currentSelect == 28 or currentSelect == 29 :
            currentSelect = tempSelect    
        printMon(playerMon.bodyBlock, 0, 1, 0)
        printMon(nmeMon.bodyBlock, 25, 1, 1)
        thumby.display.update()
    return 0  

    
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
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "trained", "their", "health!", 2) 
                elif statNameList[currentSelect] == "Agility" and myMonStats['Agility'] < myMonStats['maxAgility']: 
                    myMonStats['Agility'] = myMonStats['Agility'] + 1
                    trainAnimation(monsterBody)
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
                    trainAnimation(monsterBody)
                    thingAquired(myMonStats['given_name'], "practiced", "their", "mysticism", 2)
                elif statNameList[currentSelect] == "Tinfoil" and myMonStats['Tinfoil'] < myMonStats['maxTinfoil']: 
                    myMonStats['Tinfoil'] = myMonStats['Tinfoil'] + 1
                    trainAnimation(monsterBody)
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
                    if playerInfo.friends[0].bonusStats['trained'] < 40:
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
    #micropython.mem_info()
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
            #micropython.mem_info()
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
        thumby.display.update()
    f.close()
    del images


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
    #micropython.mem_info()
    spawnType = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    f = open('/Games/Tiny_Monster_Trainer/Curtain/here_be_monsters.ujson')
    monsterJson = ujson.load(f)
    #micropython.mem_info()
    print("aft ld json")
    tempMon = Monster()
    #gc.collect()
    numberOfMons = len(monsterJson[0]['monsterInfo'][0])
    print("Length numberOfMons = ", numberOfMons)
    for x in range(0,5):
        print("in mk rdm mon lp")
        #micropython.mem_info()
        randomNumber = random.randint(0,numberOfMons-1)
        tempMon = Monster()
        tempMon.statBlock = monsterJson[0]['monsterInfo'][0]['mon' + str(randomNumber) + 'stat'].copy()
        tempMon.bodyBlock = monsterJson[0]['monsterInfo'][1]['mon' + str(randomNumber) + 'body'].copy()
        tempMon.mutateSeed = monsterJson[0]['monsterInfo'][2]['mon' + str(randomNumber) + 'mutate'].copy()
        if (tempMon.statBlock['Type1'] == spawnType[roomElm] or tempMon.statBlock['Type2'] == spawnType[roomElm] or tempMon.statBlock['Type3'] == spawnType[roomElm]):
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
            f.close()
            del monsterJson
            return tempMon
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
    return tempMon
    

def loss(curMon):
    curMon.statBlock['currentHealth'] = curMon.statBlock['Health']
    for attacks in range(0, len(curMon.attackList)):
        curMon.attackList[attacks-1].currentUses = curMon.attackList[attacks-1].numUses
    if curMon.statBlock['trainingPoints'] >= 0:
        curMon.statBlock['trainingPoints'] = curMon.statBlock['trainingPoints'] - 1
    thingAquired(curMon.statBlock['given_name'], "is", "Disheartened", "TP lost", 2)
    # else print that no TP left to lose


## Setting up the game ##

world=[]
myGuy = Player()
myGuy = loadGame()
world = makeWorld(myGuy.playerBlock['worldSeed'])


npcMon = Monster()
activeMon = 0
room = 13 
tempRoom = room
npcMonRoaming = RoamingMonster()
monsterMovement = 0
battle = 0
victory = 0
tempPlayerPos = myGuy.currentPos

### start of patching in variables 11-18-22
for x in range(0, len(myGuy.friends)): 
    print(str(x))
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
    print("main")
    #micropython.mem_info()
    while(battle != 1):
        allUnique = 0
        nameChanged = 1
        while(allUnique != 1): # need to make sure that all given names are different for multiplayer battles
            for x in range(len(myGuy.friends)):
                for y in range(len(myGuy.friends)):
                    if myGuy.friends[x].statBlock['given_name'] == myGuy.friends[y].statBlock['given_name'] and x != y:
                        nameChanged = 1
                        thingAquired("Monsters", "need", "unique", "names", 2, 0, 0)
                        myGuy.friends[y].statBlock['given_name'] = giveName(myGuy.friends[y].statBlock['given_name'])
            if nameChanged == 1:
                nameChanged = 0
                allUnique = 1   
        if len(myGuy.friends) > myGuy.playerBlock['friendMax']:
            popItOff(myGuy.friends, "monsters, please let one go!")

        thumby.display.fill(0)
        room = mapChangeCheck(myGuy, world[room], room) # draw world map
        if tempRoom != room:
            npcMonRoaming.removeMonster()
            npcMonRoaming.placeMonster(world[room])
            tempRoom = room
            monsterMovement = random.randint(0,2)
        myGuy.movePlayer(world[room], npcMonRoaming, monsterMovement) # draws roaming monster & player (maybe not anymore, 4/16/22)
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
    npcTL = random.randint(myGuy.playerBlock['trainerLevel'] - 3, myGuy.playerBlock['trainerLevel'] + 3) + random.randint(-2, 2)
    if npcTL < 0:
        npcTL = 0

    battleMon = makeRandomStats(npcMon, random.randint(0, npcTL))
    while(battle == 1):
        victory = 0
        thumby.display.fill(0)
        victory = battleScreen(myGuy.friends[activeMon], battleMon, myGuy.playerBlock['trainerLevel'], npcTL)
        autoSwitchMon(myGuy)
        if myGuy.friends[activeMon].statBlock['currentHealth'] == 0:
            battle = 0
            loss(myGuy.friends[random.randint(0, len(myGuy.friends) - 1)])
        if npcMon.statBlock['currentHealth'] == 0:
            battle = 0
        if victory == 2:
            if len(myGuy.inventory) > 0:
                for things in range(0, len(myGuy.inventory)):
                    if myGuy.inventory[things-1].name == "Crystals":
                        if (random.randint(0,20) + myGuy.inventory[things-1].bonus + random.randint(1, myGuy.playerBlock['trainerLevel'])) > 15: 
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
        if victory == 4:
            showMonInfo(myGuy, 0, 2)
            victory = 0
        thumby.display.update()
    battleStartAnimation(0) 
    if victory == 1:
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
