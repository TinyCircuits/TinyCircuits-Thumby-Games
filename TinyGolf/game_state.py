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

from time import ticks_ms
import math

import thumbyHardware as th
import utils
import levels

bytes_3x5 = bytearray(
b'\x0e\x11\x0e\x12\x1f\x10\x12\x19\x16\x15\x15\x0a\x07\x04\x1f\x17\x15\x0d'
b'\x1f\x15\x1d\x01\x19\x07\x1f\x15\x1f\x07\x05\x1f\x1b\x04\x1b\x18\x0e\x03')

bytes_arrow_left = bytearray(b'\x04\x0a\x11')

bytes_logo = bytearray(
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x31\x1d\x07'
b'\x01\x31\x25\x00\x30\x1c\x08\x28\x18\x00\x58\x54\x30\x18\x0c\x00\x00\x00\x1c'
b'\x26\x21\x29\x19\x00\x18\x2c\x24\x1c\x00\x18\x2e\x23\x00\x38\x0e\x05\x01\x02'
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
invmask_logo = bytearray(
b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xfc\x84\x80\x80\xc0'
b'\x80\x80\x80\x80\x81\x81\x81\x83\x83\x03\x01\x01\x01\x81\xc1\xe1\xff\xc1\x80'
b'\x80\x80\x80\x80\xc0\x81\x81\x81\x81\xc1\x80\x80\x80\x80\x80\x80\xe0\xf0\xf8'
b'\xf8\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff')

bytes_footer = bytearray(
b'\x00\x60\x80\x60\x00\x90\xf8\x80\x00\x80\x00\x70\x88\x70\x00\x00\x00\x00\x00'
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x78\xa0\xc0\x00'
b'\x90\xa0\x50\x00\x00\x00\xc0\xa0\x78\x00\xc0\xa0\xf0\x00\xe0\x20\xc0\x00\xb8'
b'\xa8\x68\x00\x80\xb0\x50\x00\x40\xa0\xa0\x00\xf8\x20\xc0\x00')
invmask_footer = bytearray(
b'\x0f\x0f\x0f\x0f\x07\x03\x03\x03\x3f\x3f\x07\x03\x03\x03\x07\xff\xff\xff\xff'
b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x03\x03\x03\x1f\x07'
b'\x07\x07\x07\x07\xff\x1f\x0f\x03\x03\x03\x0f\x07\x07\x07\x0f\x0f\x0f\x03\x03'
b'\x03\x03\x03\x07\x07\x07\x07\x0f\x0f\x0f\x03\x03\x03\x0f\x1f')

@micropython.viper
def smoothstep_f10(x_f10:int) -> int:
    if x_f10 < 0:
        return 0
    if x_f10 > 1024:
        return 1024
    x2_f20 = x_f10 * x_f10
    x3_f20 = (x2_f20 * x_f10 + 0x200) >> 10
    return (3 * x2_f20 - 2 * x3_f20 + 0x200) >> 10

def score_before_continue():
    score = 0
    for i_level in range(utils.save_data.i_level):
        score += utils.save_data.arr_level_strokes[i_level] - \
            levels.levels[i_level].par
    return score

def frame_handler_noop(mgs):
    pass

DELTA_MIN_MS = const(16)
DELTA_MAX_MS = const(200)

BUTTON_L = const(0x1)
BUTTON_R = const(0x2)
BUTTON_U = const(0x4)
BUTTON_D = const(0x8)
BUTTON_A = const(0x10)
BUTTON_B = const(0x20)
BUTTON_ALL = const(0x3f)

class MicroGolfState:
    def __init__(self, game_dir, chunk_data, tr_display, tr_payload, display,
                 payload, ball):
        self.game_dir = game_dir
        self.chunk_data = chunk_data
        self.tr_display = tr_display
        self.tr_payload = tr_payload
        self.display = display
        self.payload = payload
        self.ball = ball
        self.load_level(0)
        self.continuous_play = False
        self.frame_handler = frame_handler_noop
        self.frame = 0
        self.t_ms = ticks_ms()
        self.delta_ms = 0
        self.show_timestamps = False
        self.mask_pressed = 0
        self.mask_just_pressed = 0
        self.hud = HudRenderer(self)
        self.save_reset_hold_ms = 0

    @micropython.native
    def _set_frame_button_masks(self):
        mask_pressed_new = 0
        if th.swL.value() != 1:
            mask_pressed_new |= BUTTON_L
        if th.swR.value() != 1:
            mask_pressed_new |= BUTTON_R
        if th.swU.value() != 1:
            mask_pressed_new |= BUTTON_U
        if th.swD.value() != 1:
            mask_pressed_new |= BUTTON_D
        if th.swA.value() != 1:
            mask_pressed_new |= BUTTON_A
        if th.swB.value() != 1:
            mask_pressed_new |= BUTTON_B
        self.mask_just_pressed = \
            mask_pressed_new & (self.mask_pressed ^ BUTTON_ALL)
        self.mask_pressed = mask_pressed_new

    def load_level(self, i_level):
        self.i_level = i_level
        self.level = levels.levels[i_level]
        self.chunk_data.load_level(self.level, self.game_dir + "/levels.bin")
        self.tr_display.set_chunk_data(self.chunk_data)
        self.tr_payload.set_chunk_data(self.chunk_data)
        self.num_strokes = 0
        self.ball.set_mask_layer(self.level.mask_layer_tee)
        self.ball.reset_location_f10(self.level.xw_tee << 10,
                                     self.level.yw_tee << 10)
        self.ball.set_location_hole_f10(self.level.xw_hole << 10,
                                        self.level.yw_hole << 10)
        self.ball.reset_velocity_wd_f20(0, 0)

    def draw_level(self):
        self.tr_display.rasterize_to_display(self.display, self.ball.mask_layer)

    def draw_hole(self):
        self.ball.draw_hole(self.display, self.tr_display, 0)

    def draw_ball(self):
        self.ball.draw_ball(self.display, self.tr_display, 1)

    def draw_hud(self):
        self.hud.draw_hud(self.i_level + 1, self.num_strokes + 1,
                          self.level.par)

    def draw_action_arrow(self, x, y, direction):
        cycle_ms = const(400)
        ang = (self.t_ms % (cycle_ms << 1)) * math.pi / float(cycle_ms)
        scale = const(2)
        off = int(math.sin(ang) * scale) * direction

        self.display.blit(bytes_arrow_left, x - 1 + off, y - 2, 3, 5, 0,
                          int(direction >= 0), 0)

    def advance_ball(self):
        self.ball.advance(self.delta_ms, self.tr_payload, self.payload,
                          self.chunk_data.arr_chunk_normal_wd)

    def translate_ball_to_screen(self, xs, ys):
        ball = self.ball
        self.tr_display.set_translate_map_world_to_screen_f10(
            ball.xw_f10, ball.yw_f10, xs << 10, ys << 10)

    def run_frame(self):
        self.frame += 1
        t_next_ms = ticks_ms()
        self.delta_ms = \
            max(DELTA_MIN_MS, min(DELTA_MAX_MS, t_next_ms - self.t_ms))
        self.t_ms = t_next_ms
        utils.timestamp_reset()
        utils.timestamp_add()
        self._set_frame_button_masks()
        if self.mask_pressed == (BUTTON_A | BUTTON_B):
            self.save_reset_hold_ms += self.delta_ms
            if self.save_reset_hold_ms > 3000:
                utils.delete_save()
                if utils.use_gray:
                    self.display.disableGrayscale()
                th.reset()
        else:
            self.save_reset_hold_ms = 0
        self.frame_handler(self)
        utils.timestamp_add()
        if self.show_timestamps:
            utils.timestamp_display(self.display)
        self.display.update()

class AxisHoldTracker:
    def __init__(self, button0, button1):
        self.button0 = button0
        self.button1 = button1
        self.button_held = 0
        self.just_held = False
        self.held_ms = 0

    @micropython.native
    def reset(self):
        self.button_held = 0
        self.just_held = False
        self.held_ms = 0

    @micropython.native
    def update(self, mgs):
        mask_pressed = mgs.mask_pressed
        mask_just_pressed = mgs.mask_just_pressed
        if not self.button_held:
            mask_just_pressed = mask_pressed
        delta_ms = mgs.delta_ms

        if mask_just_pressed & self.button0:
            self.button_held = self.button0
            self.just_held = True
            self.held_ms = delta_ms
        elif mask_just_pressed & self.button1:
            self.button_held = self.button1
            self.just_held = True
            self.held_ms = delta_ms
        elif mask_pressed & self.button_held:
            self.just_held = False
            self.held_ms += delta_ms
        elif self.button_held:
            self.button_held = 0
            self.just_held = False
            self.held_ms = 0

class HudRenderer:
    def __init__(self, mgs):
        self.buf0 = mgs.display.display.buffer
        self.buf1 = mgs.display.display.shading
        self.i_buf = 0

    @micropython.native
    def _reset(self):
        self.i_buf = 0

    @micropython.native
    def _add_col(self, byte_col):
        i_buf = self.i_buf
        self.buf0[i_buf] = byte_col
        self.buf1[i_buf] = 0x00
        self.i_buf = i_buf + 1

    @micropython.native
    def _add_3x5(self, c, byte_col):
        i_buf = self.i_buf
        buf0 = self.buf0
        buf1 = self.buf1
        i_chr = 3 * c
        for k in range(3):
            buf0[i_buf + k] = (bytes_3x5[i_chr + k] << 1) | byte_col
            buf1[i_buf + k] = 0x00
        self.i_buf = i_buf + 3

    @micropython.native
    def draw_hud(self, level, stroke, par):
        BG = const(0x80)
        LINE = const(0xff)

        self._reset()
        self._add_col(BG)
        self._add_3x5(level, BG)
        self._add_col(BG)
        self._add_col(LINE)
        self._add_col(BG)
        self._add_3x5(min(10, stroke), BG)
        self._add_col(BG)
        self._add_3x5(11, BG)
        self._add_col(BG)
        self._add_3x5(par, BG)
        self._add_col(BG)
        self._add_col(LINE)

ANGLE_PER_MS_SLOW_F10 = const(15)
ANGLE_PER_MS_FAST_F10 = const(90)
DURATION_SLOW_ANGLE_MS = const(1000)

SCALE_UP_PER_MS = const(1.0006)
SCALE_DOWN_PER_MS = const(0.9994)
SCALE_MIN_F10 = const(128)
SCALE_MAX_F10 = const(1024)

class RotationScaleController:
    def __init__(self):
        self.angle_start_wd = 0
        self.scale_start_f10 = 1024
        self.tracker_LR = AxisHoldTracker(BUTTON_L, BUTTON_R)
        self.tracker_UD = AxisHoldTracker(BUTTON_U, BUTTON_D)

    def reset(self):
        self.tracker_LR.reset()
        self.tracker_UD.reset()

    @micropython.native
    def control(self, mgs):
        tr_display = mgs.tr_display
        tracker_LR = self.tracker_LR
        tracker_UD = self.tracker_UD

        tracker_LR.update(mgs)
        tracker_UD.update(mgs)

        if tracker_LR.just_held:
            self.angle_start_wd = tr_display.angle_wd
        held_LR = tracker_LR.button_held
        if held_LR:
            held_ms = tracker_LR.held_ms
            slow_ms = min(DURATION_SLOW_ANGLE_MS, held_ms)
            fast_ms = max(0, held_ms - DURATION_SLOW_ANGLE_MS)
            delta_angle = (slow_ms * ANGLE_PER_MS_SLOW_F10 + \
                           fast_ms * ANGLE_PER_MS_FAST_F10 + 0x200) >> 10
            if held_LR == BUTTON_R:
                delta_angle = -delta_angle
            tr_display.set_angle_wd((self.angle_start_wd + delta_angle) % 360)

        if tracker_UD.just_held:
            self.scale_start_f10 = tr_display.scale_f10
        held_UD = tracker_UD.button_held
        if held_UD:
            if held_UD == BUTTON_U:
                scale_per_ms = SCALE_UP_PER_MS
            else:
                scale_per_ms = SCALE_DOWN_PER_MS
            coeff_scale_f10 = \
                int(math.pow(scale_per_ms, tracker_UD.held_ms) * 1024.0 + 0.5)
            scale_f10 = (coeff_scale_f10 * self.scale_start_f10 + 0x200) >> 10
            scale_clamped_f10 = \
                min(SCALE_MAX_F10, max(SCALE_MIN_F10, scale_f10))
            if scale_f10 != scale_clamped_f10:
                tracker_UD.reset()
            tr_display.set_scale_f10(scale_clamped_f10)

class FrameHandlerMenuScreen:
    def __init__(self, lines):
        self.lines = lines
        self.i_line_selected = None
        for i_line in range(len(self.lines)):
            if not self.lines[i_line][1] is None:
                self.i_line_selected = i_line
                break

    def _step_selected(self, incr):
        if self.i_line_selected is None:
            return
        num_lines = len(self.lines)
        for k in range(num_lines):
            self.i_line_selected = (self.i_line_selected + incr) % num_lines
            if not self.lines[self.i_line_selected][1] is None:
                return

    def __call__(self, mgs):
        mask_just_pressed = mgs.mask_just_pressed
        mgs.display.fill(0)
        for i_line in range(len(self.lines)):
            y = i_line << 3
            label = self.lines[i_line][0]
            if isinstance(label, bytearray):
                b = label
                w = len(b)
                x = 36 - (w >> 1)
                mgs.display.blit(b, x, y, w, 8, -1, 0, 0)
            else:
                text = label
                w = (len(text) * 6)
                x = 36 - (w >> 1)
                mgs.display.drawText(text, x, y, 1)
            if i_line == self.i_line_selected:
                mgs.draw_action_arrow(x - 5, y + 3, 1)
                mgs.draw_action_arrow(x + w + 3, y + 3, -1)
        if (mask_just_pressed & BUTTON_A) and not self.i_line_selected is None:
            self.lines[self.i_line_selected][1](mgs)
        elif mask_just_pressed & (BUTTON_U | BUTTON_D):
            incr = 1 if mask_just_pressed & BUTTON_D else -1
            self._step_selected(incr)

def menu_op_play(mgs):
    if utils.save_data.i_level:
        lvl = utils.save_data.i_level + 1
        score_clamped = min(99, score_before_continue())
        menulist_play[4] = (f"(#{lvl}, {score_clamped})", None)
        mgs.frame_handler = FrameHandlerMenuScreen(menulist_play)
    else:
        menu_op_choose_new(mgs)

def menu_op_choose_new(mgs):
    mgs.load_level(0)
    mgs.continuous_play = True
    mgs.frame_handler = FrameHandlerLevelStart(mgs)

def menu_op_choose_continue(mgs):
    mgs.load_level(utils.save_data.i_level)
    mgs.continuous_play = True
    mgs.frame_handler = FrameHandlerLevelStart(mgs)

def menu_op_practice(mgs):
    mgs.load_level(0)
    mgs.continuous_play = False
    mgs.frame_handler = FrameHandlerLevelStart(mgs)

def menu_op_gfx(mgs):
    mgs.frame_handler = FrameHandlerMenuScreen(menulist_gfx_choose)

def apply_gfx(mgs, load_as_gray):
    utils.save_data.load_as_gray = load_as_gray
    utils.save_data.save()
    if utils.use_gray == load_as_gray:
        mgs.frame_handler = FrameHandlerAttract(mgs)
        return
    if utils.is_emulator:
        utils.use_gray = load_as_gray
        if load_as_gray:
            mgs.display.enableGrayscale()
        else:
            mgs.display.disableGrayscale()
        mgs.frame_handler = FrameHandlerAttract(mgs)
    else:
        mgs.frame_handler = FrameHandlerMenuScreen(menulist_gfx_confirm)

def menu_op_choose_gray(mgs):
    apply_gfx(mgs, True)

def menu_op_choose_bw(mgs):
    apply_gfx(mgs, False)

def menu_op_dismiss_warn(mgs):
    mgs.frame_handler = FrameHandlerMenuScreen(menulist_gfx_confirm)

menulist_home = [
    (bytes_logo, None),
    ("",         None),
    ("play",     menu_op_play),
    ("practice", menu_op_practice),
    ("graphics", menu_op_gfx),
]

menulist_play = [
    ("Play Game", None),
    ("",          None),
    ("new",       menu_op_choose_new),
    ("continue",  menu_op_choose_continue),
    ("",          None),
]

menulist_gfx_choose = [
    ("Set Graphics", None),
    ("",             None),
    ("grayscale",    menu_op_choose_gray),
    ("b & w",        menu_op_choose_bw),
]

menulist_gfx_confirm = [
    ("Choice saved", None),
    ("", None),
    ("Restart game", None),
    ("to apply", None),
]

ATTRACT_LVL_WIDTH = const(72)
ATTRACT_LVL_HEIGHT = const(25)
ATTRACT_LVL_XS_MID = const(36)
ATTRACT_LVL_YS_MID = const(22)
ATTRACT_ZOOM_MS = const(1000)
ATTRACT_TOTAL_MS = const(1200)

class FrameHandlerAttract:
    def __init__(self, mgs):
        c = mgs.chunk_data
        xw_range = c.xw_hi - c.xw_lo
        yw_range = c.yw_hi - c.yw_lo
        scale_x_f10 = (ATTRACT_LVL_WIDTH << 10) // xw_range
        scale_y_f10 = (ATTRACT_LVL_HEIGHT << 10) // yw_range
        self.scale0_f10 = min(scale_x_f10, scale_y_f10) * 2
        self.scale1_f10 = self.scale0_f10 // 30
        self.scale_f10 = self.scale0_f10
        self.angle_f10 = 0
        self.xw_mid_f10 = (c.xw_lo << 10) + (xw_range << 9)
        self.yw_mid_f10 = (c.yw_lo << 10) + (yw_range << 9)
        self.animate_out = False
        self.animate_ms = 0

    def __call__(self, mgs):
        mask_just_pressed = mgs.mask_just_pressed
        mgs.display.fill(0)
        mgs.tr_display.set_angle_wd((self.angle_f10 + 0x200) >> 10)
        mgs.tr_display.set_scale_f10(self.scale_f10)
        mgs.tr_display.set_translate_map_world_to_screen_f10(
            self.xw_mid_f10, self.yw_mid_f10,
            ATTRACT_LVL_XS_MID << 10, ATTRACT_LVL_YS_MID << 10)
        mgs.draw_level()
        mgs.draw_hole()
        mgs.draw_ball()
        buf0 = mgs.display.display.buffer
        buf1 = mgs.display.display.shading
        for i in range(72):
            buf0[i] = (buf0[i] & invmask_logo[i]) | bytes_logo[i]
            buf1[i] &= invmask_logo[i]
            buf0[288 + i] = \
                (buf0[288 + i] & invmask_footer[i]) | bytes_footer[i]
            buf1[288 + i] &= invmask_footer[i]
        if mask_just_pressed:
            self.animate_out = True
        self.angle_f10 += mgs.delta_ms * 20
        if self.animate_out:
            self.animate_ms += mgs.delta_ms
            if self.animate_ms > ATTRACT_TOTAL_MS:
                mgs.frame_handler = FrameHandlerMenuScreen(menulist_home)
                return
            linear_f10 = (self.animate_ms << 10) // ATTRACT_ZOOM_MS
            c_f10 = smoothstep_f10(linear_f10)
            s_f20 = c_f10 * self.scale1_f10 + (1024 - c_f10) * self.scale0_f10
            self.scale_f10 = (s_f20 + 0x200) >> 10

XS_BALL_AIM = const(15)
YS_BALL_AIM = const(20)

START_LVL_XS_MID = const(36)
START_LVL_YS_MID = const(24)
START_LVL_WIDTH = const(70)
START_LVL_HEIGHT = const(28)

START_ANIMATION_MS = const(1500)

class FrameHandlerLevelStart:
    def __init__(self, mgs):
        tr_display = mgs.tr_display
        ball = mgs.ball
        c = mgs.chunk_data

        xw_range = c.xw_hi - c.xw_lo
        yw_range = c.yw_hi - c.yw_lo
        scale_x_f10 = (START_LVL_WIDTH << 10) // xw_range
        scale_y_f10 = (START_LVL_HEIGHT << 10) // yw_range
        self.scale0_f10 = min(scale_x_f10, scale_y_f10)
        self.scale1_f10 = 1024
        tr_display.set_angle_wd(0)
        tr_display.set_scale_f10(self.scale0_f10)
        tr_display.set_translate_map_world_to_screen_f10(
            (c.xw_lo << 10) + (xw_range << 9),
            (c.yw_lo << 10) + (yw_range << 9),
            START_LVL_XS_MID << 10, START_LVL_YS_MID << 10)
        self.xs0_f10, self.ys0_f10 = tr_display.world_to_screen_f10(
            ball.xw_f10, ball.yw_f10)
        self.xs1_f10 = XS_BALL_AIM << 10
        self.ys1_f10 = YS_BALL_AIM << 10
        self.show_banner = True
        self.animate_ms = 0

    def __call__(self, mgs):
        mask_just_pressed = mgs.mask_just_pressed
        mgs.display.fill(0)
        mgs.draw_level()
        mgs.draw_hole()
        mgs.draw_ball()
        if self.show_banner:
            mgs.display.drawFilledRectangle(0, 0, 72, 8, 0)
            hole = mgs.i_level + 1
            par = mgs.level.par
            mgs.display.drawText("Hole   Par  ", 0, 0, 1)
            mgs.display.drawText(str(hole), 30, 0, 1)
            mgs.display.drawText(str(par), 66, 0, 1)
            if not mgs.continuous_play:
                mgs.draw_action_arrow(3, 20, -1)
                mgs.draw_action_arrow(68, 20, 1)
                if mask_just_pressed & BUTTON_R:
                    mgs.load_level((mgs.i_level + 1) % len(levels.levels))
                    mgs.frame_handler = FrameHandlerLevelStart(mgs)
                elif mask_just_pressed & BUTTON_L:
                    mgs.load_level((mgs.i_level - 1) % len(levels.levels))
                    mgs.frame_handler = FrameHandlerLevelStart(mgs)
            if mask_just_pressed & (BUTTON_A | BUTTON_B):
                self.show_banner = False
        else:
            tr_display = mgs.tr_display
            ball = mgs.ball
            animate_ms = self.animate_ms + mgs.delta_ms
            self.animate_ms = animate_ms
            frac_animation_f10 = (animate_ms << 10) // START_ANIMATION_MS
            c_f10 = smoothstep_f10(frac_animation_f10)
            scale_f20 = c_f10 * self.scale1_f10 + \
                        (1024 - c_f10) * self.scale0_f10
            tr_display.set_scale_f10((scale_f20 + 0x200) >> 10)
            xs_f20 = c_f10 * self.xs1_f10 + (1024 - c_f10) * self.xs0_f10
            ys_f20 = c_f10 * self.ys1_f10 + (1024 - c_f10) * self.ys0_f10
            tr_display.set_translate_map_world_to_screen_f10(
                ball.xw_f10, ball.yw_f10,
                (xs_f20 + 0x200) >> 10, (ys_f20 + 0x200) >> 10)
            if animate_ms > START_ANIMATION_MS:
                mgs.frame_handler = FrameHandlerAim(mgs)

BALL_SPEED_AIM_F20 = const(50 << 10)
BALL_SPEED_VIS_LEN_W = const(8)

class FrameHandlerAim:
    def __init__(self, mgs, rs_controller=None):
        if rs_controller is None:
            rs_controller = RotationScaleController()
        self.rs_controller = rs_controller
        self._reset_ball_velocity(mgs)
        mgs.translate_ball_to_screen(XS_BALL_AIM, YS_BALL_AIM)

    def _reset_ball_velocity(self, mgs):
        mgs.ball.reset_velocity_wd_f20(-mgs.tr_display.angle_wd % 360,
                                       BALL_SPEED_AIM_F20)

    def _draw_ball_velocity(self, mgs):
        len_s = (mgs.tr_display.scale_f10 * BALL_SPEED_VIS_LEN_W + 0x200) >> 10
        mgs.display.drawLine(XS_BALL_AIM, YS_BALL_AIM,
                             XS_BALL_AIM + len_s, YS_BALL_AIM, 1)

    def __call__(self, mgs):
        mask_just_pressed = mgs.mask_just_pressed
        mgs.display.fill(0)
        mgs.draw_level()
        mgs.draw_hole()
        self._draw_ball_velocity(mgs)
        mgs.draw_ball()
        self.rs_controller.control(mgs)
        mgs.translate_ball_to_screen(XS_BALL_AIM, YS_BALL_AIM)
        self._reset_ball_velocity(mgs)
        mgs.draw_hud()
        if mask_just_pressed & BUTTON_A:
            mgs.frame_handler = FrameHandlerPower(mgs)

POWER_SPEED_MIN_F10 = const(20)
POWER_SPEED_MAX_F10 = const(150)
DELTA_POWER_PER_MS_F10 = const(2)

class FrameHandlerPower:
    def __init__(self, mgs):
        self.active_ms = 0
        self.power_frac_f10 = 0

    @micropython.native
    def _update_shot_power(self, mgs):
        self.active_ms += mgs.delta_ms
        p_accum_mod_2_f10 = (self.active_ms * DELTA_POWER_PER_MS_F10) & 0x7ff
        if p_accum_mod_2_f10 < 1024:
            self.power_frac_f10 = p_accum_mod_2_f10
        else:
            self.power_frac_f10 = 2048 - p_accum_mod_2_f10

    @micropython.native
    def _draw_shot_power(self, mgs):
        display = mgs.display
        display.drawRectangle(1, 9, 8, 30, 1)
        display.drawFilledRectangle(2, 10, 6, 28, 0)
        LEN_BAR_MAX = const(26)
        len_bar = max(1, (self.power_frac_f10 * LEN_BAR_MAX + 0x200) >> 10)
        display.drawFilledRectangle(
            3, 11 + LEN_BAR_MAX - len_bar, 4, len_bar, 1)

    @micropython.native
    def _set_ball_velocity(self, mgs):
        power_frac_f10 = self.power_frac_f10
        v_w_per_ms_f20 = POWER_SPEED_MAX_F10 * power_frac_f10 + \
                         POWER_SPEED_MIN_F10 * (1024 - power_frac_f10)
        mgs.ball.reset_velocity_wd_f20(mgs.ball.v_angle_wd, v_w_per_ms_f20)

    def __call__(self, mgs):
        mask_just_pressed = mgs.mask_just_pressed
        mgs.display.fill(0)
        mgs.draw_level()
        mgs.draw_hole()
        mgs.draw_ball()
        self._update_shot_power(mgs)
        self._draw_shot_power(mgs)
        self._set_ball_velocity(mgs)
        mgs.draw_hud()
        if mask_just_pressed & BUTTON_A:
            mgs.frame_handler = FrameHandlerRoll(mgs)

class FrameHandlerRoll:
    def __init__(self, mgs, rs_controller=None):
        if rs_controller is None:
            rs_controller = RotationScaleController()
        self.rs_controller = rs_controller

    def __call__(self, mgs):
        mgs.display.fill(0)
        mgs.draw_level()
        mgs.draw_hole()
        mgs.draw_ball()
        self.rs_controller.control(mgs)
        mgs.advance_ball()
        mgs.translate_ball_to_screen(XS_BALL_AIM, YS_BALL_AIM)
        mgs.draw_hud()
        if mgs.ball.is_stopped:
            if mgs.ball.in_hole:
                if mgs.continuous_play:
                    utils.save_data.arr_level_strokes[mgs.i_level] = \
                        min(255, mgs.num_strokes + 1)
                    utils.save_data.i_level = \
                        (mgs.i_level + 1) % len(levels.levels)
                    utils.save_data.save()
                mgs.frame_handler = FrameHandlerLevelEnd(mgs)
            elif mgs.ball.in_water:
                mgs.frame_handler = FrameHandlerReset(mgs, self.rs_controller)
            else:
                mgs.ball.update_last_shot()
                mgs.num_strokes += 1
                mgs.frame_handler = FrameHandlerAim(mgs, self.rs_controller)

RESET_FREEZE_MS = const(500)
RESET_ANIMATION_MS = const(1500)

class FrameHandlerReset:
    def __init__(self, mgs, rs_controller=None):
        if rs_controller is None:
            rs_controller = RotationScaleController()
        self.rs_controller = rs_controller
        self.xw_0_f10 = mgs.ball.xw_f10
        self.yw_0_f10 = mgs.ball.yw_f10
        self.xw_1_f10 = mgs.ball.xw_last_shot_f10
        self.yw_1_f10 = mgs.ball.yw_last_shot_f10
        self.animate_ms = -RESET_FREEZE_MS

    def __call__(self, mgs):
        mgs.display.fill(0)
        mgs.draw_level()
        mgs.draw_hole()
        mgs.draw_hud()
        self.rs_controller.control(mgs)
        self.animate_ms += mgs.delta_ms
        frac_animation_f10 = (self.animate_ms << 10) // RESET_ANIMATION_MS
        c1_f10 = smoothstep_f10(frac_animation_f10)
        c0_f10 = 1024 - c1_f10
        xw_f10 = (c0_f10 * self.xw_0_f10 + c1_f10 * self.xw_1_f10 + 0x200) >> 10
        yw_f10 = (c0_f10 * self.yw_0_f10 + c1_f10 * self.yw_1_f10 + 0x200) >> 10
        mgs.tr_display.set_translate_map_world_to_screen_f10(
            xw_f10, yw_f10, XS_BALL_AIM << 10, YS_BALL_AIM << 10)
        if self.animate_ms > RESET_ANIMATION_MS:
            mgs.ball.move_to_last_shot()
            mgs.num_strokes += 2
            mgs.frame_handler = FrameHandlerAim(mgs, self.rs_controller)

END_LEVEL_BANNER_MS = const(2000)

class FrameHandlerLevelEnd:
    def __init__(self, mgs):
        strokes = mgs.num_strokes + 1
        par = mgs.level.par
        diff = strokes - par
        self.animate_ms = 0
        if strokes == 1:
            self.message = "Hole in One!"
        elif diff > 3:
            self.message = "   Ouch...  "
        elif diff == 3:
            self.message = "Triple Bogey"
        elif diff == 2:
            self.message = "Double Bogey"
        elif diff == 1:
            self.message = "   Bogey    "
        elif diff == 0:
            self.message = "    Par     "
        elif diff == -1:
            self.message = "   Birdie   "
        elif diff == -2:
            self.message = "   Eagle    "
        elif diff == -3:
            self.message = " Albatross  "
        else:
            self.message = "   Nice!    "

    def __call__(self, mgs):
        mgs.display.fill(0)
        mgs.draw_level()
        mgs.draw_hole()
        mgs.draw_ball()
        mgs.draw_hud()
        mgs.display.drawLine(0, 15, 72, 15, 1)
        mgs.display.drawLine(0, 25, 72, 25, 1)
        mgs.display.drawFilledRectangle(0, 16, 72, 9, 0)
        mgs.display.drawText(self.message, 0, 17, 1)
        self.animate_ms += mgs.delta_ms
        if self.animate_ms > END_LEVEL_BANNER_MS:
            if mgs.continuous_play and mgs.i_level < len(levels.levels) - 1:
                mgs.load_level((mgs.i_level + 1) % len(levels.levels))
                mgs.frame_handler = FrameHandlerLevelStart(mgs)
            elif mgs.continuous_play:
                mgs.frame_handler = FrameHandlerScoreCard(mgs)
            else:
                mgs.frame_handler = FrameHandlerMenuScreen(menulist_home)

def encode_scorecard_num(n):
    if n < -9:
        return ":)"
    elif n > 99:
        return ":("
    else:
        return f"{n:>2}"

class FrameHandlerScoreCard:
    def __init__(self, mgs):
        num_levels = len(levels.levels)
        width_score_px = 6 * 2 * num_levels - 1
        self.max_scroll_px_f10 = (width_score_px - 36) << 10
        self.scroll_px_f10 = 0

        self.str_level = ""
        self.str_par = ""
        self.str_strokes = ""
        self.str_score = ""
        sum_par = 0
        sum_strokes = 0
        sum_score = 0
        score = 0
        for i_level in range(num_levels):
            level = i_level + 1
            par = levels.levels[i_level].par
            strokes = utils.save_data.arr_level_strokes[i_level]
            score = strokes - par
            self.str_level += encode_scorecard_num(level)
            self.str_par += encode_scorecard_num(par)
            self.str_strokes += encode_scorecard_num(strokes)
            self.str_score += encode_scorecard_num(score)
            sum_par += par
            sum_strokes += strokes
            sum_score += score
        self.str_sum_par = encode_scorecard_num(sum_par)
        self.str_sum_strokes = encode_scorecard_num(sum_strokes)
        self.str_sum_score = encode_scorecard_num(sum_score)

    def __call__(self, mgs):
        mgs.display.fill(0)
        delta_scroll_px_f10 = mgs.delta_ms * 50
        if mgs.mask_pressed & BUTTON_R:
            self.scroll_px_f10 += delta_scroll_px_f10
        elif mgs.mask_pressed & BUTTON_L:
            self.scroll_px_f10 -= delta_scroll_px_f10
        self.scroll_px_f10 = \
            min(self.max_scroll_px_f10, max(0, self.scroll_px_f10))
        scroll_px = (self.scroll_px_f10 + 0x200) >> 10
        x = 20 - scroll_px
        mgs.display.drawText(self.str_level, x, 1, 1)
        mgs.display.drawText(self.str_par, x, 11, 1)
        mgs.display.drawText(self.str_strokes, x, 21, 1)
        mgs.display.drawText(self.str_score, x, 31, 1)
        mgs.display.drawFilledRectangle(0, 0, 20, 40, 0)
        mgs.display.drawFilledRectangle(56, 0, 72, 40, 0)
        mgs.display.drawLine(0, 9, 72, 9, 1)
        mgs.display.drawLine(0, 19, 72, 19, 1)
        mgs.display.drawLine(0, 29, 72, 29, 1)
        mgs.display.drawLine(58, 0, 58, 40, 1)
        mgs.display.drawText(" # ", 1, 1, 1)
        mgs.display.drawText("Par", 1, 11, 1)
        mgs.display.drawText("Str", 1, 21, 1)
        mgs.display.drawText("Scr", 1, 31, 1)
        mgs.display.drawText(self.str_sum_par, 60, 11, 1)
        mgs.display.drawText(self.str_sum_strokes, 60, 21, 1)
        mgs.display.drawText(self.str_sum_score, 60, 31, 1)
        mgs.draw_action_arrow(65, 4, 1)
        if mgs.mask_just_pressed & (BUTTON_A | BUTTON_B):
            mgs.frame_handler = FrameHandlerAttract(mgs)
