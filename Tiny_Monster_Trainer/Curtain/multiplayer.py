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
from classLib import Player, Monster, TextForScroller, AttackMove
from funcLib import thingAquired, battleStartAnimation, printMon, drawArrows, showOptions, switchActiveMon, showMonInfo, obj_to_dict, buttonInput
from battle import Battle 


def loadGameString():
    gc.collect()
    f = open('/Games/Tiny_Monster_Trainer/Curtain/tmt.ujson')
    bigJson = ujson.load(f)
    f.close()
    return bigJson


def getKeyList(whatList=0):
    if whatList == 1:
        thisList = ['name', 'given_name','Health','Type1','Type2','Type3','Agility','Strength','Endurance','Mysticism','Tinfoil','head', 'body','legs']
    elif whatList == 2:
        thisList = ['monster', 'name', 'numUses', 'baseDamage', 'magic', 'moveElementType']
    elif whatList == 3:
        thisList = ['name', 'given_name','Health','Type1','Type2','Type3','Agility','Strength','Endurance','Mysticism','Tinfoil'] #,'head', 'body','legs']        
    elif whatList == 4: 
        thisList = ['head', 'body','legs'] 
    else:
        thisList = ['name', 'given_name','Health','Type1','Type2','Type3','Agility','Strength','Endurance','Mysticism','Tinfoil','head', 'body','legs']
    return thisList


def waitingForResponse(loadingStr, whatDoing):                
    thingAquired(whatDoing, "to other", "trainer!", loadingStr,0,0,0)
    loadingStr = loadingStr + "."
    if loadingStr == "...":
        loadingStr = ""
    return loadingStr


def getNumberOfKeyChecks(rcvCheckOrCheck, rangeNum):
    rcvCheck = {'key0' : 0}
    checkCheck = bytearray([0]) 
    myGuyBattleJson = loadGameString()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        for y in range(0,rangeNum):
            rcvCheck['key' + str(y+(x*rangeNum))] =  0 
            #thingAquired("rcvCheck", "key" + str(y+(x*rangeNum)) + " = ", str(rcvCheck['key' + str(y+(x*rangeNum))]), "",0,0,0)
            checkCheck[0] = checkCheck[0] + 1
    if rcvCheckOrCheck == 0:
        return checkCheck
    elif rcvCheckOrCheck == 1:
        return rcvCheck


def chopUpGuyToSend():
    dataToSend=[{}]
    myGuyBattleJson = loadGameString()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        if x > 0:
            dataToSend.append({})  # for data to send, might be able to go to the def with the list names and cycle through those to make this smaller
        dataToSend[x]['name'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['name']
        dataToSend[x]['given_name'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['given_name']
        dataToSend[x]['Health'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Health']
        dataToSend[x]['Type1'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Type1']
        dataToSend[x]['Type2'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Type2']
        dataToSend[x]['Type3'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Type3']
        dataToSend[x]['Agility'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Agility']
        dataToSend[x]['Strength'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Strength']
        dataToSend[x]['Endurance'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Endurance']
        dataToSend[x]['Mysticism'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Mysticism']
        dataToSend[x]['Tinfoil'] = myGuyBattleJson[0]['monsterInfo'][0]['mon' + str(x) + 'stat']['Tinfoil']
        dataToSend[x]['head'] = myGuyBattleJson[0]['monsterInfo'][1]['mon' + str(x) + 'body']['head']
        dataToSend[x]['body'] = myGuyBattleJson[0]['monsterInfo'][1]['mon' + str(x) + 'body']['body']
        dataToSend[x]['legs'] = myGuyBattleJson[0]['monsterInfo'][1]['mon' + str(x) + 'body']['legs'] 
    return dataToSend

    
def chopUpMovesToSend():   
    dataToSend=[{}]
    myGuyBattleJson = loadGameString()
    numberOfAtks = 0
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        for y in range(0, len(myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])): 
            if y == 0 and x == 0:
                pass
            else:
                dataToSend.append({})
            dataToSend[numberOfAtks]['monster'] =  x  
            dataToSend[numberOfAtks]['name'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['name'] 
            dataToSend[numberOfAtks]['numUses'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['numUses']
            dataToSend[numberOfAtks]['baseDamage'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['baseDamage']
            dataToSend[numberOfAtks]['magic'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['magic']
            dataToSend[numberOfAtks]['moveElementType'] = myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk']['attack' + str(y)]['moveElementType']
            numberOfAtks = numberOfAtks + 1
    return dataToSend
    

def getNumberOfKeyChecksMoves(rcvCheckOrCheck, rangeNum):
    rcvCheck = {'key0' : 0}
    checkCheckM = bytearray([0]) 
    myGuyBattleJson = loadGameString()
    for x in range(0, len(myGuyBattleJson[0]['monsterInfo'][0])):
        for y in range(0, len(myGuyBattleJson[0]['monsterInfo'][2]['mon' + str(x) + 'atk'])):
            for z in range(0,rangeNum):
                checkCheckM[0] = checkCheckM[0] + 1
                rcvCheck['key' + str(checkCheckM[0])] =  0
    if rcvCheckOrCheck == 0:
        return checkCheckM
    elif rcvCheckOrCheck == 1:
        return rcvCheck    


def findWhoSendsFirst():
    t0 = 0
    handshakeTimer = 0
    random.seed(time.ticks_ms())
    whoSendsFirst = bytearray([0]) 
    whoSendsFirst[0] = random.randint(1, 255)
    whoSendsFirstRcvd = bytearray([0]) 
    loadingStr = ""
    timerTrigger = 0
    while(t0 - handshakeTimer < 30):
        if timerTrigger == 1:
            t0 = time.ticks_ms()
        loadingStr = waitingForResponse(loadingStr, "Calling")
        thumby.link.send(whoSendsFirst)
        received = thumby.link.receive()
        if received != None:
            if handshakeTimer == 0:
                whoSendsFirstRcvd = received
                handshakeTimer = time.ticks_ms()
                timerTrigger = 1
                #i should do something if whoSendsFirst[0] == whoSendsFirstRcvd[0] but the odds of that are so low that i probably won't
    if whoSendsFirst[0] > whoSendsFirstRcvd[0]:
        sOr = 1
    else:
        sOr = 0
    return sOr


def sendOrReceiveGuy(sOr):   
    yourGuyJson = {}
    loadingStr = ""
    rcvCheckPlayer = {'key0' : {}}
    sendCheckPlayer = {'key0' : {}}
    rcvCheckPlayer['key0'] = 0 
    sendCheckPlayer['key0'] = 0
    myGuyBattleJson = loadGameString()
    justMyGuy = myGuyBattleJson[0]['player']
    del myGuyBattleJson
    for z in range(0,2):
        if sOr == 1:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, "Calling") 
                thumby.link.send(ujson.dumps(justMyGuy).encode())
                received = thumby.link.receive()
                if received != None:
                    rcvCheckPlayer = ujson.loads(received.decode())
                    if rcvCheckPlayer['key0'] != 1:
                        rcvCheckPlayer['key0'] = 0
        if sOr == 0:
            while(rcvCheckPlayer['key0'] == 0):
                loadingStr = waitingForResponse(loadingStr, "Calling")
                sendCheckPlayer['key0'] = 1
                received1 = thumby.link.receive()
                if received1 != None:
                    yourGuyJson = ujson.loads(received1.decode())
                    thumby.link.send(ujson.dumps(sendCheckPlayer).encode())
                    if rcvCheckPlayer['key0'] != 1:
                        rcvCheckPlayer['key0'] = 1
        rcvCheckPlayer['key0'] = 0
        if sOr == 0:
            sOr = 1
        else:
            sOr = 0 
    return yourGuyJson
                      

def sendCheckAndGetCheck(checkCheckNum):
    t0 = 0
    handshakeTimer = 0
    timerTrigger = 0
    loadingStr = ""
    checkCheckOther = bytearray([0])
    while(t0 - handshakeTimer < 300):
        if timerTrigger == 1:
            t0 = time.ticks_ms()
        loadingStr = waitingForResponse(loadingStr, "Sending Vibe")
        thumby.link.send(checkCheckNum)
        received = thumby.link.receive()
        if received != None:
            if handshakeTimer == 0:
                checkCheckOther = received
                handshakeTimer = time.ticks_ms()
                timerTrigger = 1
    return checkCheckOther
                        

def sendAndReceive(dataToSend, checkCheck, checkCheckOther, sendOrReceive, rcvCheckNum, numOfData=0, listNumber=0):
    keyList = getKeyList(listNumber)
    sendCheck = {'key0' : 0}
    dataBeingRcvd = [{}]
    xSame = 0
    loadingStr = ""
    time.sleep(.1) #11*3*22
    for c in range(0, (checkCheckOther[0])):
        sendCheck['key' + str(c)] =  0
    for z in range(0,2):
        if sendOrReceive == 1:
            for x in range (0, ((checkCheck[0])/numOfData)): 
                for y in range (0, numOfData):
                    dictToSend = {}
                    dictToRcv = {}
                    while rcvCheckNum['key' + str(y+(x*numOfData))] == 0: 
                        dictToSend['key'] = y
                        dictToSend['key2'] = y+(x*numOfData)
                        dictToSend[keyList[y]] = dataToSend[x][keyList[y]] #this is where the data I care about is being sent
                        thumby.link.send(ujson.dumps(dictToSend).encode()) 
                        received1 = thumby.link.receive()
                        dictToSend.pop(keyList[y])
                        if received1 != None:
                            try:
                                dictToRcv = ujson.loads(received1.decode())
                                loadingStr = waitingForResponse(loadingStr, "Speaking")
                                if dictToRcv['key2'] != dictToSend['key2']: #if key2 isn't different, don't advance rcvCheckNum so that it'll keep trying to send the same information to the other thumby
                                    rcvCheckNum['key'+str(y+(x*numOfData))] = 1 #if key2 is different advance change it to once so that the while ends and the x/y loops can adv
                                    loadingStr = waitingForResponse(loadingStr, "Speaking")
                            except:
                                pass
        sendLoopExit = math.ceil((checkCheckOther[0])/numOfData)
        if sendOrReceive == 0:
            for x in range (0, ((checkCheckOther[0])/numOfData)): 
                for y in range (0, numOfData):
                    dictToSend = {} 
                    dictToRcv = {}
                    while sendCheck['key' + str(y+(x*numOfData))] == 0:
                        dictToSend['key'] = y
                        dictToSend['key2'] = y+(x*numOfData)
                        thumby.link.send(ujson.dumps(dictToSend).encode())
                        received2 = thumby.link.receive()
                        if received2 != None: 
                            try:   
                                dictToRcv = ujson.loads(received2.decode())
                                loadingStr = waitingForResponse(loadingStr, "Listening")
                                if dictToRcv['key2'] == dictToSend['key2']:
                                    if x > 0 and xSame != x+y:                                    
                                        dataBeingRcvd.append({})
                                        xSame = x+y
                                    dataBeingRcvd[x][keyList[dictToRcv['key']]] = dictToRcv[keyList[dictToRcv['key']]] #original line: dataBeingRcvd[x][keyList[dictToRcv['key']]] = dictToRcv[keyList[y]]
                                    sendCheck['key' + str(y+(x*numOfData))] = 1
                                    loadingStr = waitingForResponse(loadingStr, "Listening")
                                    for m in range(0, len(dataBeingRcvd)):
                                        try:
                                            if dataBeingRcvd[m] == {}:
                                                dataBeingRcvd.pop(m)
                                        except:
                                            pass
                            except:
                                pass
                if y == (numOfData - 1) and x == (sendLoopExit - 1):
                    dictToSend['key2'] = (y+(x*numOfData)+1)
                    thumby.link.send(ujson.dumps(dictToSend).encode())
        if sendOrReceive == 0:
            sendOrReceive = 1
        else:
            sendOrReceive = 0 
        time.sleep(.5)
    return dataBeingRcvd
    

def putGhostTogether(otrMonData, otrMonMoves, yourGuyJson):
    monKeys = getKeyList(3)
    bodKeys = getKeyList(4)
    opponent = Player()
    opponent.playerBlock['name'] = yourGuyJson['name']
    opponent.playerBlock['trainerLevel'] = yourGuyJson['trainerLevel']
    opponent.playerBlock['experience'] = yourGuyJson['experience']
    opponent.playerBlock['friendMax'] = yourGuyJson['friendMax']
    opponent.playerBlock['worldSeed'] = yourGuyJson['worldSeed']
    for x in range(0, len(otrMonData)):
        rezMon = Monster()
        for y in range(0, len(monKeys)):
            monKeys = getKeyList(1)
            rezMon.statBlock[monKeys[y]] = otrMonData[x][monKeys[y]]
        for b in range(0, len(bodKeys)):
            rezMon.bodyBlock[bodKeys[b]] = otrMonData[x][bodKeys[b]]
        for z in range(0, len(rcvOtrMonMoves)):
            if rcvOtrMonMoves[z]['monster'] == x:
                tempAttackMove = AttackMove(otrMonMoves[z]['name'],
                                    otrMonMoves[z]['numUses'],
                                    otrMonMoves[z]['baseDamage'],
                                    otrMonMoves[z]['magic'],
                                    otrMonMoves[z]['moveElementType'])
                tempAttackMove.currentUses = otrMonMoves[z]['numUses']
                rezMon.attackList.append(tempAttackMove) 
        rezMon.attackList = rezMon.attackList.copy()
        opponent.friends.append(rezMon)
        opponent.friends = opponent.friends.copy()
    saveGhost(opponent)    
    

def saveGhost(ghostInfo):
    gc.collect()
    statDict = {}
    bodyDict = {}
    attackDict = {}
    for x in range(0, len(ghostInfo.friends)):
        tempAttackDict = {}
        for y in range (0, len(ghostInfo.friends[x].attackList)):
            tempAttackDict["attack" + str(y)] = obj_to_dict(ghostInfo.friends[x].attackList[y])
            attackDict["mon" + str(x) + "atk"] = tempAttackDict
        statDict["mon" + str(x) + "stat"] = ghostInfo.friends[x].statBlock
        bodyDict["mon" + str(x) + "body"] = ghostInfo.friends[x].bodyBlock
    playerDict = [{"player" : ghostInfo.playerBlock, "monsterInfo": [statDict, bodyDict, attackDict]}]
    with open('/Games/Tiny_Monster_Trainer/Ghosts/'+ghostInfo.playerBlock['name']+'.ujson', 'w') as f:
        ujson.dump(playerDict, f)
        f.close()
    del playerDict
    gc.collect()            

    
def doTheThing(dataNum, sOr):
    dataToSend1=[{}]
    listNum = 0
    checkCheck1 = bytearray([0]) 
    checkCheck1 = getNumberOfKeyChecks(0, dataNum)
    rcvCheck1 = {'key0' : 0} 
    if dataNum == 14:
        checkCheck1 = getNumberOfKeyChecks(0, dataNum)
        rcvCheck1 = getNumberOfKeyChecks(1, dataNum)
        dataToSend1 =  chopUpGuyToSend() 
        listNum = 1
    else:
        checkCheck1 = getNumberOfKeyChecksMoves(0, 6)
        rcvCheck1 = getNumberOfKeyChecksMoves(1, 6)
        dataToSend1 = chopUpMovesToSend()
        listNum = 2
    time.sleep(1)
    checkCheckOther1 = sendCheckAndGetCheck(checkCheck1)
    time.sleep(1)
    dataFromOtherThumby = sendAndReceive(dataToSend1, checkCheck1, checkCheckOther1, sOr, rcvCheck1,  dataNum, listNum)   
    return dataFromOtherThumby   


#########################################################################################################


def loadGame():
    gc.collect()
    tempPlayer = Player()
    bigJson = loadGameString()
    tempPlayer.playerBlock = bigJson[0]['player'].copy()
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


def drawArrowsGhost(d, u): # x, y):
    #arrowLR = [4,4,4,31,14,4] # 6 x 5
    arrowUD = [8,24,63,24,8] # 5 x 6
    thumby.display.blit(bytearray(arrowUD), 66, 20, 5, 6, d, 0, 0)
    thumby.display.blit(bytearray(arrowUD), 66, 3, 5, 6, u, 0, 1)


def drawIntro(player, ghost):
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
        thumby.display.fill(0)
        if(t0 - ct0 > 2800):
            thingAquired(player.playerBlock['name'], "Vs", ghost.playerBlock['name'], "Good Luck!",0,1,1)
            thumby.display.blit(bytearray(player.sprite), x-8 , y, 8, 8, -1, 1, 0)
            thumby.display.blit(bytearray(ghost.sprite), 72-x , y, 8, 8, -1, ghost.lOrR, 0)
        animateCount = animateCount + 1 
        thumby.display.drawFilledRectangle(-36+animateCount, 0, 36, 40, 1)
        thumby.display.drawFilledRectangle(72-animateCount, 0, 36, 40, 1)
        
        thumby.display.update()
 

def multiStaChk(mon2Chk, atkSel):
    if mon2Chk.attackList[atkSel].currentUses <= 0:
        outStaHP = math.floor(mon2Chk.statBlock['currentHealth'] * 0.7)
        thingAquired(mon2Chk.statBlock['given_name'], "doesn't have", "enough", "stamina!", 2, 0, 0)
        thingAquired(mon2Chk.statBlock['given_name'], "hurt itself", "& goes down", "to "+str(outStaHP)+" HP!", 2, 0, 0)
        mon2Chk.statBlock['currentHealth'] = outStaHP
    mon2Chk.attackList[atkSel].currentUses = mon2Chk.attackList[atkSel].currentUses -1                            


def tinyPause():
    #thumby.display.fill(0)
    #thumby.display.update() 
    time.sleep(.2)


def toBtl(myGuy, nme, sOr):
    gc.collect()

    battle=1
    btl = Battle()
    btl.setBattle(myGuy, nme, 1)
    myScroller = TextForScroller(myGuy.friends[0].statBlock['given_name'] + " has entered into battle with " + nme.friends[0].statBlock['given_name'] + "! Their trainer's level is " + str(nme.playerBlock['trainerLevel']) +"!" )
    curSelect = 1
    prevSelect = 1
    ###multiplayer vars
    nmeActiveInfo = [{"sAndrKey" : "", "given_name" : nme.friends[0].statBlock['given_name'], "attackNameStr" : ""}]
    nmeAttackRdy = 0
    myAtkName = ""
    myAttackRdy = 0
    attackResultsKeep =  [{}] 

    while(battle == 1):
        prevSelect = curSelect
        curSelect = btl.drawScreen(myScroller, myGuy, nme, curSelect, prevSelect)
        btl.battleBlock['myB4hp'] = myGuy.friends[0].statBlock['currentHealth'] - 0
        btl.battleBlock['nmeB4hp'] = nme.friends[0].statBlock['currentHealth'] - 0
        
        if nmeActiveInfo != None:
            if nmeActiveInfo[0]['given_name'] != nme.friends[0].statBlock['given_name'] or (nmeActiveInfo[0]['given_name'] != None and nmeActiveInfo[0]['given_name'] != nme.friends[0].statBlock['given_name']):
                for x in range(0, len(nme.friends)): 
                    if nme.friends[x].statBlock['given_name'] == nmeActiveInfo[0]['given_name']:
                        tempName = nme.friends[0].statBlock['given_name']
                        switchActiveMon(nme, nme.friends[0], nme.friends[x], x) #y'know, this looks redundant? but it works, check out later
                        nmeAttackRdy = 0
                        myAttackRdy = 0
                        thingAquired(nme.playerBlock['name'], "told", tempName, "to retreat!", 1,0,0)
                        thingAquired(nme.playerBlock['name'], "told", nme.friends[0].statBlock['given_name'], "to attack!", 1,0,0)
        
        if nmeActiveInfo != None:
            if nmeAttackRdy == 0:
                if nmeActiveInfo[0]['attackNameStr'] != "" or (nmeActiveInfo[0]['attackNameStr'] != None and nmeActiveInfo[0]['attackNameStr'] != "") :
                    for x in range(0, len(nme.friends[0].attackList)): 
                        if nme.friends[0].attackList[x].name == nmeActiveInfo[0]['attackNameStr']:
                            tempName = nme.friends[0].attackList[x].name
                            btl.battleBlock['nmeAtkSlct'] = x
                            nmeAttackRdy = 1
                else:
                    nmeAttackRdy = 0

        if btl.battleBlock['curAtkSlct'] != 15:
            for x in range(0, len(myGuy.friends[0].attackList)): 
                if myGuy.friends[0].attackList[x].name == myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].name:
                    myAtkName = myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].name
                    myAttackRdy = 1
        nmeActiveInfo = sAndrCheckActiveMon(myGuy.friends[0].statBlock['given_name'], myAtkName, nmeActiveInfo, ("test"+str(myAttackRdy)))
        if nmeActiveInfo != None:
            if nmeActiveInfo[0]['sAndrKey'] == "test1" and myAttackRdy == 1 and nmeAttackRdy == 1:
                for x in range(0,50):
                    nmeActiveInfo = sAndrCheckActiveMon(myGuy.friends[0].statBlock['given_name'], myAtkName, nmeActiveInfo, ("test"+str(myAttackRdy)))
                tinyPause()

        
        if sOr == 1 and myAttackRdy == 1 and nmeAttackRdy == 1 and myGuy.friends[0].statBlock['currentHealth'] >= 1 and nme.friends[0].statBlock['currentHealth'] >= 1 :
            agileTie = random.randint(-2,1)
            if (myGuy.friends[0].statBlock['Agility'] + myGuy.playerBlock['trainerLevel'] + agileTie) >= (nme.friends[0].statBlock['Agility'] + nme.playerBlock['trainerLevel']):
                btl.battleBlock['whoFirst'] = 0
                btl.battleCrunch(myGuy.friends[0], nme.friends[0], btl.battleBlock['curAtkSlct'], btl.battleBlock['nmeAtkSlct'], btl.battleBlock['myTL'], btl.battleBlock['nmeTL']) 
            else:
                btl.battleBlock['whoFirst'] = 1
                btl.battleCrunch(nme.friends[0], myGuy.friends[0], btl.battleBlock['nmeAtkSlct'], btl.battleBlock['curAtkSlct'], btl.battleBlock['nmeTL'], btl.battleBlock['myTL'])

            if myGuy.friends[0].statBlock['currentHealth'] == 0 and myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].currentUses == 0:
                btl.battleBlock['myText'] = "ZzZz..."
            attackResultsSend = [{'nmeMonHP' : nme.friends[0].statBlock['currentHealth'], 'myMonHP': myGuy.friends[0].statBlock['currentHealth'], 'whoGoesFirst' : btl.battleBlock['whoFirst'], 'myText' : btl.battleBlock['myText'], 'nmeText' : btl.battleBlock['nmeText'], 'sAndrKey' : 'test4'}]
            del attackResultsKeep
            attackResultsKeep = attackResultsSend.copy()
                                
            while attackResultsSend[0]['sAndrKey'] == "test4":
                attackResultsSend = sAndrAfterDmg(attackResultsKeep)
            if attackResultsSend[0]['sAndrKey'] == "test5" or attackResultsSend[0]['sAndrKey'] == "test6" :
                for x in range(0,15):
                    attackResultsSend = sAndrAfterDmg(attackResultsKeep)
                tinyPause()
            del attackResultsSend
        
        
        if sOr == 0 and myAttackRdy == 1 and nmeAttackRdy == 1 and myGuy.friends[0].statBlock['currentHealth'] >= 1 and nme.friends[0].statBlock['currentHealth'] >= 1:
            attackResultsKeep[0]['sAndrKey'] = "test4"
            while attackResultsKeep[0]['sAndrKey'] == "test4":
                attackResultsKeep = sAndrAfterDmg(attackResultsKeep) 
            if attackResultsKeep[0]['sAndrKey'] == "test5" or attackResultsKeep[0]['sAndrKey'] == "test6" :
                for x in range(0,15):
                    attackResultsKeep = sAndrAfterDmg(attackResultsKeep)
                tinyPause()
            btl.battleBlock['nmeText'] = attackResultsKeep[0]['myText']
            btl.battleBlock['myText'] = attackResultsKeep[0]['nmeText']
            myGuy.friends[0].statBlock['currentHealth'] = attackResultsKeep[0]['nmeMonHP']
            nme.friends[0].statBlock['currentHealth'] = attackResultsKeep[0]['myMonHP'] 
            btl.battleBlock['whoFirst'] = attackResultsKeep[0]['whoGoesFirst']
            multiStaChk(myGuy.friends[0], btl.battleBlock['curAtkSlct'])
        
        
        if myAttackRdy == 1 and nmeAttackRdy == 1:
            flipSoR = 0 #I goofed somewhere and it's taking too long to unspagatti it, remeber to come and fix this
            if sOr == 0:
                flipSoR = 1
            if sOr == 1:
                flipSoR = 0
            btl.attackAnimation(myGuy.friends[0].bodyBlock, nme.friends[0].bodyBlock, myGuy.friends[0].statBlock['currentHealth'], nme.friends[0].statBlock['currentHealth'], myGuy.friends[0].attackList[btl.battleBlock['curAtkSlct']].moveElementType, nme.friends[0].attackList[btl.battleBlock['nmeAtkSlct']].moveElementType, flipSoR)
            if myGuy.friends[0].statBlock['currentHealth'] == 0:
                thingAquired(myGuy.friends[0].statBlock['given_name'], "was", "knocked", " out!", 1, 0, 0)
                autoSwitchMon(myGuy)
            if nme.friends[0].statBlock['currentHealth'] == 0:
                thingAquired(nme.friends[0].statBlock['given_name'], "was", "knocked", " out!", 1, 0, 0)
                checkAutoSwitch = nme.friends[0].statBlock['given_name']
                autoSwitchMon(ghost)
                if nme.friends[0].statBlock['given_name'] != checkAutoSwitch:
                    nmeActiveInfo = None
            myAttackRdy = 0
            btl.battleBlock['curAtkSlct'] = 15
            myAtkName = ""
            nmeAttackRdy = 0
            nmeActiveInfo[0]['attackNameStr'] = ""
            myScroller = TextForScroller(myGuy.friends[0].statBlock['given_name'] + " has " + str(myGuy.friends[0].statBlock['currentHealth']) + " HP. " + nme.friends[0].statBlock['given_name'] + " has " + str(nme.friends[0].statBlock['currentHealth']) + " HP.")
            myScroller.scroller = 0
        
        btl.battleBlock['whoFirst'] = 0
        autoSwitchMon(nme)
        autoSwitchMon(myGuy)

        if myGuy.friends[0].statBlock['currentHealth'] == 0:
            battle = 0
            battleStartAnimation(0)
            thingAquired("...............", "You", " Lost!", "...............", 3, 0, 0)
        if nme.friends[0].statBlock['currentHealth'] == 0:
            battle = 0
            battleStartAnimation(0)
            thingAquired("***************", "You", " Win!", "***************", 3, 0, 0)
    
        thumby.display.update() 


def sAndrCheckActiveMon(playerCurMonGName, activeAttack, theirPrevInfo, testKey):
    thingToSend = [{"sAndrKey" : testKey, "given_name" : str(playerCurMonGName), "attackNameStr" : str(activeAttack)}]
    thumby.link.send(ujson.dumps(thingToSend).encode())
    received = thumby.link.receive()

    if received != None:
        theirStuff = ujson.loads(received.decode())
        if theirStuff[0]['sAndrKey'] == "test1" or theirStuff[0]['sAndrKey'] == "test0":
            thumby.link.send(ujson.dumps(thingToSend).encode())
            return theirStuff
    else:
        return theirPrevInfo 


def sAndrAfterDmg(resultInfoList): 
        
    thumby.link.send(ujson.dumps(resultInfoList).encode())
    received = thumby.link.receive()

    if received != None:
        theirStuff = ujson.loads(received.decode())
        if theirStuff[0]['sAndrKey'] == "test5":
            theirStuff[0]['sAndrKey'] = "test6"
            return theirStuff
        elif theirStuff[0]['sAndrKey'] == "test4":
            theirStuff[0]['sAndrKey'] = "test5"
            return theirStuff
        else:
            return resultInfoList
    else:
        return resultInfoList 
        

def wantToPlayAgain():
    battleStartAnimation(0)
    waiting = True
    againSelect = 0
    while(waiting):
        thingAquired("Play", " Again?", "", "A:Y B:N", 0, 0, 0)
        if againSelect == 0:
            againSelect = buttonInput(againSelect)
            if againSelect == 31:
                waiting = False
            elif againSelect == 30:
                machine.reset()
            else:
                againSelect = 0


################################################################################        
#All the sending and receiving stuff
thumby.display.fill(0)
thumby.display.update()

#find out who sends first
sendOrReceive2 = findWhoSendsFirst()

### v- sending guy -v
time.sleep(.5)
yourGuyJson = {}
yourGuyJson = sendOrReceiveGuy(sendOrReceive2)    

### v- sending monsters -v
time.sleep(1)
rcvOtrMonData = doTheThing(14, sendOrReceive2)

### v- sending moves -v
time.sleep(1)  
rcvOtrMonMoves = doTheThing(6, sendOrReceive2)

#getting ghost setup for multiplayer
putGhostTogether(rcvOtrMonData, rcvOtrMonMoves, yourGuyJson)

ghostName = yourGuyJson['name']
del rcvOtrMonData
del rcvOtrMonMoves
del yourGuyJson
gc.collect()

thumby.display.fill(0)
thumby.display.update()

#################################################################################
#The Battle Part

myGuy = Player()
myGuy = loadGame()

ghost = Player()
ghost = loadGhost(ghostName)

while(1):
    drawIntro(myGuy, ghost)
    random.seed(time.ticks_ms())
   
    for x in range(0,len(myGuy.friends)):
        myGuy.friends[x].statBlock['currentHealth'] = myGuy.friends[x].statBlock['Health']
        for attacks in range(0, len(myGuy.friends[x].attackList)):
            myGuy.friends[x].attackList[attacks-1].currentUses = myGuy.friends[x].attackList[attacks-1].numUses
    for x in range(0,len(ghost.friends)):
        ghost.friends[x].statBlock['currentHealth'] = ghost.friends[x].statBlock['Health']
        for attacks in range(0, len(ghost.friends[x].attackList)):
            ghost.friends[x].attackList[attacks-1].currentUses = ghost.friends[x].attackList[attacks-1].numUses
    try:
        toBtl(myGuy, ghost, sendOrReceive2)
    except Exception as e:
        f = open("/Games/Tiny_Monster_Trainer/crashA.log", "w")
        f.write(str(e) + " on Line 898 ish")
        f.close()
    wantToPlayAgain()
