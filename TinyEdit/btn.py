import thumbyButton as b

r = 0

def actionJustPressed():
	return b.actionJustPressed()

def which(actOk=True):
	global r
	if r >= 4:
		if b.buttonU.pressed():
			return 'u'
		elif b.buttonD.pressed():
			return 'd'
		elif b.buttonL.pressed():
			return 'l'
		elif b.buttonR.pressed():
			return 'r'
		elif actOk and b.buttonA.pressed():
			return 'a'
		elif actOk and b.buttonB.pressed():
			return 'b'
		else:
			r = 0
	elif r > 0:
		if b.inputPressed():
			r = r + 1
		else:
			r = 0
	else:
		if b.buttonU.justPressed():
			r = 1
			return 'U'
		if b.buttonD.justPressed():
			r = 1
			return 'D'
		if b.buttonL.justPressed():
			r = 1
			return 'L'
		if b.buttonR.justPressed():
			r = 1
			return 'R'
		if b.buttonA.justPressed():
			r = 1
			return 'A'
		if b.buttonB.justPressed():
			r = 1
			return 'B'
	return None
