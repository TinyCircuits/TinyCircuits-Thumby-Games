from thumbyGraphics import display as d
import thumbyButton as b
from sys import print_exception
from random import randrange
from _thread import start_new_thread
from thumbyAudio import audio
from time import sleep

inEmulator = None
try:
    import emulator
    inEmulator = True
except ImportError:
    inEmulator = False

baseFPS = 4
sideScrollFPS = 45
def setFPS( fps ):
    d.setFPS( fps )
setFPS( baseFPS )

def which():
    result = None
    if   b.buttonU.justPressed(): result = 'U'
    elif b.buttonD.justPressed(): result = 'D'
    elif b.buttonL.justPressed(): result = 'L'
    elif b.buttonR.justPressed(): result = 'R'
    elif b.buttonA.justPressed(): result = 'A'
    elif b.buttonB.justPressed(): result = 'B'
    b.inputJustPressed()
    return result

def sideScroll( displayString, x, y, w, b, lambdas ):
    if ( 1 + len( displayString ) ) * 6 > w:
        setFPS( sideScrollFPS )
        displayLen = len( displayString ) * 6 + w
        o = b if b > 0 else 0
        pauseStart = 10 if o > 0 else 0
        while True:
            d.drawFilledRectangle( x, y, w, 8, 1 )
            d.drawText( displayString, x + w - o, y, 0 )
            if 'lFill' in lambdas:
                lambdas[ 'lFill' ]()
            d.update()
            b = which()
            if b and b.upper() in lambdas:
                result = lambdas[ b.upper() ]()
                setFPS( baseFPS )
                return result
            if pauseStart > 0:
                pauseStart -= 1
            else:
                o = ( o + 1 ) % displayLen
    elif 'lFill' in lambdas:
        lambdas[ 'lFill' ]()
    d.drawText( displayString, x, y, 0 )
    d.update()
    b = which()
    if b and b in lambdas:
        return lambdas[ b ]()

class Menu:
    def __init__( self, items ):
        self.items = items
        self.count = len( items )
        self.item = 0
        self.action = None

    def a( self ):
        self.action = self.items[ self.item ][ 1 ]
        return True

    def u( self ):
        if self.item > 0:
            self.item = self.item - 1
        return False

    def d( self ):
        if self.item < len( self.items ) - 1:
            self.item = self.item + 1
        return False

    def l( self ):
        return True

    def r( self ):
        item = self.items[ self.item ]
        self.action = item[ 2 if len( item ) > 2 else 1 ]
        return True

    def displayItems( self ):
        return[
            ( None if self.item < 2 else               self.items[ self.item - 2 ][ 0 ] ),
            ( None if self.item < 1 else               self.items[ self.item - 1 ][ 0 ] ),
            (                                          self.items[ self.item     ][ 0 ] ),
            ( None if self.item + 1 >= self.count else self.items[ self.item + 1 ][ 0 ] ),
            ( None if self.item + 2 >= self.count else self.items[ self.item + 2 ][ 0 ] )
        ]

    def display( self ):
        def leftFill():
            d.drawFilledRectangle( 0, 16, 6, 8, 1 )
            d.drawText( '>', 0, 16, 0 )
        self.action = None
        while True:
            d.fill( 1 )
            itemY = 0
            for item in self.displayItems():
                if item:
                    if itemY == 16:
                        curr = item
                    else:
                        d.drawText( item, 6, itemY, 0 )
                itemY = itemY + 8
            if sideScroll(
                curr, 6, 16, d.width, d.width, {
                    'A':     lambda: self.a(),
                    'B':     lambda: True,
                    'U':     lambda: self.u(),
                    'D':     lambda: self.d(),
                    'u':     lambda: self.u(),
                    'd':     lambda: self.d(),
                    'L':     lambda: self.l(),
                    'R':     lambda: self.r(),
                    'lFill': lambda: leftFill()
                }):
                break
        return self.action() if self.action else None

images = {
    'BoxClosed'   : 0,
    'BoxOpen'     : 360,
    'Desk'        : 720,
    'DeskL'       : 1080,
    'DeskM'       : 1440,
    'DeskMSmsh1'  : 1800,
    'DeskMSmsh2'  : 2160,
    'DeskOpen'    : 2520,
    'DeskOpenSm'  : 2880,
    'DeskR'       : 3240,
    'DeskRLock'   : 3600,
    'DeskROpen'   : 3960,
    'Door'        : 4320,
    'DoorM'       : 4680,
    'DoorMNoKey'  : 5040,
    'DoorNoKey'   : 5400,
    'DoorOpen1'   : 5760,
    'DoorOpen2'   : 6120,
    'DoorOpen3'   : 6480,
    'DoorOpen4'   : 6840,
    'Instructions': 7200,
    'Lamp'        : 7560,
    'LampL'       : 7920,
    'LampLFlip'   : 8280,
    'LampLit'     : 8640,
    'LampLLit'    : 9000,
    'LampM'       : 9360,
    'LampMLit'    : 9720,
    'LampR'       : 10080,
    'LampRLit'    : 10440,
    'Sink'        : 10800,
    'SinkL'       : 11160,
    'SinkLHammer' : 11520,
    'SinkLOpen'   : 11880,
    'SinkM'       : 12240,
    'SinkMOpen'   : 12600,
    'SinkR'       : 12960,
    'SinkRTick'   : 13320,
    'SinkRTick3'  : 13680,
    'SinkRTickM'  : 14040,
    'SinkRTock'   : 14400,
    'SinkRTock3'  : 14760,
    'SinkRTockM'  : 15120,
    'SinkTick'    : 15480,
    'SinkTickO'   : 15840,
    'SinkTickOO'  : 16200,
    'SinkTock'    : 16560,
    'SinkTockO'   : 16920,
    'SinkTockOO'  : 17280,
    'Title'       : 17640,
}
images[ 'LampUnlit'  ] = images[ 'Lamp'  ]
images[ 'LampLUnlit' ] = images[ 'LampL' ]
images[ 'LampMUnlit' ] = images[ 'LampM' ]
images[ 'LampRUnlit' ] = images[ 'LampR' ]

sequences = {
    'main': [ 'Door', 'Desk', 'Sink', 'Lamp'        ],
    'Door': [ None, None, 'DoorM', None             ],
    'Desk': [ None, 'DeskL', 'DeskM', 'DeskR', None ],
    'Sink': [ None, 'SinkL', 'SinkM', 'SinkR', None ],
    'Lamp': [ None, 'LampL', 'LampM', 'LampR', None ]
}

states = {
    'Start'          : [ ( 'DoorM', 'Unhook key',        'ClockKey'       ), ( 'DeskL', 'Read diary', 'SeqPt1'         ) ],
    'ClockKey'       : [ ( 'SinkR', 'Wind clock',        'SeqPt2'         ), ( 'DeskL', 'Read diary', 'ClockKeySeqPt1' ) ],
    'SeqPt2'         : [ ( 'DeskL', 'Read diary',        'Sequence'       ) ],
    'ClockKeySeqPt1' : [ ( 'SinkR', 'Wind clock',        'Sequence'       ) ],
    'SeqPt1'         : [ ( 'DoorM', 'Unhook key',        'ClockKeySeqPt1' ) ],
    'Sequence'       : [ ( 'SinkM', 'Open box',          'LightBulb'      ) ],
    'LightBulb'      : [ ( 'LampM', 'Use bulb',          'LampOff'        ) ],
    'LampOff'        : [ ( 'LampM', 'Pull switch',       'Combination'    ) ],
    'Combination'    : [ ( 'DeskR', 'Enter combination', 'SmallKey'       ) ],
    'SmallKey'       : [ ( 'SinkL', 'Unlock cupboard',   'Hammer'         ) ],
    'Hammer'         : [ ( 'DeskM', 'Smash piggy bank',  'DoorKey'        ) ],
    'DoorKey'        : [ ( 'DoorM', 'Unlock door',       'Complete'       ) ],
    'Complete'       : []
}

for state in states:
    states[ state ].append ( ( 'LampL', "Press button", state ) )
    states[ state ].append ( ( 'LampR', 'Look at art',  state ) )
    if state != 'LampOff':
        states[ state ].append ( ( 'LampM', 'Pull switch', state ) )

gameData = {
    'seq'  :      [ 'main', 2 ],
    'state':      'Start',
    'items':      [],
    'bulbFitted': False,
    'lampLit':    False,
    'clockTick':  0,
    'boxOpen':    False,
    'drawOpen':   False,
    'cupbdOpen':  False,
    'pigSmashed': False,
    'film':       False
}

def drawImage( imageName ):
    with open( '/Games/EscapeRoom/images.bin', 'rb' ) as imgFile:
        imgFile.seek( images[ imageName ] )
        d.blit( imgFile.read( 360 ), 0, 0, 72, 40, -1, 0, 0 )

def drawState( times = 1 ):
    seqData = gameData[ 'seq' ]
    imageName = sequences[ seqData[ 0 ] ][ seqData[ 1 ] ]
    for _ in range( times ):
        drawImage( imageName )
        if gameData[ 'film' ]:
            d.drawFilledRectangle( 1, 0, 6, d.height, 0 )
            d.drawLine( 0, 0, 0, d.height, 1 )
            d.drawFilledRectangle( d.width - 7, 0, 6, d.height, 0 )
            rhs = d.width - 1
            d.drawLine( rhs, 0, rhs, d.height, 1 )
            startY = 2 - randrange( 2 )
            for y in range( d.height / 5 ):
                h = y * 5 + startY
                d.drawFilledRectangle( 2, h, 4, 3, 1 )
                d.drawFilledRectangle( d.width - 6, h, 4, 3, 1 )
            for scratch in range( randrange( 5 ) ):
                if scratch > 1:
                    x = randrange( 7, d.width - 7 )
                    d.drawLine( x, 0, x, d.height, 0 )
        d.update()

def drawDup( x1, y1, x2, y2 ):
    d.drawLine( x1, y1, x2, y2, 0 )
    d.drawLine( d.width - x1 - 1, y1, d.width - x2 - 1, y2, 0 )
    d.drawLine( x1, d.height - y1 - 1, x2, d.height - y2 - 1, 0 )
    d.drawLine( d.width - x1 - 1, d.height - y1 - 1, d.width - x2 - 1, d.height - y2 - 1, 0 )

def overlay():
    drawDup( 0, 0, 5, 0 )
    drawDup( 0, 1, 3, 1 )
    drawDup( 0, 2, 2, 2 )
    drawDup( 0, 3, 1, 3 )
    drawDup( 0, 4, 0, 5 )

def playCuckoo():
    audio.play( 523, 500 ) # 12|16| 
    audio.play( 392, 750 ) # 7|16| .
    sleep( 0.5 )           # 7|16| r
    audio.play( 523, 500 ) # 12|16| 
    audio.play( 392, 750 ) # 7|16| .
    sleep( 0.5 )           # 7|16| r
    audio.play( 523, 500 ) # 12|16| 
    audio.play( 392, 750 ) # 7|16| .

def showText( line1, line2 = None, line3 = None ):
    d.fill( 1 )
    d.drawText( line1, 37 - len( line1 ) * 3, 8, 0 )
    if line2:
        d.drawText( line2, 37 - len( line2 ) * 3, 18, 0 )
    if line3:
        d.drawText( line3, 37 - len( line3 ) * 3, 28, 0 )
    overlay()
    if line1 == '"...U,L,R"':
        if inEmulator:
            print( "Emulator detected - cuckoo on the main thread." )
            playCuckoo()
        else:
            start_new_thread( playCuckoo, () )
    b.inputJustPressed()
    while not which():
        d.update()

def cuckoo():
    gameData[ 'film' ] = True
    for _ in range( 3 ):
        images[ 'SinkR' ] = images[ 'SinkRTick' ]
        drawState( 3 )
        images[ 'SinkR' ] = images[ 'SinkRTock' ]
        drawState( 3 )
    images[ 'SinkR' ] = images[ 'SinkRTick3' ]
    drawState( 3 )
    images[ 'SinkR' ] = images[ 'SinkRTock3' ]
    drawState( 3 )
    images[ 'SinkR' ] = images[ 'SinkRTickM' ]
    drawState( 3 )
    images[ 'SinkR' ] = images[ 'SinkRTockM' ]
    drawState( 3 )

def showInventory():
    items = gameData[ 'items' ]
    if items:
        Menu( [ ( 'Inventory:', lambda: None ) ] + [ ( item, lambda: None ) for item in items ] ).display()
    else:
        Menu( [ ( 'Inventory:', lambda: None ), ( 'No items', lambda: None ) ] ).display()

def openBox():
    showText( 'How?' )
    images[ 'temp'  ] = images[ 'SinkM'     ]
    images[ 'SinkM' ] = images[ 'BoxClosed' ]
    drawState()
    seq = 'UDLULR'
    index = 0
    correct = True
    while True:
        btn = which()
        if not btn:
            d.update()
            continue
        if btn == 'A':
            break
        if btn == 'B':
            showInventory()
        elif btn == seq[ index ]:
            index += 1
            if index == len( seq ):
                if correct:
                    gameData[ 'film' ] = True
                    drawState( 3 )
                    images[ 'SinkM' ] = images[ 'BoxOpen' ]
                    drawState( 6 )
                    images[ 'SinkM' ] = images[ 'SinkMOpen' ]
                    gameData[ 'film' ] = False
                    return True
                showText( "Didn't open" )
                break
        else:
            index += 1
            correct = False
            if index == len( seq ):
                showText( "Didn't open" )
                break
        drawState()
    images[ 'SinkM' ] = images[ 'temp' ]
    return False;

def drawDrawBackground():
    drawImage( 'DeskRLock' )

def openDraw():
    numbers = [ 0, 0, 0 ]
    currentIndex = 0
    drawDrawBackground()
    while True:
        d.drawFilledRectangle( 16, 16, 27, 9, 1 )
        d.drawFilledRectangle( 16 + currentIndex * 9, 16, 9, 9, 0 )
        for index, number in enumerate( numbers ):
            d.drawText( str( number ), 18 + index * 9, 17, 1 if index == currentIndex else 0 )
        d.update()
        btn = which()
        if not btn:
            continue
        if btn == 'B':
            return False
        if btn == 'A':
            if numbers == [ 4, 5, 3 ]:
                break;
            else:
                showText( "Doesn't open" )
                drawDrawBackground()
        elif btn == 'U':
            numbers [ currentIndex ] += 1
            if numbers [ currentIndex ] > 9: numbers [ currentIndex ] = 0
        elif btn == 'D':
            numbers [ currentIndex ] -= 1
            if numbers [ currentIndex ] < 0: numbers [ currentIndex ] = 9
        elif btn == 'L':
            currentIndex -= 1
            if currentIndex < 0: currentIndex = 0
        elif btn == 'R':
            currentIndex += 1
            if currentIndex > 2: currentIndex = 2
    gameData[ 'film' ] = True
    drawState( 3 )
    images[ 'DeskR' ] = images[ 'DeskROpen' ]
    drawState( 4 )
    return True

def redHerring():
    gameData[ 'film' ] = True
    tmp = images[ 'LampL' ]
    def flip( t1, t2 ):
        drawState( 2 )
        images[ 'LampL' ] = images[ 'LampLFlip' ]
        drawState( 3 )
        showText( t1, t2 )
        drawState( 2 )
        images[ 'LampL' ] = tmp
        drawState( 2 )
    flip( "I'm a fish  ", '   who sings' )
    flip( "I can't do  ", 'other things' )
    flip( "I'm lovely  ", " & so caring" )
    flip( 'But only a  ', ' red herring' )

def openDoor():
    gameData[ 'film' ] = True
    drawState( 2 )
    images[ 'DoorM' ] = images[ 'DoorOpen1' ]
    drawState( 2 )
    images[ 'DoorM' ] = images[ 'DoorOpen2' ]
    drawState( 2 )
    images[ 'DoorM' ] = images[ 'DoorOpen3' ]
    drawState( 10 )
    showText( '', 'Freedom!' )
    gameData[ 'film' ] = False
    images[ 'DoorM' ] = images[ 'DoorOpen4' ]
    b.inputJustPressed()
    while not which():
        drawState()

def makeTransition( title, nextState ):
    bigKey   = 'Big key'
    smallKey = 'Small key'
    tinyKey  = 'Tiny key'
    seqPt1   = '"U,D,L..."'
    seqPt2   = '"...U,L,R"'
    bulb     = 'Bulb'
    hammer   = 'Hammer'
    success = True
    isItem = True
    textToShow = None
    if title == 'Unhook key':
        images[ 'Door' ]  = images[ 'DoorNoKey']
        images[ 'DoorM' ] = images[ 'DoorMNoKey']
        gameData[ 'items' ].append( smallKey )
        textToShow = 'Small key'
    elif title == 'Wind clock':
        gameData[ 'items' ].remove( smallKey )
        cuckoo()
        gameData[ 'items' ].append( seqPt2 )
        gameData[ 'clockTick' ] = 1
        isItem = False
        textToShow = seqPt2
    elif title == 'Read diary':
        gameData[ 'items' ].append( seqPt1 )
        isItem = False
        textToShow = seqPt1
    elif title == 'Open box':
        success = openBox()
        if success:
            gameData[ 'items' ].remove( seqPt1 )
            gameData[ 'items' ].remove( seqPt2 )
            gameData[ 'items' ].append( bulb )
            textToShow = 'Light bulb'
            gameData[ 'boxOpen' ] = True
    elif title == 'Use bulb':
        gameData[ 'items' ].remove( bulb )
        textToShow = 'Bulb is in'
        isItem = False
        gameData[ 'bulbFitted' ] = True
    elif title == 'Pull switch':
        textToShow = 'CLICK!'
        isItem = False
        if gameData[ 'bulbFitted' ]:
            if not gameData[ 'lampLit' ]:
                images[ 'Lamp'  ] = images[ 'LampLit'  ]
                images[ 'LampL' ] = images[ 'LampLLit' ]
                images[ 'LampM' ] = images[ 'LampMLit' ]
                images[ 'LampR' ] = images[ 'LampRLit' ]
                gameData[ 'lampLit' ] = True
            else:
                images[ 'Lamp'  ] = images[ 'LampUnlit'  ]
                images[ 'LampL' ] = images[ 'LampLUnlit' ]
                images[ 'LampM' ] = images[ 'LampMUnlit' ]
                images[ 'LampR' ] = images[ 'LampRUnlit' ]
                gameData[ 'lampLit' ] = False
    elif title == 'Enter combination':
        success = openDraw()
        if success:
            gameData[ 'items' ].append( tinyKey )
            images[ 'Desk' ] = images[ 'DeskOpen' ]
            gameData[ 'drawOpen' ] = True
            textToShow = tinyKey
    elif title == 'Unlock cupboard':
        gameData[ 'film' ] = True
        drawState( 3 )
        gameData[ 'items' ].remove( tinyKey )
        images[ 'SinkL' ] = images[ 'SinkLHammer' ]
        drawState( 4 )
        images[ 'SinkL' ] = images[ 'SinkLOpen' ]
        gameData[ 'items' ].append( hammer )
        gameData[ 'cupbdOpen' ] = True
        textToShow = hammer
    elif title == 'Smash piggy bank':
        gameData[ 'film' ] = True
        drawState( 3 )
        images[ 'DeskM' ] = images[ 'DeskMSmsh1' ]
        drawState( 2 )
        images[ 'DeskM' ] = images[ 'DeskMSmsh2' ]
        images[ 'Desk'  ] = images[ 'DeskOpenSm' ]
        drawState( 4 )
        gameData[ 'items' ].remove( hammer )
        gameData[ 'items' ].append( bigKey )
        gameData[ 'pigSmashed' ] = True
        textToShow = bigKey
    elif title == 'Unlock door':
        openDoor()
    elif title == "Press button":
        if gameData[ 'lampLit' ]:
            redHerring()
        else:
            textToShow = "What button?"
            isItem = False
    elif title == 'Look at art':
        if gameData[ 'lampLit' ]:
            gameData[ 'film' ] = True
            drawState( 12 )
            textToShow = 'Nice shapes'
        else:
            textToShow = 'Too dark'
        isItem = False
    else:
        raise Exception( 'Unexpected transition: ' + title )
    if textToShow:
        if isItem:
            showText( 'Item:', textToShow )
        else:
            showText( textToShow )
    if success:
        gameData[ 'state' ] = nextState

def nothingText():
    seqData = gameData[ 'seq' ]
    image = sequences[ seqData[ 0 ] ][ seqData[ 1 ] ]
    if image == 'DoorM':
        return 'Door is locked'
    if image == 'DeskL':
        return 'You already read the diary'
    if image == 'DeskM':
        return 'Piggy bank is smashed' if gameData[ 'pigSmashed' ] else 'Piggy bank - rattles when shaken'
    if image == 'DeskR':
        return 'Draw is empty' if gameData[ 'drawOpen' ] else 'Draw has a combination lock'
    if image == 'SinkL':
        return 'Cupboard is empty' if gameData[ 'cupbdOpen' ] else 'Cupboard is locked'
    if image == 'SinkM':
        return 'The box is empty' if gameData[ 'boxOpen' ] else 'Locked box under sink'
    if image == 'SinkR':
        return 'Clock is ticking' if gameData[ 'clockTick' ] > 0 else "Clock has stopped just before 3 o'clock"
    return 'Nothing to do here'

def handleInput():
    gameData[ 'film' ] = False
    key = which()
    seqData = gameData[ 'seq' ]
    oldImg = sequences[ seqData[ 0 ] ][ seqData[ 1 ] ]
    if key == 'L':
        seqData[ 1 ] = seqData[ 1 ] - 1
        seqData[ 1 ] = seqData[ 1 ] % len( sequences[ seqData[ 0 ] ] )
        if not sequences[ seqData[ 0 ] ][ seqData[ 1 ] ]:
            gameData[ 'seq' ] = [ 'main', gameData[ 'mainIndex' ] ]
    elif key == 'R':
        seqData[ 1 ] = seqData[ 1 ] + 1
        seqData[ 1 ] = seqData[ 1 ] % len( sequences[ seqData[ 0 ] ] )
        if not sequences[ seqData[ 0 ] ][ seqData[ 1 ] ]:
            gameData[ 'seq' ] = [ 'main', gameData[ 'mainIndex' ] ]
    elif key == 'U':
        if seqData[ 0 ] == 'main':
            gameData[ 'mainIndex' ] = seqData[ 1 ]
            gameData[ 'seq' ] = [ oldImg, 2 ]
    elif key == 'D':
        if seqData[ 0 ] != 'main':
            gameData[ 'seq' ] = [ 'main', gameData[ 'mainIndex' ] ]
    elif key == 'A':
        if seqData[ 0 ] == 'main':
            gameData[ 'mainIndex' ] = seqData[ 1 ]
            gameData[ 'seq' ] = [ oldImg, 2 ]
        else:
            menuItems = []
            def makeTransitionLambda( title, nextState ):
                return lambda: makeTransition( title, nextState )
            for stateInfo in states[ gameData[ 'state' ] ]:
                if stateInfo[ 0 ] == oldImg:
                    menuItems.append( ( stateInfo[ 1 ], makeTransitionLambda( stateInfo[ 1 ], stateInfo[ 2 ] ) ) )
            if not menuItems:
                menuItems.append( ( nothingText(), lambda: None ) )
            Menu ( menuItems ).display()
    elif key == 'B':
        showInventory()
    clockTick = gameData[ 'clockTick' ]
    if clockTick > 0:
        if clockTick % 6 == 0:
            images[ 'SinkR' ] = images[ 'SinkRTick3']
            if gameData[ 'cupbdOpen' ]:
                images[ 'Sink' ] = images[ 'SinkTickOO' ]
            elif gameData[ 'boxOpen' ]:
                images[ 'Sink' ] = images[ 'SinkTickO' ]
            else:
                images[ 'Sink' ] = images[ 'SinkTick' ]
        elif clockTick % 3 == 0:
            images[ 'SinkR' ] = images[ 'SinkRTock3']
            if gameData[ 'cupbdOpen' ]:
                images[ 'Sink' ] = images[ 'SinkTockOO' ]
            elif gameData[ 'boxOpen' ]:
                images[ 'Sink' ] = images[ 'SinkTockO' ]
            else:
                images[ 'Sink' ] = images[ 'SinkTock' ]
        gameData[ 'clockTick' ] = clockTick + 1

try:
    drawImage( 'Title' )
    while not which():
        d.update()
    showText( 'How are you', 'stuck in', 'this room?' )
    showText( 'And,', 'more', 'importantly,' )
    showText( 'How will you', '', 'ESCAPE?' )
    showText( 'UDLR:move', 'A:menu/act', 'B:items/cncl' )
    while gameData[ 'state' ] != 'Complete':
        drawState()
        handleInput()
except Exception as x:
    if inEmulator:
        print_exception( x )
    else:
        with open( '/Games/EscapeRoom/crashdump.log', 'w', encoding = "utf-8" ) as f:
            print_exception( x, f )
    d.fill( 0 )
    d.drawText( "Oops - died", 3,  8, 1 )
    d.drawText( "Problem was:", 0, 22, 1 )
    sideScroll( str( x ), 0, 30, d.width, -1, {
        'A': lambda: True,
        'B': lambda: True
    } )
