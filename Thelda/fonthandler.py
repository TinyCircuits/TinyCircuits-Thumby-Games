from thumby import display

class FontHandler:
    def __init__(self):
        
        #Not enough room for 'space' in letters_raw, so I added the byte array for space to it separately.
        self.space = bytearray([7,7,7,7])# BITMAP: width: 4, height: 3
        # FONT BITMAP: width: 144, height: 3 
        self.letters_white_raw = self.space + bytearray([6,1,6,0,7,7,6,0,2,5,5,0,7,5,2,0,7,6,4,0,7,3,1,0,7,5,6,0,7,2,7,0,0,7,0,0,6,4,7,0,7,2,5,0,7,4,4,0,7,3,7,0,7,1,6,0,2,5,2,0,7,3,3,0,2,5,6,0,7,3,6,0,4,7,1,0,1,7,1,0,7,4,7,0,3,4,3,0,7,6,7,0,5,2,5,0,3,6,3,0,1,7,4,0,7,5,7,0,1,7,0,0,1,7,4,0,1,3,6,0,3,2,7,0,4,7,1,0,7,6,6,0,1,1,7,0,6,7,6,0,3,3,7,0])
        self.letters_raw = self.space + bytearray([1,6,1,7,0,0,1,7,5,2,2,7,0,2,5,7,0,1,3,7,0,4,6,7,0,2,1,7,0,5,0,7,7,0,7,7,1,3,0,7,0,5,2,7,0,3,3,7,0,4,0,7,0,6,1,7,5,2,5,7,0,4,4,7,5,2,1,7,0,4,1,7,3,0,6,7,6,0,6,7,0,3,0,7,4,3,4,7,0,1,0,7,2,5,2,7,4,1,4,7,6,0,3,7,0,2,0,7,6,0,7,7,6,0,3,7,6,4,1,7,4,5,0,7,3,0,6,7,0,1,1,7,6,6,0,7,1,0,1,7,4,4,0,7])
        self.letter_maps = [] # this will hold lists of each letter's byte array values
        self.white_letter_maps = [] # this will hold lists of each letter's byte array values
        self.chunk_size = 3
        self.count = 0
        self.this_letter_map = []
        self.this_white_letter_map = []
        for number in self.letters_raw:
            if self.count < self.chunk_size:
                self.this_letter_map.append(number)
                self.count += 1
            else:
                self.letter_maps.append(self.this_letter_map)
                self.this_letter_map = []
                self.count = 0
                
        for number in self.letters_white_raw:
            if self.count < self.chunk_size:
                self.this_white_letter_map.append(number)
                self.count += 1
            else:
                self.white_letter_maps.append(self.this_white_letter_map)
                self.this_white_letter_map = []
                self.count = 0
        
        self.font_index = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        self.letter_dict = dict((char, position) for position, char in enumerate(self.font_index))
        
        self.alphabet = {}
        self.white_alphabet = {}
        
        for char in self.letter_dict:
            indv_char = self.letter_dict[char]
            char_map = self.letter_maps[indv_char]
            self.alphabet.update({char:bytearray(char_map)})
            
        for char in self.letter_dict:
            indv_char = self.letter_dict[char]
            char_map = self.white_letter_maps[indv_char]
            self.white_alphabet.update({char:bytearray(char_map)})
        
        
    def write(self, text, x: int, y: int):
            text = text.upper()
            for character in text:
                char_to_print = self.alphabet[character]
                display.blit(char_to_print, x, y, 3, 3, 1, 0, 0)
                x += 4
    
    
    def write_white(self, text, x: int, y: int):
            text = text.upper()
            for character in text:
                char_to_print = self.white_alphabet[character]
                display.blit(char_to_print, x, y, 3, 3, -1, 0, 0)
                x += 4

