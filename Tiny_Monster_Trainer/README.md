# Tiny_Monster_Trainer 
A game for the Thumby  
Move around, fight monsters, collect monsters, train monsters.  
(Version update information is at the bottom)  




############ **Game Info** ##############

**Player Info**  
To start you can only have up to two Monsters with you.  
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
Learning a new attack cost 3 Training Points, a Monster can know up to 5 attacks.  
A monster can Mutate to increase a procedurally determined stat's maximum training amount.  
A monster can mutate up to 5 times, if you have duplicates of a monster they will mutate in the same ways.  
Mutating can potentially Change the look of a monster.  
Mutating can potentially add a new type to the monster, if a type is added the monster will also learn an attack from the new type.  

**Training Point (TP) Costs**  

Training:     1 TP  
Learn Attack: 3 TP  
Mutate:       5 TP  


############ **Inspire** #############  

Every time your trainer levels up, they will get an Inspiration Point. Inspiration Points can be used to inspire your active monster.  

When a monster is inspired, their max trainable HP goes up by one and they will receive 2 Training Points.

If you inspire a monster through dancing, their max trainable agility goes up by one
If you inspire a monster through flexing, their max trainable strength goes up by one
If you inspire a monster through running, their max trainable endurance goes up by one
If you inspire a monster through meditation, their max trainable mysticism goes up by one
If you inspire a monster through origami, their max trainable tinfoil goes up by one  

  
  
############ **Campfire** #############    
    
 **Leave** : Allows you to select and leave a monster at the campfire.  
 **Bring** : Allows you to select a monster that is already at the campfire to come with you.  
 **Let Go** : Select a Monster at the campfire to release permanently.      
 **Bye** : Leaves the camp  
 
 Only three monsters can stay at the camp at a time.
 A camp can be found by going back to the same screen you started on.  
 A camp can be found randomly by exploring, it is mystically connected to the camp you store your monsters at. (SpOoKy!~)

############ **Bean, The Traveling Merchant** #############  

**Buy** : You can purchase items for sale, everything cost 10 Tiny Coins.   
**Sell**  : Sell your items, everything can be bought for 5 Tiny Coins.  
**Bye** : Leave the merchant.  
  
The only way to get Tiny Coins is to sell items.    
The merchant can be found by exploring.    
  
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

  
Updates as of 01/30/23:  
Added a merchant - Merchant will either be selling items that can increase a stat's maximum amount, or will only be selling crystals.  
Added a campfire - You can leave up to three monsters at the campfire. 
Game automatically saves after interacting with the merchant or campfire.
(I would like to store more monsters at a campfire, but I need to do more testing than I'm able to do right now. :p)  
Changed how roaming monster's stats are generated.  
Changed combat damage so that more damage is applied if a monster is hit with an attack it's weak against.  

   
Older updates can be found at:  
https://github.com/BlakeBild/Tiny_Monster_Trainer 
