from thumbyGraphics import display as d
import thumbyButton as b
from sys import print_exception
from random import randrange, randint
from time import sleep
from thumbyAudio import audio
from thumbyHardware import reset
from sys import path
if not '/Games/EscapeRoom2' in path:
  path.append( '/Games/EscapeRoom2' )
from Morse import parseMorse

DIR = '/Games/EscapeRoom2/'

inEmulator = True
try:
    import emulator
except ImportError:
    inEmulator = False

baseFPS = 4
sideScrollFPS = 45
portholeFPS = 8
def setFPS( fps ):
    d.setFPS( fps )
    return True
setFPS( baseFPS )
def setPortholeFPS():
    setFPS( portholeFPS )

def noise( length ):
    for _ in range( length ):
        audio.playBlocking( randint( 400, 500 ), 10 )

def buzz():
    d.display.invert( 1 )
    d.update()
    noise( 10 )
    d.display.invert( 0 )
    d.update()
    noise( 12 )

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

def sideScroll( displayString, fg, x, y, w, b, lambdas ):
    if ( 1 + len( displayString ) ) * 6 > w:
        setFPS( sideScrollFPS )
        displayLen = len( displayString ) * 6 + w
        o = b if b > 0 else 0
        pauseStart = 10 if o > 0 else 0
        while True:
            d.drawFilledRectangle( x, y, w, 8, 1 if fg == 0 else 0 )
            d.drawText( displayString, x + w - o, y, fg )
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
    d.drawText( displayString, x, y, fg )
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

    def displayItems( self, itemCount ):
        result = []
        if itemCount > 3:
            result.append( None if self.item < 2 else               self.items[ self.item - 2 ][ 0 ] )
        result.append    ( None if self.item < 1 else               self.items[ self.item - 1 ][ 0 ] )
        result.append    (                                          self.items[ self.item     ][ 0 ] )
        result.append    ( None if self.item + 1 >= self.count else self.items[ self.item + 1 ][ 0 ] )
        if itemCount > 3:
            result.append( None if self.item + 2 >= self.count else self.items[ self.item + 2 ][ 0 ] )
        return result

    def display( self, offset = 0, itemCount = 5, underlayRenderer = None ):
        fg = 1 if gameData[ 'state' ] == 'dark' else 0
        bg = 0 if gameData[ 'state' ] == 'dark' else 1
        def leftFill():
            d.drawFilledRectangle( offset, 16, 6, 8, bg )
            d.drawText( '>', offset, 16, fg )
        self.action = None
        while True:
            if underlayRenderer:
                underlayRenderer()
            else:
                d.fill( bg )
            itemY = ( 5 - itemCount ) * 4
            for item in self.displayItems( itemCount ):
                if item:
                    if itemY == 16:
                        curr = item
                    else:
                        d.drawText( item, offset + 6, itemY, fg )
                itemY = itemY + 8
            if sideScroll(
                curr, fg, offset + 6, 16, d.width, d.width, {
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
    'Bridge1':                 0,
    'Bridge2':               360,
    'ComputerRoom':          720,
    'ComputerRoom_dark':    1080,
    'Computer_Ctrl':        1440,
    'Computer_Doc':         1800,
    'Computer_Off':         2160,
    'ControlPanel0':        2520,
    'ControlPanel1':        2880,
    'ControlPanel2':        3240,
    'ControlPanel3':        3600,
    'ControlPanel4':        3960,
    'ControlProgram0':      4320,
    'ControlProgram1':      4680,
    'ControlProgram2':      5040,
    'ControlProgram3':      5400,
    'ControlProgramCode':   5760,
    'ControlProgram_Open':  6120,
    'ControlProgram_Open1': 6480,
    'ControlProgram_Shut':  6840,
    'Corridor_Bridge':      7200,
    'Corridor_Galley':      7560,
    'Corridor_RadioRoom':   7920,
    'DocBackground':        8280,
    'DocInstructions':      8640,
    'Document0':            9000,
    'Document1':            9360,
    'Document2':            9720,
    'Document3':           10080,
    'DrawCode':            10440,
    'FishPicture1':        10800,
    'FishPicture2':        11160,
    'FishPicture3':        11520,
    'FishPicture4':        11880,
    'Galley':              12240,
    'Galley2':             12600,
    'Galley3':             12960,
    'Hatch':               13320,
    'Hatch1':              13680,
    'Hatch2':              14040,
    'Hatch3':              14400,
    'Hatch4':              14760,
    'Hatch5':              15120,
    'Hatch6':              15480,
    'Hatch7':              15840,
    'MorseSheet':          16200,
    'MorseSheetBack':      16560,
    'Outside':             16920,
    'Periscope0':          17280,
    'Periscope1':          17640,
    'Periscope2':          18000,
    'Periscope3':          18360,
    'Periscope4':          18720,
    'Periscope5':          19080,
    'RadioRoom':           19440,
    'RadioRoom2':          19800,
    'Rescue0':             20160,
    'Rescue1':             20520,
    'Rescue2':             20880,
    'SteamyPorthole':      21240,
    'Title':               21600,
    'UnderComputer':       21960,
    'UnderComputer2':      22320,
}
images[ 'Bridge' ] = images[ 'Bridge1' ]
images[ 'Document' ] = images[ 'Document0' ]
images[ 'ControlProgram' ] = images[ 'ControlProgram0' ]

def climbOut():
    if gameData[ 'state' ] == 'trapped':
        showText( 'The hatch', 'is shut.' )
        return False
    showTextOnce( 'You climb', 'out of the', 'hatch,' )
    showTextOnce( 'wondering', 'where you', 'are..' )
    return True

movements = {
    'ComputerRoom': {
        'U': ( 'Corridor_RadioRoom', lambda: showTextOnce( 'You climb', 'up to a', 'corridor' ) ),
        'D': ( 'UnderComputer',      lambda: showTextOnce( 'Anything', 'under the', 'desk?' ) ),
        'L': ( 'ComputerRoom',       lambda: showText( "There's a", 'wall to', 'the left' ) ),
        'R': ( 'ComputerRoom',       lambda: showText( "There's a", 'wall to', 'the right' ) ),
    },
    'UnderComputer': {
        'U': ( 'ComputerRoom',  lambda: True ),
        'D': ( 'UnderComputer', lambda: showText( 'You are as', 'far down as', 'you can go' ) ),
        'L': ( 'UnderComputer', lambda: showText( 'No room to', 'move under', 'here' ) ),
        'R': ( 'UnderComputer', lambda: showText( 'No room to', 'move under', 'here' ) ),
    },
    'Corridor_RadioRoom': {
        'D': ( 'ComputerRoom',    lambda: True ),
        'U': ( 'RadioRoom',       lambda: True ),
        'L': ( 'Corridor_Galley', lambda: True ),
        'R': ( 'Corridor_Bridge', lambda: True ),
    },
    'RadioRoom': {
        'D': ( 'Corridor_RadioRoom', lambda: setFPS( baseFPS ) ),
    },
    'Corridor_Galley': {
        'R': ( 'Corridor_RadioRoom', lambda: True                                                ),
        'L': ( 'Corridor_Galley',    lambda: showText( 'Door marked', 'RESTRICTED:', 'ARMOURY' ) ),
        'U': ( 'Galley',             lambda: True                                                ),
    },
    'Galley': {
        'D': ( 'Corridor_Galley', lambda: setFPS( baseFPS ) ),
    },
    'Corridor_Bridge': {
        'L': ( 'Corridor_RadioRoom', lambda: True ),
        'R': ( 'Corridor_Bridge',    lambda: showText( 'Door marked', 'RESTRICTED:', 'ENGINE ROOM' ) ),
        'U': ( 'Bridge',             lambda: True ),
    },
    'Bridge': {
        'U': ( 'Hatch',           lambda: True ),
        'D': ( 'Corridor_Bridge', lambda: True ),
    },
    'Hatch': {
        'U': ( 'Outside', climbOut     ),
        'D': ( 'Bridge',  lambda: True ),
    },
    'Outside': {
        'D': ( 'Hatch',  lambda: True ),
    },
}

class Action:
    def __init__( self, title, prerequisite, effect, afterwards = None ):
        self.title        = title
        self.prerequisite = prerequisite
        self.effect       = effect
        self.afterwards   = afterwards

    def menuItem( self ):
        return ( self.title, lambda: self.execute() )

    def execute( self ):
        result = self.effect()
        if self.afterwards:
            self.afterwards()
        return result

def transition( imageName, intermediate = None ):
    doTransition = True
    if intermediate:
        doTransition = intermediate()
    if doTransition:
        gameData[ 'image' ] = imageName

def findLight():
    showText( 'You can', 'feel a', 'pull switch' )
    gameData[ 'lightswitch' ] = True

def lightOn():
    gameData[ 'film' ] = True
    drawState( 3 )
    audio.playBlocking( 3000, 5 )
    gameData[ 'image' ] = 'ComputerRoom'
    drawState( 4 )
    gameData[ 'film' ] = False
    gameData[ 'state' ] = 'trapped'
    return True

def lightOff():
    gameData[ 'film' ] = True
    drawState( 3 )
    audio.playBlocking( 3000, 5 )
    gameData[ 'image' ] = 'ComputerRoom_dark'
    drawState( 4 )
    gameData[ 'film' ] = False
    gameData[ 'state' ] = 'dark'
    return True

def lookAroundComputerRoom():
    showText( 'There is a', 'desk, a', 'computer,' )
    showText( 'a painting', 'of some', 'flowers,' )
    showText( 'a light', 'switch, and', 'a ladder.' )
    gameData[ 'looked' ].append( 'Comp' )

def readDocument():
    gameData[ 'image' ] = 'Document'
    while True:
        drawState()
        btn = which()
        if not btn:
            continue
        if btn in 'AB':
            return
        if btn in 'UD':
            if btn == 'U':
                gameData[ 'docPage' ] -= 1
                if gameData[ 'docPage' ] < 0: gameData[ 'docPage' ] = 0
            else:
                gameData[ 'docPage' ] += 1
                if gameData[ 'docPage' ] > 3: gameData[ 'docPage' ] = 3
            images[ 'Document' ] = images[ 'Document' + str( gameData[ 'docPage' ] ) ]
            drawState()

def useControlProgram():
    gameData[ 'image' ] = 'ControlProgram'
    while True:
        drawState()
        btn = which()
        if btn == 'A':
            if images[ 'ControlProgram' ] in [ images[ 'ControlProgram0' ], images[ 'ControlProgram2' ] ]:
                openCloseHatch()
            else:
                return
        elif btn == 'U' and images[ 'ControlProgram' ] in [ images[ 'ControlProgram1' ], images[ 'ControlProgram3' ] ]:
            images[ 'ControlProgram' ] = images[ 'ControlProgram2' if gameData[ 'unlocked' ] else 'ControlProgram0' ]
        elif btn == 'D' and images[ 'ControlProgram' ] in [ images[ 'ControlProgram0' ], images[ 'ControlProgram2' ] ]:
            images[ 'ControlProgram' ] = images[ 'ControlProgram3' if gameData[ 'unlocked' ] else 'ControlProgram1' ]

def useComputer():
    showTextOnce( 'Computer', 'displays', 'some icons' )
    gameData[ 'image' ] = 'Computer_Doc'
    drawState()
    while True:
        btn = which()
        if btn == 'B':
            showText( 'Computer', 'is off.' )
            gameData[ 'image' ] = 'ComputerRoom'
            break
        elif btn == 'A':
            if gameData[ 'image' ] == 'Computer_Doc':
                if openDocument():
                    readDocument()
                    gameData[ 'image' ] = 'Computer_Doc'
            elif gameData[ 'image' ] == 'Computer_Ctrl':
                if startControlProgram():
                    useControlProgram();
                    gameData[ 'image' ] = 'Computer_Ctrl'
            else:
                showTextOnce( 'Computer', 'is off' )
                return True
        elif btn == 'L':
            if gameData[ 'image' ] == 'Computer_Ctrl':
                gameData[ 'image' ] = 'Computer_Doc'
            elif gameData[ 'image' ] == 'Computer_Off':
                gameData[ 'image' ] = 'Computer_Ctrl'
        elif btn == 'R':
            if gameData[ 'image' ] == 'Computer_Ctrl':
                gameData[ 'image' ] = 'Computer_Off'
            elif gameData[ 'image' ] == 'Computer_Doc':
                gameData[ 'image' ] = 'Computer_Ctrl'
        drawState()

def openDocument():
    if gameData[ 'docDecrypted' ]: return True
    drawImage( 'DocInstructions' )
    while not which():
        d.update()
    colours = ""
    while len( colours ) < 4:
        choice = Menu( [
            ( 'Black',  lambda: 'K' ),
            ( 'White',  lambda: 'W' ),
            ( 'Red',    lambda: 'R' ),
            ( 'Orange', lambda: 'O' ),
            ( 'Yellow', lambda: 'Y' ),
            ( 'Green',  lambda: 'G' ),
            ( 'Blue',   lambda: 'B' ),
            ( 'Indigo', lambda: 'I' ),
            ( 'Violet', lambda: 'V' ),
            ( 'Silver', lambda: 'S' ),
            ( 'Gold',   lambda: 'D' ),
        ] ).display( 12, 3, lambda: drawImage( 'DocBackground' ) )
        if not choice: return False
        colours += choice
        drawImage( 'DocBackground' )
        d.update()
    if colours == "RBYD":
        gameData[ 'docDecrypted' ] = True
        return True
    buzz()
    showText( 'Incorrect', 'colours', background = lambda _ : drawImage( 'DocBackground' ) )
    return False

def startControlProgram():
    if gameData[ 'morseEntered' ]: return True
    result = enterCode( 'ControlProgramCode', 23, 21, [ 0, 0, 0 ], [ 4, 10, 14 ], 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' )
    if result:
        gameData[ 'morseEntered' ] = True
    else:
        buzz()
        showText( 'Incorrect', 'code', background = lambda _ : drawImage( 'DocBackground' ) )
    return result

def openCloseHatch():
    tmp = gameData[ 'image' ]
    showText( 'You hear a', 'metallic', 'sound...' )
    if gameData[ 'unlocked' ]:
        gameData[ 'image' ] = 'ControlProgram_Shut'
    else:
        gameData[ 'image' ] = 'ControlProgram_Open1' if gameData[ 'surfaced' ] else 'ControlProgram_Open'
    gameData[ 'unlocked' ] = not gameData[ 'unlocked' ]
    gameData[ 'film' ] = True
    drawState( 7 )
    gameData[ 'film' ] = False
    gameData[ 'image' ] = tmp
    images[ 'ControlProgram' ] = images[ 'ControlProgram2' if gameData[ 'unlocked' ] else 'ControlProgram0' ]
    return True

def takeScissors():
    gameData[ 'items' ].append( 'Scissors' )
    images[ 'UnderComputer' ] = images[ 'UnderComputer2' ]
    return showText( 'Item:', 'Scissors' )

def lookAroundGalley():
    showText( "There's an", 'oven & sink,', 'cupboards,' )
    showText( 'and things', 'for making', 'cups of tea' )
    gameData[ 'looked' ].append( 'Galley' )

def lookInOven():
    showText( "It's empty", '(needs ', 'cleaning)' ),
    gameData[ 'looked' ].append( 'oven' )

def lookInSink():
    showText( 'There is', 'a plug.' ),
    showText( 'What did', 'you expect', 'in there?' ),
    gameData[ 'looked' ].append( 'sink' )

def lookInCupboards():
    showText( 'They seem', 'empty,', 'but...' )
    showText( 'in the last', 'one you find', 'something.' )
    showText( 'Item:', 'Torn paper' )
    gameData[ 'items' ].append( 'Torn paper' )
    gameData[ 'looked' ].append( 'cupboards' )

def kettleOn():
    showText( 'You fill the', 'kettle and', 'switch it on' )
    gameData[ 'kettle' ] = 40

def teaCaddy():
    showText( 'You take a', 'mug from', 'the shelf...' )
    gameData[ 'film' ] = True
    drawState( 10 )
    images[ 'Galley' ] = images[ 'Galley2' ]
    drawState( 10 )
    gameData[ 'film' ] = False
    showText( 'You open', 'the tea', 'caddy.' )
    showText( 'Something', 'is inside...' )
    showText( 'Item:', 'key marked', '"R"' )
    gameData[ 'items' ].append( 'Right key' )
    return True

def lookAtSteamyWindow():
    showText( 'The steam', 'from the', 'kettle...' )
    showText( 'revealed', 'some writing', 'on the glass' )
    gameData[ 'film' ] = True
    gameData[ 'image' ] = 'SteamyPorthole'
    drawState( 20 )
    gameData[ 'film' ] = False
    showText( 'Item:', 'Steam number', '3972' )
    gameData[ 'items' ].append( 'Steam number 3972' )
    gameData[ 'image' ] = 'Galley'

def lookAroundRadioRoom():
    showText( 'There is a', 'painting', 'of flowers,' )
    showText( 'a handle of', 'some sort', 'on a string,' )
    showText( 'some radio', 'equipment', '(smoking),' )
    showText( 'and a Morse', 'code key', 'with a box.' )
    gameData[ 'looked' ].append( 'RadioRoom' )

def readTornPaper():
    oldImage = gameData[ 'image' ]
    showTextOnce( "It's part of", 'a Morse code', 'chart, torn.' )
    gameData[ 'image' ] = 'MorseSheet'
    gameData[ 'film' ] = True
    drawState( 9 )
    gameData[ 'film' ] = False
    drawState()
    while not which():
        d.update()
    gameData[ 'image' ] = oldImage

def turnTornPaper():
    oldImage = gameData[ 'image' ]
    showTextOnce( 'There is', 'something', 'on the back' )
    gameData[ 'image' ] = 'MorseSheetBack'
    gameData[ 'film' ] = True
    drawState( 9 )
    gameData[ 'film' ] = False
    drawState()
    while not which():
        d.update()
    gameData[ 'image' ] = oldImage

def sendMorse():
    gameData[ 'image' ] = 'MorseSheet'
    drawState()
    counter = 0
    pressed = False;
    timings = []
    setFPS( 50 )
    while True:
        wasPressed = pressed
        pressed = b.buttonA.pressed()
        if pressed != wasPressed:
            if wasPressed:
                audio.stop()
            else:
                audio.play( 784, 2147483647 )
            timings.append( counter )
            counter = 0
        d.update()
        counter += 1
        if ( not pressed and counter > 50 and len( timings ) > 0 ) or 'B' == which():
            timings.append( counter )
            break
    audio.stop()
    setFPS( baseFPS )
    showTextOnce( 'A paper', 'prints out', 'a record' )
    letters = parseMorse( timings ).replace( ' ', '' )
    showText( '------------', letters, '------------' )
    if 'AMN' == letters:
        showText( 'There is a', 'pause...')
        showText( '...then you', 'hear a', 'reply')
        drawState()
        for length in [ 1, -4, 3, -1, 1, -1, 3, -4, 3, -1, 3, -1, 3, -7  ]:
            if length > 0:
                audio.playBlocking( 831, length * 50 )
            else:
                sleep( abs( length ) / 10 )
        showText( 'Did you', 'get that?')
        showText( 'Luckily it', 'prints out:' )
        showText( '------------', 'EKO', '------------' )
        showText( 'Item:', 'Morse print', 'EKO' )
        gameData[ 'items' ].append( 'Morse print: EKO' )
    else:
        showText( 'Nothing', 'happens' )
    gameData[ 'image' ] = 'RadioRoom'
    setPortholeFPS()

def useMorseKey():
    showText( 'The key is', 'labelled...' )
    showText( '"Send call', 'sign, await', 'response."' )
    if 'Handle' in gameData[ 'items' ]:
        if 'Torn paper' in gameData[ 'items' ]:
            showText( 'You wind the', 'handle, then', 'tap' )
            showTextOnce( 'Press A for', 'dot, hold A', 'for dash' )
            showTextOnce( 'Pause', 'between', 'letters' )
            sendMorse()
        else:
            showText( 'You need', 'to learn', 'Morse code!' )
    else:
        showText( 'Nothing', 'happens. The', 'Morse key' )
        showText( 'has a', 'power pack', 'that needs' )
        showText( 'winding up.', "There's", 'no handle.' )

def useRadio():
    showText( 'The radio', 'equipment', 'is broken.' )
    showText( 'Smoke is', 'coming out.', 'Looks bad.' )
    gameData[ 'looked' ].append( 'radio' )

def takeHandle():
    if 'Scissors' in gameData[ 'items' ]:
        showText( "It's handy", 'having some', 'scissors' )
        showText( 'You cut the', 'string' )
        gameData[ 'items' ].append( 'Handle' )
        images[ 'RadioRoom' ] = images[ 'RadioRoom2' ]
        showText( 'Item:', 'Handle' )
    else:
        showText( 'String tied', 'too tight', 'to undo' )
    return 'Scissors' in gameData[ 'items' ]

def lookAroundBridge():
    showText( "There's a", 'lot of dials', 'and meters,' )
    showText( 'a control', 'panel (off),', ' a ladder,' )
    showText( 'a periscope', '(down),' )
    showText( '& a locked', 'draw with a', 'combination' )
    gameData[ 'looked' ].append( 'Bridge' )

def periscope( dir ):
    if 'up' == dir:
        showTextOnce( 'Periscope', 'comes up &', 'you look' )
        if gameData[ 'surfaced' ]:
            for index in range( 3, 6 ):
                gameData[ 'image' ] = 'Periscope' + str( index )
                drawState( 3 )
            showTextOnce( 'You see', 'a small', 'island' )
            showTextOnce( 'and lots', 'of empty', 'sea' )
        else:
            gameData[ 'film' ] = True
            for index in range( 3 ):
                gameData[ 'image' ] = 'Periscope' + str( index )
                drawState( 3 )
            gameData[ 'film' ] = False
            showTextOnce( 'You see', 'a red', 'herring' )
            showTextOnce( 'Must not be', 'near the', 'surface?' )
        images[ 'Bridge' ] = images[ 'Bridge2' ]
    else:
        showTextOnce( 'Periscope', 'goes down' )
        images[ 'Bridge' ] = images[ 'Bridge1' ]
    gameData[ 'periscope' ] = dir
    gameData[ 'image' ] = 'Bridge'

def useControlPanel():
    gameData[ 'film' ] = True
    gameData[ 'image' ] = 'ControlPanel0'
    drawState( 5 )
    gameData[ 'film' ] = False
    showTextOnce( 'Oh dear.', "What's that", 'language?' )
    showText( 'Careful', 'now' )
    while True:
        drawState()
        btn = which()
        if not btn:
            continue
        if btn == 'B':
            break
        if gameData[ 'image' ] == 'ControlPanel0':
            if btn == 'A':
                gameData[ 'image' ] = 'ControlPanel2'
            elif btn == 'U':
                gameData[ 'image' ] = 'ControlPanel3'
            elif btn == 'D':
                gameData[ 'image' ] = 'ControlPanel4'
        elif gameData[ 'image' ] == 'ControlPanel1':
            if btn == 'A':
                showText( 'Sirens wail', 'and lights', 'go out...' )
                showText( 'Detonations', 'shake the', 'walls...' )
                showText( 'Water pours', 'in around', 'you...' )
                showText( 'You might', 'have chosen', 'unwisely.')
                reset()
            elif btn == 'R':
                gameData[ 'image' ] = 'ControlPanel2'
        elif gameData[ 'image' ] == 'ControlPanel2':
            if btn == 'A':
                gameData[ 'image' ] = 'ControlPanel0'
            elif btn == 'L':
                gameData[ 'image' ] = 'ControlPanel1'
        elif gameData[ 'image' ] == 'ControlPanel3':
            if btn == 'A':
                if gameData[ 'surfaced' ]:
                    if gameData[ 'state' ] == 'opened':
                        showText( 'As you', 'submerge', 'you think' )
                        showText( '"The hatch', 'is still', 'open."' )
                        showText( 'Water pours', 'down on you.' )
                        showText( 'You might', 'have chosen', 'unwisely.')
                        reset()
                    else:
                        showText( 'Machinery', 'starts', 'again.' )
                        showText( 'Then there', 'is a', 'grinding' )
                        showText( 'and all is', 'quiet and', 'still' )
                else:
                    showText( 'Nothing', 'happens' )
            elif btn == 'D':
                gameData[ 'image' ] = 'ControlPanel0'
        elif gameData[ 'image' ] == 'ControlPanel4':
            if btn == 'A':
                if gameData[ 'surfaced' ]:
                    showText( 'Nothing', 'happens' )
                else:
                    showText( 'Machinery', 'clanks and', 'whirrs.' )
                    showText( 'You feel', 'the floor', 'shake.' )
                    showText( "You've made", 'this thing', 'move!' )
                    showText( 'After a', 'while, all', 'is quiet' )
                    showText( 'But the', 'floor still', 'rocks a bit' )
                    gameData[ 'surfaced' ] = True
            elif btn == 'U':
                gameData[ 'image' ] = 'ControlPanel0'
    gameData[ 'image' ] = 'Bridge'

def takeControlPanelNote():
    if 'Control panel note' not in gameData[ 'items' ]:
        showText( 'Someone', 'left a', 'note...' )
        showText( 'Item:', 'Control', 'panel note' )
        gameData[ 'items' ].append( 'Control panel note' )

def controlPanel():
    items = gameData[ 'items' ]
    if 'Left key' in items:
        if 'Right key' in items:
            showText( 'You insert', 'the keys in', 'the panel.' )
            showText( 'The panel', 'comes on.' )
            useControlPanel()
        else:
            showTextOnce( 'Key L fits', 'on the left' )
            showText( 'You need', 'another', 'key' )
            takeControlPanelNote()
    else:
        if 'Right key' in items:
            showTextOnce( 'Key R fits', 'on the right' )
            showText( 'You need', 'another', 'key' )
        else:
            showText( "There's a", 'pair of', 'keyholes.')
            showText( 'You have', 'no keys' )
            takeControlPanelNote()

def readControlPanelNote():
    showText( '"Security:', 'requires', 'cup of tea"' )
    showTextOnce( 'Hmm...', 'Strange.' )
    gameData[ 'seenNote' ] = True

def openDraw():
    result = enterCode( 'DrawCode', 12, 17, [ 0, 0, 0, 0 ], [ 3, 9, 7, 2 ], '0123456789' )
    if result:
        showText( 'Item:', 'key marked', '"L"' )
        showText( 'You shut', 'the draw' )
        gameData[ 'items' ].append( 'Left key' )
    else:
        showText( 'The draw', "doesn't", 'open.' )
    return result

def lookAroundHatch():
    showText( 'The hatch', 'above your', 'head has' )
    showText( 'a handle', 'to open & a', 'tiny display' )
    gameData[ 'looked' ].append( 'Hatch' )

def lookAtHatch():
    showTextOnce( 'The display', 'says:' )
    if gameData[ 'unlocked' ]:
        if gameData[ 'surfaced' ]:
            if gameData[ 'state' ] == 'opened':
                showText( '"OPEN"' )
            else:
                showText( '"ACTIVE"' )
        else:
            showText( '"SUBMERGED"' )
    else:
        if gameData[ 'surfaced' ]:
            showText( '"LOCKED"' )
        else:
            showText( '"LOCKED & ', 'SUBMERGED"' )

def turnHatchHandle():
    if gameData[ 'unlocked' ] and gameData[ 'surfaced' ]:
        showText( 'The handle', 'needs', 'oiling.' )
        showText( 'There is a', 'sound of', 'scraping.' )
        gameData[ 'film' ] = True
        drawState( 3 )
        images[ 'Hatch' ] = images[ 'Hatch2' ]
        for index in range( 1, 3 ):
            images[ 'Hatch' ] = images[ 'Hatch' + str( index ) ]
            drawState( 3 )
        showText( 'Then the', 'hatch', 'opens...' )
        for index in range( 2, 8 ):
            images[ 'Hatch' ] = images[ 'Hatch' + str( index ) ]
            drawState( 3 )
        gameData[ 'state' ] = 'opened'
    else:
        showText( 'The handle', 'will not', 'turn.' )

def makeTea():
    showText( 'Tea bag in,', 'pour water,', 'add milk.' )
    images[ 'Galley' ] = images[ 'Galley3' ]
    showText( 'Item:', 'cup of tea' )
    gameData[ 'items' ].append( 'Cup of tea' )

def drinkTea():
    showText( 'Delicious!' )
    gameData[ 'items' ].remove( 'Cup of tea' )
    gameData[ 'drunkTea' ] = True

def swimForIsland():
    showText( 'You look', 'into the', 'water.' )
    showText( 'A shark fin', 'glides by.' )
    showText( 'Might not', 'be a good', 'idea?' )
    gameData[ 'mightSwim' ] = False

def waitForRescue():
    showText( 'Time passes', 'and you', 'start to' )
    showText( 'wonder if', 'you have', 'really...' )
    showText( '...escaped?' )
    showText( '' )
    showText( 'Then you', 'hear a', 'noise.' )
    showText( "Something's", 'coming...' )
    gameData[ 'film' ] = True
    gameData[ 'image' ] = 'Rescue'
    setFPS( 15 )
    for index in range( 45 ):
        images[ 'Rescue' ] = images[ 'Rescue' + str( index % 3 ) ]
        drawState()
    showText( 'Rescue!' )
    for index in range( 40 ):
        drawImage( 'Outside', index )
        d.update()
    gameData[ 'state' ] = 'escaped'

readTornPaperAction        = Action( 'Read torn paper',         lambda: 'Torn paper'         in gameData[ 'items' ] and 'Morse print: EKO' not in gameData[ 'items' ], readTornPaper        )
turnTornPaperAction        = Action( 'Turn over torn paper',    lambda: 'Torn paper'         in gameData[ 'items' ] and 'Morse print: EKO' not in gameData[ 'items' ], turnTornPaper        )
readControlPanelNoteAction = Action( 'Read control panel note', lambda: 'Control panel note' in gameData[ 'items' ],                                                   readControlPanelNote )
drinkTeaAction             = Action( 'Drink tea',               lambda: 'Cup of tea'         in gameData[ 'items' ],                                                   drinkTea             )
actions = {
    'ComputerRoom_dark': [
        Action( 'Pull light switch', lambda: gameData[ 'lightswitch' ],     lambda: transition( 'ComputerRoom', lightOn )              ),
        Action( 'Feel below',        lambda: not gameData[ 'lightswitch' ], lambda: showText( 'Nothing', 'there,', 'just floor' )      ),
        Action( 'Feel left',         lambda: not gameData[ 'lightswitch' ], lambda: showText( "Can't feel", 'anything,', 'only wall' ) ),
        Action( 'Feel above',        lambda: not gameData[ 'lightswitch' ], findLight                                                  ),
        Action( 'Feel right',        lambda: not gameData[ 'lightswitch' ], lambda: showText( 'Bare wall', 'on this', 'side' )         ),
    ],
    'ComputerRoom': [
        drinkTeaAction,
        Action( 'Pull light switch',  lambda: True,                               lambda: transition( 'ComputerRoom_dark', lightOff    ) ),
        Action( 'Look around',        lambda: 'Comp' not in gameData[ 'looked' ], lookAroundComputerRoom                                 ),
        Action( 'Look at painting',   lambda: 'Comp' in gameData[ 'looked' ] ,    lambda: showText( 'Violets' )                          ),
        Action( 'Switch on computer', lambda: 'Comp' in gameData[ 'looked' ],     lambda: transition( 'ComputerRoom',      useComputer ) ),
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
    ],
    'UnderComputer': [
        drinkTeaAction,
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
        Action( 'Take scissors', lambda: 'Scissors' not in gameData[ 'items' ], takeScissors ),
    ],
    'Corridor_RadioRoom': [
        drinkTeaAction,
        Action( 'Look at paintings', lambda: True, lambda: transition( 'Corridor_RadioRoom', lookAtFish ) ),
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
    ],
    'RadioRoom': [
        drinkTeaAction,
        Action( 'Look around',        lambda: 'RadioRoom' not in gameData[ 'looked' ],                                               lookAroundRadioRoom             ),
        Action( 'Look at painting',   lambda: 'RadioRoom' in gameData[ 'looked' ],                                                   lambda: showText( 'Bluebells' ) ),
        Action( 'Use radio',          lambda: 'RadioRoom' in gameData[ 'looked' ] and 'radio'     not in gameData[ 'looked' ],       useRadio                        ),
        Action( 'Use Morse code key', lambda: 'RadioRoom' in gameData[ 'looked' ] and not 'Morse print: EKO' in gameData[ 'items' ], useMorseKey                     ),
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
        Action( 'Take handle',        lambda: 'RadioRoom' in gameData[ 'looked' ] and 'Handle' not in gameData[ 'items' ],           takeHandle                      ),
    ],
    'Corridor_Galley': [
        drinkTeaAction,
        Action( 'Look at painting', lambda: True, lambda: showText( 'Silver', 'lilies' ) ),
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
    ],
    'Galley': [
        drinkTeaAction,
        Action( 'Look around',               lambda: 'Galley' not in gameData[ 'looked' ],                                                                                                        lookAroundGalley   ),
        Action( 'Make cup of tea',           lambda: gameData[ 'kettle' ] == 0 and 'Right key' in gameData[ 'items' ] and not gameData[ 'drunkTea' ] and 'Cup of tea' not in gameData[ 'items' ], makeTea            ),
        Action( 'Look in the oven',          lambda: 'Galley' in gameData[ 'looked' ] and 'oven'      not in gameData[ 'looked' ],                                                                lookInOven         ),
        Action( 'Look in the sink',          lambda: 'Galley' in gameData[ 'looked' ] and 'sink'      not in gameData[ 'looked' ],                                                                lookInSink         ),
        Action( 'Look in the cupboards',     lambda: 'Galley' in gameData[ 'looked' ] and 'cupboards' not in gameData[ 'looked' ],                                                                lookInCupboards    ),
        Action( 'Put the kettle on',         lambda: 'Galley' in gameData[ 'looked' ] and gameData[ 'seenNote' ] and gameData[ 'kettle' ] == -1,                                                  kettleOn           ),
        Action( 'Get a mug & a tea bag',     lambda: 'Galley' in gameData[ 'looked' ] and gameData[ 'seenNote' ] and 'Right key' not in gameData[ 'items' ],                                      teaCaddy           ),
        Action( 'Look at the steamy window', lambda: 'Galley' in gameData[ 'looked' ] and gameData[ 'kettle' ] == 0 and 'Steam number 3972' not in gameData[ 'items' ],                           lookAtSteamyWindow ),
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
    ],
    'Corridor_Bridge': [
        drinkTeaAction,
        Action( 'Look at painting', lambda: True, lambda: showText( 'Orange', 'carnations' ) ),
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
    ],
    'Bridge': [
        drinkTeaAction,
        Action( 'Look around',           lambda: 'Bridge' not in gameData[ 'looked' ], lookAroundBridge ),
        Action( 'Down periscope!',       lambda: 'Bridge' in gameData[ 'looked' ] and gameData[ 'periscope' ] == 'up',       lambda: periscope( 'down'             ) ),
        Action( 'Up periscope!',         lambda: 'Bridge' in gameData[ 'looked' ] and gameData[ 'periscope' ] != 'up',       lambda: periscope( 'up'               ) ),
        Action( 'Look at control panel', lambda: 'Bridge' in gameData[ 'looked' ],                                           controlPanel                            ),
        readControlPanelNoteAction,
        Action( 'Open draw',             lambda: 'Bridge' in gameData[ 'looked' ] and 'Left key' not in gameData[ 'items' ], openDraw                                ),
        readTornPaperAction,
        turnTornPaperAction,
    ],
    'Hatch': [
        drinkTeaAction,
        Action( 'Look around',           lambda: 'Hatch' not in gameData[ 'looked' ],                                  lookAroundHatch ),
        Action( 'Look at hatch display', lambda: 'Hatch' in gameData[ 'looked' ],                                      lookAtHatch     ),
        Action( 'Turn the hatch handle', lambda: 'Hatch' in gameData[ 'looked' ] and gameData[ 'state' ] == 'trapped', turnHatchHandle ),
        readTornPaperAction,
        turnTornPaperAction,
        readControlPanelNoteAction,
    ],
    'Outside': [
        drinkTeaAction,
        Action( 'Swim to the island', lambda: gameData[ 'mightSwim' ] == True, swimForIsland ),
        Action( 'Wait for rescue',    lambda: True,                            waitForRescue ),
    ],
}

gameData = {
    'image'        : 'ComputerRoom_dark',
    'lightswitch'  : False,
    'kettle'       : -1,
    'film'         : False,
    'docDecrypted' : False,
    'morseEntered' : False,
    'docPage'      : 0,
    'periscope'    : 'down',
    'seenNote'     : False,
    'items'        : [],
    'state'        : 'dark',
    'surfaced'     : False,
    'unlocked'     : False,
    'whistled'     : False,
    'drunkTea'     : False,
    'mightSwim'    : True,
    'looked'       : []
}

def drawImage( imageName, yOffset = 0 ):
    with open( DIR + 'images.bin', 'rb' ) as imgFile:
        imgFile.seek( images[ imageName ] )
        d.blit( imgFile.read( 360 ), 0, yOffset, 72, 40, -1, 0, 0 )

portholeFrame = 0
portholeFrames = {
    'Porthole00':  0,
    'Porthole01': 10,
    'Porthole02': 20,
    'Porthole03': 30,
    'Porthole04': 40,
    'Porthole05': 50,
    'Porthole06': 60,
    'Porthole07': 70,
    'Porthole08': 80,
    'Porthole09': 90,
    'Porthole10':100,
    'Porthole11':110,
    'Porthole12':120,
    'Porthole13':130,
    'Porthole14':140,
    'Porthole15':150,
    'Porthole16':160,
    'Porthole17':170,
    'Porthole18':180,
    'Porthole19':190,
    'Porthole20':200,
    'Porthole21':210,
    'Porthole22':220,
    'Porthole23':230,
    'Porthole24':240,
    'Porthole25':250,
    'Porthole26':260,
    'Porthole27':270,
    'Porthole28':280,
    'Porthole29':290,
    'Porthole30':300,
}
portholeSeqL = [ '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '15', '16', '17', '18', '19', '20', '20', '21', '22', '22', '22', '23', '24', '25', '26', '27', '28', '29', '30' ]
portholeSeqR = [ '00', '00', '00', '00', '15', '16', '17', '18', '19', '20', '20', '21', '22', '22', '22', '23', '24', '25', '26', '27', '28', '29', '30', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00', '00' ]
def drawPortholes():
    global portholeFrame
    with open( DIR + 'portholes.bin', 'rb' ) as imgFile:
        if gameData[ 'kettle' ] != 0:
            imgFile.seek( portholeFrames [ 'Porthole' + portholeSeqL[ portholeFrame ] ] )
            d.blit( imgFile.read( 10 ), 7, 2, 8, 8, -1, 0, 0 )
        imgFile.seek( portholeFrames [ 'Porthole' + portholeSeqR[ portholeFrame ] ] )
        d.blit( imgFile.read( 10 ), 48, 2, 8, 8, -1, 0, 0 )
    portholeFrame += 1
    if portholeFrame >= len( portholeSeqL ):
        portholeFrame = 0

def drawPorthole():
    global portholeFrame
    with open( DIR + 'portholes.bin', 'rb' ) as imgFile:
        imgFile.seek( portholeFrames [ 'Porthole' + portholeSeqL[ portholeFrame ] ] )
        d.blit( imgFile.read( 10 ), 42, 4, 8, 8, -1, 0, 0 )
    portholeFrame += 1
    if portholeFrame >= len( portholeSeqL ):
        portholeFrame = 0

def drawState( times = 1 ):
    imageName = gameData[ 'image' ]
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
            b.inputJustPressed()
        if imageName == 'Galley':
            setPortholeFPS()
            drawPortholes()
        elif imageName == 'RadioRoom':
            setPortholeFPS()
            drawPorthole()
        d.update()

def drawDup( c, x1, y1, x2, y2 ):
    d.drawLine( x1, y1, x2, y2, c )
    d.drawLine( d.width - x1 - 1, y1, d.width - x2 - 1, y2, c )
    d.drawLine( x1, d.height - y1 - 1, x2, d.height - y2 - 1, c )
    d.drawLine( d.width - x1 - 1, d.height - y1 - 1, d.width - x2 - 1, d.height - y2 - 1, c )

def overlay( c ):
    drawDup( c, 0, 0, 5, 0 )
    drawDup( c, 0, 1, 3, 1 )
    drawDup( c, 0, 2, 2, 2 )
    drawDup( c, 0, 3, 1, 3 )
    drawDup( c, 0, 4, 0, 5 )

onceTexts = set()
def showTextOnce( line1, line2 = None, line3 = None ):
    textKey = line1 + '|' + ( line2 if line2 else "" ) + '|' + ( line3 if line3 else "" )
    if textKey in onceTexts:
        return True
    onceTexts.add( textKey )
    return showText( line1, line2, line3 )

def showText( line1, line2 = None, line3 = None, timeout = None, background = overlay ):
    fg = 1 if gameData[ 'state' ] == 'dark' else 0
    bg = 0 if gameData[ 'state' ] == 'dark' else 1
    d.fill( bg )
    background( fg )
    y = 14
    if line2: y -= 4
    if line3: y -= 4
    d.drawText( line1, 37 - len( line1 ) * 3, y, fg )
    if line2: d.drawText( line2, 37 - len( line2 ) * 3, y + 10, fg )
    if line3: d.drawText( line3, 37 - len( line3 ) * 3, y + 20, fg )
    b.inputJustPressed()
    while not which():
        d.update()
        if timeout != None:
            timeout -= 1
            if timeout <= 0:
                break;
    return True

def showInventory():
    items = gameData[ 'items' ]
    if items:
        Menu( [ ( 'Inventory:', lambda: None ) ] + [ ( item, lambda: None ) for item in items ] ).display()
    else:
        Menu( [ ( 'Inventory:', lambda: None ), ( 'No items', lambda: None ) ] ).display()


def enterCode( background, x, y, state, target, chars ):
    currentIndex = 0
    drawImage( background )
    while True:
        d.drawFilledRectangle( x, y, len( state ) * 9, 9, 1 )
        d.drawFilledRectangle( x + currentIndex * 9, y, 9, 9, 0 )
        for index in range( len( state ) ):
            d.drawText( chars[ state[ index ] ], x + 2 + index * 9, y + 1, 1 if index == currentIndex else 0 )
        d.update()
        btn = which()
        if not btn:
            continue
        if btn == 'B':
            return False
        if btn == 'A':
            if state == target:
                return True
            else:
                return False
        elif btn == 'U':
            state [ currentIndex ] += 1
            if state [ currentIndex ] >= len( chars ): state [ currentIndex ] = 0
        elif btn == 'D':
            state [ currentIndex ] -= 1
            if state [ currentIndex ] < 0: state [ currentIndex ] = len( chars ) - 1
        elif btn == 'L':
            currentIndex -= 1
            if currentIndex < 0: currentIndex = 0
        elif btn == 'R':
            currentIndex += 1
            if currentIndex >= len( state ): currentIndex = len( state ) - 1

def lookAtFish():
    fishNumber = 1
    while True:
        gameData[ 'image' ] = 'FishPicture' + str( fishNumber )
        gameData[ 'film' ] = True
        drawState( 9 )
        if fishNumber == 1:
            showText( '1 of 4:', 'Red', 'Herring' )
        elif fishNumber == 2:
            showText( '2 of 4:', 'Bluefin', 'Tuna' )
        elif fishNumber == 3:
            showText( '3 of 4:', 'Yellowtail', 'Snapper' )
        else:
            showText( '4 of 4:', 'Goldfish' )
        gameData[ 'film' ] = False
        while True:
            drawState()
            key = which()
            if not key:
                continue
            if key in 'ABUD':
                return True
            if key == 'L':
                if fishNumber == 1:
                    showText( 'This is', 'the first', 'picture' )
                    drawState()
                else:
                    fishNumber -= 1
                    break
            elif key == 'R':
                if fishNumber == 4:
                    showText( 'This is', 'the last', 'picture' )
                    drawState()
                else:
                    fishNumber += 1
                    break

def act():
    actionList = actions[ gameData[ 'image' ] ]
    acts = list( filter( lambda a: a.prerequisite(), actions[ gameData[ 'image' ] ] ) )
    if acts:
        Menu( [ a.menuItem() for a in acts ] ).display()
    else:
        Menu( [ ( 'Nothing to do here', lambda: None ) ] ).display()

def whistle():
    audio.play( 1500, 2147483647 )
    showText( 'The kettle', 'whistles!' )
    audio.stop()
    gameData[ 'whistled' ] = True

def move( key ):
    imageName = gameData[ 'image' ]
    if imageName == 'ComputerRoom_dark':
        showText( "It's dark,", "don't move!", 'Need light.' )
        return
    moves = movements[ imageName ]
    if key in moves:
        transition( moves[ key ][ 0 ], moves[ key ][ 1 ] )
    else:
        showText( "Can't go", 'that way' )

def tick():
    if gameData[ 'kettle' ] > 0:
        gameData[ 'kettle' ] -= 1
    if gameData[ 'kettle' ] == 0 and not gameData[ 'whistled' ]:
        whistle()

def handleInput():
    gameData[ 'film' ] = False
    key = which()
    if key == 'A':
        act()
    elif key == 'B':
        showInventory()
    elif key:
        move( key )

try:
    drawImage( 'Title' )
    while not which():
        d.update()
    showText( "It's dark." )
    showText( 'Where ARE', 'you??' )
    showText( "You're", 'stuck...' )
    showText( '...again.' )
    showText( 'How will', 'you escape', 'this time?' )
    showText( 'UDLR:move', 'A:menu/act', 'B:items/cncl' )
    while gameData[ 'state' ] != 'escaped':
        tick()
        drawState()
        handleInput()
except Exception as x:
    if inEmulator:
        print_exception( x )
    else:
        with open( DIR + 'crashdump.log', 'w', encoding = "utf-8" ) as f:
            print_exception( x, f )
    d.fill( 0 )
    d.drawText( "Oops - died", 3,  8, 1 )
    d.drawText( "Problem was:", 0, 22, 1 )
    sideScroll( str( x ), 1, 0, 30, d.width, -1, {
        'A': lambda: True,
        'B': lambda: True
    } )
