import random
from math import*
import sys
sys.path.append('/Games/th-umb')
class Logic:
	def __init__(self,g,e,s):self.gLogic=g;self.entities=e;self.sprites=s
	@micropython.native
	def entityChecker(self,invSlot):
		for entity in self.entities:
			if entity[2]==0:self.fish(self.entities.index(entity))
			elif entity[2]==1:self.bull(self.entities.index(entity))
			elif entity[2]==2:self.trader(self.entities.index(entity),invSlot)
			elif entity[2]==3:self.zombie(self.entities.index(entity))
			elif entity[2]==4:self.seed(self.entities.index(entity))
	@micropython.native
	def seed(self,i):
		entity=self.entities[i];entity[3][1]+=1
		if entity[3][1]>2:entity[3][1]=0;entity[3][0]+=1
		if entity[3][0]>10:self.gLogic.world[entity[1]*20+entity[0]]=random.randint(1,2);self.entities.remove(entity)
		xTree=entity[0]*6+self.gLogic.cInt[0];yTree=entity[1]*8+self.gLogic.cInt[1];self.gLogic.display.drawFilledRectangle(xTree,yTree,5,7,0);self.gLogic.display.drawText('s',xTree,yTree,2)
	@micropython.native
	def zombie(self,i):
		entity=self.entities[i];zombie_sprite=self.sprites.zombie
		if-1>=zombie_sprite.x>=72 or-1>=zombie_sprite.y>=40:return
		radius=[self.gLogic.pInt[0]-entity[0],self.gLogic.pInt[1]-entity[1]]
		if entity[3]>0:entity[3]-=1
		newTx=newTy=0
		if 5>radius[0]>-5 and 5>radius[1]>-5:
			newTx=entity[0];newTy=entity[1]
			if radius[0]>0:newTx+=1
			elif radius[0]<-0:newTx-=1
			if radius[1]>0:newTy+=1
			elif radius[1]<-0:newTy-=1
			ww=20;wh=len(self.gLogic.world)//ww
			if 0<=newTx<ww and 0<=newTy<wh:
				if entity[3]<=0 and self.gLogic.world[newTy*ww+newTx]not in{1,2,3,5,7,8,12,13,14,16,17,21}:entity[0]=newTx;entity[1]=newTy;entity[3]=5
		if radius[0]==0 and radius[1]==0:self.gLogic.hp()
		zombie_sprite.x=entity[0]*6+self.gLogic.cInt[0];zombie_sprite.y=entity[1]*8+self.gLogic.cInt[1];self.gLogic.display.drawSprite(zombie_sprite)
	@micropython.native
	def trader(self,i,invSlot):
		entity=self.entities[i];trader_sprite=self.sprites.trader
		if-1>=trader_sprite.x>=72 or-1>=trader_sprite.y>=40:return
		radius=[self.gLogic.pInt[0]-entity[0],self.gLogic.pInt[1]-entity[1]];entity[3]=0
		if entity[4]>0:entity[4]-=1
		newTx=newTy=0
		if invSlot!=0:
			if(5>radius[0]>-5 and 5>radius[1]>-5)and invSlot[0]in{5,6}:
				entity[3]=1;newTx=entity[0];newTy=entity[1]
				if radius[0]>1:newTx+=1
				elif radius[0]<-1:newTx-=1
				if radius[1]>1:newTy+=1
				elif radius[1]<-1:newTy-=1
				ww=20;wh=len(self.gLogic.world)//ww
				if 0<=newTx<ww and 0<=newTy<wh:
					if entity[4]<=0 and self.gLogic.world[newTy*ww+newTx]not in{1,2,3,5,7,8,12,13,14,16,17,21}:entity[0]=newTx;entity[1]=newTy;entity[4]=5
			if(radius[0]==0 and radius[1]==0)and invSlot[0]in{5,6}:
				invSlot[1]-=1;rand=random.randint(1,8)
				for i in range(random.randint(1,2)):
					if rand not in{5,6}:self.gLogic.mine_place(rand)
				self.gLogic.pInt=[random.randint(self.gLogic.pInt[0]-1,self.gLogic.pInt[0]+1),random.randint(self.gLogic.pInt[1]-1,self.gLogic.pInt[1]+1)]
		trader_sprite.x=entity[0]*6+self.gLogic.cInt[0];trader_sprite.y=entity[1]*8+self.gLogic.cInt[1];trader_sprite.setFrame(entity[3]);self.gLogic.display.drawSprite(trader_sprite)
	@micropython.native
	def bull(self,i):
		entity=self.entities[i];bull_sprite=self.sprites.bull
		if-1>=bull_sprite.x>=72 or-1>=bull_sprite.y>=40:return
		if entity[3]==0:
			player_x,player_y=self.gLogic.pInt[0],self.gLogic.pInt[1];bull_x,bull_y=entity[0],entity[1];directions=[(1,0),(-1,0),(0,1),(0,-1)]
			for(dx,dy)in directions:
				for dist in range(1,5):
					new_x=bull_x+dx*dist;new_y=bull_y+dy*dist
					if new_x==player_x and new_y==player_y:entity[4]=[dx,dy];entity[3]=1;break
		elif entity[3]==1:
			move_x,move_y=entity[4][0],entity[4][1];new_bull_x=entity[0]+move_x;new_bull_y=entity[1]+move_y
			if(new_bull_x<0 or new_bull_x>=20)or(new_bull_y<0 or new_bull_y>=10):entity[3]=0;return
			if self.gLogic.world[new_bull_y*20+new_bull_x]not in{1,2,3,5,7,8,12,13,14,16,17,21}:entity[0],entity[1]=new_bull_x,new_bull_y
			else:entity[3]=0
			if entity[0]==self.gLogic.pInt[0]and entity[1]==self.gLogic.pInt[1]:self.gLogic.hp()
		bull_sprite.x=entity[0]*6+self.gLogic.cInt[0];bull_sprite.y=entity[1]*8+self.gLogic.cInt[1];bull_sprite.setFrame(entity[3]);self.gLogic.display.drawSprite(bull_sprite)
	@micropython.native
	def fish(self,i):
		entity=self.entities[i];entity[3]-=1;fish_sprite=self.sprites.fish
		if-1>=fish_sprite.x>=72 or-1>=fish_sprite.y>=40:return
		if entity[3]<=0:
			entity[3]=10;directions=[(1,0),(-1,0),(0,1),(0,-1)];move=[]
			for(dx,dy)in directions:
				new_x=entity[0]+dx;new_y=entity[1]+dy
				if 0<=new_x<=19 and 0<=new_y<=9 and self.gLogic.world[new_y*20+new_x]==3:move.append((new_x,new_y))
			if move:self.gLogic.counting();random.seed(self.gLogic.counter);rand_move=random.choice(move);entity[0],entity[1]=rand_move
		fish_sprite.x=entity[0]*6+self.gLogic.cInt[0];fish_sprite.y=entity[1]*8+self.gLogic.cInt[1];fish_sprite.setFrame(1 if entity[3]>7 else 0);self.gLogic.display.drawSprite(fish_sprite)