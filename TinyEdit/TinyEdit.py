from thumbyGraphics import display as d
from thumbySprite import Sprite
from sys import print_exception
from sys import path
if not '/Games/TinyEdit' in path:
    path.append( '/Games/TinyEdit' )
import te_btn
from te_utility import buzz, sideScroll, defaultFont
from te_keyboard import Keyboard
from editor import Editor

inEmulator = None
try:
    import emulator
    inEmulator = True
except ImportError:
    inEmulator = False

def splash():
    d.fill(0)
    d.drawSprite(Sprite(37,20,
        bytearray([128,192,224,112,48,48,112,224,128,0,0,0,0,0,0,0,192,160,80,168,212,234,245,250,253,254,127,191,95,175,87,43,21,10,5,2,1,159,255,240,224,240,56,28,15,3,0,0,0,0,128,252,245,234,213,171,215,47,95,55,43,21,10,5,2,1,0,0,0,0,0,0,0,0,3,1,0,1,3,3,6,6,6,6,6,3,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
        0,0,0))
    d.setFont("/lib/font8x8.bin",8,8,1)
    d.drawText("Tiny",38,0,1)
    d.drawText("Edit",30,10,1)
    d.setFont("/lib/font3x5.bin",3,5,1)
    d.drawText('2',69,12,1)
    defaultFont()
    d.drawText("Text editor",3,22,1)
    d.drawText('A/B: Start',6,33,1)
    while not te_btn.actionJustPressed():
        d.update()
    te_btn.clear()

def makeSprites():
    sprites = {
        'shiftKey': Sprite( 7, 8, bytearray([255,251,129,252,129,251,255,0,4,126,3,126,4,0]) ),
        'tabKey':   Sprite( 9, 8, bytearray([247,247,247,128,193,227,247,128,255,8,8,8,127,62,28,8,127,0]) ),
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

try:
    splash()
    editor = Editor(
        lambda s, t, p, l = 0: Keyboard( s, t, p, l ),
        lambda n: sprites[ n ]
    )
    while True:
        editor.handleInput()
        if editor.display():
            break
except Exception as x:
    buzz()
    if inEmulator:
        print_exception( x )
    else:
        with open( '/Games/TinyEdit/crashdump.log', 'w', encoding = "utf-8" ) as f:
            print_exception( x, f )
    d.fill( 0 )
    d.drawText( "Editor died",  3,  8, 1 )
    d.drawText( "Problem was:", 0, 22, 1 )
    sideScroll( str( x ), 0, 30, d.width, -1, {
        'A': lambda: True,
        'B': lambda: True
    } )
