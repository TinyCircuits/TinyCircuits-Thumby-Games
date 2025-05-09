import thumby
from thumby import display as dp
import math
import random

# User configuration
NEXT_MODE_AFTER = 10 # Default: 10 / after n chars, the mode changes / final mode remains
SAVE_HIGHSCORE = False # saveData seems not to work on Thumby / get stuck in main menu
CHAR_SET = 9 # for full alphabet: 26
CHAR_SIZE = 40 # 40 for entire screen
FRAMES = 10 # set frames per second / this game does not require many frames per second


class Stretcher8x8():
    # reads pixels from drawn char and stretches pixel to CHAR_SIZE
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = []
        self.font_path = "/lib/font8x8.bin"
        
        # BITMAP: width: 72, height: 30
        title_map = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,62,42,42,62,0,0,62,32,32,62,0,0,62,10,26,46,0,0,62,12,16,62,0,0,7,0,46,42,58,0,0,0,0,0,0,0,0,0,
           255,254,252,252,252,254,7,7,7,199,198,196,196,196,198,199,255,255,255,6,4,4,252,254,255,7,7,7,254,252,252,4,6,7,199,199,199,6,4,4,252,254,255,7,7,7,230,228,228,228,6,7,15,255,255,254,12,172,172,14,255,15,239,239,30,252,12,172,174,255,255,255,
           255,255,255,255,255,255,0,0,0,127,127,127,127,127,127,127,255,255,255,0,0,0,241,241,241,0,0,0,255,255,255,0,0,0,249,249,249,0,0,0,255,255,255,0,0,0,240,240,192,0,12,60,254,255,255,255,250,251,251,250,251,250,250,250,251,251,250,250,250,255,255,255,
           63,31,15,15,15,31,60,60,60,60,28,12,12,12,28,60,63,63,31,12,12,28,63,63,63,28,12,12,15,31,63,60,60,28,15,15,15,28,60,60,63,31,15,12,12,28,63,63,63,31,12,12,12,31,63,63,63,31,15,15,15,31,63,63,63,31,15,15,15,31,63,63])
        self.title = thumby.Sprite(72,30, title_map, 0,0)
        
    def set_matrix(self, char):
        # transform to stretched char / matrix is nested listed with each nested list represents a column
        self.draw_reference(char)
        char_matrix = self.get_matrix()
        new_matrix = []
        for y in range(0, len(char_matrix)):
            new_matrix.append(self.stretch_dimension(char_matrix[y], self.height))
        self.matrix = self.stretch_dimension(new_matrix, self.width)
        
        
    def get_sprites(self, char):
        # return stretched sprite from char
        self.set_matrix(char)
        arr = self.matrix_to_array()
        a = []
        for i in range(0, len(arr)):
            a.append(255 - arr[i])
        return (thumby.Sprite(self.width, self.height, bytearray(arr), 0, 0), thumby.Sprite(self.width, self.height, bytearray(a), 0, 0))
        
        
    def draw_reference(self, char):
        # draws char for deriving original pixel matrix
        dp.fill(0)
        self.draw_title()
        dp.setFont(self.font_path, 8, 8, 1)
        dp.drawText(char, 0, 0, 1)
        self.add_loading_info()
        dp.update()
        
        
    def draw_title(self):
        # draws game title
        dp.drawSprite(self.title)
        
    
    def add_loading_info(self):
        # draws loading information with random number of dots to give it more a dynamic look
        dots = random.choice(['.', '..', '...'])
        dp.drawText("Load" + dots, 0 , 30, 1)
        

    def draw_pixels(self):
        # draws all pixels from current matrix / not needed in this game
        for x in range(0, self.width):
            for y in range(0, self.height):
                dp.setPixel(x, y, self.matrix[x][y])
        
    
    def stretch_dimension(self, array , new_size):
        # stretches reference iterable to defined size / array can be a column list or the entire matrix
        new_array = []
        n = len(array)
        i = 1
        for x in range(0, new_size):
            while x/new_size  >= i/n:
                i += 1
            new_array.append(array[i-1])
        return new_array
    
    def get_matrix(self):
        # Reference char is in top-left corner
        matrix = []
        for x in range(0,8):
            matrix.append(self.get_col(x))
        return matrix
    
    def get_col(self, x):
        # returns pixel column from reference char
        col = []
        for y in range(0,8):
            col.append(dp.getPixel(x, y))
        return col
        
        
    def matrix_to_array(self):
        # transforms nested matrix to flat list where each index contains the value of a byte-sized column
        l = []
        height = len(self.matrix[0])
        for j in range(0, math.ceil(height/8)):
            for i in range(0, len(self.matrix)):
                end_index = min(height, (j+1)*8)
                l.append(self.col_to_int(self.matrix[i][j*8:end_index]))
        return l
        
    def col_to_int(self, row):
        # bit list to int value
        n = 0
        for i in range(0, len(row)):
            n += row[i]*2**i
        return n
        
        
class Screen():
    # base class for CharScreen and InstructScreen
    def __init__(self):
        pass
    
    def draw_bg(self, color):
        dp.fill(color)
        
    def draw_fg(self, color):
        pass
    
    def draw(self, color):
        self.draw_bg(color)
        self.draw_fg(color)

class InstructScreen(Screen):
    # generates instruction screens
    def __init__(self, mode):
        Screen.__init__(self)
        self.mode = mode
        self.game_ended = False
    
    def draw_fg(self, color):
        dp.setFont("/lib/font5x7.bin", 5, 7 , color)
        if self.mode == 0:
            self.draw_set("CHAR TYPE", "Left: letter", "A: digit", ">> press A")
        elif self.mode == 1:
            self.draw_set("CHAR COLOR", "Left: black", "A: white", ">> press A")
        else:
            self.draw_set("ITERATE RULES", "2x char type", "then 2x color", ">> press A")
        self.game_ended = False
        self.wait_for_player()
      
        
        
    def game_over(self, color, score):
        self.game_ended = True
        self.draw_bg(color)
        highscore = Highscore.get()
        if score >= highscore:
            title = "SCORE: " + str(score) # change score to New HS:
            replay = "Replay?"
        else:
            title = "SCORE: " + str(score)
            replay = "Beat HS: " + str(highscore) +  "!"
        self.draw_set(title, replay, "Left: No", "A: Yes")
        self.wait_for_player()
        
    
    def draw_set(self, headline, first, second, third):
        dp.drawText(headline, 0, 0, 1) # string, x, y, color
        dp.drawLine(0, 8, 62, 8, 1)
        dp.drawText(first, 0, 12, 1)
        dp.drawText(second, 0, 21, 1)
        dp.drawText(third, 0, 30, 1)
        

    def wait_for_player(self):
        while not Player.pressed_A():
            if self.game_ended and Player.pressed_L():
                thumby.reset()
            dp.update()

        
class CharScreen(Screen):
    # generates screens where the char is centered
    def __init__(self, char, stretcher):
        Screen.__init__(self)
        self.char = char
        self.is_letter = char.isalpha()
        self.is_digit = not self.is_letter
        self.stretcher = stretcher
        self.sprite_w, self.sprite_b = stretcher.get_sprites(char)
        self.center_sprite(self.sprite_w)
        self.center_sprite(self.sprite_b)
        self.color = 0
        self.sprites = (self.sprite_w, self.sprite_b)
        
    def center_sprite(self, sprite):
        sprite.x = int((dp.width - sprite.width)/2)
        sprite.y = int((dp.height - sprite.height+ 4)/2)
        
    def draw_fg(self, color):
        dp.drawSprite(self.sprites[color])
 
    def draw(self, color):
        self.color = color
        self.draw_bg(color)
        self.draw_fg(color)


class Ruleset():
    # compares user input with current ruleset (mode)
    def __init__(self):
        self.mode = 0
        self.i = 0
        self.rule_iteration = 2
        self.rule_letter = False # starts with digit comparison
        
    def update_counter(self):
        # switches between the first two modes after two charscreens when in final mode
        if (self.i >= self.rule_iteration) and self.mode == 2:
            self.i = 0
            self.rule_letter = not self.rule_letter
        self.i += 1
        
    def check(self, btn, char):
        # btn 0: leftD, 1: A ; char: active_screen
        self.update_counter()
        
        if self.mode == 0:
            return self.check_letter_digit(btn,char)  
        elif self.mode == 1:
            return self.check_black_white(btn,char) 
        elif self.mode == 2:
            return self.check_sequence(btn,char)
        return False
        
        
    def check_letter_digit(self, btn, char):
        if btn == 0 and char.is_letter:
            return True
        elif btn == 1 and char.is_digit:
            return True
        return False
        
    def check_black_white(self,btn, char):
        if btn == 0 and char.color == 1: # char is black
            return True
        elif btn == 1 and char.color == 0: # char is white
            return True
        return False
        
    def check_sequence(self, btn, char):
        if self.rule_letter:
            return self.check_letter_digit(btn, char)
        return self.check_black_white(btn,char)

class Player():
    # contains user interactions
    @staticmethod
    def pressed_L():
        return thumby.buttonL.justPressed()
        
    @staticmethod
    def pressed_A():
        return thumby.buttonA.justPressed()
        
        
class Highscore():
    # contains highscore interactions
    @staticmethod
    def init():
        if not SAVE_HIGHSCORE: return
        thumby.saveData.setName("BurnsCharade")
        
    @staticmethod
    def get():
        if not SAVE_HIGHSCORE: return -1 
        if(thumby.saveData.hasItem("highscore")):
            return int(thumby.saveData.getItem("highscore"))
        return 0
        
    @staticmethod
    def set(score):
        if not SAVE_HIGHSCORE: return
        if(score > Highscore.get()):
            thumby.saveData.setItem("highscore", score)
            thumby.saveData.save()
            
class Game():
    # contains game logic and loop
    def __init__(self, screens):
        self.screens = screens
        self.highscore = 0
        self.colors = [0,1,1,0]
        self.instructs = [  InstructScreen(0),
                            InstructScreen(1),
                            InstructScreen(2),
                            InstructScreen(3)
                        ]
        self.first = True
        self.reset()
        
    def game_over(self):
        self.instructs[3].game_over(0, self.highscore)
        return self.reset()
                        
    def reset(self):
        self.update_highscore()
        self.highscore = -1
        self.rs = Ruleset()
        self.instructs[0].draw(0)
        self.current = random.choice(screens)
        self.current.draw(random.choice(self.colors))
        self.last = None
        dp.update()
        return 1
        
        
    def update_highscore(self):
        Highscore.set(self.highscore)
        
    
    def change_mode(self):
        if self.highscore == NEXT_MODE_AFTER*2:
            self.rs.mode = 2
            self.instructs[self.rs.mode].draw(0)
        elif self.highscore == NEXT_MODE_AFTER :
            self.rs.mode = 1
            self.instructs[self.rs.mode].draw(0)

    def act(self):
        # check user interactions
        if Player.pressed_L():
           is_correct = self.rs.check(0, self.current)
        elif Player.pressed_A():
           is_correct = self.rs.check(1, self.current)
        else:
            return self.highscore
        if is_correct:
            return self.highscore + 1
        else:
            return self.game_over()
            
       
    def loop(self):
        # game loop / update loop
        while(True):
            new_hs = self.act()
            if self.first:
                new_hs = 0
                self.first = False
            if new_hs > self.highscore:
                self.highscore = new_hs
                while self.current is self.last:
                    self.current = random.choice(self.screens)
                self.last = self.current
                self.change_mode()
                self.current.draw(random.choice(self.colors))
            dp.update()


dp.setFPS(FRAMES) 
Highscore.init()

# load char set
chars = []
# get letters
for i in range(65, 66 + CHAR_SET): 
    chars.append(chr(i))
# get digits
for i in  range(1,1 + CHAR_SET): 
    chars.append(str(i))

stretcher = Stretcher8x8(CHAR_SIZE,CHAR_SIZE)
screens = [] 
for i in range(0, len(chars)):
    screens.append(CharScreen(chars[i], stretcher))


game = Game(screens)
game.loop()
    

   
      
    