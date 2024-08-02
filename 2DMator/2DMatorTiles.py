import thumbyButton as buttons
from thumbyGraphics import display
from thumbyAnimator import AnimationPlayer
import ujson

display.setFont("/lib/font3x5.bin", 3, 5, 1)
display.setFPS(30)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lastAnim = ""
        self.animName = ""
        
    def move(self):
        self.animName = "idle"
        
        if buttons.buttonU.pressed():
            self.y -= 1
            self.animName = "walk"
        if buttons.buttonD.pressed():
            self.y += 1
            self.animName = "walk"
        if buttons.buttonL.pressed():
            self.x -= 1
            self.animName = "walk"
        if buttons.buttonR.pressed():
            self.x += 1
            self.animName = "walk"
        
        cam.update(self)
        
        display.drawFilledRectangle((self.x - cam.x) - 6, (self.y - cam.y) - 4, 14, 17, 0)
        
        for content in anim:
            try:
                if self.animName == "idle":
                    content.animate(self.animName, self.lastAnim, (self.x - cam.x, self.y - cam.y), 3)
                elif self.animName == "walk":
                    content.animate(self.animName, self.lastAnim, (self.x - cam.x, self.y - cam.y), 4)
            except Exception as e:
                print(f"Error animating: {e}")
        
        self.lastAnim = self.animName
        
        display.drawText("PX: " + str(self.x), 45, 14, 1)
        display.drawText("PY: " + str(self.y), 45, 20, 1)

class Camera:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
    
    def update(self, player):
        self.x = max(0, player.x - self.width // 2)
        self.y = max(0, player.y - self.height // 2)
        
        self.x = min(self.x, 100)  # Adjust based on your world size
        self.y = min(self.y, 100)  # Adjust based on your world size
        
        display.drawText("CX: " + str(self.x), 45, 2, 1)
        display.drawText("CY: " + str(self.y), 45, 8, 1)

class Tiles:
    def __init__(self, tiles_data):
        self.tiles_data = tiles_data
        self.tile_width = 4
        self.tile_height = 4
        
    def load_world(self):
        self.world_map = self.tiles_data["map0"]
        self.map_width = 10
        self.map_height = len(self.world_map) // self.map_width
        
    def draw(self):
        screen_width = display.width
        screen_height = display.height
        drawCount = 0
        
        for row in range(self.map_height):
            for col in range(self.map_width):
                tile = self.world_map[row * self.map_width + col]
                
                screen_x = col * self.tile_width - cam.x
                screen_y = row * self.tile_height - cam.y
                
                if ( -8 > screen_x or screen_x > screen_width + 8 and
                     -8 > screen_y or screen_y > screen_height + 8):
                    continue
                else:
                    if tile == 1:
                        display.drawFilledRectangle(screen_x, screen_y, self.tile_width, self.tile_height, 1)
                    
                    drawCount += 1
        
        print(drawCount)

file_path = "/Games/2DMator/tiles.json"
tiles_data = {}
try:
    with open(file_path, "r") as file:
        tiles_data = ujson.load(file)
        print(f"Loaded tiles: {tiles_data}")
except Exception as e:
    print(f"Error loading JSON file: {e}")

tiles = Tiles(tiles_data)
tiles.load_world()

file_path = "/Games/2DMator/file.json"
p = Player(28, 18)
cam = Camera(72, 40)
anim = [AnimationPlayer("test", (0, 0), file_path)]

while True:
    display.update()
    display.fill(0)
    
    tiles.draw()
    p.move()
