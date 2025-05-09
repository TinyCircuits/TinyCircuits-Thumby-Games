# This is the Mountains class, split from the main file to avoid out-of-
# memory errors when compiling native/viper functions.

# Note that this version is tidied up and stripped of comments for the arcade,
# and does not have the two other rendering variations that the version on GitHub has.

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


import random
from array import array


@micropython.viper
def draw_mountain_range(disp, x0:int, mountbuff1:ptr32, mountbuff2:ptr32, mountmask:ptr32):
    buffer1:ptr8 = ptr8(disp.buffer1)
    buffer2:ptr8 = ptr8(disp.buffer2)
    x:int = 72
    x0 &= 0xff
    while x < 84:
        v1:int = mountbuff1[x0]
        v2:int = mountbuff2[x0]
        m:int = mountmask[x0]
        buffer1[ 72 + x] = (buffer1[ 72 + x] & (m >>  5)) | (v1 >>  5)
        buffer1[144 + x] = (buffer1[144 + x] & (m >> 12)) | (v1 >> 12)
        buffer2[ 72 + x] = (buffer2[ 72 + x] & (m >>  5)) | (v2 >>  5)
        buffer2[144 + x] = (buffer2[144 + x] & (m >> 12)) | (v2 >> 12)
        x += 1
        x0 = (x0 + 1) & 0xff
    while x < 133:
        v1:int = mountbuff1[x0]
        v2:int = mountbuff2[x0]
        m:int = mountmask[x0]
        buffer1[      x] = (buffer1[      x] & ((m << 6) | 0x3f)) | (v1 <<  6)
        buffer1[ 72 + x] = (buffer1[ 72 + x] & (m >>  6)) | (v1 >>  6)
        buffer1[144 + x] = (buffer1[144 + x] & (m >> 13)) | (v1 >> 13)
        buffer2[      x] = (buffer2[      x] & ((m << 6) | 0x3f)) | (v2 <<  6)
        buffer2[ 72 + x] = (buffer2[ 72 + x] & (m >>  6)) | (v2 >>  6)
        buffer2[144 + x] = (buffer2[144 + x] & (m >> 13)) | (v2 >> 13)
        x += 1
        x0 = (x0 + 1) & 0xff
    while x < 144:
        v1:int = mountbuff1[x0]
        v2:int = mountbuff2[x0]
        m:int = mountmask[x0]
        buffer1[ 72 + x] = (buffer1[ 72 + x] & (m >>  5)) | (v1 >>  5)
        buffer1[144 + x] = (buffer1[144 + x] & (m >> 12)) | (v1 >> 12)
        buffer2[ 72 + x] = (buffer2[ 72 + x] & (m >>  5)) | (v2 >>  5)
        buffer2[144 + x] = (buffer2[144 + x] & (m >> 12)) | (v2 >> 12)
        x += 1
        x0 = (x0 + 1) & 0xff


class Mountains:

    def __init__(self, dither1, dither2, dith_w_mask, dith_h_mask):
        self.dith_w_mask = dith_w_mask
        self.dith_h_mask = dith_h_mask

        self.mountbuff1 = array('L', [1 << 16, 0, 0, 0] * 64)
        self.mountbuff2 = array('L', [0 << 16, 0, 0, 0] * 64)
        self.mountmask = array('L', [~(1 << 16), ~0, ~0, ~0] * 64)

        for i in range(40):
            sx = random.randrange(256)
            wl = random.randrange(4, 12)
            wr = wl + random.randrange(-3, 4)
            h = random.randrange(wl - 4, wl + 2)
            if h <  4: h = 4
            if h > 10: h = 10

            sr = random.randrange(7, 10)
            sl = random.randrange(4, 7)

            dithr1 = dither1[sr]
            dithr2 = dither2[sr]
            dithl1 = dither1[sl]
            dithl2 = dither2[sl]

            dy = 16 - h

            if wl >= h:
                scl = h / wl
                for x in range(wl):
                    y = 16 - int(x * scl + 0.5)
                    self._fill_col(sx, x, y, dy, dithl1, dithl2, 0)
            else:
                scl = wl / h
                lx = 0
                my = 16
                for _y in range(h):
                    x = int(_y * scl + 0.5)
                    y = 16 - _y
                    if x != lx:
                        self._fill_col(sx, lx, my, dy, dithl1, dithl2, 0)
                        my = 16
                    lx = x
                    if y < my:
                        my = y
                self._fill_col(sx, lx, my, dy, dithl1, dithl2, 0)

            wlp = wl // 4
            if wlp < 2: wlp = 2
            psx = sx + (wl - wlp)
            if wlp >= h:
                scl = h / wlp
                for x in range(wlp):
                    y = 16 - int(x * scl + 0.5)
                    self._fill_col(psx, x, y, dy, dithr1, dithr2, 2)
            else:
                scl = wlp / h
                lx = 0
                my = 16
                for _y in range(h):
                    x = int(_y * scl + 0.5)
                    y = 16 - _y
                    if x != lx:
                        self._fill_col(psx, lx, my, dy, dithr1, dithr2, 2)
                        my = 16
                    lx = x
                    if y < my:
                        my = y
                self._fill_col(psx, lx, my, dy, dithr1, dithr2, 2)

            if wr >= h:
                scl = h / wr
                for x in range(wr):
                    y = dy + int(x * scl + 0.5)
                    self._fill_col(sx, wl + x, y, dy, dithr1, dithr2, 1)
            else:
                scl = wr / h
                lx = wl
                my = 16
                for _y in range(h):
                    x = wl + int(_y * scl + 0.5)
                    y = dy + _y
                    if x != lx:
                        self._fill_col(sx, lx, my, dy, dithr1, dithr2, 1)
                        my = 16
                    lx = x
                    if y < my:
                        my = y
                self._fill_col(sx, lx, my, dy, dithr1, dithr2, 1)


    def _fill_col(self, sx, x, y, dy, dith1, dith2, s):
        mx = (sx + x) & 0xff
        dmx = 1 << (x & self.dith_w_mask)
        m = 1 << y
        om = m
        for py in range(y, 17):
            dx = (py - dy) & self.dith_h_mask
            if dith1[dx] & dmx:
                self.mountbuff1[mx] |= m
            else:
                self.mountbuff1[mx] &= ~m
            if dith2[dx] & dmx:
                self.mountbuff2[mx] |= m
            else:
                self.mountbuff2[mx] &= ~m
            self.mountmask[mx] &= ~m
            m <<= 1
        if s == 1:
            if True:
                self.mountbuff1[mx] &= ~om
                self.mountbuff2[mx] |= om
            else:
                self.mountbuff1[mx] |= om
                self.mountbuff2[mx] &= ~om
            self.mountmask[mx] &= ~om
        elif s == 0 and x & 1:
            self.mountbuff1[mx] |= om
            self.mountbuff2[mx] &= ~om
            self.mountmask[mx] &= ~om


    def draw(self, disp, x0:int):
        draw_mountain_range(disp, x0, self.mountbuff1, self.mountbuff2, self.mountmask)
