import thumby
import time

class Menu:
    def __init__(self, selected = 0, scroll = 0):
        self.selected = selected
        self.scroll = scroll

    def choose(self, programs):
        self.programs = programs
        self.programs.append({
            "name": "Quit Silicon8",
            "file": False
        })
        while True:
            self.animate = 0
            self.render()
            self.lastInputTime = time.ticks_ms()
            self.lastAnimateTime = time.ticks_ms()
            if self.waitInput():
                return self.programs[self.selected], self.selected, self.scroll

    def waitInput(self):
        # Wait for button release
        while thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonA.pressed() or thumby.buttonB.pressed():
            pass
        # Wait for button press
        while True:
            if thumby.buttonU.pressed() and self.selected > 0:
                self.selected -= 1
                if self.selected < self.scroll:
                    self.scroll -= 1
                return False
            if thumby.buttonD.pressed() and self.selected < len(self.programs)-1:
                self.selected += 1
                if self.selected - 3 > self.scroll:
                    self.scroll += 1
                return False
            if thumby.buttonA.pressed() or thumby.buttonB.pressed():
                return True

            # Wait for animation to start
            now = time.ticks_ms()
            if now - self.lastInputTime > 300 and now - self.lastAnimateTime > 20:
                nameLength = len(self.programs[self.selected]["name"])
                if nameLength > 12:
                    if self.animate > (nameLength + 2) * 6:
                        self.animate = 0
                    else:
                        self.animate += 1
                    self.lastAnimateTime = now
                    self.render()

    def printline(self, string, highlight = False):
        if highlight:
            thumby.display.drawFilledRectangle(0, self.row - 1, thumby.display.width, 9, 1)
            thumby.display.drawText(string, 1 - self.animate, self.row, 0)
            if len(string) > 12:
                thumby.display.drawText(string, (len(string) + 2) * 6 - self.animate + 2, self.row, 0)
        else:
            thumby.display.drawText(string, 1, self.row, 1)
        self.row += 8

    def render(self):
        thumby.display.fill(0)
        self.row = 1
        for i in range(self.scroll, len(self.programs)):
            self.printline(self.programs[i]["name"], self.selected == i)
        thumby.display.update()

class Confirm:
    def __init__(self):
        self.selected = 0
        self.scroll = 0
        self.textHeight = 0

    def choose(self, program):
        # What to display about this program?
        totalText = program["name"] + '\n\n' + program["desc"]
        if "link" in program:
            totalText += '\n\nMore info:\n' + program["link"]
        self.text = self.breakText(totalText)

        while True:
            self.render()
            while thumby.buttonU.pressed() or \
                  thumby.buttonD.pressed() or \
                  thumby.buttonA.pressed() or \
                  thumby.buttonB.pressed() or \
                  thumby.buttonL.pressed() or \
                  thumby.buttonR.pressed():
                pass
            while True:
                if thumby.buttonL.pressed():
                    self.selected = 1
                    break
                if thumby.buttonR.pressed():
                    self.selected = 0
                    break
                if thumby.buttonU.pressed() and self.scroll > 0:
                    self.scroll -= 1
                    break
                if thumby.buttonD.pressed() and self.scroll < len(self.text) - 3:
                    self.scroll += 1
                    break
                if thumby.buttonA.pressed() or thumby.buttonB.pressed():
                    return self.selected == 0

    # Figure out where to break the sentence so it makes sense to the reader.
    @micropython.native
    def breakText(self, text):
        c = const(12) # Max characters per line
        result = []
        i = 0
        while i < len(text):
            # Where to break this line?
            j = i
            brk = i + c
            while j < len(text) and j - i < c + 1:
                a = text[j]
                if j - i < c and (a == '/' or a == '&'):
                    brk = j + 1
                if a == ' ':
                    brk = j + 1
                if a == '\n':
                    brk = j + 1
                    break
                j += 1
            if j == len(text):
                brk = len(text)
            result.append(text[i:brk])
            i = brk
        return result

    @micropython.native
    def render(self):
        disp = thumby.display
        dt = disp.drawText
        disp.fill(0)

        # Show game information
        for i in range(0,4):
            j = self.scroll + i
            if j < len(self.text):
                dt(self.text[j], 0, i*8, 1)

        # Show bottom menu
        height = 10
        top = disp.height - height
        middle = int(disp.width / 2)
        disp.drawFilledRectangle(0, top, disp.width, height, 1)
        disp.drawFilledRectangle(self.selected * middle, top + 1, middle, height - 1, 0)
        dt("BACK", 6, top + 2, self.selected ^ 1)
        dt("RUN", middle + 10, top + 2, self.selected)
        disp.update()
