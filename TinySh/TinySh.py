from thumbyGraphics import display as d
from thumbySprite import Sprite
from sys import print_exception, implementation, platform, version as p_version
from os import ilistdir, stat, remove, mkdir, rmdir
from random import seed, randrange
from time import ticks_cpu
from collections import OrderedDict
from machine import unique_id
from re import search, sub
import gc

DIR = '/Games/TinySh'
VERSION = '0.1'
isDebug = False

from sys import path
if not DIR in path:
    path.append( DIR )
import sh_btn
from sh_keyboard import Keyboard
from sh_utility import buzz, sideScroll, defaultFont
from sh_menu import Menu

emulated = False
try:
    import emulator
    emulated = True
except ImportError:
    pass

def makeSprites():
    sprites = {
        'shiftKey': Sprite( 7, 8, bytearray([255,251,129,252,129,251,255,0,4,126,3,126,4,0]) ),
        'tabKey':   Sprite( 9, 8, bytearray([247,247,247,128,193,227,247,128,255,8,8,8,127,62,28,8,127,0]) )
    }

    arrowFrameData = bytearray([247,227,193,128,247,247,255,8,28,62,127,8,8,0])
    sprites[ 'leftArrowKey'  ] = Sprite( 7, 8, arrowFrameData )
    sprites[ 'rightArrowKey' ] = Sprite( 7, 8, arrowFrameData, 0, 0, 0, 1 )

    delEndFrameData = bytearray([247,235,213,170,213,170,221,190,170,182,170,190,128,8,20,42,85,42,85,34,65,85,73,85,65,127])
    sprites[ 'leftDelEndKey'  ] = Sprite( 13, 8, delEndFrameData )
    sprites[ 'rightDelEndKey' ] = Sprite( 13, 8, delEndFrameData, 0, 0, 0, 1 )

    delWordFrameData = bytearray([247,235,213,170,221,190,170,182,170,190,128,8,20,42,85,34,65,85,73,85,65,127])
    sprites[ 'leftDelWordKey'  ] = Sprite( 11, 8, delWordFrameData )
    sprites[ 'rightDelWordKey' ] = Sprite( 11, 8, delWordFrameData, 0, 0, 0, 1 )

    delFrameData = bytearray([247,235,221,190,170,182,170,190,128,8,20,34,65,85,73,85,65,127])
    sprites[ 'leftDelKey'  ] = Sprite( 9, 8, delFrameData )
    sprites[ 'rightDelKey' ] = Sprite( 9, 8, delFrameData, 0, 0, 0, 1 )

    return sprites

sprites = makeSprites()

def makeLambda( x ):
    return lambda: x

def errText( x ):
    errInf = errInfo( x.errno )
    return type( x ).__name__ + ': ' + ( '"' + errInf + '"' if errInf else str( x ) )

def logErr( x, fileName ):
    if emulated:
        print_exception( x )
    else:
        with open( DIR + '/' + fileName, 'w', encoding="utf-8" ) as f:
            print_exception( x, f )

def normalise( path ):
    return sub( '/[^/]+/\.\./', '/', path.replace( '//', '/' ) )

def exists( fullpath ):
    try:
        stat( fullpath )
        return True
    except OSError:
        return False

if exists( DIR + '/debug.log' ):
    remove( DIR + '/debug.log' )
def debug( *args ):
    if isDebug:
        if emulated:
            print( *args )
        else:
            with open( DIR + '/debug.log', 'a', encoding="utf-8" ) as f:
                print( *args, file=f )

def getFileName( path ):
    lastSlash = path.rfind ( '/' )
    if lastSlash == -1:
        return path
    return path [ lastSlash + 1 : ]

def glob2re( glob ):
    return '^' + glob.\
        replace( '\\', '\\\\' ).\
        replace( '.',  '\\.'  ).\
        replace( '[',  '\\['  ).\
        replace( ']',  '\\]'  ).\
        replace( '^',  '\\^'  ).\
        replace( '$',  '\\$'  ).\
        replace( '+',  '\\+'  ).\
        replace( '|',  '\\|'  ).\
        replace( '(',  '\\('  ).\
        replace( ')',  '\\)'  ).\
        replace( '*',  '.*'   ).\
        replace( '?',  '.'    ) + '$'

def sizeOf( path ):
    try:
        return stat( path )[ 6 ]
    except OSError:
        return -1

def pump( frm, to, append = False ):
    debug( 'Pumping from', frm)
    debug( '       ...to', to )
    with open( frm, 'rb' ) as inp, open( to, ( 'ab' if append else 'wb' ) ) as outp:
        while True:
            buf = inp.read( 512 )
            if not buf:
                break
            outp.write( buf )

def tokenise( source ):
    class State:
        UNQUOTED = 'UNQUOTED'
        SEPARATOR = 'SEPARATOR'
        SINGLE_QUOTED = 'SINGLE_QUOTED'
        DOUBLE_QUOTED = 'DOUBLE_QUOTED'
        BACKSLASH_QUOTED = 'BACKSLASH_QUOTED'
    def isQuote( char ):
        return char in '"\'\\'
    def isWS( char ):
        return char in ' \t\r\n'
    def matchedQuote( state, char ):
        if state == State.DOUBLE_QUOTED and char == '"':
            return True
        if state == State.SINGLE_QUOTED and char == "'":
            return True
        return False
    def quoteState( char ):
        if char == '"':
            return State.DOUBLE_QUOTED
        if char == "'":
            return State.SINGLE_QUOTED
        if char == '\\':
            return State.BACKSLASH_QUOTED
    state = State.UNQUOTED
    tokens = []
    token = "" if source else None
    for char in source.strip():
        if token == None:
            if isWS( char ):
                pass
            else:
                if isQuote( char ):
                    state = quoteState( char )
                    token = ""
                else:
                    token = char
        else:
            if isWS( char ):
                if state == State.UNQUOTED:
                    tokens.append( token )
                    token = None
                else:
                    token += char
                    if state == State.BACKSLASH_QUOTED:
                        state = State.UNQUOTED
            else:
                if state == State.UNQUOTED:
                    if isQuote( char ):
                        state = quoteState( char )
                    else:
                        token += char
                else:
                    if matchedQuote( state, char ):
                        state = State.UNQUOTED
                    else:
                        token += char
    if token:
        tokens.append( token )
    return tokens

class Line:
    def __init__( self, text ):
        self.text = text
        self.size = len( text )

    def getText( self, position ):
        if position > self.size:
            return '<'
        if position > 0:
            result = '<'
        else:
            result = ' '
        maxRight = position + 10
        result += self.text[ position : min( maxRight, self.size ) ]
        if maxRight < self.size:
            result = result + '>'
        return result

class File:
    def __init__ ( self, fileName ):
        self.fileName = fileName
        self.line = 0
        self.position = 0
        self.cachedLine = -1
        self.lineCache = None

    def getDisplayLines( self, hasTitle ):
        if self.line == self.cachedLine:
            return self.lineCache
        self.lineCache = []
        self.cachedLine = self.line
        start = self.line - ( 1 if hasTitle else 2 )
        end = self.line + 2
        if start < -1:
            self.lineCache.append( None )
        if start < 0:
            self.lineCache.append( None )
        with open( self.fileName, 'r', encoding="utf-8" ) as f:
            for i, line in enumerate( iter( f ) ):
                if i >= start and i <= end:
                    self.lineCache.append( Line( line ) )
                if i > end:
                    break;
        while len( self.lineCache ) < ( 4 if hasTitle else 5 ):
            self.lineCache.append( None )
        return self.lineCache

    def display( self, title = None ):
        while True:
            d.fill( 0 )
            lineY = 0
            if title:
                d.drawText( title, 0, 0, 1 )
                lineY = 8
            for line in self.getDisplayLines( title != None ):
                if line:
                    d.drawText( line.getText( self.position ), 1, lineY, 1 )
                lineY = lineY + 8
            d.update()
            b = sh_btn.which( False )
            if b:
                if b in 'AB':
                    return
                if b in 'Uu':
                    self.up()
                elif b in 'Dd':
                    self.down()
                elif b in 'Ll':
                    self.left()
                elif b in 'Rr':
                    self.right()

    def up( self ):
        if self.line > 0:
            self.line = self.line - 1

    def down( self ):
        if self.lineCache or self.lineCache == '':
            self.line = self.line + 1

    def left( self ):
        if self.position > 0:
            self.position = self.position - 1

    def right( self ):
        self.position = self.position + 1

class BadSyntax( Exception ):
    pass

class BadParams( Exception ):
    pass

class MissingEditor( Exception ):
    pass

class ScriptProblem( Exception ):
    pass

class Command:
    def setShell( self, shell ):
        self.shell = shell

    def setKeyboardGetter( self, keyboardGetter ):
        self.getKeyboard = keyboardGetter

    def readParams( self ):
        pass

    def setParams( self, words ):
        pass

    def __repr__( self ):
        return 'OMGWTF'

    def chooseDir( self, dirPath ):
        return self.choosePath( dirPath, False )

    def choosePath( self, dirPath, incFiles = True ):
        while True:
            if not dirPath[ -1 : ] == '/':
                dirPath = dirPath + '/'
            details = self.chooseDirEntry( dirPath, incFiles )
            if not details:
                return None
            newPath = details[ 0 ]
            isResult = details[ 1 ]
            if isResult:
                return newPath
            dirPath = newPath

    def chooseDirEntry( self, dirPath, incFiles ):
        dirMenuItems = []
        if dirPath != '/':
            dirMenuItems.append( ( '../', makeLambda( ( self.getDirAbove( dirPath ), False ) ) ) )
        for dirEntry in ilistdir( dirPath ):
            entryType = dirEntry[ 1 ]
            if entryType == 0x4000: # dir
                dirMenuItems.append(
                    (
                        dirEntry[ 0 ] + '/',
                        makeLambda( ( dirPath + dirEntry[ 0 ], True ) ),
                        makeLambda( ( dirPath + dirEntry[ 0 ], False ) )
                    )
                )
            elif incFiles and entryType == 0x8000: #file
                dirMenuItems.append( ( dirEntry[ 0 ], makeLambda( ( dirPath + dirEntry[ 0 ], True ) ) ) )
        return Menu( dirMenuItems ).display()

    def absolutePath( self, path ):
        if not path:
            return path
        if path.startswith( '/' ):
            return normalise( path )
        return normalise( self.shell.dirName + '/' + path )

    def exists( self, path ):
        return exists( self.absolutePath ( path ) )

    def isDir( self, path ):
        try:
            return stat( self.absolutePath ( path ) )[ 0 ] == 0x4000 # dir
        except Exception as x:
            raise BadParams( 'Bad path: ' + str( path ) + ' - ' + errText( x ) )

    def getDirAbove ( self, path ):
        if path.endswith( '/' ):
            path = path [ : -1 ]
        if not path.startswith( '/' ):
            path = self.absolutePath( path )
        lastSlash = path.rfind ( '/' )
        return path[ 0 : path.rfind( '/' ) + 1 ]

    def readPipe( self ):
        with open( self.shell.pipePath, 'r' ) as f:
            return f.read()

    def maybeReadPipe( self, param ):
        if param and '|' in param:
            return param.replace( '|', self.readPipe().strip() )
        return param

class List( Command ):
    def __init__( self ):
        super().__init__()
        self.dirName = None
        self.detail = False

    def __repr__( self ):
        result = 'listdir'
        if self.detail:
            result = result + ' --detail'
        if self.dirName:
            result = result + ' ' + self.dirName
        return result

    def readParams( self ):
        self.detail = Menu([
            ( 'no detail',   lambda: False ),
            ( 'with detail', lambda: True  )
        ]).display()
        if Menu([
                ( 'Current dir', lambda: False ),
                ( 'Choose dir',  lambda: True  )
            ]).display():
            dirName = self.choosePath( self.shell.dirName )
            if dirName:
                self.dirName = dirName
        else:
            self.dirName = None

    def setParams( self, words ):
        for word in words:
            if word in [ '--detail', '-detail', '-d', '/detail', '/d' ]:
                self.detail = True
            else:
                self.dirName = word

    def execute( self ):
        if self.dirName:
            self.dirName = self.maybeReadPipe( self.dirName )
        else:
            self.dirName = self.shell.dirName
        self.dirName = self.absolutePath( self.dirName.strip() )
        if self.isDir( self.dirName ):
            dirEntries = list( ilistdir( self.dirName ) )
            maxLen = 0
            maxDigits = 0
            for dirEntry in dirEntries:
                thisLen = len( dirEntry[ 0 ].split( '/' )[ -1 ] )
                if thisLen > maxLen:
                    maxLen = thisLen
                thisLen = len( str( dirEntry[ 3 ] ) )
                if thisLen > maxDigits:
                    maxDigits = thisLen
            for dirEntry in dirEntries:
                self.listFile( dirEntry, maxLen + 1, maxDigits )
        else:
            self.listFile( ( self.dirName, 0x8000, None, stat( self.dirName )[ 6 ] ) )

    def listFile( self, dirEntry, maxLen = -1, maxDigits = -1 ):
        name = dirEntry[ 0 ].split( '/' )[ -1 ]
        self.shell.write( name )
        entryType = dirEntry[ 1 ]
        if entryType == 0x4000: # dir
            self.shell.write( '/' )
        elif entryType == 0x8000: # file
            if self.detail:
                self.shell.write( ( '%-' + str( maxLen - len( name ) ) + 's' ) % ' ' )
                self.shell.write( ( '% ' + str( maxDigits            ) + 's' ) % str( dirEntry[ 3 ] ) )
        else:
            self.shell.write( '?!' )
        self.shell.write( '\n' )

class Pwd( Command ):
    def __repr__( self ):
        return 'pwd'

    def execute( self ):
        result = self.shell.dirName
        if result and not result[ -1 ] == '/':
            result = result + '/'
        self.shell.write( result )

class ChDir( Command ):
    def __init__( self ):
        super().__init__()
        self.dirName = None

    def __repr__( self ):
        result = 'changedir'
        if self.dirName:
            result = result + ' ' + self.dirName
        return result

    def readParams( self ):
        if Menu([
                ( 'Choose dir', lambda: True  ),
                ( 'Root dir',   lambda: False )
            ]).display():
            dirName = self.chooseDir( self.shell.dirName )
            if dirName:
                self.dirName = dirName

    def setParams( self, words ):
        for word in words:
            if not self.dirName:
                self.dirName = word

    def execute( self ):
        debug( 'Changing dir to', self.dirName )
        if self.dirName:
            self.dirName = self.maybeReadPipe( self.dirName )
        else:
            self.dirName = '/'
        self.dirName = self.absolutePath( self.dirName.strip() )
        if self.isDir( self.dirName ):
            self.shell.setDir( self.dirName )
            self.shell.write( self.dirName )
            debug( 'Changed dir to', self.shell.dirName )
        else:
            raise BadParams( 'Not a directory: ' + self.dirName )

class MkDir( Command ):
    def __init__( self ):
        super().__init__()
        self.dirName = None

    def __repr__( self ):
        result = 'makedir'
        if self.dirName:
            result = result + ' ' + self.dirName
        return result

    def readParams( self ):
        dirName = self.getKeyboard().getOutput()
        if dirName:
            self.dirName = dirName

    def setParams( self, words ):
        for word in words:
            self.dirName = word

    def execute( self ):
        self.dirName = self.absolutePath( self.maybeReadPipe( self.dirName ) )
        if self.dirName.endswith( '/' ):
            self.dirName = self.dirName[ : -1 ]
        mkdir( self.dirName )
        self.shell.write( self.dirName + '/' )

class RmDir( Command ):
    def __init__( self ):
        super().__init__()
        self.dirName = None

    def __repr__( self ):
        result = 'deletedir'
        if self.dirName:
            result = result + ' ' + self.dirName
        return result

    def readParams( self ):
        dirName = self.chooseDir( self.shell.dirName )
        if dirName:
            self.dirName = dirName

    def setParams( self, words ):
        for word in words:
            self.dirName = word

    def execute( self ):
        self.dirName = self.maybeReadPipe( self.dirName )
        self.dirName = self.absolutePath( self.dirName )
        rmdir( self.dirName )
        self.shell.write( self.dirName )

class Show( Command ):
    def __init__( self ):
        super().__init__()
        self.fileName = None

    def __repr__( self ):
        result = 'show'
        if self.fileName:
            result = result + ' ' + self.fileName
        return result

    def readParams( self ):
        fileName = self.choosePath( self.shell.dirName )
        if fileName:
            self.fileName = fileName

    def setParams( self, words ):
        for word in words:
            self.fileName = word

    def execute( self ):
        if not self.fileName:
            return
        self.fileName = self.maybeReadPipe( self.fileName )
        self.fileName = self.absolutePath( self.fileName )
        with open( self.fileName, 'r' ) as f:
            while True:
                buf = f.read( 512 )
                if not buf:
                    break
                self.shell.write( buf )

class Edit( Command ):
    def __init__( self ):
        super().__init__()
        self.fileName = None

    def __repr__( self ):
        result = 'edit'
        if self.fileName:
            result = result + ' ' + self.fileName
        return result

    def readParams( self ):
        fileName = self.choosePath( self.shell.dirName )
        if fileName:
            self.fileName = fileName

    def setParams( self, words ):
        for word in words:
            self.fileName = word

    def execute( self ):
        if not self.fileName:
            return
        if not exists( '/Games/TinyEdit/editor.py' ):
            raise MissingEditor( 'Could not find TinyEdit v2 to use as editor' )
        if not '/Games/TinyEdit' in path:
            path.append( '/Games/TinyEdit' )
        self.fileName = self.maybeReadPipe( self.fileName )
        self.fileName = self.absolutePath( self.fileName )
        gc.collect()
        from editor import Editor
        editor = Editor(
            lambda s, t = 0, p = 0, l = 0: Keyboard( s, t, p, l ),
            lambda n: sprites[ n ],
            self.fileName
        )
        while True:
            editor.handleInput()
            if editor.display():
                break
        self.shell.write( self.fileName )

class Copy( Command ):
    def __init__( self ):
        super().__init__()
        self.frm = None
        self.to = None
        self.commandName = 'copy'

    def __repr__( self ):
        result = self.commandName
        if self.frm:
            result = result + ' ' + self.frm
            if self.to:
                result = result + ' ' + self.to
        return result

    def readParams( self ):
        frm = self.choosePath( self.shell.dirName )
        if frm:
            self.frm = frm
            if Menu([
                    ( 'To current dir',    lambda: False ),
                    ( 'Choose target dir', lambda: True  )
                ]).display():
                to = self.chooseDir( self.shell.dirName )
                if to:
                    self.to = to
                    newName = getFileName( frm )
                    if Menu([
                            ( 'Same name - ' + newName, lambda: False ),
                            ( 'New name',               lambda: True  )
                        ]).display():
                        self.to = self.to + '/' + self.getKeyboard( newName ).getOutput()

    def setParams( self, words ):
        for word in words:
            if not self.frm:
                self.frm = word
            elif not self.to:
                self.to = word
            else:
                raise BadSyntax( 'To many parameters. Command was: ' + ' '.join( words ) )
        debug( 'frm:', self.frm )
        debug( ' to:', self.to  )

    def execute( self ):
        if not self.frm:
            debug( 'No frm - doing nothing' )
            return

        self.frm = self.absolutePath( self.maybeReadPipe( self.frm ) )
        if not self.to:
            # command: copy frm
            debug( 'target is current dir, same file name' )
            self.to = self.shell.dirName + '/' + getFileName( self.frm )
        else:
            # command: copy from to
            if self.exists( self.to ):
                if self.isDir( self.to ):
                    debug( 'target is to dir, same file name' )
                    self.to = self.to + '/' + getFileName( self.frm )
                else:
                    debug( 'target is to file' )
                    pass
            else:
                parent = self.getDirAbove( self.to )
                debug( 'parent is', parent )
                if self.exists( parent ):
                    if self.isDir( parent ):
                        debug( "to doesn't exist but parent does and is a dir..." )
                        debug( "...target is parent, name is rest" )
                        pass
                    else:
                        debug( "to doesn't exist but parent does and is a file, error" )
                        raise BadParams( 'Cannot copy to ' + self.to + ' because ' + parent + ' is a file' )
                else:
                    debug( 'neither to nor parent exist - error' )
                    raise BadParams( 'Cannot copy to ' + self.to + ' because ' + parent + ' does not exist' )
            debug( 'to:', self.to )
        self.to = self.absolutePath( self.to )

        pump( self.frm, self.to )
        self.afterPump()
        self.shell.write( self.to )

    def afterPump( self ):
        pass

class Move( Copy ):
    def __init__( self ):
        super().__init__()
        self.commandName = 'move'

    def afterPump( self ):
        remove( self.frm )

class Delete( Command ):
    def __init__( self ):
        super().__init__()
        self.fileName = None

    def __repr__( self ):
        result = 'delete'
        if self.fileName:
            result = result + ' ' + self.fileName
        return result

    def readParams( self ):
        fileName = self.choosePath( self.shell.dirName )
        if fileName:
            self.fileName = fileName

    def setParams( self, words ):
        for word in words:
            self.fileName = word

    def execute( self ):
        self.fileName = self.absolutePath( self.maybeReadPipe( self.fileName ) )
        remove( self.fileName )
        self.shell.write( self.fileName )

class Run( Command ):
    def __init__( self ):
        super().__init__()
        self.scriptName = None
        self.index = 0
        self.lines = []
        self.paramCache = []

    def __repr__( self ):
        result = 'run'
        if self.scriptName:
            result = result + ' ' + self.scriptName
        return result

    def readParams( self ):
        scriptName = self.choosePath( self.shell.dirName )
        if scriptName:
            self.scriptName = scriptName

    def setParams( self, words ):
        for word in words:
            dePiped = self.maybeReadPipe( word )
            if not self.scriptName:
                self.scriptName = self.absolutePath( dePiped )
            self.paramCache.append( dePiped )

    def execute( self ):
        if not self.scriptName:
            return
        d.fill( 0 )
        d.drawSprite( Sprite( 9, 11, bytearray([0,2,142,90,178,90,142,2,0,0,2,3,3,3,3,3,2,0]), 63, 0, 0 ) )
        d.update()
        for i, param in enumerate( self.paramCache ):
            self.shell.environment[ str( i ) ] = param
        def isJump( line ):
            match = search( '^jump\s+:', line )
            if match:
                return line[ match.end() - 1 : ]
            return None
        def isIf( line ):
            if search( "^if[ \t]+", line ):
                class IfResult:
                    pass
                result = IfResult()
                ifTokens = tokenise( line )
                ifTokenCount = len( ifTokens )
                if ifTokenCount < 2:
                    raise ScriptProblem( 'Not enough tokens for "if"' )
                index = 1
                if ifTokens[ index ] == 'not':
                    if ifTokenCount < 3:
                        raise ScriptProblem( 'Not enough tokens for "if not"' )
                    result.nott = True
                    index += 1
                else:
                    result.nott = False
                if ifTokens[ index ] == 'empty':
                    result.type = 'empty'
                    if ifTokenCount < index + 1:
                        if result.nott:
                            raise ScriptProblem( 'Too many tokens for "if not empty"' )
                        else:
                            raise ScriptProblem( 'Too many tokens for "if empty"' )
                elif ifTokens[ index ] in [ 'exists', 'exist' ]:
                    result.type = 'exists'
                    index += 1
                    result.filename = self.shell.substitute( self.maybeReadPipe( ifTokens[ index ] ) )
                    if ifTokenCount < index + 1:
                        if result.nott:
                            raise ScriptProblem( 'Too many tokens for "if not exists"' )
                        else:
                            raise ScriptProblem( 'Too many tokens for "if exists"' )
                elif ifTokens[ index + 1 ] in [ '=', '==' ]:
                    result.type = 'equals'
                    result.lhs = self.shell.substitute( self.maybeReadPipe( ifTokens[ index     ] ) )
                    result.rhs = self.shell.substitute( self.maybeReadPipe( ifTokens[ index + 2 ] ) )
                    if ifTokenCount < index + 3:
                        if result.nott:
                            raise ScriptProblem( 'Too many tokens for "if not equal"' )
                        else:
                            raise ScriptProblem( 'Too many tokens for "if equal"' )
                return result
            return None
        self.scriptName = self.absolutePath( self.maybeReadPipe( self.scriptName ) )
        with open( self.scriptName, 'r' ) as f:
            for line in f:
                self.lines.append( line.strip() )
        self.index = 0
        while self.index < len( self.lines ):
            line = self.lines[ self.index ]
            try:
                debug( '\nLine', self.index + 1, ':', line )
                label = isJump ( line )
                if label:
                    missingLabel = True
                    for i, possLine in enumerate( self.lines ):
                        if possLine == label:
                            missingLabel = False
                            self.index = i + 1
                            break
                    if missingLabel:
                        raise BadSyntax( 'Missing label: ' + label )
                else:
                    ifDetail = isIf( line )
                    if ifDetail:
                        ifResult = False
                        debug( 'ifType:', ifDetail.type )
                        if ifDetail.type == 'exists':
                            ifResult = self.exists( ifDetail.filename )
                            debug( 'exists', ifDetail.filename, ': ', ifResult )
                        elif ifDetail.type == 'empty':
                            debug( 'pipe size:', sizeOf( self.shell.pipePath ) )
                            ifResult = sizeOf( self.shell.pipePath ) <= 0
                        elif ifDetail.type == 'equals':
                            debug( 'lhs: [' + ifDetail.lhs + '] rhs: [' + ifDetail.rhs + ']' )
                            ifResult = ifDetail.lhs == ifDetail.rhs
                        if ifDetail.nott:
                            ifResult = not ifResult
                        debug( 'ifResult:', ifResult )
                        self.index = self.index + ( 1 if ifResult else 2 )
                    else:
                        if line == 'each':
                            with open( self.shell.pipePath, 'r' ) as f:
                                items = f.read().splitlines()
                            self.index += 1
                            action = self.lines[ self.index ]
                            for item in items:
                                debug( '\nLine', self.index + 1, ':', action )
                                shell.commandLine = action.replace( '|', item )
                                debug( 'Executing', shell.commandLine )
                                shell.execute()
                            self.index += 1
                        elif line == 'choose':
                            with open( self.shell.pipePath, 'r' ) as f:
                                items = f.read().splitlines()
                            choice = Menu( [
                                ( item, makeLambda( item ) ) for item in items
                            ] ).display()
                            with open( self.shell.pipePath, 'w' ) as f:
                                f.write( choice if choice else "" )
                            self.index += 1
                        else:
                            line = self.lines[ self.index ]
                            if line:
                                line = line.strip()
                            if line and not line.startswith( '#' ):
                                shell.commandLine = line
                                shell.execute()
                                shell.displayDebugOutput()
                            self.index += 1
            except Exception as x:
                logErr( x, 'scriptdump.log' )
                raise ScriptProblem( 'at ' + self.paramCache[ 0 ] + ' line ' + str( self.index + 1 ) + ': ' + errText( x ) )

class Env( Command ):
    def __init__( self ):
        super().__init__()
        self.name = None
        self.value = None

    def __repr__( self ):
        result = 'set'
        if self.name:
            result = result + ' ' + self.name
            if self.value:
                result = result + ' ' + self.value
        return result

    def readParams( self ):
        choice = Menu([
                ( 'define var', lambda: 'define' ),
                ( 'delete var', lambda: 'delete' ),
                ( 'show all',   lambda: 'show'   )
            ]).display()
        if choice == 'define':
            self.name = self.getKeyboard().getOutput()
            if self.name:
                self.value = self.getKeyboard().getOutput()
        elif choice == 'delete':
            self.name = Menu(
                [ ( key, makeLambda( key ) ) for key in self.shell.environment ]
            ).display()

    def setParams( self, words ):
        for word in words:
            if not self.name:
                self.name = word
            else:
                self.value = word

    def execute( self ):
        if self.name:
            self.name = self.maybeReadPipe( self.name )
            if self.value:
                self.value = self.maybeReadPipe( self.value )
                self.shell.environment[ self.name ] = self.value
                self.shell.write( self.name + '=' + self.value )
            else:
                self.shell.write( self.name )
                del( self.shell.environment[ self.name ] )
        else:
            for key in self.shell.environment:
                self.shell.write( key + '=' + self.shell.environment[ key ] + '\n' )

class Echo( Command ):
    def __init__( self ):
        super().__init__()
        self.payload = None

    def __repr__( self ):
        result = 'echo'
        if self.payload:
            result = result + ' ' + self.payload
        return result

    def readParams( self ):
        self.payload = self.getKeyboard().getOutput()

    def setParams( self, words ):
        for word in words:
            if not self.payload:
                self.payload = word
            else:
                self.payload = self.payload + ' ' + word

    def execute( self ):
        output = self.maybeReadPipe( self.payload )
        self.shell.write( output )
        if not output.endswith( '\n' ):
            self.shell.write( '\n' )

class Grep( Command ):
    def __init__( self ):
        super().__init__()
        self.regex = None
        self.fixed = False
        self.invert = False

    def __repr__( self ):
        result = 'grep'
        if self.fixed:
            result += ' --fixed'
        if self.invert:
            result += ' --invert'
        if self.regex:
            result = result + ' ' + self.regex
        return result

    def readParams( self ):
        self.fixed = Menu([
            ( 'regex', lambda: False ),
            ( 'fixed', lambda: True  )
        ]).display()
        self.invert = Menu([
            ( 'normal',   lambda: False ),
            ( 'inverted', lambda: True  )
        ]).display()
        self.regex = self.getKeyboard().getOutput()

    def setParams( self, words ):
        for word in words:
            if word in [ '--fixed', '-fixed', '-F', '/fixed', '/F' ]:
                self.fixed = True
            elif word in [ '--invert', '-invert', '-v', '/invert', '/v' ]:
                self.invert = True
            elif not self.regex:
                self.regex = word

    def execute( self ):
        with open( self.shell.pipePath, 'r' ) as f:
            for line in f:
                if line.endswith( '\n' ):
                    line = line[ 0 : -1 ]
                hit = False
                if self.fixed:
                    if self.invert:
                        if not self.regex in line:
                            hit = True
                    else:
                        if self.regex in line:
                            hit = True
                else:
                    if self.invert:
                        if not search( self.regex, line ):
                            hit = True
                    else:
                        if search( self.regex, line ):
                            hit = True
                if hit:
                    self.shell.write( line )
                    self.shell.write( '\n' )

class Find( Command ):
    def __init__( self ):
        super().__init__()
        self.namePattern = None
        self.nameRegex = None
        self.type = None
        self.invert = None

    def __repr__( self ):
        result = 'find'
        if self.type:
            result = result + ' --type ' + self.type
        if self.invert:
            result += ' --not'
        if self.namePattern:
            result = result + ' ' + self.namePattern
        return result

    def readParams( self ):
        self.type = Menu([
            ( 'files',       lambda: 'f'  ),
            ( 'directories', lambda: 'd'  ),
            ( 'either',      lambda: None )
        ]).display()
        self.invert = Menu([
            ( 'matching',     lambda: False ),
            ( 'not matching', lambda: True  ),
            ( 'all',          lambda: None  )
        ]).display()
        if self.invert:
            self.namePattern = self.getKeyboard().getOutput()

    def setParams( self, words ):
        suckType = False
        for word in words:
            if suckType:
                self.type = word
                suckType = False
            elif word in [ '--type', '-t', '/type', '/t' ]:
                suckType = True
            elif word in [ '--fixed', '-fixed', '-F', '/fixed', '/F' ]:
                self.fixed = True
            elif word in [ '--not', '-not', '-v', '/not', '/v' ]:
                self.invert = True
            elif not self.namePattern:
                self.namePattern = word

    def execute( self ):
        if self.namePattern:
            self.nameRegex = glob2re( self.namePattern )
        self.find( '/' )

    def find( self, dirName ):
        dirEntries = list( ilistdir( dirName ) )
        for dirEntry in dirEntries:
            name = dirEntry[ 0 ]
            path = ( '/' if dirName == '/' else dirName + '/' ) + name
            entryType = dirEntry[ 1 ]
            if entryType == 0x4000: # dir
                if self.type != 'f' and self.wildMatch( name ):
                    self.shell.write( path + '/\n' )
                self.find( path )
            elif entryType == 0x8000: # file
                if self.type != 'd' and self.wildMatch( name ):
                    self.shell.write( path + '\n' )
            else:
                debug( 'Unknown dir entry type:', entryType )

    def wildMatch( self, name ):
        if self.nameRegex:
            result = search( self.nameRegex, name )
        else:
            result = True
        if self.invert:
            return (not result)
        return result

class Redir( Copy ):
    def __init__( self ):
        super().__init__()

    def __repr__( self ):
        result = '>'
        if self.to:
            result = result + ' ' + self.to
        return result

    def readParams( self ):
        self.to = self.chooseDir( self.shell.dirName ) + '/' + self.getKeyboard().getOutput()

    def setParams( self, words ):
        for word in words:
            if not self.to:
                self.to = word

    def execute( self ):
        self.frm = self.shell.pipePath
        super().execute()

class Append( Command ):
    def __init__( self ):
        super().__init__()
        self.to = None

    def __repr__( self ):
        result = '>>'
        if self.to:
            result = result + ' ' + self.to
        return result

    def readParams( self ):
        self.to = self.choosePath( self.shell.dirName )

    def setParams( self, words ):
        for word in words:
            if not self.to:
                self.to = word

    def execute( self ):
        if self.to:
            pump( self.shell.pipePath, self.to, True )
            self.shell.write( self.to + '\n' )

class Ver( Command ):
    def __repr__( self ):
        return 'version'

    def execute( self ):
        self.shell.write( VERSION )

class Debug( Command ):
    def __init__( self ):
        super().__init__()
        self.on = None

    def __repr__( self ):
        if self.on == None:
            return 'debug'
        return 'debug --' + ( 'on' if self.on else 'off' )

    def readParams( self ):
        self.on = Menu([
            ( 'on',   lambda: True  ),
            ( 'off',  lambda: False ),
            ( 'show', lambda: None  )
        ]).display()

    def setParams( self, words ):
        for word in words:
            if word in [ '--on', '-on', '--true', '-true', '-t', '/on', '/true', '/t' ]:
                self.on = True
            elif word in [ '--off', '-off', '--false', '-false', '-f', '/off', '/false', '/f' ]:
                self.on = False

    def execute( self ):
        global isDebug
        if self.on != None:
            isDebug = self.on
        self.shell.write( 'Debug ' + ( 'on' if isDebug else 'off' ) )

class Exit( Command ):
    def __repr__( self ):
        return 'exit'

    def execute( self ):
        return True

class Help( Command ):
    def __repr__( self ):
        return 'help'

    def execute( self ):
        self.shell.write( 'A: menu, choose\n' )
        self.shell.write( 'B: abort\n'        )
        self.shell.write( 'R: open dir\n'     )
        self.shell.write( '\n'                )
        self.shell.write( 'More help: http://codeberg.org/JBanana/TinySh' )

class Shell:
    pipePath = DIR + '/pipe.dat'
    scriptDepth = 0
    seed( ticks_cpu() ),
    environment = {
        'UNIQUE_ID':  str( unique_id() ),
        'MP_VERSION': '.'.join( str( n ) for n in implementation[ 1 ] ),
        'P_VERSION':  p_version,
        'MACHINE':    implementation[ 2 ],
        'PLATFORM':   platform,
        'RANDOM':     '',
        'CD':         '/',
        'PWD':        '/',
        'OPENCURLY':  '{',
        'CLOSECURLY': '}'
    }
    logFile = DIR + '/log'

    def alias( self, frm, to ):
        self.commands[ frm ] = self.commands[ to ]

    def __init__( self, spriteGetter ):
        self.getSprite = spriteGetter
        self.dirName = '/'
        self.commands = OrderedDict([
            ( 'help',       lambda: Help()   ),
            ( 'run',        lambda: Run()    ),
            ( 'changedir',  lambda: ChDir()  ),
            ( 'pwd',        lambda: Pwd()    ),
            ( 'listdir',    lambda: List()   ),
            ( 'show',       lambda: Show()   ),
            ( 'edit',       lambda: Edit()   ),
            ( 'copy',       lambda: Copy()   ),
            ( 'move',       lambda: Move()   ),
            ( 'delete',     lambda: Delete() ),
            ( 'makedir',    lambda: MkDir()  ),
            ( 'deletedir',  lambda: RmDir()  ),
            ( 'env',        lambda: Env()    ),
            ( 'echo',       lambda: Echo()   ),
            ( 'grep',       lambda: Grep()   ),
            ( 'find',       lambda: Find()   ),
            ( '>',          lambda: Redir()  ),
            ( '>>',         lambda: Append() ),
            ( 'version',    lambda: Ver()    ),
            ( 'debug',      lambda: Debug()  ),
            ( 'exit',       lambda: Exit()   )
        ])

        menuItems = []
        for menuItem in self.commands.items():
            menuItems.append( menuItem )
        self.commandMenu = Menu( menuItems )
        self.alias( 'ls',     'listdir'   )
        self.alias( 'dir',    'listdir'   )
        self.alias( 'list',   'listdir'   )
        self.alias( 'cd',     'changedir' )
        self.alias( 'chdir',  'changedir' )
        self.alias( 'cat',    'show'      )
        self.alias( 'type',   'show'      )
        self.alias( 'cp',     'copy'      )
        self.alias( 'mv',     'move'      )
        self.alias( 'rm',     'delete'    )
        self.alias( 'del',    'delete'    )
        self.alias( 'mkdir',  'makedir'   )
        self.alias( 'md',     'makedir'   )
        self.alias( 'rmdir',  'deletedir' )
        self.alias( 'rd',     'deletedir' )
        self.alias( 'set',    'env'       )
        self.alias( 'export', 'env'       )
        self.alias( 'ver',    'version'   )
        try:
            remove( self.logFile )
        except:
            pass # Never mind

    def setDir( self, dirName ):
        self.dirName = dirName
        self.environment[ 'CD' ] = dirName
        self.environment[ 'PWD' ] = dirName

    def splash( self ):
        d.fill( 0 )
        d.drawSprite( Sprite( 15, 12, bytearray([224,184,12,70,162,19,161,33,195,130,134,76,88,240,192,0,3,6,4,12,9,12,6,3,0,0,0,0,0,0]), 2, 0, 0 ) )
        d.setFont( "/lib/font8x8.bin", 8, 8, 0 )
        d.drawText( "T", 17, 3, 1 )
        d.drawText( "i", 22, 3, 1 )
        d.drawText( "nySh", 28, 3, 1 )
        d.setFont( "/lib/font3x5.bin", 3, 5, 0 )
        d.drawText( VERSION, 63, 5, 1 )
        defaultFont()
        d.drawText( 'File mgmt in', 0, 14, 1 )
        d.drawText( 'a tiny shell', 0, 22, 1 )
        d.drawText( 'A/B: Start', 6, 33, 1 )
        while not sh_btn.actionJustPressed():
            d.update()
        sh_btn.clear()

    def readExecute( self ):
        command = self.commandMenu.display()
        if not command:
            return
        command.setShell( self )
        command.setKeyboardGetter( lambda t = "", p = 0, l = 0: Keyboard( self.getSprite, t, p, l ) )
        command.readParams()
        self.commandLine = str( command )
        debug( "Command:", self.commandLine )
        self.log( self.commandLine )
        return self.execute()

    def log( self, commandLine ):
        with open( self.logFile, 'a', encoding='utf-8' ) as f:
            f.write ( commandLine );
            f.write ( '\n' );

    def stripCommand( self ):
        strippedCommand = self.commandLine.strip()
        if strippedCommand and strippedCommand[ 0 ] in '#:':
            # Ignore comments and labels
            self.commandLine = ""
        else:
            self.commandLine = strippedCommand

    def buildCommand( self ):
        words = tokenise( self.commandLine )
        if not words:
            # Shouldn't be possible to get no tokens
            # but if that happens, ignore line
            return None
        commandName = words[ 0 ]
        if not commandName in self.commands:
            raise Exception( 'Unknown command: ' + commandName )
        # Get a command object
        result = self.commands[ commandName ]()
        result.setShell( self )
        if len( words ) > 1:
            result.setParams( words[ 1 : ] )
        return result

    def execute( self ):
        result = None
        self.stripCommand()
        if not self.commandLine:
            return
        self.commandLine = self.substitute( self.commandLine )
        debug( 'Command:', self.commandLine )
        command = self.buildCommand()
        if not command:
            return
        if isinstance( command, Run ):
            with open( self.pipePath, 'w' ) as f:
                f.write( "" )
            oldScriptDepth = self.scriptDepth
            oldEnvironment = self.environment
            try:
                self.environment = self.environment.copy()
                self.scriptDepth += 1
                result = command.execute()
            finally:
                self.scriptDepth = oldScriptDepth
                self.environment = oldEnvironment
        else:
            with open( self.pipePath, 'w', encoding = "utf-8" ) as f:
                self.pipe = f
                result = command.execute()
        if self.scriptDepth == 0 and not result:
            self.displayOutput()
        return result

    def substitute( self, input ):
        debug( 'Subst in', input )
        if not input:
            return ""
        self.environment[ 'RANDOM' ] = str( randrange( 671781 ) )
        # 50% of numbers from 0 to 671781 contain the digit 2 - same for 3, 4 & 5
        output = input
        if '{' in input:
            presentKeys = []
            for key in self.environment:
                if '{' + key + '}' in input:
                    presentKeys.append( key )
            for key in presentKeys:
                output = output.replace( '{' + key + '}', self.environment[ key ] )
        debug( 'Subst out', output )
        return output

    def displayDebugOutput( self ):
        debug( "Output:" )
        with open( self.pipePath, 'r', encoding="utf-8" ) as f:
            for line in f:
                debug( line.rstrip() )

    def displayOutput( self ):
        self.displayDebugOutput()
        File( self.pipePath ).display( 'Output:' )

    def write( self, text ):
        self.pipe.write( text )

def errInfo( code ):
    return {
        # Would be nicer to use constants from errno, but they aren't all defined.

        # These ones were defined in errno
        1:   'Operation not permitted',              # EPERM
        2:   'No such file or directory',            # ENOENT
        5:   'Input/output error',                   # EIO
        9:   'Bad file descriptor',                  # EBADF
        11:  'Resource temporarily unavailable',     # EAGAIN
        12:  'Cannot allocate memory',               # ENOMEM
        13:  'Permission denied',                    # EACCES
        17:  'File exists',                          # EEXIST
        19:  'No such device',                       # ENODEV
        21:  'Is a directory',                       # EISDIR
        22:  'Invalid argument',                     # EINVAL
        95:  'Operation not supported',              # EOPNOTSUPP
        98:  'Address already in use',               # EADDRINUSE
        103: 'Software caused connection abort',     # ECONNABORTED
        104: 'Connection reset by peer',             # ECONNRESET
        105: 'No buffer space available',            # ENOBUFS
        107: 'Transport endpoint is not connected',  # ENOTCONN
        110: 'Connection timed out',                 # ETIMEDOUT
        111: 'Connection refused',                   # ECONNREFUSED
        113: 'No route to host',                     # EHOSTUNREACH
        114: 'Operation already in progress',        # EALREADY
        115: 'Operation now in progress',            # EINPROGRESS

        # These ones weren't
        28:  'No space left on device',              # ENOSPC
        36:  'File name too long',                   # ENAMETOOLONG
        39:  'Directory not empty',                  # ENOTEMPTY
    }.get( code )

shell = None
try:
    shell = Shell( lambda n: sprites[ n ] )
except Exception as x:
    buzz()
    logErr( x, 'initcrash.log' )
    d.fill( 0 )
    d.drawText( "Init error", 3, 8, 1 )
    d.drawText( "Problem was:", 0, 22, 1 )
    errMsg = errText( x )
    while True:
        if sideScroll(
            errMsg,
            0,
            30,
            d.width,
            -1,
            {
                'A': lambda: True,
                'B': lambda: True
            } ):
            break
if shell:
    shell.splash()
    while True:
        try:
            if shell.readExecute():
                break
        except Exception as x:
            buzz()
            logErr( x, 'crashdump.log' )
            d.fill( 0 )
            d.drawText( "Shell error", 3, 8, 1 )
            d.drawText( "Problem was:", 0, 22, 1 )
            errMsg = errText( x )
            while True:
                if sideScroll(
                    errMsg,
                    0,
                    30,
                    d.width,
                    -1,
                    {
                        'A': lambda: True,
                        'B': lambda: True
                    } ):
                    break
