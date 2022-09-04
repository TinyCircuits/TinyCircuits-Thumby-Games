# A small 3D demo, using a display controller hack for
# flicker-free 4 shade greyscale (16 shades with dithering).
# Features spinning and/or bouncing objects, an Outrun-style road, stars,
# mountains that might be pyramids, and randomly generated music.

# The full source code is over 100KiB, so this version has been tidied up and
# stripped of comments for the arcade... full source can be found at github.com/doogle/Journey3Dg

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


from micropython import kbd_intr, mem_info
import utime
from machine import Pin, freq
import random
import gc
from math import sin, pi, sqrt
from array import array
from sys import path

path.append("/Games/Journey3Dg")

from ssd1306grey import SSD1306_SPI_Grey

gc.collect()
kbd_intr(-1)
freq(280000000)

from musicplayer import MusicPlayer

swL = Pin(3, Pin.IN, Pin.PULL_UP)
swR = Pin(5, Pin.IN, Pin.PULL_UP)
swU = Pin(4, Pin.IN, Pin.PULL_UP)
swD = Pin(6, Pin.IN, Pin.PULL_UP)
swA = Pin(27, Pin.IN, Pin.PULL_UP)
swB = Pin(24, Pin.IN, Pin.PULL_UP)

disp = SSD1306_SPI_Grey(True)

frame_rate = const(50)
frame_microsec = int(1000000.0 / frame_rate)

fpone = const(1 << 16)

@micropython.viper
def int2fp(v:int) -> int:
    return v << 16

@micropython.viper
def fp2int(v:int) -> int:
    return v >> 16

@micropython.native
def fp2float(v:int) -> float:
    return v / 65536

@micropython.native
def float2fp(v:float) -> int:
    return int(v * 65536)

@micropython.viper
def fpmul(a:int, b:int) -> int:
    return (a >> 6) * (b >> 6) >> 4

@micropython.viper
def fpmul_rot(a:int, b:int) -> int:
    return ((a >> 2) * (b >> 2)) >> 12

@micropython.viper
def fpdiv(a:int, b:int) -> int:
    return ((a << 6) // (b >> 6)) >> 4


sintab_sz = const(1024)
sintab_mask = const(sintab_sz - 1)
sintab_quart_mask = const(sintab_mask >> 2)
sintab_half_mask = const(sintab_mask >> 1)
sintab_sz_quart = const(sintab_sz >> 2)
sintab_sz_half = const(sintab_sz >> 1)
sintab:array = array('l', [ int(sin(i * ((2 * pi) / sintab_sz)) * 65536) for i in range(sintab_sz // 4)])


shadecnt = const(16) ; dith_r_spread = -shadecnt/4
dith_xs = const(2) ; dith_ys = const(2)
dith_w = const(1 << dith_xs) ; dith_h = const(1 << dith_ys)
dith_w_mask = const(dith_w - 1) ; dith_h_mask = const(dith_h - 1)
dither1 = list() ; dither2 = list()
def split(l, n):
    for i in range(0,len(l),n):
        yield l[i:i+n]
def gen_bayer(x,y):
    if dith_xs > dith_ys:
        ys = '{:0{width}b}'.format(y, width=dith_ys)
        xs = '{:0{width}b}'.format(x ^ (y << (dith_xs-dith_ys)), width=dith_xs)
        return int(''.join(reversed(''.join([i+j for i,j in zip(ys,split(xs,dith_xs // dith_ys))]))), 2)
    else:
        xs = '{:0{width}b}'.format(x, width=dith_xs)
        ys = '{:0{width}b}'.format(y ^ (x << (dith_ys-dith_xs)), width=dith_ys)
        return int(''.join(reversed(''.join([i+j for i,j in zip(xs,split(ys,dith_ys // dith_xs))]))), 2)
bayer_mat = [ [ (gen_bayer(x,y)+1)/(dith_w*dith_h) - 0.5 for x in range(dith_w) ] for y in range(dith_h) ]
def fill_smallint(v):
    for i in range((30 // dith_w) - 1):
        v |= v << dith_w
    return v
for i in range(shadecnt):
    d = [ [ max(min(round((i + dith_r_spread * v) * (3/shadecnt)), 3), 0) for v in r] for r in bayer_mat ]
    dither1.append(array('l', [ fill_smallint(sum((1 if v & 1 else 0)<<i for i,v in enumerate(r))) for r in d ]))
    dither2.append(array('l', [ fill_smallint(sum((1 if v & 2 else 0)<<i for i,v in enumerate(r))) for r in d ]))
d = None
bayer_mat = None


project_d = const(100)
project_z = const(100)

project_z_fp = const(project_z << 16)


light_pos:array = array('l', [int2fp(40), int2fp(80), int2fp(80)])
light_ambient = const(3)


@micropython.viper
def fpsin(a:int) -> int:
    a &= sintab_mask
    ta:int = a & sintab_quart_mask
    if (a & sintab_half_mask) >= sintab_sz_quart:
        ta = sintab_quart_mask - ta
    v:int = ptr32(sintab)[ta]
    if a >= sintab_sz_half:
        return 0 - v
    return v

@micropython.viper
def fpcos(a:int) -> int:
    return int(fpsin(a + sintab_sz_quart))


log_table = array('l', [0] * 256)
for i in range(2, 256):
    log_table[i] = 1 + log_table[i // 2]
log_table[0] = -1

@micropython.viper
def bit_length(v:int) -> int:
    tt:int = v >> 16
    if tt != 0:
        t:int = tt >> 8
        if int(t) != 0:
            return 25 + int(log_table[t])
        return 17 + int(log_table[tt])
    else:
        t:int = v >> 8
        if int(t) != 0:
            return 9 + int(log_table[t])
        return 1 + int(log_table[v])


@micropython.viper
def isqrt(n:int) -> int:
    if n > 0:
        x:int = 1 << (int(bit_length(n)) + 1 >> 1)
        while True:
            y:int = (x + n // x) >> 1
            if y >= x:
                return x
            x = y
    elif n == 0:
        return 0


@micropython.viper
def project_part(c:int, z:int) -> int:
    a:int = fpdiv(c, z)
    b:int = int(a) * project_d
    g:int = int(b) >> 8
    return g


@micropython.viper
def project_x(x:int, z:int) -> int:
    z -= project_z_fp
    x = 36 - int(project_part(x, z))
    return x
@micropython.viper
def project_y(y:int, z:int) -> int:
    z -= project_z_fp
    y = 20 + int(project_part(y, z))
    return y


def project_inverse_y(y, y3):
	b = y3 * project_d
	c = b / (y + 0.5)
	return c + project_z


@micropython.viper
def calc_norm_k(x0:int, y0:int, z0:int, x1:int, y1:int, z1:int) -> int:
    xm:int = fpmul(x0, x0 - x1)
    ym:int = fpmul(y0, y0 - y1)
    zm:int = fpmul(z0, z0 - z1)
    s:int = xm + ym + zm
    d:int = int(s) // project_z
    return d


@micropython.viper
def hline_dither(x0:int, x1:int, y:int, dither_row1:int, dither_row2:int, dith_x_off:int):
    if x0 < 0:
        x0 = 0
    elif x0 > 71:
        x0 = 71
    if x1 < 0:
        x1 = 0
    elif x1 > 71:
        x1 = 71

    index:int = (y >> 3) * 72
    offset:int = y & 0x07
    mask:int = 1 << offset
    imask:int = 255-mask

    dither_row1 >>= (dith_x_off + x0) & dith_w_mask
    dither_row2 >>= (dith_x_off + x0) & dith_w_mask

    buffer1 = ptr8(disp.buffer1)
    buffer2 = ptr8(disp.buffer2)

    for ww in range(index+x0, index+x1):
        if dither_row1 & 1:
            buffer1[ww] |= mask
        else:
            buffer1[ww] &= imask
        dither_row1 >>= 1
        if dither_row2 & 1:
            buffer2[ww] |= mask
        else:
            buffer2[ww] &= imask
        dither_row2 >>= 1


@micropython.viper
def rastline(x0:int, y0:int, x1:int, y1:int, rastmin:ptr8, rastmax:ptr8):
    dx:int = x1 - x0
    dy:int = y1 - y0
    if dx < 0:
        dx = 0 - dx
    if dy < 0:
        dy = 0 - dy
    x:int = x0
    y:int = y0
    sx:int = -1 if x0 > x1 else 1
    sy:int = -1 if y0 > y1 else 1
    if dx > dy:
        err:int = dx >> 1
        while x != x1:
            if 0 <= y < 40:
                if x < rastmin[y]: rastmin[y] = x
                if x > rastmax[y]: rastmax[y] = x
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err:int = dy >> 1
        while y != y1:
            if 0 <= y < 40:
                if x < rastmin[y]: rastmin[y] = x
                if x > rastmax[y]: rastmax[y] = x
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    if 0 <= y < 40:
        if x < rastmin[y]: rastmin[y] = x
        if x > rastmax[y]: rastmax[y] = x



class Road:
    curve_len_opts = array('l', [2, 4, 7, 10])
    curve_dx_opts = array('l', [float2fp(-0.25), float2fp(-0.1666), float2fp(-0.125), float2fp(0.125), float2fp(0.1666), float2fp(0.25)])

    StateEaseIn = const(0)
    StateStraight = const(1)
    StateEaseOut = const(2)

    def __init__(self, road_width, road_horizon, road_y, c1min, c1max, c2min, c2max):
        self.zoff = 0
        maxx = float2fp(road_width/2)
        self.zmap = array('l', [0] * 19)
        for y in range(19):
            self.zmap[y] = int(project_inverse_y(y + 1, road_y) * 65536)

        self.farx = -project_part(maxx, self.zmap[0] - project_z_fp)
        self.nearx = -project_part(maxx, self.zmap[-1] - project_z_fp)
        rastmin = array('B', [0xff] * 19)
        rastmax = array('B', [0] * 19)
        rastline(self.farx, 0, self.nearx, 18, rastmin, rastmax)
        self.edgerast = rastmax

        self.road_horizon = road_horizon
        self.z_horizon = self.zmap[road_horizon]
        self.z_front = self.zmap[18]

        col_scale = 1 / (self.z_front - self.z_horizon)
        self.dithA1 = array('O', [None] * 19)
        self.dithB1 = array('O', [None] * 19)
        self.dithA2 = array('O', [None] * 19)
        self.dithB2 = array('O', [None] * 19)
        c1 = c1max - c1min ; c2 = c2max - c2min
        for y in range(19):
            z = (self.zmap[y] - self.z_horizon) * col_scale
            c1s = c1 * z if z >= 0 else 0
            c2s = c2 * z if z >= 0 else 0
            c1s = round(c1s + c1min + 0.5)
            c2s = round(c2s + c2min + 0.5)
            if c1s > 15: c1s = 15
            if c2s > 15: c2s = 15
            self.dithA1[y] = dither1[c1s]
            self.dithB1[y] = dither1[c2s]
            self.dithA2[y] = dither2[c1s]
            self.dithB2[y] = dither2[c2s]

        self.botseg_dx = 0
        self.seg_dx = 0
        self.seg_z = self.z_horizon

        self.curve_state = Road.StateEaseIn
        self.curve_dx = random.choice(Road.curve_dx_opts)
        self.curve_len = random.choice(Road.curve_len_opts)
        self.curve_inc = fpone // self.curve_len
        self.curve_n = 0


    @micropython.viper
    def draw(self) -> int:
        zmap:ptr32 = ptr32(self.zmap)
        edgerast:ptr8 = ptr8(self.edgerast)
        zoff:list = int(self.zoff)
        dithA1 = self.dithA1
        dithB1 = self.dithB1
        dithA2 = self.dithA2
        dithB2 = self.dithB2
        ddx:int = 0
        seg_z:int = int(self.seg_z)
        seg_dx:int = int(self.seg_dx)
        cxfp:int = (36 << 16) + (seg_dx << 3)
        botseg_dx:int = int(self.botseg_dx)
        for y in range(18,int(self.road_horizon),-1):
            z:int = int(zmap[y])
            zw:int = z - zoff

            if z > seg_z:
                ddx += botseg_dx
            else:
                ddx += seg_dx
            cxfp += ddx

            yy:int = y + 21
            x:int = int(edgerast[y])
            xh:int = x >> 1
            cx = cxfp >> 16

            c:int = (zw >> (5+16)) & 1
            dith_y:int = (y-(zoff>>18)) & dith_h_mask
            if c:
                dA1:array = dithA1[y][dith_y]
                dB1:array = dithB1[y][dith_y]
                dA2:array = dithA2[y][dith_y]
                dB2:array = dithB2[y][dith_y]
            else:
                dA1:array = dithB1[y][dith_y]
                dB1:array = dithA1[y][dith_y]
                dA2:array = dithB2[y][dith_y]
                dB2:array = dithA2[y][dith_y]
            hline_dither(cx-x , cx-xh, yy, dA1, dA2, 0)
            hline_dither(cx-xh, cx   , yy, dB1, dB2, 0)
            hline_dither(cx   , cx+xh, yy, dA1, dA2, 0)
            hline_dither(cx+xh, cx+x , yy, dB1, dB2, 0)
        return cx

    @micropython.native
    def update(self, speed):
        seg_z = self.seg_z + speed
        if seg_z > int(self.z_front):
            self.botseg_dx = self.seg_dx
            self.seg_z = self.z_horizon

            self.curve_len -= 1
            if self.curve_state == Road.StateEaseIn:
                if self.curve_len == 0:
                    self.curve_len = random.choice(Road.curve_len_opts)
                    self.curve_state = Road.StateStraight
                    self.seg_dx = self.curve_dx
                else:
                    self.seg_dx = fpmul(self.curve_dx, fpmul(self.curve_n, self.curve_n))
                    self.curve_n += self.curve_inc
            elif self.curve_state == Road.StateStraight:
                if self.curve_len == 0:
                    self.curve_len = random.choice(Road.curve_len_opts)
                    self.curve_state = Road.StateEaseOut
                    self.curve_inc = fpone // self.curve_len
                    self.curve_n = 0
            else:
                if self.curve_len == 0:
                    self.curve_len = random.choice(Road.curve_len_opts)
                    self.curve_dx = random.choice(Road.curve_dx_opts)
                    self.curve_state = Road.StateEaseIn
                    self.curve_inc = fpone // self.curve_len
                    self.curve_n = 0
                    self.seg_dx = 0
                else:
                    self.seg_dx = self.curve_dx + fpmul(-self.curve_dx, (fpone - fpmul(fpone - self.curve_n, fpone - self.curve_n)))
                    self.curve_n += self.curve_inc
        else:
            self.seg_z = seg_z
        self.zoff = (int(self.zoff) + speed) & 0x0fffffff



class Stars:
    def __init__(self, cnt):
        stars = array('O', [None] * cnt)
        for i in range(cnt):
            stars[i] = array('l', [random.randrange(-200<<16, 200<<16),
                          random.randrange(10<<16, 100<<16),
                          random.randrange(-1000<<16, 100<<16),
                          random.randrange(1,4)])
        self.stars = stars

    @micropython.native
    def draw_update(self, xcentre, ycentre, xdelta, speed):
        xcentre -= 36
        ycentre -= 20
        for s in self.stars:
            x = project_x(s[0], s[2]) + xcentre
            y = project_y(s[1], s[2]) + ycentre
            disp.pixel(x, y, s[3])
            s[2] += speed

            if not (0 <= x < 72 and 0 <= y < 40):
                s[0] = random.randrange(-200<<16, 200<<16)
                s[1] = random.randrange(10<<16, 100<<16)
                s[2] = random.randrange(-1000<<16, -500<<16)
                s[3] = random.randrange(1,4)
            else:
                s[0] -= xdelta



class Shape:
    def __init__(self, vertices, faces, calc_normals=True):
        vertcnt = len(vertices)
        facecnt = len(faces)
        if calc_normals:
            self.vertices = array('O', vertices + ([None] * facecnt))
        else:
            self.vertices = array('O', vertices)
        self.faces = array('O', faces)
        self.rot_axis = array('l', [0, fpone, 0])
        self.rot_angle:int = 0
        self.pos = array('l', [0,0,0])
        self.pm = [array('l', [0,0,0]) for _ in range(vertcnt + (facecnt if calc_normals else 0))]
        self.p2 = [array('l', [0,0]) for _ in range(vertcnt)]
        self.facevis:List[bool] = [False] * facecnt
        self.rastmin = array('B', [0xff]*40)
        self.rastmax = array('B', [0]*40)

        if calc_normals:
            for i in range(facecnt):
                f = self.faces[i]
                n = self.calc_vertex_norm(f)
                p0i = f[0][0]
                p0 = self.vertices[p0i]
                pn = (int((p0[0]+n[0])*65536),
                      int((p0[1]+n[1])*65536),
                      int((p0[2]+n[2])*65536))
                self.vertices[i + vertcnt] = pn
                self.faces[i] = (f[0], f[1], (p0i, vertcnt + i))

        for i in range(vertcnt):
            x, y, z = self.vertices[i]
            x *= 65536 ; y *= 65536 ; z *= 65536
            self.vertices[i] = (int(x), int(y), int(z))


    def calc_vertex_norm(self, f):
        p0 = self.vertices[f[0][0]]
        p2 = self.vertices[f[0][1]]
        p1 = self.vertices[f[0][2]]
        v = (p1[0]-p0[0],p1[1]-p0[1],p1[2]-p0[2])
        w = (p2[0]-p0[0],p2[1]-p0[1],p2[2]-p0[2])
        nx = (v[1] * w[2]) - (v[2] * w[1])
        ny = (v[2] * w[0]) - (v[0] * w[2])
        nz = (v[0] * w[1]) - (v[1] * w[0])
        m = sqrt((nx*nx)+(ny*ny)+(nz*nz))
        if m == 0:
            m = 1
        nx /= m
        ny /= m
        nz /= m
        return (nx,ny,nz)


    def destructive_transform(self, pos, rot_axis, rot_angle):
        pos_save = self.pos
        rot_axis_save = self.rot_axis
        rot_angle_save = self.rot_angle

        self.pos = pos if not pos is None else [0,0,0]
        self.rot_axis = rot_axis if not rot_axis is None else [0, fpone, 0]
        self.rot_angle = rot_angle if not rot_angle is None else 0
        self.transform_vertices()
        self.vertices = [(x,y,z) for x,y,z in self.pm]

        self.pos = pos_save
        self.rot_axis = rot_axis_save
        self.rot_angle = rot_angle_save


    @micropython.viper
    def transform_vertices(self):
        px:int; py:int; pz:int
        px, py, pz = self.pos

        ra_d2:int = int(self.rot_angle) >> 1
        rax:int; ray:int; raz:int
        rax, ray, raz = self.rot_axis
        sin_ra_d2:int = fpsin(ra_d2)
        q0:int = fpcos(ra_d2)
        q1:int = fpmul_rot(rax, sin_ra_d2)
        q2:int = fpmul_rot(ray, sin_ra_d2)
        q3:int = fpmul_rot(raz, sin_ra_d2)

        q1_sq2:int = int(fpmul_rot(q1, q1)) << 1
        q2_sq2:int = int(fpmul_rot(q2, q2)) << 1
        q3_sq2:int = int(fpmul_rot(q3, q3)) << 1

        q0_q1_2:int = int(fpmul_rot(q0, q1)) << 1
        q0_q2_2:int = int(fpmul_rot(q0, q2)) << 1
        q0_q3_2:int = int(fpmul_rot(q0, q3)) << 1
        q1_q2_2:int = int(fpmul_rot(q1, q2)) << 1
        q1_q3_2:int = int(fpmul_rot(q1, q3)) << 1
        q2_q3_2:int = int(fpmul_rot(q2, q3)) << 1

        rxx:int = fpone - q2_sq2 - q3_sq2
        rxy:int = q1_q2_2 - q0_q3_2
        rxz:int = q1_q3_2 + q0_q2_2

        ryx:int = q1_q2_2 + q0_q3_2
        ryy:int = fpone - q1_sq2 - q3_sq2
        ryz:int = q2_q3_2 - q0_q1_2

        rzx:int = q1_q3_2 - q0_q2_2
        rzy:int = q2_q3_2 + q0_q1_2
        rzz:int = fpone - q1_sq2 - q2_sq2

        pm = self.pm

        x:int ; y:int ; z:int
        _x:int ; _y:int ; _z:int
        i:int = 0
        vertices = self.vertices
        vertlen:int = int(len(vertices))
        while i < vertlen:
            p3 = vertices[i]
            x,y,z = p3
            _x = fpmul(x, rxx) + fpmul(y, rxy) + fpmul(z, rxz) + px
            _y = fpmul(x, ryx) + fpmul(y, ryy) + fpmul(z, ryz) + py
            _z = fpmul(x, rzx) + fpmul(y, rzy) + fpmul(z, rzz) - pz
            pm[i][0] = _x ; pm[i][1] = _y ; pm[i][2] = _z
            i += 1


    @micropython.native
    def rastface(self, f):
        rastmin = self.rastmin
        rastmax = self.rastmax
        i = 0
        while i < 40:
            rastmin[i] = 0xff
            rastmax[i] = 0
            i += 1
        vertices = f[0]
        p2 = self.p2
        sp = p2[vertices[-1]]
        for v in vertices:
            ep = p2[v]
            rastline(sp[0], sp[1], ep[0], ep[1], rastmin, rastmax)
            sp = ep

    @micropython.viper
    def drawrast(self, s:int):
        dith_mat1:ptr32 = ptr32(dither1[s])
        dith_mat2:ptr32 = ptr32(dither2[s])
        dy:int = 0
        dx:int = 65536
        rastmin = ptr8(self.rastmin)
        rastmax = ptr8(self.rastmax)
        for y in range(40):
            mn:int = int(rastmin[y])
            mx:int = int(rastmax[y])
            if mn < mx:
                if dx == 65536:
                    dx = mn
                hline_dither(mn, mx, y, dith_mat1[dy & dith_h_mask], dith_mat2[dy & dith_h_mask], dx)
                dy += 1

    @micropython.native
    def draw(self):
        p2 = self.p2
        pm = self.pm
        faces = self.faces

        self.transform_vertices()

        i = 0
        len_p2 = len(p2)
        while i < len_p2:
            _x,_y,_z = pm[i]
            x = project_x(_x, _z)
            y = project_y(_y, _z)
            p2[i][0] = x ; p2[i][1] = y
            i += 1

        i = 0
        len_faces = len(faces)
        while i < len_faces:
            f = faces[i]
            fn = f[2]
            x0,y0,z0 = pm[fn[0]]
            x1,y1,z1 = pm[fn[1]]
            k = calc_norm_k(x0,y0,z0,x1,y1,z1)
            if (k - z0 + z1) > 0:
                s = self.calc_shade(f)
                self.rastface(f)
                self.drawrast(s)
            i += 1


    @micropython.viper
    def calc_shade(self, f) -> int:
        pm = self.pm
        xl:int = int(light_pos[0]); yl:int = int(light_pos[1]); zl:int = int(light_pos[2])
        p0 = pm[f[2][0]]
        p1 = pm[f[2][1]]
        x0:int = int(p0[0]); y0:int = int(p0[1]); z0:int = int(p0[2])
        x1:int = int(p1[0]); y1:int = int(p1[1]); z1:int = int(p1[2])

        vx:int = xl-x0 ; vy:int = yl-y0 ; vz:int = zl-z0
        wx:int = x1-x0 ; wy:int = y1-y0 ; wz:int = z1-z0

        a:int
        vx >>= 2 ; vy >>= 2 ; vz >>= 2
        while True:
            a = int(fpmul(vx,vx)) + int(fpmul(vy,vy)) + int(fpmul(vz,vz))
            if a >= 0:
                break
            a >>= 1 ; vy >>= 1; vz >>= 1
        m:int = int(isqrt(a)) << 1
        if m == 0:
            m = 2
        vx = int(fpdiv(vx,m)) <<1
        vy = int(fpdiv(vy,m)) <<1
        vz = int(fpdiv(vz,m)) <<1

        fs:int = int(f[1])

        dp:int = int(fpmul(vx, wx)) + int(fpmul(vy, wy)) + int(fpmul(vz, wz))
        if dp < 0:
            shade:int = light_ambient
        else:
            light_scale:int = fs - light_ambient
            shade:int = ((dp * light_scale) >> 16) + light_ambient
            if shade >= shadecnt:
                shade = shadecnt - 1
        return shade



shape_cube = Shape(
    [
        (-10,  10, -10),
        ( 10,  10, -10),
        ( 10, -10, -10),
        (-10, -10, -10),
        (-10,  10,  10),
        ( 10,  10,  10),
        ( 10, -10,  10),
        (-10, -10,  10),

        (   0,   8, -10), (   5,   0, -10), (   0,  -8, -10), (  -5,   0, -10),
        (   0,   5,  10), (   8,   0,  10), (   0,  -5,  10), (  -8,   0,  10),
        (  -7,  10,   7), (   7,  10,   7), (   0,  10,  -7),
        (  -4, -10,  -7), (   4, -10,  -7), (   4, -10,   7), (  -4, -10,   7),
        ( -10,   4,  -4), ( -10,   4,   4), ( -10,  -4,   4), ( -10,  -4,  -4),
        (  10,   4,  -4), (  10,   4,   4), (  10,  -4,   4), (  10,  -4,  -4),

    ], [
        ([ 0, 3, 2, 1],  6),
        ([ 4, 5, 6, 7], 10),
        ([ 0, 1, 5, 4],  6),
        ([ 7, 6, 2, 3], 11),
        ([ 0, 4, 7, 3], 12),
        ([ 1, 2, 6, 5], 12),

        ([ 8,11,10, 9], 12),
        ([12,13,14,15],  5),
        ([16,18,17],    13),
        ([19,22,21,20],  5),
        ([23,24,25,26],  6),
        ([27,30,29,28],  6),

    ])


shape_ball = Shape(
    [
        (-10,   4,  -4),
        (-10,   4,   4),
        (-10,  -4,   4),
        (-10,  -4,  -4),
        ( 10,   4,   4),
        ( 10,   4,  -4),
        ( 10,  -4,  -4),
        ( 10,  -4,   4),
        ( -4,   4,  10),
        (  4,   4,  10),
        (  4,  -4,  10),
        ( -4,  -4,  10),
        (  4,   4, -10),
        ( -4,   4, -10),
        ( -4,  -4, -10),
        (  4,  -4, -10),
        ( -4,  10,  -4),
        (  4,  10,  -4),
        (  4,  10,   4),
        ( -4,  10,   4),
        ( -4, -10,   4),
        (  4, -10,   4),
        (  4, -10,  -4),
        ( -4, -10,  -4),
    ], [
        ([ 0, 1, 2, 3], 14),
        ([ 4, 5, 6, 7], 14),
        ([ 8, 9,10,11], 12),
        ([12,13,14,15], 12),
        ([16,17,18,19], 10),
        ([20,21,22,23], 10),
        ([ 1, 8,10, 2], 10),
        ([ 9, 4, 7,10], 10),
        ([ 5,12,15, 6], 10),
        ([13, 0, 3,14], 10),
        ([19,18, 9, 8], 10),
        ([18,17, 5, 4], 10),
        ([17,16,13,12], 10),
        ([16,19, 1, 0], 10),
        ([11,10,21,20], 10),
        ([ 7, 6,22,21], 10),
        ([15,14,23,22], 10),
        ([ 3, 2,20,23], 10),
        ([ 1,19, 8],     6),
        ([ 9,18, 4],     6),
        ([ 5,17,12],     6),
        ([13,16, 0],     6),
        ([ 2,11,20],     6),
        ([10, 7,21],     6),
        ([ 6,15,22],     6),
        ([14, 3,23],     6),
    ])



road = Road(54, 6, -14, 0, 4, 2, 12)

road_speed = const(3 << 16)

stars = Stars(40)

from mountains import Mountains
mountains = Mountains(dither1, dither2, dith_w_mask, dith_h_mask)

gc.collect()

tune_seeds = [ ]

player = MusicPlayer(frame_rate, tune_seeds)


shape_cube.destructive_transform(None, [0, 0, fpone], random.randrange(-70, 70))
shape_ball.destructive_transform(None, [0, 0, fpone], random.randrange(-70, 70))

shape_cube.pos[2] = int2fp(2)
shape_ball.pos[2] = int2fp(2)

shape_lean_ang = 0

shape_ind_cube = const(0)
shape_ind_ball = const(1)
shape_state_being = const(0)
shape_state_entering = const(1)
shape_state_leaving = const(2)
shape_state_go_now = const(3)
shape_state_byeeee = const(4)
cube_y_start = const(80 << 16)
cube_y_lim = const(50 << 16)
cube_mod_init = const(0)
cube_mod_incr_entering = const(8000)
cube_mod_incr_leaving = const(600)
ball_y_start = const(34 << 16)
ball_y_lim = const(34 << 16)
ball_mod_incr = const(4096)
ball_decay_being = const(3900)
ball_decay_entering = const(2510)
ball_decay_leaving = const(4625)
ball_decay_go_already = const(5000)
ball_decay_vals = array('h', [0, 0, ball_decay_leaving, ball_decay_leaving, ball_decay_go_already])
shape_leave_t0 = utime.ticks_ms()
shape_leave_timeout = const(12000)

shape_ind_next = -1
shape_state = shape_state_entering
shape = shape_cube
shape_ind = shape_ind_cube
shape_cube.pos[1] = cube_y_start
shape_pos_mod = cube_mod_init


@micropython.native
def move_shape():
    global shape, shape_ind, shape_lean_ang
    global shape_ind_next
    global shape_leave_t0, shape_state, shape_pos_mod
    global ball_decay_vals

    shaperoad_delta = shape.pos[0] - (road.botseg_dx * 48)    # 1<<6 * 0.75
    if shaperoad_delta > 4096:
        shape.pos[0] -= 4096
    elif shaperoad_delta < -4096:
        shape.pos[0] += 4096
    else:
        shape.pos[0] -= shaperoad_delta

    ardx = road.botseg_dx
    if ardx < 0:
        ardx = -ardx
    shaperoad_delta = shape.pos[2] - ((2 << 16) - (ardx << 4))
    if shaperoad_delta > 4096:
        shape.pos[2] -= 4096
    elif shaperoad_delta < -4096:
        shape.pos[2] += 4096
    else:
        shape.pos[2] -= shaperoad_delta

    lean_ang_delta = road.botseg_dx - shape_lean_ang
    if lean_ang_delta > 256:
        shape_lean_ang += 256
    elif lean_ang_delta < -256:
        shape_lean_ang -= 256
    else:
        shape_lean_ang += lean_ang_delta
    if shape_lean_ang > 16384:
        shape_lean_ang = 16384
    elif shape_lean_ang < -16384:
        shape_lean_ang = -16384
    shape_rot_ang_sin = fpsin(shape_lean_ang >> 8)
    shape_rot_ang_cos = fpcos(shape_lean_ang >> 8)
    shape.rot_axis[0] = -fpmul_rot(shape_rot_ang_cos, shape_rot_ang_cos)
    shape.rot_axis[1] = fpmul_rot(shape_rot_ang_cos, shape_rot_ang_sin)
    shape.rot_axis[2] = -shape_rot_ang_sin

    shape.rot_angle += road_speed >> 14
    shape.rot_angle &= sintab_mask

    if shape_ind == shape_ind_cube:
        if shape_state == shape_state_being:
            b = fpsin((shape.rot_angle << 1) + sintab_sz_quart) * 4
            if b < 0: b = -b
            shape.pos[1] = (4 << 16) - b
            if utime.ticks_diff(utime.ticks_ms(), shape_leave_t0) >= shape_leave_timeout:
                shape_state = shape_state_leaving
                shape_pos_mod = cube_mod_init
        elif shape_state == shape_state_entering:
            shape.pos[1] -= shape_pos_mod
            shape_pos_mod += cube_mod_incr_entering
            b = fpsin((road.zoff >> 13) + sintab_sz_quart) * 4
            if b < 0: b = -b
            if shape.pos[1] <= (4 << 16) - b:
                shape_state = shape_state_being
                shape_leave_t0 = utime.ticks_ms()
        elif shape_state == shape_state_leaving:
            shape.pos[1] += shape_pos_mod
            shape.rot_angle += road_speed >> 15
            shape_pos_mod += cube_mod_incr_leaving
            if shape.pos[1] >= cube_y_lim:
                shape_state = shape_state_entering
                shape_ball.pos[1] = ball_y_start
                shape_pos_mod = 0
                shape_ind_next = shape_ind_ball
    else:
        if shape_state == shape_state_being:
            shape.pos[1] += shape_pos_mod
            shape_pos_mod -= ball_mod_incr
            if shape.pos[1] <= (-4 << 16):
                shape_pos_mod = (-shape_pos_mod * ball_decay_being) >> 12
            if utime.ticks_diff(utime.ticks_ms(), shape_leave_t0) >= shape_leave_timeout:
                shape_state = shape_state_leaving
        elif shape_state == shape_state_entering:
            shape.pos[1] += shape_pos_mod
            shape_pos_mod -= ball_mod_incr
            if shape.pos[1] <= (-4 << 16):
                shape_pos_mod = (-shape_pos_mod * ball_decay_entering) >> 12
                shape_state = shape_state_being
                shape_leave_t0 = utime.ticks_ms()
        elif shape_state >= shape_state_leaving:
            shape.pos[1] += shape_pos_mod
            shape_pos_mod -= ball_mod_incr
            if shape.pos[1] <= (-4 << 16):
                shape_pos_mod = (-shape_pos_mod * ball_decay_vals[shape_state]) >> 12
                if shape_state != shape_state_byeeee:
                    shape_state += 1
            if shape.pos[1] >= ball_y_lim:
                shape_state = shape_state_entering
                shape_cube.pos[1] = cube_y_start
                shape_pos_mod = cube_mod_init
                shape_ind_next = shape_ind_cube



@micropython.viper
def draw_ground():
    buffer1:ptr32 = ptr32(disp.buffer1)
    o:int = 54
    while o < 72:
        buffer1[o] = int(0xf0f0f0f0)
        o += 1
    while o < 90:
        buffer1[o] = -1
        o += 1


fade_out = False
next_tune_pressed = False ; next_tune_cnt = 0
mute_toggling = False ; mute_toggle_cnt = 0

@micropython.native
def handle_input():
    global player, fade_out
    global next_tune_pressed, next_tune_cnt
    global mute_toggling, mute_toggle_cnt

    if swB.value() == 0:
        fade_out = True

    if swA.value() == 0:
        if not next_tune_pressed:
            player.next_tune()
            next_tune_pressed = True
        next_tune_cnt = 10
    elif next_tune_pressed:
        next_tune_cnt -= 1
        if next_tune_cnt == 0:
            next_tune_pressed = False

    if swL.value() ^ swR.value() | swU.value() ^ swD.value():
        if not mute_toggling:
            player.toggle_mute()
            mute_toggling = True
        mute_toggle_cnt = 10
    elif mute_toggling:
        mute_toggle_cnt -= 1
        if mute_toggle_cnt == 0:
            mute_toggling = False


@micropython.native
def shape_update():
    global shape, shape_cube, shape_ball, shape_ind, shape_ind_next
    if shape_ind_next == shape_ind_cube:
        shape_ind = shape_ind_cube
        shape = shape_cube
        shape_cube.pos[0] = shape_ball.pos[0]
        shape_cube.pos[2] = shape_ball.pos[2]
        shape_ind_next = -1
    elif shape_ind_next == shape_ind_ball:
        shape_ind = shape_ind_ball
        shape = shape_ball
        shape_ball.pos[0] = shape_cube.pos[0]
        shape_ball.pos[2] = shape_cube.pos[2]
        shape_ind_next = -1


@micropython.native
def main(on_load):
    global player, disp, road, stars, mountains

    if on_load:
        on_load()

    disp.start()
    try:
        fade_contrast = 255 ; fade_cnt = 3
        mountain_x_speed = 0 ; mountain_x = 0

        player.start()

        while True:
            t0 = utime.ticks_us()
            player.frame()

            mountain_x_accel = mountain_x_speed - road.botseg_dx
            if mountain_x_accel > 128:
                mountain_x_speed -= 128
            elif mountain_x_accel < -128:
                mountain_x_speed += 128
            else:
                mountain_x_speed -= mountain_x_accel
            mountain_x += mountain_x_speed

            road.update(road_speed)
            disp.fill(0)
            draw_ground()
            rcx = road.draw()
            stars.draw_update(rcx, 25, road.botseg_dx << 4, road_speed << 2)
            mountains.draw(disp, mountain_x >> 13)
            move_shape()
            shape.draw()

            shape_update()

            handle_input()

            if fade_out:
                fade_cnt -= 1
                if fade_cnt == 0:
                    fade_cnt = 4
                    if fade_contrast == 0:
                        break
                    disp.contrast(fade_contrast)
                    fade_contrast >>= 1

            disp.show()

            utime.sleep_ms((frame_microsec - utime.ticks_diff(utime.ticks_us(), t0)) >> 10)
            utime.sleep_us(frame_microsec - utime.ticks_diff(utime.ticks_us(), t0) - 12)

    finally:
        player.stop()
        disp.teardown()

