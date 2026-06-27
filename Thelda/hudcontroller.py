from thumby import buttonA, buttonB, buttonU, buttonL, buttonR, display

class HudController:
    def __init__(self, my_player):
        self.rupees = str(my_player.rupees)
        self.dash_map = bytearray([1,1])
        self.keys = str(my_player.keys)
        self.bombs = str(my_player.bombs)
        self.blink_timer = 0
        self.y_height = 1
        self.is_paused = False
        self.menu_x = 1
        self.menu_y = -35
        self.deployed = False
        self.retracted = True
        self.menu_speed = 1
        self.cursor_height = 2
        self.cursor_blink = 0
        self.cursor_x = 44
        self.cursor_y = self.y_height - 34
        self.collected_items = [("boomerang"), ("bombs"), ("bow")]
        self.cursor_selection = ""
    
    
    
    def display_cursor(self, my_player):
        cursor_map = bytearray([99,65,0,0,0,65,99])
        cursor_blink_map = bytearray([0,0,0,0,0,0,0])
        if buttonR.justPressed():
            display.blit(cursor_blink_map, self.cursor_x, self.cursor_height, 7, 7, 1, 0, 0)
            if self.cursor_x <= 61:
                self.cursor_x += 6
            else:
                self.cursor_x = 44
                if self.cursor_height == self.y_height - 34:
                    self.cursor_height = self.y_height - 28
                else:
                    self.cursor_height = self.y_height - 34
        elif buttonL.justPressed():
            display.blit(cursor_blink_map, self.cursor_x, self.cursor_height, 7, 7, 1, 0, 0)
            if not self.cursor_x <= 44:
                self.cursor_x -= 6
            else:
                self.cursor_x = 62
                if self.cursor_height == self.y_height - 34:
                    self.cursor_height = self.y_height - 28
                else:
                    self.cursor_height = self.y_height - 34
                    
        if self.cursor_blink >= 20:
            self.cursor_blink = 0
            
        elif self.cursor_blink > 10:
            display.blit(cursor_blink_map, self.cursor_x, self.cursor_height, 7, 7, 1, 0, 0)
            self.cursor_blink += 1
        else:
            display.blit(cursor_map, self.cursor_x, self.cursor_height, 7, 7, 0, 0, 0)
            self.cursor_blink += 1
        cursor_xy = (self.cursor_x, self.cursor_height)
        if cursor_xy[1] == (self.y_height - 34):
            if cursor_xy[0] == 50:
                self.cursor_selection = "bombs"
            elif cursor_xy[0] == 44:
                self.cursor_selection = "boomerang"
            elif cursor_xy[0] == 56:
                self.cursor_selection = "bow"
            else:
                self.cursor_selection = ""
        if cursor_xy[1] == (self.y_height - 28):
            self.cursor_selection = ""
            
        if self.cursor_selection in self.collected_items:
            my_player.active_item = self.cursor_selection
            
        
    def display_hearts(self, my_player):
        display.drawFilledRectangle(0, self.y_height - 1, 71, 5, 0)
        heart_map = bytearray([3,6,3])
        blank_map = bytearray([0,0,0])

        if my_player.hearts <= 3:
            if self.blink_timer >= 20:
                self.blink_timer = 0
            elif self.blink_timer > 10:
                display.blit(heart_map, 51, self.y_height, 3, 3, 1, 0, 0)
                self.blink_timer += 1
            else:
                display.blit(heart_map, 51, self.y_height, 3, 3, 0, 0, 0)
                self.blink_timer += 1
        else:
            display.blit(heart_map, 51, self.y_height, 3, 3, 0, 0, 0)
            
        current_hearts = my_player.hearts / 2
        if current_hearts > 0:
            display.setPixel(56, self.y_height, 1)
        if current_hearts > 1:
            display.setPixel(58, self.y_height, 1)
        if current_hearts > 2:
            display.setPixel(60, self.y_height, 1)
        if current_hearts > 3:
            display.setPixel(62, self.y_height, 1)
        if current_hearts > 4:
            display.setPixel(64, self.y_height, 1)
        if current_hearts > 5:
            display.setPixel(66, self.y_height, 1)
        if current_hearts > 6:
            display.setPixel(68, self.y_height, 1)
        if current_hearts > 7:
            display.setPixel(70, self.y_height, 1)
        if current_hearts > 8:
            display.setPixel(56, self.y_height, 1)
        if current_hearts > 9:
            display.setPixel(58, self.y_height + 2, 1)
        if current_hearts > 10:
            display.setPixel(60, self.y_height + 2, 1)
        if current_hearts > 11:
            display.setPixel(62, self.y_height + 2, 1)
        if current_hearts > 12:
            display.setPixel(64, self.y_height + 2, 1)
        if current_hearts > 13:
            display.setPixel(66, self.y_height + 2, 1)
        if current_hearts > 14:
            display.setPixel(68, self.y_height + 2, 1)
        if current_hearts > 15:
            display.setPixel(70, self.y_height + 2, 1)
        
    def display_rupees(self, font_handler, my_player):
        self.rupees = my_player.rupees_text
        rupee_map = bytearray([6,7,3])
        display.blit(rupee_map, 1, self.y_height, 3, 3, 0, 0, 0)
        display.blit(self.dash_map, 5, self.y_height + 1, 2, 1, 0, 0, 0)
        font_handler.write_white(self.rupees, 8, self.y_height)
    
    def display_keys(self, font_handler, my_player):
        self.keys = str(my_player.keys)
        key_map = bytearray([6,2,2,5,7])
        display.blit(key_map, 22, self.y_height, 5, 3, 0, 0, 0)
        display.blit(self.dash_map, 28, self.y_height + 1, 2, 1, 0, 0, 0)
        font_handler.write_white(self.keys, 31, self.y_height)
        
    def display_bombs(self, font_handler, my_player):
        self.bombs = str(my_player.bombs)
        bomb_map = bytearray([6,6,1])
        display.blit(bomb_map, 37, self.y_height, 3, 3, 0, 0, 0)
        display.blit(self.dash_map, 41, self.y_height + 1, 2, 1, 0, 0, 0)
        font_handler.write_white(self.bombs, 44, self.y_height)
        
    def display_items(self):
        for item in self.collected_items:
            if item == "boomerang":
                display.blit(bytearray([0,4,10,17,0]), 45, self.y_height - 33, 5, 5, -1, 0, 0)
                if self.cursor_selection == "boomerang":
                    display.blit(bytearray([0,8,28,54,34,0,0]), 11, self.y_height - 29, 7, 7, -1, 0, 0)
            if item == "bombs":
                display.blit(bytearray([0,28,30,29,0]), 51, self.y_height - 33, 5, 5, -1, 0, 0)
                if self.cursor_selection == "bombs":
                    display.blit(bytearray([0,24,60,62,61,24,0]), 11, self.y_height - 29, 7, 7, -1, 0, 0)
            if item == "bow": 
                display.blit(bytearray([0,31,17,14,0]), 57, self.y_height - 33, 5, 5, -1, 0, 0)
                if self.cursor_selection == "bow":
                    display.blit(bytearray([0,0,127,65,34,28,0]), 11, self.y_height - 29, 7, 7, -1, 0, 0)
            
            if self.cursor_selection == "":
                display.blit(bytearray([0,0,0,0,0,0,0]), 11, self.y_height - 29, 7, 7, -1, 0, 0)
        
    def pause_game(self, font_handler, my_player):
        
        # BITMAP: width: 70, height: 35
        menu_map = bytearray([0,0,0,10,14,10,0,14,2,140,64,70,72,70,64,78,76,136,0,14,2,12,0,2,14,2,0,14,10,14,0,14,6,12,0,6,12,6,0,0,0,0,252,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,252,0,
           0,0,0,0,0,0,0,0,0,63,64,64,64,64,64,64,64,63,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,64,32,144,32,64,128,0,0,0,127,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,128,127,0,
           0,0,0,238,200,238,0,168,238,162,0,46,236,40,0,224,64,224,0,0,0,0,0,0,128,64,32,144,72,36,18,9,4,2,1,0,1,2,4,9,18,36,72,144,32,64,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,14,14,12,0,0,0,0,0,0,0,0,0,0,0,0,0,0,40,236,42,9,232,106,203,10,170,234,170,10,234,106,42,10,234,170,234,10,234,106,202,10,235,170,168,9,234,204,136,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        if buttonA.pressed() and buttonB.pressed() and buttonU.pressed():
            self.is_paused = True
            print("Paused")
        while self.is_paused:
            if not self.deployed:
                while self.menu_y < 0:
                    display.fill(0)
                    self.menu_y += self.menu_speed
                    self.y_height += self.menu_speed
                    display.blit(menu_map, self.menu_x, self.menu_y, 70, 35, -1, 0, 0)
                    display.drawFilledRectangle(0, self.y_height - 1, 71, 5, 0)
                    self.display_hearts(my_player)
                    self.display_rupees(font_handler, my_player)
                    self.display_keys(font_handler, my_player)
                    self.display_bombs(font_handler, my_player)
                    # self.display_items(display)
                    display.update()
                else:
                    self.deployed = True
                    self.retracted = False
                    print(self.y_height)
            
            
            if buttonA.pressed() and buttonB.pressed() and buttonU.pressed() and not self.retracted:
                if not self.retracted:
                    while self.menu_y > -35:
                        display.fill(0)
                        self.menu_y -= self.menu_speed
                        self.y_height -= self.menu_speed
                        display.blit(menu_map, self.menu_x, self.menu_y, 70, 35, -1, 0, 0)
                        # display.drawLine(44, self.y_height - 35, 69, self.y_height - 35, 1)
                        # display.drawLine(44, self.y_height - 21, 69, self.y_height - 21, 1)
                        # display.drawLine(43, self.y_height - 34, 43, self.y_height - 22, 1)
                        # display.drawLine(70, self.y_height - 34, 70, self.y_height - 22, 1)
                        display.drawFilledRectangle(0, self.y_height - 1, 71, 5, 0)
                        self.display_hearts(my_player)
                        self.display_rupees(font_handler, my_player)
                        self.display_keys(font_handler, my_player)
                        self.display_bombs(font_handler, my_player)
                        # self.display_items(display)
                        display.update()
                    else:
                        self.deployed = False
                        self.retracted = True
                        self.is_paused = False
                        print("Unpaused")
                        
            self.display_hearts(my_player)
            self.display_rupees(font_handler, my_player)
            self.display_keys(font_handler, my_player)
            self.display_bombs(font_handler, my_player)
            self.display_cursor(my_player)
            self.display_items()
            display.update()
            
        
        
        
        
        