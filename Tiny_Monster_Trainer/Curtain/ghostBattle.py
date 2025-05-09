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
from classLib import Player, Monster, TextForScroller, Item, AttackMove
from funcLib import thingAquired, battleStartAnimation, drawArrows, showOptions, buttonInput, switchActiveMon
from battle import Battle

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
        btl = Battle()
        
        battle=1
        
        for x in range(0,len(myGuy.friends)):
            myGuy.friends[x].statBlock['currentHealth'] = myGuy.friends[x].statBlock['Health']
            for attacks in range(0, len(myGuy.friends[x].attackList)):
                myGuy.friends[x].attackList[attacks-1].currentUses = myGuy.friends[x].attackList[attacks-1].numUses
        for x in range(0,len(ghost.friends)):
            ghost.friends[x].statBlock['currentHealth'] = ghost.friends[x].statBlock['Health']
            for attacks in range(0, len(ghost.friends[x].attackList)):
                ghost.friends[x].attackList[attacks-1].currentUses = ghost.friends[x].attackList[attacks-1].numUses

        btl.setBattle(myGuy, ghost, 1)
        myScroller = TextForScroller(btl.battleBlock['textScroll'])
        
        curSelect = 1
        prevSelect = 1
        while(battle == 1):
            victory = 0

            prevSelect = curSelect
            curSelect = btl.drawScreen(myScroller, myGuy, ghost, curSelect, prevSelect)


            btl.battleBlock['myB4hp'] = myGuy.friends[0].statBlock['currentHealth'] - 0
            btl.battleBlock['nmeB4hp'] = ghost.friends[0].statBlock['currentHealth'] - 0


            if btl.battleBlock['curAtkSlct'] != 15:
                agileTie = random.randint(-2,1)
                if (myGuy.friends[0].statBlock['Agility'] + myGuy.playerBlock['trainerLevel'] + agileTie) >= (ghost.friends[0].statBlock['Agility'] + ghost.playerBlock['trainerLevel']):
                    btl.npcAtkSel(ghost.friends[0].attackList)
                    btl.battleBlock['whoFirst'] = 0
                    btl.battleCrunch(myGuy.friends[0],
                                    ghost.friends[0],
                                    btl.battleBlock['curAtkSlct'],
                                    btl.battleBlock['nmeAtkSlct'],
                                    btl.battleBlock['myTL'],
                                    btl.battleBlock['nmeTL']) 
                else:
                    btl.npcAtkSel(ghost.friends[0].attackList)
                    btl.battleBlock['whoFirst'] = 1
                    btl.battleCrunch(ghost.friends[0],
                                    myGuy.friends[0],
                                    btl.battleBlock['nmeAtkSlct'],
                                    btl.battleBlock['curAtkSlct'],
                                    btl.battleBlock['nmeTL'],
                                    btl.battleBlock['myTL'])

                if myGuy.friends[0].statBlock['currentHealth'] == 0 and myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].currentUses == 0:
                    btl.battleBlock['myText'] = "ZzZz..."
                
                btl.attackAnimation(myGuy.friends[0].bodyBlock,
                                        ghost.friends[0].bodyBlock,
                                        myGuy.friends[0].statBlock['currentHealth'],
                                        ghost.friends[0].statBlock['currentHealth'],
                                        myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].moveElementType,
                                        ghost.friends[0].attackList[btl.battleBlock['nmeAtkSlct']].moveElementType)
                
                btl.battleBlock['whoFirst'] = 0
                btl.battleBlock['prvAtkSlct'] = btl.battleBlock['curAtkSlct']
                btl.damageTxt(myGuy, ghost)
                if myScroller.scrollingText != btl.battleBlock['textScroll']:
                    myScroller = TextForScroller(btl.battleBlock['textScroll'])
                    myScroller.scroller = 0
            btl.battleBlock['curAtkSlct'] = 15

            autoSwitchMon(ghost)
            autoSwitchMon(myGuy)
            if myGuy.friends[activeMon].statBlock['currentHealth'] == 0:
                battle = 0
            if ghost.friends[activeMon].statBlock['currentHealth'] == 0:
                battle = 0
                victory = 1

            thumby.display.update()

            if victory == 1:
                battle = 0

        if victory == 1:        
            battleStartAnimation(0)
            thingAquired("","You Win!","","",4,0,0)
        else:
            battleStartAnimation(0)
            thingAquired("","You Lost!","","",4,0,0)
    
    wantToPlayAgain()
