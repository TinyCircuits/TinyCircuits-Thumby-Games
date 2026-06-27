from thumbyGraphics import display as d
from sys import path
if not '/Games/TinySh' in path:
    path.append( '/Games/TinySh' )
from sh_utility import sideScroll

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
            d.drawFilledRectangle( 0, 16, 6, 8, 0 )
            d.drawText( '>', 0, 16, 1 )
        self.action = None
        while True:
            d.fill( 0 )
            itemY = 0
            for item in self.displayItems():
                if item:
                    if itemY == 16:
                        curr = item
                    else:
                        d.drawText( item, 6, itemY, 1 )
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
