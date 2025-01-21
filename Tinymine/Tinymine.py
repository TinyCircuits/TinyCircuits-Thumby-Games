import time
import thumby
import random
from sys import print_exception
import gc

DIR = '/Games/Tinymine'
from sys import path
if not DIR in path:
    path.append( DIR )
from taskrunner import startTaskRunner, addTask
from playtune import Tune

thumby.saveData.setName( 'Tinymine' )

inEmulator = False
try:
    import emulator
    inEmulator = True
except ImportError:
    pass

def log( msg ):
    if inEmulator:
        print( msg )
    else:
        #with open( DIR + '/log', 'a' ) as f:
        #    f.write( str( time.ticks_cpu() ) )
        #    f.write( ' ' )
        #    f.write( msg )
        #    f.write( '\n' )
        pass

try:
    if startTaskRunner( DIR ):
        log( 'Started tune thread' )
    else:
        log( 'Could not start tune thread' )
except Exception as x:
    if inEmulator:
        print_exception( x )
    else:
        thumby.display.fill( 0 )
        thumby.display.drawText( "ERROR", 3, 8, 1 )
        thumby.display.drawText( str( x ), 0, 20, 1 )
        thumby.display.update()
        with open( DIR + '/crashdump.log', 'w', encoding="utf-8" ) as f:
            print_exception( x, f )
        while not btn.which( False ):
            thumby.display.update()
    thumby.reset()

def shuffle( list ):
    random.seed( time.ticks_cpu() )
    # Fisher-Yates shuffle (apparently)
    for i in range( len( list ) - 1, 0, -1 ):
        j = random.randrange( i + 1 )
        list[ i ], list[ j ] = list[ j ], list[ i ]

def setUpSprites( spriteX, spriteY ):
    sprites = {}

    # 8x10 for 3 frames
    runningFrames = bytearray([16,144,255,61,43,104,132,0,1,0,0,0,0,0,0,0,0,0,254,250,86,32,0,0,0,3,1,0,3,2,0,0,0,0,144,127,125,147,16,8,0,1,2,0,0,1,0,0])
    sprites['runningRightSprite'] = thumby.Sprite(
        8, 10,
        runningFrames,
        spriteX, spriteY,
        0
    )
    sprites['runningLeftSprite'] = thumby.Sprite(
        8, 10,
        runningFrames,
        spriteX, spriteY,
        0, 1
    )

    # 8x11 for 2 frames
    sprites['climbingSprite'] = thumby.Sprite(
        8, 11,
        bytearray([0,15,240,254,254,166,48,0,0,0,7,0,0,2,1,0,0,48,166,254,254,240,15,0,0,1,2,0,0,7,0,0]),
        spriteX, spriteY - 1
    )

    # 8x10 for 4 frames
    sprites['standingSprite'] = thumby.Sprite(
        8, 10,
        bytearray([0,48,139,125,255,176,0,0,0,2,3,0,0,3,2,0,0,32,154,127,125,138,48,0,0,2,3,0,0,3,2,0,0,0,176,255,125,139,48,0,0,2,3,0,0,3,2,0,0,48,138,125,127,154,32,0,0,2,3,0,0,3,2,0]),
        spriteX, spriteY,
        -1
    )

    # 8x7 for 4 frames
    sprites['crouchingSprite'] = thumby.Sprite(
        8, 7,
        bytearray([0,80,107,29,63,112,64,0,0,64,122,31,29,106,80,0,0,64,112,63,29,107,80,0,0,80,106,29,31,122,64,0]),
        spriteX, spriteY + 3
    )

    # 8x10 for 1 frames
    sprites['squishedSprite'] = thumby.Sprite(
        8, 10,
        bytearray([0,128,64,192,128,192,128,0,3,3,3,3,3,2,3,3]),
        spriteX, spriteY,
        0
    )

    # 8x10 for 2 frames
    sprites['fallingSprite'] = thumby.Sprite(
        8, 10,
        bytearray([128,8,211,125,255,16,32,0,0,1,0,0,3,2,0,0,128,16,210,127,125,210,16,128,0,1,0,0,0,0,1,0,0,32,16,255,125,211,8,128,0,0,2,3,0,0,1,0,128,16,210,125,127,210,16,128,0,1,0,0,0,0,1,0]),
        spriteX, spriteY,
        0
    )

    # 8x10 for 1 frames
    slidingFrames = bytearray([0,128,72,83,253,127,16,8,0,1,0,3,0,0,0,0])
    sprites['slidingLeftSprite'] = thumby.Sprite(
        8, 10,
        slidingFrames,
        spriteX, spriteY,
        0
    )
    sprites['slidingRightSprite'] = thumby.Sprite(
        8, 10,
        slidingFrames,
        spriteX, spriteY,
        0, 1
    )

    # 8x10 for 2 frames
    sprites['bouncingSprite'] = thumby.Sprite(
        8, 10,
        bytearray([0,48,200,127,125,203,48,0,0,0,3,0,0,3,0,0,132,8,203,125,127,200,8,132,0,1,0,0,0,0,1,0]),
        spriteX, spriteY + 1,
        0
    )

    # 12x7 for 4 frames
    sprites['clingSprite'] = thumby.Sprite(
        12, 7,
        bytearray([28,20,24,25,62,24,24,28,18,9,8,0,0,28,20,25,26,60,48,56,22,19,8,8,56,40,48,27,124,24,20,18,9,8,8,0,0,28,20,25,26,60,48,56,22,19,8,8]),
        spriteX - 2, spriteY
    )

    # 8x10 for 1 frames
    sprites['ridingSprite'] = thumby.Sprite(
        8, 10,
        bytearray([0,208,139,253,255,152,192,0,0,0,0,0,0,0,0,0,0,208,138,255,253,138,208,0,0,0,0,0,0,0,0,0,0,192,152,255,253,139,208,0,0,0,0,0,0,0,0,0,0,208,138,253,255,138,208,0,0,0,0,0,0,0,0,0]),
        spriteX, spriteY,
        0
    )

    # 12x9 for 1 frames
    ridingLowFrames = bytearray([128,64,120,232,208,192,128,192,96,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0])
    sprites['ridingLowSpriteL'] = thumby.Sprite(
        12, 9,
        ridingLowFrames,
        spriteX, spriteY,
        0
    )
    sprites['ridingLowSpriteR'] = thumby.Sprite(
        12, 9,
        ridingLowFrames,
        spriteX - 5, spriteY,
        0, 1
    )

    return sprites

class Level:
    def __init__( self ):
        self.startRow = 0
        self.startCol = 0
        self.mine = []
        self.gold = 0
        self.carts = []
        self.snakes = []
        self.maxRow = 0
        self.maxCol = 0
        self.msgToCoords = {}
        self.coordToMsg = {}

    def addMsg( self, msgLocations ):
        parts = msgLocations.split( '=' )
        msg = parts [ 0 ]
        coords = []
        for coord in parts[ 1 ].split( ';' ):
            rc = coord.split( ',' )
            t = ( int( rc[ 0 ] ), int( rc[ 1 ] ) )
            coords.append( t )
            self.coordToMsg[ t ] = msg
        self.msgToCoords[ msg ] = coords

    def checkMsgs( self, row, col ):
        t = ( row, col )
        if t in self.coordToMsg:
            msg = self.coordToMsg[ t ]
            for coords in self.msgToCoords.pop( msg ):
                self.coordToMsg.pop( coords )
            return True, msg
        else:
            return False, None

class Cart:
    def __init__( self ):
        self.row = 0
        self.col = 0
        self.dir = 1
        self.riderOffset = 0

class Snake:
    def __init__( self ):
        self.row = 0
        self.col = 0
        self.dir = 'R'
        self.state = 0

def loadLevel( id, canJump, canRide, chaos ):
    global startTime
    if id == 1:
        startTime = time.time()
    thumby.display.fill( 0 )
    thumby.display.drawText( "Loading...", 3, 8, 1 )
    thumby.display.update()
    idStr = str( id )
    log( 'loading level ' + idStr )
    level = Level()
    mine = level.mine
    file = open( '/Games/Tinymine/mine' + idStr + '.txt', 'r' )
    lines = file.readlines ()
    file.close()
    for line in lines:
        line = line.strip()
        if canJump:
            line = line.replace( '!', ' ' )
        if canRide:
            line = line.replace( '*', ' ' )
        if not chaos:
            line = line.replace( '.', ' ' )
        if level.startRow == 0 and level.startCol == 0:
            cfg = line.split( '|' )
            rc = cfg[ 0 ].split( ',' )
            level.startRow = int( rc[ 0 ] )
            level.startCol = int( rc[ 1 ] )
            for msg in cfg[ 1 : ]:
                level.addMsg( msg )
        else:
            mine.append( line )
            cartCol = line.find( 'oo' )
            if -1 != cartCol:
                cart = Cart()
                cart.col = cartCol
                cartRow = len( level.mine ) - 1
                cart.row = cartRow
                level.carts.append( cart )
                # Remove static cart from mine
                mine[ cartRow - 1 ] = mine[ cartRow - 1 ][ : cartCol - 1 ] + '    ' + mine[ cartRow - 1 ][ cartCol + 3 : ]
                mine[ cartRow ] = mine[ cartRow ][ : cartCol ] + '  ' + mine[ cartRow ][ cartCol + 2 : ]
            snakeCol = line.find( '^+^' ) + 1
            if 0 != snakeCol:
                snake = Snake()
                snake.dir = '?'
                snakeRow = len( level.mine ) - 1
                snake.row = snakeRow
                snake.col = snakeCol
                if line[ snakeCol - 6 : snakeCol - 1 ] == '_/\\_/':
                    snake.dir = 'R'
                if line[ snakeCol + 2 : snakeCol + 7 ] == '\\_/\\_':
                    snake.dir = 'L'
                if snake.dir != '?':
                    level.snakes.append( snake )
                    # Remove static snake from mine
                    if snake.dir == 'R':
                        mine[ snakeRow ] = mine[ snakeRow ][ : snakeCol - 6 ] + '        ' + mine[ snakeRow ][ snakeCol + 2 : ]
                    else:
                        mine[ snakeRow ] = mine[ snakeRow ][ : snakeCol - 1 ] + '        ' + mine[ snakeRow ][ snakeCol + 7 : ]
            for ch in line:
                if ch == '@':
                    level.gold = level.gold + 1
    level.maxRow = len( level.mine ) - 4
    level.maxCol = len( level.mine[ 0 ] ) - 6
    if chaos:
        thumby.display.drawText( "Chaos...", 23, 31, 1 )
        thumby.display.update()
        gc.collect()
        # Get all possible positions, and remove symbols
        possibleGold = []
        for row, line in enumerate( mine ):
            for col, char in enumerate( line ):
                if char in ".@":
                    if len( possibleGold ) % 10 == 0:
                        gc.collect()
                    possibleGold.append( ( row, col ) )
            mine[ row ] = line.replace( '.', ' ' ).replace( '@', ' ' )
        # Randomise positions
        gc.collect()
        shuffle( possibleGold )
        # Put some gold back
        gc.collect()
        for pos in possibleGold [ : level.gold ]:
            line = mine[ pos[ 0 ] ]
            col = pos[ 1 ]
            mine[ pos[ 0 ] ] = line[ : col ] + '@' + line[ col + 1 : ]
        gc.collect()
    return level

def getOkDirs( mine ):
    result = []
    chars = [
        mine[ row - 1 ][ col     ], # Up
        mine[ row     ][ col + 1 ], # Right
        mine[ row + 1 ][ col     ], # Down
        mine[ row     ][ col - 1 ]  # Left
    ]
    # up?
    result.append( chars[ 0 ] == '=' )
    # right?
    result.append( chars[ 1 ] not in '|+-Y' and row % 3 == 2 )
    # down?
    result.append( chars[ 2 ] == '=' )
    # left?
    result.append( chars[ 3 ] not in '|+-Y' and row % 3 == 2 )
    return result

def levelSplash( sprites, spriteY ):
    spriteOffset = 0
    thumby.display.setFPS( 4 )

    thumby.display.fill( 0 )
    thumby.display.update()
    time.sleep( 1 )

    addTask( Tune( '150:0|8| z,4|8| ,4|8| ,1|8| ,4|16| ,4|16| ,1|8| z,4|8| ,4|16| ,4|16| ,4|16| ,1|8| z,4|8| ,4|8| ,2|8| ,4|16| ,4|8| ,20|8| ,20|8| r,4|8| ,4|8| z,1|8| ,4|16| ,4|16| ' ).play )

    splash = [
        '&& &&                  ',
        '\\\\&/&      Level ' + str( levelNumber ) + '   ',
        '&||&                   ',
        ' ||  =                 ',
        '//\\\\-=---------------',
        '     =                 '
    ]

    def drawSplash( offset, spriteDrawer ):
        thumby.display.fill( 0 )
        for i, splashTxt in enumerate( splash ):
            thumby.display.drawText( splashTxt[ offset: offset + 11 ], 3, i * 7, 1 )
        if spriteDrawer:
            spriteDrawer()
        thumby.display.update()

    def splashSprite( name, frame, y ):
        sprite = sprites[ name ]
        oldY = sprite.y
        sprite.setFrame( frame )
        sprite.y = y
        thumby.display.drawSprite( sprite )
        sprite.y = oldY

    drawSplash( 0, None )
    time.sleep( 1 )

    drawSplash( 0, lambda:splashSprite( 'climbingSprite',     0, 33 ) )
    drawSplash( 0, lambda:splashSprite( 'climbingSprite',     1, 26 ) )
    drawSplash( 0, lambda:splashSprite( 'climbingSprite',     0, 19 ) )
    thumby.display.setFPS( 7 )
    drawSplash( 1, lambda:splashSprite( 'runningRightSprite', 2, 21 ) )
    drawSplash( 2, lambda:splashSprite( 'runningRightSprite', 0, 21 ) )
    drawSplash( 3, lambda:splashSprite( 'runningRightSprite', 1, 21 ) )
    drawSplash( 4, lambda:splashSprite( 'runningRightSprite', 2, 21 ) )
    drawSplash( 5, lambda:splashSprite( 'runningRightSprite', 0, 21 ) )
    drawSplash( 6, lambda:splashSprite( 'runningRightSprite', 1, 21 ) )
    drawSplash( 7, lambda:splashSprite( 'runningRightSprite', 2, 21 ) )
    drawSplash( 8, lambda:splashSprite( 'runningRightSprite', 0, 21 ) )
    drawSplash( 9, lambda:splashSprite( 'runningRightSprite', 1, 21 ) )

    for frame in [0, 1, 2, 3, 0, 1, 2, 3]:
        drawSplash( 9, lambda:splashSprite( 'standingSprite', frame, 21 ) )

    thumby.display.fill( 0 )
    thumby.display.drawText( '  Level ' + str( levelNumber ), 3,  7, 1 )
    thumby.display.drawText( '-----------',                   3, 28, 1 )
    thumby.display.update()

    thumby.display.fill( 0 )
    thumby.display.drawText( '  Level ' + str( levelNumber ), 3,  7, 1 )
    thumby.display.update()

    thumby.display.fill( 0 )
    thumby.display.update()
    time.sleep( 0.5 )

def sayDead( reason ):
    # https://i.ytimg.com/vi/8UnfJMAknVI/maxresdefault.jpg
    addTask( Tune( '270:0|64| ,0|32| .,0|16| ,0|64| ,4|32| .,2|16| ,4|4| z,2|32| .,0|16| ,0|32| .,0|16| ,0|64| ' ).play )
    thumby.display.fill(0)
    thumby.display.setFont( "/lib/font8x8.bin", 8, 8, 1 )
    thumby.display.drawText( "R.I.P.", 11, 5, 1 )
    thumby.display.setFont( "/lib/font5x7.bin", 5, 10, 1 )
    thumby.display.drawText(
        reason,
        int( ( thumby.display.width - len( reason ) * 6 ) / 2 ),
        25, 1
    )
    thumby.display.update()
    while( not thumby.inputPressed() ):
        thumby.display.update()

def sayDone( chaos ):
    thumby.display.fill(0)
    thumby.display.setFont( "/lib/font8x8.bin", 8, 8, 1 )
    thumby.display.drawText( "Complete", 0, 5, 1 )
    thumby.display.setFont( "/lib/font5x7.bin", 5, 10, 1 )
    thumby.display.drawText("You legend!", 4, 20, 1 )
    if startTime > 0:
        msg = 'Time: ' + str( time.time() - startTime ) + 's'
        thumby.display.drawText( msg, int( ( 6 - len( msg ) / 2 ) * 6 ), 33, 1 )
    thumby.display.update()
    time.sleep( 0.5 )
    #play( [
    #    "6 S", "R XXS", "6 XS", "R XXS", "6 XS", "4 M s", "6 M", "4 M s", "0 L s"
    #] )
    #c  c# d  d# e  f  f# g  g# a  a# b  c  c# d  d# e  f  f# g  g# a  a#  b  c
    #7     6     5  4     3     2     1  0
    #0  1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21
    addTask( Tune( "240:2|16| ,2|4|r,2|8| ,2|4|r,2|8| ,6|32| ,2|32| ,6|32| ,14|64|." ).play )
    while( not thumby.inputPressed() ):
        thumby.display.update()
    thumby.display.fill(0)
    if chaos:
        thumby.display.drawText( "What next?",   6,  2, 1 )
        thumby.display.drawText( "A: chaos pls", 0, 13, 1 )
        thumby.display.drawText( "B: back to",   0, 25, 1 )
        thumby.display.drawText( "   normal",    0, 33, 1 )
        thumby.display.update()
        time.sleep( 0.5 )
        while True:
            if thumby.buttonA.pressed():
                thumby.saveData.setItem( 'levelNumber', 1 )
                thumby.saveData.save()
                break;
            elif thumby.buttonB.pressed():
                thumby.saveData.setItem( 'chaos',      'False' )
                thumby.saveData.setItem( 'canJump',    'False' )
                thumby.saveData.setItem( 'canRide',    'False' )
                thumby.saveData.setItem( 'levelNumber', 1      )
                thumby.saveData.save()
                break;
            thumby.display.update()
    else:
        thumby.display.drawText( "Next time,",   6,  3, 1 )
        thumby.display.drawText( "Gold moved!",  3, 16, 1 )
        thumby.display.drawText( "Chaos monkey", 0, 24, 1 )
        thumby.display.drawText( "caused chaos", 0, 32, 1 )
        thumby.display.update()
        time.sleep( 1 )
        while( not thumby.inputPressed() ):
            thumby.display.update()
        thumby.saveData.setItem( 'chaos', 'True' )
        thumby.saveData.setItem( 'levelNumber', 1 )
        thumby.saveData.save()

def toSemitone( goldLeft, adjustment = 'n' ):
    octaveNote = goldLeft % 7
    octaveSemitone = {
        6:10,
        5:8,
        4:7,
        3:5,
        2:3,
        1:1,
        0:0
    } [ octaveNote ]
    if adjustment == 's':
        octaveNote = octaveNote - 1
    elif adjustment == 'f':
        octaveNote = octaveNote + 1
    octave = int( goldLeft / 7 )
    semitone = octave * 12 + octaveSemitone
    return -semitone

def nextCartCol( cart, mine ):
    cartDir = cart.dir
    cartRow = cart.row
    cartCol = cart.col
    mine = level.mine
    cart.col = cartCol + cartDir
    if cartDir > 0 and ( mine[ cartRow ][ cartCol + 3 ] in '|:' or mine[ cartRow - 1 ][ cartCol + 3 ] in '|:' ):
        cart.dir = -1
    elif  cartDir < 0 and ( mine[ cartRow ][ cartCol - 4 ] in '|:' or mine[ cartRow - 1 ][ cartCol - 4 ] in '|:' ):
        cart.dir = 1

def drawChar( char, charRow, charCol, row, col, wobble = False ):
    # Adjust mine row to screen row
    drawRow = charRow - row + 3
    if drawRow >= 0 and drawRow <= 5:
        # Adjust mine col to screen col
        drawCol = charCol - col + 5
        if drawCol >= 0 and drawCol <= 12:
            yAdj = 1 if wobble and charCol % 2 == 0 else 2
            thumby.display.drawText( char, drawCol * 5 + 3, drawRow * 7 + yAdj, 1 )

def drawCart( cartRow, cartCol, row, col ):
    bodyRow = cartRow - 1
    drawChar( '\\', bodyRow, cartCol - 1, row, col       )
    drawChar( '_',  bodyRow, cartCol    , row, col       )
    drawChar( '_',  bodyRow, cartCol + 1, row, col       )
    drawChar( '/',  bodyRow, cartCol + 2, row, col       )
    drawChar( 'o',  cartRow, cartCol    , row, col, True )
    drawChar( 'o',  cartRow, cartCol + 1, row, col, True )

def moveCart( mine, cart, row, col, spriteName ):
    nextCartCol( cart, mine )
    cartRow = cart.row
    cartCol = cart.col
    drawCart( cartRow, cartCol, row, col )
    if spriteName not in [ 'cling', 'riding', 'ridingLowL', 'ridingLowR' ] and ( ( cartRow == row and ( cartCol - 1 == col or cartCol == col ) ) or ( cartRow - 1 == row and cartCol - 2 <= col and cartCol + 1 >= col ) ):
        return 'cart squish'
    return None

def cartBelow( row, col ):
    for cart in level.carts:
        adjCol = col - cart.dir
        if cart.row == row and cart.col - 2 <= adjCol and adjCol <= cart.col + 1:
            cart.riderOffset = 0 if cart.col <= adjCol else -1
            return cart
    return None

def nextSnakeState( snake, row, col ):
    if snake.state > 0:
        snake.state = snake.state + 1
        if snake.state >= 4:
            snake.state = 0
    elif snake.row == row and abs( snake.col - col ) <= 3:
        snake.state = 1

def drawSnake( snake, row, col ):
    rightSnake = snake.dir == 'R'
    snakeBody =  {
        0: '/\\_/' if rightSnake else '\\_/\\',
        1: '_^__,' if rightSnake else ',__^_',
        2: '______',
        3: '_^__,' if rightSnake else ',__^_',
    } [ snake.state ]
    headPos = -1
    if rightSnake:
        snakeStart = snake.col - 5
        for i, char in enumerate( snakeBody ):
            drawChar( char, snake.row, snakeStart + i, row, col )
        headPos = snakeStart + i + 2
        drawChar( '^', snake.row, snakeStart + i + 1, row, col )
        drawChar( '+', snake.row, headPos,            row, col )
        drawChar( '^', snake.row, snakeStart + i + 3, row, col )
    else:
        snakeStart = snake.col - {
            0: -1,
            1: 0,
            2: 1,
            3: 0
        }[ snake.state ]
        headPos = snakeStart + 1
        drawChar( '^', snake.row, snakeStart,     row, col )
        drawChar( '+', snake.row, headPos,        row, col )
        drawChar( '^', snake.row, snakeStart + 2, row, col )
        snakeStart = snakeStart + 3
        for i, char in enumerate( snakeBody ):
            drawChar( char, snake.row, snakeStart + i, row, col )
    return headPos - 1

def moveSnake( snake, row, col ):
    nextSnakeState( snake, row, col )
    headCol = drawSnake( snake, row, col )
    if snake.row == row:
        if abs(headCol - col) < 2:
            return 'snake bite'
    return None

def handleNPC( level, row, col, spriteName ):
    for cart in level.carts:
        deathReason = moveCart( level.mine, cart, row, col, spriteName )
        if deathReason:
            return deathReason
    for snake in level.snakes:
        deathReason = moveSnake( snake, row, col )
        if deathReason:
            return deathReason
    return None

def nextToCart( level, row, col ):
    for cart in level.carts:
        if cart.row == row:
            if cart.col - col == 2:
                return True
            if col - cart.col == 1:
                return True
    return False

def canCling( level, row, col ):
    return level.mine[ row ][ col ] == '=' and level.mine[ row + 1 ][ col ] != '='

# Setup
spriteY = 21
sprites = setUpSprites( 32, spriteY )
if thumby.saveData.hasItem( 'levelNumber' ):
    levelNumber = int( thumby.saveData.getItem( 'levelNumber' ) ) - 1
else:
    levelNumber = 0
row = 0
col = 0
level = None
minRow = 2
minCol = 5
spriteOffset = 0
fallCount = 0
bounceDir = 'N'
spriteName = '?'
deathReason = None
ridingCart = None
fragileFloorCount = 0
messageCount = 0

# Initial title screen
addTask( Tune( "9|16| ,11|16| ,13|16| ,14|16| ,16|16| ,18|16| ,20|16| ,21|32|." ).play )
thumby.display.setFPS( 1 )
thumby.display.setFont( "/lib/font8x8.bin", 8, 8, 1 )
thumby.display.fill( 0 )
thumby.display.drawText( "Tinymine", 0, 3, 1 )
thumby.display.update()
thumby.display.update()
thumby.display.setFont( "/lib/font5x7.bin", 5, 10, 1 )
thumby.display.drawText( "Find gold @", 3, 17, 1 )
thumby.display.update()
thumby.display.drawText( "A/B: start", 7, 30, 1 )
while( not thumby.actionJustPressed() ):
    thumby.display.update()
def miniAnim():
    spriteOffset = 0
    thumby.display.setFPS( 7 )
    sprite = sprites [ 'runningLeftSprite' ]
    oldX = sprite.x
    oldY = sprite.y
    sprite.y = 15
    sprite.x = thumby.display.width - 4
    for frame in range( 0, 2 ):
        thumby.display.drawFilledRectangle( 0, 15, thumby.display.width, 10, 0 )
        thumby.display.drawText( "Find gold @", 3, 17, 1 )
        sprite.setFrame( spriteOffset )
        thumby.display.drawSprite( sprite )
        thumby.display.update()
        sprite.x = sprite.x - 6
        spriteOffset = spriteOffset + 1
    sprite.x = oldX
    sprite.y = oldY
    sprite = sprites [ 'standingSprite' ]
    oldX = sprite.x
    oldY = sprite.y
    sprite.y = 15
    sprite.x = thumby.display.width - 10
    thumby.display.drawFilledRectangle( 57, 15, 8, 11, 0 )
    thumby.display.drawSprite( sprite )
    thumby.display.drawText( '\\|/', 57, 10, 1 )
    thumby.display.drawText( '> <',  57, 17, 1 )
    thumby.display.drawText( '/|\\', 57, 21, 1 )
    thumby.display.update()
    thumby.display.fill( 0 )
    thumby.display.setFont( "/lib/font8x8.bin", 8, 8, 1 )
    thumby.display.drawText( "Tinymine", 0, 3, 1 )
    thumby.display.setFont( "/lib/font5x7.bin", 5, 10, 1 )
    thumby.display.drawText( "A/B: start", 7, 30, 1 )
    for frame in range( 0, 2 ):
        thumby.display.drawFilledRectangle( 0, 15, thumby.display.width, 10, 0 )
        thumby.display.drawText( "Find gold", 3, 17, 1 )
        sprite.setFrame( spriteOffset )
        thumby.display.drawSprite( sprite )
        thumby.display.update()
        spriteOffset = spriteOffset + 1
    sprite.x = oldX
    sprite.y = oldY
    sprite = sprites [ 'runningRightSprite' ]
    oldX = sprite.x
    oldY = sprite.y
    sprite.y = 15
    sprite.x = thumby.display.width - 10
    for frame in range( 0, 3 ):
        thumby.display.drawFilledRectangle( 0, 15, thumby.display.width, 10, 0 )
        thumby.display.drawText( "Find gold", 3, 17, 1 )
        sprite.setFrame( spriteOffset )
        thumby.display.drawSprite( sprite )
        thumby.display.update()
        sprite.x = sprite.x + 6
        spriteOffset = spriteOffset + 1
    sprite.x = oldX
    sprite.y = oldY
    thumby.display.setFPS( 5 )
miniAnim()

def drawSplash():
    thumby.display.drawText( '\\|/', 27, 14, 1 )
    thumby.display.drawText( '> <',  27, 21, 1 )
    thumby.display.drawText( '/|\\', 27, 28, 1 )

def checkConfig( itemName ):
    return thumby.saveData.hasItem( itemName ) and thumby.saveData.getItem( itemName ) == 'True'

canJump = checkConfig( 'canJump' )
canRide = checkConfig( 'canRide' )
chaos = checkConfig( 'chaos' )
startTime = -1

# Here follows spaghetti. Sorry - it just grew and I never refactored it.
try:
    while True:
        if spriteName == 'dead':
            time.sleep( 2 )
            sayDead( deathReason )
            break
        else:
            spriteName = '?'

        if not level or level.gold == 0:
            level = None
            gc.collect()
            levelNumber = levelNumber + 1
            if levelNumber > 6:
                sayDone( chaos )
                break
            levelSplash( sprites, spriteY )
            level = loadLevel( levelNumber, canJump, canRide, chaos )
            thumby.saveData.setItem( 'levelNumber', levelNumber )
            thumby.saveData.save()
            ridingCart = None
            spriteName = '?'
            row = level.startRow
            col = level.startCol

        # Blank canvas
        thumby.display.fill( 0 )

        if ridingCart:
            # Get out of cart?
            if canCling( level, row, col ) and thumby.buttonU.pressed():
                ridingCart = None
                spriteName = 'cling'
        else:
            charBelow = level.mine[ row + 1 ][ col ]

            # Fragile floor?
            if charBelow == ',':
                fragileFloorCount = fragileFloorCount + 1
                if fragileFloorCount > 2:
                    level.mine[ row + 1 ] = level.mine[ row + 1 ][ : col ] + ' ' + level.mine[ row + 1 ][ col + 1 : ]
                    fragileFloorCount = 0

            # Falling, sliding, clinging?
            if charBelow in ' @:':
                row = row + 1
                charBelow = level.mine[ row + 1 ][ col ]
                if charBelow == '\\':
                    col = col + 1
                    bounceDir = 'R'
                    spriteName = 'slideR'
                    fallCount = 0
                elif charBelow == '/':
                    col = col - 1
                    bounceDir = 'L'
                    spriteName = 'slideL'
                    fallCount = 0
                else:
                    if bounceDir == 'R':
                        col = col + 1
                        spriteName = 'bounce'
                        charNowBelow = level.mine[ row + 1 ][ col ]
                        if charNowBelow == '/':
                            spriteOffset = 1
                        else:
                            spriteOffset = 0
                    elif bounceDir == 'L':
                        col = col - 1
                        spriteName = 'bounce'
                        charNowBelow = level.mine[ row + 1 ][ col ]
                        if charNowBelow == '\\':
                            spriteOffset = 1
                        else:
                            spriteOffset = 0
                    elif level.mine[ row - 1 ][ col ] == '=':
                        if thumby.buttonD.pressed():
                            ridingCart = cartBelow( row, col )
                            if not ridingCart:
                                fallCount = fallCount + 1
                                row = row + 1
                                spriteName = 'fall'
                        else:
                            ridingCart = None
                            spriteName = 'cling'
                        row = row - 1
                    else:
                        fallCount = fallCount + 1
                        spriteName = 'fall'
            # Bounce?
            elif charBelow in '/\\_':
                row = row - 1
                if bounceDir == 'R':
                    col = col + 1
                    spriteName = 'bounce'
                    spriteOffset = 1
                elif bounceDir == 'L':
                    col = col - 1
                    spriteName = 'bounce'
                    spriteOffset = 1
            elif fallCount > 3:
                spriteName = 'dead'
                deathReason = 'fell too far'
            else:
                bounceDir = 'N'

                # Which directions are possible?
                okDirs = getOkDirs( level.mine )

                # Translate button input to movement
                if thumby.buttonU.pressed():
                    if okDirs[ 0 ] or ( canJump and level.mine[ row - 1 ][ col ] not in '-+#/\\X' ):
                        row = row - 1
                        if row < minRow:
                            row = minRow
                        else:
                            spriteName = 'up'
                elif thumby.buttonR.pressed():
                    if okDirs[ 1 ]:
                        col = col + 1
                        if col > level.maxCol:
                            col = level.maxCol
                        else:
                            spriteName = 'right'
                            fragileFloorCount = 0
                elif thumby.buttonD.pressed():
                    if okDirs[ 2 ]:
                        row = row + 1
                        if row > level.maxRow:
                            row = level.maxRow
                        else:
                            spriteName = 'down'
                    elif spriteName == 'cling':
                        spriteName = 'riding'
                elif thumby.buttonL.pressed():
                    if okDirs[ 3 ]:
                        col = col - 1
                        if col < minCol:
                            col = minCol
                        else:
                            spriteName = 'left'
                            fragileFloorCount = 0
                fallCount = 0

        # Draw visible part of mine
        colFrom = col - 5
        colTo = col + 6
        thumby.display.drawText( level.mine[ row - 3 ][ colFrom : colTo ], 3,  0, 1 )
        thumby.display.drawText( level.mine[ row - 2 ][ colFrom : colTo ], 3,  7, 1 )
        thumby.display.drawText( level.mine[ row - 1 ][ colFrom : colTo ], 3, 14, 1 )
        thumby.display.drawText( level.mine[ row     ][ colFrom : colTo ], 3, 21, 1 )
        thumby.display.drawText( level.mine[ row + 1 ][ colFrom : colTo ], 3, 28, 1 )
        thumby.display.drawText( level.mine[ row + 2 ][ colFrom : colTo ], 3, 35, 1 )

        thisChar = level.mine[ row ][ col ]
        # Eating gold?
        if thisChar == '@':
            drawSplash()
            level.mine[ row ] = level.mine[ row ][ : col ] + ' ' + level.mine[ row ][ col + 1 : ]
            level.gold = level.gold - 1
            thumby.audio.play( int ( 880 * pow( 1.059463094359, toSemitone( level.gold ) ) ), 500 if level.gold == 0 else 200 )
        # Learning to jump?
        elif thisChar == '!':
            level.mine[ row ] = level.mine[ row ][ : col ] + ' ' + level.mine[ row ][ col + 1 : ]
            row = row - 1
            drawSplash()
            canJump = True
            thumby.saveData.setItem( 'canJump', 'True' )
            thumby.saveData.save()
            addTask( Tune( "120:-7|16| ,4|16| ,12|16| " ).play )

        # Learning to ride?
        elif thisChar == '*':
            level.mine[ row ] = level.mine[ row ][ : col ] + ' ' + level.mine[ row ][ col + 1 : ]
            row = row - 1
            drawSplash()
            canRide = True
            thumby.saveData.setItem( 'canRide', 'True' )
            thumby.saveData.save()
            addTask( Tune( "120:12|16| ,4|16| ,-7|16| " ).play )

        # Move everything else that moves
        npcDeathReason = handleNPC( level, row, col, spriteName )

        # Handle cart riding
        if ridingCart:
            thisChar = level.mine[ row ][ col ]
            col = ridingCart.col + ridingCart.dir + ridingCart.riderOffset
            if thisChar in "-\+/" or ( thisChar == '=' and level.mine[ row + 1 ][ col ] != '=' ):
                spriteName = 'ridingLowL' if ridingCart.riderOffset < 0 else 'ridingLowR'
            else:
                spriteName = 'riding'
        elif npcDeathReason:
            spriteName = 'dead'
            deathReason = npcDeathReason
        elif spriteName == '?' and nextToCart( level, row, col ):
            spriteName = 'crouching'

        # Choose sprite frame
        sprite = sprites [ {
            'up'        : 'climbingSprite',
            'down'      : 'climbingSprite',
            'left'      : 'runningLeftSprite',
            'right'     : 'runningRightSprite',
            'dead'      : 'squishedSprite',
            'fall'      : 'fallingSprite',
            'slideR'    : 'slidingRightSprite',
            'slideL'    : 'slidingLeftSprite',
            'bounce'    : 'bouncingSprite',
            'cling'     : 'clingSprite',
            'ridingLowL': 'ridingLowSpriteL',
            'ridingLowR': 'ridingLowSpriteR',
            'riding'    : 'ridingSprite',
            'crouching' : 'crouchingSprite',
            '?'         : 'standingSprite',
        }[ spriteName ] ]
        sprite.setFrame( spriteOffset )
        spriteOffset = spriteOffset + 1

        # Draw the sprite
        thumby.display.drawSprite( sprite )

        # Add message?
        if not chaos:
            showMessage, newMsg = level.checkMsgs( row, col )
            if showMessage:
                messageCount = 3
                msg = newMsg
            if messageCount > 0:
                bgColour = 1 if msg[ -1 ] in '!?' else 0
                fgColour = 1 if bgColour == 0 else 0
                thumby.display.drawFilledRectangle ( 0, 32, thumby.display.width, 8, bgColour )
                thumby.display.drawText( msg, int( thumby.display.width / 2 - len( msg ) * 3 ), 32, fgColour )
                messageCount = messageCount - 1

        # And finally display everything we've done
        thumby.display.update()

        # Extra display when ability gained
        if thisChar in '!*':
            thumby.display.display.invert( 1 )
            thumby.display.update()
            thumby.display.update()
            thumby.display.display.invert( 0 )
            thumby.display.fill( 0 )
            thumby.display.drawText( 'New ability!', 0, 0, 1 )
            if thisChar == '!':
                thumby.display.drawText( 'Jump:', 21, 16, 1 )
                thumby.display.drawText( 'Press UP', 12, 24, 1 )
            else:
                thumby.display.drawText( 'Ride cart:', 6, 16, 1 )
                thumby.display.drawText( 'Cling to ===', 0, 24, 1 )
                thumby.display.drawText( 'Drop in cart', 0, 32, 1 )
            thumby.display.update()
            while not thumby.actionPressed() and not thumby.buttonU.pressed():
                thumby.display.update()

        # Frame rate depends what character is doing
        if spriteName in [ 'left', 'right', 'falling', 'riding', 'ridingLowL', 'ridingLowR', 'cling' ]:
            thumby.display.setFPS( 7 )
        elif spriteName in [ 'up', 'down' ]:
            thumby.display.setFPS( 4 )
        else:
            thumby.display.setFPS( 5 )
except Exception as x:
    try:
        import emulator
        print_exception(x)
    except ImportError:
        with open('/Games/Tinymine/crashdump.log','w',encoding="utf-8") as f:
            print_exception(x,f)
