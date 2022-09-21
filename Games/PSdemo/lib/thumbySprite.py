import os


# Sprite class for holding pixel data 
class Sprite:
    def __init__(self, width, height, bitmapData, x = 0, y=0, key=-1, mirrorX=False, mirrorY=False):
        self.width = width
        self.height = height
        self.bitmapSource = bitmapData
        self.bitmapByteCount = width*(height//8)
        if(height%8):
            self.bitmapByteCount+=width
        self.frameCount = 1
        self.currentFrame = 0
        if type(self.bitmapSource)==str:
            self.bitmap = bytearray(self.bitmapByteCount)
            self.file = open(self.bitmapSource,'rb')
            self.file.readinto(self.bitmap)
            self.frameCount = os.stat(self.bitmapSource)[6] // self.bitmapByteCount
        elif type(self.bitmapSource)==bytearray:
            self.bitmap = memoryview(self.bitmapSource)[0:self.bitmapByteCount]
            self.frameCount = len(self.bitmapSource) // self.bitmapByteCount
        self.x = x
        self.y = y
        self.key = key
        self.mirrorX = mirrorX
        self.mirrorY = mirrorY

    def getFrame(self):
        return self.currentFrame

    def setFrame(self, frame):
        if(frame >= 0 and (self.currentFrame is not frame % (self.frameCount))):
            self.currentFrame = frame % (self.frameCount)
            offset=self.bitmapByteCount*self.currentFrame
            if type(self.bitmapSource)==str:
                self.file.seek(offset)
                self.file.readinto(self.bitmap)
                #f.close()
            elif type(self.bitmapSource)==bytearray:
                self.bitmap = memoryview(self.bitmapSource)[offset:offset+self.bitmapByteCount]