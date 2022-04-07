import gc
gc.enable()
import time
import thumby
import math
import random
import ujson
#import micropython


player3_sprite = [0,46,251,127,123,255,46,0]
blob_sprite = [56,124,124,54,62,116,124,56]
head0_sprite = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


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


class AttackMove():
    def __init__(self, name="", numUses=0, baseDamage=0, magic=0, moveElementType=""):
        self.name = name 
        self.numUses = numUses 
        self.currentUses = numUses 
        self.baseDamage = baseDamage  
        self.magic = magic 
        self.moveElementType = moveElementType


    def getAnAttackMove(self, selectionNum, elmType=""):
        f = open('/Games/Tiny_Monster_Trainer/Curtian/Attacks.ujson')
        attackJson = ujson.load(f)

        self.name = attackJson[elmType][str(selectionNum)]["name"]
        self.numUses = attackJson[elmType][str(selectionNum)]["Sta"]
        self.currentUses = attackJson[elmType][str(selectionNum)]["Sta"]
        self.baseDamage = attackJson[elmType][str(selectionNum)]["bnsDmg"]
        self.magic = attackJson[elmType][str(selectionNum)]["pOrM"]
        self.moveElementType = attackJson[elmType][str(selectionNum)]["Type"]
        f.close()


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
 

class Item():
    def __init__(self, name, key, bonus=0):
        self.name = name
        self.key = key
        self.bonus = bonus

        
    def doAction(self, monsterInfo):
        if self.key == 1:
            monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['currentHealth'] + 10 + self.bonus
            if monsterInfo.statBlock['currentHealth'] > monsterInfo.statBlock['Health']:
               monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['Health']            
        elif self.key == 2:
            monsterInfo.statBlock['maxHealth'] = monsterInfo.statBlock['maxHealth'] + 1 + self.bonus
            if  monsterInfo.statBlock['currentHealth'] < monsterInfo.statBlock['Health']:
                monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['currentHealth'] + 1 + self.bonus
                if monsterInfo.statBlock['currentHealth'] > monsterInfo.statBlock['Health']:
                     monsterInfo.statBlock['currentHealth'] = monsterInfo.statBlock['Health']
        elif self.key == 3:
            for moves in range(0, len(monsterInfo.attackList)):
                monsterInfo.attackList[moves].currentUses = monsterInfo.attackList[moves].numUses
        else:
            pass


    def getItem(self):
        randoNum = random.randint(1,5)
        if randoNum == 1:
            self.name = "Bandaids"
            self.key = 1
            self.bonus = -2
        elif randoNum == 2:
            self.name = "PushPops"
            self.key = 1
            self.bonus = 10
        elif randoNum == 3:
            self.name = "Stickers"
            self.key = 2
        elif randoNum == 4:
            self.name = "Ribbons"
            self.key = 2
            self.bonus = 1
        elif randoNum == 5:
            self.name = "Crystals"
            self.key = 3
            self.bonus = random.randint(0,7)


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
        for i in range(9 * 5):
            self.position.append(0)
        self.position[self.currentPos] = 1
 
 
    def drawPlayer(self):
        for x in range(0, 9):
            for y in range(0, 5):
                if self.position[y*9+x] == 1 :
                    thumby.display.blit(bytearray(player3_sprite), x*8 , y*8, 8, 8, -1, self.lOrR, 0)
 
 
    def movePlayer(self, currentRoom, monster, monsterMovement):
        moved = 0
        while(thumby.dpadJustPressed() == False and thumby.actionPressed == False):
            pass
        if(thumby.buttonU.pressed() == True):
            while(thumby.buttonU.pressed() == True): 
                pass
            moved = 1
            if currentRoom.floor[self.currentPos-9].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 9
                self.position[self.currentPos] = 1
        elif(thumby.buttonD.pressed() == True):
            while(thumby.buttonD.pressed() == True): 
                pass
            moved = 1
            if currentRoom.floor[self.currentPos+9].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 9
                self.position[self.currentPos] = 1
        elif(thumby.buttonL.pressed() == True):
            while(thumby.buttonL.pressed() == True): 
                pass
            moved = 1
            if currentRoom.floor[self.currentPos-1].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos - 1
                self.position[self.currentPos] = 1
                self.lOrR = 0
        elif(thumby.buttonR.pressed() == True):
            while(thumby.buttonR.pressed() == True): 
                pass
            moved = 1
            if currentRoom.floor[self.currentPos+1].isObjectHere >= 1:
                self.position[self.currentPos] = 0
                self.currentPos = self.currentPos + 1
                self.position[self.currentPos] = 1
                self.lOrR = 1
        if moved == 1:
            monster.moveMonster(self.currentPos, world[room], monsterMovement)
        monster.drawMonster()
        self.drawPlayer()


    def levelUpCheck(self):
        self.playerBlock['experience'] = self.playerBlock['experience'] + 1
        if self.playerBlock['experience'] == self.playerBlock['trainerLevel'] * 2:
            self.playerBlock['trainerLevel'] = self.playerBlock['trainerLevel'] + 1
            thingAquired("Your", "Trainer", "Level is", "Now " + str(self.playerBlock['trainerLevel']), 2)
            if self.playerBlock['trainerLevel'] % 10 == 0 & self.playerBlock['friendMax'] < 4:
                self.playerBlock['friendMax'] = self.playerBlock['friendMax'] + 1

        
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
                        'Type1',        # 1     Move types to end of keyList so that showMonInfo can be more intuitive
                        'Type2',        # 2
                        'Type3',        # 3
                        'Agility',      # 4
                        'Strength',     # 5
                        'Endurance',    # 6
                        'Mysticism',    # 7
                        'Tinfoil']      # 8
                        
        self.bodyBlock = {'head' : head0_sprite,
                            'body' : head0_sprite,
                            'legs' : head0_sprite}
                            
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
        f = open('/Games/Tiny_Monster_Trainer/Curtian/MonsterParts.ujson')
        monsterParts = ujson.load(f)

        if random.randint(0,60) != 1:
            randoNum = random.randint(0,13)
            self.bodyBlock['head'] = monsterParts["heads"][str(randoNum)]
            randoNum = random.randint(1,13)
            self.bodyBlock['body'] = monsterParts["bodies"][str(randoNum)]
            randoNum = random.randint(1,13)
            self.bodyBlock['legs'] = monsterParts["legs"][str(randoNum)]
        else:
            self.bodyBlock['head'] = monsterParts["special"]["birbHead"]
            self.bodyBlock['body'] = monsterParts["special"]["birbBody"]
            self.bodyBlock['legs'] = monsterParts["special"]["birbLegs"]
        f.close()
        del monsterParts

    
    
    def makeType(self):
        monsterTypes = ["Wind", "Earth", "Water", "Fire", "Mind", "Darkness", 
                        "Cute", "Light", "Physical", "Mystical", "Ethereal"]
        if self.statBlock['Type1'] == "":
            monType = monsterTypes[random.randint(0, len(monsterTypes)-1)]
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


    def mutateMon(self):
        if self.statBlock['trainingPoints'] > 4:
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
                thingAquired(self.statBlock['given_name'], "has", "mutated!", "", 2)
            else:
                thingAquired(self.statBlock['given_name'], "is unable to", "mutate", "again", 2)
        else:
            howManyPoints = self.statBlock['trainingPoints']
            thingAquired(self.statBlock['given_name'], ("needs " + str(5 - howManyPoints) + " more"), "Training", "Points", 2)


    def makeMonster(self):
        gc.collect()
        genStat = self.makeStat
        self.statBlock['name'] = self.makeName()
        self.statBlock['given_name'] = self.statBlock['name']
        self.statBlock['trainingPoints'] = 7
        self.statBlock['Type1'] = self.makeType()
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
        self.mutateSeed.append(random.randint(0,99))
        self.mutateSeed.append(0)

    
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
                    thumby.display.blit(bytearray(blob_sprite), x*8 ,y*8 , 8, 8, -1, 0, 0)
    
    
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


def battleStartAnimation(color):
    thumby.display.setFPS(0)
    for x in range(0,72):
        for y in range (0, 40):
            thumby.display.drawLine(x, 0, 0, y, color)
            thumby.display.drawLine(72, 40-y, 72-x, 40, color)
        thumby.display.update()
    thumby.display.fill(0)
    thumby.display.update()
    thumby.display.setFPS(30)


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


def attackAnimation(playerBod, nmeBod, attackIsPlayer, missFlag, amountOfDmg, playerHP, nmeHP, atkTxt):
    for x in range(0, 4):
        playerX = 8
        nmeX = 42
        y = 0
        nmeY = 0
        if x == 2 and attackIsPlayer == 1:
            y = 10
        elif x == 2 and attackIsPlayer == 0:
            nmeY = 10
        thumby.display.fill(0)
        printMon(playerBod, playerX + y, 1, 0)
        printMon(nmeBod, nmeX - nmeY, 1, 1)
        thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
        thumby.display.drawText(str(playerHP), 2, 30, 0)
        thumby.display.drawText(str(nmeHP), 72 - len(str(nmeHP) * 7), 30, 0)
        thumby.display.update()
        if missFlag == 1 and x > 1 and attackIsPlayer == 1: # player misses
            thumby.display.drawText(atkTxt, math.ceil(((72-(len(atkTxt))*6))/2)+1, 30, 0)
        if missFlag == 0 and x > 1 and attackIsPlayer == 1: # player hits
            thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
            thumby.display.drawText(atkTxt, math.ceil(((72-(len(atkTxt))*6))/2)+1, 30, 0)
            thumby.display.drawText(str(playerHP), 2, 30, 0)
            thumby.display.drawText(str(nmeHP - amountOfDmg), 72 - len(str(nmeHP - amountOfDmg) * 7), 30, 0)
        if missFlag == 1 and x > 1 and attackIsPlayer == 0: # nme misses
            thumby.display.drawText("Miss", 25, 30, 0)
        if missFlag == 0 and x > 1 and attackIsPlayer == 0: # nme hits
            thumby.display.drawFilledRectangle(0, 29, 72, 9, 1)
            thumby.display.drawText(atkTxt, math.ceil(((72-(len(atkTxt))*6))/2)+1, 30, 0)
            thumby.display.drawText(str(nmeHP), 72 - len(str(nmeHP) * 7), 30, 0)
            thumby.display.drawText(str(playerHP - amountOfDmg), 2, 30, 0)
        thumby.display.update()
        time.sleep(1)
        y = 0
        nmeY = 0


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
        attackAmnt = attackMon.statBlock['Mysticism'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2) 
        defence = defenceMon.statBlock['Tinfoil'] + defTrainLevel + random.randint(-1, 5)
    else:
        attackAmnt = attackMon.statBlock['Strength'] + attackTrainLevel + math.ceil((attackTrainLevel + activeAttack.baseDamage) * .2)
        defence = defenceMon.statBlock['Endurance'] + defTrainLevel + random.randint(-1, 5)
    hp2 = defenceMon.statBlock['currentHealth']
    dodge = defenceMon.statBlock['Agility'] + math.ceil(defence/2) 
    damage = 0
    hit = 1
    atkTypeBonus = 1
    defTypeBonus = 1
    if (dodge + random.randint(-abs(attackTrainLevel),100)) > (90 - defTrainLevel): # check for dodge
        if ((attackAmnt + attackMon.statBlock['Agility']) + random.randint(-10, 10)) >= dodge: # check for glance
            hit = 2
        else:
            hit = 0
    if hit > 0:
        for x in range(1,3):
            atkTypeBonus = isTypeStrong(activeAttack.moveElementType, defenceMon.statBlock[defenceMon.keyList[x]]) + atkTypeBonus
        for x in range(1,3):
            defTypeBonus = isTypeWeak(defenceMon.statBlock[defenceMon.keyList[x]], activeAttack.moveElementType) + defTypeBonus
        damage = (attackAmnt * atkTypeBonus) - (defence * defTypeBonus)
        if damage <= 0:
            damage = 1
        else:
            damage = math.ceil(damage/hit)
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
            attackAnimation(attackingMon.bodyBlock, defMon.bodyBlock, attackIsPlayer, 0, amntOfDmg, attackingMon.statBlock['currentHealth'], hpBeforeDmg, attackText)
            scrollText = (attackingMon.statBlock['given_name'] + " did " + str(amntOfDmg) + " points of damage!")
        else:
            attackAnimation(defMon.bodyBlock, attackingMon.bodyBlock, attackIsPlayer, 0, amntOfDmg, hpBeforeDmg, attackingMon.statBlock['currentHealth'], attackText)
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


def autoSwitchMon(playerInfo):
    if playerInfo.friends[0].statBlock['currentHealth'] < 1:
        x = 0
        for monsters in playerInfo.friends:
            if playerInfo.friends[x].statBlock['currentHealth'] > 0:
                switchActiveMon(playerInfo, playerInfo.friends[0], playerInfo.friends[x], x)
            x = x + 1


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


def playerInformation(playerInfo):
    thumby.display.fill(0)
    thumby.display.drawText(playerInfo.playerBlock['name'], 1, 1 ,1)
    thumby.display.blit(bytearray(player3_sprite),1 ,10 ,8 ,8 ,0 ,0 ,0)
    thumby.display.drawText("Lvl: " + str(playerInfo.playerBlock['trainerLevel']), 1, 20, 1)
    thumby.display.drawText("Exp: " + str(playerInfo.playerBlock['experience']), 1, 29, 1)
    thumby.display.update()
    time.sleep(2)


def displayItems(playerInfo):
    thumby.display.fill(0)
    curSelect = 0
    tempSelect = curSelect
    cancelCheck = 0
    optionList = []
    for items in playerInfo.inventory:
        optionList.append(items.name)
    x = len(optionList)
    if x > 0:
        while curSelect < 11:
            bottomScreenText = ("CurHP:" + str(playerInfo.friends[0].statBlock['currentHealth']))
            tempSelect = curSelect
            curSelect = showOptions(optionList, curSelect, bottomScreenText)
            if curSelect ==  31:
                playerInfo.inventory[tempSelect].doAction(playerInfo.friends[0]) 
                playerInfo.inventory.pop(tempSelect)
            elif curSelect == 30:
                pass
            elif curSelect > 11:
                curSelect = tempSelect
            thumby.display.update()
    else:
        pass


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
        print("currentSelect = ", currentSelect)
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
        if currentSelect == 31 and combatCheck == 0:
            if playerInfo.friends[0] != playerInfo.friends[x] or startOfgameCheck == 1:
                switchActiveMon(playerInfo, monsterListInfo[0], monsterListInfo[x], x)
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
                print(currentSelect, " = currentSelect")
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
        subOptionsFriends = ["Swap Active", "Train", "Learn Attack", "Give Name", "Mutate", "Back"]
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
                    goBack = 0
                    curSelect = 1
                    while(goBack != 1):
                        thumby.display.fill(0)
                        if curSelect == 28 or curSelect == 29:
                            curSelect = tempSelect
                        tempSelect = curSelect
                        curSelect = showOptions(subOptionsFriends, curSelect, "My Friends")
                        if curSelect == 31:
                            curSelect = tempSelect
                            if subOptionsFriends[curSelect] == subOptionsFriends[0]:
                                showMonInfo(playerInfo)
                            if subOptionsFriends[curSelect] == subOptionsFriends[1]:
                                trainActiveMon(playerInfo.friends[0].statBlock, playerInfo.friends[0].bodyBlock)
                            if subOptionsFriends[curSelect] == subOptionsFriends[2]:
                                trainAnAttackMove(playerInfo.friends[0].attackList, playerInfo.friends[0].statBlock, playerInfo.friends[0].keyList)
                                while len(playerInfo.friends[0].attackList) > 6:
                                    popItOff(playerInfo.friends[0].attackList, "moves! Please forget one!")
                            if subOptionsFriends[curSelect] == subOptionsFriends[3]:
                                playerInfo.friends[0].statBlock['given_name'] = giveName(playerInfo.friends[0].statBlock['given_name'])
                            if subOptionsFriends[curSelect] == subOptionsFriends[4]:
                                playerInfo.friends[0].mutateMon()
                            if subOptionsFriends[curSelect] == subOptionsFriends[5]:
                                curSelect = 1
                                goBack = 1
                        if curSelect == 30:
                            curSelect = 1
                            goBack = 1
                        thumby.display.update()
                if optionList[curSelect] == optionList[2]:
                    displayItems(playerInfo)
                if optionList[curSelect] == optionList[3]:
                    save(playerInfo)
                    thingAquired("","Game","Saved","", 1, 0)
                if optionList[curSelect] == optionList[4]: 
                    cancelCheck = 1
            if curSelect == 30:
                cancelCheck = 1
                thumby.display.fill(0)
            thumby.display.update()


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
    

def makeMonsterList(mSeed):
    gc.collect()
    random.seed(mSeed) 
    monsterList = []
    for i in range (0 , 25): # numberOfMons = 25
        thingAquired("", "Generating", "Monsters",str(i+1), 0)
        newMon = Monster()
        newMon.makeMonster()
        monsterList.append(newMon)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(1,3), "Default")
        monsterList[i].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(1,3), "Default")
        monsterList[i].attackList.append(newMonAtk)
        newMonAtk = AttackMove()
        newMonAtk.getAnAttackMove(random.randint(1,4), monsterList[i].statBlock['Type1'])
        monsterList[i].attackList.append(newMonAtk)
        noDupAtk(newMon.attackList)
        monsterList[i].makeMonBody()
    return monsterList
    

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
    tameMon(newPlayer, newPlayer.friends[0])
    newPlayer.friends.pop(0)
    newItem = Item("Crystals", 3, random.randint(0,7))
    newPlayer.inventory.append(newItem)
    newPlayer.inventory.append(newItem)
    thingAquired("", "Good", "Luck", "", 2)
    newPlayer.playerBlock['worldSeed'] = seed 
    return newPlayer 
    

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


def findAnItem(playerInv, maxItems):
    #gc.collect()
    newItem = Item("GenHeal", 1)
    newItem.getItem()
    playerInv.append(newItem)
    thingAquired("You", "found", newItem.name, "", 2)
    if maxItems <= len(playerInv):
        popItOff(playerInv, "items! Please lose one.")


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


def printMon(monsterBody, x, y, playerOrNPC):
        thumby.display.blit(bytearray(monsterBody['head']), x, y, 20, 9, 0, playerOrNPC, 0)
        thumby.display.blit(bytearray(monsterBody['body']), x, y+9, 20, 9, 0, playerOrNPC, 0)
        thumby.display.blit(bytearray(monsterBody['legs']), x, y+18, 20, 9, 0, playerOrNPC, 0)

    
def trainAnimation(monsterBody):
    f = open('/Games/Tiny_Monster_Trainer/Curtian/Other.ujson')
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


def openScreen():
    gc.collect()
    thumby.display.setFPS(40)
    f = open('/Games/Tiny_Monster_Trainer/Curtian/Other.ujson')
    images = ujson.load(f)
    myScroller = TextForScroller("Press A to Start or B to Load!")
    while(1):
        whatDo = 0
        thumby.display.fill(0)
        thumby.display.blit(bytearray(images["introTail"]), 0, 0, 25, 30, 0, 0, 0)
        thumby.display.blit(bytearray(images["introHead"]), 47, 0, 25, 30, 0, 1, 0)
        thingAquired("Tiny", "Monster", "Trainer!", "", 0, 1, 1)
        thumby.display.drawLine(0, 28, 72, 28, 1)
        thumby.display.drawText(myScroller.scrollingText, -abs(myScroller.moveScroll())+80, 30, 1)
        thumby.display.update()
        whatDo = buttonInput(whatDo)
        if whatDo == 31:
            battleStartAnimation(0)
            f.close()
            return 0
        elif whatDo == 30:
            try:
                p = open("/Games/Tiny_Monster_Trainer/Curtian/tmt.ujson", "r")
                p.close()
            except OSError:
                battleStartAnimation(0)
                f.close()
                return 0
            battleStartAnimation(0)
            f.close()
            return 1
    


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
    bigDict = [{"player" : playerInfo.playerBlock, "items" : [itemDict], "monsterInfo": [statDict, bodyDict, attackDict, mutateDict]}]
    #print(bigDict)
    with open('/Games/Tiny_Monster_Trainer/Curtian/tmt.ujson', 'w') as f:
        ujson.dump(bigDict, f)
        f.close()

def loadGame():
    gc.collect()
    tempPlayer = Player()
    f = open('/Games/Tiny_Monster_Trainer/Curtian/tmt.ujson')
    bigJson = ujson.load(f)
    tempPlayer.playerBlock = bigJson[0]['player'].copy()
    if bigJson[0]['items'] != [{}]:
        for x in range(0, len(bigJson[0]['items'])):
            tempPlayer.inventory.append(Item(bigJson[0]['items'][0]['item' + str(x)]['name'], bigJson[0]['items'][0]['item' + str(x)]['key'], bigJson[0]['items'][0]['item' + str(x)]['bonus'])) ############# key, bonus=0
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


def makeRandomStats(monToStat, trainerLevel):
    random.seed(time.ticks_ms())
    tempMon = monToStat
    tempMon.statBlock = tempMon.statBlock.copy()
    genStat = tempMon.makeStat
    tempMon.statBlock['Health'] = genStat(0) + random.randint(0, trainerLevel) 
    if tempMon.statBlock['Health'] > tempMon.statBlock['maxHealth']:
        tempMon.statBlock['Health'] = tempMon.statBlock['maxHealth']
    tempMon.statBlock['currentHealth'] = tempMon.statBlock['Health']
    for x in range (4,9):
        tempMon.statBlock[tempMon.keyList[x]] = genStat(0) + random.randint(0, trainerLevel)
        if tempMon.statBlock[tempMon.keyList[x]] > tempMon.statBlock['max' + tempMon.keyList[x]]:
            tempMon.statBlock[tempMon.keyList[x]] = tempMon.statBlock['max' + tempMon.keyList[x]]
    return tempMon

    
def makeRandomMon(monsterList, roomElm):
    random.seed(time.ticks_ms())
    spawnType = ["Earth", "Wind", "Water", "Fire", "Light", "Darkness", "Cute", 
                "Mind", "Physical", "Mystical", "Ethereal"]
    for x in range(0,10):
        thisGuyRightHere = monsterList[random.randint(0,24)]
        if (thisGuyRightHere.statBlock['Type1'] == spawnType[roomElm]
                or thisGuyRightHere.statBlock['Type2'] == spawnType[roomElm] 
                or thisGuyRightHere.statBlock['Type3'] == spawnType[roomElm]):
            thisGuyRightHere = makeRandomStats(thisGuyRightHere, 0)
            return thisGuyRightHere
    thisGuyRightHere = monsterList[random.randint(0,24)]
    thisGuyRightHere = makeRandomStats(thisGuyRightHere, 0)
    return thisGuyRightHere


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
monsterList=[]
myGuy = Player()
load = openScreen()
if load == 1: 
    myGuy = loadGame()
    if myGuy.playerBlock["worldSeed"] == 0:
        theWorldSeed = time.ticks_us()
        myGuy.playerBlock["worldSeed"] = theWorldSeed
    world = makeWorld(myGuy.playerBlock['worldSeed'])
    monsterList = makeMonsterList(myGuy.playerBlock['worldSeed'])
else:
    theWorldSeed = time.ticks_us()
    random.seed(theWorldSeed)
    world = makeWorld(theWorldSeed)
    monsterList = makeMonsterList(theWorldSeed) 
    myGuy = makePlayer(monsterList[0], monsterList[1], monsterList[2], theWorldSeed)

npcMon = Monster()
activeMon = 0
room = 13 
tempRoom = room
npcMonRoaming = RoamingMonster()
monsterMovement = 0
battle = 0
victory = 0

## Pretty much the game after this point :D ##

while(1):
    gc.collect()
    #micropython.mem_info()
    while(battle != 1):
        thumby.display.fill(0)
        room = mapChangeCheck(myGuy, world[room], room) # draw world map
        if tempRoom != room:
            npcMonRoaming.removeMonster()
            npcMonRoaming.placeMonster(world[room])
            tempRoom = room
            monsterMovement = random.randint(0,2)
        myGuy.movePlayer(world[room], npcMonRoaming, monsterMovement) # draws roaming monster & player
        optionScreen(myGuy)
        thumby.display.update()
        if myGuy.currentPos == npcMonRoaming.currentPos:
            npcMonRoaming.removeMonster()
            battle = 1
            battleStartAnimation(1)
    npcMon = makeRandomMon(monsterList, world[room].elementType)
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
                            thingAquired(npcMon.statBlock['name'], "was", "Tamed!", "<3", 3)
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
            showMonInfo(myGuy)
            victory = 0
        thumby.display.update()
    battleStartAnimation(0) 
    if victory == 1:
        myGuy.levelUpCheck()
        myGuy.friends[0].statBlock['trainingPoints'] = myGuy.friends[0].statBlock['trainingPoints'] + 1
        if len(myGuy.inventory) < myGuy.maxHelditems:
            randoNum = random.randint(1,10)
            if randoNum > 2:
                findAnItem(myGuy.inventory, myGuy.maxHelditems)
