from framebuf import FrameBuffer, MONO_HLSB
import types
import time

# Representation of the CHIP-8 display. Supports two planes and two screen
# sizes. Implementation in MicroPython of all the operations, which isn't the
# fastest, but is accurate to CHIP-8 and friends.
class AccurateDisplay:
    def __init__(self, cpu):
        self.cpu = cpu

    def reset(self):
        self.width = 64
        self.height = 32
        self.numPlanes = 1
        self.selectedPlane = 1
        self.dirty = True
        self.waitForInt = 0
        self.initBuffers()

    @micropython.native
    def initBuffers(self):
        self.buffers = [
            bytearray(int(self.width*self.height/8)),
            bytearray(int(self.width*self.height/8))
        ]
        self.frameBuffers = [
            FrameBuffer(self.buffers[0], self.width, self.height, MONO_HLSB),
            FrameBuffer(self.buffers[1], self.width, self.height, MONO_HLSB)
        ]

    # Called by 60Hz interrupt timer for dispQuirk
    @micropython.native
    def interrupt(self):
        self.waitForInt = 1

    # Clears currently selected plane
    @micropython.native
    def clear(self):
        self.clearPlanes(self.selectedPlane)

    # Clears given planes
    @micropython.native
    def clearPlanes(self, planes):
        for i in range(len(self.buffers)):
            if (i+1) & planes > 0:
                for j in range(len(self.buffers[i])):
                    self.buffers[i][j] = 0
        self.dirty = True

    @micropython.native
    def scrollDown(self, n):
        offset = int(self.width * n / 8)
        for plane in range(1, 3):
            if (plane & self.selectedPlane) == 0:
                continue
            for i in range(len(self.buffers[plane-1]) - 1, -1, -1):
                self.buffers[plane-1][i] = self.buffers[plane-1][i - offset] if i > offset else 0
            self.dirty = True

    @micropython.native
    def scrollUp(self, n):
        offset = int(self.width * n / 8)
        for plane in range(1, 3):
            if (plane & self.selectedPlane) == 0:
                continue
            maxIndex = len(self.buffers[plane-1])
            for i in range(maxIndex):
                self.buffers[plane-1][i] = self.buffers[plane-1][i + offset] if i + offset < maxIndex else 0
            self.dirty = True

    @micropython.native
    def scrollLeft(self):
        for plane in range(1, 3):
            if (plane & self.selectedPlane) == 0:
                continue
            for i in range(len(self.buffers[plane-1])):
                right = self.buffers[plane-1][i+1] >> 4 if (i+1) % self.width / 8 != 0 else 0
                left = self.buffers[plane-1][i] << 4
                self.buffers[plane-1][i] = left | right
            self.dirty = True

    @micropython.native
    def scrollRight(self):
        for plane in range(1, 3):
            if (plane & self.selectedPlane) == 0:
                continue
            for i in range(len(self.buffers[plane-1]) - 1, -1, -1):
                left = self.buffers[plane-1][i-1] << 4 if i % self.width / 8 != 0 else 0
                right = self.buffers[plane-1][i] >> 4
                self.buffers[plane-1][i] = left | right
            self.dirty = True

    @micropython.native
    def draw(self, x:int, y:int, n:int):
        if self.cpu.dispQuirk:
            self.waitForInterrupt()
        self.drawSprite(x, y, n)
        self.dirty = True

    @micropython.viper
    def drawSprite(self, x:int, y:int, n:int):
    	# Get real sprite position & height
    	xPos:int = int(self.cpu.v[x]) % int(self.width)
    	yPos:int = int(self.cpu.v[y]) % int(self.height)
        height:int = n
        if height == 0:
            self.cpu.bumpSpecType(types.SCHIP)
            height = 16

        # Do the actual drawing
        erases:bool = False
        ramPtr:ptr8 = ptr8(self.cpu.ram)
        ramIndx:int = int(self.cpu.i)
        selPlane:int = int(self.selectedPlane)
        bufSize:int = int(self.width) * int(self.height) >> 3
        width:int = int(self.width)
        pixels:int = 0
        offset:int = xPos & 7 # = xPos % 8
        clip:bool = self.cpu.clipQuirk

        for plane in range(1, 3):                   # Go through both planes
            if plane & selPlane == 0:               # Only manipulate if this plane is currently selected
                continue
            bufPtr:ptr8 = ptr8(self.buffers[plane-1])
            bufIndx:int = (yPos*width + xPos) >> 3
            for i in range(height):                 # Draw N lines
                # Does this line fall off the bottom of the screen?
                if bufIndx >= bufSize:
                    if clip:
                        continue
                    else:
                        bufIndx -= bufSize

                pixels = ramPtr[ramIndx]

                # Render left byte
                erases = erases or bufPtr[bufIndx] & (pixels >> offset) != 0
                bufPtr[bufIndx] = bufPtr[bufIndx] ^ (pixels >> offset)

                # Render right byte if needed
                if offset > 0 and bufIndx + 1 < bufSize:
                    erases = erases or bufPtr[bufIndx+1] & (pixels << 8 - offset) != 0
                    bufPtr[bufIndx+1] = bufPtr[bufIndx+1] ^ (pixels << 8 - offset)

                ramIndx += 1

                if height == 16 and bufIndx + 1 < bufSize:
                    pixels = ramPtr[ramIndx]

                    # Render right byte again
                    erases = erases or bufPtr[bufIndx+1] & (pixels >> offset) != 0
                    bufPtr[bufIndx+1] = bufPtr[bufIndx+1] ^ (pixels >> offset)

                    # Render third byte if needed
                    if offset > 0 and bufIndx + 2 < bufSize:
                        erases = erases or bufPtr[bufIndx+2] & (pixels << 8 - offset) != 0
                        bufPtr[bufIndx+2] = bufPtr[bufIndx+2] ^ (pixels << 8 - offset)

                    ramIndx += 1

                bufIndx += width >> 3

        self.cpu.v[0xF] = 1 if erases else 0 # Set collision flag

    @micropython.native
    def waitForInterrupt(self):
        self.waitForInt = 0
        while self.waitForInt == 0:
            time.sleep_ms(1)

    @micropython.native
    def setResolution(self, width, height):
        self.width = width
        self.height = height
        self.initBuffers()




class FastDisplay:
    def __init__(self, cpu):
        self.cpu = cpu

    def reset(self):
        self.width = 64
        self.height = 32
        self.numPlanes = 1
        self.selectedPlane = 1
        self.dirty = True
        self.frameBuffers = [
            FrameBuffer(bytearray(int(128*64/8)), 128, 64, MONO_HLSB),
            FrameBuffer(bytearray(int(128*64/8)), 128, 64, MONO_HLSB)
        ]

    @micropython.viper
    def interrupt(self):
        return

    # Clears currently selected plane
    @micropython.viper
    def clear(self):
        self.clearPlanes(self.selectedPlane)

    # Clears given planes
    @micropython.native
    def clearPlanes(self, planes):
        for i in range(len(self.frameBuffers)):
            if (i+1) & planes > 0:
                self.frameBuffers[i].fill(0)
        self.dirty = True

    @micropython.native
    def scrollDown(self, n):
        for i in range(len(self.frameBuffers)):
            if (i+1) & self.selectedPlane > 0:
                self.frameBuffers[i].scroll(0, n)

    @micropython.native
    def scrollUp(self, n):
        for i in range(len(self.frameBuffers)):
            if (i+1) & self.selectedPlane > 0:
                self.frameBuffers[i].scroll(0, -1 * n)

    @micropython.native
    def scrollLeft(self):
        for i in range(len(self.frameBuffers)):
            if (i+1) & self.selectedPlane > 0:
                self.frameBuffers[i].scroll(-1, 0)

    @micropython.native
    def scrollRight(self):
        for i in range(len(self.frameBuffers)):
            if (i+1) & self.selectedPlane > 0:
                self.frameBuffers[i].scroll(1, 0)

    @micropython.native
    def draw(self, x:int, y:int, n:int):
        self.drawSprite(x, y, n)
        self.dirty = True

    @micropython.native
    def drawSprite(self, x:int, y:int, n:int):
        # Get real sprite position & height
    	xPos:int = self.cpu.v[x] % self.width
    	yPos:int = self.cpu.v[y] % self.height
        height:int = n
        if height == 0:
            self.cpu.bumpSpecType(types.SCHIP)
            height = 16

        # TODO: 16 by 16 sprites

        selPlane:int = int(self.selectedPlane)
        sprite = self.cpu.ram[self.cpu.a(self.cpu.i):self.cpu.a(self.cpu.i + 16)]

        for plane in range(1, 3):                   # Go through both planes
            if plane & selPlane != 0:               # Only manipulate if this plane is currently selected
                self.frameBuffers[plane-1].blit(
                    FrameBuffer(sprite, 8, height, MONO_HLSB),
                    xPos, yPos, 8, height
                )

        self.cpu.v[0xF] = 0 # Never a collision

    @micropython.native
    def setResolution(self, width, height):
        self.width = width
        self.height = height
        self.clearPlanes(3)
