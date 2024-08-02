import thumbyButton as buttons

class Player:
    def __init__(self, x, y, camX, camY):
        self.positions = [x, y]
        self.camera = [camX, camY]
        self.cheat = 1
        self.lastPos = [0, 0]
        self.speed = [0, 0]
        self.falling = 0
        self.dash = 0
        self.timer = 0
        self.dir = 0
        self.anim = ""

    def move(self, h):
        self.lastPos = [self.positions[0], self.positions[1]]
        
        if self.cheat == 1:
            self.anim = "Idle"
            if buttons.buttonA.pressed() and self.falling < 2:
                self.positions[1] -= 1
                self.speed[1] = -3.5
                self.speed[0] *= 1.5
            if buttons.buttonL.pressed():
                self.dir = 1
                self.speed[0] -= 0.7
                self.anim = "Walk"
            if buttons.buttonR.pressed():
                self.dir = 0
                self.speed[0] += 0.7
                self.anim = "Walk"
            
            self.speed[1] += 0.3
            self.speed[0] *= 0.9
            
            if self.speed[1] > 3:
                self.speed[1] = 3
            
            self.falling += 1
            
            if self.positions[1] >= (40 - h):
                self.speed[1] = 0
                self.positions[1] = (40 - h)
                self.falling = 0
            else:
                if self.speed[1] > 0:
                    self.anim = "Fall"
                elif self.speed[1] < 0:
                    self.anim = "Jump"
            
            if buttons.buttonB.justPressed() and self.dash == 1:
                if buttons.buttonU.pressed():
                    self.speed[1] = -4
                if buttons.buttonD.pressed():
                    self.speed[1] = 4
                if buttons.buttonR.pressed():
                    self.speed[0] = 8
                if buttons.buttonL.pressed():
                    self.speed[0] = -8
                self.anim = "Spin"
                    
        else:
            if buttons.buttonL.pressed():
                self.speed[0] -= 0.7
            if buttons.buttonR.pressed():
                self.speed[0] += 0.7
            if buttons.buttonU.pressed():
                self.speed[1] = -3.5
            if buttons.buttonD.pressed():
                self.speed[1] += 0.7
            
            self.speed[0] *= 0.8
            self.speed[1] *= 0.8
        
        self.positions[0] += int(self.speed[0])
        self.positions[1] += int(self.speed[1])
    
    def update_camera(self, h):
        x_center_min, x_center_max = 32, 36
        y_center_min, y_center_max = 18, 22
        
        distance_x = abs((self.positions[0] + self.camera[0]) - (x_center_min + x_center_max) // 2)
        distance_y = abs((self.positions[1] + self.camera[1]) - (y_center_min + y_center_max) // 2)
        
        speed_multiplier_x = 1 + int(distance_x * 0.2)
        speed_multiplier_y = 1 + int(distance_y * 0.2)
        
        if (self.positions[0] + self.camera[0]) > x_center_max:
            self.camera[0] -= speed_multiplier_x
        elif (self.positions[0] + self.camera[0]) < x_center_min:
            self.camera[0] += speed_multiplier_x
    
        if ((self.positions[1] + (h - 5)) + self.camera[1]) < y_center_min:
            self.camera[1] += speed_multiplier_y
        elif ((self.positions[1] + (h - 5)) + self.camera[1]) > y_center_max:
            self.camera[1] -= speed_multiplier_y
