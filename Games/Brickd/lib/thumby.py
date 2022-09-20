import asyncio
import pygame
import time
import utime

# Add common but missing functions to time module (from redefined/recreated micropython module)
time.ticks_ms = utime.ticks_ms
time.ticks_us = utime.ticks_us
time.ticks_diff = utime.ticks_diff
time.sleep_ms = utime.sleep_ms


# See thumbyGraphics.__init__() for set_mode() call
pygame.init()
pygame.display.set_caption("Thumby game")

from thumbySprite import Sprite

from thumbyButton import buttonA, buttonB, buttonU, buttonD, buttonL, buttonR
from thumbyButton import inputPressed, inputJustPressed, dpadPressed, dpadJustPressed, actionPressed, actionJustPressed

from thumbyAudio import audio

from thumbyGraphics import display

