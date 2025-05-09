# LCD Gallery
# (c) 2024 Lauren Croney
#
# Licensed Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0).
# See LICENSE.txt for details.
import time
import random
import gc
import thumby
import Games.LCDGallery.lcd as lcd
from Games.LCDGallery.lcd import Game, ScreenActor

# Screen position constants
PLATFORM_Y = const(24)
Y_JUMP = const(9)
Y_PLAYER = const(15)
Y_DEAD = const(34)
Y_CLIFF = const(24)
X1_1 = const(0)
X1_2 = const(6)
X2_1 = const(11)
X2_2 = const(16)
X3_1 = const(22)
X3_2 = const(28)
X4_1 = const(33)
X4_2 = const(38)
X5_1 = const(44)
X5_2 = const(50)
X6_1 = const(55)
X6_2 = const(60)
X7_1 = const(65)
X_HAT = const(55)
Y1_HAT = const(7)
Y2_HAT = const(15)
X_HP = const(50)


# Class representing the player
class Player(ScreenActor):
    # Constants
    POS_ALIVE_FIRST = const(0)  # Position: On left cliff
    POS_HAT = const(10)  # Platform with hat
    POS_ALIVE_LAST = const(12)  # On right cliff
    POS_DEAD_FIRST = const(13)  # First death position
    POS_DEAD_LAST = const(11)  # Last death position

    def __init__(self):
        super().__init__()
        self.has_item = False
        self.dead = False
        self.slot = 0  # Unlike position, this is to compare against platforms
        # Add screen elements
        bmp_man1_hat = \
            bytearray([204,237,72,128,72,237,204,1,0,0,1,0,0,1])  # noqa: E231 7x9
        bmp_man2_hat = \
            bytearray([228, 237, 72, 128, 72, 237, 204, 1, 0, 0, 1,0,0,1])  # noqa: E231 | 7x9
        bmp_man3_hat = \
            bytearray([236,237,72,128,72,237,236,1,0,0,1,0,0,1])  # noqa: E231 | 7x9
        bmp_man1 = \
            bytearray([207,239,72,128,72,239,207,1,0,0,1,0,0,1]) + bmp_man1_hat  # noqa: E231
        bmp_man2 = \
            bytearray([231,239,72,128,72,239,207,1,0,0,1,0,0,1]) + bmp_man2_hat  # noqa: E231
        bmp_man3 = \
            bytearray([239,239,72,128,72,239,239,1,0,0,1,0,0,1]) + bmp_man3_hat  # noqa: E231
        bmp_dead = bytearray([9,43,55,35,0,55,35,35,35])  # noqa: E231 9x6
        self.add(thumby.Sprite(7, 9, bmp_man1, X1_1, Y_PLAYER, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man2, X1_2, Y_JUMP, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man3, X2_1, Y_PLAYER, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man2, X2_2, Y_JUMP, 1, 1, 0))
        self.add(thumby.Sprite(7, 9, bmp_man1, X3_1, Y_PLAYER, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man2, X3_2, Y_JUMP, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man3, X4_1, Y_PLAYER, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man2, X4_2, Y_JUMP, 1, 1, 0))
        self.add(thumby.Sprite(7, 9, bmp_man1, X5_1, Y_PLAYER, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man2, X5_2, Y_JUMP, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man3, X6_1, Y_PLAYER, 1, 0, 0))
        self.add(thumby.Sprite(7, 9, bmp_man2, X6_2, Y_JUMP, 1, 1, 0))
        self.add(thumby.Sprite(7, 9, bmp_man1, X7_1, Y_PLAYER, 1, 0, 0))
        self.add(thumby.Sprite(9, 6, bmp_dead, X2_1, Y_DEAD, 1, 0, 0))
        self.add(thumby.Sprite(9, 6, bmp_dead, X3_1, Y_DEAD, 1, 0, 0))
        self.add(thumby.Sprite(9, 6, bmp_dead, X4_1, Y_DEAD, 1, 0, 0))
        self.add(thumby.Sprite(9, 6, bmp_dead, X5_1, Y_DEAD, 1, 0, 0))
        self.add(thumby.Sprite(9, 6, bmp_dead, X6_1, Y_DEAD, 1, 0, 0))

    # Set player state to dead
    def die(self):
        self.dead = True
        self.position = self.POS_ALIVE_LAST + self.slot  # Move to death pos

    # Reset the player character after a single life is lost
    def revive(self):
        self.position = 0
        self.slot = 0
        self.dead = False
        self.has_item = self.give_item()

    # Reset the player character for a new game after all lives are lost
    def resurrect(self):
        self.position = 0
        self.slot = 0
        self.dead = False
        self.give_item()

    # Mark player as carrying item and update frame
    def get_item(self):
        self.has_item = True
        for sprite in self._sprites:
            sprite.setFrame(1)

    # Mark player as not carrying item and update frame
    def give_item(self):
        self.has_item = False
        for sprite in self._sprites:
            sprite.setFrame(0)

    # Move player left. Return False if player can't move, True otherwise
    def left(self):
        if self.position == 2 and not self.has_item:
            return False  # can't return to left cliff without item
        if not self.dead and self.position > self.POS_ALIVE_FIRST:
            self.position -= 1
            if self.position % 2 == 0:
                self.slot -= 1  # only change slot on even positions
            return True
        return False

    # Move player right. Return False if player can't move, True otherwise
    def right(self):
        if not self.dead and self.position < 10:
            self.position += 1
            if self.position % 2 == 0:
                self.slot += 1
            return True
        return False

    @property
    def jumping(self):
        if self.position in [1, 3, 5, 7, 9, 11]:
            return True
        else:
            return False


# Class representing one of the platforms the player jumps on
class Platform(ScreenActor):
    def __init__(self, slot, x, enabled=True):
        super().__init__()
        self.slot = slot  # Associate with a player slot
        self.level = 0
        self.eroding = False  # Has the battery started eroding?
        self.enabled = enabled  # if false, the platform will not act

        # Create screen elements
        bmp_p1 = bytearray([15,15,15,15,15,15,15,15,15])  # noqa: E231 | 9x4
        bmp_p2 = bytearray([15,15,14,12,12,12,14,15,15])  # noqa: E231 | 9x4
        bmp_p3 = bytearray([15,14,12,8,8,8,12,14,15])  # noqa: E231 | 9x4
        bmp_p4 = bytearray([14,12,8,8,8,8,8,12,14])  # noqa: E231 | 9x4
        bmp_platform = bmp_p4 + bmp_p3 + bmp_p2 + bmp_p1
        self.add(thumby.Sprite(9, 4, bmp_platform, x, PLATFORM_Y, 1, 0, 0))

    # Erode platform or reset
    def tick(self):
        if self.enabled:
            if self.level == 3:
                self.level = 0
                self.eroding = False
            elif self.eroding is True:
                self.level += 1
        self._sprites[0].setFrame(self.level)  # Reflect lvl in frame

    # Set platform to eroding
    def erode(self):
        self.eroding = True


# Class representing the hat item the player gets
class Hat(ScreenActor):
    RAISED = const(1)
    LOWERED = const(0)

    def __init__(self):
        super().__init__()

        # Create screen elements
        bmp_hat = bytearray([4,5,4,6,4,5,4,7])  # noqa: E231 | 8x3
        self.add(thumby.Sprite(8, 3, bmp_hat, X_HAT, Y2_HAT, 1, 0, 0))
        self.add(thumby.Sprite(8, 3, bmp_hat, X_HAT, Y1_HAT, 1, 0, 0))

    # Toggle raised or lowered state of hat
    def toggle(self):
        if self._pos == self.RAISED:
            self._pos = self.LOWERED
        else:
            self._pos = self.RAISED


# Game class
class Skywalk(Game):
    # Constants
    ACTION_LEFT = const(-1)
    ACTION_JUMP_LEFT = const(-2)
    ACTION_RIGHT = const(1)
    ACTION_JUMP_RIGHT = const(2)
    ACTION_NONE = const(0)
    HAT_RATE = const(40)  # rate of hat movement
    SCORE_HAT = const(3)  # points given for getting hat
    SCORE_BONUS_MAX = const(15)  # max bonus points for returning to cliff
    SCORE_BONUS_MIN = const(4)  # min bonus points for returning to cliff
    TIMEOUT_HAT = const(20)
    TIMEOUT_HAT_MIN = const(14)  # minimum time before hat can toggle
    TIMEOUT_CLIFF = const(20)
    SPEED_UP_MOD = const(40)
    SPEED_DOWN_MOD = const(200)
    EROSION_DEFAULT = const(72)  # initial erosion rate

    # Bitmaps
    bmp_cliff = bytearray([0,0,0,0,192,252,254,0,0,224,255,255,255,255])  # noqa: E231 | 7x16

    def __init__(self):
        super().__init__()
        self.action = self.ACTION_NONE
        self.platforms = [Platform(1, X2_1-1), Platform(2, X3_1-1),
                          Platform(3, X4_1-1, False), Platform(4, X5_1-1),
                          Platform(5, X6_1-1)]
        self.player = Player()
        self.hat = Hat()
        self.reset_game()

    def reset_game(self):
        super().reset_game()
        self.new_lives = [100, 200, 300, 600, 1000]  # scores at which new lives are granted
        self.erosion_rate = Skywalk.EROSION_DEFAULT  # rate of platform erosion
        self.bonus_points = 12  # bonus points for returning to cliff
        self.hat_timeout = Skywalk.TIMEOUT_HAT  # maximum ticks before hat moved
        self.cliff_timeout = Skywalk.TIMEOUT_CLIFF  # maximum ticks on cliff
        self.tick_speed = 460

    def death_anim(self):
        pos_temp = self.player.position
        self.drawframe()
        for i in range(0, 3):
            self.drawframe()
            lcd.play(lcd.sound_die)
            self.player.blank()
            self.drawframe()
            time.sleep(0.25)
            self.player.position = pos_temp

    def drawframe(self):
        thumby.display.fill(1)
        # Score
        thumby.display.drawText(str(self.score)[:5], 1, 1, 0)
        # Lives
        for i in range(0, self.lives):
            thumby.display.blit(lcd.bmp_heart, X_HP+(7*i), 1, 5, 5, -1, 0, 0)
        # Cliffs
        thumby.display.blit(Skywalk.bmp_cliff, 0, Y_CLIFF, 7, 16, -1, 0, 0)
        # Player
        thumby.display.drawSprite(self.player.sprite())
        # Hat
        if self.player.has_item is False:
            thumby.display.drawSprite(self.hat.sprite())
        # Platforms
        for p in self.platforms:
            thumby.display.drawSprite(p.sprite())

        thumby.display.update()

    # Update score and apply any effects
    def update_score(self, points):
        self.score += points
        rounded = int(self.score / 10) * 10  # round score to nearest 10
        # Update speed by score
        if self.score >= Skywalk.SPEED_DOWN_MOD and rounded % Skywalk.SPEED_DOWN_MOD == 0:
            self.erosion_rate = Skywalk.EROSION_DEFAULT
        elif self.score >= Skywalk.SPEED_UP_MOD and rounded % Skywalk.SPEED_UP_MOD == 0:
            self.erosion_rate += 10

    def gamelogic(self):
        # Reduce bonus the longer it takes to return to cliff
        if (self.gametick >= 10 and self.gametick % 10 == 0 and
                self.bonus_points > self.SCORE_BONUS_MIN and
                self.player.position > 0):
            self.bonus_points -= 1

        while time.ticks_diff(time.ticks_ms(), self.clock) < self.tick_speed:
            # While waiting for the next tick, scan for input
            # and do collision detection so the game stays responsive
            # Make sure player isn't jumping before taking input
            if (self.action != self.ACTION_JUMP_LEFT and
                    self.action != self.ACTION_JUMP_RIGHT):
                if thumby.buttonL.justPressed():
                    self.action = self.ACTION_LEFT
                elif thumby.buttonA.justPressed():
                    self.action = self.ACTION_RIGHT
                elif thumby.buttonD.pressed() and thumby.buttonB.pressed():
                    self.pause()
                    self.action = self.ACTION_NONE  # prevent movement after unpuase

            for p in self.platforms:
                # Player must be on a dropped platform AND not jumping
                if (self.player.slot == p.slot and p.level == 3 and
                        not self.player.jumping):
                    self.player.die()
                    self.death_anim()
                    self.lives -= 1
                    self.player.resurrect()
                    break

        # Give or take player item
        if (self.player.position == Player.POS_HAT and
                self.player.has_item is False and
                self.hat.position == Hat.LOWERED):
            self.player.get_item()
            self.update_score(Skywalk.SCORE_HAT)
            lcd.play(lcd.sound_item)
        elif self.player.position == 0 and self.player.has_item is True:
            self.player.give_item()
            self.update_score(self.bonus_points)
            self.bonus_points = Skywalk.SCORE_BONUS_MAX
            self.cliff_timeout = Skywalk.TIMEOUT_CLIFF
            for s in self.new_lives:
                if self.score > s and self.lives < lcd.MAX_LIVES:
                    self.lives += 1
                    self.new_lives.remove(s)
                    lcd.play(lcd.sound_life)
            lcd.play(lcd.sound_win)

        # Platforms and hat update every other tick
        if self.gametick % 2 == 0:
            if random.randint(0, 100) < self.erosion_rate:
                self.platforms[random.choice([0, 1, 3, 4])].erode()
            for p in self.platforms:
                p.tick()
            if (self.hat_timeout <= Skywalk.TIMEOUT_HAT_MIN and
                    random.randint(0, 100) < Skywalk.HAT_RATE) or self.hat_timeout == 0:
                self.hat.toggle()
                self.hat_timeout = Skywalk.TIMEOUT_HAT

        # The player can move on every tick
        if self.action == self.ACTION_RIGHT:
            moved = self.player.right()
            if moved:
                self.action = self.ACTION_JUMP_RIGHT
                lcd.play(lcd.sound_move)
            else:
                self.action = self.ACTION_NONE
        elif self.action == self.ACTION_LEFT:
            moved = self.player.left()
            if moved:
                self.action = self.ACTION_JUMP_LEFT
                lcd.play(lcd.sound_move)
            else:
                self.action = self.ACTION_NONE
        elif self.action == self.ACTION_JUMP_RIGHT:
            self.player.right()
            self.action = self.ACTION_NONE
            lcd.play(lcd.sound_tick)
        elif self.action == self.ACTION_JUMP_LEFT:
            self.player.left()
            self.action = self.ACTION_NONE
            lcd.play(lcd.sound_tick)
        elif (self.action == self.ACTION_NONE and self.player.position == 0
              and self.cliff_timeout == 0):
            self.action = self.ACTION_RIGHT
        else:
            lcd.play(lcd.sound_tick)

        # Update timing
        self.reset_clock()
        self.gametick += 1
        self.hat_timeout -= 1
        self.cliff_timeout -= 1
        if self.hat_timeout < 0:
            self.hat_timeout = Skywalk.TIMEOUT_HAT
        if self.cliff_timeout < 0:
            self.cliff_timeout = Skywalk.TIMEOUT_CLIFF

        gc.collect()
