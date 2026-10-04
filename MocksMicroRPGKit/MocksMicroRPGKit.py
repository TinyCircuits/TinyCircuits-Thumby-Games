import thumby
import random
import machine

thumby.display.setFPS(15)

# Load saved Tracker value on startup
hp = 0
try:
    f = open("track.txt", "r")
    hp = int(f.read())
    f.close()
except:
    hp = 0

state = -1
menu = ["Dice", "Oracle", "Encounter", "NPC", "Loot", "Prompt", "Twists", "Dungeon", "Weather", "Tracker", "Cards", "Exit"]
sel = 0

cards_menu = ["Standard", "Tarot", "UNO", "Back"]
c_sel = 0

res = ""
res2 = ""
jokers_on = False

# Core Data Arrays
dice = [4, 6, 8, 10, 12, 20, 100]
d_idx = 1
oracle = ["Yes, and", "Yes", "Yes, but", "No, but", "No", "No, and"]
enc = ["Conflict", "Discovery", "Obstacle", "Hazard", "NPC", "Advantage"]
npc = ["Hostile", "Wary", "Neutral", "Friendly", "Helpful"]
loot = ["Consumable", "Wealth", "Clue", "Trinket", "Gear"]
act = ["Seek", "Escort", "Defend", "Avenge", "Hunt", "Steal", "Rescue", "Explore", "Destroy", "Capture", "Protect", "Escape", "Survive", "Uncover", "Build", "Guide", "Betray", "Command", "Conceal", "Restore"]
thm = ["Artifact", "Monster", "Wealth", "Secret", "Ally", "Enemy", "Magic", "Tech", "Nature", "Undead", "Ruin", "Power", "Knowledge", "Love", "Fear", "Justice", "Chaos", "Order", "Death", "Spirit"]

# New Data Arrays
twist = ["Ally Betrays", "Lose Item", "New Threat", "Time Limit", "Weather Chg", "Trap Sprung"]
dung = ["Corridor", "Chamber", "Stairs Up", "Stairs Down", "Dead End", "Locked Door"]
weath = ["Clear", "Heavy Rain", "Thick Fog", "Bitter Cold", "Eerie Quiet", "Howling Wind"]

# Card Data Arrays
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
suits = ['Hearts', 'Spades', 'Clubs', 'Diamonds']
t_maj = ["Fool", "Magician", "Priestess", "Empress", "Emperor", "Hierophant", "Lovers", "Chariot", "Strength", "Hermit", "Wheel", "Justice", "Hanged Man", "Death", "Temperance", "Devil", "Tower", "Star", "Moon", "Sun", "Judgement", "World"]
t_suit = ["Wands", "Cups", "Swords", "Coins"]
t_rnk = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Page", "Knight", "Queen", "King"]
u_col = ["Red", "Blu", "Grn", "Yel"]
u_val = ["0","1","2","3","4","5","6","7","8","9","Skip","Rev","+2"]

def draw_bold(text, x, y):
    thumby.display.drawText(text, x, y, 1)
    thumby.display.drawText(text, x, y+1, 1)

while True:
    thumby.display.fill(0)
    
    if state == -1:
        draw_bold("Mock's Micro", 0, 8)
        draw_bold("RPG Kit", 15, 18)
        thumby.display.drawText("Press A", 15, 32, 1)
        if thumby.buttonA.justPressed():
            state = 0
            
    elif state == 0:
        thumby.display.drawText("Menu:", 0, 0, 1)
        start = max(0, min(sel - 1, len(menu) - 4))
        for i in range(4):
            if start + i < len(menu):
                item = menu[start + i]
                prefix = ">" if start + i == sel else " "
                thumby.display.drawText(prefix + item, 0, 8 + (i * 8), 1)
                
        if thumby.buttonD.justPressed():
            sel = (sel + 1) % len(menu)
        if thumby.buttonU.justPressed():
            sel = (sel - 1) % len(menu)
        if thumby.buttonA.justPressed():
            if sel == len(menu) - 1:
                machine.reset()
            else:
                # States 1 to 11 are directly matched to menu selections
                state = sel + 1
                res = ""
                res2 = ""
                
    elif state == 1:
        thumby.display.drawText("d" + str(dice[d_idx]) + ": " + str(res), 0, 0, 1)
        thumby.display.drawText("U/D: Change", 0, 16, 1)
        thumby.display.drawText("A:1dX B:Back", 0, 32, 1) 
        if thumby.buttonU.justPressed(): d_idx = (d_idx + 1) % 7
        if thumby.buttonD.justPressed(): d_idx = (d_idx - 1) % 7
        if thumby.buttonA.justPressed(): res = random.randint(1, dice[d_idx])
        if thumby.buttonB.justPressed(): state = 0
            
    elif state == 2:
        thumby.display.drawText("Oracle", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1) 
        thumby.display.drawText("A:Ask B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): res = random.choice(oracle)
        if thumby.buttonB.justPressed(): state = 0
            
    elif state == 3:
        thumby.display.drawText("Encounter", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): res = random.choice(enc)
        if thumby.buttonB.justPressed(): state = 0
        
    elif state == 4:
        thumby.display.drawText("NPC React", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): res = random.choice(npc)
        if thumby.buttonB.justPressed(): state = 0
        
    elif state == 5:
        thumby.display.drawText("Loot", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): res = random.choice(loot)
        if thumby.buttonB.justPressed(): state = 0
        
    elif state == 6:
        thumby.display.drawText("Prompt", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 10, 1)
        thumby.display.drawText(str(res2), 0, 18, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): 
            res = random.choice(act)
            res2 = random.choice(thm)
        if thumby.buttonB.justPressed(): state = 0
            
    elif state == 7:
        thumby.display.drawText("Plot Twist", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): res = random.choice(twist)
        if thumby.buttonB.justPressed(): state = 0
            
    elif state == 8:
        thumby.display.drawText("Dungeon", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): res = random.choice(dung)
        if thumby.buttonB.justPressed(): state = 0

    elif state == 9:
        thumby.display.drawText("Weather", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        if thumby.buttonA.justPressed(): res = random.choice(weath)
        if thumby.buttonB.justPressed(): state = 0

    elif state == 10:
        thumby.display.drawText("Tracker", 0, 0, 1)
        thumby.display.drawText("Val: " + str(hp), 0, 10, 1)
        
        # Flashes "Saved!" when you save the number
        if res == "Saved!":
            thumby.display.drawText(res, 36, 10, 1)
            
        thumby.display.drawText("U:+1 D:-1", 0, 20, 1)
        thumby.display.drawText("A:Sav B:Back", 0, 32, 1)
        
        if thumby.buttonU.justPressed():
            hp += 1
            res = ""
        if thumby.buttonD.justPressed():
            hp -= 1
            res = ""
        if thumby.buttonA.justPressed():
            try:
                f = open("track.txt", "w")
                f.write(str(hp))
                f.close()
                res = "Saved!"
            except:
                pass
        if thumby.buttonB.justPressed(): state = 0

    elif state == 11:
        thumby.display.drawText("Decks:", 0, 0, 1)
        for i, item in enumerate(cards_menu):
            prefix = ">" if i == c_sel else " "
            thumby.display.drawText(prefix + item, 0, 8 + (i * 8), 1)
            
        if thumby.buttonD.justPressed(): c_sel = (c_sel + 1) % 4
        if thumby.buttonU.justPressed(): c_sel = (c_sel - 1) % 4
        if thumby.buttonA.justPressed():
            if c_sel == 3:
                state = 0
            else:
                # Branches to states 12, 13, or 14
                state = 12 + c_sel
                res = ""
                res2 = ""

    elif state == 12: 
        thumby.display.drawText("Standard", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 10, 1)
        
        j_status = "ON" if jokers_on else "OFF"
        thumby.display.drawText("U/D:Jkr " + j_status, 0, 18, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        
        if thumby.buttonU.justPressed() or thumby.buttonD.justPressed():
            jokers_on = not jokers_on
            
        if thumby.buttonA.justPressed():
            max_val = 54 if jokers_on else 52
            roll = random.randint(1, max_val)
            if roll > 52:
                res = "Joker"
            else:
                idx = roll - 1
                res = ranks[idx % 13] + " " + suits[idx // 13]
                
        # Returns to the Cards sub-menu
        if thumby.buttonB.justPressed(): state = 11
            
    elif state == 13: 
        thumby.display.drawText("Tarot", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 10, 1)
        thumby.display.drawText(str(res2), 0, 18, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        
        if thumby.buttonA.justPressed():
            roll = random.randint(1, 78)
            if roll <= 22:
                res = "Major Arcana"
                res2 = t_maj[roll - 1]
            else:
                idx = roll - 23
                res = "Suit: " + t_suit[idx // 14]
                res2 = t_rnk[idx % 14]
                
        if thumby.buttonB.justPressed(): state = 11

    elif state == 14: 
        thumby.display.drawText("UNO", 0, 0, 1)
        thumby.display.drawText(str(res), 0, 16, 1)
        thumby.display.drawText("A:Gen B:Back", 0, 32, 1)
        
        if thumby.buttonA.justPressed():
            u_roll = random.randint(1, 108)
            if u_roll <= 8:
                res = "Wild" if u_roll <= 4 else "Wild +4"
            else:
                res = random.choice(u_col) + " " + random.choice(u_val)
                
        if thumby.buttonB.justPressed(): state = 11
            
    thumby.display.update()