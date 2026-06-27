import random
def floorGen(logic,sl,worldType):
	if sl.loadWorld(logic,logic.Logic,logic.sprites):return
	allEntities=[];worldNumb={0:0,1:3,2:0,3:11,4:0,5:0,6:9}.get(worldType,0);logic.world=bytearray(worldNumb for _ in range(logic.ws[0]));logic.el=logic.Logic(logic,allEntities,logic.sprites)
def worldGen(logic,sl):
	A='World Finished Generating!'
	if sl.loadWorld(logic,logic.Logic,logic.sprites):return
	types=rand=xPos=yPos=0;allEntities=[];logic.waterLine=[0,0,0];random.seed(logic.counter);logic.worldType=random.randint(0,7)
	if logic.worldType==0:
		types=[79,60,60,5,4];logic.world=bytearray(0 for _ in range(logic.ws[0]))
		for i in range(len(logic.world)):
			rand=random.randint(0,51)
			if rand<30 and types[0]>1:types[0]-=1;logic.world[i]=0
			elif types[0]==0:rand=random.randint(20,40)
			if 30<=rand<40 and types[1]>1:
				types[1]-=1;rand=random.randint(0,1)
				if rand==0:logic.world[i]=1;logic.tileColors[i]=3
				if rand==1:logic.world[i]=2;logic.tileColors[i]=2
			elif types[1]==0:rand=40
			if 40<=rand<50 and types[2]>1:
				types[2]-=1;logic.world[i]=3
				if rand>45 and types[3]>1:allEntities.append([random.randint(0,19),random.randint(0,9),0,random.randint(0,10)])
			elif types[2]==0:rand=50
			if rand>=50 and types[4]>=1:types[4]-=1;logic.world[i]=4
			xPos+=1
			if xPos==10:xPos=0;yPos+=1
		logic.waterLine=[random.randint(1,8),0,random.randint(2,3)];logic.waterLine[1]=logic.waterLine[0]+random.randint(-2,2);waterlineCreate(logic,logic.waterLine)
	elif logic.worldType==1:
		logic.world=bytearray(3 for _ in range(logic.ws[0]))
		for i in range(random.randint(5,20)):logic.counting();random.seed(logic.counter);allEntities.append([random.randint(0,19),random.randint(0,9),0,random.randint(0,10)])
	elif logic.worldType==2:
		logic.world=bytearray(0 for _ in range(logic.ws[0]));types=40
		for i in range(len(logic.world)):
			rand=random.randint(0,45)
			if rand>40 and types>=1:
				types-=1;rand=random.randint(0,1)
				if rand==0:logic.world[i]=1;logic.tileColors[i]=3
				if rand==1:logic.world[i]=2;logic.tileColors[i]=2
		for i in range(10):
			rand=random.randint(0,30)
			if rand>25:allEntities.append([random.randint(0,19),random.randint(0,9),1,0,[0,0]])
	elif logic.worldType==3:
		logic.world=bytearray(11 for _ in range(logic.ws[0]));types=[30,30,10,5]
		for i in range(len(logic.world)):
			rand=random.randint(0,75)
			if 40>rand>30 and types[0]>1:types[0]-=1;logic.world[i]=7;logic.tileColors[i]=2
			elif 50>rand>=40 and types[1]>1:types[1]-=1;logic.world[i]=8;logic.tileColors[i]=3
			elif 60>rand>=55 and types[2]>1:types[2]-=1;logic.world[i]=12;logic.tileColors[i]=1
			elif rand>=70 and types[3]>1:types[3]-=1;logic.world[i]=13;logic.tileColors[i]=1
		for i in range(4):
			rand=random.randint(0,30)
			if rand>25:allEntities.append([random.randint(0,19),random.randint(0,9),1,0,[0,0]])
		for i in range(6):
			rand=random.randint(0,30)
			if rand>25:allEntities.append([random.randint(0,19),random.randint(0,9),3,0])
	elif logic.worldType==4:
		logic.world=bytearray(0 for _ in range(logic.ws[0]));types=[1,40]
		for i in range(len(logic.world)):
			rand=random.randint(0,45)
			if rand>40 and types[1]>=1:
				types[1]-=1;rand=random.randint(0,1)
				if rand==0:logic.world[i]=1;logic.tileColors[i]=3
				if rand==1:logic.world[i]=2;logic.tileColors[i]=2
		for i in range(len(logic.world)):
			rand=random.randint(0,30)
			if rand==10 and types[0]>=1:allEntities.append([random.randint(0,19),random.randint(0,9),2,0,0]);types[0]-=1
	elif logic.worldType==5:rand=random.randint(0,2);sl.loadSpecificWorld(logic,logic.Logic,logic.sprites,rand);print(A);return 0
	elif logic.worldType==6:
		logic.world=bytearray(9 for _ in range(logic.ws[0]));types=100
		for i in range(len(logic.world)):
			rand=random.randint(0,20)
			if rand>=10 and types>=1:logic.world[i]=10
	elif logic.worldType==7:
		logic.world=bytearray(20 for _ in range(logic.ws[0]));types=20
		for i in range(len(logic.world)):
			rand=random.randint(0,20)
			if rand>=15 and types>=1:logic.world[i]=21
	logic.el=logic.Logic(logic,allEntities,logic.sprites);allEntities=[];print(A)
@micropython.native
def waterlineCreate(logic,wl):
	aE=[];x1,y1,x2,y2=0,wl[0],19,wl[1];size=wl[2];dx=abs(x2-x1);dy=abs(y2-y1);sx=1 if x1<x2 else-1;sy=1 if y1<y2 else-1;err=dx-dy
	while True:
		index=y1*logic.ws[1]+x1
		if 0<=index<len(logic.world):
			logic.world[index]=3
			for i in range(1,size+1):
				w_index=(y1-i)*logic.ws[1]+x1
				if 0<=w_index<len(logic.world):logic.world[w_index]=3
		if x1==x2 and y1==y2:break
		e2=2*err
		if e2>-dy:err-=dy;x1+=sx
		if e2<dx:err+=dx;y1+=sy
	print(aE);return aE