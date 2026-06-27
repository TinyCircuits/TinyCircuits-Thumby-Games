import thumby
import random
import time
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
# Display dimensions
DISP_WIDTH = 72
DISP_HEIGHT = 40

# Grid dimensions
GRID_COLS = 7
GRID_ROWS = 6

# Cell dimensions
CELL_WIDTH = DISP_WIDTH // GRID_COLS
CELL_HEIGHT = (DISP_HEIGHT - 4) // GRID_ROWS

random.seed(time.ticks_ms())

grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

def draw_grid(selected_col, ai_move=0):
    """Draws the game grid and pieces, highlighting the selected column."""
    thumby.display.fill(0)  # Clear display
    # Draw grid lines
    for i in range(0, GRID_COLS+1):
        thumby.display.drawLine(i * CELL_WIDTH, 4, i * CELL_WIDTH, DISP_HEIGHT, 1)
    for j in range(1, GRID_ROWS):
        thumby.display.drawLine(0, j * CELL_HEIGHT + 4, DISP_WIDTH, j * CELL_HEIGHT + 4, 1)
    # Draw pieces
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x = col * CELL_WIDTH
            y = row * CELL_HEIGHT + 4
            if grid[row][col] == 1:
                thumby.display.drawRectangle(x + 2, y + 2, CELL_WIDTH - 3, CELL_HEIGHT - 3, 1)
                thumby.display.drawRectangle(x + 2, y + 2, CELL_WIDTH - 4, CELL_HEIGHT - 4, 1)
            elif grid[row][col] == 2:
                thumby.display.drawRectangle(x + 2, y + 2, CELL_WIDTH - 3, CELL_HEIGHT - 3, 1)
            # Highlight the selected column with a filled rectangle at the top
            if col == selected_col:
                if ai_move:
                    thumby.display.drawFilledRectangle(x + 1, 0, CELL_WIDTH -2, CELL_HEIGHT -1, 0)
                    thumby.display.setPixel(x + 3, 3, 1)
                    thumby.display.setPixel(x + 5, 3, 1)
                    thumby.display.setPixel(x + 7, 3, 1)
                else:
                    thumby.display.drawLine(x + 2, 1, x + CELL_WIDTH // 2, 4, 1)  # Left slant
                    thumby.display.drawLine(x + CELL_WIDTH // 2, 4, x + CELL_WIDTH - 2, 1, 1)  # Right slant
    thumby.display.update()

def valid_moves():
    """Returns a list of columns that are not full."""
    return [c for c in range(GRID_COLS) if grid[0][c] == 0]

def make_move(col, player):
    """Place a piece in the specified column for the given player."""
    for row in reversed(range(GRID_ROWS)):
        if grid[row][col] == 0:
            grid[row][col] = player
            return True
    return False

def check_win(player):
    """Check if the given player has won the game."""
    # Check horizontal, vertical and diagonal conditions
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            if col + 3 < GRID_COLS and all(grid[row][col+i] == player for i in range(4)):
                return True
            if row + 3 < GRID_ROWS and all(grid[row+i][col] == player for i in range(4)):
                return True
            if col + 3 < GRID_COLS and row + 3 < GRID_ROWS and all(grid[row+i][col+i] == player for i in range(4)):
                return True
            if col + 3 < GRID_COLS and row - 3 >= 0 and all(grid[row-i][col+i] == player for i in range(4)):
                return True
    return False

def minimax(grid, depth, isMaximizing, alpha, beta):
    if depth == 0 or check_win(1) or check_win(2):
        return evaluate_board(grid)
    
    if isMaximizing:
        maxEval = float('-inf')
        for col in range(GRID_COLS):
            row = get_next_open_row(grid, col)
            if row is not None:
                grid[row][col] = 2
                eval = minimax(grid, depth - 1, False, alpha, beta)
                grid[row][col] = 0
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return maxEval
    else:
        minEval = float('inf')
        for col in range(GRID_COLS):
            row = get_next_open_row(grid, col)
            if row is not None:
                grid[row][col] = 1
                eval = minimax(grid, depth - 1, True, alpha, beta)
                grid[row][col] = 0
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return minEval


def get_next_open_row(grid, col):
    for r in range(GRID_ROWS-1, -1, -1):
        if grid[r][col] == 0:
            return r
    return None

def evaluate_board(grid):
    """ Evaluates the board for scoring based on open lines for 4 in a row """
    score = 0
    # Check horizontal locations for potential four in a row
    for row in range(GRID_ROWS):
        row_array = [int(grid[row][col]) for col in range(GRID_COLS)]
        for col in range(GRID_COLS - 3):
            window = row_array[col:col + 4]
            score += evaluate_window(window)

    # Check vertical locations for potential four in a row
    for col in range(GRID_COLS):
        col_array = [int(grid[row][col]) for row in range(GRID_ROWS)]
        for row in range(GRID_ROWS - 3):
            window = col_array[row:row + 4]
            score += evaluate_window(window)

    # Check positively sloped diagonals
    for row in range(GRID_ROWS - 3):
        for col in range(GRID_COLS - 3):
            window = [grid[row + i][col + i] for i in range(4)]
            score += evaluate_window(window)

    # Check negatively sloped diagonals
    for row in range(GRID_ROWS - 3):
        for col in range(3, GRID_COLS):
            window = [grid[row + i][col - i] for i in range(4)]
            score += evaluate_window(window)

    return score

def evaluate_window(window):
    score = 0
    if window.count(2) == 4:
        score += 1000
    elif window.count(1) == 4:
        score -= 1000
    elif window.count(2) == 3 and window.count(0) == 1:
        score += 100
    elif window.count(1) == 3 and window.count(0) == 1:
        score -= 200 # Penalise allowing a winning move
    elif window.count(2) == 2 and window.count(0) == 2:
        score += 10  # Reward positions with two AI pieces and two open slots

    return score

def ai_move():
    filled_cells = sum(grid[row][col] != 0 for row in range(GRID_ROWS) for col in range(GRID_COLS))
    # Depth settings based on difficulty level and game stage
    depth_settings = {
        0: (0, 0, 0),  # Very Easy: (Early, Mid, Late)
        1: (1, 1, 1),  # Easy: (Early, Mid, Late)
        2: (1, 2, 2),  # Medium: (Early, Mid, Late)
        3: (2, 3, 4),   # Hard: (Early, Mid, Late)
        4: (3, 4, 4)   # Ultra
    }
    
    # Select depth based on the number of filled cells
    if filled_cells < 5:
        depth = depth_settings[difficulty_level][0]  # Early game depth
    elif filled_cells < 10:
        depth = depth_settings[difficulty_level][1]  # Mid game depth
    else:
        depth = depth_settings[difficulty_level][2]  # Late game depth

    best_score = float('-inf')
    best_cols = []
    for col in range(GRID_COLS):
        row = get_next_open_row(grid, col)
        if row is not None:
            grid[row][col] = 2  # Temporarily make the move
            score = minimax(grid, depth, False, float('-inf'), float('inf'))
            grid[row][col] = 0  # Undo the move
            print("Col "+str(col)+ " score: "+str(score))
            if score > best_score:
                best_score = score
                best_cols = [col]  # Reset the list with the current column
            elif score == best_score:
                best_cols.append(col)

    best_col = random.choice(best_cols) if best_cols else random.choice(valid_moves())
    make_move(best_col, 2)


def game_loop():
    global grid,gameState,TITLE_PAGE
    current_player = random.choice([1, 2])  # 1 for Player, 2 for AI
    thumby.display.drawFilledRectangle(0, 0, 72, 8, 0)
    if current_player == 1:
        thumby.display.drawText("Player starts!", 5, 2, 1)
    else:
        thumby.display.drawText("AI starts!", 5, 2, 1)
    thumby.display.update()
    time.sleep(1.5)
    selected_col = 3  # Default starting column in the middle

    # Reset the game state
    grid = [[0 for _ in range(GRID_COLS)] for _ in range(GRID_ROWS)]

    # Randomly choose the starting player
    
    while True:
        if current_player == 1:
            draw_grid(selected_col)
            # Player's turn
            if thumby.buttonL.pressed():
                selected_col = max(0, selected_col - 1)
                draw_grid(selected_col)  # Redraw grid with new selection
                time.sleep(0.1)  # Debounce delay

            if thumby.buttonR.pressed():
                selected_col = min(GRID_COLS - 1, selected_col + 1)
                draw_grid(selected_col)  # Redraw grid with new selection
                time.sleep(0.1)  # Debounce delay

            if thumby.buttonA.pressed():
                if make_move(selected_col, 1):  # Player makes a move
                    draw_grid(selected_col, 1)  # Update the grid to show the player's move
                    if check_win(1):
                        thumby.display.drawFilledRectangle(0, 0, 72, 8, 0)
                        thumby.display.drawText("Player Wins!", 5, 2, 1)
                        thumby.display.update()
                        time.sleep(3)
                        gameState = TITLE_PAGE
                        break  # Exit the while loop to reset the game
                    current_player = 2  # Switch to AI's turn
                    thumby.display.update()

        elif current_player == 2:
            # AI's turn
            draw_grid(selected_col, 1)
            ai_move()
            draw_grid(selected_col)  # Update the grid to show the AI's move
            if check_win(2):
                thumby.display.drawFilledRectangle(0, 0, 72, 8, 0)
                thumby.display.drawText("AI Wins!", 5, 2, 1)
                thumby.display.update()
                time.sleep(3)
                gameState = TITLE_PAGE
                break  # Exit the while loop to reset the game
            current_player = 1  # Switch back to the player's turn

        time.sleep(0.1)  # General debounce delay


def display_and_select_difficulty():
    difficulties = ["Very Easy", "Easy", "Medium", "Hard", "Ultra (Slow)"]
    selected_difficulty = 1  # Default to medium difficulty

    while True:
        thumby.display.fill(0)  # Clear display

        # Display each difficulty option
        for i, difficulty in enumerate(difficulties):
            display_text = f"{i+1}. {difficulty}"  # Construct the display string with index and name
            if i == selected_difficulty:
                # Highlight the selected difficulty
                thumby.display.drawText(">", 0, i * 8, 1)  # Adjust Y-position based on display size
                thumby.display.drawText(display_text, 6, i * 8, 1)
            else:
                thumby.display.drawText(display_text, 6, i * 8, 1)

        thumby.display.update()

        # Navigation through difficulty levels
        if thumby.buttonU.pressed():
            selected_difficulty = (selected_difficulty - 1) % len(difficulties)
        elif thumby.buttonD.pressed():
            selected_difficulty = (selected_difficulty + 1) % len(difficulties)
        elif thumby.buttonA.pressed():
            # Confirm selection
            thumby.display.fill(0)  # Optional: Clear display or display a confirmation message here
            break  # Exit the loop

        time.sleep(0.1)  # Debounce buttons

    return selected_difficulty  # Return the index of the selected difficulty level


TITLE_PAGE = 0
AI_SELECTION = 1
GAME_LOOP = 2
gameState = TITLE_PAGE  # Initial state
thumby.display.setFPS(60)  # Set frame rate

# Timing for flashing text
textFlashInterval = 500  # Time in milliseconds
lastFlashTime = time.ticks_ms()

textVisible = True

# BITMAP: width: 72, height: 40
title = bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,192,112,48,24,12,14,14,14,7,7,7,7,135,103,247,247,7,7,7,7,15,14,14,30,24,24,48,96,96,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,192,240,120,60,60,152,220,216,220,220,220,30,31,199,193,192,192,192,0,192,192,192,128,192,194,3,195,194,143,15,194,192,0,128,192,192,192,192,192,192,0,128,192,195,223,207,222,92,220,220,220,220,220,216,24,248,224,128,0,0,0,0,0,0,0,
           0,0,0,0,0,0,63,255,255,0,254,255,255,195,195,195,195,227,193,0,63,127,96,127,127,0,127,127,3,7,63,63,0,63,63,7,31,63,63,0,63,63,118,118,118,54,48,0,63,127,224,224,121,123,0,0,255,255,0,0,0,0,207,255,127,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,3,7,12,29,25,27,59,51,99,99,67,192,192,128,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,128,192,192,96,112,112,113,57,56,56,28,15,7,1,0,0,0,0,0,0,0,0,
           0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,7,12,8,24,24,48,48,48,112,112,112,240,240,240,240,240,240,112,240,112,112,112,48,112,48,56,8,12,6,7,3,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

while True:
    
    if gameState == TITLE_PAGE:
        # Clear display
        thumby.display.fill(0)

        # Draw the title
        thumby.display.blit(title, 0, 0, 72, 40, -1, 0, 0)
        
        # Handle flashing text
        currentTime = time.ticks_ms()
        if currentTime - lastFlashTime > textFlashInterval:
            textVisible = not textVisible
            lastFlashTime = currentTime
        
        if textVisible:
            thumby.display.drawText("Press A", 22, 26, 1)
        
        # Update the display
        thumby.display.update()
        
        if thumby.buttonA.pressed():
            gameState = AI_SELECTION
            thumby.display.fill(0)
            time.sleep(0.3)

    elif gameState == AI_SELECTION:
        global difficulty_level
        difficulty_level = display_and_select_difficulty()
        gameState = GAME_LOOP
        time.sleep(0.5)
        thumby.display.fill(0)    
    elif gameState == GAME_LOOP:
        game_loop()
