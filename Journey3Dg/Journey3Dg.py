# This is a small loader stub to
# a) check version
# b) show button usage
# c) hide the import/parse/init time for the larger main file

# Please take a look at Journey3Dg_main.py for the main() attraction

# Note that this version is tidied up and stripped of comments for the arcade.

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


from micropython import kbd_intr
from ssd1306 import SSD1306_SPI
from utime import sleep_ms, ticks_ms, ticks_diff
from machine import Pin, SPI, freq, soft_reset
from framebuf import FrameBuffer, MONO_VLSB
from os import uname
from gc import collect

kbd_intr(-1)
freq(280000000)

display = SSD1306_SPI(72, 40, SPI(0, sck=Pin(18), mosi=Pin(19)), dc=Pin(17), res=Pin(20), cs=Pin(16))

def check_upython_version(major, minor, revision):
    up_ver = [int(s) for s in uname().release.split('.')]
    if up_ver[0] > major:
        return True
    if up_ver[0] == major:
        if up_ver[1] > minor:
            return True
        if up_ver[1] == minor:
            return up_ver[2] >= revision
    return False

def fade_in():
    sleep_ms(28)
    for i in range(8):
        display.contrast(1 << i)
        sleep_ms(28)
        for j in range(i):
            display.contrast((1 << i) | (1 << j))
            sleep_ms(28)
    display.contrast(127)

@micropython.native
def fade_out():
    global display, t0
    sleep_ms(2800 - ticks_diff(ticks_ms(), t0))
    for i in range(7, -1, -1):
        for j in range(i-1, -1, -1):
            if j >= 0:
                display.contrast((1 << i) | (1 << j))
            else:
                display.contrast(1 << i)
            sleep_ms(40)
    display.contrast(0)
    sleep_ms(40)
    for i in range(360):
        display.buffer[i] = 0
    display.show()
    display.contrast(127)
    sleep_ms(200)
    display = None


def emu_check():
    try:
        import emulator
    except ImportError:
        return True
    import thumby
    thumby.display.fill(0)
    thumby.display.drawText('Cannot run', 6, 3, 1)
    thumby.display.drawText('  in the', 6, 15, 1)
    thumby.display.drawText(' emulator', 6, 27, 1)
    thumby.display.display.show()
    return False


def version_check():
    if not check_upython_version(1, 19, 1):
        import thumby
        thumby.display.fill(0)
        thumby.display.drawText('Needs v1.19', 0, 0, 1)
        thumby.display.drawText('Pls update', 0, 13, 1)
        thumby.display.drawText('Thumby using', 0, 23, 1)
        thumby.display.drawText('Code Editor', 0, 33, 1)
        thumby.display.display.show()
        while not thumby.inputPressed():
            sleep_ms(1)
        return False
    return True


def start():
    intro = bytearray((b'\x00\x00\x00\x00\x00@\x80\x82~\x02\x00p\x88\x88\x88p\x00x\x80\x80@\xf8\x00\xf8\x10\x08\x08\x10'
                        b'\x00\xf8\x10\x08\x08\xf0\x00p\xa8\xa8\xa80\x00\x18\xa0\xa0\xa0x\x00\x00\x00B\x82\x8a\x96b\x00'
                        b'\xfe\x82\x82D8\x00\x00\x10(\xa8\xa8x\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x84\x84\x04\x04'
                        b'\x04\x04\x04\x04\x04\x04\x04\x04\x04\x84D\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04'
                        b'\x04\x04D\x84\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\xc4\x04\x04\x04'
                        b'\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x04\x00\x00\x00\x00\x00\x00\x06\x86\x9f\x9f\x06'
                        b'\x06\x00\x00\t\x00\x00\x00\x00\x00\x07\x08\x10\x00\x00\x0f\x10\x10\x08\x1f\x00\x1f\x02\x01\x01'
                        b'\x1e\x00\x00\x90\x08\x07\x00\x00\x1f\x01\x06\x01\x1e\x00\x0f\x90\x10\x08\x1f\x00\x01\x0f\x11'
                        b'\x10\x08\x00\x0e\x15\x15\x15\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x08\x08\x08?'
                        b'\x00\x00\x00\x12\x00\x00\x00\x00>\x04\x02\x02<\x00\x1c***\x0c\x00"\x14\x08\x14"\x00\x02\x1f" '
                        b'\x10\x00\x00\x00\x00\x00\x00\x00\x02\x1f" \x10\x00\x1e  \x10>\x00>\x04\x02\x02<\x00\x1c***\x0c'
                        b'\x00\x00\x00\x00\x00\x00\x7fIII6\x00\x00\x00$\x00\x00\x00\x008TTT\x18\x00D(\x10(D\x00\x00D}@\x00'
                        b'\x00\x04?D@ \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    display.contrast(0)
    display.buffer[:] = intro
    intro = None
    display.show()
    fade_in()

def end():
    global display
    collect()
    display = SSD1306_SPI(72, 40, SPI(0, sck=Pin(18), mosi=Pin(19)), dc=Pin(17), res=Pin(20), cs=Pin(16))
    fb = FrameBuffer(display.buffer, 72, 40, MONO_VLSB)
    fb.fill(0)
    display.show()
    display.contrast(0)
    sleep_ms(200)
    fb.text('End', 26, 16, 1)
    display.show()
    fade_in()
    sleep_ms(800)


if emu_check():
    if version_check():
        start()

        t0 = ticks_ms()

        check_upython_version = None
        version_check = None
        emu_check = None
        start = None
        collect()

        exec('''
from Games.Journey3Dg.Journey3Dg_main import main
main(fade_out)
''', {'fade_out': fade_out})

        end()

    if __name__ != '__main__':
        soft_reset()
