# Thumgeon

# Explore an endless, tough-as-nails pseudorandom dungeon
# crawler. Collect items, potions, and weapons, kill monsters
# with aforementioned loot -- and stay alive!

# Written by Mason Watmough for TinyCircuits.
# Last edited 22-Jun-2024

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from machine import freq, Pin
freq(250_000_000)

import thumby
from time import ticks_ms
from random import seed as random_seed, randint
from gc import enable as gc_enable, collect as gc_collect

freq(48_000_000)
gc_enable()

thumby.display.setFPS(30)
fontWidth = const(6) # 6 pixels per character


# Sprite data for game objects

swordSpr = bytes([3,7,14,92,56,48,200,64])
bowSpr = bytes([0,129,126,129,129,90,60,0])
potSpr = bytes([4,113,210,174,212,174,210,116])
keySpr = bytes([0,24,36,36,24,8,24,8])
snackSpr = bytes([96,192,184,52,42,19,14,4])
pantsSpr = bytes([0,252,254,14,14,254,252,0])
shirtSpr = bytes([156,254,254,212,172,254,254,156])
magicSpr = bytes([66,219,60,110,76,32,219,66])
blockSpr = bytes([160,110,170,102,10,230,170,102]) # Walls
stairSpr = bytes([126,253,253,241,241,193,193,126])
signSpr = bytes([28,42,54,250,238,54,42,28])
doorSpr = bytes([254,6,3,1,1,3,6,254])
chestSpr = bytes([252,70,126,74,82,126,70,252])
hpupSpr = bytes([124,16,96,0,240,82,39,2])
mpupSpr = bytes([120,16,32,16,120,2,7,2])
itemSprites = (swordSpr, bowSpr, potSpr, keySpr, snackSpr, pantsSpr, shirtSpr, magicSpr, hpupSpr, mpupSpr)

blobSpr = bytes([96,144,248,152,248,240,224,192])
spiritSpr = bytes([0,12,18,62,114,76,32,0])
arachSpr = bytes([96,208,240,116,114,228,120,0])
skeleSpr = bytes([48,8,214,127,213,10,48,0])
wizardSpr = bytes([144,204,254,247,204,16,122,4])
tempestSpr = bytes([0,20,84,92,170,174,42,12])
monsterSprites = (blobSpr, spiritSpr, arachSpr, skeleSpr, wizardSpr, tempestSpr)

shopSpr = bytes([128,228,106,210,64,254,72,254,64,92,98,92,64,126,202,132,255,
    234,245,234,245,234,229,48,174,249,63,249,174,48,224,255])

# Icons for HUD
hpSpr = bytes([30,62,120,62,30])
mpSpr = bytes([72,108,62,27,9])

signMessages = (
    bytes("I wonder\nif anyone\nwill see\nthis...?", 'ascii'),
    bytes("I've been\ndown here\nfor DAYS!", 'ascii'),
    bytes("Who keeps\nleaving\nweapons\ndown\nhere?", 'ascii'),
    bytes("Always\nremember:\nfinders\nkeepers!", 'ascii'),
    bytes("Man, I\nhad so\nmuch\ngold...\n...had...", 'ascii'),
    bytes("Hang in\nthere!\n- M.W.", 'ascii'),
    bytes("Happy\ncrawling,\nfellow\nknight.", 'ascii'),
    bytes("Only 8\ngold for\nan ULTRA\nSWORD!?", 'ascii'),
    bytes("Why do\nall these\npotions\ntaste so\nterrible?", 'ascii'),
    bytes("Am I the\nonly\nperson\ndown\nhere?", 'ascii'),
    bytes("This food\ncould be\ncenturies\nold...", 'ascii'),
    bytes("It smells\nlike an\nancient\ncloset.", 'ascii'),
    bytes("How many\nknights\nhave been\ndown\nhere?", 'ascii'),
    bytes("Who took\nmy epic\nbow!?", 'ascii'),
    bytes("Who keeps\nleaving\nrocks in\nmy shirt?", 'ascii'),
    bytes("Man...\nI'm\ntired.", 'ascii'),
    bytes("How do\nskeletons\ncarry GP\nwithout\npockets?", 'ascii'),
    bytes("HELP!\nWIZARD\nTURNED\nME INTO\nA SIGN", 'ascii'),
    bytes("I just\nkeep\ngoing\ndeeper.", 'ascii'),
    bytes("SCORPIONS\n\nSCORPIONS\nin a\nDUNGEON!", 'ascii'),
    bytes("Sure is\ndrafty\nfor a\ndungeon.", 'ascii'),
    bytes("Cool\nplace!\nToo many\nrooms.\n7 / 10", 'ascii'),
    bytes("SIX\nbroken\nbows and\nnot ONE\nsnack.", 'ascii'),
)


swL = Pin(3, Pin.IN, Pin.PULL_UP)
swR = Pin(5, Pin.IN, Pin.PULL_UP)
swU = Pin(4, Pin.IN, Pin.PULL_UP)
swD = Pin(6, Pin.IN, Pin.PULL_UP)
swA = Pin(24, Pin.IN, Pin.PULL_UP)
swB = Pin(27, Pin.IN, Pin.PULL_UP)

swLstate=1
swRstate=1
swUstate=1
swDstate=1
swAstate=1
swBstate=1

# Blocking input function

def getcharinputNew():
    global swLstate
    global swRstate
    global swUstate
    global swDstate
    global swAstate
    global swBstate

    if(swLstate==0 and swL.value() == 0):
        swLstate=1
        return 'L'
    elif(swLstate==1 and swL.value() == 1):
        swLstate=0

    if(swRstate==0 and swR.value() == 0):
        swRstate=1
        return 'R'
    elif(swRstate==1 and swR.value() == 1):
        swRstate=0

    if(swUstate==0 and swU.value() == 0):
        swUstate=1
        return 'U'
    elif(swUstate==1 and swU.value() == 1):
        swUstate=0

    if(swDstate==0 and swD.value() == 0):
        swDstate=1
        return 'D'
    elif(swDstate==1 and swD.value() == 1):
        swDstate=0

    if(swAstate==0 and swA.value() == 0):
        swAstate=1
        return '1'
    elif(swAstate==1 and swA.value() == 1):
        swAstate=0

    if(swBstate==0 and swB.value() == 0):
        swBstate=1
        return '2'
    elif(swBstate==1 and swB.value() == 1):
        swBstate=0

    return ' '


goldChr = "$" # Symbol for in-game currency or gold
curMsg = ""
lastHit = ""

def addhp(n):
    player.hp = player.hp + n
    if(player.hp > player.maxhp):
        player.hp = player.maxhp

def addmp(n):
    player.mp = player.mp + n
    if(player.mp > player.maxmp):
        player.mp = player.maxmp

def addgp():
    player.gp = player.gp + randint(1, 5) + floorNo
    if(player.gp > 999):
        player.gp = 999

class dungeonTile:
    def __init__(self, ttype, *data):
        self.tiletype = ttype
        self.tiledata = []
        for i in range(len(data)):
            self.tiledata.append(data[i])

    def actOn(self):
        global curMsg
        global roomno
        global floorNo
        global exitSpawned
        if(self.tiletype == 1):
            # Tile is a block
            curMsg = "a wall."

        elif(self.tiletype == 2):
            # Tile is a door
            if(len(self.tiledata) == 0):
                curMsg = "ERR!"
            else:
                curMsg = "" # entered
                global currentRoom
                global player
                currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                currentRoom = self.tiledata[0]
                player.tilex = self.tiledata[1]
                player.tiley = self.tiledata[2]

        elif(self.tiletype == 3):
            # Tile is stairs to next floor
            curMsg = "the exit?"
            roomno = 0
            exitSpawned = False
            floorNo = floorNo + 1
            currentRoom.tiles.clear()
            gc_collect()
            currentRoom = dungeonRoom()
            generateRoom(currentRoom)
            ensureExit(currentRoom)
            while(currentRoom.getTile(player.tilex, player.tiley).tiletype != 0):
                player.tilex = randint(1, 7)
                player.tiley = randint(1, 3)

        elif(self.tiletype == 4):
            # Tile is a sign
            if(len(self.tiledata) == 0):
                curMsg = "nothing."
            else:
                # Draw the sign's text
                thumby.display.fill(0)
                y = 0
                signMsg = str(self.tiledata, 'ascii')
                for line in signMsg.split("\n"):
                    thumby.display.drawText(line, 0, y, 1)
                    y = y + 8
                thumby.display.update()

                # Wait for the player to finish reading
                while(getcharinputNew() == ' '):
                    pass
                curMsg = ""

        elif(self.tiletype == 6):
            # Tile is a chest
            chestGold = randint(1, 15)
            player.gp += chestGold
            curMsg = "got "+goldChr+str(chestGold)+"!"
            self.tiledata.clear()
            self.tiletype = 0

        elif(self.tiletype == 7):
            # Tile is an item
            curMsg = itemname(self)
            # Check to see if the player can carry it
            if(player.maxwt - itemwt(itemname(self)) >= player.wt):
                # Pick it up off the ground
                player.inventory.append(itemname(self))
                player.wt = player.wt + itemwt(itemname(self))
                self.tiledata.clear()
                self.tiletype = 0
            else:
                # Explain why we can't pick it up.
                curMsg = "no room!"

        elif(self.tiletype == 8):
            # Tile is a monster
            if(player.helditem == -1):
                # Attack with hand for 1-3 dmg
                dmg = randint(1, 3)
                self.tiledata[1] = self.tiledata[1] - dmg
                curMsg = "hit " + str(dmg) + "pts"
                if(self.tiledata[1] <= 0):
                    # Monster is dead
                    self.tiledata.clear()
                    self.tiletype = 0
                    addgp()
            else:
                # Attack with held item
                if(player.mp >= manacost(player.inventory[player.helditem])):
                    player.mp = player.mp - manacost(player.inventory[player.helditem])
                    dmgrng = itemdmg(player.inventory[player.helditem])
                    dmg = randint(dmgrng[0], dmgrng[1])
                    self.tiledata[1] = self.tiledata[1] - dmg
                    curMsg = "hit " + str(dmg) + "pts"
                    if(self.tiledata[1] <= 0):
                        # Monster is dead
                        self.tiledata.clear()
                        self.tiletype = 0
                        addgp()
                    if(player.inventory[player.helditem] == "bsc lch" or player.inventory[player.helditem] == "adv lch" or player.inventory[player.helditem] == "ult lch"):
                        # Leech spell, add damage to health
                        addhp(dmg)
                    # Check if we're using a confusion spell
                    if(player.inventory[player.helditem] == "bsc cnfs"):
                        self.tiledata[2] = self.tiledata[2] + 3
                    elif(player.inventory[player.helditem] == "adv cnfs"):
                        self.tiledata[2] = self.tiledata[2] + 5
                    elif(player.inventory[player.helditem] == "ult cnfs"):
                        self.tiledata[2] = self.tiledata[2] + 8

                    # Check if we're using a healing spell
                    if(player.inventory[player.helditem] == "bsc heal"):
                        addhp(3)
                    elif(player.inventory[player.helditem] == "adv heal"):
                        addhp(5)
                    elif(player.inventory[player.helditem] == "ult heal"):
                        addhp(8)
                else:
                    # Couldn't cast, punch instead
                    dmg = randint(1, 3)
                    curMsg = "hit " + str(dmg) + "pts"
                    self.tiledata[1] = self.tiledata[1] - dmg
                    if(self.tiledata[1] <= 0):
                        # Monster is dead
                        self.tiledata.clear()
                        self.tiletype = 0
                        addgp()

        elif(self.tiletype == 9):
            # Shop tile, open shop inventory
            actpos = 0
            selpos = 0
            inventory = 0
            curMsg = ""
            while(swAstate != 1):
                thumby.display.fill(0)
                if(inventory == 0):
                    if(len(player.inventory) > 0):
                        selpos = min(selpos, len(player.inventory)-1)
                        thumby.display.drawText(player.inventory[selpos], 0, 8, 1)
                        thumby.display.drawText(goldChr+str(itemprice(player.inventory[selpos])[1]), 0, 16, 1)
                    if(actpos == 0):
                        thumby.display.drawFilledRectangle(0, 0, 24, 8, 1)
                        thumby.display.drawText("inv", 0, 0, 0)
                        thumby.display.drawText("sell", 32, 0, 1)
                    else:
                        thumby.display.drawText("inv", 0, 0, 1)
                        thumby.display.drawFilledRectangle(32, 0, 32, 8, 1)
                        thumby.display.drawText("sell", 32, 0, 0)
                else:
                    if(len(currentRoom.shopInv) > 0):
                        selpos = min(selpos, len(currentRoom.shopInv)-1)
                        thumby.display.drawText(currentRoom.shopInv[selpos], 0, 8, 1)
                        thumby.display.drawText(goldChr+str(itemprice(currentRoom.shopInv[selpos])[0]), 0, 16, 1)
                    if(actpos == 0):
                        thumby.display.drawFilledRectangle(0, 0, 32, 8, 1)
                        thumby.display.drawText("shop", 0, 0, 0)
                        thumby.display.drawText("buy", 40, 0, 1)
                    else:
                        thumby.display.drawText("shop", 0, 0, 1)
                        thumby.display.drawFilledRectangle(40, 0, 24, 8, 1)
                        thumby.display.drawText("buy", 40, 0, 0)
                thumby.display.drawText(goldChr+str(player.gp), 64-len(str(player.gp))*fontWidth, 32, 1)
                thumby.display.update()
                while(getcharinputNew() == ' '):
                    pass
                if(swUstate == 1):
                    selpos = max(0, selpos-1)
                elif(swDstate == 1):
                    if(inventory == 0):
                        # In player inv
                        selpos = min(len(player.inventory)-1, selpos+1)
                    else:
                        # In shop inv
                        selpos = min(len(currentRoom.shopInv)-1, selpos+1)
                elif(swLstate == 1):
                    actpos = 0
                elif(swRstate == 1):
                    actpos = 1
                elif(swBstate == 1):
                    # Player hit selection
                    if(actpos == 0):
                        # Player changed inventory
                        if(inventory == 0):
                            inventory = 1
                        else:
                            inventory = 0
                    else:
                        # Player traded item
                        if(inventory == 0 and len(player.inventory) > 0):
                            # Sell item
                            player.wt = player.wt - itemwt(player.inventory[selpos])
                            if(player.helditem == selpos):
                                player.helditem = -1
                            if(player.pantsitem == selpos):
                                player.pantsitem = -1
                            if(player.shirtitem == selpos):
                                player.shirtitem = -1
                            currentRoom.shopInv.append(player.inventory[selpos])
                            player.gp = player.gp + itemprice(player.inventory[selpos])[1]
                            player.inventory.pop(selpos)
                        else:
                            if(player.gp >= itemprice(currentRoom.shopInv[selpos])[0]):
                                # Buy item
                                player.wt = player.wt + itemwt(currentRoom.shopInv[selpos])
                                player.gp = player.gp - itemprice(currentRoom.shopInv[selpos])[0]
                                player.inventory.append(currentRoom.shopInv[selpos])
                                currentRoom.shopInv.pop(selpos)
                            else:
                                thumby.display.drawText("Not", 0, 24, 1)
                                thumby.display.drawText("enough", 0, 32, 1)
                                thumby.display.update()
                                while(getcharinputNew() == ' '):
                                    pass

        elif(player.helditem != -1):
            # If the player is holding an item, try using it
            if(itemtile(player.inventory[player.helditem]).tiledata[0] == 0):
                # Held item is a sword
                curMsg = "swing!"
            elif(itemtile(player.inventory[player.helditem]).tiledata[0] == 1):
                # Held item is a bow, shoot an arrow
                x = player.tilex
                y = player.tiley
                if(player.facing == 0):
                    # Player is facing upwards
                    y = player.tiley - 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        y = y - 1
                elif(player.facing == 2):
                    # Player is facing downward
                    y = player.tiley + 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        y = y + 1
                elif(player.facing == 1):
                    # Player is facing right
                    x = player.tilex + 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        x = x + 1
                elif(player.facing == 3):
                    # Player is facing left
                    x = player.tilex - 1
                    while(currentRoom.getTile(x, y).tiletype == 0):
                        x = x - 1
                if(currentRoom.getTile(x, y).tiletype == 8):
                    # Hit monster, deal damage
                    dmgrng = itemdmg(player.inventory[player.helditem])
                    dmg = randint(dmgrng[0], dmgrng[1])
                    currentRoom.getTile(x, y).tiledata[1] = currentRoom.getTile(x, y).tiledata[1] - dmg
                    curMsg = "hit " + str(dmg) + "pts"
                    if(currentRoom.getTile(x, y).tiledata[1] <= 0):
                        # Monster is dead
                        currentRoom.getTile(x, y).tiledata.clear()
                        currentRoom.getTile(x, y).tiletype = 0
                        addgp()
                else:
                    curMsg = "missed."

            elif(itemtile(player.inventory[player.helditem]).tiledata[0] == 7):
                # Held item is a spell, try casting it
                if(player.mp >= manacost(player.inventory[player.helditem])):
                    player.mp = player.mp - manacost(player.inventory[player.helditem])
                    x = player.tilex
                    y = player.tiley
                    if(player.facing == 0):
                        # Player is facing upwards
                        y = player.tiley - 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            y = y - 1
                    elif(player.facing == 2):
                        # Player is facing downward
                        y = player.tiley + 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            y = y + 1
                    elif(player.facing == 1):
                        # Player is facing right
                        x = player.tilex + 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            x = x + 1
                    elif(player.facing == 3):
                        # Player is facing left
                        x = player.tilex - 1
                        while(currentRoom.getTile(x, y).tiletype == 0):
                            x = x - 1
                    if(currentRoom.getTile(x, y).tiletype == 8 and player.inventory[player.helditem] != "bsc heal" and player.inventory[player.helditem] != "adv heal" and player.inventory[player.helditem] != "ult heal"):
                        # Hit monster, deal damage
                        dmgrng = itemdmg(player.inventory[player.helditem])
                        dmg = randint(dmgrng[0], dmgrng[1])
                        currentRoom.getTile(x, y).tiledata[1] = currentRoom.getTile(x, y).tiledata[1] - dmg
                        curMsg = "hit " + str(dmg) + "pts"
                        if(currentRoom.getTile(x, y).tiledata[1] <= 0):
                            # Monster is dead
                            currentRoom.getTile(x, y).tiledata.clear()
                            currentRoom.getTile(x, y).tiletype = 0
                            addgp()

                        if(player.inventory[player.helditem] == "bsc cnfs"):
                            currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] + 3
                        elif(player.inventory[player.helditem] == "adv cnfs"):
                            currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] + 5
                        elif(player.inventory[player.helditem] == "ult cnfs"):
                            currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] + 8

                        if(player.inventory[player.helditem] == "bsc lch" or player.inventory[player.helditem] == "adv lch" or player.inventory[player.helditem] == "ult lch"):
                            # Leech spell, add damage to health
                            addhp(dmg)
                    elif(player.inventory[player.helditem] != "bsc tlpt" and player.inventory[player.helditem] != "adv tlpt" and player.inventory[player.helditem] == "ult tlpt"):
                        curMsg = "missed."
                    if(player.helditem != -1 and player.inventory[player.helditem] == "bsc tlpt"):
                        currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                        if(x - player.tilex < 0):
                            dx = x - player.tilex + 1
                            if(dx < -3):
                                dx = -3
                            player.tilex = player.tilex + dx
                        elif(x - player.tilex > 0):
                            dx = x - player.tilex - 1
                            if(dx > 3):
                                dx = 3
                            player.tilex = player.tilex + dx
                        if(y - player.tiley < 0):
                            dy = y - player.tiley + 1
                            if(dy < -3):
                                dy = -3
                            player.tiley = player.tiley + dy
                        elif(y - player.tiley > 0):
                            dy = y - player.tiley - 1
                            if(dy > 3):
                                dy = 3
                            player.tiley = player.tiley + dy
                    elif(player.helditem != -1 and player.inventory[player.helditem] == "adv tlpt"):
                        currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                        if(x - player.tilex < 0):
                            dx = x - player.tilex + 1
                            if(dx < -5):
                                dx = -5
                            player.tilex = player.tilex + dx
                        elif(x - player.tilex > 0):
                            dx = x - player.tilex - 1
                            if(dx > 5):
                                dx = 5
                            player.tilex = player.tilex + dx
                        if(y - player.tiley < 0):
                            dy = y - player.tiley + 1
                            if(dy < -5):
                                dy = -5
                            player.tiley = player.tiley + dy
                        elif(y - player.tiley > 0):
                            dy = y - player.tiley - 1
                            if(dy > 5):
                                dy = 5
                            player.tiley = player.tiley + dy
                    elif(player.helditem != -1 and player.inventory[player.helditem] == "ult tlpt"):
                        currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                        if(x - player.tilex < 0):
                            dx = x - player.tilex + 1
                            if(dx < -7):
                                dx = -7
                            player.tilex = player.tilex + dx
                        elif(x - player.tilex > 0):
                            dx = x - player.tilex - 7
                            if(dx > 7):
                                dx = 7
                            player.tilex = player.tilex + dx
                        if(y - player.tiley < 0):
                            dy = y - player.tiley + 1
                            if(dy < -7):
                                dy = -7
                            player.tiley = player.tiley + dy
                        elif(y - player.tiley > 0):
                            dy = y - player.tiley - 1
                            if(dy > 7):
                                dy = 7
                            player.tiley = player.tiley + dy
                    if(player.inventory[player.helditem] == "bsc heal"):
                        addhp(3)
                    elif(player.inventory[player.helditem] == "adv heal"):
                        addhp(5)
                    elif(player.inventory[player.helditem] == "ult heal"):
                        addhp(8)
                else:
                    curMsg = "no mana!"
            elif(player.helditem != -1 and itemtile(player.inventory[player.helditem]).tiledata[0] == 2):
                # Held item is a potion, drink it
                curMsg = "yuck!"
                if(player.inventory[player.helditem] == "sml hpot"):
                    addhp(5)
                elif(player.inventory[player.helditem] == "sml mpot"):
                    addmp(5)
                elif(player.inventory[player.helditem] == "big hpot"):
                    addhp(8)
                elif(player.inventory[player.helditem] == "big mpot"):
                    addmp(8)
                player.wt = player.wt - itemwt(player.inventory[player.helditem])

                player.inventory.pop(player.helditem)
                player.helditem = -1

            elif(player.helditem != -1 and player.inventory[player.helditem] == "food"):
                # Held item is food, eat it
                curMsg = "yum!"
                player.inventory.pop(player.helditem)
                player.helditem = -1
                player.wt = player.wt - 1
                addhp(3)

            elif(player.helditem != -1 and player.inventory[player.helditem] == "hpup"):
                # Held item is hpup
                curMsg = "+5 maxhp!"
                player.wt = player.wt - itemwt(player.inventory[player.helditem])
                player.inventory.pop(player.helditem)
                player.helditem = -1
                player.maxhp = player.maxhp + 5

            elif(player.helditem != -1 and player.inventory[player.helditem] == "mpup"):
                # Held item is hpup
                curMsg = "+5 maxmp!"
                player.wt = player.wt - itemwt(player.inventory[player.helditem])
                player.inventory.pop(player.helditem)
                player.helditem = -1
                player.maxmp = player.maxmp + 5

            else:
                # Action couldn't be resolved
                curMsg = "???"

        else:
            # Action couldn't be resolved
            curMsg = "???"


def manacost(itemName):
    items = {
        "bsc cnfs": 3,
        "bsc fblt": 4,
        "bsc eblt": 5,
        "bsc lch": 3,
        "bsc tlpt": 4,
        "bsc heal": 5,
        "adv cnfs": 5,
        "adv fblt": 7,
        "adv eblt": 8,
        "adv lch": 6,
        "adv tlpt": 7,
        "adv heal": 9,
        "ult cnfs": 9,
        "ult fblt": 10,
        "ult eblt": 11,
        "ult lch": 9,
        "ult tlpt": 8,
        "ult heal": 12,
    }
    return items.get(itemName, 0)

# Given an item name, return the buy/sell price in gp
def itemprice(itemName):
    items = {
        "brknswd": [4, 2],
        "basicswd": [10, 4],
        "swd": [20, 8],
        "goodswd": [35, 15],
        "epicswd": [55, 20],
        "ultraswd": [70, 25],
        "brknbow": [4, 2],
        "basicbow": [10, 4],
        "bow": [20, 8],
        "goodbow": [35, 15],
        "epicbow": [55, 20],
        "ultrabow": [70, 25],
        "bsc cnfs": [14, 5],
        "bsc fblt": [12, 6],
        "bsc eblt": [13, 5],
        "bsc lch": [15, 7],
        "bsc heal": [17, 8],
        "bsc tlpt": [15, 7],
        "adv cnfs": [30, 10],
        "adv fblt": [25, 10],
        "adv eblt": [25, 11],
        "adv lch": [32, 15],
        "adv heal": [35, 17],
        "adv tlpt": [32, 15],
        "ult cnfs": [55, 20],
        "ult fblt": [50, 18],
        "ult eblt": [50, 20],
        "ult lch": [65, 30],
        "ult heal": [75, 37],
        "ult tlpt": [65, 30],
        "pants": [15, 8],
        "shirt": [15, 8],
        "food": [6, 3],
        "sml hpot": [10, 5],
        "sml mpot": [10, 5],
        "big hpot": [15, 7],
        "big mpot": [15, 7],
        "hpup": [50, 25],
        "mpup": [50, 25],
    }
    return items.get(itemName, [0, 0])

# Given an item name, return the range of damage it can deal
def itemdmg(itemName):
    items = {
        "brknswd": [2, 5],
        "basicswd": [3, 7],
        "swd": [5, 8],
        "goodswd": [7, 10],
        "epicswd": [10, 15],
        "ultraswd": [13, 20],
        "brknbow": [2, 4],
        "basicbow": [3, 5],
        "bow": [3, 7],
        "goodbow": [5, 8],
        "epicbow": [7, 9],
        "ultrabow": [8, 11],
        "bsc cnfs": [0, 1],
        "bsc fblt": [3, 6],
        "bsc eblt": [4, 6],
        "bsc lch": [1, 2],
        "adv cnfs": [1, 2],
        "adv fblt": [6, 8],
        "adv eblt": [6, 8],
        "adv lch": [2, 4],
        "ult cnfs": [1, 3],
        "ult fblt": [8, 10],
        "ult eblt": [9, 11],
        "ult lch": [3, 5],
    }
    return items.get(itemName, [1, 3])


# Given an item tile, spit out the name of the item
def itemname(itemTile):
    swords = {
        -1: "brknswd",
        0: "basicswd",
        1: "swd",
        2: "goodswd",
        3: "epicswd",
        4: "ultraswd",
    }
    bows = {
        -1: "brknbow",
        0: "basicbow",
        1: "bow",
        2: "goodbow",
        3: "epicbow",
        4: "ultrabow",
    }
    pots = {
        0: "sml hpot",
        1: "sml mpot",
        2: "big hpot",
        3: "big mpot",
    }
    spells = {
        0: "bsc cnfs",
        1: "bsc fblt",
        2: "bsc eblt",
        3: "bsc lch",
        4: "bsc tlpt",
        5: "bsc heal",
        6: "adv cnfs",
        7: "adv fblt",
        8: "adv eblt",
        9: "adv lch",
        10: "adv tlpt",
        11: "adv heal",
        12: "ult cnfs",
        13: "ult fblt",
        14: "ult eblt",
        15: "ult lch",
        16: "ult tlpt",
        17: "ult heal",
    }
    if(itemTile.tiledata[0] == 0):
        return swords.get(itemTile.tiledata[1], "??? swd")
    elif(itemTile.tiledata[0] == 1):
        return bows.get(itemTile.tiledata[1], "??? bow")
    elif(itemTile.tiledata[0] == 2):
        return pots.get(itemTile.tiledata[1], "??? pot")
    elif(itemTile.tiledata[0] == 3):
        return "key"
    elif(itemTile.tiledata[0] == 4):
        return "food"
    elif(itemTile.tiledata[0] == 5):

        return "pants"
    elif(itemTile.tiledata[0] == 6):
        return "shirt"
    elif(itemTile.tiledata[0] == 7):
        return spells.get(itemTile.tiledata[1], "??? tome")
    elif(itemTile.tiledata[0] == 8):
        return "hpup"
    elif(itemTile.tiledata[0] == 9):
        return "mpup"
    else:
        return "???"

# Given the name of an item, spit out the equivalent tile
def itemtile(itemName):
    tiles = {
        "brknswd": dungeonTile(7, 0, -1),
        "basicswd": dungeonTile(7, 0, 0),
        "swd": dungeonTile(7, 0, 1),
        "goodswd": dungeonTile(7, 0, 2),
        "epicswd": dungeonTile(7, 0, 3),
        "ultraswd": dungeonTile(7, 0, 4),
        "??? swd": dungeonTile(7, 0, -2),
        "brknbow": dungeonTile(7, 1, -1),
        "basicbow": dungeonTile(7, 1, 0),
        "bow": dungeonTile(7, 1, 1),
        "goodbow": dungeonTile(7, 1, 2),
        "epicbow": dungeonTile(7, 1, 3),
        "ultrabow": dungeonTile(7, 1, 4),
        "??? bow": dungeonTile(7, 1, -2),
        "sml hpot": dungeonTile(7, 2, 0),
        "sml mpot": dungeonTile(7, 2, 1),
        "big hpot": dungeonTile(7, 2, 2),
        "big mpot": dungeonTile(7, 2, 3),
        "??? pot": dungeonTile(7, 2, -2),
        "key": dungeonTile(7, 3),
        "food": dungeonTile(7, 4),
        "pants": dungeonTile(7, 5),
        "shirt": dungeonTile(7, 6),
        "bsc cnfs": dungeonTile(7, 7, 0),
        "bsc fblt": dungeonTile(7, 7, 1),
        "bsc eblt": dungeonTile(7, 7, 2),
        "bsc lch": dungeonTile(7, 7, 3),
        "bsc tlpt": dungeonTile(7, 7, 4),
        "bsc heal": dungeonTile(7, 7, 5),
        "adv cnfs": dungeonTile(7, 7, 6),
        "adv fblt": dungeonTile(7, 7, 7),
        "adv eblt": dungeonTile(7, 7, 8),
        "adv lch": dungeonTile(7, 7, 9),
        "adv tlpt": dungeonTile(7, 7, 10),
        "adv heal": dungeonTile(7, 7, 11),
        "ult cnfs": dungeonTile(7, 7, 12),
        "ult fblt": dungeonTile(7, 7, 13),
        "ult eblt": dungeonTile(7, 7, 14),
        "ult lch": dungeonTile(7, 7, 15),
        "ult tlpt": dungeonTile(7, 7, 16),
        "ult heal": dungeonTile(7, 7, 17),
        "??? tome": dungeonTile(7, 7, -2),
        "hpup": dungeonTile(7, 8),
        "mpup": dungeonTile(7, 9),
    }
    return tiles.get(itemName, dungeonTile(0, 0, 0))

# Given the name of an item, return its weight
def itemwt(itemName):
    switcher = {
        "brknswd": 2,
        "basicswd": 2,
        "swd": 2,
        "goodswd": 3,
        "epicswd": 3,
        "ultraswd": 3,
        "??? swd": 2,
        "brknbow": 2,
        "basicbow": 2,
        "bow": 2,
        "goodbow": 2,
        "epicbow": 3,
        "ultrabow": 3,
        "??? bow":2,
        "sml hpot": 1,
        "sml mpot": 1,
        "big hpot": 2,
        "big mpot": 2,
        "??? pot": 1,
        "key": 1,
        "food": 1,
        "pants": 3,
        "shirt": 3,
        "bsc cnfs": 1,
        "bsc fblt": 1,
        "bsc eblt": 1,
        "bsc lch": 1,
        "bsc tlpt": 1,
        "bsc heal": 1,
        "adv cnfs": 1,
        "adv fblt": 1,
        "adv eblt": 1,
        "adv lch": 1,
        "adv tlpt": 1,
        "adv heal": 1,
        "ult cnfs": 1,
        "ult fblt": 1,
        "ult eblt": 1,
        "ult lch": 1,
        "ult tlpt": 1,
        "ult heal": 1,
        "??? tome": 1,
        "hpup": 2,
        "mpup": 2,
    }
    return switcher.get(itemName, 0)


class dungeonRoom:
    def __init__(self):
        self.tiles = []
        self.shopInv = []
        self.hasShop = False
        # Each dungeon room is exactly 9*5=45 tiles
        for i in range(45):
            self.tiles.append(dungeonTile(0))

        # Generate walls
        for x in range(9):
            self.tiles[x] = dungeonTile(1)
            self.tiles[4*9+x] = dungeonTile(1)
        for y in range(5):
            self.tiles[y*9] = dungeonTile(1)
            self.tiles[y*9+8] = dungeonTile(1)

    # draws the tiles of the room ONLY
    def drawRoom(self):
        for x in range(9):
            for y in range(5):
                tile = self.tiles[y*9+x]
                if(tile.tiletype == 1):
                    # Block tile
                    thumby.display.blit(blockSpr, x*8, y*8, 8, 8, -1, 0, 0)
                elif(tile.tiletype == 2):
                    # Door tile
                    thumby.display.blit(doorSpr, x*8, y*8, 8, 8, -1, 0, 0)
                elif(tile.tiletype == 3):
                    # Stairs tile
                    thumby.display.blit(stairSpr, x*8, y*8, 8, 8, -1, 0, 0)
                elif(tile.tiletype == 4):
                    # Sign tile
                    thumby.display.blit(signSpr, x*8, y*8, 8, 8, -1, 0, 0)
                elif(tile.tiletype == 5):
                    # The player
                    thumby.display.drawText("@", (x*8)+1, (y*8)+1, 1)
                elif(tile.tiletype == 6):
                    # Chest tile
                    thumby.display.blit(chestSpr, x*8, y*8, 8, 8, -1, 0, 0)
                elif(tile.tiletype == 7):
                    # item tile
                    thumby.display.blit(itemSprites[int(tile.tiledata[0])], x*8, y*8, 8, 8, -1, 0, 0)
                elif(tile.tiletype == 8):
                    # Monster tile
                    if(ticks_ms() % 1000 > 500):
                        thumby.display.blit(monsterSprites[int(tile.tiledata[0])], x*8, y*8, 8, 8, 0, 0, 0)
                    else:
                        thumby.display.blit(monsterSprites[int(tile.tiledata[0])], x*8, y*8-1, 8, 8, 0, 0, 0)
        if(self.hasShop):
            thumby.display.blit(shopSpr, 16, 8, 16, 16, -1, 0, 0)

    def getTile(self, tx, ty):
        return self.tiles[ty*9+tx]


class playerobj:
    def __init__(self):
        self.hp = 20
        self.maxhp = 20
        self.armor = 0
        self.mp = 15
        self.maxmp = 15
        # self.name = newname
        self.tilex = 4
        self.tiley = 2
        self.wt = itemwt("basicswd") + itemwt("pants") + itemwt("sml hpot") + itemwt("sml hpot") + itemwt("bsc cnfs")
        self.maxwt = 30
        self.inventory = ["basicswd", "pants", "sml hpot", "sml hpot", "bsc cnfs"]
        self.helditem = -1
        self.shirtitem = -1
        self.pantsitem = -1
        self.facing = 0 # 0 up, 1 right, 2 down, 3 left.
        self.gp = 0


random_seed()

def getRandomFreePosition(room):
    px = randint(1, 7)
    py = randint(1, 3)

    # Check that tile is empty and there are no doors this could block
    while(room.getTile(px, py).tiletype != 0 or ((px==4 and py==1) or (px==4 and py==3) or (px==1 and py==2) or (px==7 and py==2))):
        px = randint(1, 7)
        py = randint(1, 3)
    return [px, py]

floorNo = 1
roomno = 0
maxrooms = 12
exitSpawned = False

t1Items = ("brknswd", "basicswd", "brknbow", "basicbow", "sml hpot", "sml mpot", "food", "shirt", "pants", "bsc cnfs", "bsc fblt", "bsc eblt", "bsc tlpt", "bsc lch", "bsc heal")
t2Items = ("swd", "bow", "goodswd", "goodbow", "big hpot", "big mpot", "hpup", "mpup", "adv cnfs", "adv fblt", "adv eblt", "adv tlpt", "adv lch", "adv heal")
t3Items = ("epicswd", "ultraswd", "epicbow", "ultrabow", "ult cnfs", "ult fblt", "ult eblt", "ult tlpt", "ult lch", "ult heal")

# Procedural generation function
def generateRoom(room):
    # Each wall has a 1/(chance+1) chance of having a door to another room
    global roomno
    global maxrooms
    global exitSpawned
    if(roomno < maxrooms):
        roomno = roomno + 1
        # Generate up to 3 more rooms
        for k in range(3):
            if(randint(0, k) == 0):
                if(randint(0, 1) == 0):
                    if(randint(0, 1) == 0 and room.getTile(4, 0).tiletype != 2):
                        # Put door on north wall
                        room.getTile(4, 0).tiletype = 2
                        room.getTile(4, 1).tiledata.clear()
                        room.getTile(4, 1).tiletype = 0
                        room.getTile(4, 0).tiledata.append(dungeonRoom())
                        room.getTile(4, 0).tiledata.append(4)
                        room.getTile(4, 0).tiledata.append(3)
                        room.getTile(4, 0).tiledata[0].getTile(4, 4).tiletype = 2
                        room.getTile(4, 0).tiledata[0].getTile(4, 3).tiledata.clear()
                        room.getTile(4, 0).tiledata[0].getTile(4, 3).tiletype = 0
                        room.getTile(4, 0).tiledata[0].getTile(4, 4).tiledata.append(room)
                        room.getTile(4, 0).tiledata[0].getTile(4, 4).tiledata.append(4)
                        room.getTile(4, 0).tiledata[0].getTile(4, 4).tiledata.append(1)
                        generateRoom(room.getTile(4, 0).tiledata[0])
                    elif(room.getTile(4, 4).tiletype != 2):
                        # Put door on south wall
                        room.getTile(4, 4).tiletype = 2
                        room.getTile(4, 3).tiledata.clear()
                        room.getTile(4, 3).tiletype = 0
                        room.getTile(4, 4).tiledata.append(dungeonRoom())
                        room.getTile(4, 4).tiledata.append(4)
                        room.getTile(4, 4).tiledata.append(1)
                        room.getTile(4, 4).tiledata[0].getTile(4, 0).tiletype = 2
                        room.getTile(4, 4).tiledata[0].getTile(4, 1).tiledata.clear()
                        room.getTile(4, 4).tiledata[0].getTile(4, 1).tiletype = 0
                        room.getTile(4, 4).tiledata[0].getTile(4, 0).tiledata.append(room)
                        room.getTile(4, 4).tiledata[0].getTile(4, 0).tiledata.append(4)
                        room.getTile(4, 4).tiledata[0].getTile(4, 0).tiledata.append(3)
                        generateRoom(room.getTile(4, 4).tiledata[0])
                else:
                    if(randint(0, 1) == 0 and room.getTile(0, 2).tiletype != 2):
                        # Put door on west wall
                        room.getTile(0, 2).tiletype = 2
                        room.getTile(1, 2).tiledata.clear()
                        room.getTile(1, 2).tiletype = 0
                        room.getTile(0, 2).tiledata.append(dungeonRoom())
                        room.getTile(0, 2).tiledata.append(7)
                        room.getTile(0, 2).tiledata.append(2)
                        room.getTile(0, 2).tiledata[0].getTile(8, 2).tiletype = 2
                        room.getTile(0, 2).tiledata[0].getTile(7, 2).tiledata.clear()
                        room.getTile(0, 2).tiledata[0].getTile(7, 2).tiletype = 0
                        room.getTile(0, 2).tiledata[0].getTile(8, 2).tiledata.append(room)
                        room.getTile(0, 2).tiledata[0].getTile(8, 2).tiledata.append(1)
                        room.getTile(0, 2).tiledata[0].getTile(8, 2).tiledata.append(2)
                        generateRoom(room.getTile(0, 2).tiledata[0])
                    elif(room.getTile(8, 2).tiletype != 2):
                        # Put door on east wall
                        room.getTile(8, 2).tiletype = 2
                        room.getTile(7, 2).tiledata.clear()
                        room.getTile(7, 2).tiletype = 0
                        room.getTile(8, 2).tiledata.append(dungeonRoom())
                        room.getTile(8, 2).tiledata.append(1)
                        room.getTile(8, 2).tiledata.append(2)
                        room.getTile(8, 2).tiledata[0].getTile(0, 2).tiletype = 2
                        room.getTile(8, 2).tiledata[0].getTile(1, 2).tiledata.clear()
                        room.getTile(8, 2).tiledata[0].getTile(1, 2).tiletype = 0
                        room.getTile(8, 2).tiledata[0].getTile(0, 2).tiledata.append(room)
                        room.getTile(8, 2).tiledata[0].getTile(0, 2).tiledata.append(7)
                        room.getTile(8, 2).tiledata[0].getTile(0, 2).tiledata.append(2)
                        generateRoom(room.getTile(8, 2).tiledata[0])

        #Each room has a 10% chance of having a chest in it
        if(randint(0, 9) == 0):
            px = randint(2,6)
            py = randint(1,3)
            while(room.getTile(px, py).tiletype != 0):
                px = randint(2,6)
                py = randint(1,3)
            room.getTile(px, py).tiletype = 6

        # Each room has (roomno) / maxrooms chance to have the exit in it
        if(randint(roomno, maxrooms) == roomno and not exitSpawned):
            pos = getRandomFreePosition(room)
            room.getTile(pos[0], pos[1]).tiletype = 3
            #print("Spawned exit")
            exitSpawned = True


        # Each room has a 10% chance of having a shopkeep
        if(randint(0, 9) == 0):
            room.hasShop = True
            room.getTile(2, 1).tiletype = 9
            room.getTile(3, 1).tiletype = 9
            room.getTile(2, 2).tiletype = 9
            room.getTile(3, 2).tiletype = 9
            for i in range(randint(2, 4)):
                room.shopInv.append(t1Items[randint(0, len(t1Items)-1)])
            for i in range(randint(1, 3)):
                room.shopInv.append(t2Items[randint(0, len(t2Items)-1)])
            for i in range(randint(0, 2)):
                room.shopInv.append(t3Items[randint(0, len(t3Items)-1)])

        # Each room has a 10% chance of having a sign
        if(randint(0, 9) == 0):
            if room.getTile(4, 2).tiletype == 0:
                room.getTile(4, 2).tiletype = 4
                room.getTile(4, 2).tiledata = signMessages[randint(0, len(signMessages) - 1)]

        if(randint(0, 2) == 0):
        # Each room has a 33% chance of having a broken or basic-tier piece of loot in it
            pos = getRandomFreePosition(room)
            item = dungeonTile(0)
            sel = randint(0, 5)
            if(sel == 0):
                # Put a sword there
                if(randint(0, 1) == 0):
                    item = itemtile("basicswd")
                else:
                    item = itemtile("brknswd")
            elif(sel == 1):
                # Put a bow there
                if(randint(0, 1) == 0):
                    item = itemtile("basicbow")
                else:
                    item = itemtile("brknbow")
            elif(sel == 2):
                # Put food there
                item = itemtile("food")
            elif(sel == 3):
                # Put a spell there
                spells = {
                    0: "bsc fblt",
                    1: "bsc eblt",
                    2: "bsc cnfs",
                    3: "bsc lch",
                    4: "bsc tlpt",
                    5: "bsc heal",
                }
                item = itemtile(spells.get(randint(0, 5), "??? tome"))
            elif(sel == 4):
                # Put a potion there
                if(randint(0, 1) == 0):
                    item = itemtile("sml hpot")
                else:
                    item = itemtile("sml mpot")
            elif(sel == 5):
                # Put some clothing there
                if(randint(0, 1) == 0):
                    item = itemtile("shirt")
                else:
                    item = itemtile("pants")
            room.getTile(pos[0], pos[1]).tiletype = item.tiletype
            room.getTile(pos[0], pos[1]).tiledata = item.tiledata.copy()

        # Each room has a 5% chance of having a normal or good-tier peice of loot in it
        if(randint(0, 19) == 0):
            pos = getRandomFreePosition(room)
            item = dungeonTile(0)
            sel = randint(0, 4)
            if(sel == 0):
                # Put a sword there
                if(randint(0, 1) == 0):
                    item = itemtile("goodswd")
                else:
                    item = itemtile("swd")
            elif(sel == 1):
                # Put a bow there
                if(randint(0, 1) == 0):
                    item = itemtile("goodbow")
                else:
                    item = itemtile("bow")
            elif(sel == 2):
                # Put a spell there
                spells = {
                    0: "adv fblt",
                    1: "adv eblt",
                    2: "adv cnfs",
                    3: "adv lch",
                    4: "adv tlpt",
                    5: "adv heal",
                }
                item = itemtile(spells.get(randint(0, 5), "??? tome"))
            elif(sel == 3):
                # Put a potion there
                if(randint(0, 1) == 0):
                    item = itemtile("big hpot")
                else:
                    item = itemtile("big mpot")
            elif(sel == 4):
                # put a hpup or mpup there
                if(randint(0, 1) == 0):
                    item = itemtile("hpup")
                else:
                    item = itemtile("mpup")
            room.getTile(pos[0], pos[1]).tiletype = item.tiletype
            room.getTile(pos[0], pos[1]).tiledata = item.tiledata.copy()

        if(randint(0, 99) == 0):
        # Each room has a 1% chance of having an epic or ultra-tier piece of loot in it
            pos = getRandomFreePosition(room)
            item = dungeonTile(0)
            sel = randint(0, 2)
            if(sel == 0):
                # Put a sword there
                if(randint(0, 1) == 0):
                    item = itemtile("ultraswd")
                else:
                    item = itemtile("epicswd")
            elif(sel == 1):
                # Put a bow there
                if(randint(0, 1) == 0):
                    item = itemtile("ultrabow")
                else:
                    item = itemtile("epicbow")
            elif(sel == 2):
                # Put a spell there
                spells = {
                    0: "ult fblt",
                    1: "ult eblt",
                    2: "ult cnfs",
                    3: "ult lch",
                    4: "ult tlpt",
                    5: "ult heal",
                }
                item = itemtile(spells.get(randint(0, 5), "??? tome"))
            room.getTile(pos[0], pos[1]).tiletype = item.tiletype
            room.getTile(pos[0], pos[1]).tiledata = item.tiledata.copy()

        # Each room has a 50% chance of having a monster in it
        if(randint(0, 1) == 0):
            pos = getRandomFreePosition(room)
            room.getTile(pos[0], pos[1]).tiletype = 8
            room.getTile(pos[0], pos[1]).tiledata.append(randint(0, len(monsterSprites) - 1))
            room.getTile(pos[0], pos[1]).tiledata.append(randint(10, 15) + 2 * floorNo)
            room.getTile(pos[0], pos[1]).tiledata.append(1)
        # Each room has a 20% chance of having another monster in it
        if(randint(0, 4) == 0):
            pos = getRandomFreePosition(room)
            room.getTile(pos[0], pos[1]).tiletype = 8
            room.getTile(pos[0], pos[1]).tiledata.append(randint(0, len(monsterSprites) - 1))
            room.getTile(pos[0], pos[1]).tiledata.append(randint(10, 15) + 2 * floorNo)
            room.getTile(pos[0], pos[1]).tiledata.append(1)
turnCounter = 0

def ensureExit(room):
    global exitSpawned
    if not exitSpawned:
        pos = getRandomFreePosition(room)
        room.getTile(pos[0], pos[1]).tiletype = 3
        exitSpawned = True


# Draw the entire gamestate, including Heads-Up-Display (HUD)
def drawGame():
    global display
    global curMsg
    thumby.display.fill(0)
    currentRoom.drawRoom()

    hpHUDWidth=(len(str(player.hp))+1)*fontWidth
    thumby.display.drawRectangle(1, 1, hpHUDWidth, 8, 1)
    thumby.display.drawFilledRectangle(0, 0, hpHUDWidth, 8, 0)
    thumby.display.drawText(str(player.hp), 6, 0, 1)
    thumby.display.blit(hpSpr,0,0,5,8,-1,0,0)

    mpHUDWidth=(len(str(player.mp))+1)*fontWidth
    thumby.display.drawRectangle(71-mpHUDWidth, 1, 32, 8, 1)
    thumby.display.drawFilledRectangle(72-mpHUDWidth, 0, 32, 8, 0)
    thumby.display.drawText(str(player.mp), 73-mpHUDWidth, 0, 1)
    thumby.display.blit(mpSpr,67,0,5,8,-1,0,0)

    floorHUD=str(floorNo)+"F"
    floorHUDWidth=len(floorHUD)*fontWidth
    thumby.display.drawRectangle(71-floorHUDWidth, 31, 32, 9, 1)
    thumby.display.drawFilledRectangle(72-floorHUDWidth, 32, 32, 8, 0)
    thumby.display.drawText(floorHUD, 73-floorHUDWidth, 33, 1)

    if(curMsg == ""):
        # Default 'Msg' will show the Player's gold pieces
        curMsg = goldChr+str(player.gp)

    curMsgWidth=len(curMsg)*fontWidth
    thumby.display.drawRectangle(0, 31, curMsgWidth+1, 9, 1)
    thumby.display.drawFilledRectangle(0, 32, curMsgWidth, 8, 0)
    thumby.display.drawText(curMsg, 0, 33, 1)

    thumby.display.update()


def updateMonsters():
    for y in range(5):
        for x in range(9):
            if(currentRoom.getTile(x, y).tiletype == 8):
                # Monster tile, update it
                if(currentRoom.getTile(x, y).tiledata[2] == 0):

                    # Monster is not stunned
                    dx = player.tilex - x
                    dy = player.tiley - y
                    if((dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)):
                        global lastHit
                        # Monster is within range, attack the player
                        # Make a random attack damage
                        dmg = randint(1, 5) + randint(0, floorNo)
                        # Handle armor
                        if(player.shirtitem != -1):
                            dmg = dmg - 2
                        if(player.pantsitem != -1):
                            dmg = dmg - 1
                        dmg = 1 if dmg < 1 else dmg
                        player.hp = player.hp - dmg
                        lastHit = {0: "blob", 1: "spirit", 2: "arachnid", 3: "skeleton", 4: "wizard", 5: "tempest"}.get(currentRoom.getTile(x, y).tiledata[0], "???")
                    elif(abs(dx) > abs(dy)):
                        if(dx < 0):
                            # Move monster left if we can
                            if(currentRoom.getTile(x-1, y).tiletype == 0):
                                currentRoom.getTile(x-1, y).tiletype = 8
                                currentRoom.getTile(x-1, y).tiledata = currentRoom.getTile(x, y).tiledata.copy()
                                currentRoom.getTile(x-1, y).tiledata[2] = 1
                                currentRoom.getTile(x, y).tiledata.clear()
                                currentRoom.getTile(x, y).tiletype = 0
                        else:
                            # Move monster right if we can
                            if(currentRoom.getTile(x+1, y).tiletype == 0):
                                currentRoom.getTile(x+1, y).tiletype = 8
                                currentRoom.getTile(x+1, y).tiledata = currentRoom.getTile(x, y).tiledata.copy()
                                currentRoom.getTile(x+1, y).tiledata[2] = 1
                                currentRoom.getTile(x, y).tiledata.clear()
                                currentRoom.getTile(x, y).tiletype = 0
                    else:
                        if(dy < 0):
                            # Move monster up if we can
                            if(currentRoom.getTile(x, y-1).tiletype == 0):
                                currentRoom.getTile(x, y-1).tiletype = 8
                                currentRoom.getTile(x, y-1).tiledata = currentRoom.getTile(x, y).tiledata.copy()
                                currentRoom.getTile(x, y-1).tiledata[2] = 1
                                currentRoom.getTile(x, y).tiledata.clear()
                                currentRoom.getTile(x, y).tiletype = 0
                        else:
                            # Move monster down if we can
                            if(currentRoom.getTile(x, y+1).tiletype == 0):
                                currentRoom.getTile(x, y+1).tiletype = 8
                                currentRoom.getTile(x, y+1).tiledata = currentRoom.getTile(x, y).tiledata.copy()
                                currentRoom.getTile(x, y+1).tiledata[2] = 1
                                currentRoom.getTile(x, y).tiledata.clear()
                                currentRoom.getTile(x, y).tiletype = 0
                else:
                    # Monster is stunned, decrease the timer
                    currentRoom.getTile(x, y).tiledata[2] = currentRoom.getTile(x, y).tiledata[2] - 1


# Draw title screen
thumby.display.fill(0)
thumby.display.drawText("Thumgeon", 12, 0, 1)
thumby.display.drawText("@", 33, 17, 1)
while(not thumby.actionJustPressed()):
    color = ticks_ms() % 1000 < 500
    thumby.display.drawFilledRectangle(0, 31, 72, 9, 1-color)
    thumby.display.drawText("Press A/B", 9, 32, color)
    thumby.display.update()


# Main game loop
while(True):
    turnCounter = 0
    roomno = 0
    floorNo = 1
    exitSpawned = False
    # Make the starting room
    currentRoom = dungeonRoom()
    currentRoom.tiles[2*9+2] = dungeonTile(4)
    currentRoom.tiles[2*9+2].tiledata = bytes("Welcome!\n\nA to act\nB for inv\n - have fun!", 'ascii')
    generateRoom(currentRoom)
    ensureExit(currentRoom)

    # Make the player
    player = playerobj()

    while(player.hp > 0):

        # Put the player in their correct location
        currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
        drawGame()
        # Get and handle input
        if(getcharinputNew() != ' '):

            # Handle d-pad
            if(swUstate == 1):
                player.facing = 0
                if(currentRoom.getTile(player.tilex, player.tiley-1).tiletype == 0):
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                    player.tiley = player.tiley-1
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
                curMsg = ""
                updateMonsters()
                if(turnCounter % 4 == 0):
                    turnCounter = 0
                    addmp(1)
                turnCounter = turnCounter + 1
            elif(swDstate == 1):
                player.facing = 2
                if(currentRoom.getTile(player.tilex, player.tiley+1).tiletype == 0):
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                    player.tiley = player.tiley+1
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
                curMsg = ""
                updateMonsters()
                if(turnCounter % 4 == 0):
                    turnCounter = 0
                    addmp(1)
                turnCounter = turnCounter + 1
            elif(swLstate == 1):
                player.facing = 3
                if(currentRoom.getTile(player.tilex-1, player.tiley).tiletype == 0):
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                    player.tilex = player.tilex-1
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
                curMsg = ""
                updateMonsters()
                if(turnCounter % 4 == 0):
                    turnCounter = 0
                    addmp(1)
                turnCounter = turnCounter + 1
            elif(swRstate == 1):
                player.facing = 1
                if(currentRoom.getTile(player.tilex+1, player.tiley).tiletype == 0):
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 0
                    player.tilex = player.tilex+1
                    currentRoom.getTile(player.tilex, player.tiley).tiletype = 5
                curMsg = ""
                updateMonsters()
                if(turnCounter % 4 == 0):
                    turnCounter = 0
                    addmp(1)
                turnCounter = turnCounter + 1

            # Handle action 'A'-button
            elif(swBstate == 1):
                curMsg = "act on?"
                drawGame()
                while(getcharinputNew() == ' '):
                    pass
                if(swUstate == 1):
                    player.facing = 0
                    currentRoom.getTile(player.tilex, player.tiley-1).actOn()
                    updateMonsters()
                    if(turnCounter % 4 == 0):
                        turnCounter = 0
                        addmp(1)
                    turnCounter = turnCounter + 1
                elif(swDstate == 1):
                    player.facing = 2
                    currentRoom.getTile(player.tilex, player.tiley+1).actOn()
                    updateMonsters()
                    if(turnCounter % 4 == 0):
                        turnCounter = 0
                        addmp(1)
                    turnCounter = turnCounter + 1
                elif(swLstate == 1):
                    player.facing = 3
                    currentRoom.getTile(player.tilex-1, player.tiley).actOn()
                    updateMonsters()
                    if(turnCounter % 4 == 0):
                        turnCounter = 0
                        addmp(1)
                    turnCounter = turnCounter + 1
                elif(swRstate == 1):
                    player.facing = 1
                    currentRoom.getTile(player.tilex+1, player.tiley).actOn()
                    updateMonsters()
                    if(turnCounter % 4 == 0):
                        turnCounter = 0
                        addmp(1)
                    turnCounter = turnCounter + 1
                elif(swBstate == 1):
                    curMsg = ""

            # Handle inventory 'B'-button
            elif(swAstate == 1):
                selpos = 0
                actpos = 1
                while(getcharinputNew() != '1'):

                    # Menu navigation
                    if(swUstate == 1):
                        selpos = selpos-1
                        while(swUstate == 1):
                            getcharinputNew()
                    elif(swDstate == 1):
                        selpos = selpos+1
                        while(swDstate == 1):
                            getcharinputNew()
                    if(swLstate == 1):
                        actpos = 0
                        while(swLstate == 1):
                            getcharinputNew()
                    elif(swRstate == 1):
                        actpos = 1
                        while(swRstate == 1):
                            getcharinputNew()

                    # Handle item selection
                    if(swBstate == 1):

                        if(actpos == 1):
                            # Equip selected item
                            if(player.inventory[selpos] == "shirt"):
                                player.shirtitem = selpos
                            elif(player.inventory[selpos] == "pants"):
                                player.pantsitem = selpos
                            else:
                                player.helditem = selpos
                            curMsg = "eqp'd."
                            updateMonsters()
                            if(turnCounter % 4 == 0):
                                turnCounter = 0
                                addmp(1)
                            turnCounter = turnCounter + 1
                            break

                        elif(actpos == 0 and len(player.inventory) != 0):
                            # Drop selected item
                            curMsg = "where?"
                            drawGame()
                            while(getcharinputNew() == ' '):
                                pass
                            tile = itemtile(player.inventory[selpos])

                            # Try to drop the item where the player selected, or explain that something is in the way
                            if(swUstate == 1):
                                if(currentRoom.getTile(player.tilex, player.tiley-1).tiletype == 0):
                                    currentRoom.getTile(player.tilex, player.tiley-1).tiletype = tile.tiletype
                                    currentRoom.getTile(player.tilex, player.tiley-1).tiledata = tile.tiledata
                                    player.wt = player.wt - itemwt(player.inventory[selpos])
                                    player.inventory.pop(selpos)
                                    curMsg = "dropped"
                                else:
                                    curMsg = "can't!"
                            elif(swDstate == 1):
                                if(currentRoom.getTile(player.tilex, player.tiley+1).tiletype == 0):
                                    currentRoom.getTile(player.tilex, player.tiley+1).tiletype = tile.tiletype
                                    currentRoom.getTile(player.tilex, player.tiley+1).tiledata = tile.tiledata
                                    player.wt = player.wt - itemwt(player.inventory[selpos])
                                    player.inventory.pop(selpos)
                                    curMsg = "dropped"
                                else:
                                    curMsg = "can't!"
                            elif(swLstate == 1):
                                if(currentRoom.getTile(player.tilex-1, player.tiley).tiletype == 0):
                                    currentRoom.getTile(player.tilex-1, player.tiley).tiletype = tile.tiletype
                                    currentRoom.getTile(player.tilex-1, player.tiley).tiledata = tile.tiledata
                                    player.wt = player.wt - itemwt(player.inventory[selpos])
                                    player.inventory.pop(selpos)
                                    curMsg = "dropped"
                                else:
                                    curMsg = "can't!"
                            elif(swRstate == 1):
                                if(currentRoom.getTile(player.tilex+1, player.tiley).tiletype == 0):
                                    currentRoom.getTile(player.tilex+1, player.tiley).tiletype = tile.tiletype
                                    currentRoom.getTile(player.tilex+1, player.tiley).tiledata = tile.tiledata
                                    player.wt = player.wt - itemwt(player.inventory[selpos])
                                    player.inventory.pop(selpos)
                                    curMsg = "dropped"
                                else:
                                    curMsg = "can't!"
                            # Make sure the player isn't holding it anymore
                            if(curMsg == "dropped"):
                                if(player.helditem == selpos):
                                    player.helditem = -1
                                if(player.shirtitem == selpos):
                                    player.shirtitem = -1
                                if(player.pantsitem == selpos):
                                    player.pantsitem = -1
                            updateMonsters()
                            if(turnCounter % 4 == 0):
                                turnCounter = 0
                                addmp(1)
                            turnCounter = turnCounter + 1
                            break


                    # Make sure our selection is actually valid
                    if(selpos < 0):
                        selpos = 0
                    if(selpos >= len(player.inventory)):
                        selpos = len(player.inventory)-1

                    # Only 3 lines to use for showing items
                    l1 = ""
                    l2 = ""
                    l3 = ""
                    if(selpos < len(player.inventory) and len(player.inventory) > 0):
                        l1 = player.inventory[selpos]
                        l1 += '<'
                    if(selpos+1 < len(player.inventory)):
                        l2 = player.inventory[selpos+1]
                    if(selpos+2 < len(player.inventory)):
                        l3 = player.inventory[selpos+2]

                    # Draw everything
                    thumby.display.fill(0)
                    wtHUD=str(player.wt)+"/"+str(player.maxwt)+"wt"
                    thumby.display.drawText(wtHUD, 73-(len(wtHUD)*fontWidth), 0, 1)
                    # Highlight the equipped item(s)
                    if(player.helditem == selpos or player.pantsitem == selpos or player.shirtitem == selpos):
                        thumby.display.drawFilledRectangle(0, 8, len(l1)*fontWidth, 8, 1)
                        thumby.display.drawText(l1, 0, 8, 0)
                    else:
                        thumby.display.drawText(l1, 0, 8, 1)
                    if(player.helditem == selpos+1 or player.pantsitem == selpos+1 or player.shirtitem == selpos+1):
                        thumby.display.drawFilledRectangle(0, 16, len(l2)*fontWidth, 8, 1)
                        thumby.display.drawText(l2, 0, 16, 0)
                    else:
                        thumby.display.drawText(l2, 0, 16, 1)
                    if(player.helditem == selpos+2 or player.pantsitem == selpos+2 or player.shirtitem == selpos+2):
                        thumby.display.drawFilledRectangle(0, 24, len(l3)*fontWidth, 8, 1)
                        thumby.display.drawText(l3, 0, 24, 0)
                    else:
                        thumby.display.drawText(l3, 0, 24, 1)
                    if(actpos == 0):
                        thumby.display.drawFilledRectangle(0, 32, 32, 8, 1)
                        thumby.display.drawText("drop", 0, 32, 0)
                        thumby.display.drawText("eqp", 48, 32, 1)
                    elif(actpos == 1):
                        thumby.display.drawText("drop", 0, 32, 1)
                        thumby.display.drawFilledRectangle(48, 32, 24, 8, 1)
                        thumby.display.drawText("eqp", 48, 32, 0)
                    thumby.display.update()
            else:
                # Clear the current message
                curMsg = ""
            drawGame()


    thumby.display.fill(0)
    thumby.display.drawText("You died!", 0, 0, 1)
    thumby.display.drawText("Killed by", 0, 8, 1)
    thumby.display.drawText("dungeon", 0, 16, 1)
    thumby.display.drawText(lastHit, 0, 24, 1)
    thumby.display.drawText("floor "+str(floorNo), 0, 32, 1)
    thumby.display.update()

    while(not thumby.actionPressed()):
        pass

    select = 0
    thumby.display.fill(0)
    thumby.display.drawText("Restart?", 0, 8, 1)
    thumby.actionJustPressed() # Debounce
    while(not thumby.actionJustPressed()):
        thumby.display.drawFilledRectangle(0, 16, 24, 8, 1-select)
        thumby.display.drawText("yes", 0, 16, select)
        thumby.display.drawFilledRectangle(40, 16, 16, 8, select)
        thumby.display.drawText("no", 40, 16, 1-select)
        thumby.display.update()
        if(thumby.buttonL.pressed()):
            select = 0
        if(thumby.buttonR.pressed()):
            select = 1

    # Free memory
    del currentRoom
    del player
    curMsg = ""
    gc_collect()

    if(select == 1):
        thumby.reset() # Exit game to main menu
    # Else: Restart game loop
