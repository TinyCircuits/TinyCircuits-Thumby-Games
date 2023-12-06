#Note: code V squished to save mem
from thumbyGraphics import display as d
from thumbySprite import Sprite
import thumbyHardware as hardware
from thumbyAudio import audio
from sys import print_exception
from os import ilistdir
from random import randint
from re import search
from sys import path
if not '/Games/TinyEdit' in path:
	path.append( '/Games/TinyEdit' )
import btn

baseFPS=12
d.setFPS(baseFPS)

def defaultFont():
	d.setFont("/lib/font5x7.bin",5,10,1)

def noise(length):
	for _ in range(length):
		audio.playBlocking(randint(400,500),10)

def buzz():
	d.display.invert(1)
	d.update()
	noise(3)
	d.display.invert(0)
	d.update()
	noise(12)

def sideScroll(st,x,y,w,b,lm):
	if len(st)*6>w:
		global baseFPS
		d.setFPS(45)
		stLen=len(st)*6+w
		o=b if b>0 else 0
		while True:
			d.drawFilledRectangle(x,y,w,8,0)
			d.drawText(st,x+w-o,y,1)
			if 'lFill' in lm:
				lm['lFill']()
			d.update()
			b=btn.which(False)
			if b and b.upper() in lm:
				d.setFPS(baseFPS)
				return lm[b.upper()]()
			o=(o+1)%(stLen)
	elif 'lFill' in lm:
		lm['lFill']()
	d.drawText(st,x,y,1)
	d.update()
	b=btn.which(False)
	if b and b.upper() in lm:
		return lm[b.upper()]()

def splash():
	d.fill(0)
	d.drawSprite(Sprite(37,20,
		bytearray([128,192,224,112,48,48,112,224,128,0,0,0,0,0,0,0,192,160,80,168,212,234,245,250,253,254,127,191,95,175,87,43,21,10,5,2,1,159,255,240,224,240,56,28,15,3,0,0,0,0,128,252,245,234,213,171,215,47,95,55,43,21,10,5,2,1,0,0,0,0,0,0,0,0,3,1,0,1,3,3,6,6,6,6,6,3,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
		0,0,0))
	d.setFont("/lib/font8x8.bin",8,8,1)
	d.drawText("Tiny",38,0,1)
	d.drawText("Edit",30,10,1)
	defaultFont()
	d.drawText("Text editor",3,22,1)
	d.drawText('A/B: Start',6,33,1)
	while not btn.actionJustPressed():
		d.update()

def getDirAbove(path):
	return path[0:path.rfind('/',0,len(path)-1)]

class Sprites:
	shiftKey=Sprite(7,8,
		bytearray([255,251,129,252,129,251,255,0,4,126,3,126,4,0]))
	tabKey=Sprite(9,8,
		bytearray([247,247,247,128,193,227,247,128,255,8,8,8,127,62,28,8,127,0]))
	arrowFrameData=bytearray([247,227,193,128,247,247,255,8,28,62,127,8,8,0])
	leftArrowKey=Sprite(7,8,
		arrowFrameData)
	rightArrowKey=Sprite(7,8,
		arrowFrameData,0,0,0,1)
	delEndFrameData=bytearray([247,235,213,170,213,170,221,190,170,182,170,190,128,8,20,42,85,42,85,34,65,85,73,85,65,127])
	leftDelEndKey=Sprite(13,8,
		delEndFrameData)
	rightDelEndKey=Sprite(13,8,
		delEndFrameData,0,0,0,1)
	delWordFrameData=bytearray([247,235,213,170,221,190,170,182,170,190,128,8,20,42,85,34,65,85,73,85,65,127])
	leftDelWordKey=Sprite(11,8,
		delWordFrameData)
	rightDelWordKey=Sprite(11,8,
		delWordFrameData,0,0,0,1)
	delFrameData=bytearray([247,235,221,190,170,182,170,190,128,8,20,34,65,85,73,85,65,127])
	leftDelKey=Sprite(9,8,
		delFrameData)
	rightDelKey=Sprite(9,8,
		delFrameData,0,0,0,1)
	moveIcon=Sprite(5,11,
		bytearray([68,198,255,198,68,0,0,1,0,0]),
		0,16,0)

class Menu:
	def __init__(s,items):
		s.items=items
		s.count=len(items)
		s.item=0
		s.result=None

	def a(s):
		s.result=s.items[s.item][1]()
		return True

	def u(s):
		if s.item>0:
			s.item=s.item-1
		return False

	def d(s):
		if s.item<len(s.items)-1:
			s.item=s.item+1
		return False

	def displayItems(s):
		return[
			(None if s.item<2 else s.items[s.item-2][0]),
			(None if s.item<1 else s.items[s.item-1][0]),
			(s.items[s.item][0]),
			(None if s.item+1>=s.count else s.items[s.item+1][0]),
			(None if s.item+2>=s.count else s.items[s.item+2][0])
		]

	def display(s):
		def lF():
			d.drawFilledRectangle(0,16,6,8,0)
			d.drawText('>',0,16,1)
		s.result=None
		while True:
			d.fill(0)
			itemY=0
			for item in s.displayItems():
				if item:
					if itemY==16:
						curr=item
					else:
						d.drawText(item,6,itemY,1)
				itemY=itemY+8
			if sideScroll(curr,6,16,d.width,d.width,{'A':lambda:s.a(),'B':lambda:True,'U':lambda:s.u(),'D':lambda:s.d(),'lFill':lambda:lF()}):
				break
		return s.result

shownKbInstructions=False

class Key:
	def __init__(s,character):
		s.character=character
		s.selected=False

	def display(s,x,y):
		if s.character==' ':
			if s.selected:
				d.drawFilledRectangle(x,y,16,8,1)
			d.setFont("/lib/font3x5.bin",3,5,1)
			d.drawText('[sp]',x+1,y+2,0 if s.selected else 1)
			defaultFont()
			return 16
		if s.selected:
			d.drawFilledRectangle(x,y,7,8,1)
		d.drawText(s.character,x+1,y,0 if s.selected else 1)
		return 7

	def select(s,selected):
		s.selected=selected

	def press(s):
		return s.character

class ActionKey:
	def __init__(s,action,sprite):
		s.selected=False
		s.sprite=sprite
		s.action=action

	def display(s,x,y):
		s.sprite.x=x
		s.sprite.y=y
		s.sprite.setFrame(0 if s.selected else 1)
		d.drawSprite(s.sprite)
		return s.sprite.width

	def select(s,selected):
		s.selected=selected

	def press(s):
		ch=s.action()
		return ch if ch else ''

class KeyRow:
	def __init__(s,rowNum,characters,selected=0):
		s.rowNum=rowNum
		s.keys=[]
		for character in characters:
			s.keys.append(Key(character))
		s.selected=selected
		if selected:
			s.select(selected)

	def append(s,key):
		s.keys.append(key)

	def insert(s,index,key):
		s.keys.insert(index,key)

	def select(s,index):
		s.keys[s.selected].select(False)
		if index<0:
			s.selected=len(s.keys)-1
		elif index>=len(s.keys):
			s.selected=0
		else:
			s.selected=index
		s.keys[s.selected].select(True)

	def deselect(s):
		s.keys[s.selected].select(False)

	def display(s):
		offset=s.rowNum
		for i,key in enumerate(s.keys):
			offset=offset+key.display(offset,s.rowNum*8)

	def right(s):
		s.select(s.selected+1)

	def left(s):
		s.select(s.selected-1)

	def getCharacter(s):
		return s.keys[s.selected].press()

class KeyLayer:
	def __init__(s,characterRows):
		s.rows=[]
		for i,characterRow in enumerate(characterRows):
			s.rows.append(KeyRow(i,characterRow))
		s.row=3

	def add(s,key,rowNum):
		s.rows[rowNum].append(key)

	def insert(s,key,rowNum,index):
		s.rows[rowNum].insert(index,key)

	def display(s):
		for row in s.rows:
			row.display()

	def up(s):
		if s.row>0:
			index=s.rows[s.row].selected
			s.rows[s.row].deselect()
			s.row=s.row-1
			s.rows[s.row].select(index)

	def down(s):
		if s.row<len(s.rows)-1:
			index=s.rows[s.row].selected
			s.rows[s.row].deselect()
			s.row=s.row+1
			s.rows[s.row].select(index)

	def left(s):
		s.rows[s.row].left()

	def right(s):
		s.rows[s.row].right()

	def getCharacter(s):
		return s.rows[s.row].getCharacter();

class Keyboard:
	def __init__(s,text,position,layer=0):
		s.layers=[
			KeyLayer(['qwertyuiop','asdfghjkl','zxcvbnm,.',' ']),
			KeyLayer(['QWERTYUIOP','ASDFGHJKL','ZXCVBNM()',' ']),
			KeyLayer(['1234567890','!"#$%^&*[]',"`_+-=;:@'~",' ']),
			KeyLayer(['1234567890','#<>?/|\\{}','',' '])
		]
		shiftKey=ActionKey(lambda:s.shiftKey(),Sprites.shiftKey)
		shiftKey.selected=True
		tabKey=ActionKey(lambda:'\t',Sprites.tabKey)
		for i in range(4):
			s.layers[i].insert(tabKey,3,0)
			s.layers[i].insert(shiftKey,3,0)

		leftArrowKey=ActionKey(lambda:s.leftArrow(),Sprites.leftArrowKey)
		for i in range(4):
			s.layers[i].add(leftArrowKey,3)
		rightArrowKey=ActionKey(lambda:s.rightArrow(),Sprites.rightArrowKey)
		for i in range(4):
			s.layers[i].add(rightArrowKey,3)

		s.layers[3].add(ActionKey(lambda:s.leftDelEnd(),Sprites.leftDelEndKey),2)

		leftDelWordKey=ActionKey(lambda:s.leftDelWord(),Sprites.leftDelWordKey)
		for i in range(3):
			s.layers[i].add(leftDelWordKey,3)
		s.layers[3].add(leftDelWordKey,2)

		delKey=ActionKey(lambda:s.delKey(),Sprites.leftDelKey)
		for i in range(3):
			s.layers[i].add(delKey,3)
		s.layers[3].add(delKey,2)

		s.layers[3].add(ActionKey(lambda:s.rightDel(),Sprites.rightDelKey),2)
		s.layers[3].add(ActionKey(lambda:s.rightDelWord(),Sprites.rightDelWordKey),2)
		s.layers[3].add(ActionKey(lambda:s.rightDelEnd(),Sprites.rightDelEndKey),2)

		s.layer=layer
		s.text=text
		s.cursor=min(position+6,len(text))

	def shiftKey(s):
		s.layer=s.layer+1
		if s.layer>=len(s.layers):
			s.layer=0

	def delKey(s):
		if s.cursor>0:
			s.text=s.text[0:s.cursor-1]+s.text[s.cursor:]
			s.cursor=s.cursor-1
		else:
			buzz()

	def rightDel(s):
		if s.cursor < len(s.text):
			s.text=s.text[0:s.cursor]+s.text[s.cursor+1:]
		else:
			buzz()

	def leftDelWord(s):
		pre=s.text[0:s.cursor]
		match=search(r'(\w+|\W+)$',pre)
		if match:
			start=match.start()
			s.text=pre[0:start]+s.text[s.cursor:]
			s.cursor=start
		else:
			buzz()

	def rightDelWord(s):
		post=s.text[s.cursor:]
		match=search(r'^(\w+|\W+)',post)
		if match:
			end=match.end()
			s.text=s.text[0:s.cursor]+post[end:]
		else:
			buzz()

	def leftDelEnd(s):
		s.text=s.text[s.cursor:]
		s.cursor=0

	def rightDelEnd(s):
		s.text=s.text[0:s.cursor]

	def leftArrow(s):
		if s.cursor>0:
			s.cursor=s.cursor-1

	def rightArrow(s):
		if s.cursor<len(s.text):
			s.cursor=s.cursor+1

	def display(s):
		d.fill(0)
		s.layers[s.layer].display()
		textLen=len(s.text)
		if textLen<=10:
			windowStart=0
			windowEnd=len(s.text)
		elif s.cursor <=6:
			windowStart=0
			windowEnd=min(10,textLen)
		else:
			windowStart=s.cursor-6
			windowEnd=min(textLen,s.cursor+4)
		windowText=s.text[windowStart:windowEnd]
		if windowStart>0:
			d.drawText('<',0,33,1)
		adjCursor=s.cursor-windowStart
		for i,ch in enumerate(windowText):
			x=6*i+6
			if i==adjCursor:
				d.drawFilledRectangle(x,33,6,8,1)
				colour=0
			else:
				colour=1
			d.drawText(ch,x,33,colour)
		if s.cursor==textLen:
			d.drawFilledRectangle(adjCursor*6+6,33,6,8,1)
		if textLen>windowEnd:
			d.drawText('>',66,33,1)
		d.update()

	def handleInput(s):
		b=btn.which()
		if not b:
			return None
		if b in 'Uu':
			s.layers[s.layer].up()
		elif b in 'Dd':
			s.layers[s.layer].down()
		elif b in 'Rr':
			s.layers[s.layer].right()
		elif b in 'Ll':
			s.layers[s.layer].left()
		elif b in 'Aa':
			s.handlePress()
		elif b=='B':
			result=s.text
			s.text=''
			return result
		return None

	def handlePress(s):
		keyOut=s.layers[s.layer].getCharacter()
		if len(keyOut)>0:
			s.text=s.text[0:s.cursor]+keyOut+s.text[s.cursor:]
			s.cursor=s.cursor+1

	def instructions(s):
		global shownKbInstructions
		shownKbInstructions=True
		d.fill(0)
		d.drawText('Keyboard:',12,0,1)
		d.drawText('U',6,8,1)
		d.drawText('L R cursor',0,16,1)
		d.drawText('D',6,24,1)
		d.drawText('--more--',12,32,1)
		while(not btn.actionJustPressed()):
			d.update()
		d.fill(0)
		d.drawText('Keyboard:',12,0,1)
		d.drawText('A: press key',0,8,1)
		d.drawText('B: close',0,16,1)
		d.drawText('--start--',6,32,1)
		while(not btn.actionJustPressed()):
			d.update()

	def getOutput(s):
		global shownKbInstructions
		if not shownKbInstructions:
			s.instructions()
		while True:
			s.display()
			output=s.handleInput()
			if output or output=='':
				return output

class Line:
	def __init__(s,text):
		s.text=text
		s.size=len(text)

	def getText(s,position):
		if position>s.size:
			return '<'
		if position>0:
			result='<'
		else:
			result=' '
		maxRight=position+10
		result+=s.text[position:min(maxRight,s.size)]
		if maxRight<s.size:
			result=result+'>'
		return result

class Mode:
	MENU=1
	SCROLL=2
	MOVE=3
	SPLIT=4

class File:
	def __init__(s,fileName):
		s.fileName=fileName
		s.lines=[]
		if fileName:
			with open(fileName,encoding="utf-8") as f:
				for line in f.read().splitlines():
					s.lines.append(Line(line))
		if len(s.lines)==0:
			s.lines.append(Line(""))
		s.line=0
		s.position=0
		s.splitPosition=-1

	def getDisplayLine(s,index):
		if index<0 or index>=len(s.lines):
			return None
		return s.lines[index].getText(s.position)

	def getDisplayLines(s):
		return[
			s.getDisplayLine(s.line-2),
			s.getDisplayLine(s.line-1),
			s.getDisplayLine(s.line),
			s.getDisplayLine(s.line+1),
			s.getDisplayLine(s.line+2)
		]

	def getFullLine(s,index=None):
		if index==None:
			return s.lines[s.line].text
		if index<0 or index>=len(s.lines):
			return None
		return s.lines[index].text

	def display(s,mode):
		d.fill(0)
		if mode==Mode.SPLIT:
			Sprites.leftArrowKey.setFrame(1)
			Sprites.rightArrowKey.setFrame(1)
		lineY=0
		for line in s.getDisplayLines():
			if line:
				if lineY==16:
					if mode==Mode.MOVE:
						d.drawText(line,1,lineY,1)
						d.drawRectangle(6,lineY,d.width-12,8,1)
						d.drawFilledRectangle(0,lineY,6,7,0)
						Sprites.moveIcon.x=0
						d.drawSprite(Sprites.moveIcon)
						d.drawFilledRectangle(d.width-6,lineY,6,7,0)
						Sprites.moveIcon.x=d.width-5
						d.drawSprite(Sprites.moveIcon)
					elif mode==Mode.SPLIT:
						d.drawText(line,1,lineY,1)
						top=lineY-1
						rhs=d.width-7
						d.drawLine(6,top,rhs,top,1)
						d.drawFilledRectangle(0,lineY,6,7,0)
						Sprites.leftArrowKey.x=0
						Sprites.leftArrowKey.y=lineY
						d.drawSprite(Sprites.leftArrowKey)
						d.drawLine(6,lineY,6,lineY+7,1)
						d.drawFilledRectangle(rhs,lineY,6,7,0)
						Sprites.rightArrowKey.x=rhs
						Sprites.rightArrowKey.y=lineY
						d.drawSprite(Sprites.rightArrowKey)
						d.drawLine(rhs,lineY,rhs,lineY+7,1)
					else:
						d.drawFilledRectangle(0,16,d.width,8,1)
						d.drawText(line,1,lineY,0)
				else:
					d.drawText(line,1,lineY,1)
				if lineY==24 and mode==Mode.SPLIT:
					d.drawFilledRectangle(0,lineY,6,7,0)
					Sprites.leftArrowKey.y=lineY
					d.drawSprite(Sprites.leftArrowKey)
					d.drawLine(6,lineY,6,lineY+7,1)
					rhs=d.width-7
					bottom=lineY+7
					d.drawLine(6,bottom,rhs,bottom,1)
					d.drawFilledRectangle(rhs,lineY,6,7,0)
					Sprites.rightArrowKey.y=lineY
					d.drawSprite(Sprites.rightArrowKey)
					d.drawLine(rhs,bottom,rhs,lineY,1)
			lineY=lineY+8
		d.update()

	def goTo(s,line):
		if line>=0 and line<len(s.lines):
			s.line=line
		else:
			buzz()

	def up(s):
		if s.line>0:
			s.line=s.line-1

	def down(s):
		if s.line+1<len(s.lines):
			s.line=s.line+1

	def moveUp(s):
		if s.line>0:
			s.lines.insert(s.line-1,s.lines.pop(s.line))
			s.line=s.line-1
		else:
			buzz()

	def moveDown(s):
		if s.line<len(s.lines)-1:
			s.lines.insert(s.line+1,s.lines.pop(s.line))
			s.line=s.line+1
		else:
			buzz()

	def left(s):
		if s.position>0:
			s.position=s.position-1

	def right(s):
		s.position=s.position+1

	def setPosition(s,position):
		if position>=0:
			s.position=position
		else:
			buzz()

	def selectLine(s,lineNumber):
		if lineNumber>=0 and lineNumber<len(s.lines):
			s.line=lineNumber
		else:
			buzz()

	def replaceLine(s,newText):
		s.lines[s.line]=Line(newText)

	def deleteLine(s):
		if len(s.lines)>1:
			s.lines.pop(s.line)
			if s.line>=len(s.lines):
				s.line=len(s.lines)-1
		else:
			buzz()

	def joinNext(s):
		if s.line<len(s.lines)-1:
			s.replaceLine(s.getFullLine()+' '+s.lines[s.line+1].text)
			s.lines.pop(s.line+1)
		else:
			buzz()

	def startSplit(s):
		originalLine=s.getFullLine()
		lenOriginalLine=len(originalLine)
		if s.position+6>lenOriginalLine:
			s.position=max(lenOriginalLine-6,0)
		s.splitPosition=min(s.position+6,lenOriginalLine)
		s.duplicateLine()
		s.replaceLine(s.getFullLine()[s.splitPosition:])
		s.up()
		s.replaceLine(originalLine[0:s.splitPosition])

	def shiftSplitLeft(s):
		if s.splitPosition>0:
			s.down()
			s.replaceLine(s.lines[s.line-1].text[-1]+s.getFullLine())
			s.up()
			s.replaceLine(s.getFullLine()[0:-1])
			if s.position>0:
				s.position=s.position-1
			s.splitPosition=s.splitPosition-1
		else:
			buzz()

	def shiftSplitRight(s):
		if len(s.lines[s.line+1].text)>0:
			s.replaceLine(s.getFullLine()+s.lines[s.line+1].text[0])
			s.down()
			s.replaceLine(s.getFullLine()[1:])
			s.up()
			if s.splitPosition>6:
				s.position=s.position+1
			s.splitPosition=s.splitPosition+1
		else:
			buzz()

	def duplicateLine(s):
		line=s.lines[s.line]
		newLine=Line(line.text)
		s.lines.insert(s.line,newLine)
		s.line=s.line+1

	def save(s,dir):
		if not s.fileName:
			s.fileName=dir+'/'+Keyboard("",0).getOutput()
		with open(s.fileName,'w',encoding="utf-8") as f:
			for thisLine in s.lines:
				f.write(thisLine.text)
				f.write('\n')

class Editor:
	def __init__(s):
		s.mode=Mode.MENU
		s.file=None
		s.dir=''
		s.findStr=''
		s.findLine=0
		s.noFileMenu=Menu([
			('Open...',lambda:s.open()),
			('Help',lambda:s.hlp()),
			('Exit',lambda:hardware.reset())
		])
		s.withFileMenu=Menu([
			('File...',lambda:s.fileMenu.display()),
			('Line...',lambda:s.lineMenu.display()),
			('Help',lambda:s.hlp()),
			('Exit',lambda:hardware.reset())
		])
		s.fileMenu=Menu([
			('Open...',lambda:s.open()),
			('Save...',lambda:s.save()),
			('New...',lambda:s.new())
		])
		s.lineMenu=Menu([
			('Duplicate',lambda:s.file.duplicateLine()),
			('Move',lambda:s.move()),
			('Find...',lambda:s.find()),
			('Find next',lambda:s.findNext()),
			('Go to...',lambda:s.goTo()),
			('Join next',lambda:s.file.joinNext()),
			('Split',lambda:s.split()),
			('Delete',lambda:s.file.deleteLine())
		])

	def save(s):
		if s.file.fileName:
			m=Menu([
				(s.file.fileName[s.file.fileName.rfind('/')+1:],lambda:s.file.save(s.dir)),
				('Save as...',lambda:s.saveAs())
			])
			m.display()
		else:
			s.file.save(s.dir)

	def saveAs(s):
		s.file.fileName=None
		s.file.save(s.dir)

	def hlp(s):
		d.fill(0)
		d.drawText("Keys:",18,0,1)
		d.drawText("U",12,8,1)
		d.drawText("L R scroll",6,16,1)
		d.drawText("D",12,24,1)
		d.drawText("--more--",12,32,1)
		while not btn.actionJustPressed():
			d.update()
		d.fill(0)
		d.drawText("A menu,",0,0,1)
		d.drawText("choose",24,8,1)
		d.drawText("B edit line,",0,16,1)
		d.drawText("close menu",12,24,1)
		d.drawText("--key help--",0,32,1)
		while not btn.actionJustPressed():
			d.update()
		def drwSp(sp,x,y):
			sp.x=x
			sp.y=y
			sp.setFrame(1)
			d.drawSprite(sp)
		d.fill(0)
		drwSp(Sprites.leftDelKey,0,0)
		drwSp(Sprites.rightDelKey,10,0)
		d.drawText("Del",21,0,1)
		drwSp(Sprites.leftDelWordKey,0,8)
		drwSp(Sprites.rightDelWordKey,12,8)
		d.drawText("Del chnk",25,8,1)
		drwSp(Sprites.leftDelEndKey,0,16)
		drwSp(Sprites.rightDelEndKey,14,16)
		d.drawText("Del EOL",29,16,1)
		drwSp(Sprites.shiftKey,2,24)
		d.drawText("Shift",12,24,1)
		sideScroll('More help: http://codeberg.org/JBanana/TinyEdit',0,33,d.width,0,{'A':lambda:None,'B':lambda:None})

	def chooseFile(s,dirPath=None):
		if not dirPath:
			dirPath='/'
		while True:
			if not dirPath[-1:]=='/':
				dirPath=dirPath+'/'
			dirEntry=s.chooseDirEntry(dirPath)
			if not dirEntry:
				return None
			newPath=dirEntry[0]
			entryType=dirEntry[1]
			if entryType==0x4000: #dir
				dirPath=newPath
			elif entryType==0x8000: #file
				return newPath

	def chooseDirEntry(s,dirPath):
		def makeLambda(dirEntry):
			return lambda:dirEntry
		dirMenuItems=[]
		if dirPath!='/':
			dirAbove=getDirAbove(dirPath)
			if dirAbove=='':
				dirAbove='/'
			dirMenuItems.append(('../',makeLambda((dirAbove,0x4000))))
		for dirEntry in ilistdir(dirPath):
			entryType=dirEntry[1]
			if entryType==0x4000:
				dirMenuItems.append((dirEntry[0]+'/',makeLambda((dirPath+dirEntry[0],0x4000))))
			elif entryType==0x8000:
				dirMenuItems.append((dirEntry[0],makeLambda((dirPath+dirEntry[0],0x8000))))
		return Menu(dirMenuItems).display()

	def open(s,fileName=None):
		if fileName:
			s.file=File(fileName)
			return
		if s.file:
			chosenPath=s.chooseFile(getDirAbove(s.file.fileName))
		else:
			chosenPath=s.chooseFile()
		if chosenPath:
			s.file=File(chosenPath)
			s.dir=getDirAbove(chosenPath)

	def new(s):
		lastDir=s.dir
		s.file=File(None)
		s.dir=lastDir

	def editLine(s):
		s.file.replaceLine(Keyboard(s.file.getFullLine(),s.file.position).getOutput())

	def move(s):
		s.mode=Mode.MOVE

	def find(s):
		s.findStr=Keyboard(s.findStr,0).getOutput()
		s.findLine=0
		s.findNext()

	def goTo(s):
		try:
			s.file.goTo(int(Keyboard(str(s.file.line+1),0,2).getOutput())-1)
		except ValueError:
			buzz()

	def split(s):
		s.file.startSplit()
		s.mode=Mode.SPLIT

	def findNext(s):
		while True:
			line=s.file.getFullLine(s.findLine)
			if line or line=='':
				s.findLine=s.findLine+1
				position=line.find(s.findStr)
				if position>=0:
					s.file.selectLine(s.findLine-1)
					s.file.setPosition(max(0,position-3))
					break
			else:
				buzz()
				break

	def pressedU(s):
		if s.mode==Mode.SPLIT:
			return
		if s.mode==Mode.MOVE:
			s.file.moveUp()
		else:
			s.file.up()

	def pressedD(s):
		if s.mode==Mode.SPLIT:
			return
		if s.mode==Mode.MOVE:
			s.file.moveDown()
		else:
			s.file.down()

	def pressedL(s):
		if s.mode==Mode.SPLIT:
			s.file.shiftSplitLeft()
		else:
			s.file.left()

	def pressedR(s):
		if s.mode==Mode.SPLIT:
			s.file.shiftSplitRight()
		else:
			s.file.right()

	def handleInput(s):
		b=btn.which()
		if not b:
			return
		if b in 'Uu':
			s.pressedU()
		elif b in 'Dd':
			s.pressedD()
		elif b in 'Ll':
			s.pressedL()
		elif b in 'Rr':
			s.pressedR()
		elif b=='B':
			if s.mode==Mode.MOVE or s.mode==Mode.SPLIT:
				s.mode=Mode.SCROLL
			else:
				s.editLine()
		elif b=='A':
			if s.mode==Mode.MOVE or s.mode==Mode.SPLIT:
				s.mode=Mode.SCROLL
			else:
				s.mode=Mode.MENU

	def display(s):
		if s.mode==Mode.MENU:
			if s.file:
				s.withFileMenu.display()
			else:
				s.noFileMenu.display()
			if s.file and s.mode==Mode.MENU:
				s.mode=Mode.SCROLL
		elif s.file:
			s.file.display(s.mode)
		else:
			buzz()
			s.mode=Mode.MENU

try:
	splash()
	editor=Editor()
	while True:
		editor.handleInput()
		editor.display()
except Exception as x:
	buzz()

	try:
		import emulator
		print_exception(x)
	except ImportError:
		with open('/Games/TinyEdit/crashdump.log','w',encoding="utf-8") as f:
			print_exception(x,f)
	d.fill(0)
	d.drawText("Editor died",3,8,1)
	d.drawText("Problem was:",0,22,1)
	sideScroll(str(x),0,30,d.width,-1,{'A':lambda:hardware.reset(),'B':lambda:hardware.reset()})
