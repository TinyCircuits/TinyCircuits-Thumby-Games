import thumby
import time
import random

from sys import path
if not '/Games/TinyTunes' in path:
    path.append( '/Games/TinyTunes' )

import keyboard
import buttons

baseFPS = 8
thumby.saveData.setName( "TinyTunes" )

def splash():
    thumby.display.fill( 0 )
    thumby.display.update()
    thumby.display.drawSprite(
        thumby.Sprite(
            11, 16,
            bytearray([0,0,0,0,252,36,18,18,18,9,255,112,240,248,120,127,0,28,60,62,30,31]),
            3, 1, 0
        )
    )
    thumby.display.setFont( "/lib/font8x8.bin", 8, 8, 1 )
    thumby.display.drawText( "Tiny", 17, 0, 1 )
    thumby.display.drawText( "Tunes", thumby.display.width - 48, 10, 1 )
    thumby.display.update()
    thumby.display.setFont( "/lib/font5x7.bin", 5, 10, 1 )
    thumby.display.update()
    thumby.display.drawText( "Music editor", 1, 22, 1 )
    buttonMsg = 'Help: A   Start: B'
    offset = 0
    strLen = len( buttonMsg ) * 6 + thumby.display.width
    global baseFPS
    thumby.display.setFPS( 45 )
    while True:
        thumby.display.update()
        if thumby.buttonA.justPressed():
            thumby.display.setFPS( baseFPS )
            return True
        if thumby.buttonB.justPressed():
            thumby.display.setFPS( baseFPS )
            return False
        thumby.display.drawFilledRectangle(0, 33, thumby.display.width, 8, 0)
        thumby.display.drawText( buttonMsg, thumby.display.width - offset, 33, 1 )
        offset = ( offset + 1 ) % strLen

def instructions():
    thumby.display.fill( 0 )
    thumby.display.drawText( "Instructions",  0,  0, 1 )
    thumby.display.drawText( "U/D: pitch",    0,  8, 1 )
    thumby.display.drawText( "  L: prev",     0, 16, 1 )
    thumby.display.drawText( "  R: nxt/add",  0, 24, 1 )
    thumby.display.drawText( " -- more --",   0, 32, 1 )
    while not thumby.actionJustPressed():
        thumby.display.update()
    thumby.display.fill( 0 )
    thumby.display.drawText( "A: menu,",     0,  0, 1 )
    thumby.display.drawText( "  choose",     0,  8, 1 )
    thumby.display.drawText( "B: play tune", 0, 16, 1 )
    thumby.display.drawText( "  close menu", 0, 24, 1 )
    thumby.display.drawText( " -- start --", 0, 32, 1 )
    while not thumby.actionJustPressed():
        thumby.display.update()

sprites = {
    'clef' : thumby.Sprite(
        13, 40,
        bytearray([0,0,0,0,0,0,248,62,15,30,248,0,0,0,0,0,0,128,192,255,248,124,31,7,0,0,224,248,126,31,135,227,241,127,240,48,112,240,192,1,15,28,48,99,111,80,64,71,248,32,24,15,0,0,0,0,60,124,252,200,64,96,63,0,0]),
        0, 0, 0
    ),
    'breve' : thumby.Sprite(
        11, 5,
        bytearray([31,0,31,14,18,17,9,14,31,0,31]),
        0, 0, 0
    ),
    'breve_rest' : thumby.Sprite(
        5, 5,
        bytearray([31,31,31,31,31]),
        0, 14, 0
    ),
    'semibreve' : thumby.Sprite(
        5, 5,
        bytearray([14,18,17,9,14]),
        0, 0, 0
    ),
    'semibreve_rest' : thumby.Sprite(
        5, 5,
        bytearray([3,3,3,3,3]),
        0, 14, 0
    ),
    'minim' : thumby.Sprite(
        5, 14,
        bytearray([0,0,0,0,255,28,36,34,18,31]),
        0, 0, 0
    ),
    'minim_rot' : thumby.Sprite(
        5, 14,
        bytearray([254,18,17,9,14,63,0,0,0,0]),
        0, 0, 0
    ),
    'minim_rest' : thumby.Sprite(
        5, 5,
        bytearray([24,24,24,24,24]),
        0, 14, 0
    ),
    'crotchet' : thumby.Sprite(
        5, 14,
        bytearray([0,0,0,0,255,28,60,62,30,31]),
        0, 0, 0
    ),
    'crotchet_rot' : thumby.Sprite(
        5, 14,
        bytearray([254,30,31,15,14,63,0,0,0,0]),
        0, 0, 0
    ),
    'crotchet_rest' : thumby.Sprite(
        5, 13,
        bytearray([97,242,62,28,8,12,30,7,3,2]),
        0, 15, 0
    ),
    'quaver' : thumby.Sprite(
        8, 14,
        bytearray([0,0,0,0,255,14,28,48,28,60,62,30,31,0,0,0]),
        0, 0, 0
    ),
    'quaver_rot' : thumby.Sprite(
        5, 14,
        bytearray([254,30,31,15,14,63,28,14,3,0]),
        0, 0, 0
    ),
    'quaver_rest' : thumby.Sprite(
        5, 11,
        bytearray([6,15,138,116,14,0,6,1,0,0]),
        0, 14, 0
    ),
    'semiquaver' : thumby.Sprite(
        8, 14,
        bytearray([0,0,0,0,255,206,156,48,28,60,62,30,31,1,3,6]),
        0, 0, 0
    ),
    'semiquaver_rot' : thumby.Sprite(
        5, 14,
        bytearray([254,30,159,207,14,63,59,29,6,0]),
        0, 0, 0
    ),
    'semiquaver_rest' : thumby.Sprite(
        7, 16,
        bytearray([192,224,70,143,202,52,14,0,193,49,14,1,0,0]),
        0, 14, 0
    ),
    'sharp' : thumby.Sprite(
        5, 14,
        bytearray([40,126,20,63,10]),
        0, 0, 0
    ),
    'cursor' : thumby.Sprite(
        5, 3,
        bytearray([4,2,1,2,4]),
        48, 37, 0
    ),
    'cursor_rot' : thumby.Sprite(
        5, 3,
        bytearray([1,2,4,2,1]),
        48, 0, 0
    ),
    'slur' : thumby.Sprite(
        7, 3,
        bytearray([4,2,3,3,3,2,4]),
        0, 0, 0
    ),
    'slur_rot' : thumby.Sprite(
        7, 3,
        bytearray([1,2,6,6,6,2,1]),
        0, 0, 0
    )
}

def buzz():
    print( 'BUZZ!' )
    for _ in range( 30 ):
        thumby.audio.playBlocking( random.randint( 400, 500 ), 10 )

class Note:
    def __init__( self, pitch='0', length='16', flags=' ' ):
        self.pitch = int( pitch ) # 0 = C4, one ledger line down on treble clef
        self.length = int( length ) # 16 = crotchet
        self.flags = flags # details tbc

    @classmethod
    def parse( cls, initStr ):
        initElems = initStr.split( '|' )
        return cls( initElems[ 0 ], initElems[ 1 ], initElems[ 2 ] )

    def __repr__( self ):
        return str( self.pitch ) + '|' + str( self.length ) + '|' + self.flags

    def getSprite( self ):
        global sprites
        if 'r' in self.flags:
            spriteName = {
                  4: 'semiquaver_rest',
                  8: 'quaver_rest',
                 16: 'crotchet_rest',
                 32: 'minim_rest',
                 64: 'semibreve_rest',
                128: 'breve_rest',
            } [ self.length ]
        elif self.pitch < 11:
            spriteName = {
                  4: 'semiquaver',
                  8: 'quaver',
                 16: 'crotchet',
                 32: 'minim',
                 64: 'semibreve',
                128: 'breve',
            } [ self.length ]
        else:
            spriteName = {
                  4: 'semiquaver_rot',
                  8: 'quaver_rot',
                 16: 'crotchet_rot',
                 32: 'minim_rot',
                 64: 'semibreve',
                128: 'breve',
            } [ self.length ]
        return sprites[ spriteName ]

    def isSharp( self ):
        return {
            0:  False, # C
            1:  True,  # C#
            2:  False, # D
            3:  True,  # D#
            4:  False, # E
            5:  False, # F
            6:  True,  # F#
            7:  False, # G
            8:  True,  # G#
            9:  False, # A
            10: True,  # A#
            11: False  # B
        } [ self.pitch % 12 ]

    def draw( self, offset ):
        global sprites
        sprite = self.getSprite()
        isSharp = self.isSharp()
        isNotRest = not 'r' in self.flags
        sharpAdj = 0
        if isNotRest:
            spriteHeight = {
                0:  26,  # C4
                1:  26,  # C#
                2:  23,  # D
                3:  23,  # D#
                4:  20,  # E
                5:  17,  # F
                6:  17,  # F#
                7:  14,  # G
                8:  14,  # G#
                9:  11,  # A
                10: 11,  # A#
                11: 8,   # B
                12: 5,   # C
                13: 5,   # C#
                14: 2,   # D
                15: 2,   # D#
                16: -1,  # E
                17: -4,  # F
                18: -4,  # F#
                19: -7,  # G
                20: -7  # G#
            } [ self.pitch ]
            if self.pitch > 10 or self.length > 32:
                spriteHeight = spriteHeight + 9
            else:
                sharpAdj = 9
            sprite.y = spriteHeight
        else:
            spriteHeight = sprite.y
        width = 0
        if isSharp and isNotRest:
            sharpSprite = sprites[ 'sharp' ]
            sharpSprite.x = offset
            sharpSprite.y = spriteHeight - 1 + sharpAdj
            thumby.display.drawSprite( sharpSprite )
            sprite.x = offset + sharpSprite.width
            width = width + sharpSprite.width
        else:
            sprite.x = offset
        thumby.display.drawSprite( sprite )
        width = width + sprite.width
        if 's' in self.flags and isNotRest:
            dotX = sprite.x + 2
            if self.pitch > 10:
                dotY = sprite.y + sprite.height + 1
                if ( dotY - 2 ) % 6 == 0:
                    dotY = dotY + 1
            else:
                dotY = sprite.y - 2
                if dotY % 6 == 0:
                    dotY = dotY - 1
            thumby.display.drawLine( dotX, dotY, dotX, dotY, 1)
        if 'z' in self.flags and isNotRest:
            if self.pitch > 10:
                slurSprite = sprites[ 'slur_rot' ]
                slurSprite.y = sprite.y + sprite.height + 1
            else:
                slurSprite = sprites[ 'slur' ]
                slurSprite.y = sprite.y - 4
            slurSprite.x = sprite.x + sprite.width - 3
            thumby.display.drawSprite( slurSprite )
        if '.' in self.flags:
            dotX = sprite.x + sprite.width + 1
            dotY = spriteHeight + sharpAdj
            if ( dotY - 2 ) % 6 == 0:
                dotY = dotY + 2
            thumby.display.drawLine( dotX, dotY, dotX, dotY, 1)
            width = width + 1
        return width

    def width( self ):
        width = self.getSprite().width
        if self.isSharp():
            global sprites
            width = width + sprites[ 'sharp' ].width
        if '.' in self.flags:
            width = width + 1
        return width

    def play( self ):
        totalMillis = 15.625 * self.length + 0.5
        if '.' in self.flags:
            totalMillis = totalMillis * 1.5
        if not 'r' in self.flags:
            if 'z' in self.flags:
                soundMillis = totalMillis * 1.1
            elif 's' in self.flags:
                soundMillis = totalMillis * 0.75
            else:
                soundMillis = totalMillis * 0.95
            thumby.audio.play(
                int(
                    261.63 *
                        pow(
                            1.059463094359,
                            self.pitch
                        )
                ),
                int( soundMillis )
            )
        time.sleep( totalMillis / 1000 )

    def raisePitch( self ):
        if self.pitch < 20:
            self.pitch = self.pitch + 1
        else:
            buzz()

    def lowerPitch( self ):
        if self.pitch > 0:
            self.pitch = self.pitch - 1
        else:
            buzz()

    def shorten( self ):
        if self.length > 4:
            self.length = int( self.length / 2 )
        else:
            buzz()

    def lengthen( self ):
        if self.length < 128:
            self.length = int( self.length * 2 )
        else:
            buzz()

    def dot( self ):
        if '.' in self.flags:
            self.flags = self.flags.replace( '.', '' )
        else:
            self.flags = self.flags + '.'

    def rest( self ):
        if 'r' in self.flags:
            self.flags = self.flags.replace( 'r', '' )
        else:
            self.flags = self.flags + 'r'

    def staccato( self ):
        if 's' in self.flags:
            self.flags = self.flags.replace( 's', '' )
        else:
            self.flags = self.flags + 's'
            if 'z' in self.flags:
                self.flags = self.flags.replace( 'z', '' )

    def zlur( self ):
        if 'z' in self.flags:
            self.flags = self.flags.replace( 'z', '' )
        else:
            self.flags = self.flags + 'z'
            if 's' in self.flags:
                self.flags = self.flags.replace( 's', '' )

class Tune:
    def __init__( self, initString = None ):
        self.notes = []
        if initString:
            for noteStr in initString.split( ',' ):
                self.notes.append( Note.parse( noteStr ) )
        else:
            self.notes.append( Note() )
        self.note = 0

    def __repr__( self ):
        return ','.join( map( repr, self.notes ) )

    def play( self ):
        self.note = 0
        self.playHere()

    def playHere( self ):
        thumby.display.setFPS( 60 )
        for note in self.notes[ self.note : ]:
            self.display();
            self.note = self.note + 1
            note.play()
        self.note = self.note - 1
        global baseFPS
        thumby.display.setFPS( baseFPS )

    def raisePitch( self ):
        self.notes[ self.note ].raisePitch()

    def lowerPitch( self ):
        self.notes[ self.note ].lowerPitch()

    def prev( self ):
        if self.note > 0:
            self.note = self.note - 1
        else:
            buzz()

    def next( self, allowDuplicate ):
        if self.note < len( self.notes ) - 1:
            self.note = self.note + 1
        elif allowDuplicate:
            self.duplicate()
        else:
            buzz()

    def shorten( self ):
        self.notes[ self.note ].shorten()

    def lengthen( self ):
        self.notes[ self.note ].lengthen()

    def dot( self ):
        self.notes[ self.note ].dot()

    def duplicate( self ):
        note = self.notes[ self.note ]
        newNote = Note()
        newNote.pitch = note.pitch
        newNote.length = note.length
        newNote.flags = note.flags
        self.notes.insert( self.note, newNote )
        self.note = self.note + 1

    def delete( self ):
        if len( self.notes ) > 1:
            self.notes.pop( self.note )
            if self.note >= len( self.notes ):
                self.note = len( self.notes ) - 1
        else:
            buzz()

    def rest( self ):
        self.notes[ self.note ].rest()

    def staccato( self ):
        self.notes[ self.note ].staccato()

    def zlur( self ):
        self.notes[ self.note ].zlur()

    def toStart( self ):
        self.note = 0

    def toEnd( self ):
        self.note = len( self.notes ) - 1

    def display( self ):
        thumby.display.fill( 0 )
        thumby.display.drawLine( 0,  7, thumby.display.width,  7, 1 )
        thumby.display.drawLine( 0, 13, thumby.display.width, 13, 1 )
        thumby.display.drawLine( 0, 19, thumby.display.width, 19, 1 )
        thumby.display.drawLine( 0, 25, thumby.display.width, 25, 1 )
        thumby.display.drawLine( 0, 31, thumby.display.width, 31, 1 )
        global sprites
        clef = sprites[ 'clef' ]
        offsets = [ 0, clef.width + 2 ]
        leftWidth = offsets[ 1 ]
        for note in self.notes[ : self.note ]:
            leftWidth = leftWidth + note.width() + 2
            offsets.append( leftWidth )
        offsets = [ w - leftWidth + 48 for w in offsets ]
        if offsets[ 0 ] >= - clef.width:
            clef.x = offsets[ 0 ]
            thumby.display.drawSprite( clef )
        for noteIndex, note in enumerate( self.notes[ : self.note ] ):
            note = self.notes[ noteIndex ]
            notePos = offsets[ noteIndex ] + 1
            if notePos >= -5 - note.width():
                note.draw( offsets[ noteIndex + 1 ] )
        # I'm sure that this could have been done in one go.
        # But I only worked out positions for the notes to the
        # left of the current note. So now I do the remainder.
        noteIndex = self.note
        currentOffset = 48
        while noteIndex < len( self.notes ) and currentOffset <= 72:
            note = self.notes[ noteIndex ]
            currentOffset = currentOffset + note.draw( currentOffset ) + 2
            noteIndex = noteIndex + 1
        if self.notes[ self.note ].pitch < 19:
            thumby.display.drawSprite( sprites[ 'cursor_rot' ] )
        if self.notes[ self.note ].pitch > 3:
            thumby.display.drawSprite( sprites[ 'cursor' ] )
        thumby.display.update()

class Menu:
    def __init__( self, items ):
        self.items = items
        self.count = len( items )
        self.item = 0

    def handleButton( self, button ):
        if not button:
            return
        if button in 'Uu':
            if self.item > 0:
                self.item = self.item - 1
            return False
        if button in 'Dd':
            if self.item < len( self.items ) - 1:
                self.item = self.item + 1
            return False
        if button == 'A':
            self.items[ self.item ][ 1 ]()
            return True
        if button == 'B':
            return True
        return False

    def displayItems( self ):
        result = []
        result.append( None if self.item < 2 else self.items[ self.item - 2 ][ 0 ] )
        result.append( None if self.item < 1 else self.items[ self.item - 1 ][ 0 ] )
        result.append( self.items[ self.item ][ 0 ] )
        result.append( None if self.item + 1 >= self.count else self.items[ self.item + 1 ][ 0 ] )
        result.append( None if self.item + 2 >= self.count else self.items[ self.item + 2 ][ 0 ] )
        return result

    def display( self ):
        thumby.display.fill( 0 )
        itemY = 0
        for item in self.displayItems():
            if item:
                thumby.display.drawText( '>' + item if itemY == 16 else ' ' + item, 1, itemY, 1 )
            itemY = itemY + 8
        thumby.display.update()

class Editor:
    def __init__( self ):
        self.dirName = '.'
        self.tune = Tune()
        self.fileName = None
        if thumby.saveData.hasItem( self.dirName ):
            self.directory = thumby.saveData.getItem( self.dirName ).split( '|' )
        else:
            self.loadSampleTunes()
        self.menuMode = False
        self.menu = Menu(
            [
                ( 'Shorten',     lambda: self.tune.shorten()  ),
                ( 'Lengthen',    lambda: self.tune.lengthen() ),
                ( 'Note...',     lambda: self.menuNote()      ),
                ( 'To start',    lambda: self.tune.toStart()  ),
                ( 'To end',      lambda: self.tune.toEnd()    ),
                ( 'Play here',   lambda: self.tune.playHere() ),
                ( 'Save...',     lambda: self.menuSave()      ),
                ( 'Load...',     lambda: self.load()          ),
                ( 'Del save...', lambda: self.delete()        ),
                ( 'New tune...', lambda: self.confirmNew()    ),
                ( 'Exit',        lambda: thumby.reset()       )
            ]
        )
        self.noteMenu = Menu(
            [
                ( 'Duplicate',   lambda: self.tune.duplicate() ),
                ( '+/- Dot',     lambda: self.tune.dot()       ),
                ( '+/- Rest',    lambda: self.tune.rest()      ),
                ( '+/- Stacca.', lambda: self.tune.staccato()  ),
                ( '+/- Slur',    lambda: self.tune.zlur()      ),
                ( 'Delete note', lambda: self.tune.delete()    ),
            ]
        )

    def loadSampleTunes( self ):
        self.directory = []
        self.loadSampleTune( self.directory, 'RAINBOW',    '4|64| ,16|64| ,15|32| ,11|16| ,13|16| ,15|32| ,16|32| ,4|64| ,13|64| ,11|64| .,1|64| ,9|64| ,8|32| ,4|16| ,6|16| ,8|32| ,9|32| ,6|32| ,1|16| ,4|16| ,6|32| ,8|32| ,4|64| ' )
        self.loadSampleTune( self.directory, 'DECK',       '12|32| ,10|8| ,9|16| ,7|16| ,5|16| ,7|16| ,9|16| ,5|16| ,7|8| ,9|8| ,10|8| ,7|8| ,9|32| ,7|8| ,5|16| ,4|16| ,5|64| ' )
        self.loadSampleTune( self.directory, 'FURELISE',   '16|16| ,15|16| ,16|16| ,15|16| ,16|16| ,11|16| ,14|16| ,12|16| ,9|64| ,0|16| ,4|16| ,9|16| ,11|64| ,4|16| ,8|16| ,11|16| ,12|32| ' )
        self.loadSampleTune( self.directory, 'DOGGIE',     '7|16| ,12|16| ,7|16| ,4|16| ,0|16| .,9|8| ,7|8| ,4|8| ,7|16| ,2|32| z,2|16| ,2|16| r,7|16| ,11|16| ,9|16| ,7|16| ,5|16| ,11|16| ,9|16| ,7|32| .z,7|16| ,7|16| r,7|16| ,12|16| ,7|16| ,4|16| ,0|16| .,9|8| ,7|8| ,4|8| ,7|16| ,2|32| z,2|16| ,2|16| r,7|16| ,11|16| ,9|16| ,7|16| ,5|16| ,4|16| ,2|16| ,0|64| .' )
        self.loadSampleTune( self.directory, 'SMOKE',      '2|32| s,5|32| s,7|32| s,8|16| r,2|32| s,5|32| s,8|16| s,7|16| .,7|16| r.,2|32| s,5|32| s,7|32| s,7|16| sr,5|32| s,2|32| s.' )
        self.loadSampleTune( self.directory, 'SMOKEJOLLY', '2|8| ,2|8| r,5|8| ,5|8| r,7|16| .,2|8| ,2|8| r,5|8| ,5|8| r,9|8| ,7|32| ,2|8| ,2|8| r,5|8| ,5|8| r,7|16| .,5|8| ,5|8| r,2|32| .' )
        thumby.saveData.setItem( self.dirName, '|'.join( self.directory ) )
        thumby.saveData.save()

    def loadSampleTune( self, dir, name, tuneString ):
        thumby.saveData.setItem( name, tuneString )
        dir.append ( name )

    def menuNote( self ):
        self.noteMenu.display()
        while not self.noteMenu.handleButton( buttons.whichButton() ):
            self.noteMenu.display()

    def menuSave( self ):
        if self.fileName:
            saveMenu = Menu(
                [
                    ( self.fileName, lambda: self.saveReplace() ),
                    ( 'Save as...',  lambda: self.saveAs()      )
                ]
            )
            saveMenu.display()
            while not saveMenu.handleButton( buttons.whichButton() ):
                saveMenu.display()
        else:
            self.saveAs()

    def saveAs( self ):
        tempFileName = keyboard.Keyboard().getOutput()
        print( 'Name is ' + tempFileName )
        if tempFileName in self.directory:
            print( 'Name ' + tempFileName + ' found in directory' )
            confirmMenu = Menu(
                [
                    ( 'Cancel',  lambda: None                              ),
                    ( 'Replace', lambda: self.saveWithName( tempFileName ) )
                ]
            )
            while not confirmMenu.handleButton( buttons.whichButton() ):
                confirmMenu.display()
        else:
            self.fileName = tempFileName
            print( 'Saving as ' + self.fileName )
            if not self.fileName in self.directory:
                print( 'Writing directory entry for ' + self.fileName )
                self.directory.append( self.fileName )
                self.writeDir()
            print( 'Writing tune for ' + self.fileName )
            thumby.saveData.setItem( self.fileName, str( self.tune ) )
            thumby.saveData.save()

    def saveWithName( self, fileName ):
        self.fileName = fileName
        self.saveReplace()

    def saveReplace( self ):
        print( 'Replacing ' + self.fileName )
        if not self.fileName in self.directory:
            print( 'Writing directory entry for ' + self.fileName )
            self.directory.append( self.fileName )
            self.writeDir()
        print( 'Writing tune for ' + self.fileName )
        thumby.saveData.setItem( self.fileName, str( self.tune ) )
        thumby.saveData.save()

    def writeDir( self ):
        thumby.saveData.setItem( self.dirName, '|'.join( self.directory ) )

    def load( self ):
        def makeLambda( fileName ):
            return lambda: self.loadName( fileName )
        loadMenuItems = []
        for dirItem in self.directory:
            loadMenuItems.append( ( dirItem, makeLambda( dirItem ) ) )
        if len( loadMenuItems ) == 0:
            self.noTunes()
        else:
            loadMenu = Menu( loadMenuItems )
            loadMenu.display()
            while not loadMenu.handleButton( buttons.whichButton() ):
                loadMenu.display()

    def noTunes( self ):
        thumby.display.fill( 0 )
        thumby.display.drawText( 'No tunes',     10,  9, 1 )
        thumby.display.drawText( 'A/B continue',  0, 25, 1 )
        while not thumby.actionJustPressed():
            thumby.display.update()

    def loadName( self, name ):
        if thumby.saveData.hasItem( name ):
            self.tune = Tune( thumby.saveData.getItem( name ) )
            self.fileName = name
        else:
            buzz()

    def delete( self ):
        def makeLambda( fileName ):
            return lambda: self.deleteName( fileName )
        deleteMenuItems = []
        for dirItem in self.directory:
            deleteMenuItems.append( ( dirItem, makeLambda( dirItem ) ) )
        if len( deleteMenuItems ) == 0:
            self.noTunes()
        else:
            deleteMenu = Menu( deleteMenuItems )
            deleteMenu.display()
            while not deleteMenu.handleButton( buttons.whichButton() ):
                deleteMenu.display()

    def deleteName( self, name ):
        if thumby.saveData.hasItem( name ):
            thumby.saveData.delItem( name )
        else:
            buzz()
        if name in self.directory:
            self.directory.remove( name )
        self.writeDir()
        thumby.saveData.save()

    def confirmNew( self ):
        confirmMenu = Menu(
            [
                ( 'No, keep', lambda: None           ),
                ( 'Yes, new', lambda: self.newTune() )
            ]
        )
        confirmMenu.display()
        while not confirmMenu.handleButton( buttons.whichButton() ):
            confirmMenu.display()

    def newTune( self ):
        self.tune = Tune()
        self.fileName = None

    def handleInput( self ):
        button = buttons.whichButton()
        if not button:
            return
        if self.menuMode:
            if self.menu.handleButton( button ):
                self.menuMode = False
        elif button in 'Uu':
            self.tune.raisePitch()
        elif button in 'Dd':
            self.tune.lowerPitch()
        elif button in 'Ll':
            self.tune.prev()
        elif button == 'R':
            self.tune.next( True )
        elif button == 'r':
            self.tune.next( False )
        elif button == 'B':
            self.tune.play()
        elif button == 'A':
            self.menuMode = True

    def display( self ):
        if self.menuMode:
            self.menu.display()
        else:
            self.tune.display()

thumby.display.setFPS( baseFPS )
if splash():
    instructions()
editor = Editor()
while True:
    editor.handleInput()
    editor.display()
