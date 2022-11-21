import gc
gc.enable()
import time
import thumby
import math
import random
import ujson


def thingAquired(word1, word2, itemName, word4 ="", setSleep=1, skipUpdate=0, skipFill=0):
    if skipFill == 0:
        thumby.display.fill(0)
    thumby.display.drawText(word1, math.floor(((72-(len(word1))*6))/2), 1, 1)
    thumby.display.drawText(word2, math.floor(((72-(len(word2))*6))/2), 10, 1)
    thumby.display.drawText(itemName, math.floor(((72-(len(itemName))*6))/2), 19, 1)
    thumby.display.drawText(word4, math.floor(((72-(len(word4))*6))/2), 28, 1)
    if skipUpdate == 0:
        thumby.display.update()
    time.sleep(setSleep)
    

class Player:
    def __init__(self):                                           
        self.playerBlock = {'name' : "CoolDude",
                            'trainerLevel' : 1,
                            'experience' : 0,
                            'friendMax' : 2,
                            'worldSeed' : 0}
        self.lOrR = 0    
        self.friends = []
        self.inventory = []
        self.maxHelditems = 10
        self.currentPos = math.ceil((9 * 5) / 2)
        self.position = []
        self.sprite = [0,46,251,127,123,255,46,0]
        for i in range(9 * 5):
            self.position.append(0)
        self.position[self.currentPos] = 1
 
 
    def drawPlayer(self):
        for x in range(0, 9):
            for y in range(0, 5):
                if self.position[y*9+x] == 1 :
                    thumby.display.blit(bytearray(self.sprite), x*8 , y*8, 8, 8, -1, self.lOrR, 0)


    def movePlayer(self, currentRoom, monster, monsterMovement):
        while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
            pass
        if(thumby.buttonU.pressed() == True):
            while(thumby.buttonU.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos-9].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 9
                self.position[self.currentPos] = 1
        elif(thumby.buttonD.pressed() == True):
            while(thumby.buttonD.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos+9].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 9
                self.position[self.currentPos] = 1
        elif(thumby.buttonL.pressed() == True):
            while(thumby.buttonL.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos-1].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 1
                self.position[self.currentPos] = 1
                self.lOrR = 0
        elif(thumby.buttonR.pressed() == True):
            while(thumby.buttonR.pressed() == True): 
                pass
            if currentRoom.floor[self.currentPos+1].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 1
                self.position[self.currentPos] = 1
                self.lOrR = 1
        self.drawPlayer()


    def levelUpCheck(self):
        self.playerBlock['experience'] = self.playerBlock['experience'] + 1
        if self.playerBlock['experience'] >= self.playerBlock['trainerLevel'] * 2:
            self.playerBlock['trainerLevel'] = self.playerBlock['trainerLevel'] + 1
            thingAquired(self.playerBlock['name'], "Your Trainer", "Level Is", "Now " + str(self.playerBlock['trainerLevel']), 2)
            if self.playerBlock['trainerLevel'] % 10 == 0 and self.playerBlock['friendMax'] < 5:
                self.playerBlock['friendMax'] = self.playerBlock['friendMax'] + 1
                thingAquired(self.playerBlock['name'], "can now", "have " + str(self.playerBlock['friendMax']), "monsters!", 2)

                

class RoamingMonster:
    def __init__ (self, currentPos=0, position=[]):
        self.currentPos = currentPos
        self.position = position
        for i in range(9 * 5):
            self.position.append(0)
    
    
    def drawMonster(self):
        for x in range(0, 9):
            for y in range(0, 5):
                if self.position[y*9+x] == 1 :
                    thumby.display.blit(bytearray([56,124,124,54,62,116,124,56]), x*8 ,y*8 , 8, 8, -1, 0, 0)
    
    
    def placeMonster(self, map):
        random.seed(time.ticks_ms())
        findEmptySpot = 0
        while(findEmptySpot != 1):
            findEmptySpot = random.randint(9, 34)
            if map.floor[findEmptySpot].isObjectHere == 1:
                self.currentPos = findEmptySpot
                self.position[self.currentPos] = 1
                findEmptySpot = 1
    
    
    def removeMonster(self):
        self.position[self.currentPos] = 0
        self.currentPos = 0
    
    
    def moveMonster(self, playerPos, currentRoom, monsterMovement=0):
        if monsterMovement == 0:
            if math.ceil(self.currentPos/9) > math.ceil(playerPos/9): 
                if currentRoom.floor[self.currentPos-9].isObjectHere >= 1:  # check for blocked
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos - 9
                    self.position[self.currentPos] = 1
            elif math.ceil(self.currentPos/9) < math.ceil(playerPos/9): # move monster down
                if currentRoom.floor[self.currentPos+9].isObjectHere >= 1: # check for blocked
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos + 9
                    self.position[self.currentPos] = 1
            elif self.currentPos == playerPos: # if monster is on same tile as player, don't move
                pass
            elif self.currentPos >= playerPos: # move monster left
                if currentRoom.floor[self.currentPos-1].isObjectHere >= 1: # check for blocked 
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos - 1
                    self.position[self.currentPos] = 1
            elif self.currentPos <= playerPos: # move monster right
                if currentRoom.floor[self.currentPos+1].isObjectHere >= 1: # check for blocked
                    self.position[self.currentPos] = 0
                    self.currentPos = self.currentPos + 1
                    self.position[self.currentPos] = 1
        else:
            randomDirList = [-9, -1, 0, 1, 9]
            x = random.randint(0,4)
            if currentRoom.floor[self.currentPos + randomDirList[x]].isObjectHere == 1: # check for blocked
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + randomDirList[x]
                self.position[self.currentPos] = 1


class Monster:
    def __init__(self):
        self.statBlock = {'name' : "", 
                        'given_name' : "",
                        'trainingPoints' : 7,
                        'Type1' : "",
                        'Type2' : "",
                        'Type3' : "",
                        'Health' : 1,
                        'currentHealth' : 1,
                        'maxHealth' : 1,
                        'Strength' : 1,
                        'maxStrength' : 1,
                        'Agility' : 1,
                        'maxAgility' : 1,
                        'Endurance' : 1,
                        'maxEndurance' : 1,
                        'Mysticism' : 1,
                        'maxMysticism' : 1,
                        'Tinfoil' : 1,
                        'maxTinfoil' : 1}

        self.keyList = ['Health',       # 0  
                        'Type1',        # 1 
                        'Type2',        # 2
                        'Type3',        # 3
                        'Agility',      # 4
                        'Strength',     # 5
                        'Endurance',    # 6
                        'Mysticism',    # 7
                        'Tinfoil']      # 8
                        
        self.bodyBlock = {'head' : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            'body' : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            'legs' : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]}
        
        self.attackList = []
        self.mutateSeed = []
                

    @staticmethod
    def makeName():
        gc.collect()
        name = ""
        prevLetter1 = 0
        prevLetter2 = 0
        name_length = random.randrange(3, 8)
        firstLetter = 1
        capAlphabet = [' ', 'A', 'E', 'I', 'O','U','Y','B','C','D','F','G','H',
                        'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 
                        'W', 'X', 'Z']
        alphabet = [' ', 'a', 'e', 'i', 'o', 'u', 'y', 'b', 'c', 'd', 'f', 'g',
                    'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q','r', 's', 't', 'v',
                    'w', 'x', 'z']
        for i in range(1, name_length): 
            if firstLetter < 1: 
                if prevLetter1 >= 6 and prevLetter2 >= 6: 
                    getLetter = random.randint(1, 5)
                    if getLetter == prevLetter1 and getLetter == prevLetter2:
                        getLetter = random.randint(1, 26) 
                        if getLetter == prevLetter1:
                            while getLetter != prevLetter1:
                                getLetter = random.randint(1, 26)
                    prevLetter2 = prevLetter1
                    prevLetter1 = getLetter
                    letter = alphabet[getLetter]
                else: 
                    getLetter = random.randint(1, 26)
                    prevLetter2 = prevLetter1
                    prevLetter1 = getLetter
                    letter = alphabet[getLetter]
            else: 
                getLetter = random.randint(1, 26)
                prevLetter2 = prevLetter1
                prevLetter1 = getLetter
                letter = capAlphabet[getLetter]
                firstLetter = 0
            name = name + letter
            if letter == "q" or letter == "Q":
                name = name + "u"
        shortNameCheck = len(name)
        if shortNameCheck == 2:
            if prevLetter1 >= 6 and prevLetter2 >=6:
                getLetter = random.randint(1, 5)
                name = capAlphabet[prevLetter2] + alphabet[getLetter] + alphabet[prevLetter1]
        return name

    
    @staticmethod
    def makeStat(baseStat, maxStat=0):
        if baseStat < 3:  
            baseStat = random.randint(3, 10)
            return baseStat
        elif maxStat == 1:
            maxStat = random.randint(7, 21)
            if maxStat < baseStat:
                maxStat = baseStat
            return maxStat
        return baseStat
    
    
    def makeMonBody(self):
        gc.collect()
        f = open('/Games/Tiny_Monster_Trainer/Curtain/MonsterParts.ujson')
        monsterParts = ujson.load(f)

        if random.randint(0,120) != 1:
            randoNum = random.randint(0,17)
            self.bodyBlock['head'] = monsterParts["heads"][str(randoNum)]
            randoNum = random.randint(1,17)
            self.bodyBlock['body'] = monsterParts["bodies"][str(randoNum)]
            randoNum = random.randint(1,17)
            self.bodyBlock['legs'] = monsterParts["legs"][str(randoNum)]
        else:
            self.bodyBlock['head'] = monsterParts["special"]["birbHead"]
            self.bodyBlock['body'] = monsterParts["special"]["birbBody"]
            self.bodyBlock['legs'] = monsterParts["special"]["birbLegs"]
        f.close()
        del monsterParts

    
    
    def makeType(self, type1=0):
        monsterTypes = ["Wind", "Earth", "Water", "Fire", "Mind", "Darkness", 
                        "Cute", "Light", "Physical", "Mystical", "Ethereal"]
        if self.statBlock['Type1'] == "":
            monType = monsterTypes[type1]
            return monType
        elif self.statBlock['Type2'] == "":
            monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
            while monType == self.statBlock['Type1']:
                monType = monsterTypes[random.randint(1, len(monsterTypes)-1)]
            return monType
        elif self.statBlock['Type3'] == "":
            monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
            while monType == self.statBlock['Type1'] or monType == self.statBlock['Type2']:
                monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
            return monType
        return monType


    def makeMonster(self, type1=0):
        gc.collect()
        genStat = self.makeStat
        self.statBlock['name'] = self.makeName()
        self.statBlock['given_name'] = self.statBlock['name']
        self.statBlock['trainingPoints'] = 7
        self.statBlock['Type1'] = self.makeType(type1)
        randoNum = random.randint(1,3)
        if randoNum == 1:
            self.statBlock['Type2'] = self.makeType()
            randoNum = random.randint(1,100)
            if randoNum == 1:
                self.statBlock['Type3'] = self.makeType()
        self.statBlock['Health'] = genStat(0)
        self.statBlock['currentHealth'] = self.statBlock['Health']
        self.statBlock['maxHealth'] = genStat(self.statBlock['Health'], 1)
        for x in range (4,9):
            self.statBlock[self.keyList[x]] = genStat(0)
            self.statBlock['max' + self.keyList[x]] = genStat(self.statBlock[self.keyList[x]], 1)
        self.mutateSeed.append(random.randint(0,255))
        self.mutateSeed.append(0)
 

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
                        randoNum = random.randint(0,3)
                        myAttack.getAnAttackMove(randoNum, self.statBlock['Type2'])
                        self.attackList.append(myAttack)
                        noDupAtk(self.attackList)
                    elif self.statBlock['Type3'] == "":
                        self.statBlock['Type3'] = self.makeType()
                        myAttack = AttackMove()
                        randoNum = random.randint(0,3)
                        myAttack.getAnAttackMove(randoNum, self.statBlock['Type3'])
                        noDupAtk(self.attackList)
                    self.statBlock['maxHealth'] = self.statBlock['maxHealth'] + 20
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


class AttackMove():
    def __init__(self, name="", numUses=0, baseDamage=0, magic=0, moveElementType=""):
        self.name = name 
        self.numUses = numUses 
        self.currentUses = numUses 
        self.baseDamage = baseDamage  
        self.magic = magic 
        self.moveElementType = moveElementType


    def getAnAttackMove(self, selectionNum, elmType=""):
        f = open('/Games/Tiny_Monster_Trainer/Curtain/Attacks.ujson')
        attackJson = ujson.load(f)

        self.name = attackJson[elmType][str(selectionNum)]["name"]
        self.numUses = attackJson[elmType][str(selectionNum)]["Sta"]
        self.currentUses = attackJson[elmType][str(selectionNum)]["Sta"]
        self.baseDamage = attackJson[elmType][str(selectionNum)]["bnsDmg"]
        self.magic = attackJson[elmType][str(selectionNum)]["pOrM"]
        self.moveElementType = attackJson[elmType][str(selectionNum)]["Type"]
        f.close() 
 
    
class Item():
    def __init__(self, name, key, bonus=0):
        self.name = name
        self.key = key
        self.bonus = bonus
        
        
    def doAction(self, monsterInfo):
        if self.key == 1 or self.key == 2:
            monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['currentHealth'] + 10 + self.bonus
            if monsterInfo.statBlock['currentHealth'] > monsterInfo.statBlock['Health']:
               monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['Health']            
        if self.key == 2:
            if monsterInfo.bonusStats['item'] <= 30:
                keyList=['maxHealth', 'maxStrength', 'maxAgility', 'maxEndurance', 'maxMysticism', 'maxTinfoil']
                monsterInfo.bonusStats['item'] = monsterInfo.bonusStats['item'] + 1
                monsterInfo.statBlock[keyList[abs(self.bonus)]] = monsterInfo.statBlock[keyList[abs(self.bonus)]] + 1
        elif self.key == 3:
            for moves in range(0, len(monsterInfo.attackList)):
                monsterInfo.attackList[moves].currentUses = monsterInfo.attackList[moves].numUses
        else:
            pass


    def getItem(self):
        randoNum = random.randint(0,11)
        self.key = 2
        
        if randoNum == 0:
            self.name = "Stickers"
            self.bonus = randoNum
        elif randoNum == 1:
            self.name = "Vitamins"
            self.bonus = -abs(randoNum)
        elif randoNum == 2:
            self.name = "Helium"
            self.bonus = -abs(randoNum)
        elif randoNum == 3:
            self.name = "Pillows"
            self.bonus = -abs(randoNum)
        elif randoNum == 4:
            self.name = "Stardust"
            self.bonus = -abs(randoNum)
        elif randoNum == 5:
            self.name = "Tinfoil"
            self.bonus = -abs(randoNum)
        elif randoNum < 9:
            self.name = "Bandaids"
            self.key = 1
            self.bonus = 2
        elif randoNum < 8:
            self.name = "PushPops"
            self.key = 1
            self.bonus = 12
        else: 
            self.name = "Crystals"
            self.key = 3
            self.bonus = random.randint(0,7)        

class TextForScroller():
    def __init__(self, scrollingText):
        self.scrollingText = scrollingText
        self.scrollerLength = len(self.scrollingText) * 6 + 82
        self.scroller = 0

    
    def moveScroll(self):
        if self.scroller >= self.scrollerLength:
                self.scroller = 0
        else:
            self.scroller = self.scroller + 1
        return self.scroller

 
class Tile:
    def __init__(self):
        self.tileType = 0
        self.isObjectHere = 0

           
    def generateTile(self, preTileType):
        if preTileType == 1: # wall
            self.isObjectHere = 0
        elif preTileType == 2: # floor
            self.tileType = 2 
            self.isObjectHere = 1
        elif preTileType == 3: # door
            self.tileType = 3 
            self.isObjectHere = 2
        elif preTileType == 8: # crack
            self.tileType = 8 
            self.isObjectHere = 1
        else:
            self.tileType = 1 # wall
            self.isObjectHere = 0
            
            
class Map:
    def __init__(self):
        self.elementType = 0
        self.floor = []
        for i in range(9 * 5):
            floorTile = Tile()
            self.floor.append(floorTile)
            self.floor[i].tileType = 2
            self.floor[i].isObjectHere = 1 
        for x in range(0, 9): 
            self.floor[x].tileType = 1 
            self.floor[x].isObjectHere = 0
            self.floor[4*9+x].tileType = 1
            self.floor[4*9+x].isObjectHere = 0
        for y in range(0, 5):
            self.floor[y*9].tileType = 1 
            self.floor[y*9].isObjectHere = 0
            self.floor[y*9+8].tileType = 1
            self.floor[y*9+8].isObjectHere = 0
        for x in range(0, 9):
            if x == math.floor(9 / 2):
                self.floor[x].tileType = 3 
                self.floor[x].isObjectHere = 2
                self.floor[4*9+x].tileType = 3
                self.floor[4*9+x].isObjectHere = 2
        for y in range(0, 5):
            if y == math.floor(5 / 2):
                self.floor[y*9].tileType = 3
                self.floor[y*9].isObjectHere = 2
                self.floor[y*9+8].tileType = 3
                self.floor[y*9+8].isObjectHere = 2

 
    def procGenMap(self):
        self.elementType = random.randint(0,10)
        for x in range (0,9):
            for y in range(0,5):
                floor = self.floor[y*9+x]
                if floor.tileType == 1:
                    pass
                if floor.tileType == 2:
                    somethingHere = random.randint(0,20) # chance for random thing on map
                    if somethingHere == 1:
                        terrainTile = random.randrange(7,9)
                        self.floor[y*9+x].generateTile(terrainTile)

 
    def displayMap(self):
        wall_sprite = [24,126,255,102,102,255,126,24]
        floor_sprite = [0,0,0,0,0,0,0,0]
        floor_crack = [0,0,0,0,40,20,0,0]
        door_sprite = [255,255,3,1,17,19,255,255]
        tree2_sprite = [0,14,95,119,127,91,14,0]
        mountain1_sprite = [192,120,12,30,63,14,60,224]
        tablet_sprite = [128,248,132,146,146,132,248,128]
        fireOrGrass_sprite = [152,112,230,60,240,30,251,128]
        for x in range(0, 9):
            for y in range(0, 5):
                floor = self.floor[y*9+x]
                if(floor.tileType == 1 and self.elementType < 2):
                    thumby.display.blit(bytearray(mountain1_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 1 and self.elementType < 4):
                    thumby.display.blit(bytearray(fireOrGrass_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 1 and self.elementType < 6):
                    thumby.display.blit(bytearray(wall_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 1 and self.elementType < 9):
                    thumby.display.blit(bytearray(tree2_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 1):
                    thumby.display.blit(bytearray(tablet_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)   
                elif(floor.tileType == 2):
                    thumby.display.blit(bytearray(floor_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 3):
                    thumby.display.blit(bytearray(door_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
                elif(floor.tileType == 8):
                    thumby.display.blit(bytearray(floor_crack), x*8 ,y*8 , 8, 8, 0, 0, 0)
                else:
                    thumby.display.blit(bytearray(tree2_sprite), x*8 ,y*8 , 8, 8, 0, 0, 0)
