# Miminised Thumby grayscale library (version 4.0.2-hemlock)
# See: https://github.com/Timendus/thumby-grayscale

from utime import sleep_ms, ticks_diff, ticks_ms, sleep_us
from machine import Pin, SPI, idle, mem32
import _thread
from array import array

emulator = None
try:
    import emulator
except ImportError:
    pass

_THREAD_STOPPED    = const(0)
_THREAD_RUNNING    = const(1)
_ST_THREAD       = const(0)
_ST_COPY_BUFFS   = const(1)
_ST_CALIBRATOR   = const(2)
_ST_MODE         = const(3)
_WIDTH = const(72)
_HEIGHT = const(40)
_BUFF_SIZE = const((_HEIGHT // 8) * _WIDTH)
_BUFF_INT_SIZE = const(_BUFF_SIZE // 4)
# Timing parameters for each mode
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


class Grayscale:
    def __init__(self):
        self._spi = SPI(0, sck=Pin(18), mosi=Pin(19))
        self._dc = Pin(17)
        self._cs = Pin(16)
        self._res = Pin(20)
        self._spi.init(baudrate=100 * 1000 * 1000, polarity=0, phase=0)
        self._res.init(Pin.OUT, value=1)
        self._dc.init(Pin.OUT, value=0)
        self._cs.init(Pin.OUT, value=1)
        self.drawBuffer = bytearray(_BUFF_SIZE*2)
        self.buffer = memoryview(self.drawBuffer)[:_BUFF_SIZE]
        self.shading = memoryview(self.drawBuffer)[_BUFF_SIZE:]
        self._subframes = array('O', [bytearray(_BUFF_SIZE),
            bytearray(_BUFF_SIZE), bytearray(_BUFF_SIZE)])
        self.lastUpdateEnd = 0
        self._contrastSrc = bytearray(18)
        self._contrast = bytearray(3)
        self._state = array('I', [_THREAD_STOPPED,0,87,0])

    # GPU (Gray Processing Unit) thread function
    @micropython.viper
    def _display_thread(self):
        state = ptr32(self._state)
        contrastSrc = ptr8(self._contrastSrc)
        contrast = ptr8(self._contrast)
        bb = ptr32(self.buffer)
        bs = ptr32(self.shading)
        sf = self._subframes
        params = ptr8(_params)
        mode = state[_ST_MODE]
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
        while 1:
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
                sio[5] = 1 << 17
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
                    mode = state[_ST_MODE]
                    while i < _BUFF_INT_SIZE:
                        v1 = bb[i]
                        v2 = bs[i]
                        wd = v1 ^ v2
                        w = v1 & wd
                        di = ((i&3)+i)&1
                        di1 = (d1 if di else d2)
                        di2 =  (d2 if di else d1)
                        b1[i] = wd
                        b2[i] = v1
                        b3[i] = w
                        if mode == 0:
                            b1[i] = v1 | v2
                        elif mode == 2:
                            b1[i] = v1 | (v2 & di1)
                            b2[i] = v1 | (v2 & di2)
                        elif mode >= 4:
                            lg = v1 & v2
                            b2[i] = w | (lg & di1)
                            b3[i] = w | (lg & di2)
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
                sio[6] = 1 << 17
                while (tmr[10] - (time_pre + params[18+mfn]*calib)) < 0: pass
                fn += 1

    @micropython.native
    def update(self):
        state = self._state
        if emulator:
            mem32[0xD0000000+0x01C] = 1 << 2
        elif state[_ST_THREAD] == _THREAD_RUNNING:
            state[_ST_COPY_BUFFS] = 1
            while state[_ST_COPY_BUFFS] != 0:
                idle()
        else:
            self._dc(1)
            self._spi.write(self.buffer)

        frameTimeMs = 1000 // 60 # 60 FPS
        lastUpdateEnd = self.lastUpdateEnd
        frameTimeRemaining = frameTimeMs - ticks_diff(ticks_ms(), lastUpdateEnd)
        while frameTimeRemaining > 1:
            sleep_ms(1)
            frameTimeRemaining = frameTimeMs - ticks_diff(ticks_ms(), lastUpdateEnd)
        while frameTimeRemaining > 0:
            frameTimeRemaining = frameTimeMs - ticks_diff(ticks_ms(), lastUpdateEnd)
        self.lastUpdateEnd = ticks_ms()

display = Grayscale()
display_buffer = display.buffer
display_update = display.update

class _GrayscaleLauncher:
    def __init__(self):
        gs = display
        if (emulator):
            self._init_emu_screen(gs)
            emulator.screen_breakpoint(1)
            mem32[0xD0000000+0x01C] = 1 << 2
            return
        gs._res(1)
        sleep_us(10)
        gs._res(0)
        sleep_us(10)
        gs._res(1)
        sleep_us(20)
        gs._cs(0)
        gs._dc(0)
        gs._spi.write(bytearray([
            0xae, 0x20,0x00, 0x40, 0xa1, 0xa8,39, 0xc8, 0xd3,0, 0xda,0x12,
            0xd5,0xf0, 0xd9,0x11, 0xdb,0x20, 0xa4, 0xa6, 0x8d,0x14, 0xad,0x30, 0xaf]))
        gs._dc(1)
        zero32 = bytearray([0] * 32)
        for _ in range(32):
            gs._spi.write(zero32)
        gs._dc(0)
        gs._spi.write(bytearray([0x21,28,99, 0x22,0,4]))
        calibrate = False
        try:
            with open("thumbyGS.cfg", "r") as fh:
                vls = fh.read().split('\n')
                for fhd in vls:
                    if fhd.startswith('gsV3,'):
                        _, _, conf = fhd.partition("timing,")
                        gs._state[_ST_CALIBRATOR] = int(conf.split(',')[0])
                        _, _, conf = fhd.partition("oled,")
                        gs._state[_ST_MODE] = int(conf.split(',')[0])
                        break
                else:
                    raise ValueError()
        except (OSError, ValueError):
            from os import stat
            fontFile = "/lib/font5x7.bin"
            sz = stat(fontFile)[6]
            self.font_bmap = bytearray(sz)
            with open(fontFile, 'rb') as fh:
                fh.readinto(self.font_bmap)
            self.font_glyphcnt = sz // 5
            def info(*m):
                self.drawFilledRectangle(gs, 0, 0, 72, 40, 0)
                for i, l in enumerate(m):
                    self.drawText(gs, l, 0, i*8, 1)
                gs.update()
                unA = Pin(27, Pin.IN, Pin.PULL_UP).value
                while not unA(): idle()
                sleep_ms(200)
                while unA(): idle()
                sleep_ms(200)
                while not unA(): idle()
                sleep_ms(200)
            info("", "CALIBRATE", "", "GRAYSCALE...")
            info("Pick clearer", "  image with", "   <-  ->", "then press A", "         ...")
            calibrate = True
        contrastSrc = gs._contrastSrc
        c = 127
        try:
            with open("thumby.cfg", "r") as fh:
                _, _, conf = fh.read().partition("brightness,")
                b = int(conf.split(',')[0])
                if b == 0: c = 1
                if b == 1: c = 28
        except (OSError, ValueError):
            pass
        from math import sqrt, floor
        if c < 1: c = 1
        if c > 127: c = 127
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
        _thread.stack_size(2048)
        self._init_grayscale(gs)
        _thread.start_new_thread(gs._display_thread, ())
        while gs._state[_ST_THREAD] != _THREAD_RUNNING:
            idle()
        if calibrate:
            self.calibrate(gs)

    def calibrate(self, gs):
        rec = self.drawFilledRectangle
        tex = self.drawText
        presets = [(87,0),(107,1),(80,0),(95,0),(100,1),(115,1),
            (107,4),(87,2),(87,3),(87,5),(111,0),(111,2)]
        unL = Pin(3, Pin.IN, Pin.PULL_UP).value
        unR = Pin(5, Pin.IN, Pin.PULL_UP).value
        unA = Pin(27, Pin.IN, Pin.PULL_UP).value
        state = gs._state
        def sample(title, param, offset):
            rec(gs, 0, 0, 72, 40, 2)
            rec(gs, 2, 0, 68, 30, 3)
            rec(gs, 8, 0, 56, 20, 2)
            rec(gs, 16, 0, 40, 10, 0)
            tex(gs, title, 17, 1, 3)
            tex(gs, param, offset, 12, 1)
            tex(gs, "GRAYSCALE", 10, 22, 1)
            tex(gs, "CALIBRATION", 4, 32, 3)
            gs.update()
            if not unL():
                while not unL(): idle()
                sleep_ms(200)
                return -1
            if not unR():
                while not unL(): idle()
                sleep_ms(200)
                return 1
            return 0
        p = 0
        while not unA(): idle()
        sleep_ms(200)
        while unA():
            p = (p + sample("Preset:", chr(p+65), 34)) % len(presets)
            state[_ST_CALIBRATOR] = presets[p][0]
            state[_ST_MODE] = presets[p][1]
        sleep_ms(200)
        while not unA(): idle()
        sleep_ms(200)
        while unA():
            state[_ST_CALIBRATOR] = min(200, max(1, state[_ST_CALIBRATOR] +
                sample(" Tune:", str(state[_ST_CALIBRATOR]), 28)))
        rec(gs, 0, 0, 72, 40, 0)
        vls = []
        try:
            with open("thumbyGS.cfg", "r") as fh:
                vls = fh.read().split('\n')
        except OSError: pass
        nvl = f"gsV3,timing,{str(state[_ST_CALIBRATOR])},oled,{str(state[_ST_MODE])}"
        for i, vl in enumerate(vls):
            if vl.startswith('gsV3,'):
                vls[i] = nvl
                break
        else:
            vls.append(nvl)
        with open("thumbyGS.cfg", "w") as fh:
            fh.write('\n'.join(vls))

    @micropython.viper
    def _init_emu_screen(self, gs):
        Pin(2, Pin.OUT)
        emulator.screen_breakpoint(ptr16(gs.drawBuffer))

    @micropython.viper
    def _init_grayscale(self, gs):
        state = ptr32(gs._state)
        contrastSrc = ptr8(gs._contrastSrc)
        contrast = ptr8(gs._contrast)
        subs = gs._subframes
        bb = ptr32(gs.buffer)
        bs = ptr32(gs.shading)
        b1 = ptr32(subs[0])
        b2 = ptr32(subs[1])
        b3 = ptr32(subs[2])
        blitsub = ptr8(subs[0])
        d1 = int(0xAA55AA55)
        d2 = int(0x55AA55AA)
        sio = ptr32(0xd0000000)
        spi0 = ptr32(0x4003c000)
        tmr = ptr32(0x40054000)
        mode = state[_ST_MODE]
        i = 0
        while i < _BUFF_INT_SIZE:
            v1 = bb[i]
            v2 = bs[i]
            wd = v1 ^ v2
            w = v1 & wd
            di = ((i&3)+i)&1
            di1 = (d1 if di else d2)
            di2 =  (d2 if di else d1)
            b1[i] = wd
            b2[i] = v1
            b3[i] = w
            if mode == 0:
                b1[i] = v1 | v2
            elif mode == 2:
                b1[i] = v1 | (v2 & di1)
                b2[i] = v1 | (v2 & di2)
            elif mode >= 4:
                lg = v1 & v2
                b2[i] = w | (lg & di1)
                b3[i] = w | (lg & di2)
            i += 1
        while (spi0[3] & 4) == 4: i = spi0[2]
        while (spi0[3] & 0x10) == 0x10: pass
        while (spi0[3] & 4) == 4: i = spi0[2]
        sio[5] = 1 << 17 # dc(1)
        i = 0
        while i < 144:
            while (spi0[3] & 2) == 0: pass
            spi0[2] = blitsub[i]
            i += 1
        while (spi0[3] & 4) == 4: i = spi0[2]
        while (spi0[3] & 0x10) == 0x10: pass
        while (spi0[3] & 4) == 4: i = spi0[2]
        sio[6] = 1 << 17
        cmode = mode*3
        contrast[0] = contrastSrc[cmode]
        contrast[1] = contrastSrc[cmode + 1]
        contrast[2] = contrastSrc[cmode + 2]
        spi0[2] = 0x81; spi0[2] = contrast[0]
        spi0[2] = 0xae
        spi0[2] = 0xd3; spi0[2] = 47
        time_pre = tmr[10] + 4000
        while (tmr[10] - time_pre) < 0: pass
        spi0[2] = 0xa8; spi0[2] = 1
        spi0[2] = 0xa6
        spi0[2] = 0xaf

    @micropython.viper
    def drawFilledRectangle(self, gs, x:int, y:int, width:int, height:int, colour:int):
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
        buffer = ptr8(gs.buffer)
        shading = ptr8(gs.shading)
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
    def drawText(self, gs, stringToPrint, x:int, y:int, colour:int):
        buffer = ptr8(gs.buffer)
        shading = ptr8(gs.shading)
        font_bmap = ptr8(self.font_bmap)
        font_glyphcnt = int(self.font_glyphcnt)
        font_width = 5
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
            ou += 1
            ol += 1
            x += 1
_GrayscaleLauncher()
del _GrayscaleLauncher
