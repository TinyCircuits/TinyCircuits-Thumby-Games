import sys,random,thumbyButton as buttons,gc
gc.collect()
sys.path.append('/Games/th-umb')
try:from gameLogic import Game;from thumbyGrayscale import display;import worldGen as wg;from entityLogic import Logic;import sprites,sl;from crafting import Craft
except ImportError:print(ImportError)
display.setFPS(10)
try:
	renderWorld=0;inst=Game(0,0,10,10,200,20,10,display,Logic,sprites,wg,sl,0);crafter=Craft(inst,buttons);inst.craft=crafter;inst.seedCreator();wg.worldGen(inst,sl)
	try:sl.playerLoad(inst)
	except Exception:inst.pInt[0]=random.randint(0,19);inst.pInt[1]=random.randint(0,9);inst.worldCoords[0]=random.randint(5,15);inst.worldCoords[1]=random.randint(5,15);sl.playerSave(inst);print(Exception)
except Exception:print(Exception)
while True:
	display.fill(0)
	try:
		if inst.hInt[1]<=0:renderWorld=1
		else:renderWorld=0
		if renderWorld==0:
			display.setFont('/lib/font5x7.bin',5,7,1);inst.camSystem(0);inst.drawWorld()
			if inst.buttonCraft==1:inst.invDump()
		elif renderWorld==1:
			display.setFont('/lib/font3x5.bin',3,7,1);display.drawText('You Died.',20,13,1);display.drawText('A/B to respawn',13,19,1);display.drawText('A: Bed 1',13,25,1);display.drawText('B: Bed 2',13,31,1)
			if buttons.buttonA.justPressed():
				renderWorld=0
				if inst.beds[0]!=0:inst.pInt[0]=inst.beds[0][0];inst.pInt[1]=inst.beds[0][1];inst.worldCoords[0]=inst.beds[0][2];inst.worldCoords[1]=inst.beds[0][3]
				else:inst.pInt[0]=random.randint(0,19);inst.pInt[1]=random.randint(0,9);inst.worldCoords[0]=random.randint(0,20);inst.worldCoords[1]=random.randint(0,20)
				wg.worldGen(inst,sl);inst.hInt[1]=inst.hInt[0]
			elif buttons.buttonB.justPressed():
				renderWorld=0
				if inst.beds[1]!=0:inst.pInt[0]=inst.beds[1][0];inst.pInt[1]=inst.beds[1][1];inst.worldCoords[0]=inst.beds[1][2];inst.worldCoords[1]=inst.beds[1][3]
				else:inst.pInt[0]=random.randint(0,19);inst.pInt[1]=random.randint(0,9);inst.worldCoords[0]=random.randint(0,20);inst.worldCoords[1]=random.randint(0,20)
				wg.worldGen(inst,sl);inst.hInt[1]=inst.hInt[0]
	except OSError as e:print(e)
	gc.collect();inst.counting();display.update()