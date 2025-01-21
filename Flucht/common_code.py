import math
import random

############# UTILS #############

def clamp(num, min_value, max_value):
	return max(min(num, max_value), min_value)

def lerp(ratio, min_value, max_value):
	return min_value + ratio * (max_value - min_value)

# CONSTANTS

SCREEN_WIDTH = 40
SCREEN_HEIGHT = 72

WALL_WIDTH = 3

TESTING_MODE = False
GOD_MODE = False or TESTING_MODE
DRAW_PARTICLES = True

DEBUG_DRAW_FPS = False

PLAYER_WIDTH = 5
PLAYER_HEIGHT = PLAYER_WIDTH

GRAVITY = 120.0
MAX_SPEED = 900.0

JUMP_INITIAL_SPEED_Y = 100.0 if TESTING_MODE else 30.0
JUMP_INITIAL_SPEED_X = 60.0

JUMP_SPEED_CONTINUATION_SPEED_Y = JUMP_INITIAL_SPEED_Y * 2.0
JUMP_SPEED_CONTINUATION_SPEED_X = JUMP_INITIAL_SPEED_X
JUMP_CHAIN_BOOST_FACTOR = 1.25

SCROLL_MIN_HEIGHT = round(SCREEN_HEIGHT * 0.5)

KEY_PRESS_BUFFER_TIME = 0.2

SCREENSHAKE_AFTER_GAMEOVER_TIME = 0.3

# accumulating speed
JUMP_KEY_TIME_ACCUMULATE = 0.2
NUM_JUMPS_FOR_ACCUMULATE = 2
ACCUM_SPEED_FACTOR = 1.3

MAX_GRAB_TIME_FOR_ACCUM_TO_CONTINUE = 0.1

TIME_TO_IGNORE_INPUT_AFTER_GAMEOVER = 1.0

sprite_sizes = dict()

def generate_sprites(game_interface):
	global sprite_sizes
	
	def generate_sprite(name, anchor_x, anchor_y, sprite, key=-1):
		global sprite_sizes
	
		TRANSPOSE = True
		SPRITE_HEIGHT = len(sprite)
		SPRITE_WIDTH = len(sprite[0])
		
		sprite_sizes[name] = [SPRITE_WIDTH, SPRITE_HEIGHT]
		
		if TRANSPOSE:
			(SPRITE_HEIGHT, SPRITE_WIDTH) = (SPRITE_WIDTH, SPRITE_HEIGHT)
		
		SPRITE_BYTE_ROWS = SPRITE_HEIGHT // 8
		if SPRITE_HEIGHT % 8 != 0:
			SPRITE_BYTE_ROWS += 1

		data = []
				
		for row_index in range(SPRITE_BYTE_ROWS):
			for x in range(SPRITE_WIDTH):
				byte = 0
				y = row_index * 8
				
				row_height = 8
				if row_index == SPRITE_BYTE_ROWS - 1:
					if SPRITE_HEIGHT % 8 != 0:
						row_height = SPRITE_HEIGHT % 8
						
				for bit_offset in range(row_height):
					
					value = sprite[SPRITE_WIDTH - x - 1][y] if TRANSPOSE else sprite[y][x]
					
					if value != ' ':
						byte += 1 << bit_offset
					
					y += 1
				
				data.append(byte)

		game_interface.init_sprite(name, SPRITE_WIDTH, SPRITE_HEIGHT, bytearray(data), anchor_x, anchor_y, key)
		
	def generate_sprite_mirrored(name, anchor_x, anchor_y, sprite, key=-1):
		generate_sprite(name + '_LEFT',  anchor_x, anchor_y, sprite,                                  key)
		generate_sprite(name + '_RIGHT', anchor_x, anchor_y, [list(reversed(row)) for row in sprite], key)
		
	generate_sprite('SPRITE_TITLE', 0, 56, [
		'                                        ',
		'                                        ',
		'                                        ',
		'  xxxxxx xx                xx       xx  ',
		'  xxxxxx xx                xx       xx  ',
		'  xx     xx xx   xx  xxxxx xxxxxx  xxxx ',
		'  xx     xx xx   xx xxxxxx xxxxxxx xxxx ',
		'  xxxx   xx xx   xx xx     xx   xx  xx  ',
		'  xxxx   xx xx   xx xx     xx   xx  xx  ',
		'  xx     xx xx   xx xx     xx   xx  xx  ',
		'  xx     xx xx   xx xx     xx   xx  xx  ',
		'  xx     xx xxxxxxx xxxxxx xx   xx  xx  ',
		'  xx     xx  xxxxx   xxxxx xx   xx  xx  ',
		'                                        ',
		'                                        ',
		'                                        ',
	])
	
	generate_sprite('SPRITE_SCORE', 0, 58, [
		'                                        ',
		'                                        ',
		'                                        ',
		'    xxxxx                               ',
		'   xxxxxx  xxxx  xxxx  xxxx  xxxx  xx   ',
		'   xx     xxxxx xxxxxx xxxx xxxxxx xx   ',
		'   xxxxx  xx    xx  xx xx   xx  xx      ',
		'    xxxxx xx    xx  xx xx   xxxxxx      ',
		'       xx xx    xx  xx xx   xx          ',
		'   xxxxxx xxxxx xxxxxx xx   xxxxxx xx   ',
		'   xxxxx   xxxx  xxxx  xx    xxxxx xx   ',
		'                                        ',
		'                                        ',
		'                                        ',
	])
	
	generate_sprite('SPRITE_BEST', 6, 28, [
		'                            ',
		'                            ',
		'  xxxx               x      ',
		'  x   x  xxx   xxxx xxxx x  ',
		'  xxxx  x   x x      x      ',
		'  x   x xxxxx  xxx   x      ',
		'  x   x x         x  x      ',
		'  xxxx   xxxx xxxx    xx x  ',
		'                            ',
		'                            ',
	])
	
	generate_sprite('SPRITE_DIGIT_0', 0, 0, [
		'xxxxx',
		'xxxxx',
		'xx xx',
		'xx xx',
		'xx xx',
		'xx xx',
		'xxxxx',
		'xxxxx',
	])
	generate_sprite('SPRITE_DIGIT_1', 0, 0, [
		'  xx ',
		'  xx ',
		'  xx ',
		'  xx ',
		'  xx ',
		'  xx ',
		'  xx ',
		'  xx ',
	])
	generate_sprite('SPRITE_DIGIT_2', 0, 0, [
		'xxxxx',
		'xxxxx',
		'   xx',
		'xxxxx',
		'xxxxx',
		'xx   ',
		'xxxxx',
		'xxxxx',
	])
	generate_sprite('SPRITE_DIGIT_3', 0, 0, [
		'xxxxx',
		'xxxxx',
		'   xx',
		' xxxx',
		' xxxx',
		'   xx',
		'xxxxx',
		'xxxxx',
	])
	generate_sprite('SPRITE_DIGIT_4', 0, 0, [
		'xx xx',
		'xx xx',
		'xx xx',
		'xxxxx',
		'xxxxx',
		'   xx',
		'   xx',
		'   xx',
	])
	generate_sprite('SPRITE_DIGIT_5', 0, 0, [
		'xxxxx',
		'xxxxx',
		'xx   ',
		'xxxxx',
		'xxxxx',
		'   xx',
		'xxxxx',
		'xxxxx',
	])
	generate_sprite('SPRITE_DIGIT_6', 0, 0, [
		'xxxxx',
		'xxxxx',
		'xx   ',
		'xxxxx',
		'xxxxx',
		'xx xx',
		'xxxxx',
		'xxxxx',
	])
	generate_sprite('SPRITE_DIGIT_7', 0, 0, [
		'xxxxx',
		'xxxxx',
		'   xx',
		'   xx',
		'   xx',
		'   xx',
		'   xx',
		'   xx',
	])
	generate_sprite('SPRITE_DIGIT_8', 0, 0, [
		'xxxxx',
		'xxxxx',
		'xx xx',
		'xxxxx',
		'xxxxx',
		'xx xx',
		'xxxxx',
		'xxxxx',
	])
	generate_sprite('SPRITE_DIGIT_9', 0, 0, [
		'xxxxx',
		'xxxxx',
		'xx xx',
		'xxxxx',
		'xxxxx',
		'   xx',
		'xxxxx',
		'xxxxx',
	])
	
	generate_sprite('SPRITE_DIGIT_SMALL_0', 0, 0, [
		'xxx',
		'x x',
		'x x',
		'x x',
		'xxx',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_1', 0, 0, [
		' x ',
		' x ',
		' x ',
		' x ',
		' x ',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_2', 0, 0, [
		'xxx',
		'  x',
		'xxx',
		'x  ',
		'xxx',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_3', 0, 0, [
		'xxx',
		'  x',
		'xxx',
		'  x',
		'xxx',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_4', 0, 0, [
		'x x',
		'x x',
		'xxx',
		'  x',
		'  x',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_5', 0, 0, [
		'xxx',
		'x  ',
		'xxx',
		'  x',
		'xxx',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_6', 0, 0, [
		'xxx',
		'x  ',
		'xxx',
		'x x',
		'xxx',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_7', 0, 0, [
		'xxx',
		'  x',
		'  x',
		'  x',
		'  x',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_8', 0, 0, [
		'xxx',
		'x x',
		'xxx',
		'x x',
		'xxx',
	])
	generate_sprite('SPRITE_DIGIT_SMALL_9', 0, 0, [
		'xxx',
		'x x',
		'xxx',
		'  x',
		'xxx',
	])
	
	generate_sprite_mirrored('SPRITE_WALL', 0, 0, [
		' xx',
		' xx',
		' xx',
		'  x',
		'  x',
		' xx',
		' xx',
		'  x',
		'  x',
	])
	
	generate_sprite_mirrored('SPRITE_SPIKE', 0, 0, [
		'xxx   ',
		'xxxxxx',
		'xxx   ',
	])
	
	generate_sprite_mirrored('SPRITE_WEEDS_1', 0, 0, [
		'  x',
		'xx ',
		'   ',
		'x  ',
		' x ',
	])
	
	generate_sprite_mirrored('SPRITE_WEEDS_2', 0, 0, [
		'x  ',
		'  x',
		'xx ',
		'   ',
		'x  ',
		' x ',
	])
	
	generate_sprite_mirrored('SPRITE_WEEDS_3', 0, 0, [
		'  x ',
		'xx x',
		'  x ',
		'    ',
		'xx  ',
		'  x ',
	])
	
	generate_sprite_mirrored('SPRITE_BRICKS_1', 0, 0, [
		'    xxx      ',
		'             ',
		'  xxx xxx xxx',
		'             ',
		'xxx xxx xxx  ',
		'             ',
		'  xxx xxx xxx',
		'             ',
		'        xxx  ',
	])
		
	generate_sprite_mirrored('SPRITE_BRICKS_2', 0, 0, [
		'    xxx  ',
		'         ',
		'  xxx xxx',
		'         ',
		'xxx xxx  ',
		'         ',
		'  xxx xxx',
	])
		
	generate_sprite_mirrored('SPRITE_BRICKS_3', 0, 0, [
		'  xxx    ',
		'         ',
		'xxx xxx  ',
		'         ',
		'  xxx xxx',
	])

def get_random_from_list_without_repeating(full_list, recent_indices, recent_capacity):
	index = random.randrange(0, len(full_list))
	
	while index in recent_indices:
		index = random.randrange(0, len(full_list))
	
	if len(recent_indices) == recent_capacity:
		recent_indices.pop(0)
	
	recent_indices.append(index)
	
	return full_list[index]

# AUX CLASSES

class BackgroundElement:
	world_pos = [0.0, 0.0]
	parallax_factor = 1
	sprite_name = ''
	
	def __init__(self, pos = [0.0, 0.0], parallax_factor = 1, sprite_name = ''):
		self.world_pos = pos
		self.parallax_factor = parallax_factor
		self.sprite_name = sprite_name
	
	def draw(self, game_interface, camera_bottom_y):
		x = self.world_pos[0]
		y = (self.world_pos[1] - camera_bottom_y) // self.parallax_factor
		h = sprite_sizes[self.sprite_name][1]
		if y <= SCREEN_HEIGHT and y + h >= 0:
			game_interface.drawSprite_location(self.sprite_name, x, y)
		pass

class Particle:
	pos = [0.0, 0.0]
	vel = [0.0, 0.0]
	
	size = [1, 1]
	use_gravity = True
	time_left = float("inf")
	blink_time = 0.0
	blink_rate = 3.0/60
	gravity_factor = 1.0
	
	def __init__(self, pos = [0.0, 0.0], vel = [0.0, 0.0], use_gravity = True, time_left = float("inf"), blink_time = 0.0, blink_rate = 3.0/60, gravity_factor = 1.0, size = [1, 1]):
		self.pos = pos
		self.vel = vel
		self.use_gravity = use_gravity
		self.time_left = time_left
		self.blink_time = blink_time
		self.blink_rate = blink_rate
		self.gravity_factor = gravity_factor
		self.size = size

# STATE

STATE_TITLE_SCREEN          = 0
STATE_GAME_OVER             = 1
STATE_GRABBING_LEFT         = 2
STATE_GRABBING_RIGHT        = 3
STATE_JUMPING_LEFT_ACTIVE   = 4
STATE_JUMPING_LEFT_PASSIVE  = 5
STATE_JUMPING_RIGHT_ACTIVE  = 6
STATE_JUMPING_RIGHT_PASSIVE = 7

STATE_NAMES = {
	STATE_TITLE_SCREEN:          'STATE_TITLE_SCREEN',
	STATE_GAME_OVER:             'STATE_GAME_OVER',
	STATE_GRABBING_LEFT:         'STATE_GRABBING_LEFT',
	STATE_GRABBING_RIGHT:        'STATE_GRABBING_RIGHT',
	STATE_JUMPING_LEFT_ACTIVE:   'STATE_JUMPING_LEFT_ACTIVE',
	STATE_JUMPING_LEFT_PASSIVE:  'STATE_JUMPING_LEFT_PASSIVE',
	STATE_JUMPING_RIGHT_ACTIVE:  'STATE_JUMPING_RIGHT_ACTIVE',
	STATE_JUMPING_RIGHT_PASSIVE: 'STATE_JUMPING_RIGHT_PASSIVE',
}
	
current_state = STATE_TITLE_SCREEN
	
def StateIsGrabbing():
	return current_state in (STATE_GRABBING_LEFT, STATE_GRABBING_RIGHT)
	
def StateIsJumping():
	return current_state in (STATE_JUMPING_LEFT_ACTIVE, STATE_JUMPING_LEFT_PASSIVE, STATE_JUMPING_RIGHT_ACTIVE, STATE_JUMPING_RIGHT_PASSIVE)
	
def StateIsJumpingLeft():
	return current_state in (STATE_JUMPING_LEFT_ACTIVE, STATE_JUMPING_LEFT_PASSIVE)
	
def StateIsJumpingRight():
	return current_state in (STATE_JUMPING_RIGHT_ACTIVE, STATE_JUMPING_RIGHT_PASSIVE)
	
def StateIsJumpingActive():
	return current_state in (STATE_JUMPING_LEFT_ACTIVE, STATE_JUMPING_RIGHT_ACTIVE)
	
def StateIsJumpingPassive():
	return current_state in (STATE_JUMPING_LEFT_PASSIVE, STATE_JUMPING_RIGHT_PASSIVE)

def StateIsPlaying():
	return StateIsGrabbing() or StateIsJumping()

time_since_last_state_change = 0.0

f_camera_bottom_y = 0.0

player_size = []
player_pos = []
player_vel = []
player_rect = []

key_was_pressed = False

key_pressed_start_time = 0.0

jump_start_time = 0.0
grab_start_time = 0.0

last_blink_start = 0.0

full_jump_chain = 0
is_boosting = False
last_boost_particle_gen_time = 0.0

game_over_time = 0.0

time_since_game_start = 0.0

background_elements = []
wall_elements_left = []
wall_elements_right = []
hazards_left = []
hazards_right = []
particles = []

frame_num = 0
last_score = 0

is_grounded = False
time_since_grounded = 0.0

recent_bg_elements = []
recent_wall_elements = []

LEVEL_GEN_HAZARD_START_HEIGHT = SCREEN_HEIGHT
LEVEL_GEN_BG_ELEM_START_HEIGHT = SCREEN_HEIGHT // 2
LEVEL_GEN_WALL_ELEM_START_HEIGHT = 0

LEVEL_GEN_HAZARD_END_HEIGHT = SCREEN_HEIGHT * 30
LEVEL_GEN_HAZARD_START_SEPARATION = 100
LEVEL_GEN_HAZARD_START_SEPARATION_VARIATION = 40
LEVEL_GEN_HAZARD_START_SIZE_MIN = 2
LEVEL_GEN_HAZARD_START_SIZE_MAX = 3
LEVEL_GEN_HAZARD_END_SEPARATION = 50
LEVEL_GEN_HAZARD_END_SEPARATION_VARIATION = 20
LEVEL_GEN_HAZARD_END_SIZE_MIN = 4
LEVEL_GEN_HAZARD_END_SIZE_MAX = 4

LEVEL_GEN_BG_ELEM_SPRITE_NAMES = ['SPRITE_BRICKS_1_LEFT', 'SPRITE_BRICKS_2_LEFT', 'SPRITE_BRICKS_3_LEFT', 'SPRITE_BRICKS_1_RIGHT', 'SPRITE_BRICKS_2_RIGHT', 'SPRITE_BRICKS_3_RIGHT']
LEVEL_GEN_BG_ELEM_SEPARATION = 100
LEVEL_GEN_BG_ELEM_SEPARATION_VARIATION = 50
LEVEL_GEN_BG_ELEM_PARALLAX_FACTOR = 2

LEVEL_GEN_WALL_ELEM_SPRITE_NAMES = ['SPRITE_WEEDS_1', 'SPRITE_WEEDS_2', 'SPRITE_WEEDS_3']
LEVEL_GEN_WALL_ELEM_HAZARD_BUFFER = 5
LEVEL_GEN_WALL_ELEM_SEPARATION = 30
LEVEL_GEN_WALL_ELEM_SEPARATION_VARIATION = 10

LEVEL_GEN_HAZARDS_END_HEIGHT_MARGIN = 100
LEVEL_GEN_BG_ELEMS_END_HEIGHT_MARGIN = 20

LEVEL_GEN_MINIMUM_HEIGHT_INCREASE = 20
last_generation_height = -LEVEL_GEN_MINIMUM_HEIGHT_INCREASE

def create_level_elements(current_y_pos):
	global hazards_left
	global hazards_right
	global background_elements
	global wall_elements_left
	global wall_elements_right
	global last_generation_height
	
	# only actually generate by MINIMUM_HEIGHT_INCREASE_FOR_LEVEL_GEN increments, instead of each frame, etc.
	if current_y_pos >= last_generation_height + LEVEL_GEN_MINIMUM_HEIGHT_INCREASE:
		last_generation_height = current_y_pos
	else:
		return
		
	print('level gen at', current_y_pos)
	
	# background elements are generated in a smaller range,
	#   so that they can properly check overlaps against hazards
	#   (ensuring that they have been already generated)
	hazards_end_height  = current_y_pos + SCREEN_HEIGHT + LEVEL_GEN_HAZARDS_END_HEIGHT_MARGIN
	bg_elems_end_height = current_y_pos + SCREEN_HEIGHT + LEVEL_GEN_BG_ELEMS_END_HEIGHT_MARGIN
	
	# hazards
	if True:
		start_y_left  = hazards_left[-1][0]  if len(hazards_left)  > 0 else LEVEL_GEN_HAZARD_START_HEIGHT
		start_y_right = hazards_right[-1][0] if len(hazards_right) > 0 else LEVEL_GEN_HAZARD_START_HEIGHT
		
		ratio = float(current_y_pos - LEVEL_GEN_HAZARD_START_HEIGHT) / float(LEVEL_GEN_HAZARD_END_HEIGHT - LEVEL_GEN_HAZARD_START_HEIGHT)
		ratio = clamp(ratio, 0.0, 1.0)
		
		hazard_separation = round(lerp(ratio, float(LEVEL_GEN_HAZARD_START_SEPARATION), float(LEVEL_GEN_HAZARD_END_SEPARATION)))
		hazard_separation_variation = round(lerp(ratio, float(LEVEL_GEN_HAZARD_START_SEPARATION_VARIATION), float(LEVEL_GEN_HAZARD_END_SEPARATION_VARIATION)))
		hazard_size_min = round(lerp(ratio, float(LEVEL_GEN_HAZARD_START_SIZE_MIN), float(LEVEL_GEN_HAZARD_END_SIZE_MIN)))
		hazard_size_max = round(lerp(ratio, float(LEVEL_GEN_HAZARD_START_SIZE_MAX), float(LEVEL_GEN_HAZARD_END_SIZE_MAX)))
		
		hazard_size = hazard_size_min + round(random.random() * float(hazard_size_max - hazard_size_min))
		
		def generate_hazards(hazard_list, next_y):
			while True:
				next_y = next_y + random.randrange(
					hazard_separation - hazard_separation_variation,
					hazard_separation + hazard_separation_variation + 1)
				
				if next_y > hazards_end_height:
					break
				
				hazard_list.append([next_y, hazard_size])
		
		generate_hazards(hazards_left,  start_y_left)
		generate_hazards(hazards_right, start_y_right)
	
	# background elements
	if True:

		start_y = LEVEL_GEN_BG_ELEM_START_HEIGHT
		if len(background_elements) > 0:
			last_bg_elem = background_elements[-1]
			start_y = last_bg_elem.world_pos[1] + sprite_sizes[last_bg_elem.sprite_name][1]
		next_y = start_y
		
		while True:
			next_y = next_y + random.randrange(
				LEVEL_GEN_BG_ELEM_SEPARATION - LEVEL_GEN_BG_ELEM_SEPARATION_VARIATION,
				LEVEL_GEN_BG_ELEM_SEPARATION + LEVEL_GEN_BG_ELEM_SEPARATION_VARIATION + 1
			)
			
			if next_y // LEVEL_GEN_BG_ELEM_PARALLAX_FACTOR > bg_elems_end_height:
				break
			
			name = get_random_from_list_without_repeating(LEVEL_GEN_BG_ELEM_SPRITE_NAMES, recent_bg_elements, 3)
			sprite_width  = sprite_sizes[name][0]
			sprite_height = sprite_sizes[name][1]
			remaining_margin = (SCREEN_WIDTH - sprite_width) // 2
			margin = min(remaining_margin - 1, 10)
			
			x = random.randrange(margin, SCREEN_WIDTH - margin - sprite_width + 1)
			
			background_elements.append(BackgroundElement([x, next_y], LEVEL_GEN_BG_ELEM_PARALLAX_FACTOR, name))
			
			next_y += sprite_height
	
	# wall elements
	if True:
		
		start_y = LEVEL_GEN_WALL_ELEM_START_HEIGHT
		if len(wall_elements_left) > 0:
			last_elem = wall_elements_left[-1]
			elem_y = last_elem.world_pos[1] + sprite_sizes[last_elem.sprite_name][1]
			start_y = max(start_y, elem_y)
		if len(wall_elements_right) > 0:
			last_elem = wall_elements_right[-1]
			elem_y = last_elem.world_pos[1] + sprite_sizes[last_elem.sprite_name][1]
			start_y = max(start_y, elem_y)
		next_y = start_y
		
		while True:
			next_y = next_y + random.randrange(
				LEVEL_GEN_WALL_ELEM_SEPARATION - LEVEL_GEN_WALL_ELEM_SEPARATION_VARIATION,
				LEVEL_GEN_WALL_ELEM_SEPARATION + LEVEL_GEN_WALL_ELEM_SEPARATION_VARIATION + 1)
			
			if next_y > bg_elems_end_height:
				break
			
			name = get_random_from_list_without_repeating(LEVEL_GEN_WALL_ELEM_SPRITE_NAMES, recent_wall_elements, 1)
			is_left = (random.randrange(2) == 0)
			name += '_LEFT' if is_left else '_RIGHT'
			sprite_size = sprite_sizes[name]
			
			y = next_y
			x = (WALL_WIDTH) if is_left else (SCREEN_WIDTH - WALL_WIDTH - sprite_size[0])
		
			hazards_list = hazards_left if is_left else hazards_right
			wall_elements = wall_elements_left if is_left else wall_elements_right
			
			overlap = False
			for hazard in hazards_list:
				hazard_height = 4 * hazard[1]

				this_overlap = (y < hazard[0] + hazard_height + LEVEL_GEN_WALL_ELEM_HAZARD_BUFFER) and (y + sprite_size[1] > hazard[0] - LEVEL_GEN_WALL_ELEM_HAZARD_BUFFER)
				overlap = overlap or this_overlap
			
			if not overlap:
				wall_elements.append(BackgroundElement([x, y], 1, name))


def SwitchState(state):
	global current_state
	global time_since_last_state_change
	if current_state != state:
		current_state = state
		time_since_last_state_change = 0.0

def get_jump_speed_factor():
	return JUMP_CHAIN_BOOST_FACTOR if is_boosting else 1.0

def init_state(game_interface):
	global f_camera_bottom_y
	global background_elements
	global wall_elements_left
	global wall_elements_right
	global particles
	global hazards_left
	global hazards_right
	global player_size
	global player_pos
	global player_vel
	global player_rect
	global key_pressed_start_time
	global jump_start_time
	global grab_start_time
	global full_jump_chain
	global is_boosting
	global last_boost_particle_gen_time
	global last_blink_start
	global last_score
	global time_since_last_state_change
	global is_grounded
	global time_since_grounded
	global last_generation_height
	
	f_camera_bottom_y = 0.0
	last_generation_height = -LEVEL_GEN_MINIMUM_HEIGHT_INCREASE
	
	player_size = [PLAYER_WIDTH, PLAYER_HEIGHT]
	player_pos = [float(WALL_WIDTH), 2.0]
	player_vel = [0.0, 0.0]

	player_rect = [round(player_pos[0]), round(player_pos[1]), round(player_pos[0]) + player_size[0] - 1, round(player_pos[1]) + player_size[1] - 1]
	
	key_pressed_start_time = 0.0
	time_since_last_state_change = 0.0

	jump_start_time = 0.0
	grab_start_time = 0.0

	full_jump_chain = 0
	is_boosting = False
	
	last_blink_start = time_since_game_start
	
	last_score = 0
	
	is_grounded = True
	time_since_grounded = 0.0

	particles = []
	
	hazards_left = [[50, 3]]
	hazards_right = []
	
	background_elements = []
	wall_elements_left = []
	wall_elements_right = []
	
	create_level_elements(SCREEN_HEIGHT)

fps_list = [0.0] * 10
current_fps_index = 0
	
save_data = {}

def game_loop(key_pressed, delta_time, game_interface):
	global f_camera_bottom_y
	global key_was_pressed
	global player_size
	global player_pos
	global player_vel
	global player_rect
	global key_pressed_start_time
	global jump_start_time
	global grab_start_time
	global full_jump_chain
	global frame_num
	global hazards_left
	global hazards_right
	global particles
	global background_elements
	global wall_elements_left
	global wall_elements_right
	global game_over_time
	global is_boosting
	global last_boost_particle_gen_time
	global last_blink_start
	global last_score
	global time_since_last_state_change
	global current_fps_index
	global fps_list
	global is_grounded
	global time_since_grounded
	global time_since_game_start
	global save_data
	
	time_since_last_state_change += delta_time
	
	current_fps_index = (current_fps_index + 1) % len(fps_list)
	fps_list[current_fps_index] = 0.0 if frame_num == 0 else 1.0/delta_time
	fps = int(sum(fps_list) / len(fps_list))
	
	if frame_num == 0:
		generate_sprites(game_interface)
		init_state(game_interface)
		save_data = game_interface.load_data()
		
		if 'highscore' in save_data:
			print('high score:', save_data['highscore'])
	else:
		time_since_game_start += delta_time
	
	frame_num += 1
	
	game_interface.draw_offset = [0, 0]
	
	key_just_pressed = False
	if not key_was_pressed and key_pressed:
		key_just_pressed = True
		key_pressed_start_time = time_since_game_start
	key_was_pressed = key_pressed
	
	key_pressed_time = (time_since_game_start - key_pressed_start_time) if key_pressed else 0.0
	
	key_just_pressed_input_buffered = key_just_pressed or (key_pressed and (key_pressed_time <= KEY_PRESS_BUFFER_TIME))
		
	game_over_this_frame = False
	
	###################################
	############# UPDATE ##############
	###################################
	
	## LEVEL GEN
	create_level_elements(int(f_camera_bottom_y + SCREEN_HEIGHT))
	
	## UPDATE VELOCITY
	
	player_vel[1] -= delta_time * GRAVITY
	
	is_jumping = current_state in (STATE_JUMPING_LEFT_ACTIVE, STATE_JUMPING_LEFT_PASSIVE, STATE_JUMPING_RIGHT_ACTIVE, STATE_JUMPING_RIGHT_PASSIVE)
	jump_time = (time_since_game_start - jump_start_time) if is_jumping else 0.0
	
	is_grabbing = current_state in (STATE_GRABBING_LEFT, STATE_GRABBING_RIGHT)
	grab_time = (time_since_game_start - grab_start_time) if is_grabbing else 0.0
	
	## STATE MACHINE
	
	# first of all deal with non-playing states
	if current_state == STATE_TITLE_SCREEN:
		if key_just_pressed:
			SwitchState(STATE_GRABBING_LEFT) # convert it to grabbing left if starting, then it will be automatically handled normally
	elif current_state == STATE_GAME_OVER:
		time_since_game_over = time_since_game_start - game_over_time
		if time_since_game_over > TIME_TO_IGNORE_INPUT_AFTER_GAMEOVER:
			if key_just_pressed:
				# restore initial state
				init_state(game_interface)
				SwitchState(STATE_TITLE_SCREEN) # this will render at the end
		
		if time_since_game_over <= SCREENSHAKE_AFTER_GAMEOVER_TIME:
			game_interface.draw_offset = [random.randrange(-1, 2), random.randrange(-1, 2)]
	
	# now deal with playing states
	if current_state == STATE_GRABBING_LEFT:
		if key_just_pressed_input_buffered:
			
			if full_jump_chain > NUM_JUMPS_FOR_ACCUMULATE:
				is_boosting = True
			
			player_vel[0] = JUMP_INITIAL_SPEED_X * get_jump_speed_factor()
			player_vel[1] = JUMP_INITIAL_SPEED_Y * get_jump_speed_factor()
			
			SwitchState(STATE_JUMPING_RIGHT_ACTIVE)
			jump_start_time = time_since_game_start
			print(frame_num, time_since_game_start, str(round(float(f_camera_bottom_y + SCROLL_MIN_HEIGHT) / player_size[1])) + 'm JUMP', full_jump_chain)
			
			if DRAW_PARTICLES:
				for i in range(random.randrange(2,5)):
					particles.append(Particle(pos=[player_pos[0], player_pos[1] + random.randrange(0, player_size[1]-1)], vel=[random.randrange(1,10), random.uniform(JUMP_INITIAL_SPEED_Y*0.3, JUMP_INITIAL_SPEED_Y*0.7)], time_left=0.5, blink_time=0.5))
		else:
			if grab_time > MAX_GRAB_TIME_FOR_ACCUM_TO_CONTINUE:
				full_jump_chain = 0
				is_boosting = False
			
	elif current_state == STATE_GRABBING_RIGHT:
		if key_just_pressed_input_buffered:
			
			if full_jump_chain > NUM_JUMPS_FOR_ACCUMULATE:
				is_boosting = True
				
			player_vel[0] = -JUMP_INITIAL_SPEED_X * get_jump_speed_factor()
			player_vel[1] =  JUMP_INITIAL_SPEED_Y * get_jump_speed_factor()
			
			SwitchState(STATE_JUMPING_LEFT_ACTIVE)
			jump_start_time = time_since_game_start
			print(frame_num, time_since_game_start, str(round(float(f_camera_bottom_y + SCROLL_MIN_HEIGHT) / player_size[1])) + 'm JUMP', full_jump_chain)
			
			if DRAW_PARTICLES:
				for i in range(random.randrange(2,5)):
					particles.append(Particle(pos=[player_pos[0] + player_size[0] - 1, player_pos[1] + random.randrange(0, player_size[1]-1)], vel=[-random.randrange(1,10), random.uniform(JUMP_INITIAL_SPEED_Y*0.3, JUMP_INITIAL_SPEED_Y*0.7)], time_left=0.5, blink_time=0.5))
		else:
			if grab_time > MAX_GRAB_TIME_FOR_ACCUM_TO_CONTINUE:
				full_jump_chain = 0
				is_boosting = False
			
	elif current_state == STATE_JUMPING_RIGHT_ACTIVE:
		if key_pressed:
			if jump_time <= JUMP_KEY_TIME_ACCUMULATE:
				
				ratio = jump_time / JUMP_KEY_TIME_ACCUMULATE
				speed_x = lerp(ratio, JUMP_INITIAL_SPEED_X, JUMP_SPEED_CONTINUATION_SPEED_X)
				speed_y = lerp(ratio, JUMP_INITIAL_SPEED_Y, JUMP_SPEED_CONTINUATION_SPEED_Y)
				
				# continue with active jump
				player_vel[0] = speed_x * get_jump_speed_factor()
				player_vel[1] = speed_y * get_jump_speed_factor()
			else:
				# stop active jump
				SwitchState(STATE_JUMPING_RIGHT_PASSIVE)
				full_jump_chain += 1
		else:
			# stop active jump
			SwitchState(STATE_JUMPING_RIGHT_PASSIVE)
			full_jump_chain = 0
			is_boosting = False
			
	elif current_state == STATE_JUMPING_LEFT_ACTIVE:
		if key_pressed:
			if jump_time <= JUMP_KEY_TIME_ACCUMULATE:
				
				ratio = jump_time / JUMP_KEY_TIME_ACCUMULATE
				speed_x = -lerp(ratio, JUMP_INITIAL_SPEED_X, JUMP_SPEED_CONTINUATION_SPEED_X)
				speed_y =  lerp(ratio, JUMP_INITIAL_SPEED_Y, JUMP_SPEED_CONTINUATION_SPEED_Y)
				
				# continue with active jump
				player_vel[0] = speed_x * get_jump_speed_factor()
				player_vel[1] = speed_y * get_jump_speed_factor()
			else:
				# stop active jump
				SwitchState(STATE_JUMPING_LEFT_PASSIVE)
				full_jump_chain += 1
		else:
			# stop active jump
			SwitchState(STATE_JUMPING_LEFT_PASSIVE)
			full_jump_chain = 0
			is_boosting = False
			
	elif current_state == STATE_JUMPING_RIGHT_PASSIVE:
		pass
	elif current_state == STATE_JUMPING_LEFT_PASSIVE:
		pass
	elif current_state == STATE_TITLE_SCREEN:
		pass
	elif current_state == STATE_GAME_OVER:
		pass
	else:
		print("UNKNOWN STATE", current_state)
	
	# max speed
	player_vel[0] = clamp(player_vel[0], -MAX_SPEED, +MAX_SPEED)
	player_vel[1] = clamp(player_vel[1], -MAX_SPEED, +MAX_SPEED)
	
	## UPDATE POSITION
	
	player_pos[0] += delta_time * player_vel[0]
	player_pos[1] += delta_time * player_vel[1]
	
	## COLLIDE
	
	if StateIsPlaying():
		if player_pos[0] < WALL_WIDTH:
			player_pos[0] = WALL_WIDTH
			player_vel[0] = 0
			if StateIsJumpingLeft():
				SwitchState(STATE_GRABBING_LEFT)
				grab_start_time = time_since_game_start
		
		if player_pos[0] + player_size[0] > SCREEN_WIDTH - WALL_WIDTH:
			player_pos[0] = SCREEN_WIDTH - WALL_WIDTH - player_size[0]
			player_vel[0] = 0
			if StateIsJumpingRight():
				SwitchState(STATE_GRABBING_RIGHT)
				grab_start_time = time_since_game_start
		
	if player_pos[1] < 2:
		if f_camera_bottom_y == 0.0:
			player_pos[1] = 2
			player_vel[1] = 0
			if not is_grounded:
				is_grounded = True
				time_since_grounded = 0.0
			else:
				time_since_grounded += delta_time
		else:
			is_grounded = False
	else:
		is_grounded = False
	
	## SQUASH / STRETCH
	player_size = [PLAYER_WIDTH, PLAYER_HEIGHT]
	if True:
		# wall left
		if current_state == STATE_GRABBING_LEFT:
			if time_since_last_state_change < 0.1:
				player_size[0] = PLAYER_WIDTH - 1
				player_size[1] = PLAYER_HEIGHT + 1
			# untouched player_pos
		
		# wall right
		if current_state == STATE_GRABBING_RIGHT:
			if time_since_last_state_change < 0.1:
				player_size[0] = PLAYER_WIDTH - 1
				player_size[1] = PLAYER_HEIGHT + 1
			player_pos[0] = SCREEN_WIDTH - WALL_WIDTH - player_size[0]
			
		## ground
		if StateIsGrabbing() and is_grounded and time_since_grounded <= 0.1:
			player_size[1] = PLAYER_HEIGHT - 1
	
	# ROUND TO INT
		
	# xmin, ymin, xmax, ymax
	player_rect = [round(player_pos[0]), round(player_pos[1]), round(player_pos[0]) + player_size[0] - 1, round(player_pos[1]) + player_size[1] - 1]
	
	f_camera_bottom_y = max(f_camera_bottom_y, player_pos[1] - SCROLL_MIN_HEIGHT)
	camera_bottom_y = round(f_camera_bottom_y)
	
	# CHECK OVERLAPS
	
	# hazards
	if not GOD_MODE:
		if current_state == STATE_GRABBING_LEFT:
			for hazard in hazards_left:
				hazard_height = 4 * hazard[1]
				overlap = (player_rect[1] < hazard[0] + hazard_height) and (player_rect[3] > hazard[0])
				if overlap:
					game_over_this_frame = True
		if current_state == STATE_GRABBING_RIGHT:
			for hazard in hazards_right:
				hazard_height = 4 * hazard[1]
				overlap = (player_rect[1] < hazard[0] + hazard_height) and (player_rect[3] > hazard[0])
				if overlap:
					game_over_this_frame = True
		
		# bottom
		if StateIsPlaying() and camera_bottom_y > 0:
			if player_pos[1] <= camera_bottom_y:
				game_over_this_frame = True
	
	
	if game_over_this_frame:
		game_over_time = time_since_game_start
		last_score = round(float(camera_bottom_y + SCROLL_MIN_HEIGHT) / player_size[1])
		
		prev_high_score = 0
		if 'highscore' in save_data:
			prev_high_score = int(save_data['highscore'])
		
		print("Game over! Score:", str(last_score) + 'm', "Pixel height:", camera_bottom_y + SCROLL_MIN_HEIGHT)
		
		if last_score > prev_high_score:
			print("High score! Previous was", prev_high_score)
			save_data['highscore'] = last_score
			game_interface.save_data(save_data)
		else:
			print("Prev high score was", prev_high_score)
		
		SwitchState(STATE_GAME_OVER)
		
		if DRAW_PARTICLES:
			avg = [(player_rect[0] + player_rect[2]) * 0.5, (player_rect[1] + player_rect[3]) * 0.5]
			for x in range(player_rect[0], player_rect[2]):
				for y in range(player_rect[1], player_rect[3]):
					offset = [x - avg[0], y - avg[1]]
					vel = [offset[0] * random.randrange(0, 100)*0.1, offset[1] * random.randrange(00, 100)*0.1]
					vel[1] += 10
					time_left = random.randrange(70, 100)*0.01
					particles.append(Particle(pos=[x, y], vel=vel, time_left=time_left, blink_time=time_left*0.5, gravity_factor=0.5))
	
	
	
	###################################
	############## DRAW ###############
	###################################
	
	# sky
	game_interface.fill(0)
	
	# parallax background details
	if current_state != STATE_GAME_OVER or time_since_last_state_change <= SCREENSHAKE_AFTER_GAMEOVER_TIME:
		for bg_elem in background_elements:
			bg_elem.draw(game_interface, camera_bottom_y)
		for bg_elem in wall_elements_left:
			bg_elem.draw(game_interface, camera_bottom_y)
		for bg_elem in wall_elements_right:
			bg_elem.draw(game_interface, camera_bottom_y)
	
	# don't draw player if gameover, but that's the only case	
	if current_state != STATE_GAME_OVER:
		game_interface.drawFilledRectangle(player_rect[0] - 1, player_rect[1] - camera_bottom_y - 1, player_size[0] + 2, player_size[1] + 2, 0)
		game_interface.drawFilledRectangle(player_rect[0],     player_rect[1] - camera_bottom_y,     player_size[0],     player_size[1],     1)
	
	looking_right = current_state in (STATE_TITLE_SCREEN, STATE_GRABBING_LEFT, STATE_JUMPING_RIGHT_ACTIVE, STATE_JUMPING_RIGHT_PASSIVE)
	
	# WAVE if idle for long
	is_waving = False
	if player_vel[0] == 0 and player_vel[1] == 0 and time_since_last_state_change > 10:
		is_waving = (int(time_since_last_state_change) % 10 == 0)
		if is_waving:
			wave_offset = int(10 * (time_since_last_state_change - int(time_since_last_state_change))) % 2
			y = player_rect[1] - 1 + player_size[1] - 1 - camera_bottom_y - wave_offset
			if current_state in (STATE_GRABBING_LEFT, STATE_TITLE_SCREEN):
				game_interface.setPixel(player_rect[0] + player_size[0], y, 1)
			elif current_state == STATE_GRABBING_RIGHT:
				game_interface.setPixel(player_rect[0] - 1, y, 1)
				
	# EYES
	vertical_eye_offset = 0
	if player_vel[1] < -25:
		vertical_eye_offset = -2
	elif player_vel[1] < -10:
		vertical_eye_offset = -1
	# look down every now and then for variation:
	if player_vel[0] == 0 and player_vel[1] == 0 and not is_waving and time_since_last_state_change > 2.0:
		f = 0.23 * time_since_game_start
		if (f - int(f)) < 0.23:
			vertical_eye_offset = -1
	time_since_last_blink_start = time_since_game_start - last_blink_start
	if time_since_last_blink_start > 2.5:
		last_blink_start = time_since_game_start
		time_since_last_blink_start = 0.0
	blinking = time_since_last_blink_start > 0.2 or current_state not in (STATE_GRABBING_LEFT, STATE_GRABBING_RIGHT, STATE_TITLE_SCREEN)
	if looking_right:
		game_interface.setPixel(player_rect[0] + player_size[0] - 4,                  player_rect[1] - camera_bottom_y + player_size[1] - 2 + vertical_eye_offset, 0 if blinking else 1)
		game_interface.setPixel(player_rect[0] + player_size[0] - 1, player_rect[1] - camera_bottom_y + player_size[1] - 2 + vertical_eye_offset, 0 if blinking else 1)
	else:
		game_interface.setPixel(player_rect[0],                      player_rect[1] - camera_bottom_y + player_size[1] - 2 + vertical_eye_offset, 0 if blinking else 1)
		game_interface.setPixel(player_rect[0] + 3, player_rect[1] - camera_bottom_y + player_size[1] - 2 + vertical_eye_offset, 0 if blinking else 1)
			
	# LIMBS
	if current_state in (STATE_JUMPING_LEFT_ACTIVE, STATE_JUMPING_LEFT_PASSIVE):
		# moving left: limbs lower right
		game_interface.setPixel(player_rect[0] + 1,              player_rect[1] - 1                      - camera_bottom_y, 1)
		game_interface.setPixel(player_rect[0] + player_size[0], player_rect[1] - 1 + player_size[1] - 1 - camera_bottom_y, 1)
		game_interface.setPixel(player_rect[0] + player_size[0], player_rect[1] - 1                      - camera_bottom_y, 1)
	if current_state in (STATE_JUMPING_RIGHT_ACTIVE, STATE_JUMPING_RIGHT_PASSIVE):
		# moving right: limbs lower left
		game_interface.setPixel(player_rect[0] - 1                     , player_rect[1] - 1 + player_size[1] - 1 - camera_bottom_y, 1)
		game_interface.setPixel(player_rect[0] - 1                     , player_rect[1] - 1                      - camera_bottom_y, 1)
		game_interface.setPixel(player_rect[0] - 1 + player_size[0] - 1, player_rect[1] - 1                      - camera_bottom_y, 1)
	
	# floor
	if camera_bottom_y == 0:
		game_interface.drawLine(0, 0 - camera_bottom_y, SCREEN_WIDTH-1, 0 - camera_bottom_y, 1)
		game_interface.drawLine(0, 1 - camera_bottom_y, SCREEN_WIDTH-1, 1 - camera_bottom_y, 1)
	
	# wall patterns
	if True:
		for y in range((-camera_bottom_y % 9) - 10, SCREEN_HEIGHT+10, 9):
			game_interface.drawSprite_location('SPRITE_WALL_LEFT', 0, y+2)
			game_interface.drawSprite_location('SPRITE_WALL_RIGHT', SCREEN_WIDTH - WALL_WIDTH, y+2)
	
	# spikes, floor, and walls after character, to hide the outlines
	if True:
		spike_width = sprite_sizes['SPRITE_SPIKE_RIGHT'][0]
		
		for hazard in hazards_left:
			if hazard[0] < camera_bottom_y + SCREEN_HEIGHT + 1:
				hazard_height = 4 * hazard[1]
				game_interface.drawFilledRectangle(1, hazard[0] - camera_bottom_y, 2, hazard_height + 1, 1)
				
				for y in range(0, hazard[1]):
					game_interface.drawSprite_location('SPRITE_SPIKE_LEFT', WALL_WIDTH, hazard[0] + y*4 + 1 - camera_bottom_y)
					
		for hazard in hazards_right:
			if hazard[0] < camera_bottom_y + SCREEN_HEIGHT + 1:
				hazard_height = 4 * hazard[1]
				game_interface.drawFilledRectangle(SCREEN_WIDTH-3, hazard[0] - camera_bottom_y, 2, hazard_height, 1)
				
				for y in range(0, hazard[1]):
					game_interface.drawSprite_location('SPRITE_SPIKE_RIGHT', SCREEN_WIDTH - WALL_WIDTH - spike_width, hazard[0] + y*4 + 1 - camera_bottom_y)
	
	
	# random particles for boost
	if DRAW_PARTICLES and StateIsJumping() and is_boosting:
		if time_since_game_start - last_boost_particle_gen_time > 0.1:
			last_boost_particle_gen_time = time_since_game_start
			particles.append(Particle(pos=[player_rect[0], player_rect[1]], use_gravity=False, time_left=0.5, blink_time=999))
			particles.append(Particle(pos=[player_rect[2], player_rect[1]], use_gravity=False, time_left=0.5, blink_time=999))
	
	# PARTICLES
	if DRAW_PARTICLES:
		for particle in particles:
			if particle.use_gravity:
				particle.vel[1] -= GRAVITY * particle.gravity_factor * delta_time
				
			particle.pos[0] += particle.vel[0] * delta_time
			particle.pos[1] += particle.vel[1] * delta_time
			
			particle.time_left -= delta_time
			
			if particle.time_left > 0:
				show_particle = True
				
				if particle.time_left < particle.blink_time:
					stage = math.floor(particle.time_left / particle.blink_rate)
					show_particle = (stage % 2 == 0)
				
				if show_particle:
					for x in range(0, particle.size[0]):
						for y in range(0, particle.size[1]):
							game_interface.setPixel(round(particle.pos[0]) + x, round(particle.pos[1]) - y - camera_bottom_y, 1)
	
	def draw_centered_number(num, y, small=False):
		digits = [int(i) for i in str(num)]
		num_digits = len(digits)
		DIGIT_WIDTH = 3 if small else 5
		DIGIT_HEIGHT = 5 if small else 8
		
		width = num_digits * DIGIT_WIDTH + (num_digits - 1)
		left = SCREEN_WIDTH / 2 - width / 2
		
		game_interface.drawFilledRectangle(left-2, y-1, width + 4, DIGIT_HEIGHT + 2, 0)
		
		for digit in digits:
			sprite_name = ('SPRITE_DIGIT_SMALL_' if small else 'SPRITE_DIGIT_') + str(digit)
			game_interface.drawSprite_location(sprite_name, left, y)
			left += DIGIT_WIDTH + 1
	
	# UI
	if current_state is STATE_TITLE_SCREEN:
		game_interface.drawSprite('SPRITE_TITLE')
		game_interface.draw_battery()
	elif current_state is STATE_GAME_OVER:
		game_interface.drawSprite('SPRITE_SCORE')
		height = 2 * math.sin(5 * time_since_last_state_change) + 48
		draw_centered_number(last_score, int(height))
		
		if 'highscore' in save_data:
			prev_high_score = int(save_data['highscore'])
			if prev_high_score > 0:
				game_interface.drawSprite('SPRITE_BEST')
				draw_centered_number(prev_high_score, 22, True)
	
	# draw fps
	if DEBUG_DRAW_FPS:
		draw_centered_number(int(fps), 4, True)
		
		
	
	###################################
	############ CLEANUP ##############
	###################################
	
	# remove hazards that are too far down
	hazards_left  = [h for h in hazards_left  if h[0] + 4*h[1] >= camera_bottom_y]
	hazards_right = [h for h in hazards_right if h[0] + 4*h[1] >= camera_bottom_y]
	
	# remove old particles and out of camera
	if DRAW_PARTICLES:
		particles = [p for p in particles if (p.time_left > 0 and p.pos[1] >= camera_bottom_y)]
