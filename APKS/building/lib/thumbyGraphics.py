import asyncio
import pygame
from os import stat
from time import ticks_ms, ticks_diff, sleep_ms
from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR



def open(path, mode):
    # If absolute path, append CPython wasm path to building root (mimic Thumby FS)
    if path[0] == '/':
        path = '/data/data/building/assets' + path

    import builtins
    from pathlib import Path
    
    filename = Path(path)
    filename.parent.mkdir(parents=True, exist_ok=True)

    return builtins.open(path, mode)



class GraphicsClass:
    def __init__(self, width, height):
        self.surface = pygame.display.set_mode((72, 40), pygame.SCALED | pygame.RESIZABLE)
        self.width = width
        self.height = height
        self.max_x = width-1
        self.max_y = height-1
        self.frameRate = 60 # Unlike the official Thumby library, cap this at 60 by default since it can go very fast
        self.lastUpdateEnd = 0
        self.setFont('lib/font5x7.bin', 5, 7, 1)

        self.clock = pygame.time.Clock()

    def setFont(self, fontFile, width, height, space):
        self.textBitmapSource = fontFile
        self.textBitmapFile = open(self.textBitmapSource, 'rb')
        self.textWidth = width
        self.textHeight = height
        self.textSpaceWidth = space
        self.textBitmap = bytearray(self.textWidth)
        self.textCharCount = stat(self.textBitmapSource)[6] // self.textWidth
        
    def setFPS(self, newFrameRate):
        self.frameRate = newFrameRate
    
    async def update(self):
        # Update screen and sleep to give webpage UI time
        pygame.display.flip()
        await asyncio.sleep(0)
        self.clock.tick(self.frameRate)

        # if self.frameRate>0:
        #     frameTimeRemaining = round(1000/self.frameRate) - ticks_diff(ticks_ms(), self.lastUpdateEnd)
        #     while(frameTimeRemaining>1):
        #         buttonA.update()
        #         buttonB.update()
        #         buttonU.update()
        #         buttonD.update()
        #         buttonL.update()
        #         buttonR.update()
        #         sleep_ms(1)
        #         frameTimeRemaining = round(1000/self.frameRate) - ticks_diff(ticks_ms(), self.lastUpdateEnd)
        #     while(frameTimeRemaining>0):
        #         frameTimeRemaining = round(1000/self.frameRate) - ticks_diff(ticks_ms(), self.lastUpdateEnd)
        # self.lastUpdateEnd=ticks_ms()

        # Look for quit events (escape or exit button)
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    pygame.quit()

    def brightness(self, setting):
        pass

    def fill(self, color):
        color *= 255
        self.surface.fill((color, color, color))

    def setPixel(self, x, y, color):
        color *= 255
        self.surface.set_at((x, y), (color, color, color))

    def getPixel(self, x, y) -> int:
        if not 0<=x<int(self.width):
            return 0
        if not 0<=y<int(self.height):
            return 0

        return int(self.surface.get_at((x, y))[0] / 255)

    def drawLine(self, x1, y1, x2, y2, color):
        color *= 255
        pygame.draw.line(self.surface, (color, color, color), (x1, y1), (x2, y2))

    def drawRectangle(self, x, y, width, height, color):
        color *= 255
        pygame.draw.rect(self.surface, (color, color, color), pygame.Rect(x, y, width, height), 1)

    def drawFilledRectangle(self, x, y, width, height, color):
        color *= 255
        self.surface.fill((color, color, color), pygame.Rect(x, y, width, height))

    def drawText(self, stringToPrint, x, y, color):
        color *= 255
        stringToPrint = bytearray(stringToPrint, "utf8")
        stringCharIndex = 0
        while stringCharIndex < len(stringToPrint):
            charBitMap = stringToPrint[stringCharIndex] - 0x20
            
            if 0 <= charBitMap <= self.textCharCount:
                if x+self.textWidth > 0 and x < self.width and y+self.textHeight > 0 and y < self.height:
                    self.textBitmapFile.seek(self.textWidth*charBitMap)
                    self.textBitmap = self.textBitmapFile.read(self.textWidth)

                    # Write each VLSB byte and bit to the pygame surface for mirroring
                    ib = 0
                    for row in range(0, self.textHeight, 8):
                        for col in range(0, self.textWidth, 1):
                            for i in range(0, 8, 1):
                                if ((self.textBitmap[ib] & (0b00000001 << i)) >> i) == 1:
                                    self.surface.set_at((x+col, y+row + i), (color, color, color))
                            ib += 1

            stringCharIndex += 1
            x += self.textWidth + self.textSpaceWidth

    def blit(self, sprtptr, x, y, width, height, key, mirrorX, mirrorY):
        blitSurface = pygame.Surface((width, height))

        # Write each VLSB byte and bit to the pygame surface for mirroring
        ib = 0
        for row in range(0, height, 8):
            for col in range(0, width, 1):
                if ib >= len(sprtptr):
                    break

                for i in range(0, 8, 1):
                    color = ((sprtptr[ib] & (0b00000001 << i)) >> i) * 255
                    blitSurface.set_at((col, row + i), (color, color, color))
                ib += 1
        
        # Do the mirroring
        pygame.transform.flip(blitSurface, mirrorX, mirrorY)

        # Take each pixel from blitting surface and copy to screen surface while obeying key rule
        for ix in range(0, width, 1):
            for iy in range(0, height, 1):
                color = blitSurface.get_at((ix, iy))
                if int(key * 255) != int(color[0]):
                    self.surface.set_at((x+ix, y+iy), color)

    def drawSprite(self, s):
        self.blit(s.bitmap, int(s.x), int(s.y), s.width, s.height, s.key, s.mirrorX, s.mirrorY)

    def blitWithMask(self, sprtptr, x, y, width, height, key, mirrorX, mirrorY, maskptr):
        self.blit(sprtptr, int(x), int(y), width, height, key, mirrorX, mirrorY)

    def drawSpriteWithMask(self, s, m):
        self.blit(s.bitmap, int(s.x), int(s.y), s.width, s.height, s.key, s.mirrorX, s.mirrorY)
        

display = GraphicsClass(72, 40)
