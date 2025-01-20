from thumbyGraphics import display as d
from thumbySprite import Sprite
from os import ilistdir
from sys import path
if not '/Games/TinyEdit' in path:
    path.append( '/Games/TinyEdit' )
import te_btn
from te_utility import buzz, sideScroll, getDirAbove
from te_menu import Menu
from filechunks import FileChunks

class Mode:
    MENU   = 1
    SCROLL = 2
    MOVE   = 3
    SPLIT  = 4

class File:
    def __init__( self, fileName, keyboardGetter, spriteGetter ):
        self.fileName = fileName if fileName else ""
        self.fileChunks = FileChunks( self.fileName )
        self.position = 0
        self.splitPosition = -1
        self.getKeyboard = keyboardGetter
        self.getSprite = spriteGetter

    def getCurrentLineIndex( self ):
        return self.fileChunks.getCurrentLineIndex()

    def getDisplayLine( self, index ):
        if index < 0 or index >= self.fileChunks.lineCount():
            return None
        return self.fileChunks.getLine( index ).getText( self.position )

    def getDisplayLines( self ):
        line = self.fileChunks.getCurrentLineIndex()
        return[
            self.getDisplayLine( line - 2 ),
            self.getDisplayLine( line - 1 ),
            self.getDisplayLine( line     ),
            self.getDisplayLine( line + 1 ),
            self.getDisplayLine( line + 2 )
        ]

    def getFullLine( self, index = None ):
        if index == None:
            return self.fileChunks.getCurrentLine().text
        if index < 0 or index >= self.fileChunks.lineCount():
            return None
        return self.fileChunks.getLine( index ).text

    def display( self, mode ):
        d.fill( 0 )
        leftArrowKey = self.getSprite( 'leftArrowKey' )
        rightArrowKey = self.getSprite( 'rightArrowKey' )
        if mode == Mode.SPLIT:
            leftArrowKey.setFrame( 1 )
            rightArrowKey.setFrame( 1 )
        lineY = 0
        moveIcon = Sprite( 5, 11,
            bytearray([68,198,255,198,68,0,0,1,0,0]),
            0, 16, 0 )
        for line in self.getDisplayLines():
            if line:
                if lineY == 16:
                    if mode == Mode.MOVE:
                        d.drawText( line, 1, lineY, 1 )
                        d.drawRectangle( 6, lineY, d.width - 12, 8, 1 )
                        d.drawFilledRectangle( 0, lineY, 6, 7, 0 )
                        moveIcon.x = 0
                        d.drawSprite( moveIcon )
                        d.drawFilledRectangle( d.width - 6, lineY, 6, 7, 0 )
                        moveIcon.x = d.width - 5
                        d.drawSprite( moveIcon )
                    elif mode == Mode.SPLIT:
                        d.drawText( line, 1, lineY, 1 )
                        top = lineY - 1
                        rhs = d.width - 7
                        d.drawLine( 6, top, rhs, top, 1 )
                        d.drawFilledRectangle( 0, lineY, 6, 7, 0 )
                        leftArrowKey.x = 0
                        leftArrowKey.y = lineY
                        d.drawSprite( leftArrowKey )
                        d.drawLine( 6, lineY, 6, lineY + 7, 1 )
                        d.drawFilledRectangle( rhs, lineY, 6, 7, 0 )
                        rightArrowKey.x = rhs
                        rightArrowKey.y = lineY
                        d.drawSprite( rightArrowKey )
                        d.drawLine( rhs, lineY, rhs, lineY + 7, 1 )
                    else:
                        d.drawFilledRectangle( 0, 16, d.width, 8, 1 )
                        d.drawText( line, 1, lineY, 0 )
                else:
                    d.drawText( line, 1, lineY, 1 )
                if lineY == 24 and mode == Mode.SPLIT:
                    d.drawFilledRectangle( 0, lineY, 6, 7, 0 )
                    leftArrowKey.y = lineY
                    d.drawSprite( leftArrowKey )
                    d.drawLine( 6, lineY, 6, lineY + 7, 1 )
                    rhs = d.width - 7
                    bottom = lineY + 7
                    d.drawLine( 6, bottom, rhs, bottom, 1 )
                    d.drawFilledRectangle( rhs, lineY, 6, 7, 0 )
                    rightArrowKey.y = lineY
                    d.drawSprite( rightArrowKey )
                    d.drawLine( rhs, bottom, rhs, lineY, 1 )
            lineY = lineY + 8
        d.update()

    def goTo( self, line ):
        if line >= 0 and line < self.fileChunks.lineCount():
            self.fileChunks.setCurrentLineIndex( line )
        else:
            buzz()

    def up( self ):
        line = self.fileChunks.getCurrentLineIndex()
        if line > 0:
            self.fileChunks.setCurrentLineIndex( line - 1 )

    def down( self ):
        line = self.fileChunks.getCurrentLineIndex()
        if line + 1 < self.fileChunks.lineCount():
            self.fileChunks.setCurrentLineIndex( line + 1 )

    def moveUp( self ):
        line = self.fileChunks.getCurrentLineIndex()
        if line > 0:
            self.fileChunks.moveUp()
        else:
            buzz()

    def moveDown( self ):
        line = self.fileChunks.getCurrentLineIndex()
        if line < self.fileChunks.lineCount() - 1:
            self.fileChunks.moveDown()
        else:
            buzz()

    def left( self ):
        if self.position > 0:
            self.position = self.position - 1

    def right( self ):
        self.position = self.position + 1

    def setPosition( self, position ):
        if position >= 0:
            self.position = position
        else:
            buzz()

    def replaceLine( self, newText ):
        self.fileChunks.replaceCurrentLine( newText )

    def deleteLine( self ):
        self.fileChunks.deleteCurrentLine()

    def joinNext( self ):
        if self.fileChunks.getCurrentLineIndex() < self.fileChunks.lineCount() - 1:
            nextLine = self.getCurrentLineIndex() + 1
            self.replaceLine( self.getFullLine() + ' ' + self.getFullLine( nextLine ) )
            self.goTo( nextLine )
            self.deleteLine()
            self.goTo( nextLine - 1 )
        else:
            buzz()

    def startSplit( self ):
        originalLine = self.getFullLine()
        lenOriginalLine = len( originalLine )
        if self.position + 6 > lenOriginalLine:
            self.position = max( lenOriginalLine - 6, 0 )
        self.splitPosition = min( self.position + 6, lenOriginalLine )
        self.duplicateLine()
        self.replaceLine( self.getFullLine()[ self.splitPosition : ] )
        self.up()
        self.replaceLine( originalLine[ 0 : self.splitPosition ] )

    def shiftSplitLeft( self ):
        currentText = self.getFullLine()
        nextText = self.getFullLine( self.getCurrentLineIndex() + 1 )
        if self.splitPosition > 0:
            self.down()
            self.replaceLine( currentText[ -1 ] + nextText )
            self.up()
            self.replaceLine( currentText[ 0 : -1 ] )
            if self.position > 0:
                self.position = self.position - 1
            self.splitPosition = self.splitPosition - 1
        else:
            buzz()

    def shiftSplitRight( self ):
        currentText = self.getFullLine()
        nextText = self.getFullLine( self.getCurrentLineIndex() + 1 )
        if len( nextText ) > 0:
            self.replaceLine( currentText + nextText[ 0 ] )
            self.down()
            self.replaceLine( nextText[ 1 : ] )
            self.up()
            if self.splitPosition > 6:
                self.position = self.position + 1
            self.splitPosition = self.splitPosition + 1
        else:
            buzz()

    def duplicateLine( self ):
        self.fileChunks.duplicateCurrentLine()
        self.down()

    def insertLine( self ):
        self.fileChunks.insertLine( "" )

    def save( self, dir ):
        if not self.fileName:
            self.fileName = dir + '/' + self.getKeyboard( self.getSprite, "", 0 ).getOutput()
        with open( self.fileName, 'w', encoding = "utf-8" ) as f:
            self.fileChunks.writeTo( f )

    def close ( self ):
        self.fileChunks.close()

class Editor:
    def __init__( self, keyboardGetter, spriteGetter, log = None, filePath = None ):
        if log: log( 'Editor __init__ start' )
        self.getKeyboard = keyboardGetter
        self.getSprite = spriteGetter
        self.mode = Mode.MENU
        self.file = None
        self.dir = ''
        self.findStr = ''
        self.findLine = 0
        self.noFileMenu = Menu( [
            ( 'Open...', lambda: self.open() ),
            ( 'Help',    lambda: self.hlp()  ),
            ( 'Exit',    lambda: True        )
        ] )
        self.withFileMenu = Menu( [
            ( 'File...', lambda: self.fileMenu.display() ),
            ( 'Line...', lambda: self.lineMenu.display() ),
            ( 'Help',    lambda: self.hlp()              ),
            ( 'Exit',    lambda: self.exit()             )
        ] )
        self.fileMenu = Menu( [
            ( 'Open...', lambda: self.open() ),
            ( 'Save...', lambda: self.save() ),
            ( 'New...',  lambda: self.new()  )
        ] )
        self.lineMenu = Menu( [
            ( 'Insert',   lambda: self.file.insertLine()    ),
            ( 'Duplicate',lambda: self.file.duplicateLine() ),
            ( 'Move',     lambda: self.move()               ),
            ( 'Find...',  lambda: self.find()               ),
            ( 'Find next',lambda: self.findNext()           ),
            ( 'Go to...', lambda: self.goTo()               ),
            ( 'Join next',lambda: self.file.joinNext()      ),
            ( 'Split',    lambda: self.split()              ),
            ( 'Delete',   lambda: self.file.deleteLine()    )
        ])
        if filePath:
            self.open( filePath )
            self.mode = Mode.SCROLL
        if log: log( 'Editor __init__ end' )

    def save( self ):
        if self.file.fileName:
            m = Menu( [
                ( self.file.fileName[ self.file.fileName.rfind( '/' ) + 1 : ], lambda: self.file.save( self.dir ) ),
                ( 'Save as...',                                                lambda: self.saveAs()              )
            ])
            m.display()
        else:
            self.file.save( self.dir )

    def saveAs( self ):
        self.file.fileName = None
        self.file.save( self.dir )

    def hlp( self ):
        d.fill( 0 )
        d.drawText( "Keys:",     18,  0, 1 )
        d.drawText( "U",         12,  8, 1 )
        d.drawText( "L R scroll", 6, 16, 1 )
        d.drawText( "D",         12, 24, 1 )
        d.drawText( "--more--",  12, 32, 1 )
        while not te_btn.actionJustPressed():
            d.update()
        d.fill( 0 )
        d.drawText( "A menu,",      0,  0, 1 )
        d.drawText( "choose",      24,  8, 1 )
        d.drawText( "B edit line,", 0, 16, 1 )
        d.drawText( "close menu",  12, 24, 1 )
        d.drawText( "--key help--", 0, 32, 1 )
        while not te_btn.actionJustPressed():
            d.update()
        def drwSp( sp, x, y ):
            sp.x = x
            sp.y = y
            sp.setFrame( 1 )
            d.drawSprite( sp )
        d.fill( 0 )
        drwSp( self.getSprite( 'leftDelKey'  ),  0, 0 )
        drwSp( self.getSprite( 'rightDelKey' ), 10, 0 )
        d.drawText( "Del", 21, 0, 1 )
        drwSp( self.getSprite( 'leftDelWordKey'  ),  0, 8 )
        drwSp( self.getSprite( 'rightDelWordKey' ), 12, 8 )
        d.drawText( "Del chnk", 25, 8, 1 )
        drwSp( self.getSprite( 'leftDelEndKey'  ),  0, 16 )
        drwSp( self.getSprite( 'rightDelEndKey' ), 14, 16 )
        d.drawText( "Del EOL", 29, 16, 1 )
        drwSp( self.getSprite( 'shiftKey' ), 2, 24 )
        d.drawText( "Shift", 12, 24, 1 )
        sideScroll( 'More help: http://codeberg.org/JBanana/TinyEdit', 0, 33, d.width, 0, {
            'A': lambda: None,
            'B': lambda: None
        } )

    def exit( self ):
        self.file.close()
        return True

    def chooseFile( self, dirPath = None ):
        if not dirPath:
            dirPath = '/'
        while True:
            if not dirPath[ -1 : ] == '/':
                dirPath = dirPath + '/'
            dirEntry = self.chooseDirEntry( dirPath )
            if not dirEntry:
                return None
            newPath = dirEntry[ 0 ]
            entryType = dirEntry[ 1 ]
            if entryType == 0x4000: #dir
                dirPath = newPath
            elif entryType == 0x8000: #file
                return newPath

    def chooseDirEntry( self, dirPath ):
        def makeLambda( dirEntry ):
            return lambda: dirEntry
        dirMenuItems = []
        if dirPath != '/':
            dirAbove = getDirAbove( dirPath )
            if dirAbove == '':
                dirAbove = '/'
            dirMenuItems.append( ( '../', makeLambda( ( dirAbove, 0x4000 ) ) ) )
        for dirEntry in ilistdir( dirPath ):
            entryType = dirEntry[ 1 ]
            if entryType == 0x4000:
                dirMenuItems.append( ( dirEntry[ 0 ] + '/', makeLambda( ( dirPath + dirEntry[ 0 ], 0x4000 ) ) ) )
            elif entryType == 0x8000:
                dirMenuItems.append( ( dirEntry[ 0 ], makeLambda( ( dirPath + dirEntry[ 0 ], 0x8000 ) ) ) )
        return Menu( dirMenuItems ).display()

    def open( self, fileName = None ):
        if fileName:
            if self.file:
                self.file.close()
            self.file = File( fileName, self.getKeyboard, self.getSprite )
            return
        if self.file:
            chosenPath = self.chooseFile( getDirAbove( self.file.fileName ) )
        else:
            chosenPath = self.chooseFile()
        if chosenPath:
            if self.file:
                self.file.close()
            self.file = File( chosenPath, self.getKeyboard, self.getSprite )
            self.dir = getDirAbove( chosenPath )

    def new( self ):
        lastDir = self.dir
        if self.file:
            self.file.close()
        self.file = File( None, self.getKeyboard, self.getSprite )
        self.file.insertLine()
        self.dir = lastDir

    def editLine( self ):
        self.file.replaceLine( self.getKeyboard( self.getSprite, self.file.getFullLine(), self.file.position ).getOutput() )

    def move( self ):
        self.mode = Mode.MOVE

    def find( self ):
        self.findStr = self.getKeyboard( self.getSprite, self.findStr, 0 ).getOutput()
        self.findLine = 0
        self.findNext()

    def goTo( self ):
        try:
            self.file.goTo( int( self.getKeyboard( self.getSprite, str( self.file.getCurrentLineIndex() + 1 ), 0, 2 ).getOutput() ) - 1 )
        except ValueError:
            buzz()

    def split( self ):
        self.file.startSplit()
        self.mode=Mode.SPLIT

    def findNext( self ):
        while True:
            self.file.goTo( self.findLine )
            text = self.file.getFullLine( self.findLine )
            if text == None:
                buzz()
                break
            position = text.find( self.findStr )
            self.findLine += 1
            if position >= 0:
                self.file.setPosition( max( 0, position - 3 ) )
                break

    def pressedU( self ):
        if self.mode == Mode.SPLIT:
            return
        if self.mode == Mode.MOVE:
            self.file.moveUp()
        else:
            self.file.up()

    def pressedD( self ):
        if self.mode == Mode.SPLIT:
            return
        if self.mode == Mode.MOVE:
            self.file.moveDown()
        else:
            self.file.down()

    def pressedL( self ):
        if self.mode == Mode.SPLIT:
            self.file.shiftSplitLeft()
        else:
            self.file.left()

    def pressedR( self ):
        if self.mode == Mode.SPLIT:
            self.file.shiftSplitRight()
        else:
            self.file.right()

    def handleInput( self ):
        b = te_btn.which()
        if not b:
            return
        if b in 'Uu':
            self.pressedU()
        elif b in 'Dd':
            self.pressedD()
        elif b in 'Ll':
            self.pressedL()
        elif b in 'Rr':
            self.pressedR()
        elif b=='B':
            if self.mode == Mode.MOVE or self.mode == Mode.SPLIT:
                self.mode = Mode.SCROLL
            else:
                self.editLine()
        elif b == 'A':
            if self.mode == Mode.MOVE or self.mode == Mode.SPLIT:
                self.mode = Mode.SCROLL
            else:
                self.mode = Mode.MENU

    def display( self ):
        if self.mode == Mode.MENU:
            result = None
            if self.file:
                result = self.withFileMenu.display()
            else:
                result = self.noFileMenu.display()
            if self.file and self.mode == Mode.MENU:
                self.mode = Mode.SCROLL
            return result
        if self.file:
            self.file.display( self.mode )
            return None
        buzz()
        self.mode = Mode.MENU
        return None
