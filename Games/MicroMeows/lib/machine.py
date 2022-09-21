import pygame


def freq(f):
    print("machine.freq() called")

def reset():
    print("machine.reset() called")


class Pin:
    IN = 0
    OUT = 1
    PULL_UP = 2
    value = 0

    def __init__(self, pin_number, p2, p3):
        if pin_number == 3:     # A
            self.key = pygame.K_a
        elif pin_number == 5:   # D
            self.key = pygame.K_d
        elif pin_number == 4:   # W
            self.key = pygame.K_w
        elif pin_number == 6:   # S
            self.key = pygame.K_s
        elif pin_number == 24:  # RA
            self.key = pygame.K_RIGHT
        elif pin_number == 27:  # LA
            self.key = pygame.K_LEFT

    def value(self, set_to=None):
        if set_to != None:
            value = set_to
        else:
            value = int(pygame.key.get_pressed()[self.key])
            return value