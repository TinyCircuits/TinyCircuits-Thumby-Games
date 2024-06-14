import time
import thumby
import math

from sys import path
if not '/Games/TinyTunes' in path:
    path.append( '/Games/TinyTunes' )

import buttons

shownInstructions = False

class Key:
    def __init__( self, letter ):
        self.letter = letter
        self.selected = False

    def display( self, x, y ):
        thumby.display.drawFilledRectangle(x, y, 7, 8, 1 if self.selected else 0 )
        thumby.display.drawText( self.letter, x + 1, y, 0 if self.selected else 1 )

    def select( self, selected ):
        self.selected = selected

    def press( self ):
        return self.letter

class DelKey:
    def __init__( self, action ):
        self.selected = False
        self.sprite = thumby.Sprite(
            10, 8, # 2 frames
            bytearray([239,215,187,125,125,85,109,85,125,1,16,40,68,130,130,170,146,170,130,254]),
            0, 0
        )
        self.action = action

    def display( self, x, y ):
        self.sprite.x = x + 2
        self.sprite.y = y
        self.sprite.setFrame( 0 if self.selected else 1 )
        thumby.display.drawSprite( self.sprite )

    def select( self, selected ):
        self.selected = selected

    def press( self ):
        self.action()
        return ''

class KeyRow:
    def __init__( self, rowNum, letters, selected = 0 ):
        self.rowNum = rowNum
        self.keys = []
        for letter in letters:
            self.keys.append( Key( letter ) )
        self.selected = selected
        if selected:
            self.select( selected )

    def select( self, index ):
        rowLen = len( self.keys )
        self.keys[ self.selected ].select( False )
        if index < 0:
            self.selected = rowLen - 1
        elif index >= rowLen:
            self.selected = 0
        else:
            self.selected = index
        self.keys[ self.selected ].select( True )

    def deselect( self ):
        self.keys[ self.selected ].select( False )

    def display( self ):
        for x, key in enumerate( self.keys ):
            key.display( x * 7 + 3 * self.rowNum, self.rowNum * 8 )

    def right( self ):
        self.select( self.selected + 1 )

    def left( self ):
        self.select( self.selected - 1 )

    def getLetter( self ):
        return self.keys[ self.selected ].press()

class Keyboard:
    def __init__( self ):
        self.rows = [
            KeyRow( 0, "1234567890" ),
            KeyRow( 1, "QWERTYUIOP" ),
            KeyRow( 2, "ASDFGHJKL", 4 ),
            KeyRow( 3, "ZXCVBNM" )
        ]
        self.rows[ 3 ].keys.append( DelKey( lambda : self.delKey() ) )
        self.row = 2
        self.output = ''

    def delKey( self ):
        if self.output != '':
            self.output = self.output[ : len( self.output ) - 1 ]

    def display( self ):
        thumby.display.fill( 0 )
        for row in self.rows:
            row.display()
        thumby.display.drawText( self.output, 0, 33, 1 )
        thumby.display.update()

    def handleInput( self ):
        button = buttons.whichButton()
        if not button:
            return None
        if button in 'Uu':
            if self.row > 0:
                index = self.rows[ self.row ].selected
                self.rows[ self.row ].deselect()
                self.row = self.row - 1
                self.rows[ self.row ].select( index )
        elif button in 'Dd':
            if self.row < len( self.rows ) - 1:
                index = self.rows[ self.row ].selected
                self.rows[ self.row ].deselect()
                self.row = self.row + 1
                self.rows[ self.row ].select( index )
        elif button in 'Rr':
            self.rows[ self.row ].right()
        elif button in 'Ll':
            self.rows[ self.row ].left()
        elif button in 'Aa':
            keyOut = self.rows[ self.row ].getLetter()
            self.output = self.output + keyOut
        elif button == 'B':
            result = self.output
            self.output = ''
            return result
        return None

    def instructions( self ):
        global shownInstructions
        shownInstructions = True
        thumby.display.fill( 0 )
        thumby.display.drawText( '  Keyboard:', 0,  0, 1 )
        thumby.display.drawText( 'U/D/L/R:',    0,  8, 1 )
        thumby.display.drawText( '   cursor',   0, 16, 1 )
        thumby.display.drawText( 'A: select',   0, 24, 1 )
        thumby.display.drawText( 'B: OK',       0, 32, 1 )
        while( not thumby.actionJustPressed() ):
            thumby.display.update()

    def getOutput( self ):
        global shownInstructions
        if not shownInstructions:
            self.instructions()
        while True:
            self.display()
            output = self.handleInput()
            if output:
                return output
