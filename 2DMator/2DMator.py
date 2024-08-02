import thumbyButton as buttons
from thumbyGraphics import display
from thumbyAnimator import AnimationPlayer

x, y = 0, 0
lastAnim = ""
file_path = "/Games/2DMator/file.json"

display.setFont("/lib/font3x5.bin", 3, 5, 1)
display.setFPS(30)

def move():
    global x, y, lastAnim
    
    animName = "idle"
    
    if buttons.buttonU.pressed():
        y -= 1
        animName = "walk"
    if buttons.buttonD.pressed():
        y += 1
        animName = "walk"
    
    if buttons.buttonL.pressed():
        x -= 1
        animName = "walk"
    if buttons.buttonR.pressed():
        x += 1
        animName = "walk"
    
    for content in anim:
        try:
            if animName == "idle":
                content.animate(animName, lastAnim, (x, y), 3)
            elif animName == "walk":
                content.animate(animName, lastAnim, (x, y), 4)
        except Exception as e:
            print(f"Error animating: {e}")
    
    lastAnim = animName

anim = [AnimationPlayer("test", (28, 18), file_path)]

while True:
    display.fill(0)
    
    move()
    
    display.update()
