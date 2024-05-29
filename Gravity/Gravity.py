import thumbyButton as buttons
import time
import machine
import random
import thumby
from math import cos, sin, radians
from sys import path as syspath

from thumby import display
random.seed(time.ticks_ms())
display.setFPS(30)

thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)

# Function to generate new terrain segments
def generate_terrain_segment(start_x, width, height, prev_y):
    end_x = start_x + width
    # Create generally smoother terrain with occasional spikes
    spike_chance = 0.2
    smooth_y = prev_y + random.randint(-7, 7)
    if random.random() < spike_chance:
        end_y = prev_y + random.randint(-12, 12)
    else:
        end_y = smooth_y
    
    # Add occasional downward slopes and canyons
    if random.random() < 0.07:
        end_y += random.randint(10, 30)  # Downhill slope
    if random.random() < 0.05:
        end_y -= random.randint(10, 20)  # Crevice or canyon
    
    # Ensure end_y stays within the screen height limits
    end_y = max(0, min(height, end_y))
    
    return (end_x, end_y)

# Function to get terrain height at a given x position
def get_terrain_height(x, terrain):
    for i in range(len(terrain) - 1):
        if terrain[i][0] <= x <= terrain[i + 1][0]:
            # Linear interpolation between terrain points
            x1, y1 = terrain[i]
            x2, y2 = terrain[i + 1]
            return y1 + (y2 - y1) * (x - x1) // (x2 - x1)
    return terrain[-1][1]

# Initialize terrain
def initialize_terrain():
    terrain = [(0, 30)]
    for i in range(1, 10):
        terrain.append(generate_terrain_segment(terrain[-1][0], 8, 40, terrain[-1][1]))
    return terrain
    
# Initialize custom
def initialize_custom_terrain():
    return generate_custom_terrain_segment(-1)
    
    
def generate_custom_terrain_segment(x):
    x = int(x)
    try:
        start_index = next(i for i, point in enumerate(aligned_points) if point[0] > x)
    except StopIteration:
        return []
    next_points = aligned_points[start_index:start_index + 10]
    return next_points
    

def getTrackStartEnd(track_name):
    track_coords = {
        'Intro': (11, 14),
        'Shorty': (8, 7),
        'Slope': (8, 12),
        'Crackle': (9, 9),
        'Knolls': (11, 9),
        'Deep': (9, 11),
        'Cliff': (8, 9),
        'Hole': (7, 8),
        'Original': (8, 8),
        'Savvy': (11, 8),
        'Indoor': (8, 7),
        'Spikeholes': (13, 12),
        'Downhill': (6, 8),
        'Hillclimb': (6, 9),
        'Modesty': (8, 9),
        'Blocks': (7, 12),
        'Bumps': (11, 6),
        'Spikehops': (12, 15),
        'Pillar': (7, 7),
        'Trenches': (8, 8),
        'Floorboards': (10, 12),
        'Tip top': (8, 11),
        'Dantes Peak': (12, 12),
        'Abrupt': (8, 9),
        'Undertaker': (10, 13),
        'Liberty': (7, 11),
        'Intense': (14, 10),
        '100%': (5, 8),
        'Training day': (6, 8),
        'Trial again': (13, 12)
    }
    return track_coords[track_name]

terrain = initialize_terrain()
aligned_points = None

class Wheel:
    def __init__(self, pos, velocity, angular_velocity):
        self.pos = pos
        self.velocity = velocity
        self.acceleration = [0, 0]
        self.angular_velocity = angular_velocity

    def apply_physics(self, terrain):
        self.velocity[1] += 0.2  # gravity
        self.velocity[1] *= (1 - 0.1)  #friction with air
        self.pos = [p + v for p, v in zip(self.pos, self.velocity)]
        self.velocity = [v + a for v, a in zip(self.velocity, self.acceleration)]
        terrain_height = get_terrain_height(self.pos[0], terrain)
            
        if self.pos[1] >= terrain_height - 3:
            # Calculate slope of the terrain
            left_x = self.pos[0] - 1
            right_x = self.pos[0] + 1
            left_height = get_terrain_height(left_x, terrain)
            right_height = get_terrain_height(right_x, terrain)
            slope = (right_height - left_height) // (right_x - left_x)
            
            # Adjust horizontal velocity based on the slope
            self.velocity[0] += slope * 0.2 
            #vertical velocity bounce
            if -0.2 > self.velocity[1] > 0.2:
                self.velocity[1] *= -1 / 2.2
            else:
                self.velocity[1] -= 0.45

    def draw(self, offset_x, offset_y):
        draw_circle(int(self.pos[0] - offset_x), int(self.pos[1] - offset_y), 3, 1)
        display.setPixel(int(self.pos[0] - offset_x), int(self.pos[1] - offset_y), 1)

class Bike:
    def __init__(self, pos, wheel_offset, friction=0.1):
        self.pos = pos
        self.wheel_offset = wheel_offset
        self.friction = friction
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.angular_velocity = 0

        self.wheel1_hit_flag = False
        self.wheel2_hit_flag = False

    def apply_physics(self, terrain):
        xfriction = .02  # air resistance
        if self.wheel1_hit_flag:
            xfriction += .033  # tyre resistance
        if self.wheel2_hit_flag:
            xfriction += .033  # tyre resistance
        self.velocity[0] *= (1 - xfriction)
        self.velocity[1] *= (1 - self.friction)  # gravity
        self.pos = [p + v for p, v in zip(self.pos, self.velocity)]
        self.velocity = [v + a for v, a in zip(self.velocity, self.acceleration)]

        wheel1_pos = self.rotate_point(self.pos[0] - self.wheel_offset, self.pos[1], self.angular_velocity)
        wheel2_pos = self.rotate_point(self.pos[0] + self.wheel_offset, self.pos[1], self.angular_velocity)

        terrain_height1 = get_terrain_height(wheel1_pos[0], terrain)
        terrain_height2 = get_terrain_height(wheel2_pos[0], terrain)

        # Apply wheelie effect
        self.angular_velocity -= self.acceleration[0] * 16  # Adjust this factor for stronger/weaker wheelie effect

        # tyre ground bounce
        if wheel1_pos[1] >= terrain_height1 - 3 or wheel2_pos[1] >= terrain_height2 - 3:
            if -0.2 > self.velocity[1] > 0.2:
                self.velocity[1] *= -1 / 2.2
            else:
                self.velocity[1] -= 0.45

        if wheel1_pos[1] >= terrain_height1 - 3:
            self.wheel1_hit_flag = True
        else:
            self.wheel1_hit_flag = False
            
        if wheel2_pos[1] >= terrain_height2 - 3:
            self.wheel2_hit_flag = True
        else:
            self.wheel2_hit_flag = False
            
        x_diff = wheel2_pos[0] - wheel1_pos[0]

        if wheel1_pos[1] <= terrain_height1 - 3:
            mult1 = 1
            if wheel2_pos[1] >= terrain_height2 - 3:
                mult1 += 2
            self.adjust_angular_velocity(wheel1_pos[1], terrain_height1, mult1, x_diff, negative=False)

        if wheel2_pos[1] <= terrain_height2 - 3:
            mult2 = 1
            if wheel1_pos[1] >= terrain_height1 - 3:
                mult2 += 2
            self.adjust_angular_velocity(wheel2_pos[1], terrain_height2, mult2, x_diff)

        self.pos = self.rotate_point(self.pos[0], self.pos[1], self.angular_velocity)
        self.velocity[1] += 0.1
        if not self.wheel1_hit_flag and not self.wheel2_hit_flag:
            self.velocity[1] += 0.1
            
        # Check for bike angle and apply forward or backward acceleration if both wheels are touching the ground
        if self.wheel1_hit_flag and self.wheel2_hit_flag:
            wheel_diff = wheel1_pos[1] - wheel2_pos[1]  # Difference in y-coordinates of the wheels
            if wheel_diff > 3:  # Angled forward
                self.velocity[0] -= 0.2
            elif wheel_diff < -3:  # Angled backward
                self.velocity[0] += 0.2

    def adjust_angular_velocity(self, wheel_y, terrain_y, mult=1, x_diff=1, negative=True):
        angular_acceleration = 15 * (x_diff / (2 * self.wheel_offset))
        self.angular_velocity += angular_acceleration if negative else -angular_acceleration

    def rotate_point(self, x, y, angle):
        angle_rad = radians(angle)
        dx, dy = x - self.pos[0], y - self.pos[1]
        new_x = dx * cos(angle_rad) - dy * sin(angle_rad) + self.pos[0]
        new_y = dx * sin(angle_rad) + dy * cos(angle_rad) + self.pos[1]
        return new_x, new_y

    def update(self, terrain):
        wheel1_pos = self.rotate_point(self.pos[0] - self.wheel_offset, self.pos[1], self.angular_velocity)
        wheel2_pos = self.rotate_point(self.pos[0] + self.wheel_offset, self.pos[1], self.angular_velocity)
        terrain_height1 = get_terrain_height(wheel1_pos[0], terrain)
        terrain_height2 = get_terrain_height(wheel2_pos[0], terrain)
        

        if wheel1_pos[1] >= terrain_height1 - 5:
            if buttons.buttonA.pressed():
                if self.wheel1_hit_flag and self.wheel2_hit_flag:
                    dx = wheel2_pos[0] - wheel1_pos[0]
                    dy = wheel2_pos[1] - wheel1_pos[1]
                    length = (dx**2 + dy**2)**0.5
                    if length != 0:
                        dir_x = dx / length
                        dir_y = dy / length
                        self.acceleration[0] += 0.2 * dir_x
                        self.acceleration[1] += 0.2 * dir_y
                else:
                    self.acceleration[0] += 0.2
        if wheel2_pos[1] >= terrain_height2 - 5:
            if buttons.buttonB.pressed():
                # Apply negative acceleration if velocity is positive
                if self.velocity[0] > 0:
                    self.acceleration[0] -= 0.2
                    # Ensure velocity doesn't go below 0
                    if self.velocity[0] + self.acceleration[0] < 0:
                        self.acceleration[0] = -self.velocity[0]
                else:
                    self.acceleration[0] += 0.2
                    # Ensure velocity doesn't go above 0
                    if self.velocity[0] + self.acceleration[0] > 0:
                        self.acceleration[0] = -self.velocity[0]
        if buttons.buttonR.pressed():
            self.angular_velocity += 3.5
        if buttons.buttonL.pressed():
            self.angular_velocity -= 3.5

        self.apply_physics(terrain)
        self.acceleration = [0, 0]
        seat_pos = self.rotate_point(self.pos[0] + 1, self.pos[1] - 4, self.angular_velocity)
        terrain_heightseat_pos = get_terrain_height(seat_pos[0], terrain)
        # Check if the bike has flipped and the seat hit the ground
        if (seat_pos[1] >= terrain_heightseat_pos) and (wheel1_pos[0] > wheel2_pos[0]):
            self.crash(terrain)

        # Check if either wheel is more than 8 pixels under the terrain
        if wheel1_pos[1] > terrain_height1 + 6 or wheel2_pos[1] > terrain_height2 + 6 or seat_pos[1] > terrain_heightseat_pos + 6:
            self.crash(terrain)

    def crash(self, terrain):
        global gameState, high_score, current_score

        display.update()  # Refresh the screen
    
        wheel1_pos = self.rotate_point(self.pos[0] - self.wheel_offset, self.pos[1], self.angular_velocity)
        wheel2_pos = self.rotate_point(self.pos[0] + self.wheel_offset, self.pos[1], self.angular_velocity)
        
        self.velocity[0]=random.random()*2-1
        wheel1 = Wheel(wheel1_pos, self.velocity[:], self.angular_velocity)
        self.velocity[0]=random.random()*2-1
        wheel2 = Wheel(wheel2_pos, self.velocity[:], self.angular_velocity)
    
        for _ in range(60):  # Let the wheels bounce around for a second (30 frames at 30 FPS)
            display.fill(0)
            wheel1.apply_physics(terrain)
            wheel2.apply_physics(terrain)
    
            offset_x = self.pos[0] - 36
            offset_y = self.pos[1] - 20
    
            draw_terrain(terrain, int(offset_x), int(offset_y))
            wheel1.draw(offset_x, offset_y)
            wheel2.draw(offset_x, offset_y)
            
            display.update()
            time.sleep(1 / 30)
        
        # Check and update the high score if in GAME_LOOP mode
        if gameState == GAME_LOOP:
            if current_score > high_score:
                high_score = current_score
                thumby.saveData.setItem("Endless_highScore", high_score)
                thumby.saveData.save()
                # Display "New High Score" message
                display.fill(0)
                display.drawText("New High Score!", 5, 20, 1)
                display.drawText(f"{int(high_score)}", 5, 30, 1)
                display.update()
                time.sleep(2)
        
        reset_game()  # Reset the game state
        gameState = TITLE_PAGE  # Return to title screen


    def draw(self, offset_x, offset_y):
        current_time = time.ticks_ms()
        if self.wheel1_hit_flag:
            wheel1_pos = self.rotate_point(self.pos[0] - self.wheel_offset, self.pos[1] - 1, self.angular_velocity)
        else:
            wheel1_pos = self.rotate_point(self.pos[0] - self.wheel_offset, self.pos[1], self.angular_velocity)

        if self.wheel2_hit_flag:
            wheel2_pos = self.rotate_point(self.pos[0] + self.wheel_offset - 1, self.pos[1] - 1, self.angular_velocity)
        else:
            wheel2_pos = self.rotate_point(self.pos[0] + self.wheel_offset, self.pos[1], self.angular_velocity)

        forkbase_pos = self.rotate_point(self.pos[0] + 2, self.pos[1] - 8, self.angular_velocity)

        display.setPixel(int(wheel1_pos[0] - offset_x), int(wheel1_pos[1] - offset_y), 1)
        display.setPixel(int(wheel2_pos[0] - offset_x), int(wheel2_pos[1] - offset_y), 1)

        draw_circle(int(wheel1_pos[0] - offset_x), int(wheel1_pos[1] - offset_y), 3, 1)
        draw_circle(int(wheel2_pos[0] - offset_x), int(wheel2_pos[1] - offset_y), 3, 1)

        seat_pos = self.rotate_point(self.pos[0] + 1, self.pos[1] - 4, self.angular_velocity)
        engine_pos = self.rotate_point(self.pos[0] - 1, self.pos[1] - 1, self.angular_velocity)
        handle_pos = self.rotate_point(self.pos[0] + 3, self.pos[1] - 7, self.angular_velocity)
        rear_pos = self.rotate_point(self.pos[0] - 7, self.pos[1] - 6, self.angular_velocity)
        susp_pos = self.rotate_point(self.pos[0] - 4, self.pos[1], self.angular_velocity)
        centre_pos = self.rotate_point(self.pos[0] - 2, self.pos[1] - 4, self.angular_velocity)

        if 0 <= seat_pos[0] - offset_x < 72 and 0 <= seat_pos[1] - offset_y < 72:
            display.drawLine(int(wheel1_pos[0] - offset_x), int(wheel1_pos[1] - offset_y), int(engine_pos[0] - offset_x), int(engine_pos[1] - offset_y), 1)
            display.drawLine(int(engine_pos[0] - offset_x), int(engine_pos[1] - offset_y), int(handle_pos[0] - offset_x), int(handle_pos[1] - offset_y), 1)
            display.drawLine(int(forkbase_pos[0] - offset_x), int(forkbase_pos[1] - offset_y), int(wheel2_pos[0] - offset_x), int(wheel2_pos[1] - offset_y), 1)
            display.drawLine(int(seat_pos[0] - offset_x), int(seat_pos[1] - offset_y), int(rear_pos[0] - offset_x), int(rear_pos[1] - offset_y), 1)
            display.drawLine(int(susp_pos[0] - offset_x), int(susp_pos[1] - offset_y), int(centre_pos[0] - offset_x), int(centre_pos[1] - offset_y), 1)

def draw_circle(x_center, y_center, radius, c):
    x = radius
    y = 0
    decision = 1 - x

    while y <= x:
        display.setPixel(int(x_center + x), int(y_center + y), c)
        display.setPixel(int(x_center - x), int(y_center + y), c)
        display.setPixel(int(x_center + x), int(y_center - y), c)
        display.setPixel(int(x_center - x), int(y_center - y), c)
        display.setPixel(int(x_center + y), int(y_center + x), c)
        display.setPixel(int(x_center - y), int(y_center + x), c)
        display.setPixel(int(x_center + y), int(y_center - x), c)
        display.setPixel(int(x_center - y), int(y_center - x), c)

        y += 1
        if decision <= 0:
            decision += 2 * y + 1
        else:
            x -= 1
            decision += 2 * (y - x) + 1

def draw_terrain(terrain, offset_x, offset_y, depth=6, screen_width=72, screen_height=40):
    global start_index, end_index, aligned_points, flag_positions
    half_depth = depth // 2
    half_screen_width = screen_width // 2
    front_terrain = []
    back_terrain = []

    # Calculate front and back terrain positions with perspective effect
    for x, y in terrain:
        # Convert world coordinates to screen coordinates
        screen_x = x - offset_x
        screen_y = y - offset_y
        
        # Calculate the perspective shift based on the distance from the center of the screen
        perspective_shift = (screen_x - half_screen_width) * half_depth // half_screen_width
        
        front_terrain.append((screen_x + perspective_shift, screen_y + half_depth))
        back_terrain.append((screen_x - perspective_shift, screen_y - half_depth))

    # Function to draw a flag
    def draw_flag(base_x, base_y):
        if 0 <= base_x < screen_width and 0 <= base_y < screen_height:
            flag_height = 13
            triangle_height = 3
            # Draw the flag pole (vertical line)
            display.drawLine(base_x, base_y, base_x, base_y - flag_height, 1)
            # Draw the triangle at the top of the flag pole
            triangle_base = [
                (base_x, base_y - flag_height),
                (base_x, base_y - flag_height + triangle_height),
                (base_x + triangle_height, base_y - flag_height + triangle_height // 2)
            ]
            for i in range(len(triangle_base)):
                x1, y1 = triangle_base[i]
                x2, y2 = triangle_base[(i + 1) % len(triangle_base)]
                display.drawLine(x1, y1, x2, y2, 1)

    # Draw front terrain line
    for i in range(len(front_terrain) - 1):
        x1, y1 = front_terrain[i]
        x2, y2 = front_terrain[i + 1]
        display.drawLine(x1, y1, x2, y2, 1)
    
    # Draw back terrain line
    for i in range(len(back_terrain) - 1):
        x1, y1 = back_terrain[i]
        x2, y2 = back_terrain[i + 1]
        display.drawLine(x1, y1, x2, y2, 1)
    
    # Connect front and back terrain lines
    for i in range(len(terrain)):
        x1, y1 = front_terrain[i]
        x2, y2 = back_terrain[i]
        display.drawLine(x1, y1, x2, y2, 1)
        
    if flag_positions:
        for pos in flag_positions:
            x, y = pos
            screen_x = x - offset_x
            screen_y = y - offset_y
            perspective_shift = (screen_x - half_screen_width) * half_depth // half_screen_width

            front_x = screen_x + perspective_shift
            front_y = screen_y + half_depth
            back_x = screen_x - perspective_shift
            back_y = screen_y - half_depth

            draw_flag(front_x, front_y)
            draw_flag(back_x, back_y)



def reset_game():
    global terrain, bike, lap_start_time, record_lap_time, flag_positions
    terrain = initialize_flat_terrain()
    flag_positions = [title_terrain[5]]
    bike = Bike([20, 0], 6)
    lap_start_time = None
    record_lap_time = None
    
def start_game():
    global terrain, bike, lap_start_time, record_lap_time, flag_positions
    terrain = initialize_terrain()
    flag_positions = None
    bike = Bike([36, get_terrain_height(36, terrain)-10], 6)


# Function to generate new terrain segments (flat terrain at y=12)
def generate_flat_terrain_segment(start_x, width):
    end_x = start_x + width
    end_y = 13 # Flat terrain at y=12
    return (end_x, end_y)


import struct

# Function to deserialize track data
def deserialize_track_data(serialized_data):
    offset = 0
    tracks = []
    
    while offset < len(serialized_data):
        # Deserialize the name
        name_length = struct.unpack_from('B', serialized_data, offset)[0]
        offset += 1
        name = serialized_data[offset:offset + name_length].decode('utf-8')
        offset += name_length
        
        # Deserialize startX, startY, finishX, and finishY
        startX, startY, finishX, finishY = struct.unpack_from('>iiii', serialized_data, offset)
        offset += 16
        
        # Deserialize the points
        num_points = struct.unpack_from('H', serialized_data, offset)[0]
        offset += 2
        points = []
        for _ in range(num_points):
            x, y = struct.unpack_from('>ii', serialized_data, offset)
            offset += 8
            points.append((x, y))
        
        tracks.append([name, startX, startY, finishX, finishY, points])
    
    return tracks


def start_custom_track(track):
    global aligned_points, terrain, bike, lap_start_time, record_lap_time, start_index,end_index, track_name, flag_positions
    track_name = track[0]
    start_index,end_index = getTrackStartEnd(track_name)
    custom_track = track

    scale_factor = 0.5
    scaled_points = [(x * scale_factor, y * -1 * scale_factor) for x, y in custom_track[5]]
    
    first_point = scaled_points[0]
    x_offset = -first_point[0]
    y_offset = 20 - first_point[1]
    
    aligned_points = [(int(x + x_offset), int(y + y_offset)) for x, y in scaled_points]
    terrain = initialize_custom_terrain()
    start_x_flag = aligned_points[start_index][0]
    
    flag_positions = [aligned_points[start_index], aligned_points[-end_index]]

    bike = Bike([start_x_flag - 20, get_terrain_height(start_x_flag -20, terrain) - 10], 6)
    lap_start_time = None
    record_lap_time = None
    if thumby.saveData.hasItem(track_name + "_fastestLapTime"):
        record_lap_time = thumby.saveData.getItem(track_name + "_fastestLapTime")


# Initialize flat terrain
def initialize_flat_terrain():
    terrain = [(0, 12)]
    for i in range(1, 10):
        terrain.append(generate_flat_terrain_segment(terrain[-1][0], 8))
    return terrain

def display_menu(track_names, selected_index):
    display.fill(0)
    
    # Determine the number of visible tracks
    visible_tracks = 5  # Number of tracks to show on the display at one time
    
    # Determine the start and end indices for the visible tracks
    start = max(0, min(selected_index - visible_tracks // 2, len(track_names) - visible_tracks))
    end = min(len(track_names), start + visible_tracks)

    # Draw the track names
    for i in range(start, end):
        y = (i - start) * 8  # Adjust this if your line height differs
        if i == selected_index:
            display.drawText("> " + track_names[i], 2, y, 1)
        else:
            display.drawText(track_names[i], 10, y, 1)

    # Calculate and draw the scrollbar
    total_tracks = len(track_names)
    scrollbar_height = 38  # Height of the scrollbar area
    bar_height = max(4, scrollbar_height * visible_tracks // total_tracks)  # Minimum height for visibility
    scrollbar_y = (scrollbar_height - bar_height) * selected_index // (total_tracks - 1)
    
    display.drawRectangle(66, 0, 6, scrollbar_height+2, 1)  # Draw the scrollbar outline
    display.drawFilledRectangle(67, 1 + scrollbar_y, 4, bar_height, 1)  # Draw the scrollbar fill

    display.update()

# Function to format time in seconds with milliseconds
def format_time(ms_time):
    seconds = ms_time // 1000
    milliseconds = ms_time % 1000
    return f"{seconds}.{milliseconds:03d}s"

terrain = initialize_flat_terrain()
bike = Bike([20, 0], 6)

# Load the serialized data from the file (replace 'path_to_your_file' with the actual file path)
with open('/Games/Gravity/track_data_bytes.bin', 'rb') as file:
    serialized_data = file.read()

# Deserialize the data
track_data = deserialize_track_data(serialized_data)
track_names = [track[0] for track in track_data]
track_name = None

TITLE_PAGE = 0
GAME_LOOP = 1
CUSTOM_TRACK = 2
TRACK_MENU = 3

gameState = TITLE_PAGE
textVisible = True
lastFlashTime = time.ticks_ms()
textFlashInterval = 500
selected_track_index = 0

title_terrain = [(-10, 15), (0, 23), (10, 32), (20, 34), (30, 31), (36, 24), (40, 37), (50, 34), (60, 33), (67, 35), (80, 52)]

flag_positions = [title_terrain[5]]

lap_start_time = None
record_lap_time = None
new_record = False
start_index,end_index = None,None

# Initialize the high score for endless
thumby.saveData.setName("Gravity")
high_score = thumby.saveData.getItem("Endless_highScore")
current_score = 0
if high_score is None:
    high_score = 0

while True:
    if gameState == TITLE_PAGE:
        # Clear display
        display.fill(0)
        # Draw the title
        draw_terrain(title_terrain, 0, 0)
        display.drawText("Gravity", 4, 13, 1)
        display.drawText("Trial", 13, 21, 1)
        bike.update(terrain)
        # Display the bike without controls
        bike.draw(0, 0)

        # Handle flashing text
        currentTime = time.ticks_ms()
        if currentTime - lastFlashTime > textFlashInterval:
            textVisible = not textVisible
            lastFlashTime = currentTime
        display.drawText("Classic", 44, 2, 1)
        display.drawText("Endless", 44, 18, 1)
        if textVisible:
            display.drawText("Press A", 44, 8, 1)
            display.drawText("Press B", 44, 24, 1)
        
        # Update the display
        display.update()
        
        if buttons.buttonB.pressed():
            start_game()  # Ensure the game is reset when starting
            gameState = GAME_LOOP
            display.fill(0)
            time.sleep(0.3)

        if buttons.buttonA.pressed():
            gameState = TRACK_MENU
            display.fill(0)
            time.sleep(0.3)

    elif gameState == TRACK_MENU:
        display_menu(track_names, selected_track_index)
        
        if buttons.buttonU.pressed():
            selected_track_index = (selected_track_index - 1) % len(track_names)
            time.sleep(0.2)
        
        if buttons.buttonD.pressed():
            selected_track_index = (selected_track_index + 1) % len(track_names)
            time.sleep(0.2)
        
        if buttons.buttonA.pressed():
            start_custom_track(track_data[selected_track_index])
            gameState = CUSTOM_TRACK
            display.fill(0)
            time.sleep(0.3)
        
        if buttons.buttonB.pressed():
            gameState = TITLE_PAGE
            display.fill(0)
            time.sleep(0.3)

    elif gameState == GAME_LOOP:
        bike.update(terrain)

        # Update the score
        current_score = bike.pos[0]

        # Remove old terrain segments and add new ones
        if bike.pos[0] - terrain[0][0] > 72:
            terrain.pop(0)
        while terrain[-1][0] < bike.pos[0] + 72:
            terrain.append(generate_terrain_segment(terrain[-1][0], 8, 40, terrain[-1][1]))

        bike_y = bike.pos[1]
        offset_x = bike.pos[0] - 36
        offset_y = bike_y - 20

        draw_terrain(terrain, int(offset_x), int(offset_y))
        bike.draw(offset_x, offset_y)
        
        # Drawing lap time and record time
        if current_score is not None:
            display.drawFilledRectangle(0, 35, 72, 5, 0)
            display.drawText(f"{int(current_score)}", 0, 35, 1)
        if high_score is not None:
            display.drawFilledRectangle(52, 35, 72, 5, 0)
            display.drawText(f"{int(high_score)}", 40, 35, 1)

        display.update()
        display.fill(0)
    

    elif gameState == CUSTOM_TRACK:
    
        # Remove old terrain segments and add new ones
        if bike.pos[0] - terrain[0][0] > 72:
            terrain.pop(0)
        while terrain[-1][0] < int(bike.pos[0]) + 72:
            newterrain = generate_custom_terrain_segment(terrain[-1][0])
            terrain.extend(newterrain)
            if len(newterrain)<10:
                break
            
        bike.update(terrain)


        bike_y = bike.pos[1]
        offset_x = bike.pos[0] - 36
        offset_y = bike_y - 20

        draw_terrain(terrain, int(offset_x), int(offset_y))
        bike.draw(offset_x, offset_y)

        # Check if bike passes the first flag
        first_flag_x = aligned_points[start_index][0]

        if lap_start_time is None and bike.pos[0] > first_flag_x :
            lap_start_time = time.ticks_ms()
        
        # Check if bike passes the second flag
        second_flag_x = aligned_points[-end_index][0]
        if lap_start_time is not None and bike.pos[0] > second_flag_x :
            lap_time = time.ticks_ms() - lap_start_time
            lap_start_time = None
            display.fill(0)
            # Check if it's a new record
            if record_lap_time is None or lap_time < record_lap_time:
                record_lap_time = lap_time
                thumby.saveData.setItem(track_name + "_fastestLapTime", record_lap_time)
                thumby.saveData.save()
                
                # Display "New Record" message if a new record is set
                display.drawText("New Record", 20, 20, 1)
                display.drawText(format_time(record_lap_time), 20, 30, 1)
                display.update()
                time.sleep(2)
                new_record = False
                reset_game()  # Reset the game state
                gameState = TITLE_PAGE  # Return to title screen
            else:
                # Display "New Record" message if a new record is set
                display.drawText("Try Again", 1, 10, 1)
                display.drawText(f"Time  : {format_time(lap_time)}", 10, 20, 1)
                display.drawText(f"Record: {format_time(record_lap_time)}", 10, 30, 1)
                display.update()
                time.sleep(2)
                new_record = False
                reset_game()  # Reset the game state
                gameState = TITLE_PAGE  # Return to title screen

        # Drawing lap time and record time
        if lap_start_time is not None:
            current_lap_time = time.ticks_ms() - lap_start_time
            display.drawFilledRectangle(0, 35, 72, 5, 0)
            display.drawText(format_time(current_lap_time), 0, 35, 1)
        if record_lap_time is not None:
            display.drawFilledRectangle(52, 35, 72, 5, 0)
            display.drawText(format_time(record_lap_time), 40, 35, 1)

        display.update()
        display.fill(0)