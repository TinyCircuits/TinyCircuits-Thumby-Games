import thumby
import random
import time
import math

#random.seed(5)

FRAME_TIME = 0.05 # real device
# FRAME_TIME = 0.02 # emulator

head = None
scissors = None
hairs = None
pimples = None
score = 0

class BaldHead:
    WIDTH = 72   # Thumby screen width
    HEIGHT = 40  # Thumby screen height
    
    def __init__(self, display):
        self.display = display
        self.width = display.width
        self.height = display.height
        # Ellipse parameters
        self.centerX = self.width // 2
        self.centerY = self.height + 20   # center pushed below screen
        self.radiusX = self.width // 2
        self.radiusY = 35
        
        self.bitmap = self._make_bitmap()
        self.sprite = thumby.Sprite(BaldHead.WIDTH, BaldHead.HEIGHT,
                                    self.bitmap, 0, 0)
    
    def _make_bitmap(self):
        buf = bytearray(self.width * self.height // 8)

        for x in range(self.width):
            dx = (x - self.centerX) / self.radiusX
            if abs(dx) <= 1:
                y = int(self.centerY - self.radiusY * (1 - dx*dx)**0.3)
                if 0 <= y < self.height:
                    byte_index = x + (y // 8) * self.width
                    bit_index = y % 8
                    buf[byte_index] |= (1 << bit_index)
        return buf
        
    def random_point_on_head(self):
        """Return a random (x, y) point inside the bald head (arc and below)."""
        while True:
            x = random.randint(12, self.width - 1) # from 12
                # to prevent spawning hairs where the scissors can't reach
                # that is, the left end of the screen
            dx = (x - self.centerX) / self.radiusX
            if abs(dx) <= 1:
                # yArc = top boundary of the head at this x
                yArc = int(self.centerY - self.radiusY * (1 - dx*dx)**0.3)
                if 0 <= yArc < self.height:
                    # pick random y between arc and bottom of screen
                    y = random.randint(yArc, self.height - 1)
                    return (x, y)


    def draw(self):
        self.display.drawSprite(self.sprite)

class Hair:
    
    # BITMAP: width: 3, height: 5
    hair_segment_1 = bytearray([31,0,0])
    # BITMAP: width: 3, height: 10
    hair_segment_2 = bytearray([224,31,0,
               3,0,0])
    # BITMAP: width: 3, height: 15
    hair_segment_3 = bytearray([0,224,31,
               124,3,0])
    # BITMAP: width: 3, height: 20
    hair_segment_4 = bytearray([0,31,224,
               128,124,3,
               15,0,0])
    # BITMAP: width: 3, height: 25
    hair_segment_5 = bytearray([31,224,0,
               0,131,124,
               240,15,0,
               1,0,0])
    # BITMAP: width: 3, height: 30
    hair_segment_6 = bytearray([224,31,0,
               3,124,128,
               0,240,15,
               62,1,0])
    # BITMAP: width: 3, height: 35
    hair_segment_7 = bytearray([0,224,31,
               124,131,0,
               0,15,240,
               192,62,1,
               7,0,0])
    # BITMAP: width: 3, height: 40
    hair_segment_8 = bytearray([0,31,224,
               128,124,3,
               15,240,0,
               0,193,62,
               248,7,0])
    hair_segments_bitmaps = [
        hair_segment_1, hair_segment_2, hair_segment_3, 
        hair_segment_4, hair_segment_5, hair_segment_6, 
        hair_segment_7, hair_segment_8
        ]
    
    def __init__(self, display, start_point, grow_time=5):
        self.display = display
        self.x, self.y = start_point
        self.grow_time = grow_time
        self.start_time = time.ticks_ms()
        self.finished = False
        self.hair_segments_bitmaps = Hair.hair_segments_bitmaps  # list of cumulative bitmaps (5,10,...,40)
        
    def update(self):
        elapsed = (time.ticks_ms() - self.start_time) / (2000.0 * (FRAME_TIME / 0.02))
        if elapsed > self.grow_time:
            elapsed = self.grow_time
            self.finished = True
    
        # Current hair length proportional to elapsed time
        length = int((elapsed / self.grow_time) * self.y)
    
        segment_height = 5
        current_segment_index = length // segment_height     # 0,1,2,... up to 8 (for 40px)
        remainder = length % segment_height                  # 0..4
    
        # 1) Draw the cumulative bitmap for the current full segment (if any)
        if current_segment_index > 0:
            seg = min(current_segment_index, len(self.hair_segments_bitmaps))  # clamp to available bitmaps
            bitmap = self.hair_segments_bitmaps[seg - 1]
            height = seg * segment_height  # 5,10,15,...,40
    
            sprite = thumby.Sprite(
                width=3, height=height,
                bitmapData=bitmap,
                x=self.x - 1, y=self.y - height
            )
            self.display.drawSprite(sprite)
    
        # 2) Draw the remainder pixels above the last full segment
        pattern = [-1, 0, 1, 0]
        for pixel_index in range(remainder):
            # We are inside the next segment “in progress”
            seg_for_offset = current_segment_index
            column_offset = pattern[seg_for_offset % len(pattern)]
    
            yy = self.y - (current_segment_index * segment_height + pixel_index)
            xx = self.x + column_offset
            if 0 <= xx < self.display.width and 0 <= yy < self.display.height:
                self.display.setPixel(xx, yy, 1)
        
        # Check if hair tip reached top of screen
        hair_top_y = self.y - length
        if hair_top_y <= 0:
            return "GAME_OVER"


class Scissors:
    WIDTH = 12
    HEIGHT = 12

    def __init__(self, display, x=20, y=10):
        self.display = display
        self.x = x
        self.y = y

        # BITMAP: width: 12, height: 12
        self.bitmap = bytearray([
            28,162,162,162,188,64,64,160,160,16,16,8,
            7,8,8,8,7,0,0,0,0,1,1,2
        ])
        self.sprite = thumby.Sprite(Scissors.WIDTH, Scissors.HEIGHT, self.bitmap, self.x, self.y)
        
        self.direction = 1   # 1 = right, -1 = left
        self.SPEED = (display.width - Scissors.WIDTH) / 3.0  # pixels per second (cross in 2s)
        self.speed = self.SPEED
        self.last_update = time.ticks_ms()
        self.stopped_until = None
        # BITMAP: width: 12, height: 12
        self.alt_bitmap = bytearray([28,162,162,162,188,64,64,64,96,96,96,64,
                   7,8,8,8,7,0,0,0,0,0,0,0])

    def draw(self):
        # Sync sprite position
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.display.drawSprite(self.sprite)

    def move_to(self, x, y):
        self.x = max(0, min(self.display.width - Scissors.WIDTH, x))
        self.y = max(0, min(self.display.height - Scissors.HEIGHT, y))
        
    def get_cut_line_range(self):
        """
        Cutting line is the 6th row from the bottom of the scissors sprite.
        Returns (y, x_start, x_end).
        """
        row_from_top = Scissors.HEIGHT - 6   # 6th from bottom
        y_line = self.y + row_from_top
        x_start = self.x + 6   # from 6th pixel (counting from left)
        x_end   = self.x + Scissors.WIDTH    # to the end (12th pixel)
        return (y_line, x_start, x_end)
    
    def intersects_hair(self, hair):
        """
        Check if scissors cutting line intersects with given hair.
        """
        y_line, x_start, x_end = self.get_cut_line_range()

        # Hair top position (highest y it reaches)
        hair_top_y = hair.y - int((time.ticks_ms() - hair.start_time) / (1000.0 * (FRAME_TIME / 0.02)) / hair.grow_time * hair.y)

        # Hair is trimmable if it reaches or passes the cutting line
        if hair_top_y <= y_line <= hair.y:
            # Hair horizontal span (3 pixels wide centered on x)
            hair_x_start = hair.x - 1
            hair_x_end   = hair.x + 1
            # Check horizontal overlap
            if hair_x_end >= x_start and hair_x_start <= x_end:
                return True
        return False
        
    def update(self):
        now = time.ticks_ms()
    
        # Handle stop timer
        if self.stopped_until and time.ticks_ms() < self.stopped_until:
            self.speed = 0
            self.SPEED += 0.2
            #return
        elif self.stopped_until and time.ticks_ms() >= self.stopped_until:
            # End stop: restore. normal bitmap
            self.sprite.bitmap = self.bitmap
            self.stopped_until = None
            self.speed = self.SPEED
    
        # Movement
        elapsed = (now - self.last_update) / 1000.0
        self.last_update = now
        self.x += self.direction * self.speed * elapsed
    
        # Bounce at edges
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        elif self.x >= self.display.width - Scissors.WIDTH:
            self.x = self.display.width - Scissors.WIDTH
            self.direction = -1

class Pimple:
    WIDTH = 10
    HEIGHT = 3
    # BITMAP: width: 8, height: 3
    BITMAP = bytearray([4,2,2,3,1,1,3,2,2,4])
    
    x = None
    y = None
    sprite = None
    display = None
    maturity = 0
    
    def __init__(self, display, start_point):
        self.display = display
        self.x, self.y = start_point
        self.sprite = thumby.Sprite(self.WIDTH, self.HEIGHT, self.BITMAP, self.x, self.y)
    
    def update(self):
        if self.maturity == 0 or self.maturity == 3 or self.maturity == 6:
            thumby.audio.play(1500, 80)
        self.maturity += 1
        if self.maturity > 80: # Blipping
            if self.maturity % 3 != 2: # Blipping
                self.display.drawSprite(self.sprite)
        else:
            if self.maturity > 150: # 20 FPS => maturity 100 in 5s
                return "GAME_OVER"
            else:
                self.display.drawSprite(self.sprite)

class Cream:
    WIDTH = 3
    HEIGHT = 5
    # BITMAP: width: 3, height: 5
    BITMAP = bytearray([3,15,24])
    
    x = None
    y = None
    sprite = None
    display = None
    
    def __init__(self, display, start_x):
        self.display = display
        self.x = int(start_x)
        self.y = 0 # top of the screen
        self.sprite = thumby.Sprite(self.WIDTH, self.HEIGHT, self.BITMAP, self.x, self.y)
        
        self.wind_dir = random.choice([-1, 1])   # left or right
        self.wind_force = random.uniform(0.2, 0.4)  # strength of wind push
    
    def update(self):
    
        # Vertical fall
        self.y += 1   # gentle descent
    
        # Horizontal wind push
        self.x += self.wind_dir * self.wind_force
    
        # Player input: arrows counteract wind
        if thumby.buttonL.pressed():
            self.x -= 3.0
        elif thumby.buttonR.pressed():
            self.x += 3.0
    
        # Keep cream inside screen bounds
        self.x = max(0, min(self.display.width - Cream.WIDTH, int(self.x)))
    
        # Draw
        self.sprite.x = int(self.x)
        self.sprite.y = int(self.y)
        self.display.drawSprite(self.sprite)
        
        if self.y > 42:
            return "GAME_OVER"
    
    def intersects_pimple(self, pimple):
        """Return True if cream bottom edge overlaps with given pimple sprite."""
        cream_bottom_y = self.y + Cream.HEIGHT - 1
        cream_left_x   = self.x
        cream_right_x  = self.x + Cream.WIDTH - 1

        pimple_top_y    = pimple.y
        pimple_bottom_y = pimple.y + Pimple.HEIGHT - 1
        pimple_left_x   = pimple.x
        pimple_right_x  = pimple.x + Pimple.WIDTH - 1

        # Check vertical overlap: cream bottom touches pimple area
        if pimple_top_y <= cream_bottom_y <= pimple_bottom_y:
            # Check horizontal overlap
            if cream_right_x >= pimple_left_x and cream_left_x <= pimple_right_x:
                return True
        return False
    

def reset_game():
    global head, scissors, hairs, pimples, cream, score
    thumby.display.fill(0)
    head = BaldHead(thumby.display)
    scissors = Scissors(thumby.display, x=random.randint(0, thumby.display.width - Scissors.WIDTH), y=10)
    hairs = []
    pimples = []
    cream = None
    score = 0

def menu():
    
    ### INSTRUCTIONS
    thumby.display.drawText("A to", 20, 2, 1)
    thumby.display.drawText("trim", 20, 11, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("B to", 20, 2, 1)
    thumby.display.drawText("apply", 20, 11, 1)
    thumby.display.drawText("cream", 20, 20, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    thumby.display.drawText("L/R to", 20, 2, 1)
    thumby.display.drawText("steer", 20, 11, 1)
    thumby.display.drawText("cream", 20, 20, 1)
    thumby.display.update()
    time.sleep(1.0)
    thumby.display.fill(0)
    ### END OF INSTRUCTIONS
    
    # BITMAP: width: 72, height: 80
    grubol_bitmap = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,191,223,207,239,239,247,247,247,247,247,231,207,223,191,127,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,143,231,248,254,255,255,255,191,125,127,255,255,247,255,255,255,255,255,255,255,254,0,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,192,31,127,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,159,224,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,135,115,251,251,251,27,139,231,243,253,252,254,254,254,254,255,255,254,254,254,253,253,251,251,251,251,251,251,251,251,251,253,252,253,251,247,207,31,79,239,239,207,31,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,15,111,103,119,119,15,28,129,227,248,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,248,195,7,81,92,31,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,224,159,63,127,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,191,159,207,243,248,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,254,253,249,243,195,139,27,59,123,251,251,251,251,251,251,3,251,251,253,253,253,253,253,125,29,205,242,248,252,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,121,19,199,223,223,223,223,192,31,223,223,207,199,211,221,222,95,31,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,253,253,253,253,253,253,253,252,253,253,253,253,253,252,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
    
    # BITMAP: width: 72, height: 80
    grubol_inverted_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,32,48,16,16,8,8,8,8,8,24,48,32,64,128,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,112,24,7,1,0,0,0,64,130,128,0,0,8,0,0,0,0,0,0,0,1,255,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,224,128,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,96,31,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,120,140,4,4,4,228,116,24,12,2,3,1,1,1,1,0,0,1,1,1,2,2,4,4,4,4,4,4,4,4,4,2,3,2,4,8,48,224,176,16,16,48,224,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,240,144,152,136,136,240,227,126,28,7,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,60,248,174,163,224,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,31,96,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,96,48,12,7,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,2,6,12,60,116,228,196,132,4,4,4,4,4,4,252,4,4,2,2,2,2,2,130,226,50,13,7,3,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,134,236,56,32,32,32,32,63,224,32,32,48,56,44,34,33,160,224,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,2,2,2,2,2,2,2,3,2,2,2,2,2,3,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
               0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    
    for i in range(41):
        grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_bitmap, 0, 0-40+i)
        
        thumby.display.fill(0)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.update()
        time.sleep(0.02)
    
    time.sleep(0.5)
    thumby.display.drawText("Grubole", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("2", 18, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Bald", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Chap", 2, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Sim", 6, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("ulator", 4, 2, 0)
    thumby.display.update()
    time.sleep(0.5)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press", 2, 2, 0)
    thumby.display.drawText("A to", 2, 11, 0)
    thumby.display.drawText("start", 2, 20, 0)
    thumby.display.update()
    time.sleep(0.5)
    grubol_sprite = thumby.Sprite(72, 80,
                                        grubol_inverted_bitmap, 0, 0)
    thumby.display.drawSprite(grubol_sprite)
    thumby.display.drawText("Press", 2, 2, 1)
    thumby.display.drawText("A to", 2, 11, 1)
    thumby.display.drawText("start", 2, 20, 1)
    thumby.display.update()
    time.sleep(0.5)
        

def main():
    
    global head, scissors, hairs, pimples, cream, score

    game_over = False
    game_over_time = 0.0
    is_menu = True
    
    reset_game()

    spawn_prob =  0.015 + 1/1000 * math.log(10 * scissors.speed) # spawn probability * a factor which depend on the scissors speed
    
    
    
    while True:
        
        if is_menu:
            menu()
            while is_menu:
                if thumby.buttonA.justPressed():
                    is_menu = False

        if game_over:
            thumby.display.fill(0)
            thumby.display.drawText("GAME OVER", 10, 10, 1)
            thumby.display.drawText("Score: " + str(score), 10, 20, 1)
            thumby.display.update()
            time.sleep(0.1)
            
            # Wait 1 second before allowing restart
            if time.ticks_ms() - game_over_time > 1000:
                if thumby.buttonA.justPressed():
                    game_over = False
                    reset_game()
                if thumby.buttonB.justPressed():
                    thumby.reset()
            continue # loop over "if game_over"

        thumby.display.fill(0)
        head.draw()
        rand = random.random()
        
        if thumby.buttonA.justPressed():
            scissors.stopped_until = time.ticks_add(time.ticks_ms(), int(0.8 * 1000))
            # Swap to alternate bitmap
            if scissors.alt_bitmap:
                scissors.sprite.bitmap = scissors.alt_bitmap
            
            hairs_len1 = len(hairs)
            hairs = [h for h in hairs if not scissors.intersects_hair(h)] # remove hairs which have just been cut
            hairs_len2 = len(hairs)
            if hairs_len1 != hairs_len2:
                score = score + (hairs_len1 - hairs_len2)
                thumby.audio.play(900, 60)
        
        if thumby.buttonB.justPressed():
            if cream is None:
                cream = Cream(thumby.display, 35) # 72 is screen width, 10 is the offset


        scissors.update()
        scissors.draw()
        
        if cream is not None:
            result = cream.update()
            if result == "GAME_OVER":
                game_over = True
            else:
                # Check collision with pimples
                for p in pimples[:]:   # iterate over a copy since we may remove
                    if cream.intersects_pimple(p):
                        pimples.remove(p)
                        cream = None   # remove cream too
                        score += 10
                        break          # stop checking further pimples
        
        if rand < spawn_prob or len(hairs) == 0: # once in a while a new hair appears
            point = head.random_point_on_head()
            hairs.append(Hair(thumby.display, point))
            
            if rand < spawn_prob / 2 : # once in a while a new pimple appears
                point = head.random_point_on_head()
                if point[0] > 65 or point[1] > 35: # too right or too low
                    continue
                else:
                    pimples.append(Pimple(thumby.display, point))
        
        for h in hairs:
            result = h.update()
            if result == "GAME_OVER":
                game_over = True
                game_over_time = time.ticks_ms()
                
        for p in pimples:
            result = p.update()
            if result == "GAME_OVER":
                game_over = True
                game_over_time = time.ticks_ms()
        
        thumby.display.update()
        time.sleep(FRAME_TIME)



# Run program
main()
