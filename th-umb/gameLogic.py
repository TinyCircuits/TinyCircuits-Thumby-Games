import random
from math import*
import thumbyButton as buttons
emulator=True
try:import emulator
except ImportError:emulator=False
class Game:
	def __init__(self,px,py,cx,cy,ws,wx,wy,d,l,s,wg,sl,craft):self.wg=wg;self.sprites=s;self.Logic=l;self.sl=sl;self.display=d;self.el=None;self.pInt=[px,py];self.beds=[0,0];self.iInt=0;self.buttonCraft=0;self.craft=craft;self.invArea=0;self.hInt=bytearray([3,3,0]);self.lInt=bytearray([px,py]);self.cInt=[cx,cy];self.mineLoc=bytearray([px,py,0]);self.jumpedWorlds=None;self.inv=[[17,5],[12,1],0,0,0,0,0,0];self.invNames=['Wood','Seed','Rock','Coal','Ruby','Amethyst','Pickaxe','Axe','Slab','Step','Furnace','Table','Bed','Bucket','Bucket+','Apple','Mavrest'];self.firstLoad=True;self.world=bytearray(0 for _ in range(ws));self.ws=bytearray([ws,wx,wy]);self.worldCoords=[0,0];self.waterLine=bytearray([0,0,0]);self.tileColors=bytearray(random.randint(1,3)for _ in range(len(self.world)));self.countType=bytearray([wx,wy]);self.worldType=0;self.extraInts=bytearray([0,0]);self.counter=random.randint(-2000,2000);self.moveDir=0;self.floor=0
	def seedCreator(self):
		while not(buttons.buttonU.justPressed()or buttons.buttonD.justPressed()or buttons.buttonR.justPressed()or buttons.buttonL.justPressed()or buttons.buttonA.justPressed()or buttons.buttonB.justPressed()):self.display.fill(0);self.counter+=random.randint(-1000,1000);random.seed(self.counter);self.counter=(self.counter+200000)%400000-200000;self.display.drawSprite(self.sprites.Title);self.display.update()
	def counting(self):self.counter+=random.randint(-1000,1000);self.counter=(self.counter+200000)%400000-200000
	@micropython.native
	def randomGlitch(self):
		if self.worldType==7:
			for i in range(random.randint(5,15)):glitches="-'#+/[]@&$!";random_glitches=random.choice(glitches);x,y=random.randint(1,65),random.randint(1,32);self.display.drawFilledRectangle(x,y,5,7,0);self.display.drawText(random_glitches,x,y,random.randint(1,3))
	@micropython.native
	def placeObj(self,step,xPos,yPos,cct):
		x=xPos+self.cInt[0];y=yPos+self.cInt[1]
		def update_tile_color():
			if self.extraInts[0]==cct:self.tileColors[step]=random.randint(2,3)
			self.display.drawText('w',x,y,self.tileColors[step])
		def draw_pocket_sprite():self.sprites.pocket.x=x;self.sprites.pocket.y=y;self.display.drawSprite(self.sprites.pocket)
		def randomLetter():letters='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';random_letter=random.choice(letters);self.display.drawText(random_letter,x,y,random.randint(1,3))
		draw_actions={0:lambda:self.display.drawText('G',x,y,self.tileColors[step]),1:lambda:self.display.drawText('t',x,y,self.tileColors[step]),2:lambda:self.display.drawText('t',x,y,self.tileColors[step]),3:update_tile_color,4:draw_pocket_sprite,5:lambda:self.display.drawText('W',x,y,self.tileColors[step]),6:lambda:self.display.drawText('B',x,y,self.tileColors[step]),7:lambda:self.display.drawText('r',x,y,self.tileColors[step]),8:lambda:self.display.drawText('c',x,y,self.tileColors[step]),9:lambda:self.display.drawText('S',x,y,self.tileColors[step]),10:lambda:self.display.drawText('I',x,y,self.tileColors[step]),11:lambda:self.display.drawText('F',x,y,self.tileColors[step]),12:lambda:self.display.drawText('R',x,y,1),13:lambda:self.display.drawText('A',x,y,1),14:lambda:self.display.drawText('_',x,y,1),15:lambda:self.display.drawText('|',x,y,1),16:lambda:self.display.drawText('#',x,y,1),17:lambda:self.display.drawText('0',x,y,1),18:lambda:self.display.drawText('=',x,y,1),19:lambda:self.display.drawText('U',x,y,1),20:randomLetter,21:lambda:self.display.drawText('M',x,y,1)}
		if self.world[step]in draw_actions:draw_actions[self.world[step]]()
	@micropython.native
	def mine_place(self,item):
		for i in range(len(self.inv)):
			if self.inv[i]!=0 and self.inv[i][0]==item:self.inv[i][1]+=1;break
			if self.inv[i]==0:self.inv[i]=[item,1];break
	def objCheck(self,step):
		current_world=self.world[step];current_inv_slot=self.inv[self.iInt];hit=0
		if current_world in{0,3,9,10,11}and current_inv_slot!=0:
			obj_type=current_inv_slot[0]
			if obj_type==2:
				self.el.entities.append([self.mineLoc[0],self.mineLoc[1],4,[0,0]]);self.inv[self.iInt][1]-=1
				if current_inv_slot[1]==0:self.inv[self.iInt]=0
			elif obj_type==16:
				self.hInt[1]+=1;self.inv[self.iInt][1]-=1
				if current_inv_slot[1]==0:self.inv[self.iInt]=0
			elif obj_type==14:
				if current_world==3:self.inv[self.iInt][0]=15;hit=1
				elif current_world in{0,9,10,11}:self.inv[self.iInt]=0;self.world[step]=19;self.tileColors[step]=1
			elif obj_type==15:
				rand=random.randint(1,3)
				if current_world in{0,9,10,11}:self.inv[self.iInt][0]=14;self.world[step]=3;self.tileColors[step]={0:rand,1:2,2:rand,3:rand,4:rand,5:rand,6:1,7:random.randint(1,3)}.get(self.worldType,rand)
			elif obj_type in{1,3,4,5,6,9,10,11,12,13,17}and hit!=1:
				self.world[step]={1:5,3:7,4:8,5:12,6:13,9:14,10:15,11:17,12:16,13:18,17:21}[obj_type];self.tileColors[step]={1:1,3:2,4:3,5:1,6:1,9:1,10:1,11:1,12:1,13:1,17:1}[obj_type];self.inv[self.iInt][1]-=1
				if current_inv_slot[1]==0:self.inv[self.iInt]=0
		elif current_world!=0 and hit!=1:
			if current_inv_slot==0:
				if current_world==1:self.mine_place(1);hit=1
				elif current_world==2:
					self.tileColors[step]=3;self.world[step]=1
					if random.randint(0,5)>3:self.mine_place(16)
					self.mine_place(2)
				elif current_world==4:self.inv.append(0);hit=1
				elif current_world==7:self.mine_place(3);hit=1
				elif current_world==19:self.mine_place(14);hit=1
				elif current_world==18:self.beds[1]=self.beds[0];self.beds[0]=[self.pInt[0],self.pInt[1],self.worldCoords[0],self.worldCoords[1]]
				elif current_world==16:self.mine_place(12);self.display.fill(1);hit=1
				elif current_world==15:self.mine_place(10);self.display.fill(1);hit=1
			elif current_inv_slot!=0:
				if current_inv_slot[0]==8:
					if current_world==1:
						for i in range(3):self.mine_place(1)
						hit=1
					elif current_world==5:self.mine_place(1);hit=1
					elif current_world==14:self.mine_place(9);hit=1
					elif current_world==15:self.mine_place(10);hit=1
					elif current_world==16:self.mine_place(12);hit=1
					elif current_world==18:self.mine_place(13);hit=1
				elif current_inv_slot[0]==7:
					if current_world==12:self.mine_place(5);self.display.fill(1);hit=1
					elif current_world==13:self.mine_place(6);self.display.fill(1);hit=1
					elif current_world==7:
						rand=random.randint(0,20)
						if 5<rand<=10:self.mine_place(5);self.display.fill(1)
						elif 20>rand>=15:self.mine_place(6);self.display.fill(1)
						hit=1
					elif current_world==8:self.mine_place(4);hit=1
					elif current_world==17:self.mine_place(11);hit=1
					elif current_world==21:self.mine_place(17);self.display.fill(1);hit=1
		if hit==1:rand=random.randint(1,3);self.world[step]={0:0,1:3,2:0,3:11,4:0,5:0,6:9,7:20}.get(self.worldType,0);self.tileColors[step]={0:rand,1:2,2:rand,3:rand,4:rand,5:rand,6:1}.get(self.worldType,rand)
	@micropython.native
	def drawOthers(self,cct):
		p_x=self.pInt[0]*6+self.cInt[0];p_y=self.pInt[1]*8+self.cInt[1];mine_x=self.mineLoc[0]*6+self.cInt[0];mine_y=self.mineLoc[1]*8+self.cInt[1];self.sprites.pSpr.x,self.sprites.pSpr.y=p_x,p_y;self.sprites.mineIcon.x,self.sprites.mineIcon.y=mine_x,mine_y;self.el.entityChecker(self.inv[self.iInt])
		if self.inv[self.iInt]!=0:
			if self.inv[self.iInt][1]<=0:self.inv[self.iInt]=0
		self.display.drawSprite(self.sprites.pSpr)
		if self.mineLoc[2]==1 and self.extraInts[0]<6:self.display.drawSprite(self.sprites.mineIcon)
		elif self.extraInts[0]>5:self.display.drawFilledRectangle(p_x,p_y,5,7,0)
		self.extraInts[0]=(self.extraInts[0]+1)%(cct+1)
	@micropython.native
	def drawWorld(self):
		xPos=yPos=step=water=ice=0;cct=10
		if self.world[self.pInt[1]*20+self.pInt[0]]==15:self.changeFloor()
		for y in range(self.countType[1]):
			for x in range(self.countType[0]):
				if xPos==self.pInt[0]*6 and yPos==self.pInt[1]*8:
					if self.world[step]in{1,2,5,7,8,12,13,16,17,21}:self.camSystem(1)
					elif self.world[step]==3:water=1
					elif self.world[step]==10:ice=1
					else:self.moveDir
				if xPos==self.mineLoc[0]*6 and yPos==self.mineLoc[1]*8 and buttons.buttonA.justPressed()and self.mineLoc[2]==1:self.objCheck(step)
				if-6<xPos+self.cInt[0]<73 and-8<yPos+self.cInt[1]<41:self.placeObj(step,xPos,yPos,cct)
				xPos+=6;step+=1
			yPos+=8;xPos=0
		if water==1:self.camSystem(2)
		elif ice==1:self.camSystem(3)
		self.randomGlitch();self.drawOthers(cct)
	@micropython.native
	def mine(self):
		self.mineLoc[0]=self.pInt[0];self.mineLoc[1]=self.pInt[1]
		if buttons.buttonU.pressed():self.mineLoc[1]-=1
		if buttons.buttonD.pressed():self.mineLoc[1]+=1
		if buttons.buttonL.pressed():self.mineLoc[0]-=1
		if buttons.buttonR.pressed():self.mineLoc[0]+=1
	@micropython.native
	def invDump(self):
		self.display.drawFilledRectangle(0,30,72,10,0);self.display.drawFilledRectangle(0,0,12,8,0);self.display.drawText(str(self.hInt[1]),1,1,1)
		if buttons.buttonD.justPressed():self.invArea=min(len(self.craft.items),self.invArea+1)
		if buttons.buttonU.justPressed():self.invArea=max(0,self.invArea-1)
		if self.invArea==0:
			if buttons.buttonL.justPressed():self.iInt=max(0,self.iInt-1)
			if buttons.buttonR.justPressed():self.iInt=min(len(self.inv)-1,self.iInt+1)
			if self.inv[self.iInt]!=0:
				self.display.drawText(self.invNames[self.inv[self.iInt][0]-1],5,32,1);self.display.drawFilledRectangle(53,0,23,8,0)
				if self.inv[self.iInt][1]<=99:self.display.drawText(str(self.inv[self.iInt][1]),54,1,1)
				else:self.display.drawText('99+',54,1,1)
			else:self.display.drawText('Empty',5,32,1)
		elif self.invArea>=1:self.craft.checkForCraft()
	@micropython.native
	def move(self):
		self.jumpedWorlds=0;check=0
		if not buttons.buttonA.pressed():
			if buttons.buttonU.justPressed():self.pInt[1]-=1;self.moveDir=1;check=1
			if buttons.buttonD.justPressed():self.pInt[1]+=1;self.moveDir=2;check=1
			if buttons.buttonL.justPressed():self.pInt[0]-=1;self.moveDir=3;check=1
			if buttons.buttonR.justPressed():self.pInt[0]+=1;self.moveDir=4;check=1
		return check
	@micropython.native
	def changeWorld(self,pos,amt):
		self.sl.saveWorld(self)
		if pos!=2:self.worldCoords[pos]+=amt
		self.jumpedWorlds=1;self.worldCoords[0]=self.worldCoords[0]%21;self.worldCoords[1]=self.worldCoords[1]%21;self.wg.worldGen(self,self.sl)
	@micropython.native
	def changeFloor(self):
		self.sl.saveWorld(self);self.jumpedWorlds=1;self.floor=0 if self.floor+1>1 else self.floor+1;self.wg.floorGen(self,self.sl,self.worldType)
		if self.floor==1:self.world[self.pInt[1]*20+self.pInt[0]]=15
		self.pInt[0]+=random.randint(-1,1);self.pInt[1]+=random.randint(-1,1)
	@micropython.native
	def clamp(self,m):
		if m==1 and self.floor==0:
			if self.pInt[1]>=10:self.pInt[1]=0;self.changeWorld(1,1)
			if self.pInt[1]<=-1:self.pInt[1]=9;self.changeWorld(1,-1)
			if self.pInt[0]>=20:self.pInt[0]=0;self.changeWorld(0,1)
			if self.pInt[0]<=-1:self.pInt[0]=19;self.changeWorld(0,-1)
		self.cInt[1]+=8 if self.pInt[1]*8+self.cInt[1]<=9 else 0;self.cInt[1]-=8 if self.pInt[1]*8+self.cInt[1]>=26 else 0;self.cInt[0]+=6 if self.pInt[0]*6+self.cInt[0]<=15 else 0;self.cInt[0]-=6 if self.pInt[0]*6+self.cInt[0]>=51 else 0;self.cInt[0]=max(-48,min(self.cInt[0],1));self.cInt[1]=max(-40,min(self.cInt[1],1))
		if m!=1:self.pInt[0]=max(0,min(self.pInt[0],19));self.pInt[1]=max(0,min(self.pInt[1],9))
	@micropython.native
	def hp(self):
		if self.hInt[2]<=0:self.pInt[0]+=random.randint(-1,1);self.pInt[1]+=random.randint(-1,1);self.hInt[1]-=1;self.hInt[2]=10;self.display.fill(0)
		else:return
		if self.hInt[1]>self.hInt[0]:self.hInt[1]=self.hInt[0]
	@micropython.native
	def camSystem(self,check):
		if buttons.buttonA.pressed()and self.mineLoc[2]==0:self.buttonCraft=1;return
		self.buttonCraft=0;moved=0;cheat=0;self.hInt[2]=max(0,self.hInt[2]-1)
		if cheat==0:
			if check==0:
				self.lInt[0],self.lInt[1]=self.pInt[0],self.pInt[1]
				if self.mineLoc[2]!=1:moved=self.move()
				else:self.mine()
				if buttons.buttonB.justPressed()and not buttons.buttonA.pressed():self.mineLoc[2]=(self.mineLoc[2]+1)%2
				if moved!=0:self.sl.playerSave(self)
				self.clamp(moved)
			elif check==1 and self.jumpedWorlds==0:self.pInt[0],self.pInt[1]=self.lInt[0],self.lInt[1]
			elif check==2:
				self.extraInts[1]+=1
				if self.extraInts[1]>1:self.pInt[0]+=random.randint(-1,1);self.pInt[1]+=random.randint(-1,1);self.extraInts[1]=0
			elif check==3:
				self.extraInts[1]+=1
				if self.extraInts[1]>1:
					if self.moveDir==1:self.pInt[1]-=1
					elif self.moveDir==2:self.pInt[1]+=1
					elif self.moveDir==3:self.pInt[0]-=1
					elif self.moveDir==4:self.pInt[0]+=1
					self.extraInts[1]=0
				self.clamp(0)
		elif cheat==1:
			if check!=0:return
			self.lInt[0],self.lInt[1]=self.pInt[0],self.pInt[1]
			if self.mineLoc[2]!=1:moved=self.move()
			else:self.mine()
			if buttons.buttonB.justPressed():self.mineLoc[2]=(self.mineLoc[2]+1)%2
			self.clamp(moved)