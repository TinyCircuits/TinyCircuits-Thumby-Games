# This is a driver for Thumby's SSD1306 display controller to create
# 4 shades (black, dark grey, light grey, white) by rapidly switching between
# multiple framebuffers, using a controller hack to avoid frame synchronisation
# issues without requiring the FR signal.
# This version has been tidied up and stripped of comments for the arcade.
# The original file on GitHub has extra methods that can be used for drawing
# lines, rectangles, text etc.
# Note that a version of this driver is available in github.com/Timendus/thumby-grayscale
# The version there has been modified to provide a similar interface to
# GraphicsClass in thumbyGraphics.py.

# Copyright 2022 David Steinberg <david@sonabuzz.com>


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import micropython
import utime
from machine import Pin, SPI, freq, idle
import _thread
import os
import gc
from array import array

if freq() < 125000000:
    freq(125000000)

def _check_upython_version(major, minor, release):
    up_ver = [int(s) for s in os.uname().release.split('.')]
    if up_ver[0] > major:
        return True
    if up_ver[0] == major:
        if up_ver[1] > minor:
            return True
        if up_ver[1] == minor:
            if up_ver[2] >= release:
                return True
    return False

SSD1306_SPI_Grey_pre_frame_time_us    = const( 785)     # 8 rows: ( 8*(1+1+50)) / 530e3 seconds
SSD1306_SPI_Grey_frame_time_us        = const(4709)     # 48 rows: (49*(1+1+50)) / 530e3 seconds

SSD1306_SPI_Grey_ThreadState_Starting   = const(0)
SSD1306_SPI_Grey_ThreadState_Stopped    = const(1)
SSD1306_SPI_Grey_ThreadState_Running    = const(2)
SSD1306_SPI_Grey_ThreadState_Stopping   = const(3)
SSD1306_SPI_Grey_ThreadState_Waiting    = const(4)

SSD1306_SPI_Grey_StateIndex_State       = const(0)
SSD1306_SPI_Grey_StateIndex_CopyBuffs   = const(1)
SSD1306_SPI_Grey_StateIndex_PendingCmd  = const(2)
SSD1306_SPI_Grey_StateIndex_ContrastChng= const(3)


class SSD1306_SPI_Grey:

    def __init__(self, delay_start):

        if not _check_upython_version(1, 19, 1):
            raise NotImplementedError('Greyscale support requires at least Micropython v1.19.1. Please update via the Thumby code editor')

        self.spi = SPI(0, sck=Pin(18), mosi=Pin(19))
        self.dc = Pin(17)
        self.cs = Pin(16)
        self.res = Pin(20)

        self.spi.init(baudrate=100 * 1000 * 1000, polarity=0, phase=0)
        self.res.init(Pin.OUT, value=1)
        self.dc.init(Pin.OUT, value=0)
        self.cs.init(Pin.OUT, value=1)

        self.width = 72
        self.height = 40
        self.max_x = 72 - 1
        self.max_y = 40 - 1
        self.pages = self.height // 8
        self.buffer_size = self.pages * self.width
        self.buffer1 = bytearray(self.buffer_size)
        self.buffer2 = bytearray(self.buffer_size)
        self._buffer1 = bytearray(self.buffer_size)
        self._buffer2 = bytearray(self.buffer_size)
        self._buffer3 = bytearray(self.buffer_size)

        self.pre_frame_cmds = bytearray([0xa8,0, 0xd3,52])
        self.post_frame_cmds = bytearray([0xd3,40+(64-57), 0xa8,57-1])

        self.post_frame_adj = [bytearray([0x81,0x3]), bytearray([0x81,0x7f]), bytearray([0x81,0xff])]

        self._state = array('I', [0,0,0,0xff])

        self.pending_cmds = bytearray([0] * 8)

        self.fill(0)
        self.copy_buffers()

        self.delay_start = delay_start
        if delay_start:
            self._state[SSD1306_SPI_Grey_StateIndex_State] = SSD1306_SPI_Grey_ThreadState_Waiting
        else:
            self.init_display()
            gc.collect()
            self._state[SSD1306_SPI_Grey_StateIndex_State] = SSD1306_SPI_Grey_ThreadState_Starting
        _thread.stack_size(1024)
        _thread.start_new_thread(self._display_thread, ())
        if not delay_start:
            while self._state[SSD1306_SPI_Grey_StateIndex_State] != SSD1306_SPI_Grey_ThreadState_Running:
                idle()


    # allow use of 'with'
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        self.teardown()


    def start(self):
        if not self.delay_start:
            return
        self.init_display()
        gc.collect()
        self._state[SSD1306_SPI_Grey_StateIndex_State] = SSD1306_SPI_Grey_ThreadState_Starting


    def reset(self):
        self.res(1)
        utime.sleep_ms(1)
        self.res(0)
        utime.sleep_ms(10)
        self.res(1)
        utime.sleep_ms(10)


    def init_display(self):
        self.cs(1)
        self.reset()
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([
            0xae, 0x20,0x00, 0x40, 0xa1, 0xa8,63, 0xc8, 0xd3,0, 0xda,0x12, 0xd5,0xf0, 0xd9,0x11, 0xdb,0x20, 0x81,0x7f,
            0xa4, 0xa6, 0x8d,0x14, 0xad,0x30, 0xaf]))
        self.dc(1)
        zero32 = bytearray([0] * 32)
        for _ in range(32):
            self.spi.write(zero32)
        self.dc(0)
        self.spi.write(bytearray([0x21,28,99, 0x22,0,4]))


    def teardown(self):
        if self._state[SSD1306_SPI_Grey_StateIndex_State] == SSD1306_SPI_Grey_ThreadState_Waiting:
            return
        if self._state[SSD1306_SPI_Grey_StateIndex_State] == SSD1306_SPI_Grey_ThreadState_Running:
            self._state[SSD1306_SPI_Grey_StateIndex_State] = SSD1306_SPI_Grey_ThreadState_Stopping
            while self._state[SSD1306_SPI_Grey_StateIndex_State] != SSD1306_SPI_Grey_ThreadState_Stopped:
                idle()
        self.cs(1)
        self.reset()
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([
            0xae, 0x20,0x00, 0x40, 0xa1, 0xa8,self.height-1, 0xc8, 0xd3,0, 0xda,0x12, 0xd5,0x80,
            0xd9,0xf1, 0xdb,0x20, 0x81,0x7f,
            0xa4, 0xa6, 0x8d,0x14, 0xad,0x30, 0xaf,
            0x21,28,99, 0x22,0,4]))
        self.cs(1)

    @micropython.viper
    def show(self):
        state:ptr32 = ptr32(self._state)
        state[SSD1306_SPI_Grey_StateIndex_CopyBuffs] = 1
        if state[SSD1306_SPI_Grey_StateIndex_State] != SSD1306_SPI_Grey_ThreadState_Running:
            return
        while state[SSD1306_SPI_Grey_StateIndex_CopyBuffs] != 0:
            idle()

    def show_async(self):
        self._state[SSD1306_SPI_Grey_StateIndex_CopyBuffs] = 1


    def contrast(self, c):
        if c < 0:
            c = 0
        elif c > 255:
            c = 255
        self._state[SSD1306_SPI_Grey_StateIndex_ContrastChng] = c

    def contrast_sync(self, c):
        if c < 0:
            c = 0
        elif c > 255:
            c = 255
        self._state[SSD1306_SPI_Grey_StateIndex_ContrastChng] = c
        if self._state[SSD1306_SPI_Grey_StateIndex_State] != SSD1306_SPI_Grey_ThreadState_Running:
            return
        while self._state[SSD1306_SPI_Grey_StateIndex_ContrastChng] != 0xffff:
            idle()


    @micropython.viper
    def copy_buffers(self):
        b1:ptr32 = ptr32(self.buffer1) ; b2:ptr32 = ptr32(self.buffer2)
        _b1:ptr32 = ptr32(self._buffer1) ; _b2:ptr32 = ptr32(self._buffer2) ; _b3:ptr32 = ptr32(self._buffer3)
        i:int = 0
        while i < 90:
            v1:int = b1[i]
            v2:int = b2[i]
            _b1[i] = v1 | v2
            _b2[i] = v2
            _b3[i] = v1 & v2
            i += 1
        self._state[SSD1306_SPI_Grey_StateIndex_CopyBuffs] = 0


    @micropython.viper
    def _display_thread(self):
        buffers:ptr32 = ptr32(array('L', [ptr8(self._buffer1), ptr8(self._buffer2), ptr8(self._buffer3)]))
        post_frame_adj:ptr32 = ptr32(array('L', [ptr8(self.post_frame_adj[0]), ptr8(self.post_frame_adj[1]), ptr8(self.post_frame_adj[2])]))
        state:ptr32 = ptr32(self._state)
        pre_frame_cmds:ptr8 = ptr8(self.pre_frame_cmds)
        post_frame_cmds:ptr8 = ptr8(self.post_frame_cmds)

        spi0:ptr32 = ptr32(0x4003c000)
        tmr:ptr32 = ptr32(0x40054000)
        sio:ptr32 = ptr32(0xd0000000)

        b1:ptr32 = ptr32(self.buffer1) ; b2:ptr32 = ptr32(self.buffer2)
        _b1:ptr32 = ptr32(self._buffer1) ; _b2:ptr32 = ptr32(self._buffer2) ; _b3:ptr32 = ptr32(self._buffer3)
        pending_cmds:ptr8 = ptr8(self.pending_cmds)

        fn:int ; i:int ; t0:int
        v1:int ; v2:int ; contrast:int
        spibuff:ptr8

        while state[SSD1306_SPI_Grey_StateIndex_State] == SSD1306_SPI_Grey_ThreadState_Waiting:
            pass

        state[SSD1306_SPI_Grey_StateIndex_State] = SSD1306_SPI_Grey_ThreadState_Running
        while state[SSD1306_SPI_Grey_StateIndex_State] == SSD1306_SPI_Grey_ThreadState_Running:
            fn = 0
            while fn < 3:
                time_out = tmr[10] + SSD1306_SPI_Grey_pre_frame_time_us
                sio[6] = 1 << 17 # dc(0)
                i = 0
                while i < 4:
                    while (spi0[3] & 2) == 0: pass
                    spi0[2] = pre_frame_cmds[i]
                    i += 1
                while (spi0[3] & 4) == 4: i = spi0[2]
                while (spi0[3] & 0x10) == 0x10: pass
                while (spi0[3] & 4) == 4: i = spi0[2]

                sio[5] = 1 << 17 # dc(1)
                i = 0
                spibuff:ptr8 = ptr8(buffers[fn])
                while i < 360:
                    while (spi0[3] & 2) == 0: pass
                    spi0[2] = spibuff[i]
                    i += 1
                while (spi0[3] & 4) == 4: i = spi0[2]
                while (spi0[3] & 0x10) == 0x10: pass
                while (spi0[3] & 4) == 4: i = spi0[2]

                sio[6] = 1 << 17 # dc(0)
                i = 0
                spibuff:ptr8 = ptr8(post_frame_adj[fn])
                while i < 2:
                    while (spi0[3] & 2) == 0: pass
                    spi0[2] = spibuff[i]
                    i += 1
                while (spi0[3] & 4) == 4: i = spi0[2]
                while (spi0[3] & 0x10) == 0x10: pass
                while (spi0[3] & 4) == 4: i = spi0[2]

                while (tmr[10] - time_out) < 0:
                    pass

                time_out = tmr[10] + SSD1306_SPI_Grey_frame_time_us
                i = 0
                while i < 4:
                    while (spi0[3] & 2) == 0: pass
                    spi0[2] = post_frame_cmds[i]
                    i += 1
                i = 0
                spibuff:ptr8 = ptr8(post_frame_adj[fn])
                while i < 2:
                    while (spi0[3] & 2) == 0: pass
                    spi0[2] = spibuff[i]
                    i += 1
                while (spi0[3] & 4) == 4: i = spi0[2]
                while (spi0[3] & 0x10) == 0x10: pass
                while (spi0[3] & 4) == 4: i = spi0[2]

                if (fn == 2) and (state[SSD1306_SPI_Grey_StateIndex_CopyBuffs] != 0):
                    i = 0
                    while i < 90:
                        v1 = b1[i]
                        v2 = b2[i]
                        _b1[i] = v1 | v2
                        _b2[i] = v2
                        _b3[i] = v1 & v2
                        i += 1
                    state[SSD1306_SPI_Grey_StateIndex_CopyBuffs] = 0
                elif (fn == 2) and (state[SSD1306_SPI_Grey_StateIndex_ContrastChng] != 0xff):
                    contrast = state[SSD1306_SPI_Grey_StateIndex_ContrastChng]
                    state[SSD1306_SPI_Grey_StateIndex_ContrastChng] = 0xff
                    ptr8(post_frame_adj[0])[1] = contrast >> 6
                    ptr8(post_frame_adj[1])[1] = contrast >> 1
                    ptr8(post_frame_adj[2])[1] = contrast
                elif state[SSD1306_SPI_Grey_StateIndex_PendingCmd]:
                    i = 0
                    while i < 8:
                        while (spi0[3] & 2) == 0: pass
                        spi0[2] = pending_cmds[i]
                        i += 1
                    while (spi0[3] & 4) == 4: i = spi0[2]
                    while (spi0[3] & 0x10) == 0x10: pass
                    while (spi0[3] & 4) == 4: i = spi0[2]
                    state[SSD1306_SPI_Grey_StateIndex_PendingCmd] = 0

                while (tmr[10] - time_out) < 0:
                    pass

                fn += 1
        self._thread_stopping()
        return

    @micropython.viper
    def _thread_stopping(self):
        _b1:ptr32 = ptr32(self._buffer1)
        i = 0
        while i < 90:
            _b1[i] = 0
            i += 1
        self.dc(1)
        self.spi.write(self._buffer1)
        self._state[SSD1306_SPI_Grey_StateIndex_State] = SSD1306_SPI_Grey_ThreadState_Stopped


    @micropython.viper
    def fill(self, s:int):
        buffer1:ptr32 = ptr32(self.buffer1)
        buffer2:ptr32 = ptr32(self.buffer2)
        f1:int = -1 if s & 1 else 0
        f2:int = -1 if s & 2 else 0
        i:int = 0
        while i < 90:
            buffer1[i] = f1
            buffer2[i] = f2
            i += 1


    @micropython.viper
    def pixel(self, x:int, y:int, s:int):
        if x < 0 or x >= 72 or y < 0 or y >= 40:
            return
        o:int = (y >> 3) * 72 + x
        m:int = 1 << (y & 7)
        im:int = 255-m
        buffer1 = ptr8(self.buffer1)
        buffer2 = ptr8(self.buffer2)
        if s & 1:
            buffer1[o] |= m
        else:
            buffer1[o] &= im
        if s & 2:
            buffer2[o] |= m
        else:
            buffer2[o] &= im

