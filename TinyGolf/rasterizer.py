# TinyGolf
# Copyright Daniel Schroeder 2023
#
# This file is part of TinyGolf.
#
# TinyGolf is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# TinyGolf is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# TinyGolf. If not, see <https://www.gnu.org/licenses/>.

# - COMMENTS REMOVED TO SAVE SPACE -
# For commented version, see https://github.com/dan5sch/thumby-mini-golf-public

from array import array
import utils


@micropython.viper
def fill_or_column_mask_unchecked(
    buf0:ptr8, buf1:ptr8, x:int, y0:int, y1:int, width:int, fill_mask0:int,
    fill_mask1:int):
    yb0 = y0 >> 3
    yb1 = y1 >> 3
    ym0 = y0 & 7
    ym1 = y1 & 7
    i = x + width * yb0
    if yb0 == yb1:
        mask = (((1 << (ym1 - ym0 + 1)) - 1) << ym0)
        buf0[i] |= mask & fill_mask0
        buf1[i] |= mask & fill_mask1
    else:

        mask = ((0xff >> ym0) << ym0)
        buf0[i] |= mask & fill_mask0
        buf1[i] |= mask & fill_mask1
        i_last = x + width * yb1
        i += width
        while i < i_last:
            buf0[i] = fill_mask0
            buf1[i] = fill_mask1
            i += width
        mask = ((2 << ym1) - 1)
        buf0[i] |= mask & fill_mask0
        buf1[i] |= mask & fill_mask1


I_RL_SP = const(0)
I_RL_SP_B = const(1)
I_RL_SP_E = const(2)
I_RL_A = const(3)
I_RL_FLAGS = const(4)
I_RL_A_S_A_P = const(5)
I_RL_REGION_0_1 = const(6)
I_RL_PAYLOAD_0_1 = const(7)
I_RL_NUM_FIELDS = const(8)

RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT = const(0x1)
RL_FLAG_BIT_DELTA_P_IS_POSITIVE = const(0x2)
RL_FLAG_BIT_IS_PAST_EXIT = const(0x4)
RL_FLAG_BIT_A_M_IS_A_P = const(0x8)
RL_FLAG_BIT_CORRECT_ENDPOINTS = const(0x10)
RL_FLAG_SHIFT_MASK_LAYER = const(5)
RL_FLAG_ALL_BITS = const(0x1ff)

RL_NUM_BYTES = const(I_RL_NUM_FIELDS << 2)

RL_SP_BIAS = const(0x4000)
RL_P_E_DONT_CORRECT = const(0x00007fff)
RL_NUM_REGIONS = const(8)
RL_REGION_UNUSED = const(RL_NUM_REGIONS)


@micropython.viper
def rl_init(base:ptr32, s_b:int, p_b:int, s_e:int, p_e:int, region0:int,
            region1:int, payload0:int, payload1:int, mask_layer:int,
            is_past_exit:bool):
    d_s = s_e - s_b
    d_p = p_e - p_b
    delta_p_is_positive = bool(True)
    if d_p < 0:
        delta_p_is_positive = bool(False)
        d_p = 0 - d_p
    is_steep = bool(d_p > d_s)
    p = int(0)
    a = int(0)
    a_s = int(0)
    a_p = int(0)
    a_m_is_a_p = bool(True)
    correct_endpoints = bool(False)
    if d_s == 0:
        if is_past_exit:
            if p_e > p_b:
                p = p_e
            else:
                p = p_b
            p += 1
        else:
            if p_e < p_b:
                p = p_e
            else:
                p = p_b
    elif is_steep:
        p = p_b
        if not delta_p_is_positive:
            p += 1
        a = d_p
        a_s = 2 * d_p
        a_p = 2 * d_s
        a_m = a_s
        a_m_is_a_p = bool(False)
        if (delta_p_is_positive and is_past_exit) or \
           (not delta_p_is_positive and not is_past_exit):
            correct_endpoints = bool(True)
            num_steps_p = (a // a_p) + 1
            a += a_s - num_steps_p * a_p
            if delta_p_is_positive:
                p += num_steps_p
                p_e += 1
            else:
                p -= num_steps_p
        else:
            p_e = int(RL_P_E_DONT_CORRECT)
    else:
        if is_past_exit:
            p = p_b + 1
        else:
            p = p_b
        a = d_s
        a_s = 2 * d_p
        a_p = 2 * d_s
        a_m_is_a_p = bool(True)
        p_e = int(RL_P_E_DONT_CORRECT)
    flags = int(RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT)
    if delta_p_is_positive:
        flags |= int(RL_FLAG_BIT_DELTA_P_IS_POSITIVE)
    if is_past_exit:
        flags |= int(RL_FLAG_BIT_IS_PAST_EXIT)
    if a_m_is_a_p:
        flags |= int(RL_FLAG_BIT_A_M_IS_A_P)
    if correct_endpoints:
        flags |= int(RL_FLAG_BIT_CORRECT_ENDPOINTS)
    flags |= mask_layer << int(RL_FLAG_SHIFT_MASK_LAYER)
    sp = (s_b << 16) | p
    base[int(I_RL_SP)] = sp
    base[int(I_RL_SP_B)] = sp
    base[int(I_RL_SP_E)] = (s_e << 16) | p_e
    base[int(I_RL_A)] = a
    base[int(I_RL_FLAGS)] = flags
    base[int(I_RL_A_S_A_P)] = (a_s << 16) | a_p
    base[int(I_RL_REGION_0_1)] = (region0 << 16) | region1
    base[int(I_RL_PAYLOAD_0_1)] = (payload0 << 16) | payload1

@micropython.viper
def rl_seek_s_to(rl:ptr32, s_after:int):
    s_e = rl[int(I_RL_SP_E)] >> 16
    if s_after > s_e:
        return
    s_b = rl[int(I_RL_SP_B)] >> 16
    if s_after < s_b:
        s_after = s_b
    a_s = rl[int(I_RL_A_S_A_P)] >> 16
    a_p = rl[int(I_RL_A_S_A_P)] & 0xffff
    a_m = a_s
    if bool(rl[int(I_RL_FLAGS)] & int(RL_FLAG_BIT_A_M_IS_A_P)):
        a_m = a_p
    if s_after < (rl[int(I_RL_SP)] >> 16):
        rl[int(I_RL_SP)] = rl[int(I_RL_SP_B)]
        rl[int(I_RL_FLAGS)] |= int(RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT)
        rl[int(I_RL_A)] = a_m >> 1
        if bool(rl[int(I_RL_FLAGS)] & int(RL_FLAG_BIT_CORRECT_ENDPOINTS)):
            n_p = (rl[int(I_RL_A)] // a_p) + 1
            rl[int(I_RL_A)] += a_s - n_p * a_p
    s_before = rl[int(I_RL_SP)] >> 16
    if s_after > s_before:
        num_steps_s = s_after - s_before
        rl[int(I_RL_A)] += num_steps_s * a_s
        rl[int(I_RL_SP)] += num_steps_s << 16
        if rl[int(I_RL_A)] >= a_m:
            num_steps_p = ((rl[int(I_RL_A)] - a_m) // a_p) + 1
            rl[int(I_RL_A)] -= num_steps_p * a_p
            if bool(rl[int(I_RL_FLAGS)] & int(RL_FLAG_BIT_DELTA_P_IS_POSITIVE)):
                rl[int(I_RL_SP)] += num_steps_p
            else:
                rl[int(I_RL_SP)] -= num_steps_p
        if s_after == s_e:
            rl[int(I_RL_FLAGS)] |= int(RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT)
            if bool(rl[int(I_RL_FLAGS)] & int(RL_FLAG_BIT_CORRECT_ENDPOINTS)):
                rl[int(I_RL_SP)] = rl[int(I_RL_SP_E)]
        else:
            rl[int(I_RL_FLAGS)] &= \
                (int(RL_FLAG_ALL_BITS) ^ int(RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT))

@micropython.viper
def rl_increment_s(rl:ptr32):
    if (rl[int(I_RL_SP)] ^ rl[int(I_RL_SP_E)]) < 0x10000:
        return
    a_s = rl[int(I_RL_A_S_A_P)] >> 16
    a_p = rl[int(I_RL_A_S_A_P)] & 0xffff
    a_m = a_s
    if bool(rl[int(I_RL_FLAGS)] & int(RL_FLAG_BIT_A_M_IS_A_P)):
        a_m = a_p
    rl[int(I_RL_A)] += a_s
    rl[int(I_RL_SP)] += 0x10000
    if rl[int(I_RL_A)] >= a_m:
        num_steps_p = ((rl[int(I_RL_A)] - a_m) // a_p) + 1
        rl[int(I_RL_A)] -= num_steps_p * a_p
        if bool(rl[int(I_RL_FLAGS)] & int(RL_FLAG_BIT_DELTA_P_IS_POSITIVE)):
            rl[int(I_RL_SP)] += num_steps_p
        else:
            rl[int(I_RL_SP)] -= num_steps_p
    if (rl[int(I_RL_SP)] ^ rl[int(I_RL_SP_E)]) < 0x10000:
        rl[int(I_RL_FLAGS)] |= int(RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT)
        if bool(rl[int(I_RL_FLAGS)] & int(RL_FLAG_BIT_CORRECT_ENDPOINTS)):
            rl[int(I_RL_SP)] = rl[int(I_RL_SP_E)]
    else:
        rl[int(I_RL_FLAGS)] &= \
            (int(RL_FLAG_ALL_BITS) ^ int(RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT))


PB_MAX_PIXELS = const(1024)

class PayloadBuffer:
    def __init__(self):
        self.buffer = array('h', range(PB_MAX_PIXELS))
        for i in range(len(self.buffer)):
            self.buffer[i] = 0
        self.width = 1
        self.height = 1

    @micropython.native
    def set_dimensions(self, width, height):
        if width * height > PB_MAX_PIXELS:
            raise RuntimeError(
                f"setting too-large payload buffer {width}, {height}")
        self.width = width
        self.height = height

    @micropython.viper
    def fill(self, payload:int):
        buf = ptr16(self.buffer)
        size = int(self.width) * int(self.height)
        for i in range(size):
            buf[i] = payload



SR_MAX_NUM_RL = const(512)

SR_BUFFER_TYPE_DISPLAY = const(0)
SR_BUFFER_TYPE_PAYLOAD = const(1)

class ScanlineRasterizer:
    def __init__(self, arr_region_fill0, arr_region_fill1):
        self.num_rl = 0
        SHARD_NUM_FIELDS = const(256)
        RL_PER_SHARD = const(SHARD_NUM_FIELDS // I_RL_NUM_FIELDS)
        NUM_SHARDS = const((SR_MAX_NUM_RL + RL_PER_SHARD - 1) // RL_PER_SHARD)
        self.shards = [array('l', range(SHARD_NUM_FIELDS)) \
                       for i in range(NUM_SHARDS)]
        self.arr_ptr_rl_sorted = array('P', range(SR_MAX_NUM_RL))
        self._fill_ptrs()

        self.arr_region_insideness = array('l', [0] * (RL_NUM_REGIONS + 1))
        self.arr_region_payload = array('l', [0] * (RL_NUM_REGIONS + 1))
        self.arr_region_fill0 = arr_region_fill0
        self.arr_region_fill1 = arr_region_fill1

    @micropython.viper
    def _fill_ptrs(self):
        arr_ptr_rl_sorted = ptr32(self.arr_ptr_rl_sorted)
        i_shard_next = int(0)
        i_rl_shard = int(RL_PER_SHARD)
        ptr_rl = int(0)
        for i_rl in range(int(SR_MAX_NUM_RL)):
            if i_rl_shard >= int(RL_PER_SHARD):
                i_rl_shard = int(0)
                ptr_rl = int(ptr(self.shards[i_shard_next]))
                i_shard_next += int(1)
            arr_ptr_rl_sorted[i_rl] = ptr_rl
            ptr_rl += int(RL_NUM_BYTES)
            i_rl_shard += int(1)

    @micropython.native
    def clear_edges(self):
        self.num_rl = 0

    @micropython.native
    def set_num_rl(self, num_rl):
        self.num_rl = num_rl

    @micropython.viper
    def _allocate_rl(self) -> ptr:
        num_rl = int(self.num_rl)
        if num_rl == int(SR_MAX_NUM_RL):
            print("allocating too many rl")
            num_rl -= 1
        self.set_num_rl(num_rl + 1)
        return ptr(self.arr_ptr_rl_sorted[num_rl])

    @micropython.viper
    def _sort_range_ptr_rl_insertion(self, i_begin:int, i_end:int):
        if i_begin >= i_end:
            return
        arr_ptr_rl_sorted = ptr32(self.arr_ptr_rl_sorted)
        sp_sorted_max = ptr32(arr_ptr_rl_sorted[i_begin])[int(I_RL_SP)]
        i_to_insert = i_begin + 1
        while i_to_insert < i_end:
            sp_to_insert = \
                ptr32(arr_ptr_rl_sorted[i_to_insert])[int(I_RL_SP)]
            if sp_to_insert < sp_sorted_max:
                i_dest = i_to_insert - 1
                swap = arr_ptr_rl_sorted[i_dest]
                arr_ptr_rl_sorted[i_dest] = arr_ptr_rl_sorted[i_to_insert]
                arr_ptr_rl_sorted[i_to_insert] = swap
                while i_dest > i_begin:
                    i_prev = i_dest - 1
                    sp_prev = ptr32(arr_ptr_rl_sorted[i_prev])[int(I_RL_SP)]
                    if sp_to_insert < sp_prev:
                        swap = arr_ptr_rl_sorted[i_prev]
                        arr_ptr_rl_sorted[i_prev] = arr_ptr_rl_sorted[i_dest]
                        arr_ptr_rl_sorted[i_dest] = swap
                        i_dest -= 1
                    else:
                        break
            else:
                sp_sorted_max = sp_to_insert
            i_to_insert += 1

    @micropython.viper
    def set_region_fill_bytes(self, i_region:int, buf0:ptr8, buf1:ptr8):
        dest0 = ptr8(uint(ptr(self.arr_region_fill0)) + 8 * i_region)
        dest1 = ptr8(uint(ptr(self.arr_region_fill1)) + 8 * i_region)
        for i in range(8):
            dest0[i] = buf0[i]
            dest1[i] = buf1[i]

    @micropython.viper
    def add_edge_line_fill(self, x_b:int, y_b:int, x_e:int, y_e:int,
                           region_line:int, region_fill:int, payload_line:int,
                           payload_fill:int, mask_layer:int):
        s_b = x_b + int(RL_SP_BIAS)
        p_b = y_b + int(RL_SP_BIAS)
        s_e = x_e + int(RL_SP_BIAS)
        p_e = y_e + int(RL_SP_BIAS)

        region_unused = int(RL_REGION_UNUSED)
        has_line = bool(region_line != region_unused)

        is_single_scanline = bool(s_e == s_b)
        winding_is_past_exit = bool(s_e > s_b)
        if not winding_is_past_exit:
            swap = s_b
            s_b = s_e
            s_e = swap
            swap = p_b
            p_b = p_e
            p_e = swap

        need_enter = has_line
        region_fill_enter = region_unused
        if is_single_scanline or not winding_is_past_exit:
            need_enter = True
            region_fill_enter = region_fill
        if need_enter:
            rl_enter = ptr32(self._allocate_rl())
            rl_init(rl_enter, s_b, p_b, s_e, p_e, region_line,
                    region_fill_enter, payload_line, payload_fill, mask_layer,
                    False)

        need_past_exit = has_line
        region_fill_past_exit = region_unused
        if is_single_scanline or winding_is_past_exit:
            need_past_exit = True
            region_fill_past_exit = region_fill
        if need_past_exit:
            rl_past_exit = ptr32(self._allocate_rl())
            rl_init(rl_past_exit, s_b, p_b, s_e, p_e, region_line,
                    region_fill_past_exit, payload_line, payload_fill,
                    mask_layer, True)

    @micropython.viper
    def rasterize_to_buffer(self, buf0:ptr, buf1:ptr, buffer_type:int,
                            mask_layer:int, x_first:int, y_first:int, x_dim:int,
                            y_dim:int):
        if buffer_type == int(SR_BUFFER_TYPE_DISPLAY):
            utils.timestamp_add()
        num_rl = int(self.num_rl)
        arr_ptr_rl_sorted = ptr32(self.arr_ptr_rl_sorted)
        arr_region_insideness = ptr32(self.arr_region_insideness)
        arr_region_payload = ptr32(self.arr_region_payload)
        arr_region_fill0 = ptr8(self.arr_region_fill0)
        arr_region_fill1 = ptr8(self.arr_region_fill1)
        region_unused = int(RL_REGION_UNUSED)

        buffer_is_payload = bool(buffer_type == int(SR_BUFFER_TYPE_PAYLOAD))
        num_scanlines = x_dim
        len_scanline = y_dim
        s_first = x_first + int(RL_SP_BIAS)
        s_last = s_first + num_scanlines - 1
        p_first = y_first + int(RL_SP_BIAS)
        p_past_last = p_first + len_scanline

        for i in range(num_rl):
            rl = ptr32(arr_ptr_rl_sorted[i])
            rl_seek_s_to(rl, s_first)
        self._sort_range_ptr_rl_insertion(0, num_rl)
        if buffer_type == int(SR_BUFFER_TYPE_DISPLAY):
            utils.timestamp_add()
        s = s_first
        i_rl_s_begin = int(0)
        while i_rl_s_begin < num_rl:
            rl_s_begin = ptr32(arr_ptr_rl_sorted[i_rl_s_begin])
            s = rl_s_begin[int(I_RL_SP)] >> 16
            if s >= s_first:
                break
            i_rl_s_begin += 1
        i_rl_s_end = i_rl_s_begin

        while i_rl_s_begin < num_rl:
            if s > s_last:
                break
            if i_rl_s_end == i_rl_s_begin:
                while i_rl_s_end < num_rl:
                    rl_s_end = ptr32(arr_ptr_rl_sorted[i_rl_s_end])
                    s_end = rl_s_end[int(I_RL_SP)] >> 16
                    if s_end != s:
                        break
                    i_rl_s_end += 1
            for i in range(int(RL_NUM_REGIONS) + 1):
                arr_region_insideness[i] = 0
            p_span_begin = p_first

            i_rl_in_s = i_rl_s_begin
            while i_rl_in_s < i_rl_s_end:
                rl_in_s = ptr32(arr_ptr_rl_sorted[i_rl_in_s])
                p = rl_in_s[int(I_RL_SP)] & 0xffff
                if p > p_span_begin:
                    clamped_span = bool(p >= p_past_last)
                    if clamped_span:
                        p = p_past_last
                    for i_reg in range(int(RL_NUM_REGIONS)):
                        if arr_region_insideness[i_reg] > 0:
                            if buffer_is_payload:
                                x = s - s_first
                                y_begin = p_span_begin - p_first
                                i_pay = x + y_begin * x_dim
                                i_pay_end = i_pay + (p - p_span_begin) * x_dim
                                buf_payload = ptr16(buf0)
                                payload = arr_region_payload[i_reg]
                                while i_pay < i_pay_end:
                                    buf_payload[i_pay] = payload
                                    i_pay += x_dim
                            else:
                                x = s - s_first
                                fill_mask0 = \
                                    arr_region_fill0[8 * i_reg + (x & 0x7)]
                                fill_mask1 = \
                                    arr_region_fill1[8 * i_reg + (x & 0x7)]
                                y0 = p_span_begin - p_first
                                y1 = p - 1 - p_first
                                fill_or_column_mask_unchecked(
                                    buf0, buf1, x, y0, y1, x_dim, fill_mask0,
                                    fill_mask1)
                            break
                    if clamped_span:
                        p_span_begin = int(0x7fffffff)
                    else:
                        p_span_begin = p
                flags = rl_in_s[int(I_RL_FLAGS)]
                if (flags >> int(RL_FLAG_SHIFT_MASK_LAYER)) & mask_layer:
                    is_past_exit = bool(flags & int(RL_FLAG_BIT_IS_PAST_EXIT))
                    at_endpoint = \
                        bool(flags & int(RL_FLAG_BIT_SCANLINE_HAS_ENDPOINT))
                    delta_inside = int(2)
                    if at_endpoint:
                        delta_inside = int(1)
                    if is_past_exit:
                        delta_inside = 0 - delta_inside
                    region_0_1 = rl_in_s[int(I_RL_REGION_0_1)]
                    arr_region_insideness[region_0_1 >> 16] += delta_inside
                    arr_region_insideness[region_0_1 & 0xffff] += delta_inside
                    if buffer_is_payload and not is_past_exit:
                        payload_0_1 = rl_in_s[int(I_RL_PAYLOAD_0_1)]
                        arr_region_payload[region_0_1 >> 16] = payload_0_1 >> 16
                        arr_region_payload[region_0_1 & 0xffff] = \
                            payload_0_1 & 0xffff
                rl_increment_s(rl_in_s)
                i_rl_in_s += 1

            s += 1
            while i_rl_s_end < num_rl:
                rl_s_end = ptr32(arr_ptr_rl_sorted[i_rl_s_end])
                s_end = rl_s_end[int(I_RL_SP)] >> 16
                if s_end != s:
                    break
                i_rl_s_end += 1
            self._sort_range_ptr_rl_insertion(i_rl_s_begin, i_rl_s_end)
            while i_rl_s_begin < i_rl_s_end:
                rl_s_begin = ptr32(arr_ptr_rl_sorted[i_rl_s_begin])
                s_begin = rl_s_begin[int(I_RL_SP)] >> 16
                if s_begin == s:
                    break
                i_rl_s_begin += 1
            if i_rl_s_begin == i_rl_s_end and i_rl_s_begin < num_rl:
                rl_s_begin = ptr32(arr_ptr_rl_sorted[i_rl_s_begin])
                s = rl_s_begin[int(I_RL_SP)] >> 16

        if buffer_type == int(SR_BUFFER_TYPE_DISPLAY):
            utils.timestamp_add()


list_diameter_circle = [
bytearray(b'\x01'),
bytearray(b'\x03\x03'),
bytearray(b'\x07\x07\x07'),
bytearray(b'\x06\x0f\x0f\x06'),
bytearray(b'\x0e\x1f\x1f\x1f\x0e'),
bytearray(b'\x0c\x1e\x3f\x3f\x1e\x0c'),
bytearray(b'\x1c\x3e\x7f\x7f\x7f\x3e\x1c'),
bytearray(b'\x3c\x7e\xff\xff\xff\xff\x7e\x3c'),
bytearray(b'\
\x38\xfe\xfe\xff\xff\xff\xfe\xfe\x38\
\x00\x00\x00\x01\x01\x01\x00\x00\x00')]
list_diameter_circle_line = [
bytearray(b'\x01'),
bytearray(b'\x03\x03'),
bytearray(b'\x07\x05\x07'),
bytearray(b'\x06\x09\x09\x06'),
bytearray(b'\x0e\x11\x11\x11\x0e'),
bytearray(b'\x0c\x12\x21\x21\x12\x0c'),
bytearray(b'\x1c\x22\x41\x41\x41\x22\x1c'),
bytearray(b'\x3c\x42\x81\x81\x81\x81\x42\x3c'),
bytearray(b'\
\x38\xc6\x82\x01\x01\x01\x82\xc6\x38\
\x00\x00\x00\x01\x01\x01\x00\x00\x00')]

scratch_blit = bytearray(18)

@micropython.native
def draw_circle_line_fill(display, xs_center_f10, ys_center_f10, diameter_f10,
                          color_line, color_fill):
    global scratch_blit

    diameter_max = len(list_diameter_circle)
    diameter = (diameter_f10 + 0x200) >> 10
    if diameter < 1:
        diameter = 1
    elif diameter > diameter_max:
        diameter = diameter_max
    rad_floor = diameter >> 1
    xs = ((xs_center_f10 + 0x200) >> 10) - rad_floor
    ys = ((ys_center_f10 + 0x200) >> 10) - rad_floor
    if color_line == color_fill:
        blit_src = list_diameter_circle[diameter - 1]
    else:
        blit_src = list_diameter_circle_line[diameter - 1]
    if color_line:
        blit_to_use = blit_src
    else:
        blit_to_use = scratch_blit
        for i in range(len(blit_src)):
            blit_to_use[i] = blit_src[i] ^ 0xff
    if color_line == color_fill:
        key = 1 - color_line
        display.blit(blit_to_use, xs, ys, diameter, diameter, key, 0, 0)
    else:
        key = -1
        display.blitWithMask(blit_to_use, xs, ys, diameter, diameter, key, 0, 0,
                             list_diameter_circle[diameter - 1])
