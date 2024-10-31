# LCD Gallery
# (c) 2024 Lauren Croney
#
# Licensed Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0).
# See LICENSE.txt for details.
import time
import thumby

# Constants
MAX_LIVES = const(3)

# Shared bitmap assets
bmp_arrow_r = bytearray([31,31,0,17,27])  # noqa: E231 | 5x5
bmp_arrow_l = bytearray([27,17,0,31,31])  # noqa: E231 | 5x5
bmp_arrow_u = bytearray([27,25,24,25,27])  # noqa: E231 | 5x5
bmp_arrow_d = bytearray([27,19,3,19,27])  # noqa: E231 | 5x5
blank_5x5 = bytearray([31,31,31,31,31])  # noqa: E231 | 5x5
bmp_arrow_lr = bytearray([31,31,0,17,27])  # noqa: E231 | 5x5 (for mirroring)
bmp_arrow_ud = bytearray([27,25,24,25,27])  # noqa: E231 | 5x5 (for mirroring)
bmp_heart = bytearray([25,16,1,16,25])  # noqa: E231 | 5x5


# Sound engine
class Note:
    def __init__(self, pitch, duration):
        self.pitch = pitch
        self.duration = duration

    @property
    def value(self):
        return self.pitch, self.duration


class Sound:
    def __init__(self, notes, blocking=False, repetitions=1):
        self.notes = notes
        self.blocking = blocking
        self.repetitions = repetitions


def play(sound):
    for i in range(sound.repetitions):
        for note in sound.notes:
            if sound.blocking is True:
                thumby.audio.playBlocking(*note.value)
            else:
                thumby.audio.play(*note.value)


sound_tie = Sound([Note(1020, 30)])
sound_tick = Sound([Note(1000, 20)])
sound_move = Sound([Note(600, 30)])
sound_win = Sound([Note(1000, 20), Note(1500, 20), Note(1000, 20)], True, 3)
sound_score = Sound([Note(1600, 50)])
sound_item = Sound([Note(800, 30), Note(1000, 30)], True)
sound_die = Sound([Note(300, 500)], True)
sound_life = Sound([Note(700, 500), Note(800, 500), Note(1048, 500), Note(1396, 500)], True)
sound_pause = Sound([Note(523, 200), Note(1046, 200), Note(2093, 200)], True)
sound_unpause = Sound([Note(2093, 200), Note(1046, 200), Note(523, 200)], True)


class ScreenActor:
    bmp_blank = bytearray([1])

    def __init__(self):
        self._pos = 0
        self._sprites = []
        self._blank = thumby.Sprite(1, 1, bytearray([1]), 80, 80, 1, 0, 0)

    def add(self, sprite):
        self._sprites.append(sprite)

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, value):
        if value > len(self._sprites):
            raise Exception("invalid actor position")
        self._pos = int(value)

    def blank(self):
        self._pos = -1

    def sprite(self):
        try:
            if self._pos >= 0:
                return self._sprites[self._pos]
        except Exception as e:
            print(f"Exception in ScreenActor.sprite(): {e}")
            print(f"pos={self._pos} class={type(self)}")

        return self._blank  # return blank by default


class Game:
    # Parent class for games
    def __init__(self):
        thumby.display.setFPS(30)
        self.hiscore = 0
        self.score = 0
        self.lives = MAX_LIVES
        self.tick_speed = 500  # ms
        self.cycle_length = 1  # number of ticks per cycle
        self.clock = time.ticks_ms()  # start clock
        self.gametick = 1

    def reset_clock(self):
        self.clock = time.ticks_ms()  # reset clock

    def main_loop(self):
        thumby.display.setFont("/Games/LCDGallery/font_segment.bin", 5, 7, 1)
        while self.lives > 0:
            self.drawframe()
            self.gamelogic()
        self.game_over()

        self.reset_game()

    # Pause game and return True for resume, False for quit
    def pause(self):
        play(sound_pause)
        selection = 0
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        while True:
            thumby.display.fill(1)
            thumby.display.drawText("*PAUSED*", 13, 1, 0)
            thumby.display.drawText(" QUIT", 10, 14, 0)
            thumby.display.drawText(" RESUME", 10, 23, 0)

            if selection == 0:
                thumby.display.blit(bmp_arrow_lr, 1, 15, 5, 5, 1, 0, 0)
                if thumby.buttonA.justPressed():
                    self.lives = 0  # quit
                    return False
            elif selection == 1:
                thumby.display.blit(bmp_arrow_lr, 1, 24, 5, 5, 1, 0, 0)
                if thumby.buttonA.justPressed():
                    play(sound_unpause)
                    return True
            thumby.display.update()

            if thumby.buttonU.justPressed():
                selection = 0
            elif thumby.buttonD.justPressed():
                selection = 1

    def save_score(self):
        name = type(self).__name__
        thumby.saveData.setItem("highscore_"+name, self.hiscore)
        thumby.saveData.save()

    def game_over(self):
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        if self.score > self.hiscore:
            self.hiscore = self.score
            self.save_score()

        thumby.display.fill(1)
        thumby.display.drawText("GAME OVER", 1, 1, 0)
        thumby.display.drawText(f"SCORE={self.score}", 1, 9, 0)
        thumby.display.drawText(f"HI={self.hiscore}", 1, 17, 0)
        thumby.display.update()
        clock = time.ticks_ms()
        # Return to menu after a pause
        while time.ticks_diff(time.ticks_ms(), clock) < 2000:
            pass
        clock = time.ticks_ms()

    # Individual games will augment this
    def reset_game(self):
        self.score = 0
        self.player.resurrect()
        self.lives = MAX_LIVES
