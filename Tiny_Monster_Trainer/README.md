# Tiny_Monster_Trainer 
A game for the Thumby  
Move around, fight monsters, collect monsters, train monsters.  
(Version update information is at the bottom)  



############ **Game Info** ##############

**Player Info**  
To start you can only have up to two Monsters with you.    
Each Monster starts with 7 training points.
If you get an additional Monster, you will be asked you to select one & let it go.  
Every 10 Trainer Levels you can have an additional Monster with you, up to a maximum of 5.  
Your Trainer Level also influences how well your Active Monster can fight.  
The higher your Trainer Level, you'll seek out stronger Roaming Monsters to fight.  

**Monster Stats**  
**Health**: Amount of Health the Monster can have.  
**Agility**: Used to determine who attacks first and chance to dodge an attack.  
**Strength**: Used to determine damage for physical attacks.  
**Endurance**: Used to determine defense for physical attacks.  
**Mysticism**: Used to determine damage for magical attacks.   
**Tinfoil**: Used to determine defense for magical attacks.  
**Types**: The Type that the Monster is and what pool of moves it can learn from.  

**Battles**  
**Swap**: shows you your Active Monster and you can select another one of your Monsters to be the Active one.  
**Info**: Shows the opposing Monster's Stats/Types & the Active Monster's Stats/Types.  
**Attack**: Lets you pick a move to use against the opposing Monster.  
**Run**: Lets you escape the battle.  
**Tame**: Lets you try to tame the opposing Monster, at the cost of one Crystal.   

**If a fight is won**, Your active monster will gain 1 Training Point, you will gain an Experience Point towards your Trainer Level, & you might get an Item.  
**If a fight is lost**, one of your Monsters will have its HP & Stamina restored, but it will also be disheartened and lose a Training Point.  


############ **Training** #############  

Train is used to increase a stat by 1 point, up to a maximum amount.  
Learning a new attack cost 3 Training Points, a Monster can know up to 6 attacks.  
A monster can Mutate to increase a procedurally determined stat's maximum training amount.  
A monster can mutate up to 5 times, if you have duplicates of a monster they will mutate in the same ways.  
Mutating can potentially Change the look of a monster.  
Mutating can potentially add a new type to the monster, if a type is added the monster will also learn an attack from the new type.  

**Training Point (TP) Costs**  

Training:     1 TP  
Learn Attack: 3 TP  
Mutate:       5 TP  


############# **Items** ##############  
Items are not usable during combat.  
  
**For items that increase the a stat's maximum trainable amount:**  
  You can only do this 30 times per monster. If you give a monster more than 30 items that do this the maximum number will not go up anymore, but the monster will still recover any HP that the item is set to restore.

#######  
**Item List**  
#######  
  
**Bandaids** - Heals 8 HP  
**PushPops** - Heals 20 HP  
  
**Stickers** - Raises max trainable HP by 1 and heals for 10  
**Vitamins** - Raises max trainable Strength by 1 and heals for 9  
**Helium** - Raises max trainable Agility by 1 and heals for 8  
**Pillows** - Raises max trainable Endurance by 1 and heals for 7  
**Stardust** - Raises max trainable Mysticism by 1 and heals for 6  
**Tinfoil** - Raises max trainable Tinfoil by 1 and heals for 5  

**Crystals** - Will restore all stamina for all moves that the active Monster knows.  **Crystals are also needed for Taming Monsters.** They are consumed by the opposing monster while attempting to Tame  
  
############# **Types: Strengths and Weakness** ##############  

Bonus damage/defense is based on the Attack's Element Type vs Defending Monster Type  

Type | is Strong against | is Weak against
------- | ------|----------
**Earth**       |Wind      | Fire  
**Wind**        |Water     | Earth  
**Water**       |Fire      | Wind  
**Fire**        |Earth     | Water  
------- | ------|----------
**Light**       |Darkness  | Mind  
**Darkness**    |Cute      |Light  
**Cute**        |Mind      |Darkness  
**Mind**        |Light     |Cute  
------- | ------|----------
**Physical**    |Mystical  |Ethereal  
**Mystical**    |Ethereal  |Physical  
**Ethereal**    |Physical  |Mystical  


  
  
#######**Attacks**#######  

If the monster doesn't have the stamina for an attack: They will lose a % of their HP rounded up, then proceed with the attack.  


########  
**Attack List**  
########  
  
(Basic isn't a Monster Type, Basic attacks can't be learned, They are just default starting moves that a Monster can have)  


Monster Type | Attack Name | Element Type | Damage based on Strength/Mysticism
:------- | :-------: | :-------: | :-------:
**Basic** | | | 
------- |"Poke"       |No Element Type      | Strength  
------- |"Hit"        |No Element Type      | Strength  
------- |MagicHit"    |No Element Type      | Mysticism   
**Earth** |   |   |  
------- |"RockToss"        |Earth       | Strength  
------- |"Quake"           |Earth       | Mysticism  
------- |"Pressure"        |Water       | Mysticism     
------- |"Entomb"          |Darkness    | Strength    
**Wind**| |   |   |  
------- |"Gust"        | Wind        | Strength  
------- |"Cyclone"     | Wind        | Mysticism  
------- |"Lightning"   | Light       | Strength  
------- |"Divine Wind" | Ethereal    | Mysticism  
**Water**|   |   |  
------- |"Geyser"      | Water       | Physical  
------- |"Ice Shards"  | Water       | Mysticism  
------- |"Freeze"      | Mind        | Mysticism  
------- |"Wave"        | Physical    | Strength  
**Fire**|   |   |                                  
------- |"Torch"       | Fire        | Strength  
------- |"Blaze"       | Fire        | Mysticism  
------- |"Flare"       | Light       | Mysticism  
------- |"Inferno"     | Wind        | Strength  
**Light**|   |   |                                
------- |"Dazzle"      | Light       | Strength  
------- |"Razzle"      | Light       | Mysticism  
------- |"Radiance"    | Fire        | Strength  
------- |"Gleam"       | Mystical    | Mysticism  
**Darkness**|   |   |
------- |"Murk"        | Darkness    | Strength  
------- |"Shadow"      | Darkness    | Mysticism  
------- |'Unholy Poke" | Mystical    | Strength  
------- |"Dire Ruin"   | Ethereal    | Mysticism  
**Cute**|   |   |
------- |"Sing Song"   | Cute        | Strength  
------- |"Adorbes"     | Cute        | Mysticism  
------- |"Bubbles"     | Water       | Strength  
------- |"Fluff Ball"  | Physical    | Mysticism  
**Mind**|   |   |
------- |"Headbutt"     | Mind       | Strength  
------- |"Psychic"      | Mind       | Mysticism  
------- |"Telekinesis" | Earth      | Strength  
------- |"Good Vibes"   | Cute       | Mysticism  
**Physical**|   |   |
------- |"Body Slam"    | Physical   | Strength  
------- |"Super Hit"    | Physical   | Mysticism  
------- |"Boulder Toss" | Earth      | Strength  
------- |"Love Tap"     | Cute       | Strength  
**Mystical**|   |   |
------- |"Magic Missile" | Mystical   | Strength  
------- |"Ritual"       | Mystical   | Mysticism  
------- |"Rune Toss"    | Wind       | Strength  
------- |"Immolate"     | Fire       | Mysticism  
**Ethereal**|   |   |
------- |"Spooky Hit"    | Ethereal   | Strength   
------- |"Superlunary"   | Ethereal   | Mysticism   
------- |"Obscurity"     | Darkness   | Mysticism  
------- |"Rue"           | Mind       | Mysticism  
  
  
Updates as of 01/17/23:  
Added battle.py so that the battle code is in once place.    
Fixed it so you can't give a name more than 12 characters.  
Fixed it so that the game with have the last attack used be the first selection when you go back into the attack screen.  
Lowered the amount of times you can inspire a monster.  
Changed the chances for taming a monster.  
Rewrote the battle formulas so they are just better.  
Now when an attack happens, it'll grab a random number from a range based on your Str/Myst, then compare it to a number taken from a range based on the opposing monster's Agility.  
There is a chance for an automatic hit and an automatic miss.  
There is now a chance for a crit. The game doesn't let you know if a crit happened yet. The odds of a crit are pretty low. There are 3 levels of severity for crits & you need to be within a small range of the target number to get one. The target number is based on your Str/Myst & your trainer's level.  
   
Older updates can be found at:  
https://github.com/BlakeBild/Tiny_Monster_Trainer 
