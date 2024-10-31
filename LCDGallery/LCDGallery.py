# LCD Gallery
# (c) 2024 Lauren Croney
#
# Licensed Creative Commons Attribution-ShareAlike 3.0 (CC BY-SA 3.0).
# See LICENSE.txt for details.
import gc
import time
import thumby
import Games.LCDGallery.lcd as lcd
import Games.LCDGallery.skywalk as skywalk
import Games.LCDGallery.fight as fight
import Games.LCDGallery.juggle as juggle


class Launcher:
    VERSION = const(1.0)

    def __init__(self):
        t = time.ticks_us()
        self.skywalk = None
        self.fight = None
        self.juggle = None

        # Load high scores
        self.hiscore_skywalk = 0
        self.hiscore_fight = 0
        self.hiscore_juggle = 0
        if thumby.saveData.hasItem("highscore_Skywalk"):
            print("Loaded high scores")
            self.hiscore_skywalk = thumby.saveData.getItem("highscore_Skywalk")
        if thumby.saveData.hasItem("highscore_Juggle"):
            self.hiscore_juggle = thumby.saveData.getItem("highscore_Juggle")
        if thumby.saveData.hasItem("highscore_Fight"):
            self.hiscore_fight = thumby.saveData.getItem("highscore_Fight")
        t_diff = time.ticks_diff(time.ticks_us(), t)
        print('Launcher constructor took {:6.3f}ms'.format(t_diff/1000))

    def soundtest(self):
        selections = [('tick', lcd.sound_tick),
                      ('move', lcd.sound_move),
                      ('win', lcd.sound_win),
                      ('score', lcd.sound_score),
                      ('get_item', lcd.sound_item),
                      ('die', lcd.sound_die),
                      ('tie', lcd.sound_tie),
                      ('life', lcd.sound_life),
                      ('pause', lcd.sound_pause),
                      ('unpause', lcd.sound_unpause)]

        selection = 0
        while True:
            if thumby.buttonL.justPressed() and selection > 0:
                selection -= 1
            elif thumby.buttonR.justPressed() and selection < len(selections)-1:
                selection += 1
            elif thumby.buttonB.justPressed():
                self.titlescreen()
            elif thumby.buttonA.justPressed():
                lcd.play(selections[selection][1])

            thumby.display.fill(1)

            if selection > 0:  # left arrow
                thumby.display.blit(lcd.bmp_arrow_lr, 6, 16, 5, 5, 1, 1, 0)
            if selection < len(selections)-1:  # right arrow
                thumby.display.blit(lcd.bmp_arrow_lr, 65, 16, 5, 5, 1, 0, 0)
            thumby.display.drawText("B=Menu", 1, 1, 0)
            thumby.display.drawText(f"{selections[selection][0].center(10)}",
                                    6, 15, 0)
            thumby.display.update()

    def aboutpage(self):
        while True:
            thumby.display.fill(1)
            thumby.display.drawText("Lauren Rad", 1, 1, 0)
            thumby.display.drawText("(c) 2023", 1, 10, 0)
            thumby.display.drawText(f"v{Launcher.VERSION}", 1, 18, 0)
            thumby.display.update()
            if thumby.inputJustPressed():
                return

    def clearscores(self):
        # Clear high scores
        thumby.saveData.setItem("highscore_Skywalk", 0)
        thumby.saveData.setItem("highscore_Juggle", 0)
        thumby.saveData.setItem("highscore_Fight", 0)
        self.hiscore_skywalk = 0
        self.hiscore_juggle = 0
        self.hiscore_fight = 0
        if self.skywalk is not None:
            self.skywalk.hiscore = 0  # Game object's copy
        if self.fight is not None:
            self.fight.hiscore = 0
        if self.juggle is not None:
            self.juggle.hiscore = 0
        thumby.saveData.save()
        thumby.display.drawText("Cleared".center(10), 6, 25, 0)
        thumby.display.update()
        time.sleep(0.5)

    def titlescreen(self):
        t = time.ticks_us()
        selection = 0
        SELECT_SKYWALK = const(0)
        SELECT_FIGHT = const(1)
        SELECT_JUGGLE = const(2)
        SELECT_QUIT = const(3)
        SELECT_INFO = const(4)
        SELECT_SOUND_TEST = const(5)
        SELECT_CLEAR = const(6)
        # Duel is still called Fight internally in the code
        modes = ("Sky Quest", "Duel", "Juggle", "Quit", "Info", "Sound Test",
                 "Clear Saves")

        t_diff = time.ticks_diff(time.ticks_us(), t)
        print('Titlescreen took {:6.3f}ms to load'.format(t_diff/1000))
        while True:
            thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
            thumby.display.fill(1)
            thumby.display.drawText("LCD Gallery!".center(12), 1, 1, 0)
            thumby.display.drawText(f"{modes[selection].center(10)}", 6, 15, 0)

            if selection > 0:
                thumby.display.blit(lcd.bmp_arrow_lr, 1, 16, 5, 5, 1, 1, 0)  # left arrow
            if selection < len(modes)-1:
                thumby.display.blit(lcd.bmp_arrow_lr, 65, 16, 5, 5, 1, 0, 0)  # right arrow
            if selection == 0:
                thumby.display.drawText(f"Hi {self.hiscore_skywalk}", 1, 32, 0)
            elif selection == 1:
                thumby.display.drawText(f"Hi {self.hiscore_fight}", 1, 32, 0)
            elif selection == 2:
                thumby.display.drawText(f"Hi {self.hiscore_juggle}", 1, 32, 0)

            thumby.display.update()
            if thumby.buttonL.justPressed() and selection > 0:
                selection -= 1
            elif thumby.buttonR.justPressed() and selection < len(modes)-1:
                selection += 1

            if thumby.buttonA.justPressed():
                if selection == SELECT_SKYWALK:
                    if self.skywalk is None:
                        self.skywalk = skywalk.Skywalk()
                        self.skywalk.hiscore = self.hiscore_skywalk
                    self.skywalk.main_loop()
                    self.hiscore_skywalk = self.skywalk.hiscore  # update hiscore
                elif selection == SELECT_FIGHT:
                    if self.fight is None:
                        self.fight = fight.Fight()
                        self.fight.hiscore = self.hiscore_fight
                    self.fight.main_loop()
                    self.hiscore_fight = self.fight.hiscore
                elif selection == SELECT_JUGGLE:
                    if self.juggle is None:
                        self.juggle = juggle.Juggle()
                        self.juggle.hiscore = self.hiscore_juggle
                    self.juggle.main_loop()
                    self.hiscore_juggle = self.juggle.hiscore
                elif selection == SELECT_QUIT:
                    break
                elif selection == SELECT_INFO:
                    self.aboutpage()
                elif selection == SELECT_SOUND_TEST:
                    self.soundtest()
                elif selection == SELECT_CLEAR:
                    self.clearscores()

        print("Quitting...")
        thumby.reset()


# Begin launch
print("Launching LCD Gallery...")
gc.enable()
print(f"bytes free: {gc.mem_free()}")
thumby.saveData.setName("LCDGallery")
launcher = Launcher()
launcher.titlescreen()
