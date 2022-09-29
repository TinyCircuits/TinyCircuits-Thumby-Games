import os
import copy



# Redefine the open function to create a directory for a file if it doesn't already exist (mimic MicroPython)
def new_open(path, mode):
    if str(type(path)) == "<class 'pathlib.PosixPath'>":
        path = path.as_posix()

    # If absolute path, append CPython wasm path to building root (mimic Thumby FS)
    if path[0] == '/':
        path = '/data/data/building/assets' + path

    from pathlib import Path
    
    filename = Path(path)
    try:
        filename.parent.mkdir(parents=True, exist_ok=True)
    except:
        pass

    return __builtins__["old_open"](path, mode)


def new_stat(path, follow_symlinks=True):
    if str(type(path)) == "<class 'pathlib.PosixPath'>":
        path = path.as_posix()

    # If absolute path, append CPython wasm path to building root (mimic Thumby FS)
    if path[0] == '/':
        path = '/data/data/building/assets' + path
    
    return os.old_stat(path, follow_symlinks=follow_symlinks)


__builtins__["old_open"] = copy.deepcopy(__builtins__["open"])
__builtins__["open"] = new_open

os.old_stat = copy.deepcopy(os.stat)
os.stat = new_stat



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