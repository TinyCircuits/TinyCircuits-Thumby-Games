from thumbyGraphics import display
from math import sqrt

def desc(x, y, l):
    if l == 0:
        if x == 1 and y == 3:
            d = 'BACK'
        elif x == 2 and y == 3:
            d = 'CLEAR'
        else:
            d = ''
    elif l == 1:
        if x == 0: d = ''
        elif x == 1:
            if y == 0:
                d = 'LEFT'
            elif y == 2:
                d = 'POWER'
            elif y == 3:
                d = 'ROOT'
            else: d = ''
        elif x == 2:
            if y == 0:
                d = 'RIGHT'
            elif y == 2:
                d = 'POINT'
            else: d = ''
    return d
            
def char(x, y, l):
    if l == 0:
        if x == 0:
            if y == 0: c = '1'
            elif y == 1: c = '4'
            elif y == 2: c = '7'
            elif y == 3: c = '0'
        elif x == 1:
            if y == 0: c = '2'
            elif y == 1: c = '5'
            elif y == 2: c = '8'
            elif y == 3: c = 'del'
        elif x == 2:
            if y == 0: c = '3'
            elif y == 1: c = '6'
            elif y == 2: c = '9'
            elif y == 3: c = 'clr'
    elif l == 1:
        if x == 0:
            if y == 0: c = '+'
            elif y == 1: c = '-'
            elif y == 2: c = '*'
            elif y == 3: c = '/'
        elif x == 1:
            if y == 0: c = 'left'
            elif y == 1: c = '('
            elif y == 2: c = '^'
            elif y == 3: c = 'a'
        elif x == 2:
            if y == 0: c = 'right'
            elif y == 1: c = ')'
            elif y == 2: c = '.'
            elif y == 3: c = '%'
    return c

def solve(exp):
    exp = str(exp)
    if '^' in exp:
        exp = exp.replace('^', '**')
    if 'a' in exp:
        exp = exp.replace('a', 'math.sqrt')
    if '%' in exp:
        exp = exp.replace('%', '/100*')
    
    return eval(exp)
        
def printex(message):
      if len(message) > 12:
          message = message[:12]+'\n'+message[12:]
          if len(message) > 25:
              message = message[:25]+'\n'+message[25:]
              if len(message) > 38:
                  message = message[:38]+'\n'+message[38:]
                  if len(message) > 51:
                      message = message[:51]+'\n'+message[51:]
                  
      message = str(message)
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