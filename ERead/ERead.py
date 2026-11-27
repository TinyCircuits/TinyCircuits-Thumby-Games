from thumbyGraphics import display
import thumby
import time

char = 0
pgturns = 0

thumby.saveData.setName("ERead")

if (thumby.saveData.hasItem("pgturns")):
    pgturns = int(thumby.saveData.getItem("pgturns"))

try:
    f = open("book.txt", "x")
    f.close()
    f = open("book.txt", "w")
    f.write("No Book Found")
    f.close()
except OSError:
    pass

display.setFPS(30)
book = "Hello"
while True:
    char = pgturns*12
    for i in range(5):
        try:
            f = open("book.txt")
            f.seek(char)
            book = f.read(12)
            display.drawText(str(book), 0, i*10, 1)
            char += 12
        
        except FileNotFoundError:
            f = open("book.txt", "x")
    
        f.close()
        
    if thumby.buttonD.pressed():
        pgturns += 1
        time.sleep(0.05)
    elif thumby.buttonU.pressed():
        time.sleep(0.05)
        if pgturns > 0:
            pgturns -= 1
            
    if thumby.buttonB.pressed():
        thumby.saveData.setItem("pgturns", pgturns)
        thumby.saveData.save()
        break

    char = 0
    display.update()
    display.fill(0)

