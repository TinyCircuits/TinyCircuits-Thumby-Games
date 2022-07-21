import time
import thumby
import sys

CURRENT_FOLDER = '/Games/Flucht'
sys.path.insert(1, CURRENT_FOLDER)

import common_code

CONFIG_FILE_PATH = CURRENT_FOLDER + '/config.cfg'

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 72

class game_interface:
	sprites = dict()
	draw_offset = [0, 0]
	
	def setPixel(self, x, y, color):
		x += self.draw_offset[1]
		y += self.draw_offset[0]
		thumby.display.setPixel(int(y), int(x), color)
	
	def drawLine(self, x1, y1, x2, y2, color):
		x1 += self.draw_offset[1]
		y2 += self.draw_offset[0]
		x1 += self.draw_offset[1]
		y2 += self.draw_offset[0]
		thumby.display.drawLine(int(y1), int(x1), int(y2), int(x2), color)
		
	def drawRectangle(self, x, y, w, h, color):
		x += self.draw_offset[1]
		y += self.draw_offset[0]
		thumby.display.drawRectangle(int(y), int(x), int(h), int(w), color)
		
	def drawFilledRectangle(self, x, y, w, h, color):
		x += self.draw_offset[1]
		y += self.draw_offset[0]
		thumby.display.drawFilledRectangle(int(y), int(x), int(h), int(w), color)
	
	def fill(self, color):
		thumby.display.fill(color)

	def drawSprite(self, name):
		sprite = self.sprites[name]
		
		sprite.x += self.draw_offset[1]
		sprite.y += self.draw_offset[0]
		
		if sprite.x <= SCREEN_HEIGHT and sprite.x + sprite.width >= 0:
			thumby.display.drawSprite(sprite)
		
		sprite.x -= self.draw_offset[1]
		sprite.y -= self.draw_offset[0]
	
	def drawSprite_location(self, name, x, y):
		
		sprite = self.sprites[name]
		sprite.x = y
		sprite.y = x
		
		self.drawSprite(name)

	def get_current_time(self):
		return time.ticks_ms() * 0.001
	
	def init_sprite(self, name, width, height, data, x, y, key=-1):
		if not name in self.sprites:
			self.sprites[name] = thumby.Sprite(width, height, data, y, x, key=key)

	def save_data(self, data_dict):
		with open(CONFIG_FILE_PATH, 'w') as file:
			for key in data_dict:
				file.write(str(key) + ':' + str(data_dict[key]))
		
	def load_data(self):
		data_dict = {}
		
		try:
			with open(CONFIG_FILE_PATH, 'r') as file:
				for line in file:
					tokens = line.split(':')
					if len(tokens) >= 2:
						key = tokens[0]
						value = ':'.join(tokens[1:])
						data_dict[key] = value
		except:
			pass			
		return data_dict

_game_interface = game_interface()

thumby.display.setFPS(60)

last_frame_timestamp = _game_interface.get_current_time()

while True:
	current_frame_timestamp = _game_interface.get_current_time()
	delta_time = current_frame_timestamp - last_frame_timestamp
	last_frame_timestamp = current_frame_timestamp
	
	pressed = thumby.buttonA.pressed() or thumby.buttonB.pressed() or thumby.buttonU.pressed() or thumby.buttonD.pressed() or thumby.buttonL.pressed() or thumby.buttonR.pressed()
	common_code.game_loop(pressed, delta_time, _game_interface)

	thumby.display.update()