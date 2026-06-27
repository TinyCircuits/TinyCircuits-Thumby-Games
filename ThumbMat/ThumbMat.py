import random
import thumbyButton as buttons
from thumbyGraphics import display
Number = int
import time

times = None
moves = None
scramble = None
AoT = None
i = None
startTime = None
now = None
Ao5 = None
time2 = None
k = None

def __print_to_display__(message):
      message = str(message)
      display.fill(0)
      txt = [""]
      for line in message.split("\n"):
          for word in line.split(" "):
              next_len = len(txt[-1]) + len(word) + 1
              if next_len*display.textWidth + (next_len-1) > display.width:
                  txt += [""]
              txt[-1] += (" " if txt[-1] else "") + word
          txt += [""]
      for ln, line in enumerate(txt):
          display.drawText(line, 0, (display.textHeight+1)*ln, 1)
      display.display.show()



times = []
moves = ['R', "R'", 'L', "L'", 'U', "U'", 'D', "D'", 'B', "B'", 'F', "F'"]
scramble = ''.join([str(x) for x in [moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)], ', ', moves[int(random.randint(1, len(moves)) - 1)]]])
AoT = 0
i = 0
startTime = 0
now = 0
Ao5 = 0
while not (buttons.buttonB.justPressed() or buttons.buttonL.justPressed() or buttons.buttonR.justPressed() or buttons.buttonU.justPressed() or buttons.buttonD.justPressed() or buttons.buttonA.pressed()):
  __print_to_display__('Timer:^         AoT:<              Scramble:>               Ao5:v ')
while 1 == 1:
  i = 0
  __print_to_display__('Hold to start')
  while not i > 1000:
    if buttons.buttonR.justPressed():
      __print_to_display__(scramble)
      scramble = ''.join([str(x2) for x2 in [moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)], ', ', moves[int(random.randint(1, 12) - 1)]]])
    if buttons.buttonU.justPressed():
      __print_to_display__('Hold to start')
    if len(times) != 0:
      if buttons.buttonL.justPressed():
        k = 0
        for count in range(int(len(times))):
          k = (k if isinstance(k, Number) else 0) + 1
          AoT = AoT + times[int(k - 1)]
        AoT = AoT / (len(times) * 1000)
        __print_to_display__(''.join([str(x3) for x3 in ['Average of Total: ', AoT, 's']]))
      if buttons.buttonD.justPressed() and len(times) >= 5:
        Ao5 = Ao5 + times[int((len(times) + 0) - 1)]
        Ao5 = Ao5 + times[int((len(times) - 1) - 1)]
        Ao5 = Ao5 + times[int((len(times) - 2) - 1)]
        Ao5 = Ao5 + times[int((len(times) - 3) - 1)]
        Ao5 = Ao5 + times[int((len(times) - 4) - 1)]
        Ao5 = Ao5 / 5000
        __print_to_display__(''.join([str(x4) for x4 in ['Average of 5: ', Ao5, 's']]))
    if buttons.buttonL.pressed() or buttons.buttonR.pressed() or buttons.buttonU.pressed() or buttons.buttonD.pressed() or buttons.buttonB.pressed() or buttons.buttonA.pressed():
      i = (i if isinstance(i, Number) else 0) + 1
    if not (buttons.buttonL.pressed() or buttons.buttonR.pressed() or buttons.buttonU.pressed() or buttons.buttonD.pressed() or buttons.buttonB.pressed() or buttons.buttonA.pressed()):
      i = 0
    if i > 999:
      __print_to_display__('0.000' + 's')
  while buttons.buttonL.pressed() or buttons.buttonR.pressed() or buttons.buttonU.pressed() or buttons.buttonD.pressed() or buttons.buttonB.pressed() or buttons.buttonA.pressed():
    __print_to_display__('0.000' + 's')
  startTime = time.ticks_ms()
  while not (buttons.buttonB.justPressed() or buttons.buttonL.justPressed() or buttons.buttonR.justPressed() or buttons.buttonU.justPressed() or buttons.buttonD.justPressed() or buttons.buttonA.pressed()):
    now = time.ticks_ms()
    __print_to_display__(str((now - startTime) / 1000) + 's')
  time2 = [now - startTime]
  times = times + time2
  time.sleep_ms(250)
  while not (buttons.buttonB.justPressed() or buttons.buttonL.justPressed() or buttons.buttonR.justPressed() or buttons.buttonU.justPressed() or buttons.buttonD.justPressed() or buttons.buttonA.pressed()):
    time.sleep_ms(1)