from utime import sleep_ms, ticks_diff, ticks_ms, sleep_us
from machine import Pin, SPI, idle, mem32
import _thread
from os import stat
from math import sqrt, floor
from array import array
from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR
from thumbyHardware import HWID
from sys import modules

__version__ = '4.0.2-hemlock'


emulator = None
try:
    import emulator
except ImportError:
    pass

@micropython.viper
def fpdiv(a:int, b:int) -> int:
    return ((a << 6) // (b >> 6)) << 4

@micropython.viper
def fpmul(a:int, b:int) -> int:
    return (a >> 6) * (b >> 6) >> 4
        
class Sprite:
    @micropython.native
    def __init__(self, width, height, bitmapData, x = 0, y=0, key=-1, mirrorX=False, mirrorY=False):
        self.width = width
        self.height = height
        self.scaledWidth = width
        self.scaledHeight = height
        self.scale = 1<<16
        self.bitmapSource = bitmapData
        self.bitmapByteCount = width*(height//8)
        if(height%8):
            self.bitmapByteCount+=width
        self.frameCount = 1
        self.currentFrame = 0
        self._shaded = False
        self._usesFile = False
        if isinstance(bitmapData, (tuple, list)):
            if (len(bitmapData) != 2) or (type(bitmapData[0]) != type(bitmapData[1])):
                raise ValueError('bitmapData must be a bytearray, string, or tuple of two bytearrays or strings')
            self._shaded = True
            if isinstance(bitmapData[0], str):
                self._usesFile = True
                if stat(bitmapData[0])[6] != stat(bitmapData[1])[6]:
                    raise ValueError('Sprite files must match in size')
                self.bitmap = (bytearray(self.bitmapByteCount), bytearray(self.bitmapByteCount))
                self.files = (open(bitmapData[0],'rb'),open(bitmapData[1],'rb'))
                self.files[0].readinto(self.bitmap[0])
                self.files[1].readinto(self.bitmap[1])
                self.frameCount = stat(bitmapData[0])[6] // self.bitmapByteCount
            elif isinstance(bitmapData[0], bytearray):
                if len(bitmapData[0]) != len(bitmapData[1]):
                    raise ValueError('Sprite bitplanes must match in size')
                self.frameCount = len(bitmapData[0]) // self.bitmapByteCount
                self.bitmap = [
                    memoryview(bitmapData[0])[0:self.bitmapByteCount],
                    memoryview(bitmapData[1])[0:self.bitmapByteCount]
                ]
            else:
                raise ValueError('bitmapData must be a bytearray, string, or tuple of two bytearrays or strings')
        elif isinstance(bitmapData, str):
            self._usesFile = True
            self.bitmap = bytearray(self.bitmapByteCount)
            self.file = open(bitmapData,'rb')
            self.file.readinto(self.bitmap)
            self.frameCount = stat(bitmapData)[6] // self.bitmapByteCount
        elif isinstance(bitmapData, bytearray):
            self.bitmap = memoryview(bitmapData)[0:self.bitmapByteCount]
            self.frameCount = len(bitmapData) // self.bitmapByteCount
        else:
            raise ValueError('bitmapData must be a bytearray, string, or tuple of two bytearrays or strings')
        self.x = x
        self.y = y
        self.key = key
        self.mirrorX = mirrorX
        self.mirrorY = mirrorY

    @micropython.native
    def getFrame(self):
        return self.currentFrame

    @micropython.native
    def setFrame(self, frame):
        if(frame >= 0 and (self.currentFrame is not frame % (self.frameCount))):
            self.currentFrame = frame % (self.frameCount)
            offset=self.bitmapByteCount*self.currentFrame
            if self._shaded:
                if self._usesFile:
                    self.files[0].seek(offset)
                    self.files[1].seek(offset)
                    self.files[0].readinto(self.bitmap[0])
                    self.files[1].readinto(self.bitmap[1])
                else:
                    self.bitmap[0] = memoryview(self.bitmapSource[0])[offset:offset+self.bitmapByteCount]
                    self.bitmap[1] = memoryview(self.bitmapSource[1])[offset:offset+self.bitmapByteCount]
            else:
                if self._usesFile:
                    self.file.seek(offset)
                    self.file.readinto(self.bitmap)
                else:
                    self.bitmap = memoryview(self.bitmapSource)[offset:offset+self.bitmapByteCount]

    @micropython.native
    def setScale(self, scale:int):
        self.scale = scale
        self.scaledWidth = fpmul(self.width<<16, scale)>>16
        self.scaledHeight = fpmul(self.height<<16, scale)>>16
    
    @micropython.native
    def setLifes(self, lifes:int):
        self.lifes = lifes
    
    @micropython.native
    def getLifes(self) -> int:
        return self.lifes
        
_THREAD_STOPPED    = const(0)
_THREAD_RUNNING    = const(1)
_THREAD_STOPPING   = const(2)
_ST_THREAD       = const(0)
_ST_COPY_BUFFS   = const(1)
_ST_PENDING_CMD  = const(2)
_ST_INVERT       = const(3)
_ST_CALIBRATOR   = const(4)
_ST_MODE         = const(5)
_params = bytearray([
    # time_pre
    75, 75, 75,
    90, 90,  0,
    75, 75, 75,
    75, 75, 75,
    90, 90,  0,
    75, 75, 75,
    # time_end
    56, 56, 56,
    44, 42, 48,
    56, 56, 56,
    56, 56, 56,
    44, 42, 48,
    56, 56, 56,
    # offset
    47, 47, 47,
    60, 62, 56,
    47, 47, 47,
    47, 47, 47,
    60, 62, 56,
    47, 47, 47,
    # mux
    56, 56, 56,
    43, 41, 47,
    56, 56, 56,
    56, 56, 56,
    43, 41, 47,
    56, 56, 56])

_WIDTH = const(72)
_HEIGHT = const(40)
_BUFF_SIZE = const((_HEIGHT // 8) * _WIDTH)
_BUFF_INT_SIZE = const(_BUFF_SIZE // 4)


class Grayscale:

    BLACK     = 0
    WHITE     = 1
    DARKGRAY  = 2
    LIGHTGRAY = 3

    def __init__(self):
        self._spi = SPI(0, sck=Pin(18), mosi=Pin(19))
        self._dc = Pin(17)
        self._cs = Pin(16)
        self._res = Pin(20)
        self._spi.init(baudrate=100 * 1000 * 1000, polarity=0, phase=0)
        self._res.init(Pin.OUT, value=1)
        self._dc.init(Pin.OUT, value=0)
        self._cs.init(Pin.OUT, value=1)

        self.display = self # This acts as both the GraphicsClass and SSD1306
        self.pages = _HEIGHT // 8
        self.width = _WIDTH
        self.height = _HEIGHT
        self.max_x = _WIDTH - 1
        self.max_y = _HEIGHT - 1

        self.drawBuffer = bytearray(_BUFF_SIZE*2)
        self.buffer = memoryview(self.drawBuffer)[:_BUFF_SIZE]
        self.shading = memoryview(self.drawBuffer)[_BUFF_SIZE:]

        self._subframes = array('O', [bytearray(_BUFF_SIZE),
            bytearray(_BUFF_SIZE), bytearray(_BUFF_SIZE)])

        self._brightness = 127
        try:
            with open("thumby.cfg", "r") as fh:
                _, _, conf = fh.read().partition("brightness,")
                b = int(conf.split(',')[0])
                # Set to the relevant brightness level
                if b == 0: self._brightness = 1
                if b == 1: self._brightness = 28
        except (OSError, ValueError):
            pass
        self._contrastSrc = bytearray(18)
        self._contrast = bytearray(3)

        self._state = array('I', [_THREAD_STOPPED,0,0,0,87,0])

        self._pendingCmds = bytearray(8)

        self.setFont('lib/font5x7.bin', 5, 7, 1)

        self.lastUpdateEnd = 0
        self.frameRate = 0

        self._initEmuScreen()

        if 'thumbyGraphics' in modules:
            self.buffer[:] = modules['thumbyGraphics'].display.display.buffer
        self.init_display()

        self.brightness(self._brightness)

        if not emulator:
            try:
                with open("thumbyGS.cfg", "r") as fh:
                    vls = fh.read().split('\n')
                    for fhd in vls:
                        if fhd.startswith('gsV3,'):
                            _, _, conf = fhd.partition("timing,")
                            self._state[_ST_CALIBRATOR] = int(conf.split(',')[0])
                            _, _, conf = fhd.partition("oled,")
                            self._state[_ST_MODE] = int(conf.split(',')[0])
                            break
                    else:
                        raise ValueError()

            except (OSError, ValueError):
                if HWID < 2:
                    self._state[_ST_CALIBRATOR] = 87
                    self._state[_ST_MODE] = 0
                else:
                    self.calibrate()

    def __enter__(self):
        self.enableGrayscale()
        return self
        
    def __exit__(self, type, value, traceback):
        self.disableGrayscale()


    @micropython.viper
    def _initEmuScreen(self):
        if not emulator:
            return
        Pin(2, Pin.OUT) # Ready display handshake pin
        emulator.screen_breakpoint(ptr16(self.drawBuffer))
        self._clearEmuFunctions()

    def _clearEmuFunctions(self):
        def _disabled(*arg, **kwdarg):
            pass
        self.invert = _disabled
        self.reset = _disabled
        self.poweron = _disabled
        self.poweroff = _disabled
        self.init_display = _disabled
        self.write_cmd = _disabled


    def reset(self):
        self._res(1)
        sleep_us(10)
        self._res(0)
        sleep_us(10)
        self._res(1)
        sleep_us(20)

    def init_display(self):
        self.reset()
        self._cs(0)
        self._dc(0)
        self._spi.write(bytearray([
            0xae, 0x20,0x00, 0x40, 0xa1, 0xa8,39, 0xc8, 0xd3,0, 0xda,0x12,
            0xd5,0xf0, 0xd9,0x11, 0xdb,0x20, 0xa4, 0xa6, 0x8d,0x14, 0xad,0x30, 0xaf]))
        self._dc(1)
        # Clear the entire GDRAM
        zero32 = bytearray([0] * 32)
        for _ in range(32):
            self._spi.write(zero32)
        self._dc(0)
        self._spi.write(bytearray([0x21,28,99, 0x22,0,4]))

    def enableGrayscale(self):
        if emulator:
            emulator.screen_breakpoint(1)
            self.show()
            return

        if self._state[_ST_THREAD] == _THREAD_RUNNING:
            return

        _thread.stack_size(2048)
        self._init_grayscale()
        _thread.start_new_thread(self._display_thread, ())
        while self._state[_ST_THREAD] != _THREAD_RUNNING:
            idle()


    def disableGrayscale(self):
        if emulator:
            emulator.screen_breakpoint(0)
            self.show()
            return

        if self._state[_ST_THREAD] != _THREAD_RUNNING:
            return
        self._state[_ST_THREAD] = _THREAD_STOPPING
        while self._state[_ST_THREAD] != _THREAD_STOPPED:
            idle()
        self._deinit_grayscale()
        # Draw B/W view of current frame
        self.show()
        # Resume device color inversion
        if self._state[_ST_INVERT]:
            self.write_cmds(0xa6 | 1)
        self.brightness(self._brightness)


    @micropython.native
    def write_cmd(self, cmd):
        if isinstance(cmd, list):
            cmd = bytearray(cmd)
        elif not isinstance(cmd, bytearray):
            cmd = bytearray([cmd])
        if self._state[_ST_THREAD] == _THREAD_RUNNING:
            pendingCmds = self._pendingCmds
            if len(cmd) > len(pendingCmds):
                raise ValueError('Cannot send more than %u bytes using write_cmd()' % len(pendingCmds))
            i = 0
            while i < len(cmd):
                pendingCmds[i] = cmd[i]
                i += 1
            while i < len(pendingCmds):
                pendingCmds[i] = 0x3e
                i += 1
            self._state[_ST_PENDING_CMD] = 1
            while self._state[_ST_PENDING_CMD]:
                idle()
        else:
            self._dc(0)
            self._spi.write(cmd)

    def poweroff(self):
        self.write_cmd(0xae)
    def poweron(self):
        self.write_cmd(0xaf)


    @micropython.viper
    def invert(self, invert:int):
        state = ptr32(self._state)
        invert = 1 if invert else 0
        state[_ST_INVERT] = invert
        state[_ST_COPY_BUFFS] = 1
        if state[_ST_THREAD] != _THREAD_RUNNING:
            self.write_cmd(0xa6 | invert)


    @micropython.viper
    def show(self):
        state = ptr32(self._state)
        if state[_ST_THREAD] == _THREAD_RUNNING:
            state[_ST_COPY_BUFFS] = 1
            while state[_ST_COPY_BUFFS] != 0:
                idle()
        elif emulator:
            mem32[0xD0000000+0x01C] = 1 << 2
        else:
            self._dc(1)
            self._spi.write(self.buffer)

    @micropython.viper
    def show_async(self):
        state = ptr32(self._state)
        if state[_ST_THREAD] == _THREAD_RUNNING:
            state[_ST_COPY_BUFFS] = 1
        else:
            self.show()


    @micropython.native
    def setFPS(self, newFrameRate):
        self.frameRate = newFrameRate

    @micropython.native
    def update(self):
        self.show()
        if self.frameRate > 0:
            frameTimeMs = 1000 // self.frameRate
            lastUpdateEnd = self.lastUpdateEnd
            frameTimeRemaining = frameTimeMs - ticks_diff(ticks_ms(), lastUpdateEnd)
            while frameTimeRemaining > 1:
                buttonA.update()
                buttonB.update()
                buttonU.update()
                buttonD.update()
                buttonL.update()
                buttonR.update()
                sleep_ms(1)
                frameTimeRemaining = frameTimeMs - ticks_diff(ticks_ms(), lastUpdateEnd)
            while frameTimeRemaining > 0:
                frameTimeRemaining = frameTimeMs - ticks_diff(ticks_ms(), lastUpdateEnd)
        self.lastUpdateEnd = ticks_ms()

    @micropython.viper
    def brightness(self, c:int):
        if c < 1: c = 1
        if c > 127: c = 127
        state = ptr32(self._state)
        contrastSrc = ptr8(self._contrastSrc)

        cc = int(floor(sqrt(c<<17)))
        contrastSrc[0] = (cc*30>>12)-1
        contrastSrc[1] = (cc*72>>12)+14
        c3 = (cc*340>>12)+20
        contrastSrc[2] = c3 if c3 < 255 else 255
        contrastSrc[3] = (cc*30>>12)-1
        contrastSrc[4] = (cc*257>>12)
        contrastSrc[5] = (cc*257>>12)
        contrastSrc[6] = (cc*50>>12)-3
        contrastSrc[7] = (cc*50>>12)-3
        c3 = (cc*340>>12)-20
        contrastSrc[8] = c3 if c3 < 255 else 255
        contrastSrc[9] = contrastSrc[3]
        contrastSrc[10] = contrastSrc[4]
        contrastSrc[11] = contrastSrc[5]
        contrastSrc[12] = contrastSrc[3]
        contrastSrc[13] = contrastSrc[4]
        contrastSrc[14] = contrastSrc[5]
        contrastSrc[15] = contrastSrc[3]
        contrastSrc[16] = contrastSrc[4]
        contrastSrc[17] = contrastSrc[5]

        if state[_ST_THREAD] != _THREAD_RUNNING:
            if emulator:
                emulator.brightness_breakpoint(c)
            else:
                self.write_cmd([0x81, c])
        setattr(self, '_brightness', c)

    @micropython.viper
    def _init_grayscale(self):
        state = ptr32(self._state)
        contrastSrc = ptr8(self._contrastSrc)
        contrast = ptr8(self._contrast)
        mode = state[_ST_MODE]

        # Draw and sub-frame buffers in 32bit for fast copying
        bb = ptr32(self.buffer)
        bs = ptr32(self.shading)
        b1 = ptr32(self._subframes[0])
        b2 = ptr32(self._subframes[1])
        b3 = ptr32(self._subframes[2])
        d1 = int(0xAA55AA55)
        d2 = int(0x55AA55AA)

        sio = ptr32(0xd0000000)
        spi0 = ptr32(0x4003c000)
        tmr = ptr32(0x40054000)

        i = 0
        inv = -1 if state[_ST_INVERT] else 0
        while i < _BUFF_INT_SIZE:
            v1 = bb[i] ^ inv
            v2 = bs[i]
            wd = v1 ^ v2
            w = v1 & wd
            di = ((i&3)+i)&1
            di1 = (d1 if di else d2)
            di2 =  (d2 if di else d1)
            b1[i] = wd # white || darkGray [DIM]
            b2[i] = v1 # white || lightGray [MID]
            b3[i] = w # white [BRIGHT]
            if mode == 0:
                b1[i] = v1 | v2 # white || lightGray || darkGray [DIM]
            elif mode == 2:
                b1[i] = v1 | (v2 & di1) # white || lightGray || dither-darkGray [DIM]
                b2[i] = v1 | (v2 & di2) # white || lightGray || dither-darkGray [DIM]
            elif mode >= 4:
                lg = v1 & v2
                b2[i] = w | (lg & di1) # white || dither-lightGray [BRIGHT]
                b3[i] = w | (lg & di2) # white || dither-lightGray [BRIGHT]
            i += 1

        while (spi0[3] & 4) == 4: i = spi0[2]
        while (spi0[3] & 0x10) == 0x10: pass
        while (spi0[3] & 4) == 4: i = spi0[2]
        sio[5] = 1 << 17 # dc(1)
        i = 0
        blitsub = ptr8(self._subframes[0])
        while i < 144:
            while (spi0[3] & 2) == 0: pass
            spi0[2] = blitsub[i]
            i += 1

        while (spi0[3] & 4) == 4: i = spi0[2]
        while (spi0[3] & 0x10) == 0x10: pass
        while (spi0[3] & 4) == 4: i = spi0[2]
        sio[6] = 1 << 17 # dc(0)

        cmode = state[_ST_MODE]*3
        contrast[0] = contrastSrc[cmode]
        contrast[1] = contrastSrc[cmode + 1]
        contrast[2] = contrastSrc[cmode + 2]
        spi0[2] = 0x81; spi0[2] = contrast[0]

        spi0[2] = 0xae
        spi0[2] = 0xd3; spi0[2] = 47
        time_pre = tmr[10] + 4000
        while (tmr[10] - time_pre) < 0: pass
        spi0[2] = 0xa8; spi0[2] = 1 # Row resets OLED2
        spi0[2] = 0xa6 # disable hardware invert
        spi0[2] = 0xaf # Row resets OLED1

    @micropython.viper
    def _display_thread(self):
        state = ptr32(self._state)
        contrastSrc = ptr8(self._contrastSrc)
        contrast = ptr8(self._contrast)
        pendingCmds = ptr8(self._pendingCmds)
        params = ptr8(_params)
        mode = state[_ST_MODE]

        bb = ptr32(self.buffer)
        bs = ptr32(self.shading)
        sf = self._subframes
        b1 = ptr32(sf[0])
        b2 = ptr32(sf[1])
        b3 = ptr32(sf[2])
        subframes = ptr32(array('L', [b1, b2, b3]))
        d1 = int(0xAA55AA55)
        d2 = int(0x55AA55AA)

        sio = ptr32(0xd0000000)
        spi0 = ptr32(0x4003c000)
        tmr = ptr32(0x40054000)

        state[_ST_THREAD] = _THREAD_RUNNING
        while state[_ST_THREAD] == _THREAD_RUNNING:
            calib = state[_ST_CALIBRATOR]
            fn = 0
            while fn < 3:
                mfn = mode*3+fn
                time_pre = tmr[10] + params[mfn]*10

                if fn != 2 or mode != 1:
                    spi0[2] = 0xd3; spi0[2] = 40
                    spi0[2] = 0xa8; spi0[2] = 1

                while (tmr[10] - time_pre) < 0: pass

                spi0[2] = 0x81; spi0[2] = contrast[fn]

                spi0[2] = 0xd3
                spi0[2] = params[36+mfn]
                spi0[2] = 0xa8
                spi0[2] = params[54+mfn]

                spi0[2] = 0x81; spi0[2] = contrast[fn]

                while (spi0[3] & 4) == 4: i = spi0[2]
                while (spi0[3] & 0x10) == 0x10: pass
                while (spi0[3] & 4) == 4: i = spi0[2]
                sio[5] = 1 << 17 # dc(1)

                blitsub = ptr8(subframes[fn])
                i = 144
                while i < 360:
                    if i == 216:
                        while (tmr[10] - (time_pre + 8*calib)) < 0: pass
                    if i == 288:
                        while (tmr[10] - (time_pre + 16*calib)) < 0: pass
                    while (spi0[3] & 2) == 0: pass
                    spi0[2] = blitsub[i]
                    i += 1

                if fn == 2 and (state[_ST_COPY_BUFFS] != 0 or mode != state[_ST_MODE]):
                    i = 0
                    inv = -1 if state[_ST_INVERT] else 0
                    mode = state[_ST_MODE]
                    while i < _BUFF_INT_SIZE:
                        v1 = bb[i] ^ inv
                        v2 = bs[i]
                        wd = v1 ^ v2
                        w = v1 & wd
                        di = ((i&3)+i)&1
                        di1 = (d1 if di else d2)
                        di2 =  (d2 if di else d1)
                        b1[i] = wd # white || darkGray [DIM]
                        b2[i] = v1 # white || lightGray [MID]
                        b3[i] = w # white [BRIGHT]
                        if mode == 0:
                            b1[i] = v1 | v2 # white || lightGray || darkGray [DIM]
                        elif mode == 2:
                            b1[i] = v1 | (v2 & di1) # white || lightGray || dither-darkGray [DIM]
                            b2[i] = v1 | (v2 & di2) # white || lightGray || dither-darkGray [DIM]
                        elif mode >= 4:
                            lg = v1 & v2
                            b2[i] = w | (lg & di1) # white || dither-lightGray [BRIGHT]
                            b3[i] = w | (lg & di2) # white || dither-lightGray [BRIGHT]
                        i += 1
                    state[_ST_COPY_BUFFS] = 0
                    cmode = mode*3
                    contrast[0] = contrastSrc[cmode]
                    contrast[1] = contrastSrc[cmode + 1]
                    contrast[2] = contrastSrc[cmode + 2]

                blitsub = ptr8(subframes[fn+1 if fn < 2 else 0])
                i = 0
                while (tmr[10] - (time_pre + 24*calib)) < 0: pass
                while i < 144:
                    if i == 72:
                        while (tmr[10] - (time_pre + 32*calib)) < 0: pass
                    while (spi0[3] & 2) == 0: pass
                    spi0[2] = blitsub[i]
                    i += 1

                while (spi0[3] & 4) == 4: i = spi0[2]
                while (spi0[3] & 0x10) == 0x10: pass
                while (spi0[3] & 4) == 4: i = spi0[2]
                sio[6] = 1 << 17 # dc(0)

                if fn == 2 and state[_ST_PENDING_CMD] != 0:
                    i = 0
                    while i < 8:
                        while (spi0[3] & 2) == 0: pass
                        spi0[2] = pendingCmds[i]
                        i += 1
                    state[_ST_PENDING_CMD] = 0

                while (tmr[10] - (time_pre + params[18+mfn]*calib)) < 0: pass

                fn += 1

        state[_ST_THREAD] = _THREAD_STOPPED

    @micropython.viper
    def _deinit_grayscale(self):
        spi0 = ptr32(0x4003c000)

        spi0[2] = 0xd3; spi0[2] = 0
        spi0[2] = 0xa8; spi0[2] = 39
        spi0[2] = 0x22; spi0[2] = 0; spi0[2] = 4


    @micropython.viper
    def fill(self, colour:int):
        buffer = ptr32(self.buffer)
        shading = ptr32(self.shading)
        f1 = -1 if colour & 1 else 0
        f2 = -1 if colour & 2 else 0
        i = 0
        while i < _BUFF_INT_SIZE:
            buffer[i] = f1
            shading[i] = f2
            i += 1


    @micropython.viper
    def drawFilledRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        if x + width <= 0 or x >= _WIDTH or y + height <= 0 or y >= _HEIGHT:
            return
        if width <= 0 or height <= 0: return
        if x < 0:
            width += x
            x = 0
        if y < 0:
            height += y
            y = 0
        x2 = x + width
        y2 = y + height
        if x2 > _WIDTH:
            x2 = _WIDTH
            width = _WIDTH - x
        if y2 > _HEIGHT:
            y2 = _HEIGHT
            height = _HEIGHT - y

        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)

        o = (y >> 3) * _WIDTH
        oe = o + x2
        o += x
        strd = _WIDTH - width

        c1 = colour & 1
        c2 = colour & 2
        v1 = 0xff if c1 else 0
        v2 = 0xff if c2 else 0

        yb = y & 7
        ybh = 8 - yb
        if height <= ybh:
            m = ((1 << height) - 1) << yb
        else:
            m = 0xff << yb
        im = 255-m
        while o < oe:
            if c1:
                buffer[o] |= m
            else:
                buffer[o] &= im
            if c2:
                shading[o] |= m
            else:
                shading[o] &= im
            o += 1
        height -= ybh
        while height >= 8:
            o += strd
            oe += _WIDTH
            while o < oe:
                buffer[o] = v1
                shading[o] = v2
                o += 1
            height -= 8
        if height > 0:
            o += strd
            oe += _WIDTH
            m = (1 << height) - 1
            im = 255-m
            while o < oe:
                if c1:
                    buffer[o] |= m
                else:
                    buffer[o] &= im
                if c2:
                    shading[o] |= m
                else:
                    shading[o] &= im
                o += 1


    @micropython.viper
    def drawRectangle(self, x:int, y:int, width:int, height:int, colour:int):
        dfr = self.drawFilledRectangle
        dfr(x, y, width, 1, colour)
        dfr(x, y, 1, height, colour)
        dfr(x, y+height-1, width, 1, colour)
        dfr(x+width-1, y, 1, height, colour)


    @micropython.viper
    def setPixel(self, x:int, y:int, colour:int):
        if x < 0 or x >= _WIDTH or y < 0 or y >= _HEIGHT:
            return
        o = (y >> 3) * _WIDTH + x
        m = 1 << (y & 7)
        im = 255-m
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)
        if colour & 1:
            buffer[o] |= m
        else:
            buffer[o] &= im
        if colour & 2:
            shading[o] |= m
        else:
            shading[o] &= im

    @micropython.viper
    def getPixel(self, x:int, y:int) -> int:
        if x < 0 or x >= _WIDTH or y < 0 or y >= _HEIGHT:
            return 0
        o = (y >> 3) * _WIDTH + x
        m = 1 << (y & 7)
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)
        colour = 0
        if buffer[o] & m:
            colour = 1
        if shading[o] & m:
            colour |= 2
        return colour

    @micropython.viper
    def drawLine(self, x0:int, y0:int, x1:int, y1:int, colour:int):
        if x0 == x1:
            self.drawFilledRectangle(x0, y0, 1, y1 - y0, colour)
            return
        if y0 == y1:
            self.drawFilledRectangle(x0, y0, x1 - x0, 1, colour)
            return
        dx = x1 - x0
        dy = y1 - y0
        sx = 1
        if dy < 0:
            x0,x1 = x1,x0
            y0,y1 = y1,y0
            dy = 0 - dy
            dx = 0 - dx
        if dx < 0:
            dx = 0 - dx
            sx = -1
        x = x0
        y = y0
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)

        o = (y >> 3) * _WIDTH + x
        m = 1 << (y & 7)
        im = 255-m
        c1 = colour & 1
        c2 = colour & 2

        if dx > dy:
            err = dx >> 1
            x1 += 1
            while x != x1:
                if 0 <= x < _WIDTH and 0 <= y < _HEIGHT:
                    if c1:
                        buffer[o] |= m
                    else:
                        buffer[o] &= im
                    if c2:
                        shading[o] |= m
                    else:
                        shading[o] &= im
                err -= dy
                if err < 0:
                    y += 1
                    m <<= 1
                    if m & 0x100:
                        o += _WIDTH
                        m = 1
                        im = 0xfe
                    else:
                        im = 255-m
                    err += dx
                x += sx
                o += sx
        else:
            err = dy >> 1
            y1 += 1
            while y != y1:
                if 0 <= x < _WIDTH and 0 <= y < _HEIGHT:
                    if c1:
                        buffer[o] |= m
                    else:
                        buffer[o] &= im
                    if c2:
                        shading[o] |= m
                    else:
                        shading[o] &= im
                err -= dx
                if err < 0:
                    x += sx
                    o += sx
                    err += dy
                y += 1
                m <<= 1
                if m & 0x100:
                    o += _WIDTH
                    m = 1
                    im = 0xfe
                else:
                    im = 255-m



    def setFont(self, fontFile, width, height, space):
        sz = stat(fontFile)[6]
        self.font_bmap = bytearray(sz)
        with open(fontFile, 'rb') as fh:
            fh.readinto(self.font_bmap)
        self.font_width = width
        self.font_height = height
        self.font_space = space
        self.font_glyphcnt = sz // width


    @micropython.viper
    def drawText(self, stringToPrint, x:int, y:int, colour:int):
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)
        font_bmap = ptr8(self.font_bmap)
        font_width = int(self.font_width)
        font_space = int(self.font_space)
        font_glyphcnt = int(self.font_glyphcnt)
        sm1o = 0xff if colour & 1 else 0
        sm1a = 255 - sm1o
        sm2o = 0xff if colour & 2 else 0
        sm2a = 255 - sm2o
        ou = (y >> 3) * _WIDTH + x
        ol = ou + _WIDTH
        shu = y & 7
        shl = 8 - shu
        for c in memoryview(stringToPrint):
            if isinstance(c, str):
                co = int(ord(c)) - 0x20
            else:
                co = int(c) - 0x20
            if co < font_glyphcnt:
                gi = co * font_width
                gx = 0
                while gx < font_width:
                    if 0 <= x < _WIDTH:
                        gb = font_bmap[gi + gx]
                        gbu = gb << shu
                        gbl = gb >> shl
                        if 0 <= ou < _BUFF_SIZE:
                            # paint upper byte
                            buffer[ou] = (buffer[ou] | (gbu & sm1o)) & 255-(gbu & sm1a)
                            shading[ou] = (shading[ou] | (gbu & sm2o)) & 255-(gbu & sm2a)
                        if (shl != 8) and (0 <= ol < _BUFF_SIZE):
                            # paint lower byte
                            buffer[ol] = (buffer[ol] | (gbl & sm1o)) & 255-(gbl & sm1a)
                            shading[ol] = (shading[ol] | (gbl & sm2o)) & 255-(gbl & sm2a)
                    ou += 1
                    ol += 1
                    x += 1
                    gx += 1
            ou += font_space
            ol += font_space
            x += font_space


    @micropython.viper
    def blit(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int):
        if x+width < 0 or x >= _WIDTH:
            return
        if y+height < 0 or y >= _HEIGHT:
            return
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)

        if isinstance(src, (tuple, list)):
            shd = 1
            src1 = ptr8(src[0])
            src2 = ptr8(src[1])
        else:
            shd = 0
            src1 = ptr8(src)
            src2 = ptr8(0)

        stride = width

        srcx = 0 ; srcy = 0
        dstx = x ; dsty = y
        sdx = 1
        if mirrorX:
            sdx = -1
            srcx += width - 1
            if dstx < 0:
                srcx += dstx
                width += dstx
                dstx = 0
        else:
            if dstx < 0:
                srcx = 0 - dstx
                width += dstx
                dstx = 0
        if dstx+width > _WIDTH:
            width = _WIDTH - dstx
        if mirrorY:
            srcy = height - 1
            if dsty < 0:
                srcy += dsty
                height += dsty
                dsty = 0
        else:
            if dsty < 0:
                srcy = 0 - dsty
                height += dsty
                dsty = 0
        if dsty+height > _HEIGHT:
            height = _HEIGHT - dsty

        srco = (srcy >> 3) * stride + srcx
        srcm = 1 << (srcy & 7)

        dsto = (dsty >> 3) * _WIDTH + dstx
        dstm = 1 << (dsty & 7)
        dstim = 255 - dstm

        while height != 0:
            srcco = srco
            dstco = dsto
            i = width
            while i != 0:
                v = 0
                if src1[srcco] & srcm:
                    v = 1
                if shd and (src2[srcco] & srcm):
                    v |= 2
                if (key == -1) or (v != key):
                    if v & 1:
                        buffer[dstco] |= dstm
                    else:
                        buffer[dstco] &= dstim
                    if v & 2:
                        shading[dstco] |= dstm
                    else:
                        shading[dstco] &= dstim
                srcco += sdx
                dstco += 1
                i -= 1
            dstm <<= 1
            if dstm & 0x100:
                dsto += _WIDTH
                dstm = 1
                dstim = 0xfe
            else:
                dstim = 255 - dstm
            if mirrorY:
                srcm >>= 1
                if srcm == 0:
                    srco -= stride
                    srcm = 0x80
            else:
                srcm <<= 1
                if srcm & 0x100:
                    srco += stride
                    srcm = 1
            height -= 1

    @micropython.native
    def drawSprite(self, s):
        self.blit(s.bitmap, s.x, s.y, s.width, s.height, s.key, s.mirrorX, s.mirrorY)

    @micropython.viper
    def blitScaled(self, src, x:int, y:int, width:int, height:int, key:int, mirrorX:int, mirrorY:int, scale:int, realWidth:int):
        if(x+width<0 or x>71):
            return
        if(y+height<0 or y>39):
            return
        buffer = ptr8(self.buffer)
        shading = ptr8(self.shading)
    
        if isinstance(src, (tuple, list)):
            shd = 1
            src1 = ptr8(src[0])
            src2 = ptr8(src[1])
        else:
            shd = 0
            src1 = ptr8(src)
            src2 = ptr8(0)
    
        xStart=int(x)
        yStart=int(y)
        
        yFirst=0-yStart
        blitHeight=height
        if yFirst<0:
            yFirst=0
        if yStart+height>40:
            blitHeight = 40-yStart
        y=yFirst
        
        xFirst=0-xStart
        blitWidth=width
        if xFirst<0:
            xFirst=0
        if xStart+width>72:
            blitWidth = 72-xStart
            
        while y < blitHeight:
            x=xFirst
            while x < blitWidth:
                sy = (((height-1-y if mirrorY==1 else y)*scale)>>8)
               
                i = (sy >> 3) * realWidth + (((width-1-x if mirrorX==1 else x)*scale)>>8)
                pixel_pos = ((yStart+y) >> 3) * int(72) + xStart+x
                bit_pos = 1 << ((yStart+y) & 0x07)
                
                # Determine the color (0-3) based on both buffers
                color = 0
                if src1[i] & (1 << (sy & 0x07)):
                    color |= 1
                if shd == 1 and (src2[i] & (1 << (sy & 0x07))):
                    color |= 2
                    
                if color != key:
                    if color & 1:
                        buffer[pixel_pos] |= bit_pos
                    else:
                        buffer[pixel_pos] &= 0xff ^ bit_pos
                        
                    if shd == 1:
                        if color & 2:
                            shading[pixel_pos] |= bit_pos
                        else:
                            shading[pixel_pos] &= 0xff ^ bit_pos
                x+=1
            y+=1
    
    @micropython.native
    def drawSpriteWithScale(self, s):
        self.blitScaled(s.bitmap, s.x, s.y, s.scaledWidth, s.scaledHeight, s.key, s.mirrorX, s.mirrorY, fpdiv(256<<16, s.scale)>>16, s.width)
        
display = Grayscale()
display.enableGrayscale()
