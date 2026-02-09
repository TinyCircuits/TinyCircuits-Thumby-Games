import thumby
import time
import math
import random

# Screen
SCR_W = 72
SCR_H = 40
CENTER_X = SCR_W // 2

# World / gameplay
SPEED = 100.0            # m/s
GATE_DISTANCE = 200.0    # meters between gates
PIX_PER_METER = 40.0     # perspective scale factor (tweak)
STEER_ACCEL = math.radians(120.0)
ANG_FRICTION = 2.0
MAX_YAW_RATE = math.radians(120.0)

# Gate sizing
START_GATE_WIDTH = 30.0
WIDTH_SHRINK_FACTOR = 0.90
MIN_GATE_WIDTH = 4.0
STARS_NUM = 15

# Crossing threshold (how close forward to consider crossing)
CROSS_Z_THRESH = 5.0

class Game:
    def __init__(self):
        self.state = "menu"   # "menu", "game", "gameover"
        self.last_ms = time.ticks_ms()
        self.reset_game_vars()

    def reset_game_vars(self):
        # Car/world state
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.yaw_rate = 0.0

        # Gates / score
        self.gate_count = 0
        self.gate_width = START_GATE_WIDTH

        # Spawn first gate directly ahead
        self.spawn_next_gate(initial=True)

        # Running flag
        self.running = True
        
        # Background stars
        self.stars = []
        for i in range(STARS_NUM):
            sx = random.randint(0, SCR_W - 1)
            sy = random.randint(0, int((SCR_H - 1)/3)) # only the upper 1/3 of the screen
            blink = random.randint(0, 20)  # blink timer
            self.stars.append([sx, sy, blink])
        
        # Speed lines
        self.speed_lines_blink_timer = 0

    def spawn_next_gate(self, initial=False):
        # On initial spawn, place straight ahead; otherwise random offset
        if initial:
            offset_deg = 0.0
            self.gate_width = START_GATE_WIDTH
        else:
            offset_deg = random.uniform(-28.0, 28.0)
            # shrink gate width
            self.gate_width = max(MIN_GATE_WIDTH, self.gate_width * WIDTH_SHRINK_FACTOR)

        offset_rad = math.radians(offset_deg)
        angle = self.heading + offset_rad
        dx = math.cos(angle) * GATE_DISTANCE
        dy = math.sin(angle) * GATE_DISTANCE
        self.gate_x = self.x + dx
        self.gate_y = self.y + dy

    def start_game(self):
        self.reset_game_vars()
        self.state = "game"

    def update(self, dt):
        if self.state != "game" or not self.running:
            return

        # Input
        left = thumby.buttonL.pressed()
        right = thumby.buttonR.pressed()
        steer_input = 0.0
        if left and not right:
            steer_input = -1.0
        elif right and not left:
            steer_input = 1.0

        # Angular dynamics
        self.yaw_rate += steer_input * STEER_ACCEL * dt
        # clamp
        if self.yaw_rate > MAX_YAW_RATE:
            self.yaw_rate = MAX_YAW_RATE
        elif self.yaw_rate < -MAX_YAW_RATE:
            self.yaw_rate = -MAX_YAW_RATE
        # damping
        self.yaw_rate -= self.yaw_rate * ANG_FRICTION * dt
        # integrate heading
        self.heading += self.yaw_rate * dt

        # Forward motion (fixed speed)
        vx = math.cos(self.heading) * SPEED
        vy = math.sin(self.heading) * SPEED
        self.x += vx * dt
        self.y += vy * dt

        # Check gate crossing / miss
        self.check_gate_cross()

    def check_gate_cross(self):
        # Local coordinates relative to car heading
        dx = self.gate_x - self.x
        dy = self.gate_y - self.y
        forward_x = math.cos(self.heading)
        forward_y = math.sin(self.heading)
        right_x = math.cos(self.heading + math.pi/2.0)
        right_y = math.sin(self.heading + math.pi/2.0)

        z_local = dx * forward_x + dy * forward_y   # forward distance
        x_local = dx * right_x + dy * right_y       # lateral offset

        # If we've reached the gate plane (or passed it)
        if z_local <= CROSS_Z_THRESH:
            # If within gate width -> success
            if abs(x_local) <= (self.gate_width * 0.5):
                self.play_gate_beep(self.gate_count) # Play beep based on current score
                self.gate_count += 1
                self.spawn_next_gate(initial=False)
            else:
                # Missed gate -> game over
                self.running = False
                self.state = "gameover"

    def draw(self):
        d = thumby.display
        d.fill(0)

        if self.state == "menu":
            # Short menu text to fit tiny screen
            self.menu()
            while self.state == "menu":
                if thumby.buttonA.justPressed():
                    self.start_game()
        elif self.state == "game":
            # Draw starfield background first
            self.draw_stars(d)
            # Draw gate (perspective)
            self.draw_gate(d)
            # Draw static car symbol at bottom center
            self.draw_car_symbol(d)
            # HUD: only score
            d.drawText(str(self.gate_count), 0, 0, 1)
        elif self.state == "gameover":
            # Show game over and score
            d.drawText("GAME OVER", CENTER_X - 24, 8, 1)
            # Score line
            score_text = "SCORE:" + str(self.gate_count)
            # center score text roughly
            d.drawText(score_text, CENTER_X - (len(score_text)*3), 20, 1)
            d.drawText("A=restart", CENTER_X - 24, 30, 1)

        d.update()

    def draw_gate(self, d):
        # Transform gate into car-local coordinates
        dx = self.gate_x - self.x
        dy = self.gate_y - self.y
        forward_x = math.cos(self.heading)
        forward_y = math.sin(self.heading)
        right_x = math.cos(self.heading + math.pi/2.0)
        right_y = math.sin(self.heading + math.pi/2.0)

        z_local = dx * forward_x + dy * forward_y
        x_local = dx * right_x + dy * right_y

        # Only draw if in front and not extremely close (avoid weird stretching)
        if z_local <= 1.0:
            return

        # Keep gate square: size scales with 1 / distance
        size_px = int((self.gate_width * PIX_PER_METER) / z_local)
        size_px = max(2, min(size_px, SCR_W))

        # Angle left/right relative to forward axis
        angle = math.atan2(x_local, z_local)
        half_fov = math.radians(30.0)  # narrow FOV for tiny screen
        if angle < -half_fov or angle > half_fov:
            return

        # Map angle to screen X
        x_center = int(CENTER_X + (angle / half_fov) * (CENTER_X - 6))
        gate_left = x_center - size_px // 2
        gate_top = (SCR_H // 2) - (size_px // 2)

        # Clamp to screen bounds
        if gate_left < -size_px or gate_left > SCR_W:
            return
        gate_left = max(0, min(gate_left, SCR_W - size_px))
        gate_top = max(0, min(gate_top, SCR_H - size_px))

        # drawRectangle(x, y, w, h, color)
        d.drawRectangle(gate_left, gate_top, size_px, size_px, 1)

    def draw_car_symbol(self, d):
        # Static small triangle at bottom center (no rotation)
        base_x = CENTER_X
        base_y = SCR_H - 6
        d.drawLine(base_x - 4, base_y, base_x, base_y - 6, 1)
        d.drawLine(base_x, base_y - 6, base_x + 4, base_y, 1)
        d.drawLine(base_x + 4, base_y, base_x - 4, base_y, 1)
        
        # Now speed lines
        self.speed_lines_blink_timer += 1
        if self.speed_lines_blink_timer < 5:
            d.drawLine(base_x - 4, base_y + 2, base_x - 6, base_y + 4, 1)
            d.drawLine(base_x - 0, base_y + 2, base_x - 0, base_y + 4, 1)
            d.drawLine(base_x + 4, base_y + 2, base_x + 6, base_y + 4, 1)
        else:
            d.drawLine(base_x - 2, base_y + 2, base_x - 2, base_y + 4, 1)
            d.drawLine(base_x + 2, base_y + 2, base_x + 2, base_y + 4, 1)
            
            d.drawLine(base_x - 8, base_y + 2, base_x - 10, base_y + 4, 1)
            d.drawLine(base_x + 8, base_y + 2, base_x + 10, base_y + 4, 1)
            
            if (self.speed_lines_blink_timer == 8):
                self.speed_lines_blink_timer = 0

    def draw_stars(self, d):
        for star in self.stars:
            x, y, blink = star
            # Twinkle effect: toggle brightness every few frames
            if blink == 0:
                d.setPixel(x, y, 0)  # off
            else:
                d.setPixel(x, y, 1)  # on
            # Update blink timer
            star[2] = (blink + 1) % 20

    def handle_buttons(self):
        # Menu -> start
        if self.state == "menu" and thumby.buttonA.justPressed():
            self.start_game()
        # Gameover -> restart immediately
        elif self.state == "gameover" and thumby.buttonA.justPressed():
            self.start_game()
        elif self.state == "gameover" and thumby.buttonB.justPressed():
            thumby.reset()
            
    def play_gate_beep(self, score):
        freq = 100 + 20 * score
        thumby.audio.play(freq, 80)   # 80 ms beep feels snappy
    
    def menu(self):
        # BITMAP: width: 72, height: 80
        grubol_bitmap = bytearray([255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,191,159,223,239,239,239,239,239,239,223,223,223,159,191,191,63,127,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,1,252,254,255,255,255,255,159,189,255,255,255,255,247,255,255,255,255,255,255,126,129,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,127,127,127,127,127,127,191,223,207,247,247,251,251,251,251,248,253,251,243,247,239,239,207,223,223,223,223,223,223,223,223,239,231,231,233,236,239,207,63,127,127,127,127,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,192,159,63,127,255,7,249,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,252,3,255,127,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,31,223,223,223,222,193,0,63,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,127,159,0,209,220,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,254,254,254,254,254,254,254,253,243,231,223,223,31,191,191,191,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,127,191,63,191,223,207,239,251,252,255,252,253,253,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,240,231,15,255,255,255,255,255,255,255,63,192,255,255,255,255,255,255,127,143,243,252,254,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,63,223,223,216,195,239,239,239,111,7,128,47,111,239,207,207,199,211,88,31,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,254,254,254,254,254,254,254,254,254,255,255,255,255,254,254,254,254,254,254,255,255,255,255,255,255,255,255,255,255,255,255,255,255,
           255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255,255])
        
        # BITMAP: width: 72, height: 80
        grubol_inverted_bitmap = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,64,96,32,16,16,16,16,16,16,32,32,32,96,64,64,192,128,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,254,3,1,0,0,0,0,96,66,0,0,0,0,8,0,0,0,0,0,0,129,126,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,128,128,128,128,128,128,64,32,48,8,8,4,4,4,4,7,2,4,12,8,16,16,48,32,32,32,32,32,32,32,32,16,24,24,22,19,16,48,192,128,128,128,128,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63,96,192,128,0,248,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,252,0,128,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,224,32,32,32,33,62,255,192,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,96,255,46,35,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,2,12,24,32,32,224,64,64,64,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,64,192,64,32,48,16,4,3,0,3,2,2,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,24,240,0,0,0,0,0,0,0,192,63,0,0,0,0,0,0,128,112,12,3,1,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,192,32,32,39,60,16,16,16,144,248,127,208,144,16,48,48,56,44,167,224,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        
        for i in range(41):
            grubol_sprite = thumby.Sprite(72, 80,
                                            grubol_bitmap, 0, 0-40+i)
            
            thumby.display.fill(0)
            thumby.display.drawSprite(grubol_sprite)
            thumby.display.update()
            time.sleep(0.02)
        
        time.sleep(0.5)
        thumby.display.drawText("Grubol", 2, 2, 0)
        thumby.display.update()
        time.sleep(0.5)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.drawText("1", 18, 2, 0)
        thumby.display.update()
        time.sleep(0.5)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.drawText("Kapor", 2, 2, 0)
        thumby.display.update()
        time.sleep(0.5)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.drawText("3D", 16, 2, 0)
        thumby.display.update()
        time.sleep(0.5)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.drawText("Press A", 2, 2, 0)
        thumby.display.drawText("to start", 2, 11, 0)
        thumby.display.drawText("", 2, 20, 0)
        thumby.display.update()
        time.sleep(0.5)
        grubol_sprite = thumby.Sprite(72, 80,
                                            grubol_inverted_bitmap, 0, 0)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.drawText("Press A", 2, 2, 1)
        thumby.display.drawText("to start", 2, 11, 1)
        thumby.display.drawText("", 2, 20, 1)
        thumby.display.update()
        time.sleep(0.5)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.drawText("Press A", 2, 2, 1)
        thumby.display.drawText("to", 2, 11, 1)
        thumby.display.drawText("", 2, 20, 1)
        thumby.display.update()
        time.sleep(0.5)
        thumby.display.drawSprite(grubol_sprite)
        thumby.display.drawText("Press A", 2, 2, 1)
        thumby.display.drawText("to", 2, 11, 1)
        thumby.display.drawText("start", 36, 27, 1)
        thumby.display.update()
        time.sleep(0.5)

# Main loop
game = Game()

while True:
    time.sleep_ms(10) # 70 FPS
    now = time.ticks_ms()
    dt_ms = time.ticks_diff(now, game.last_ms)
    game.last_ms = now
    dt = max(0.0, min(dt_ms / 1000.0, 0.05))

    game.handle_buttons()
    game.update(dt)
    game.draw()
