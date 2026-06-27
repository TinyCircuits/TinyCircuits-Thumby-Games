# LCD Gallery
# (c) 2024 Lauren Croney
#
# Licensed Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0).
# See LICENSE.txt for details.
import gc
import time
import random
import thumby
import Games.LCDGallery.lcd as lcd
from Games.LCDGallery.lcd import Game, ScreenActor

# Screen positioning constants
Y_T_1 = const(9)  # top thing position
Y_T_2 = const(17)  # ...
Y_T_3 = const(23)  # ...
Y_T_4 = const(30)  # bottom thing position
X_T_1 = const(8)  # thing / paddle slot 1
X_T_2 = const(23)  # thing / paddle slot 2
X_T_3 = const(38)  # thing / paddle slot 3
X_T_4 = const(53)  # thing / paddle slot 4
X_BUBBLE = const(51)  # bubble x
Y_BUBBLE = const(7)  # bubble y
Y_PADDLE = const(32)  # paddle y


class Player(ScreenActor):
    DEFAULT_LIVES = 3  # Default number of lives for the player.
    MAX_POSITION = 3  # The maximum number of position slots

    def __init__(self):
        super().__init__()
        self.dead = False
        # Add screen elements
        bmp_paddleup = bytearray([247,247,247,247,247,247,247,247,247])  # noqa: E231 | 9x8
        bmp_paddledown = bytearray([239,223,191,191,191,191,191,223,239])  # noqa: E231 | 9x8
        bmp_paddle = bmp_paddledown + bmp_paddleup
        self.add(thumby.Sprite(9, 8, bmp_paddle, X_T_1-2, Y_PADDLE, 1, 0, 0))
        self.add(thumby.Sprite(9, 8, bmp_paddle, X_T_2-2, Y_PADDLE, 1, 0, 0))
        self.add(thumby.Sprite(9, 8, bmp_paddle, X_T_3-2, Y_PADDLE, 1, 0, 0))
        self.add(thumby.Sprite(9, 8, bmp_paddle, X_T_4-2, Y_PADDLE, 1, 0, 0))

    # Reset the player character for a new game after all lives are lost
    def resurrect(self):
        self.position = 0
        self.dead = False

    # Move the player left one position.
    # Return False if the player can't move more, True otherwise.
    def left(self):
        if self.position > 0:
            self.position -= 1
        else:
            return False

        return True

    # Return False if the player can't move more, True otherwise.
    def right(self):
        if self.position < Player.MAX_POSITION:
            self.position += 1
        else:
            return False

        return True


# The things the player is juggling.
class Thing(ScreenActor):
    # Constants
    DEF_FALLRATE = 33
    TIMER_MAX = 4  # Miss timer

    # Takes a list of screen objects, start position, and start dir.
    # Position 0 is the dropped, broken thing. After that each pos is higher
    def __init__(self, pos, dir, x, bmps, num=1):
        super().__init__()
        self._pos = pos  # Override default start position of 0
        self._pos_default = pos  # Save default position
        self._dir = dir  # direction: 1 = rising, -1 = falling
        self._dir_default = dir  # Save default direction
        self.frozen = False
        self.fallrate = Thing.DEF_FALLRATE
        self.num = num
        self.timer = Thing.TIMER_MAX
        # Create screen elements given list of bitmaps and x position
        self.add(thumby.Sprite(5, 5, bmps[0], x, Y_T_4, 1, 0, 0))
        self.add(thumby.Sprite(5, 5, bmps[1], x, Y_T_3, 1, 0, 0))
        self.add(thumby.Sprite(5, 5, bmps[2], x, Y_T_2, 1, 0, 0))
        self.add(thumby.Sprite(5, 5, bmps[3], x, Y_T_1, 1, 0, 0))

    # Go back up when hit
    def hit(self):
        self._dir = 1
        self.position += 1
        self.timer = Thing.TIMER_MAX

    # Reset the default position and dir for this thing.
    def reset(self):
        self.position = self._pos_default
        self._dir = self._dir_default
        self.timer = Thing.TIMER_MAX
        self.frozen = False

    def move(self):
        if self.frozen:
            return  # Don't move if item is frozen

        # If the peak has been reached, drop back down
        if self._dir == 1 and self.position == len(self._sprites)-1:
            self._dir = -1
        # Otherwise if it's in the air, there is a chance that it will fall anyway
        elif self._dir == 1 and self.position > 1 and random.randint(0, 100) < self.fallrate:
            self._dir = -1
        elif self.position == 0:
            self._dir = 0  # let the miss timer take care of this
        try:
            self.position += self._dir
        except Exception as e:
            print(f"exception {e} pos={self.position} dir={self._dir}")

    @property
    def about_to_fall(self):
        return self._dir == -1 and self.position == 0


# Class representing the bubble that holds thing 4
class Bubble(ScreenActor):
    def __init__(self):
        super().__init__()
        bmp_bubble = \
            bytearray([131,125,254,254,254,254,254,125,131,1,1,0,0,0,0,0,1,1])  # noqa: E231 | 9x9
        self.add(thumby.Sprite(9, 9, bmp_bubble, X_BUBBLE, Y_BUBBLE, 1, 0, 0))


# Game class
class Juggle(Game):
    # Constants
    NEW_LIVES = [100, 200, 400, 600, 1000]  # values to be tweaked
    SPEED_UP_MOD = const(5)  # When to speed up (modulo)
    SPEED_DOWN_MOD = const(100)  # When to speed down (modulo)
    FREEZE_RATE = const(25)  # How often bubble activates
    ACTION_LEFT = const(-1)
    ACTION_RIGHT = const(1)
    ACTION_NONE = const(0)
    CYCLE_LENGTH = const(16)  # ticks per cycle
    TICK_DEFAULT = const(145)  # default tick speed

    def __init__(self):
        super().__init__()

        self.action = Juggle.ACTION_NONE  # Set default player action

        # Thing bitmaps (5x5)
        bmps_thing1 = [bytearray([25, 4, 16, 4, 25]),
                       bytearray([21, 17, 10, 0, 17]),
                       bytearray([19, 4, 1, 4, 19]),
                       bytearray([17, 0, 10, 17, 21])]
        bmps_thing2 = [bytearray([14, 16, 30, 0, 14]),
                       bytearray([6, 21, 21, 21, 0]),
                       bytearray([14, 0, 15, 1, 14]),
                       bytearray([0, 21, 21, 21, 12])]
        bmps_thing3 = [bytearray([27, 1, 8, 1, 27]),
                       bytearray([17, 21, 0, 17, 27]),
                       bytearray([27, 16, 2, 16, 27]),
                       bytearray([27, 17, 0, 21, 17])]
        bmps_thing4 = [bytearray([7, 0, 30, 6, 0]),
                       bytearray([4, 4, 13, 13, 1]),
                       bytearray([0, 12, 15, 0, 28]),
                       bytearray([16, 22, 22, 4, 4])]

        self.things = [Thing(1, 1, X_T_1, bmps_thing1, 0),
                       Thing(1, 1, X_T_2, bmps_thing2, 1),
                       Thing(1, 1, X_T_3, bmps_thing3, 2),
                       Thing(1, 1, X_T_4, bmps_thing4, 3)]
        self.player = Player()
        self.bubble = Bubble()
        self.move_order = [1, 3, 2, 0]  # Order to move things
        self.tick_speed = Juggle.TICK_DEFAULT

    # Add speed reset to game reset
    def reset_game(self):
        super().reset_game()
        self.tick_speed = Juggle.TICK_DEFAULT

    # Handle the player dropping a thing
    def die(self):
        self.lives -= 1
        old_pos = self.player.position
        for i in range(4):
            if i % 2 == 0:
                self.player.blank()  # flash player off
            else:
                self.player.position = old_pos  # flash on
            self.drawframe()
            lcd.play(lcd.sound_die)
            time.sleep(0.25)

        for thing in self.things:
            thing.reset()  # Reset the positions

    def drawframe(self):
        thumby.display.fill(1)

        # Draw health
        for i in range(0, self.lives):
            thumby.display.blit(lcd.bmp_heart, 66, 1+(7*i), 5, 5, -1, 0, 0)
        # Draw player sprite
        thumby.display.drawSprite(self.player.sprite())
        # Draw thing sprites
        for i in range(4):
            thumby.display.drawSprite(self.things[i].sprite())
        # Draw bubble if first thing is frozen
        if self.things[3].frozen:
            thumby.display.drawSprite(self.bubble.sprite())

        # Draw score
        thumby.display.drawText(str(self.score)[:7], 1, 1, 0)
        thumby.display.update()

    def gamelogic(self):
        moved = False  # Player has moved

        # Set actions for next tick based on input
        if thumby.buttonL.justPressed():
            self.action = Juggle.ACTION_LEFT
        elif thumby.buttonA.justPressed():
            self.action = Juggle.ACTION_RIGHT
        elif thumby.buttonD.pressed() and thumby.buttonB.pressed():
            self.pause()

        if (self.score in self.NEW_LIVES) and (self.lives < lcd.MAX_LIVES):
            self.lives += 1  # Grant a new life at certain scores
            self.score += 10  # Advance score so only one life is granted
            lcd.play(lcd.sound_life)

        if self.action == Juggle.ACTION_LEFT:
            lcd.play(lcd.sound_move)
            self.player.left()
            moved = True
        elif self.action == Juggle.ACTION_RIGHT:
            lcd.play(lcd.sound_move)
            self.player.right()
            moved = True

        if moved is True:
            self.player.sprite().setFrame(0)  # Reset player sprite when moving
            moved = False
            self.action = Juggle.ACTION_NONE

        if time.ticks_diff(time.ticks_ms(), self.clock) > self.tick_speed:
            if self.gametick % 4 == 0:
                self.player.sprite().setFrame(0)  # Reset player sprite
                # Collision detection
                for i in range(4):
                    if self.things[i].about_to_fall and i == self.player.position:
                        # Collision
                        self.player.sprite().setFrame(1)  # Set sprite to hit frame
                        self.score += 1
                        self.things[i].hit()  # Bounce it back
                        lcd.play(lcd.sound_score)
                        # Adjust speed at different scores
                        if (self.score >= Juggle.SPEED_DOWN_MOD and
                                self.score % Juggle.SPEED_DOWN_MOD == 0):
                            self.tick_speed = Juggle.TICK_DEFAULT
                        elif (self.score >= Juggle.SPEED_UP_MOD and
                                self.score % Juggle.SPEED_UP_MOD == 0):
                            self.tick_speed -= 5
            elif self.gametick % 2 == 0:
                lcd.play(lcd.sound_tick)
                # Move things in a set order
                t = int((self.gametick % Juggle.CYCLE_LENGTH) / 4)
                self.things[self.move_order[t]].move()

                # Random chance to freeze or unfreeze last item
                if (random.randint(0, 100) < Juggle.FREEZE_RATE
                        and self.things[3].position == 3):
                    self.things[3].frozen = not self.things[3].frozen
            else:
                for i in range(4):
                    if self.things[i].position == 0:
                        self.things[i].timer -= 1

            # Check for miss
            for i in range(4):
                if (self.things[i].timer == 0 and i != self.player.position):
                    self.things[i].blank()
                    self.die()  # Miss

            self.gametick += 1
            self.reset_clock()
            gc.collect()
