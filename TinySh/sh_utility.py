from thumbyAudio import audio
from random import randint
from thumbyGraphics import display as d
import sh_btn

def noise( length ):
    for _ in range( length ):
        audio.playBlocking( randint( 400, 500 ), 10 )

def buzz():
    d.display.invert( 1 )
    d.update()
    noise( 5 )
    d.display.invert( 0 )
    d.update()
    noise( 10 )

baseFPS = 6
sideScrollFPS = 45
def setFPS( fps ):
    d.setFPS( fps )
setFPS( baseFPS )

def defaultFont():
    d.setFont( "/lib/font5x7.bin", 5, 7, 1 )

def sideScroll( displayString, x, y, w, b, lambdas ):
    if ( 1 + len( displayString ) ) * 6 > w:
        setFPS( sideScrollFPS )
        displayLen = len( displayString ) * 6 + w
        o = b if b > 0 else 0
        pauseStart = 10 if o > 0 else 0
        while True:
            d.drawFilledRectangle( x, y, w, 8, 0 )
            d.drawText( displayString, x + w - o, y, 1 )
            if 'lFill' in lambdas:
                lambdas[ 'lFill' ]()
            d.update()
            b = sh_btn.which( False )
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
    d.drawText( displayString, x, y, 1 )
    d.update()
    b = sh_btn.which( False )
    if b and b in lambdas:
        return lambdas[ b ]()
