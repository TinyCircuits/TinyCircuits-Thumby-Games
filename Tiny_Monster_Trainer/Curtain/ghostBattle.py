import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys 
import machine
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Map, Monster, Tile, RoamingMonster, TextForScroller, Item, AttackMove
from funcLib import thingAquired, battleStartAnimation, printMon, drawArrows, showOptions, popItOff, buttonInput, noDupAtk, giveName, tameMon, switchActiveMon, save, showMonInfo
#from wilderness import loadGame

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


def loadGhost(ghostFile):
    gc.collect()
    tempPlayer = Player()
    f = open('/Games/Tiny_Monster_Trainer/Ghosts/'+ghostFile+'.ujson')
    bigGhostJson = ujson.load(f)
    tempPlayer.playerBlock = bigGhostJson[0]['player'].copy()
    for x in range(0, len(bigGhostJson[0]['monsterInfo'][0])):
        tempMon = Monster()
        tempMon.statBlock = bigGhostJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat'].copy()
        tempMon.bodyBlock = bigGhostJson[0]['monsterInfo'][1]['mon' + str(x) + 'body'].copy()
        for y in range(0, len(bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])): 
            tempAttackMove = AttackMove(bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['name'], 
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['numUses'],
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['baseDamage'],
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['magic'],
                                        bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['moveElementType'])
            tempAttackMove.currentUses = bigGhostJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['currentUses']
            tempMon.attackList.append(tempAttackMove) 
        tempMon.attackList = tempMon.attackList.copy()
        tempPlayer.friends.append(tempMon)
        tempPlayer.friends = tempPlayer.friends.copy()
    tempPlayer.lOrR = 0
    f.close()
    del bigGhostJson
    return tempPlayer


def autoSwitchMon(playerInfo):
    if playerInfo.friends[0].statBlock['currentHealth'] < 1:
        x = 0
        for monsters in playerInfo.friends:
            if playerInfo.friends[x].statBlock['currentHealth'] > 0:
                switchActiveMon(playerInfo, playerInfo.friends[0], playerInfo.friends[x], x)
            x = x + 1
        if playerInfo.friends[0].statBlock['currentHealth'] > 0:
            thingAquired(playerInfo.playerBlock['name']+"'s", playerInfo.friends[0].statBlock['given_name'], "is now",  "Acvtive!", 2)


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


def typeAsNum(moveType):
    typeList = ["", "Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    typeNumber = 0
    for i in range(0,12):
        if moveType == typeList[i]:
            typeNumber = i
    return typeNumber
    

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
        if ((math.ceil(attackAmnt/2) + attackMon.statBlock['Agility']) + glanceCheck) >= dodge+defTrainLevel: # check for glance
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
    random.seed(time.ticks_ms())
    myScroller = TextForScroller(playerMon.statBlock['given_name'] + " has entered into battle with " + nmeMon.statBlock['name'] + "! Their trainer's level is " + str(npcTrainLevel) +"!" )
    currentSelect = 1
    tempSelect = currentSelect
    options = ["Info", "Atk", "Swap"] 
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
                        if nmeMon.statBlock['currentHealth'] <= 0:
                            playerMon.attackList[selectCheck].currentUses = playerMon.attackList[selectCheck].currentUses -1
                            if playerMon.attackList[selectCheck].currentUses < 0:
                                playerMon.attackList[selectCheck].currentUses = 0
                            return 
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
                    if nmeMon.statBlock['currentHealth'] <= 0:
                        return  
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
    
'''
def refresh(curMon):
    curMon.statBlock['currentHealth'] = curMon.statBlock['Health']
    for attacks in range(0, len(curMon.attackList)):
        curMon.attackList[attacks-1].currentUses = curMon.attackList[attacks-1].numUses
        print(str(curMon['currentHealth']))'''


def drawArrowsGhost(d, u): # x, y):
    #arrowLR = [4,4,4,31,14,4] # 6 x 5
    arrowUD = [8,24,63,24,8] # 5 x 6    # last three are: key, mirrorX, mirrorY

    thumby.display.blit(bytearray(arrowUD), 66, 20, 5, 6, d, 0, 0)
    thumby.display.blit(bytearray(arrowUD), 66, 3, 5, 6, u, 0, 1)


def pickGhost():
    import os
    curSelect = 0
    cancelCheck = 0
    tempSelect = curSelect
    bottomText = "Pick a Ghost"
    files = os.listdir("/Games/Tiny_Monster_Trainer/Ghosts/")
    for x in range(len(files)):
        files[x] = files[x].replace('.ujson', '')
    while cancelCheck != 1:
        curSelect = showOptions(files, curSelect, bottomText)
        drawArrowsGhost(0, 0)
        if curSelect == 28 or curSelect == 29:
            curSelect = tempSelect
        if curSelect == 31:
            curSelect = tempSelect
            return files[curSelect] 
        if curSelect == 30:
            cancelCheck = 1
            thumby.display.fill(0)
            return ""
        tempSelect = curSelect
        thumby.display.update()


def drawIntro(player, ghost):
    
    ghostTitle = getTitle(ghost.playerBlock['worldSeed'])
    #thingAquired(player.playerBlock['name'], "Vs.", ghostTitle, ghost.playerBlock['name'],0,1,1)
    
    t0 = 0
    ct0 = time.ticks_ms()
    x = 10 
    y = 11
    animateCount = 0
    thumby.display.fill(0)
    thumby.display.update()
    time.sleep(1)
    while(t0 - ct0 < 5000):
        t0 = time.ticks_ms()
        randoNumber = random.randint(-1,1)
        randoNumber2 = random.randint(-1,1)
        randoNumber3 = random.randint(-1,1)
        thumby.display.fill(0)
        if(t0 - ct0 > 2800):
            thingAquired(player.playerBlock['name'], "Vs", ghostTitle, ghost.playerBlock['name'],0,1,1)
            thumby.display.blit(bytearray(player.sprite), x+randoNumber-8 , y+randoNumber2, 8, 8, -1, 1, 0)
            thumby.display.blit(bytearray(ghost.sprite), 72-(x+randoNumber2) , y+randoNumber3, 8, 8, -1, ghost.lOrR, 0)
        animateCount = animateCount + 1 
        thumby.display.drawFilledRectangle(-36+animateCount, 0, 36, 40, 1)
        thumby.display.drawFilledRectangle(72-animateCount, 0, 36, 40, 1)
        thumby.display.update()


def getTitle(rSeed):
    random.seed(rSeed)
    titleList=["Eldritch", "Murky", "The Lich", "Elder",
                "Ye Old", "Undead", "Spooky", "Spooky",
                "Spooky", "Gastly", "Haunting", "Just"]
    title = random.randint(0,11)
    return titleList[title]
    
    
def wantToPlayAgain():
    battleStartAnimation(0)
    waiting = True
    currentSelect = 0
    t0 = 0
    ct0 = time.ticks_ms()
    while(waiting):
        thingAquired("", "Play", " Again?", "A:Y B:N", 0, 0, 0)
        t0 = time.ticks_ms()
        if(t0 - ct0 >= 10000):
            waiting = False
        if currentSelect == 0:
            currentSelect = buttonInput(currentSelect)
            if currentSelect == 31:
                waiting = False
            elif currentSelect == 30:
                machine.reset()
            else:
                currentSelect = 0


while(1):
    ghostFile = pickGhost()
    thumby.display.fill(0)
    thumby.display.update()

    
    if ghostFile != "":
        myGuy = Player()
        myGuy = loadGame()
        ghost = Player()
        ghost = loadGhost(ghostFile)
        
        drawIntro(myGuy, ghost)
        
        victory=0
        activeMon=0
        battle=1
        
        for x in range(0,len(myGuy.friends)):
            myGuy.friends[x].statBlock['currentHealth'] = myGuy.friends[x].statBlock['Health']
            for attacks in range(0, len(myGuy.friends[x].attackList)):
                myGuy.friends[x].attackList[attacks-1].currentUses = myGuy.friends[x].attackList[attacks-1].numUses
        for x in range(0,len(ghost.friends)):
            ghost.friends[x].statBlock['currentHealth'] = ghost.friends[x].statBlock['Health']
            for attacks in range(0, len(ghost.friends[x].attackList)):
                ghost.friends[x].attackList[attacks-1].currentUses = ghost.friends[x].attackList[attacks-1].numUses
        
        while(battle == 1):
            victory = 0
            thumby.display.fill(0)
            victory = battleScreen(myGuy.friends[activeMon], ghost.friends[activeMon], myGuy.playerBlock['trainerLevel'], ghost.playerBlock['trainerLevel'])
            autoSwitchMon(ghost)
            autoSwitchMon(myGuy)
    
            if myGuy.friends[activeMon].statBlock['currentHealth'] == 0:
                battle = 0
            if ghost.friends[activeMon].statBlock['currentHealth'] == 0:
                battle = 0
                victory = 1
            if victory == 4:
                showMonInfo(myGuy, 0, 2)
                victory = 0
            thumby.display.update()
            #battleStartAnimation(0) 
            if victory == 1:
                battle = 0
                
        if victory == 1:        
            battleStartAnimation(0)
            thingAquired("","You Win!","","",4,0,0)
        else:
            battleStartAnimation(0)
            thingAquired("","You Lost!","","",4,0,0)
    
    wantToPlayAgain()
