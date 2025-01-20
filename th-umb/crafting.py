_E='Furnace'
_D='Amethyst'
_C='Bucket+'
_B='Bucket'
_A='Pickaxe'
class Craft:
	def __init__(self,logic,b):self.enabled=[1,1];self.logic=logic;self.craftSpot=0;self.buttons=b;self.amt=0;self.items=[[_A,'Axe','Step','Slab',_B,_C,'Bed'],[_D,'Ruby','Coal'],['Table',_E]]
	@micropython.native
	def checkForCraft(self):
		posX,posY=self.logic.pInt[0],self.logic.pInt[1]
		if posX==0:posX=1
		elif posX==19:posX=18
		if posY==0:posY=1
		elif posY==9:posY=8
		self.enabled=[0,0];step=0;posTypes=[-1,-1,0,-1,1,-1,-1,0,0,0,1,0,-1,1,0,1,1,1]
		for i in range(9):
			if self.logic.world[(posY+posTypes[step+1])*20+(posX+posTypes[step])]==16:self.enabled[0]=1
			if self.logic.world[(posY+posTypes[step+1])*20+(posX+posTypes[step])]==17:self.enabled[1]=1
			step+=2
		self.crafting()
	@micropython.native
	def tableCraft(self,check,item):
		slot=[-1]*len(check)
		for i in range(len(self.logic.inv)):
			if self.logic.inv[i]!=0:
				for l in range(len(check)):
					if self.logic.inv[i][0]==check[l][0]:slot[l]=i
		for l in range(len(slot)):
			if slot[l]==-1:return 0
		@micropython.native
		def checker():
			for i in range(len(slot)):
				if self.logic.inv[slot[i]][1]>=check[i][1]:
					self.logic.inv[slot[i]][1]-=check[i][1]
					if self.logic.inv[slot[i]][1]<=0:self.logic.inv[slot[i]]=0
					return 1
			return 0
		for l in range(len(self.logic.inv)):
			if self.logic.inv[l]==0:
				if checker()==1:self.logic.inv[l]=[item,1]
				self.logic.display.fill(2);return
			elif self.logic.inv[l][0]==item:
				if checker()==1:self.logic.inv[l][1]+=1
				self.logic.display.fill(2);return
	@micropython.native
	def crafting(self):
		if self.logic.invArea!=0:
			self.amt=len(self.items[self.logic.invArea-1])-1
			if self.amt<self.craftSpot:self.craftSpot=self.amt
			if self.buttons.buttonL.justPressed():self.craftSpot=max(0,self.craftSpot-1)
			if self.buttons.buttonR.justPressed():self.craftSpot=min(self.amt,self.craftSpot+1)
		if self.logic.invArea==1 and self.enabled[0]==1:
			self.logic.display.drawText(self.items[0][self.craftSpot],5,32,1);self.logic.display.drawText('#',66,32,1);check=[]
			if self.buttons.buttonB.justPressed():
				if self.items[0][self.craftSpot]==_A:check=[[1,3],[3,5]];self.tableCraft(check,7)
				elif self.items[0][self.craftSpot]=='Axe':check=[[1,3],[3,4]];self.tableCraft(check,8)
				elif self.items[0][self.craftSpot]=='Slab':check=[[1,2]];self.tableCraft(check,9)
				elif self.items[0][self.craftSpot]=='Step':check=[[17,5]];self.tableCraft(check,10)
				elif self.items[0][self.craftSpot]==_B:check=[[5,3]];self.tableCraft(check,14)
				elif self.items[0][self.craftSpot]==_C:check=[[5,3],[6,3]];self.tableCraft(check,15)
				elif self.items[0][self.craftSpot]=='Bed':check=[[1,3],[5,3]];self.tableCraft(check,13)
			return
		elif self.logic.invArea==1 and self.enabled[0]==0:self.logic.display.drawText('Need #',5,32,1);return
		if self.logic.invArea==2 and self.enabled[1]==1:
			self.logic.display.drawText(self.items[1][self.craftSpot],5,32,1);self.logic.display.drawText('0',66,32,1);check=[]
			if self.buttons.buttonB.justPressed():
				if self.items[1][self.craftSpot]==_D:check=[[4,2]];self.tableCraft(check,6)
				elif self.items[1][self.craftSpot]=='Ruby':check=[[4,3]];self.tableCraft(check,5)
				elif self.items[1][self.craftSpot]=='Coal':check=[[1,1]];self.tableCraft(check,4)
			return
		elif self.logic.invArea==2 and self.enabled[1]==0:self.logic.display.drawText('Need 0',5,32,1);return
		if self.logic.invArea==3:
			self.logic.display.drawText(self.items[2][self.craftSpot],5,32,1);self.logic.display.drawText('+',66,32,1);check=[]
			if self.buttons.buttonB.justPressed():
				if self.items[2][self.craftSpot]=='Table':check=[[1,4]];self.tableCraft(check,12)
				elif self.items[2][self.craftSpot]==_E:check=[[3,4]];self.tableCraft(check,11)
			return