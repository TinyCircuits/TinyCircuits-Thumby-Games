# Import the 'thumby' module to interact with the Thumby game system hardware, 
# 'random' for generating randomness (like maze layout), and 'time' to work with time-based functions.
import thumby
import random
import time

# Initialize the random seed with the current time in milliseconds to ensure 
# the maze generated is different every time the game starts.
random.seed(time.ticks_ms())
thumby.display.setFPS(60)
# Game settings that dictate the gameplay experience.
flash_rate = 0.03  # Controls the blinking speed of the player's avatar.
branching_factor = 0.2  # Determines the starting frequency of path splits within the maze.
direction_change_factor = 0.6  # Adjusts the starting likelihood of the path changing direction.

# Initial button states - False indicates that the button is not pressed
button_states = {'up': False, 'down': False, 'left': False, 'right': False, 'a': False, 'b': False}

# Timestamps for when buttons were first pressed, initialized to 0
button_press_times = {'up': 0, 'down': 0, 'left': 0, 'right': 0, 'a': 0, 'b': 0}

# Duration threshold in milliseconds for a button hold to count as continuous press
hold_duration_threshold = 100  # Adjust this value as needed for your game


# Numeric representations for each cardinal direction within the maze.
N, S, E, W = 1, 2, 4, 8  # North, South, East, West, respectively.
# A dictionary mapping each direction to its opposite. This helps in carving the maze paths effectively.
OPPOSITE = {N: S, S: N, E: W, W: E}

# Randomly shuffles the directions to ensure varied maze generation.
def shuffle_directions():
    directions = [(N, 0, -1), (S, 0, 1), (E, 1, 0), (W, -1, 0)]  # Direction tuples also include movement deltas (dx, dy).
    for i in range(len(directions) - 1, 0, -1):  # Fisher-Yates shuffle algorithm.
        j = random.randint(0, i)
        directions[i], directions[j] = directions[j], directions[i]
    return directions

# Iteratively carves passages in the maze grid, starting from an initial position.
def carve_passages_iteratively(start_x, start_y, grid):
    stack = [(start_x, start_y, None)]  # Initialize stack with starting position; 'None' signifies no previous direction.
    while stack:
        # Decide randomly whether to continue from the current path or to branch out.
        index = random.randint(0, len(stack) - 1) if random.random() < branching_factor else -1
        cx, cy, last_dir = stack.pop(index)  # Current position and direction.
        directions = shuffle_directions()  # Get a list of shuffled directions to explore.
        # If we have a last direction and decide not to change direction, prioritize the last direction.
        if last_dir and random.random() > direction_change_factor:
            directions.sort(key=lambda d: d[0] == last_dir, reverse=True)
        for direction, dx, dy in directions:
            nx, ny = cx + dx, cy + dy  # Calculate new position based on direction deltas.
            # Check if the new position is valid (within bounds and not already visited).
            if 0 <= nx < maze_width and 0 <= ny < maze_height and grid[ny][nx] == 0:
                grid[cy][cx] |= direction  # Mark the direction in the current cell.
                grid[ny][nx] |= OPPOSITE[direction]  # Mark the opposite direction in the new cell.
                # Add both current and new positions to the stack to explore further.
                stack.append((cx, cy, direction))
                stack.append((nx, ny, direction))
                break  # Move to the next position in the stack after carving a passage.

# Generates the maze grid with the specified width and height.
def generate_maze(width, height):
    grid = [[0] * width for _ in range(height)]  # Initialize grid with zeros (unvisited cells).
    carve_passages_iteratively(0, 0, grid)  # Start carving passages from the top-left corner.
    return grid
    
# Draws the generated maze on the Thumby display.
def draw_maze(grid):
    for y in range(maze_height):
        for x in range(maze_width):
            px, py = x * effective_cell_step, y * effective_cell_step  # Calculate pixel positions based on cell size.
            cell = grid[y][x]
            # Draw bottom and right walls based on the cell's direction flags, except for the goal cell.
            if cell & S == 0 or (x == maze_width - 1 and y == maze_height - 1):
                thumby.display.drawLine(px, py + cell_size - 1, px + cell_size - 1, py + cell_size - 1, 1)
            if cell & E == 0 and not (x == maze_width - 1 and y == maze_height - 1):
                thumby.display.drawLine(px + cell_size - 1, py, px + cell_size - 1, py + cell_size - 1, 1)
            # Draw top and left walls for all cells to ensure enclosure.
            if y == 0: thumby.display.drawLine(px, py, px + cell_size - 1, py, 1)
            if x == 0: thumby.display.drawLine(px, py, px, py + cell_size - 1, 1)

# Add a new variable to track the last 10 inputs
input_sequence = []

# This function updates the player's position based on input from the game's directional buttons.
# It also tracks the sequence of button presses for detecting special input patterns (e.g., the Konami code).
# Additionally, it ensures that the player's movement is constrained within the boundaries of the maze and
# valid according to the maze's layout.
def update_player(player_pos, grid):
    global input_sequence, maze_width, maze_height, last_move_time, button_press_times, hold_duration_threshold
    import time  # Ensure time is imported if not already
    current_time = time.ticks_ms()
    input_detected = False

    directions = {
        thumby.buttonU: ('up', 0, -1, N), 
        thumby.buttonD: ('down', 0, 1, S),
        thumby.buttonL: ('left', -1, 0, W),
        thumby.buttonR: ('right', 1, 0, E),
    }

    for button, (direction, dx, dy, dir_flag) in directions.items():
        if button.pressed():
            input_detected = True
            if not button_states[direction]:  # Button was not pressed before
                button_states[direction] = True
                button_press_times[direction] = current_time
                # Initial movement
                if grid[player_pos[1]][player_pos[0]] & dir_flag:
                    player_pos[0] += dx
                    player_pos[1] += dy
                    input_sequence.append(direction)
            else:
                # Check for continuous movement if button is held
                if current_time - button_press_times[direction] >= hold_duration_threshold:
                    button_press_times[direction] = current_time  # Reset timer for repeat action
                    if grid[player_pos[1]][player_pos[0]] & dir_flag:
                        player_pos[0] += dx
                        player_pos[1] += dy
                        input_sequence.append(direction)
        else:
            button_states[direction] = False  # Reset state when button is released

    # Handling A and B buttons
    for button, direction in [(thumby.buttonA, 'a'), (thumby.buttonB, 'b')]:
        if button.pressed():
            if not input_detected:  # Only mark input_detected if no other buttons were pressed
                input_detected = True
            if not button_states[direction]:  # This check ensures we only add once per press
                button_states[direction] = True
                button_press_times[direction] = current_time
                input_sequence.append(direction)
        else:
            button_states[direction] = False

    if input_detected:
        input_sequence = input_sequence[-10:]
        if check_konami_code():
            input_sequence = []
            flash_path(player_pos, grid, maze_width, maze_height)

    player_pos[0] = min(max(player_pos[0], 0), maze_width - 1)
    player_pos[1] = min(max(player_pos[1], 0), maze_height - 1)

konami_code = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a']
def check_konami_code():
    # Define the Konami code sequence
    print(input_sequence)
    return input_sequence == konami_code

def find_path_to_exit(start_x, start_y, grid, maze_width, maze_height):
    # Directions (N, S, E, W) and their corresponding deltas in (dx, dy) format.
    directions = [(N, 0, -1), (S, 0, 1), (E, 1, 0), (W, -1, 0)]
    
    # Stack for DFS, starting with the initial position and no predecessor.
    stack = [(start_x, start_y)]
    
    # Visited set to keep track of visited cells, initialized with the start cell.
    visited = set([(start_x, start_y)])
    
    # Predecessor map, mapping each cell to the cell from which it was visited.
    predecessor = {(start_x, start_y): None}
    
    while stack:
        # Current position
        cx, cy = stack.pop()
        
        # Check if we've reached the exit
        if cx == maze_width - 1 and cy == maze_height - 1:
            # Prepare to reconstruct and return the path from exit to start
            path = []
            current_cell = (cx, cy)
            while current_cell is not None:
                path.append(current_cell)
                current_cell = predecessor.get(current_cell)  # Use get() to avoid KeyError
            path.reverse()  # The path is reconstructed from exit to start, so we need to reverse it.
            return path
        
        # Explore neighboring cells
        for direction, dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            
            # Check if the neighbor is within bounds and not visited
            if 0 <= nx < maze_width and 0 <= ny < maze_height and (nx, ny) not in visited:
                # Check if there's a direct path between the current cell and the neighbor
                if grid[cy][cx] & direction and grid[ny][nx] & OPPOSITE[direction]:
                    stack.append((nx, ny))
                    visited.add((nx, ny))
                    predecessor[(nx, ny)] = (cx, cy)
    
    # If the exit was not found, which should not happen in a proper maze, return an empty path.
    return []




def flash_path(start_pos, maze, maze_width, maze_height):
    # Find the path from the current position to the exit.
    path = find_path_to_exit(start_pos[0], start_pos[1], maze, maze_width, maze_height)
    
    # Temporarily display the path.
    for x, y in path:
        px, py = x * effective_cell_step + 1, y * effective_cell_step + 1
        draw_player(px, py, cell_size - 2, 1)  # Reuse draw_player function to highlight the path.
        thumby.display.update()
        time.sleep(0.01)  # Adjust timing based on desired flash rate.
    
    # Optionally clear the path highlight after showing it.
    time.sleep(1)  # Show the path for a moment.
    # Redraw the maze and player to "clear" the path highlight.
    thumby.display.fill(0)
    draw_maze(maze)
    px, py = start_pos[0] * effective_cell_step + 1, start_pos[1] * effective_cell_step + 1
    draw_player(px, py, cell_size - 2, 1)
    thumby.display.update()


# Renders the player's avatar on the display as a blinking square.
def draw_player(x, y, size, brightness):
    # Draw a filled square by drawing horizontal lines across the specified size.
    for i in range(size):
        thumby.display.drawLine(x, y + i, x + size - 1, y + i, brightness)

# Displays a start screen for each level of the game, briefly pausing to allow the player to prepare.
def show_level_start_screen(level):
    thumby.display.fill(0)  # Clear the display.
    # Draw the level number at the center of the screen.
    thumby.display.drawText("Level " + str(level), 20, 20, 1)
    thumby.display.update()  # Refresh the display to show the text.
    time.sleep(1)  # Pause for a moment before starting the level.

level_times = []  # To store completion times for each level
timer_duration_base = 20  # Base duration for the timer

# The main game loop, iterating through levels with varying cell sizes.
for cell_size in range(8, 2, -1):  # Each iteration represents a new level with a different maze complexity.
    effective_cell_step = cell_size - 1  # Calculate the step between cells to adjust drawing scale.
    # Concise calculation of maze dimensions, adjusting if the size exceeds display limits.
    maze_width = 72 // effective_cell_step - int((72 // effective_cell_step * effective_cell_step) > 72 - 1)
    maze_height = 40 // effective_cell_step - int((40 // effective_cell_step * effective_cell_step) > 40 - 2)

    
    
    # Apply a random shift around ±0.3 to the branching and direction change factors for each level.
    # Ensure that the factors remain within reasonable bounds [0, 1].
    current_branching_factor = max(0, min(1, branching_factor + random.uniform(-0.3, 0.3)))
    current_direction_change_factor = max(0, min(1, direction_change_factor + random.uniform(-0.3, 0.3)))

    maze = generate_maze(maze_width, maze_height)  # Generate a new maze for the level.
    player_pos = [0, 0]  # Initialize player position at the start of the maze.
    flash_counter = 0  # Initialize the counter for controlling player avatar blinking.
    timer_start = time.ticks_ms()
    
    show_level_start_screen(9 - cell_size)  # Display the start screen for the current level.

    while True:  # Game loop for the current level.
        current_time = time.ticks_ms()
        elapsed_time = (current_time - timer_start) // 1000  # Convert milliseconds to seconds
        remaining_time = max(0, timer_duration_base - elapsed_time)
        if remaining_time == 0:
            thumby.display.fill(0)
            thumby.display.drawText("Time's Up!", 10, 20, 1)
            thumby.display.update()
            time.sleep(1)
            break  # End the game if timer runs out
        thumby.display.fill(0)  # Clear the display for drawing.
        draw_maze(maze)  # Draw the maze.
        update_player(player_pos, maze)  # Update the player's position based on input.
        flash_counter = (flash_counter + 1) % (flash_rate * 2)  # Update the flash counter.
        px, py = player_pos[0] * effective_cell_step + 1, player_pos[1] * effective_cell_step + 1  # Calculate the player's pixel position.
        if flash_counter < flash_rate: 
            draw_player(px, py, cell_size - 2, 1)  # Draw the player avatar if within the flash phase.
        # Draw timer bar
        timer_bar_length = int((remaining_time / timer_duration_base) * 72)  # Scale timer length to screen width
        thumby.display.drawLine(0, 39, timer_bar_length, 39, 1)
        thumby.display.update()  # Refresh the display with the updated scene.
        if player_pos == [maze_width - 1, maze_height - 1]:# Check if the player has reached the end of the maze.
            level_times.append(timer_duration_base - remaining_time)  # Record completion time
            break 
        #time.sleep(0.01)  # Brief pause to control game speed.
    
    if remaining_time == 0: break  # Stop game loop if time ran out
    timer_duration_base += 15  # Increase base timer duration for the next level

# Clear the display for the final message or completion times
thumby.display.fill(0)

# Check if the player won the game by completing all levels
if remaining_time > 0:
    # Display a victory message
    thumby.display.drawText("You Win!", 20, 20, 1)
else:
    # Display a victory message
    thumby.display.drawText("You Lose!", 20, 20, 1)

thumby.display.update()
time.sleep(2)  # Pause to display the win message
thumby.display.fill(0)  # Clear the display before showing times

# Display completion times for each level completed
for i, level_time in enumerate(level_times, 1):
    # Display the time for each level
    thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
    thumby.display.drawText(f"L{i}: {level_time}s", 5, (i-1) * 6, 1)

# Calculate the total time by summing up all level completion times
total_time = sum(level_times)
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
thumby.display.drawText(f"All: {total_time}s", 35, 35, 1)

# Update the display to show the completion times
thumby.display.update()
while True:
    if thumby.buttonA.pressed():break
    time.sleep(0.1)