import gc
gc.enable()
from time import sleep as sleepy
import thumby
import math
import sys
import ujson
import micropython
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Monster, TextForScroller


def makeTheList(theObj):
    gc.collect()
    makingAList = []
    if hasattr(theObj[0],  'statBlock') == True:
        for names in range(0, len(theObj)):
            makingAList.append(theObj[names].statBlock['given_name'])
    else:
        for names in range(0, len(theObj)):
            makingAList.append(theObj[names].name)
    return makingAList


def thingAquired(word1, word2, itemName, word4 ="", setSleep=1, skipUpdate=0, skipFill=0):
    if skipFill == 0:
        thumby.display.fill(0)
    thumby.display.drawText(word1, math.floor(((72-(len(word1))*6))/2), 1, 1)
    thumby.display.drawText(word2, math.floor(((72-(len(word2))*6))/2), 10, 1)
    thumby.display.drawText(itemName, math.floor(((72-(len(itemName))*6))/2), 19, 1)
    thumby.display.drawText(word4, math.floor(((72-(len(word4))*6))/2), 28, 1)
    if skipUpdate == 0:
        thumby.display.update()
    sleepy(setSleep)

    
def battleStartAnimation(color):
    thumby.display.setFPS(0)
    for x in range(0,72):
        for y in range (0, 40):
            thumby.display.drawLine(x, 0, 0, y, color)
            thumby.display.drawLine(72, 40-y, 72-x, 40, color)
        thumby.display.update()
    thumby.display.fill(color)
    thumby.display.update()
    thumby.display.setFPS(40)
    
    
def currentSelectCheckRange(optionAmount, currentSelect):
    if optionAmount > 1 and optionAmount !=2:
        if currentSelect > optionAmount - 2 :
            currentSelect = currentSelect - optionAmount
        if currentSelect < -abs(optionAmount) + 2:
            currentSelect = currentSelect + optionAmount
    else:
        if currentSelect > optionAmount - 1 :
            currentSelect = currentSelect - optionAmount
        if currentSelect < -abs(optionAmount) + 1:
            currentSelect = currentSelect + optionAmount
    return currentSelect 
    

def popItOff(theListofObjs, word):
    thumby.display.fill(0)
    #gc.collect()
    myScroller = TextForScroller("Too many " + word)
    currentSelect = 0
    tempSelect = currentSelect
    origListLen = len(theListofObjs)
    listOfNames = makeTheList(theListofObjs)
    while(origListLen == len(theListofObjs)):
        tempSelect = currentSelect
        currentSelect = showOptions(listOfNames, currentSelect, "", 0)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 30, 1)
        if currentSelect == 31:
            theListofObjs.pop(tempSelect)
        if currentSelect > 10:
            currentSelect = tempSelect
        thumby.display.update()


def showOptions(options, currentSelect, bottomText, x=0):
    optionAmount = len(options)
    currentSelect = currentSelectCheckRange(optionAmount, currentSelect)
    thumby.display.fill(0)
    thumby.display.drawFilledRectangle(0+x, 10, 72, 9, 1)
    if optionAmount > 1: 
        thumby.display.drawText(options[currentSelect - 1], 1+x, 2, 1) # prints top opt
        if optionAmount > 2:
            thumby.display.drawText(options[currentSelect+1], 1+x, 20, 1) #prints bottom opt
    thumby.display.drawText(options[currentSelect], 1+x, 11, 0) # prints center opt
    thumby.display.drawLine(0, 29, 72, 29, 1)
    if bottomText != "":
        thumby.display.drawText(bottomText, 1, 31, 1) # prints other info on bottom of screen
    currentSelect = buttonInput(currentSelect)
    if optionAmount <= 1:
        if currentSelect == 31:
            return currentSelect
        elif currentSelect == 30:
            return currentSelect
        elif currentSelect > 0 or currentSelect < 0:
            return 0
    return currentSelect


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

    
def buttonInput(selectPos):                
    selectionBoxPos = selectPos
    while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
        pass
    if(thumby.buttonU.pressed() == True):
        while(thumby.buttonU.pressed() == True): 
            pass
        selectionBoxPos = selectionBoxPos - 1
    elif(thumby.buttonD.pressed() == True):
        while(thumby.buttonD.pressed() == True): 
            pass
        if (selectionBoxPos <= 26):
            selectionBoxPos = selectionBoxPos + 1
    elif(thumby.buttonL.pressed() == True):
        while(thumby.buttonL.pressed() == True): 
            pass
        selectionBoxPos = 29
    elif(thumby.buttonR.pressed() == True):
        while(thumby.buttonR.pressed() == True): 
            pass
        selectionBoxPos = 28
    elif(thumby.buttonA.pressed() == True):
        while(thumby.buttonA.pressed() == True):
            pass
        selectionBoxPos = 31
    elif(thumby.buttonB.pressed() == True):
        while(thumby.buttonB.pressed() == True):
            pass
        selectionBoxPos = 30
    return selectionBoxPos
    
    
def giveName(beingNamed):
    capAlphabet = [' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    character_list = [' ','a','b','c','d','e','f','g', 'h', 'i', 'j','k','l',
                        'm','n', 'o', 'p','q','r','s','t','u','v','w','x','y','z'] 
    selected_chars = beingNamed
    c = 1
    tempC = c
    goBack = 0
    addDelLtr2 = [0,124,18,18,124,0,0,40,40,40,40,0,124,84,84,0,120,16,8,120,0,124,68,68,56,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           8,28,42,8,8,8,0,20,20,20,20,0,62,34,34,28,0,62,42,42,0,62,32,32,0,62,42,42,0,2,62,2,0,62,42,42,0,0,0,0,
           4,4,4,21,14,4,0,10,10,10,10,0,31,5,5,31,0,31,17,17,14,0,31,17,17,14,0,0,31,16,16,1,31,1,0,31,9,9,22,0]
    while(goBack != 1):
        tempC = c
        c = showOptions(character_list, c, selected_chars, 0)
        thumby.display.drawFilledRectangle(8, 10, 72, 9, 0)
        thumby.display.blit(bytearray(addDelLtr2), 25, 3, 40, 21, -1, 0, 0)
        thumby.display.update()
        if c == 28:
            if len(selected_chars) == 0 or selected_chars[-1] == ' ':
                selected_chars = selected_chars + capAlphabet[tempC]
            else:
                selected_chars = selected_chars + character_list[tempC]
        elif c == 29:
            if len(selected_chars) > 0:
                selected_chars = selected_chars.rstrip(selected_chars[-1])
        elif c == 31:
            if len(selected_chars) > 0 :
                beingNamed = selected_chars
                goBack = 1
        if c >= 28:
            c = tempC
    return beingNamed
    

def tameMon(playerInfo, npcMon):
    gc.collect()
    newMon = Monster()
    newMon.statBlock = npcMon.statBlock.copy()
    newMon.bodyBlock = npcMon.bodyBlock.copy()
    newMon.attackList = npcMon.attackList.copy()
    newMon.mutateSeed = npcMon.mutateSeed.copy()
    playerInfo.friends.append(newMon)
    if len(playerInfo.friends) > playerInfo.playerBlock['friendMax']:
            popItOff(playerInfo.friends, "monsters, please let one go!")


def switchActiveMon(playerInfo, oldActiveMon, newActiveMon, newActiveMonOldPos):
    gc.collect()
    tempMon = oldActiveMon
    tempMon.statBlock = oldActiveMon.statBlock.copy()
    tempMon.bodyBlock = oldActiveMon.bodyBlock.copy() 
    tempMon.attackList = oldActiveMon.attackList.copy()
    tempMon.mutateSeed = oldActiveMon.mutateSeed.copy() 
    playerInfo.friends[0] = newActiveMon
    playerInfo.friends[0].statBlock = newActiveMon.statBlock.copy()
    playerInfo.friends[0].bodyBlock = newActiveMon.bodyBlock.copy()
    playerInfo.friends[0].attackList = newActiveMon.attackList.copy()
    playerInfo.friends[0].mutateSeed = newActiveMon.mutateSeed.copy() 
    playerInfo.friends[newActiveMonOldPos] = tempMon
    playerInfo.friends[newActiveMonOldPos].statBlock = tempMon.statBlock.copy()
    playerInfo.friends[newActiveMonOldPos].bodyBlock = tempMon.bodyBlock.copy()
    playerInfo.friends[newActiveMonOldPos].attackList = tempMon.attackList.copy() 
    playerInfo.friends[newActiveMonOldPos].mutateSeed = tempMon.mutateSeed.copy()
    

def printMon(monsterBody, x, y, playerOrNPC):
    thumby.display.blit(bytearray(monsterBody['head']), x, y, 20, 9, 0, playerOrNPC, 0)
    thumby.display.blit(bytearray(monsterBody['body']), x, y+9, 20, 9, 0, playerOrNPC, 0)
    thumby.display.blit(bytearray(monsterBody['legs']), x, y+18, 20, 9, 0, playerOrNPC, 0)


def drawArrows(l, r, d, u=1): # x, y):
    arrowLR = [4,4,4,31,14,4] # 6 x 5
    arrowUD = [8,24,63,24,8] # 5 x 6    # last three are: key, mirrorX, mirrorY
    thumby.display.blit(bytearray(arrowLR), 1, 17, 6, 5, l, abs(l), 0)
    thumby.display.blit(bytearray(arrowLR), 65, 17, 6, 5, r, 0, 0)
    thumby.display.blit(bytearray(arrowUD), 66, 30, 5, 6, d, 0, 0)
    thumby.display.blit(bytearray(arrowUD), 66, 4, 5, 6, u, 0, abs(u))


def showMonInfo(playerInfo, startOfgameCheck=0, combatCheck=0):
    left = 1
    right = -1
    down = -1
    up = -1
    x = 0
    xMonRange = len(playerInfo.friends)
    currentSelect = -2
    tempSelect = currentSelect
    tempSelect2 = tempSelect
    goBack = 0
    monsterListInfo = playerInfo.friends
    while(goBack != 1): 
        if currentSelect == 9:
            currentSelect = -2
        if currentSelect == -3:
            currentSelect = 8
        currentSelect = currentSelectCheckRange(10, currentSelect)
        tempSelect2 = tempSelect
        tempSelect = currentSelect
        thumby.display.fill(0)
        if currentSelect == -2: 
            printMon(monsterListInfo[x].bodyBlock, 25 ,0, 0)
            drawArrows(left, right, down, up)
            thumby.display.drawText(monsterListInfo[x].statBlock['given_name'], math.floor(((72-(len(monsterListInfo[x].statBlock['given_name']))*6))/2), 28, 1)
        elif currentSelect == -1:
            thingAquired(monsterListInfo[x].statBlock['given_name'], "is a", monsterListInfo[x].statBlock['name'], "", 0, 1)
            drawArrows(left, right, down, up)
        elif currentSelect <= 8:
            while(monsterListInfo[x].statBlock[monsterListInfo[x].keyList[currentSelect]] == ""):
                if tempSelect2 < currentSelect:
                    currentSelect = currentSelect + 1
                elif tempSelect2 > currentSelect:
                    currentSelect = currentSelect - 1
                else:
                    currentSelect = currentSelect - 1
            thingAquired(monsterListInfo[x].statBlock['given_name'] + "'s",
                        monsterListInfo[x].keyList[currentSelect], 
                        "is",str(monsterListInfo[x].statBlock[monsterListInfo[x].keyList[currentSelect]]), 0, 1)
            drawArrows(left, right, down, up)
        thumby.display.update()
        currentSelect = buttonInput(currentSelect)
        if currentSelect == 31 and combatCheck != 1:
            if playerInfo.friends[0] != playerInfo.friends[x] or startOfgameCheck == 1:
                if playerInfo.friends[x].statBlock['currentHealth'] == 0:
                    thingAquired(monsterListInfo[x].statBlock['given_name'], "does not", "have enough", "HP to fight!", 2)
                switchActiveMon(playerInfo, monsterListInfo[0], monsterListInfo[x], x)
                goBack = 1
                if combatCheck != 2: #need to while switching in battle if selected mon has HPs
                    thingAquired(monsterListInfo[0].statBlock['given_name'], "is now", "your active", "monster!", 2)
                x = 0
                currentSelect = -2
                if startOfgameCheck == 1:
                    goBack = 1
            else:
                currentSelect = tempSelect
        elif currentSelect == 30 and startOfgameCheck == 0:
            goBack = 1
        elif currentSelect == 28:
            x = x + 1
            currentSelect = tempSelect
            if x >= xMonRange:
                x = x - 1
        elif currentSelect == 29:
            x = x - 1
            currentSelect = tempSelect
            if x < 0:
                x = x + 1
        elif currentSelect >= 30:
            currentSelect = -2
        else:
            pass
        if x > 0 and x < (xMonRange-1):
            left = -1
            right = -1
        elif xMonRange == 1:
            left = 1
            right = 1
        elif x == (xMonRange - 1):
            left = -1
            right = 1
        elif x == 0:
            left = 1
            right = -1

    
def obj_to_dict(obj):
    return obj.__dict__


def save(playerInfo):
    gc.collect()
    statDict = {}
    bodyDict = {}
    attackDict = {}
    mutateDict = {}
    itemDict = {}
    for x in range(0, len(playerInfo.friends)):
        tempAttackDict = {}
        for y in range (0, len(playerInfo.friends[x].attackList)):
            tempAttackDict["attack" + str(y)] = obj_to_dict(playerInfo.friends[x].attackList[y])
            attackDict["mon" + str(x) + "atk"] = tempAttackDict
        statDict["mon" + str(x) + "stat"] = playerInfo.friends[x].statBlock
        bodyDict["mon" + str(x) + "body"] = playerInfo.friends[x].bodyBlock
        mutateDict["mon" + str(x) + "mutate"] = playerInfo.friends[x].mutateSeed
    for x in range(0, len(playerInfo.inventory)):
        itemDict["item" + str(x)] = obj_to_dict(playerInfo.inventory[x])
    playerDict = [{"player" : playerInfo.playerBlock, "items" : [itemDict], "monsterInfo": [statDict, bodyDict, attackDict, mutateDict]}]
    #print(playerDict)
    with open('/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson', 'w') as f:
        ujson.dump(playerDict, f)
        f.close()
    del playerDict
    gc.collect()    
