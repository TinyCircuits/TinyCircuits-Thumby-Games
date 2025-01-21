import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
import sys
sys.path.append("/Games/Tiny_Monster_Trainer/Curtain/")
from classLib import Player, Monster, Item, AttackMove
from funcLib import thingAquired, buttonInput, noDupAtk, giveName, tameMon, save, showMonInfo

    
def makeMonsterList(mSeed):
    gc.collect()
    random.seed(mSeed)
    statDict = {}
    bodyDict = {}
    mutateDict = {}
    monsterList = []
    monsterCount = 0
    for i in range (0 , 11): # number of mons = i * n  (Leave this at 11, so it can cycle through each type)
        for n in range (0,2): # numberOfMons = 22  (game will work on the emulator at 33 monsters, but it will run out of memory as a fight starts in wilderness.py on a physical thumby)
            gc.collect()
            thingAquired("", "Generating", "Monsters",str(monsterCount+1), 0)
            newMon = Monster()
            newMon.makeMonster(i)
            monsterList.append(newMon)
            monsterList[monsterCount].makeMonBody()
            statDict["mon" + str(monsterCount) + "stat"] = monsterList[monsterCount].statBlock
            bodyDict["mon" + str(monsterCount) + "body"] = monsterList[monsterCount].bodyBlock
            mutateDict["mon" + str(monsterCount) + "mutate"] = monsterList[monsterCount].mutateSeed
            monsterCount = monsterCount + 1
            #print("Mon: ", monsterCount, ", name is ", newMon.statBlock['name'], ", type1 = ", newMon.statBlock['Type1'])
    
    MonsterDict = [{"monsterInfo": [statDict, bodyDict, mutateDict], "monsterGenSeed" : [mSeed]}]
    #print("BMD = ", MonsterDict)
    with open('/Games/Tiny_Monster_Trainer/Curtain/here_be_monsters.ujson', 'w') as f:
        ujson.dump(MonsterDict, f)
        f.close()
    del MonsterDict
    gc.collect()
    try:
        p = open("/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson", "r")
        p.close()
    except OSError:
        randomNum1 = 0
        randomNum2 = 0
        randomNum3 = 0
        while (randomNum1 == randomNum2 or randomNum1 == randomNum3 or randomNum2 == randomNum3):
            randomNum1 = random.randint(0, monsterCount-1)
            randomNum2 = random.randint(0, monsterCount-1)
            randomNum3 = random.randint(0, monsterCount-1)
        myGuy = makePlayer(monsterList[randomNum1], monsterList[randomNum2], monsterList[randomNum3], theWorldSeed)    
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(1,3), "Default")
        myGuy.friends[0].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(1,3), "Default")
        myGuy.friends[0].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(1,4), myGuy.friends[0].statBlock['Type1'])
        myGuy.friends[0].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(1,4), myGuy.friends[0].statBlock['Type1'])
        myGuy.friends[0].attackList.append(newMonAtk)
        noDupAtk(myGuy.friends[0].attackList)
        noDupAtk(myGuy.friends[0].attackList)
        save(myGuy, "tmt")

def makePlayer(monster1, monster2, monster3, seed):
    gc.collect()
    currentSelect = 0
    newPlayer = Player()
    thumby.display.fill(0)
    thingAquired("Press A", "to give", "your", "name!", 0)
    while(currentSelect != 31):
        currentSelect = buttonInput(currentSelect)
    currentSelect = 0
    newPlayer.playerBlock['name'] = giveName(newPlayer.playerBlock['name'])
    thumby.display.fill(0)
    thingAquired("Press A", "to pick", "your", "Monster!", 0)
    while(currentSelect != 31):
        currentSelect = buttonInput(currentSelect)
    currentSelect = 0
    newPlayer.friends.append(monster1)
    newPlayer.friends.append(monster2)
    newPlayer.friends.append(monster3)
    showMonInfo(newPlayer, 1)
    thumby.display.update()
    newPlayer.friends.pop()
    newPlayer.friends.pop()
    tameMon(newPlayer, newPlayer.friends[0], newPlayer.friends[0].statBlock)
    newPlayer.friends.pop(0)
    newItem = Item("Crystals", 3, random.randint(0,7))
    newPlayer.inventory.append(newItem)
    newPlayer.inventory.append(newItem)
    thingAquired("", "Good", "Luck", "", 2)
    newPlayer.playerBlock['worldSeed'] = seed 
    return newPlayer 


    
try:
    p = open("/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson", "r")
    p.close()
    p = open("/Games/Tiny_Monster_Trainer/Curtain/here_be_monsters.ujson", "r")
    p.close()
except OSError:
    theWorldSeed = time.ticks_us()
    random.seed(theWorldSeed)
    #print("world seed = ", theWorldSeed)
    monsterList = makeMonsterList(theWorldSeed) 
