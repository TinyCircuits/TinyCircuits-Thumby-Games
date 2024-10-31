# LCD Gallery
# (c) 2024 Lauren Croney
#
# Licensed Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0).
# See LICENSE.txt for details.

import thumby
import time
import random
import Games.LCDGallery.lcd as lcd
from Games.LCDGallery.lcd import Game, ScreenActor

# Screen positioning constants
PLAYER_Y = const(20)
GUN_Y = const(23)
P_GUN_X = const(24)
C_GUN_X = const(39)
PLAYER_HP_X = const(1)
CPU_HP_X = const(67)
CPU_X = const(47)
FRAME_X = const(7)  # frame x offset from edge
FRAME_Y = const(9)
ARROWS_X = const(34)
ARROWS_Y = const(2)
PLAYER_X = const(19)


class Player(ScreenActor):
    # Actions
    NONE = const(0)
    DODGE = const(1)
    KO = const(2)
    SHOOT = const(3)
    MAX_HP = const(100)

    # Other constants
    POINT_VALUE = const(5)

    def __init__(self):
        super().__init__()
        self.num = -1
        self.action = Player.NONE
        self.hp = Player.MAX_HP

    # Set player stance to dodging
    def dodge(self):
        self.position = Player.DODGE

    # Set player stance to KO
    def ko(self):
        self.position = Player.KO

    # Reset player to default stance and action
    def reset(self):
        self.position = Player.NONE
        self.action = Player.NONE

    def resurrect(self):
        self.reset()
        self.hp = Player.MAX_HP


class Countdown(ScreenActor):
    # The countdown arrows
    def __init__(self, x, y):
        super().__init__()
        self.add(thumby.Sprite(5, 5, lcd.bmp_arrow_r, x, y, 1, 0, 0))
        self.add(thumby.Sprite(5, 5, lcd.blank_5x5, x, y, -1, 0, 0))

    def hide(self):
        self.position = 1

    def unhide(self):
        self.position = 0


class Fight(Game):
    # Some named constants for game behavior.
    CPU_REACT_MIN = const(420)  # minimum CPU reaction time; ms
    CPU_REACT_MAX = const(690)  # maximum CPU reaction time; ms
    COUNTDOWN_MIN = const(700)
    COUNTDOWN_MAX = const(1100)
    POINTS_WIN = const(40)  # bonus points for winning duel
    BONUS_HP = const(30)

    # Game states
    STATE_DEFAULT = const(-1)
    STATE_COUNTDOWN = const(0)
    STATE_FIGHT = const(1)
    STATE_CPU_DEAD = const(2)
    STATE_PLAYER_DEAD = const(3)

    # Shared bitmaps
    bmp_hp = bytearray([1,1,1,1])  # noqa: E231 | 4x3

    def __init__(self):
        super().__init__()
        self.player1_num = 0
        self.player2_num = 0
        self.state = Fight.STATE_DEFAULT
        # Countdown arrows
        self.arrows = [Countdown(ARROWS_X, ARROWS_Y),
                       Countdown(ARROWS_X+8, ARROWS_Y),
                       Countdown(ARROWS_X+16, ARROWS_Y),
                       Countdown(ARROWS_X+24, ARROWS_Y)]

        # The number frames
        bmp_frame = \
            bytearray([0,254,254,254,254,254,254,254,0,0,3,3,3,3,3,3,3,0])  # noqa: E231 | 9x11
        self.frame1 = ScreenActor()
        self.frame1.add(thumby.Sprite(9, 11, bmp_frame, FRAME_X, FRAME_Y, 1, 0, 0))
        self.frame1.blank()

        self.frame2 = ScreenActor()
        self.frame2.add(thumby.Sprite(9, 11, bmp_frame, thumby.display.width-FRAME_X-9,
                                      FRAME_Y, 1, 0, 0))
        self.frame2.blank()

        # Players
        bmp_man = bytearray([251,113,48,2,48,121,15,6,16,28,0,14])  # noqa: E231 | 6x13
        bmp_man_dodge = \
            bytearray([255,255,255,255,119,35,1,229,225,243,31,15,  # noqa: E231
                       7,16,12,4,16,28,31,31])  # noqa: E231 | 10x13
        bmp_ko = \
            bytearray([9,43,43,35,1,1,35,55,55,33,0,9,35])  # noqa: E231 | 13x6

        self.player = Player()
        self.player.add(thumby.Sprite(6, 13, bmp_man, PLAYER_X, PLAYER_Y, 1, 1, 0))
        self.player.add(thumby.Sprite(10, 13, bmp_man_dodge, PLAYER_X-10, PLAYER_Y, 1, 1, 0))
        self.player.add(thumby.Sprite(13, 6, bmp_ko, PLAYER_X-13, 33, 1, 1, 0))

        self.cpu = Player()
        self.cpu.add(thumby.Sprite(6, 13, bmp_man, CPU_X, PLAYER_Y, 1, 0, 0))
        self.cpu.add(thumby.Sprite(10, 13, bmp_man_dodge, CPU_X+6, PLAYER_Y, 1, 0, 0))
        self.cpu.add(thumby.Sprite(13, 6, bmp_ko, CPU_X+6, 33, 1, 0, 0))

        # Guns
        bmp_gun = bytearray([15,15,15,19,25,24,26,28,30,30])  # noqa: E231 | 10x5
        self.player_gun = ScreenActor()
        self.player_gun.add(thumby.Sprite(10, 5, bmp_gun, P_GUN_X, GUN_Y, 1, 0, 0))
        self.cpu_gun = ScreenActor()
        self.cpu_gun.add(thumby.Sprite(10, 5, bmp_gun, C_GUN_X, GUN_Y, 1, 1, 0))
        self.player_gun.blank()  # hide by default
        self.cpu_gun.blank()
        self.winner = None
        self.tick_speed = 1020  # tick speed override

    def reset_game(self):
        super().reset_game()
        self.cpu.resurrect()
        self.state = Fight.STATE_DEFAULT
        self.player_gun.blank()
        self.cpu_gun.blank()

    # Draw countdown anim; return True if need to restart countdown, False otherwise
    def countdown(self):
        self.frame1.blank()  # number frame 1 off
        self.frame2.blank()  # number frame 2 off
        thumby.display.drawSprite(self.frame1.sprite())
        thumby.display.drawSprite(self.frame2.sprite())
        for arrow in self.arrows:
            arrow.unhide()
            thumby.display.drawSprite(arrow.sprite())
        thumby.display.update()

        count_speed = random.uniform(Fight.COUNTDOWN_MIN, Fight.COUNTDOWN_MAX)
        arrow = 0
        clock = time.ticks_ms()
        while arrow < 4:
            if time.ticks_diff(time.ticks_ms(), clock) > count_speed:
                lcd.play(lcd.sound_move)
                self.arrows[arrow].hide()
                thumby.display.drawSprite(self.arrows[arrow].sprite())
                thumby.display.update()
                arrow += 1
                clock = time.ticks_ms()
            if thumby.buttonD.pressed and thumby.buttonB.pressed():
                p = self.pause()
                if p is False:
                    return True
                else:
                    self.drawframe()
                    return True

        return False

    def drawframe(self):
        thumby.display.fill(1)
        # Draw score
        thumby.display.setFont('/Games/LCDGallery/font_segment.bin', 5, 7, 1)
        thumby.display.drawText(str(self.score)[:5], 1, 1, 0)
        # Draw playfield and players
        thumby.display.drawSprite(self.player.sprite())
        thumby.display.drawSprite(self.cpu.sprite())
        thumby.display.drawSprite(self.player_gun.sprite())
        thumby.display.drawSprite(self.cpu_gun.sprite())

        # Draw BANG! text if gun is drawn
        thumby.display.setFont('/lib/font3x5.bin', 3, 5, 1)
        if self.player_gun.position == 0:
            thumby.display.drawText("bang!", PLAYER_X-2, PLAYER_Y-7, 0)
        if self.cpu_gun.position == 0:
            thumby.display.drawText("bang!", CPU_X-10, PLAYER_Y-7, 0)

        # Draw HP meters
        for i in range(int(self.player.hp/10)):
            thumby.display.blit(Fight.bmp_hp, PLAYER_HP_X, 36-(i*3), 4, 3, -1,
                                0, 0)
        if self.state != Fight.STATE_DEFAULT:
            for i in range(int(self.cpu.hp/10)):
                thumby.display.blit(Fight.bmp_hp, CPU_HP_X, 36-(i*3), 4, 3, -1,
                                    0, 0)

        if self.state == Fight.STATE_CPU_DEAD:
            thumby.display.setFont('/lib/font3x5.bin', 3, 5, 1)
            thumby.display.drawText("RIP", 41, 34, 0)
        elif self.state == Fight.STATE_PLAYER_DEAD:
            thumby.display.setFont('/lib/font3x5.bin', 3, 5, 1)
            thumby.display.drawText("RIP", 20, 34, 0)
        elif self.state == Fight.STATE_FIGHT:
            # Draw number frames
            self.frame1.position = 0  # number frame 1 on
            self.frame2.position = 0  # number frame 2 on
            thumby.display.drawSprite(self.frame1.sprite())
            thumby.display.drawSprite(self.frame2.sprite())
            # Draw nums
            thumby.display.setFont('/Games/LCDGallery/font_segment.bin', 5, 7, 1)
            thumby.display.drawText(str(self.player1_num), FRAME_X+2, FRAME_Y+2, 0)
            thumby.display.drawText(str(self.player2_num), thumby.display.width-FRAME_X-7,
                                    FRAME_Y+2, 0)
        thumby.display.update()

    def win(self, damage):
        self.cpu.hp -= (damage * 2)
        lcd.play(lcd.sound_win)
        if self.cpu.hp <= 0:
            self.state = Fight.STATE_CPU_DEAD
            # CPU death anim
            for i in range(0, 3):
                self.drawframe()
                lcd.play(lcd.sound_win)
                self.cpu.blank()
                self.drawframe()
                time.sleep(0.5)
                self.cpu.ko()
            self.state = Fight.STATE_DEFAULT
            self.cpu.blank()
            self.player_gun.blank()
            self.drawframe()

            self.score += Fight.POINTS_WIN
            self.cpu.hp = Player.MAX_HP

            # Restore 20 HP to player on win
            self.player.hp += Fight.BONUS_HP
            if self.player.hp > Player.MAX_HP:
                self.player.hp = Player.MAX_HP

    def lose(self, damage):
        self.player.hp -= (damage * 2)
        if self.player.hp <= 0:
            self.state = Fight.STATE_PLAYER_DEAD
            for i in range(0, 3):
                self.drawframe()
                lcd.play(lcd.sound_die)
                self.player.blank()
                self.drawframe()
                time.sleep(0.5)
                self.player.ko()

            self.lives = 0
        else:
            self.player.ko()
            lcd.play(lcd.sound_die)

    # add to player score
    def player_score(self, score):
        self.score += score

    # since the CPU opponent doesn't have a score, deduct from player score
    def cpu_score(self, score):
        self.score -= score
        if self.score < 0:
            self.score = 0

    def gamelogic(self):
        self.player.reset()
        self.cpu.reset()
        self.frame1.blank()
        self.frame2.blank()
        time.sleep(self.tick_speed/1000)
        acted = False  # Has anyone acted?
        self.player1_num = random.randint(0, 9)
        self.player2_num = random.randint(0, 9)
        self.player_gun.blank()
        self.cpu_gun.blank()

        # Do countdown; game can be paused during countdown
        self.state = Fight.STATE_COUNTDOWN
        self.drawframe()
        restart = self.countdown()
        if restart is True:
            return  # After unpausing, start over
        self.state = Fight.STATE_FIGHT
        self.drawframe()

        if self.lives == 0:
            return  # Exit if quit while paused

        cpu_reaction = random.randint(Fight.CPU_REACT_MIN, Fight.CPU_REACT_MAX)
        clock = time.ticks_ms()
        while not acted:
            # Special case: if both players drew a 0 then roll again
            if self.player1_num == 0 and self.player2_num == 0:
                lcd.play(lcd.sound_tie)
                time.sleep(0.5)
                return

            if thumby.buttonA.justPressed():
                self.player_gun.position = 0  # show player gun
                self.player.action = Player.SHOOT
                acted = True
                # Check if the hit was effective
                if self.player1_num >= self.player2_num:
                    self.cpu.ko()
                else:
                    self.cpu_gun.position = 0  # cpu will shoot back
                    self.drawframe()
                    self.player_gun.blank()
                    self.player.ko()
            elif thumby.buttonL.justPressed():
                self.player.dodge()
                self.player.action = Player.DODGE
                acted = True
            else:
                # If the CPU is done waiting, react
                if time.ticks_diff(time.ticks_ms(), clock) > cpu_reaction:
                    if self.player1_num > self.player2_num:
                        self.cpu.action = Player.DODGE
                        self.cpu.dodge()
                    # CPU will hit on equal numbers
                    elif self.player2_num >= self.player1_num:
                        self.cpu.action = Player.SHOOT
                        self.player.ko()
                        self.cpu_gun.position = 0  # show CPU gun
                    else:
                        self.cpu.action = Player.NONE
                    acted = True

        # Make sound for action
        lcd.play(lcd.sound_move)

        # Determine who won this matchup
        if self.player.action == Player.DODGE:
            # If the player dodged, the only thing that mattered is
            # if they needed to
            if self.player1_num < self.player2_num:
                self.win(0)
                self.score += 2  # successful player dodge
            elif self.player1_num == self.player2_num:
                # player dodged on a tie, no action
                lcd.play(lcd.sound_tie)
            else:
                self.player.ko()  # erroneous dodge, fall over and get hurt
                self.lose(8)
        elif self.player.action == Player.SHOOT:
            if not self.cpu.action == Player.DODGE:
                if self.player1_num >= self.player2_num:
                    self.win(self.player1_num)
                    self.score += 3  # successful player hit
                else:
                    self.lose(self.player2_num)  # unsuccessful player hit
        elif self.cpu.action == Player.SHOOT:
            self.lose(self.player2_num)  # successful CPU hit
