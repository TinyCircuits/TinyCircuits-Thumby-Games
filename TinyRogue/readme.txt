====MANUAL====

	INDEX
	1.	installation
	2.	controls
	3.	actions
	 i.	 exploration
	 ii.	 combat
	4.	abilities
	 i.	 active
	 ii.	 passive
	5.	items
	6.	spells
	7.	modding
	 i.	 configuration
	 ii.	 graphics
	 iii.	 story
	 iv.	 abilities
	 v.	 spells
	 vi.	 classes
	 vii.	 monsters
	 viii.	 bosses
	8.	copyright


==1. Installation==

	PICO-8

	PICO DISPLAY PACK

	THUMBY


==2. Controls==

	PICO-8

		* Arrow keys for movement
		* Arrow keys to cycle through menus, Z/X to select
		* Hold down any button for 1+ second to bring up item menu outside of fights

	PICO DISPLAY PACK
		
		* B/Y/A/X for movement
		* A/B to cycle through menus, X/Y to select
		* Hold down any button for 1+ second to bring up item menu outside of fights

	THUMBY

		* D-pad for menus or movement
		* D-pad to cycle through menus, A/B to select
		* Hold down any button for 1+ seconds to bring up item menu outside of fights


==3. Actions==

	EXPLORATION

		Navigate around the dungeon
		Take the stairs or stay on the same floor
		Hold any key for 1+ seconds to bring up item menu

	COMBAT

		Hit       - 50% chance to hit 1 random enemy for 1hp/level
		Item      - opens up players item list
		Ability   - use active ability belonging to player (see active abilities)
		Run       - player loses 1hp/enemy, 50% chance to escape to nearby area 


==4. Abilities==

=4i. Active ability=
These abilities can only be used during combat.

	ID NAME         EFFECT
	1. Fury         attacks number of times equal to level but decreases accuracy by 25%
	2. Pray         random effect: cast known spells, heal 1hp/level, flee, nothing
	3. Flee         allows user to escape to nearby cell without damage
	4. Cast         allows user to cast known spells (!!not suitable spell effect!!)
	5. Burn         damages all enemies for 1hp/level, *2 if single enemy
	6. Drain        damages 1 enemy for 0.5hp/level (min. 1) and restores hp equal to damage to user
	7. Void         damages all enemies for 0.5hp/level (min. 1), *2 if single enemy, and restores hp equal to damage to user
	8. Shift        gain abilities/passives of random monster <= level until end of next fight
	9. Heal         heals user for 2hp/level
	10.Aura         attack that automatically hits for 0.75hp/level (min. 1)
	11.Slay         damages 1 enemy for 9999hp


==4ii. Passive ability==
These abilities are used automatically when appropriate.

	ID NAME         EFFECT
	1. Resist       reduces all damage by 1 point
	2. Regen        regenerate HP over time (automatic outside of combat)
	3. Disarm       disarms any encountered traps
	4. Learn        learn unknown spells from scrolls
	5. Strike       increases accuracy of any attack by 50%
	6. Immune       takes minimum damage (max. 1)
	7. Dodge        decrease attackers accuracy by 33%
	8. Might		increases all damage by 1 point


==5. Items==
Scrolls can only be used in combat, with no cost to hp, except if the player has the learn passive in which case the spell added to the players known spells. All items are consumed after use.

	ID NAME         EFFECT
	1. Potion       heals user 2hp/level
	2. Map          reveals map
	3. Tools		disarms any traps
	4. *xxxxx       scroll of the spell of the same name
	

==6. Spells==
All spells cost the caster 1hp to cast

	ID NAME         EFFECT	
	1. Missile      same effect as the ability "smite"
	2. Bless        same effect as the ability "pray"
	3. Blink        same effect as the ability "flee"
	4. Fireball     same effect as the ability "burn"
	5. Siphon       same effect as the ability "drain"
	6. Vortex       same effect as the ability "void"
	7. Reshape      same effect as the ability "shift"
	8. Heal         same effect as the ability "heal"
	9. Holy         same effect as the ability "fury"
	10.Slay         same effect as the ability "slay"


====7. MODDING====
TinyRogue allows for limited modding of the game without the need to change any code, by modifying some of the files the overall experience of the game can be altered.

==7i. Configuration==
Two files contain some of the basic setup of the game, modifying the config file will overwrite how the base game will play.

	FILENAME		DESCRIPTION
	settings.txt	contains default settings for the game
	config.txt		contains chances of various effects being trigger

	KEY				VALUE	SETTINGS DESCRIPTION
	image			1		uses text instead of images if set to 0
	story			1		skips story explaination if set to 0
	popup			0		popup windows wiggles side-to-side if set to 1
	audio			1		disables all audio if set to 0
	fades			1		disables transition fade if set to 0

	KEY				VALUE	CONFIG DESCRIPTION
	tohit			0.5		50% chance of damaging monster
	toblock			0.5		50% chance of avoiding damage from monsters
	toavoid			0.5		50% chance of avoiding damage from traps
	toregen			0.25	25% chance of regaining 1hp inside combat (automatic out of combat)
	toactive		0.25	25% chance of monsters using active ability in combat
	tomove			0.05	5% chance of monsters moving when player moves
	gengaps			1		1 wall gap per floor is generated
	genmonsters		1		1 monster per floor is generated
	gentraps		0.5		1 trap per 2 floors the player generated
	gentreasures	0.25	1 treasure per 4 floors the player generated
	genboss			10		starting floor at which boss monsters will appear
	timepopup		1		duration for popups to appear on screen

==7ii. Graphics==
Three images are contained for use with the game, the title screen, main menu, and sprites for the game. All images are black and white with a solid black background. To update these graphics the file needs to be edited or replaced with a file of the same canvas size. All other graphics are based on the system font. Sprites are split into 8x8 tiles with an id of 0 for top left corner and 15 in the bottom right corner. Sprites 8 to 15 are reserved with the remaining to be used for monsters.

	FILENAME 		DESCRIPTION
	title.png		64x32px black and white image
	menu.png		64x16px black and white image
	sprites.png		64x16px black and white image

==7iii. Story==
The game has the potential to display a shorty story at the start of each game to act as flavour text.

	FILENAME		DESCRIPTION
	story.txt		maximum 9 characters per line, separate lines using \n or newline

==7iv. Abilities==
Currently unused, intended as an in-game description for all abilities.

	FILENAME		DESCRIPTION
	abilities.txt	contains description of both active and passive abilities

	KEY				DESCRIPTION
	name			name of ability (recommended 4 characters, max 9)
	description		description of ability (dilimited by "\n", max 9 characters per line)


==7v. Spells==
Spells are separated by the ";" delimiter. Preceeding the information are the keys which determine the order in which to read the data. Unused key data can be left off (see sample for example of how this works in practice). The last entry must not have a ";" at the end or else this creates an empty entry.

	FILENAME		DESCRIPTION
	spells.txt		contains description of spells

	KEY				DESCRIPTION
	id				id of spell (must be in asending order)
	name			name of spell (max 9 characters)
	effect			name of ability to use (must match an existing active ability name)

	sample spells:
		id,name,effect;1,missile,aura;2,blink,flee

==7vi. Classes==
Classes are separated by the ";" delimiter. Preceeding the information are the keys which determine the order in which to read the data. Unused key data can be left off (see sample for example of how this works in practice). The last entry must not have a ";" at the end or else this creates an empty entry.

	FILENAME		DESCRIPTION
	classes.txt		contains description of player classes

	KEY				DESCRIPTION
	id      		character to display on screen (1 character)
	img				image number to use from sprites.png
	name    		name of class (max 9 characters)
	hp      		hp/level (min 1)
	active  		active ability (max 1)
	passive 		passive ability (max 1)
	spells  		known spells, delimited by |
	items			starting items, delimited by |

	sample:
		id,img,name,hp,active,passive,spells,items;@,1,hero,12,cast,resist,bless|drain,potion|map;@,2,hermit,5,flee;@,3,commoner,6

==7vii. Monsters==
Monsters are separated by the ";" delimiter. Preceeding the information are the keys which determine the order in which to read the data. Unused key data can be left off (see sample for example of how this works in practice). The last entry must not have a ";" at the end or else this creates an empty entry.

	FILENAME		DESCRIPTION
	monsters.txt	contains description of monsters

	KEY				DESCRIPTION
	id				character to display on screen (1 character)
	img				image number to use from sprites.png
	name			name of monster (max 9 characters)
	level			damage potential and which floors the monster can appear on
	hp				hp of monster
	active			active ability (max 1)
	passive			passive ability (max 1)
	spells			know spells, delimited by | 

	sample:
		id,img,name,level,hp,active,passive,spells;h,7,hyena,2,3,flee;@,4,warrior,5,15,,resist

==7viii. Bosses==
Works exactly the same as the monsters file except for boss monsters only

	FILENAME	DESCRIPTION
	bosses.txt	contains description of bosses


====COPYRIGHT====

This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA) http://creativecommons.org/licenses/by-sa/4.0/ This license lets others remix, adapt, and build upon your work even for commercial purposes, as long as they credit you and license their new creations under the identical terms. This license is often compared to “copyleft” free and open source software licenses. All new works based on yours will carry the same license, so any derivatives will also allow commercial use. 

TinyRogue: Created by Kieron Scott, 2021