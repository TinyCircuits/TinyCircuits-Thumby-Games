from thumbyGraphics import display
from thumbySprite import Sprite
from re import search
from thumbyAudio import audio
from random import randint

DIR = '/Games/TinySh'

from sys import path
if not DIR in path:
    path.append( DIR )
import sh_btn
from sh_utility import defaultFont

shownKbInstructions=False

class Key:
    def __init__( self, character ):
        self.character = character
        self.selected = False

    def display( self, x, y ):
        if self.character==' ':
            if self.selected:
                display.drawFilledRectangle( x, y, 16, 8, 1 )
            display.setFont( "/lib/font3x5.bin", 3, 5, 1 )
            display.drawText( '[sp]', x + 1, y + 2, 0 if self.selected else 1 )
            defaultFont()
            return 16
        if self.selected:
            display.drawFilledRectangle( x, y, 7, 8, 1 )
        display.drawText( self.character, x + 1, y, 0 if self.selected else 1 )
        return 7

    def select( self, selected ):
        self.selected = selected

    def press( self ):
        return self.character

class ActionKey:
    def __init__( self, action, sprite ):
        self.selected = False
        self.sprite = sprite
        self.action = action

    def display( self, x, y ):
        self.sprite.x = x
        self.sprite.y = y
        self.sprite.setFrame( 0 if self.selected else 1 )
        display.drawSprite( self.sprite )
        return self.sprite.width

    def select( self, selected ):
        self.selected = selected

    def press( self ):
        ch = self.action()
        return ch if ch else ''

class KeyRow:
    def __init__( self, rowNum, characters, selected = 0 ):
        self.rowNum = rowNum
        self.keys = []
        for character in characters:
            self.keys.append( Key( character ) )
        self.selected = selected
        if selected:
            self.select( selected )

    def append( self, key ):
        self.keys.append( key )

    def insert( self, index, key ):
        self.keys.insert( index, key )

    def select( self,index ):
        self.keys[ self.selected ].select( False )
        if index < 0:
            self.selected = len( self.keys ) - 1
        elif index >= len( self.keys ):
            self.selected = 0
        else:
            self.selected = index
        self.keys[ self.selected ].select( True )

    def deselect( self ):
        self.keys[ self.selected ].select( False )

    def display( self ):
        offset = self.rowNum
        for i, key in enumerate( self.keys ):
            offset = offset + key.display( offset, self.rowNum * 8 )

    def right( self ):
        self.select( self.selected + 1 )

    def left( self ):
        self.select( self.selected - 1 )

    def getCharacter( self ):
        return self.keys[ self.selected ].press()

class KeyLayer:
    def __init__( self, characterRows ):
        self.rows=[]
        for i, characterRow in enumerate( characterRows ):
            self.rows.append( KeyRow( i, characterRow ) )
        self.row = 3

    def add( self, key, rowNum ):
        self.rows[ rowNum ].append( key )

    def insert( self, key, rowNum, index ):
        self.rows[ rowNum ].insert( index, key )

    def display( self ):
        for row in self.rows:
            row.display()

    def up( self ):
        if self.row > 0:
            index = self.rows[ self.row ].selected
            self.rows[ self.row ].deselect()
            self.row = self.row - 1
            self.rows[ self.row ].select( index )

    def down( self ):
        if self.row < len( self.rows ) - 1:
            index = self.rows[ self.row ].selected
            self.rows[ self.row ].deselect()
            self.row = self.row + 1
            self.rows[ self.row ].select( index )

    def left( self ):
        self.rows[ self.row ].left()

    def right( self ):
        self.rows[ self.row ].right()

    def getCharacter( self ):
        return self.rows[ self.row ].getCharacter();

class Keyboard:
    def __init__( self, getSprite, text = "", position = 0, layer = 0 ):
        self.layers = [
            KeyLayer( [ 'qwertyuiop', 'asdfghjkl',  'zxcvbnm,.', ' ' ] ),
            KeyLayer( [ 'QWERTYUIOP', 'ASDFGHJKL',  'ZXCVBNM()', ' ' ] ),
            KeyLayer( [ '1234567890', '!"#$%^&*[]', "`_+-=;:@'~",' ' ] ),
            KeyLayer( [ '1234567890', '#<>?/|\\{}', '',          ' ' ] )
        ]
        shiftKey = ActionKey( lambda:self.shiftKey(), getSprite( 'shiftKey' ) )
        shiftKey.selected = True
        tabKey = ActionKey( lambda:'\t', getSprite( 'tabKey' ) )
        for i in range( 4 ):
            self.layers[ i ].insert( tabKey, 3, 0 )
            self.layers[ i ].insert( shiftKey, 3, 0 )

        leftArrowKey = ActionKey( lambda:self.leftArrow(), getSprite( 'leftArrowKey' ) )
        rightArrowKey = ActionKey( lambda:self.rightArrow(), getSprite( 'rightArrowKey' ) )
        for i in range( 4 ):
            self.layers[ i ].add( leftArrowKey, 3 )
            self.layers[ i ].add( rightArrowKey, 3 )

        self.layers[ 3 ].add( ActionKey( lambda:self.leftDelEnd(), getSprite( 'leftDelEndKey' ) ), 2 )

        leftDelWordKey = ActionKey( lambda:self.leftDelWord(), getSprite( 'leftDelWordKey' ) )
        for i in range( 3 ):
            self.layers[ i ].add( leftDelWordKey, 3 )
        self.layers[ 3 ].add( leftDelWordKey, 2 )

        delKey=ActionKey( lambda:self.delKey(), getSprite( 'leftDelKey' ) )
        for i in range( 3 ):
            self.layers[ i ].add( delKey, 3 )
        self.layers[ 3 ].add( delKey, 2 )

        self.layers[ 3 ].add( ActionKey( lambda:self.rightDel(),     getSprite( 'rightDelKey'     ) ), 2 )
        self.layers[ 3 ].add( ActionKey( lambda:self.rightDelWord(), getSprite( 'rightDelWordKey' ) ), 2 )
        self.layers[ 3 ].add( ActionKey( lambda:self.rightDelEnd(),  getSprite( 'rightDelEndKey'  ) ), 2 )

        self.layer = layer
        self.text = text
        self.cursor = min( position + 6, len( text ) )

    def shiftKey( self ):
        self.layer = self.layer + 1
        if self.layer >= len( self.layers ):
            self.layer = 0

    def delKey( self ):
        if self.cursor > 0:
            self.text = self.text[ 0 : self.cursor - 1 ] + self.text[ self.cursor : ]
            self.cursor = self.cursor - 1
        else:
            buzz()

    def rightDel( self ):
        if self.cursor < len( self.text ):
            self.text = self.text[ 0 : self.cursor ] + self.text[ self.cursor + 1 : ]
        else:
            buzz()

    def leftDelWord( self ):
        pre = self.text[ 0 : self.cursor ]
        match = search( r'(\w+|\W+)$', pre )
        if match:
            start = match.start()
            self.text = pre[ 0 : start ] + self.text[ self.cursor : ]
            self.cursor = start
        else:
            buzz()

    def rightDelWord( self ):
        post = self.text[ self.cursor : ]
        match = search( r'^(\w+|\W+)', post )
        if match:
            end = match.end()
            self.text = self.text[ 0 : self.cursor ] + post[ end : ]
        else:
            buzz()

    def leftDelEnd( self ):
        self.text = self.text[ self.cursor : ]
        self.cursor = 0

    def rightDelEnd( self ):
        self.text = self.text[ 0 : self.cursor ]

    def leftArrow( self ):
        if self.cursor > 0:
            self.cursor = self.cursor - 1

    def rightArrow( self ):
        if self.cursor < len( self.text ):
            self.cursor = self.cursor + 1

    def display( self ):
        display.fill( 0 )
        self.layers[ self.layer ].display()
        textLen = len( self.text )
        if textLen <= 10:
            windowStart = 0
            windowEnd = len( self.text )
        elif self.cursor <= 6:
            windowStart = 0
            windowEnd = min( 10, textLen )
        else:
            windowStart = self.cursor - 6
            windowEnd = min( textLen, self.cursor + 4 )
        windowText = self.text[ windowStart : windowEnd ]
        if windowStart > 0:
            display.drawText( '<', 0, 33, 1 )
        adjCursor = self.cursor - windowStart
        for i, ch in enumerate( windowText ):
            x = 6 * i + 6
            if i == adjCursor:
                display.drawFilledRectangle( x, 33, 6, 8, 1 )
                colour = 0
            else:
                colour = 1
            display.drawText( ch, x, 33, colour )
        if self.cursor == textLen:
            display.drawFilledRectangle( adjCursor * 6 + 6, 33, 6, 8, 1 )
        if textLen > windowEnd:
            display.drawText( '>', 66, 33, 1 )
        display.update()

    def handleInput( self ):
        b = sh_btn.which()
        if not b:
            return None
        if b in 'Uu':
            self.layers[ self.layer ].up()
        elif b in 'Dd':
            self.layers[ self.layer ].down()
        elif b in 'Rr':
            self.layers[ self.layer ].right()
        elif b in 'Ll':
            self.layers[ self.layer ].left()
        elif b in 'Aa':
            self.handlePress()
        elif b == 'B':
            result = self.text
            self.text = ''
            return result
        return None

    def handlePress( self ):
        keyOut = self.layers[ self.layer ].getCharacter()
        if len( keyOut ) > 0:
            self.text = self.text[ 0 : self.cursor ] + keyOut + self.text[ self.cursor : ]
            self.cursor = self.cursor + 1

    def instructions( self ):
        global shownKbInstructions
        shownKbInstructions = True
        display.fill( 0 )
        display.drawText( 'Keyboard:', 12, 0, 1 )
        display.drawText( 'U', 6, 8, 1 )
        display.drawText( 'L R cursor', 0, 16, 1 )
        display.drawText( 'D', 6, 24, 1 )
        display.drawText( '--more--', 12, 32, 1 )
        while( not sh_btn.actionJustPressed() ):
            display.update()
        display.fill( 0 )
        display.drawText( 'Keyboard:', 12, 0, 1 )
        display.drawText( 'A: press key', 0, 8, 1 )
        display.drawText( 'B: close', 0, 16, 1 )
        display.drawText( '--start--', 6, 32, 1 )
        while( not sh_btn.actionJustPressed() ):
            display.update()

    def getOutput( self ):
        global shownKbInstructions
        if not shownKbInstructions:
            self.instructions()
        while True:
            self.display()
            output = self.handleInput()
            if output or output == '':
                return output
