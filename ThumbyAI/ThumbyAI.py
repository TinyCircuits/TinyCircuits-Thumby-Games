import thumby
import time
import math
import random
import gc

#
# --------------------------------------------------------------------
# FONT & SCREEN SETUP
# --------------------------------------------------------------------
# Thumby includes a 72x40 pixel display. The 3x5 font in "/lib/font3x5.bin"
# saves space when drawing text on screen.
thumby.display.setFont("/lib/font3x5.bin", 3, 5, 1)
SCREEN_W = 72
SCREEN_H = 40

# Each 3x5 character occupies about 4 pixels in width (3 for the glyph + 1 spacing),
# so a single line can hold ~18 characters in 72 pixels of width.
MAX_CHARS_PER_LINE = 18

#
# --------------------------------------------------------------------
# DATASET: CELSIUS -> FAHRENHEIT (21 SAMPLES)
# --------------------------------------------------------------------
# Celsius values range from 0 to 100 in steps of 5, producing a list of 21 total 
# samples as inputs for training.
#
# Fahrenheit is computed by F = (9/5)*C + 32, producing a corresponding list of 21
# samples as targets for training.
#  
# The network sees only the numeric training pairs.
c_values = list(range(0, 101, 5))
f_values = [(9/5)*c + 32 for c in c_values]

# Normalization is required because the hidden layer uses sigmoid,
# which expects inputs and outputs in or near [0..1].
def normalize_c(c):
    return c / 100.0

def normalize_f(f):
    return (f - 32.0) / 180.0

def denormalize_f(fn):
    return fn * 180.0 + 32.0

# Build the training set by normalizing c_values and f_values.
training_inputs  = [[normalize_c(c)] for c in c_values]
training_targets = [[normalize_f(f)] for f in f_values]

#
# --------------------------------------------------------------------
# NEURAL NETWORK: 1 -> 5 -> 1 (LINEAR OUTPUT)
# --------------------------------------------------------------------
# This network has:
#   - 1 input neuron (normalized C)
#   - 5 hidden neurons (using sigmoid)
#   - 1 output neuron (using a linear activation)
# The final output is unconstrained, which helps a linear mapping like C->F.
INPUT_SIZE  = 1
HIDDEN_SIZE = 5
OUTPUT_SIZE = 1

W1 = []
B1 = []
W2 = []
B2 = []

# Training parameters
LEARNING_RATE = 0.2   # Lower rate for stability
EPOCHS = 500          # Increase to improve convergence

def init_network():
    # Initializes all weights/biases randomly in [-1, 1].
    # Runs garbage collection to free memory on the Thumby.
    global W1, B1, W2, B2
    gc.collect()

    def rand_weight():
        return random.uniform(-1, 1)

    # W1 is (HIDDEN_SIZE x INPUT_SIZE), B1 is (HIDDEN_SIZE,)
    W1 = [[rand_weight() for _ in range(INPUT_SIZE)] for _ in range(HIDDEN_SIZE)]
    B1 = [rand_weight() for _ in range(HIDDEN_SIZE)]

    # W2 is (OUTPUT_SIZE x HIDDEN_SIZE), B2 is (OUTPUT_SIZE,)
    W2 = [[rand_weight() for _ in range(HIDDEN_SIZE)] for _ in range(OUTPUT_SIZE)]
    B2 = [rand_weight() for _ in range(OUTPUT_SIZE)]

    gc.collect()

def sigmoid(x):
    # Applies a sigmoid clamp to avoid overflow on exponent.
    if x > 10:
        x = 10
    if x < -10:
        x = -10
    return 1.0 / (1.0 + math.e**(-x))

def dsigmoid(y):
    # Computes derivative of sigmoid if y=sigmoid(x).
    return y * (1.0 - y)

#
# --------------------------------------------------------------------
# FORWARD PASS (HIDDEN: SIGMOID, OUTPUT: LINEAR)
# --------------------------------------------------------------------
def forward_pass(x):
    # Passes input x through the hidden layer using sigmoid,
    # then computes a linear output with no final sigmoid.
    global W1, B1, W2, B2

    # Hidden layer
    h = []
    for i in range(HIDDEN_SIZE):
        sum_h = B1[i]
        for j in range(INPUT_SIZE):
            sum_h += W1[i][j] * x[j]
        h.append(sigmoid(sum_h))

    # Output layer (linear)
    o = []
    for i in range(OUTPUT_SIZE):
        sum_o = B2[i]
        for j in range(HIDDEN_SIZE):
            sum_o += W2[i][j] * h[j]
        o.append(sum_o)  # raw linear output
    return h, o

#
# --------------------------------------------------------------------
# BACKPROP (FINAL LAYER IS LINEAR)
# --------------------------------------------------------------------
def backprop(x, h, o, t):
    # Adjusts weights/biases in two stages:
    #  1) Linear output error
    #  2) Sigmoid hidden layer error
    global W1, B1, W2, B2

    # Output layer error: (t - o) for a linear final neuron
    output_errors = []
    for i in range(OUTPUT_SIZE):
        error = t[i] - o[i]
        output_errors.append(error)

    # Hidden layer errors (uses dsigmoid on the hidden output)
    hidden_errors = []
    for i in range(HIDDEN_SIZE):
        err_sum = 0.0
        for j in range(OUTPUT_SIZE):
            err_sum += output_errors[j] * W2[j][i]
        hidden_errors.append(err_sum * dsigmoid(h[i]))

    # Update W2, B2 (linear output layer)
    for i in range(OUTPUT_SIZE):
        for j in range(HIDDEN_SIZE):
            W2[i][j] += LEARNING_RATE * output_errors[i] * h[j]
        B2[i] += LEARNING_RATE * output_errors[i]

    # Update W1, B1 (sigmoid hidden layer)
    for i in range(HIDDEN_SIZE):
        for j in range(INPUT_SIZE):
            W1[i][j] += LEARNING_RATE * hidden_errors[i] * x[j]
        B1[i] += LEARNING_RATE * hidden_errors[i]

#
# --------------------------------------------------------------------
# TRAIN NETWORK
# --------------------------------------------------------------------
def train_network():
    # Runs EPOCHS times through the entire dataset.
    for epoch in range(EPOCHS):
        for i, inp in enumerate(training_inputs):
            t = training_targets[i]
            h, o = forward_pass(inp)
            backprop(inp, h, o, t)

#
# --------------------------------------------------------------------
# TRAINING SCREEN
# --------------------------------------------------------------------
def display_training_screen():
    # Clears the screen, draws "TRAINING..." centered, then updates.
    thumby.display.fill(0)
    text_str = "TRAINING..."
    text_str_2 = "Please Wait"
    text_width = len(text_str) * 4
    x = (SCREEN_W - text_width) // 2
    y = (SCREEN_H - 7) // 2
    thumby.display.drawText(text_str, x, y - 2, 1)
    thumby.display.drawText(text_str_2, x, y + 6, 1)
    thumby.display.update()

#
# --------------------------------------------------------------------
# WRAPPING FUNCTIONS FOR TUTORIAL
# --------------------------------------------------------------------
def wrap_text(line, max_chars=18):
    wrapped = []
    start = 0
    while start < len(line):
        wrapped.append(line[start:start+max_chars])
        start += max_chars
    return wrapped

def wrap_tutorial_lines(lines, max_chars=18):
    final = []
    for l in lines:
        if len(l) > max_chars:
            sub_lines = wrap_text(l, max_chars)
            final.extend(sub_lines)
        else:
            final.append(l)
    return final

#
# --------------------------------------------------------------------
# SCROLLABLE TUTORIAL SCREEN
# --------------------------------------------------------------------
def display_tutorial():
    raw_tutorial_lines = [
        "C->F",
        "",
        "1->5->1 network,",
        "sigmoid hidden,",
        "linear output.",
        "Steps of 5C from",
        "0 to 100.",
        "500 epochs,",
        "LR=0.2.",
        "Should predict",
        "100C near 212F.",
        "",
        "Press Up/Down to",
        "scroll. Press B to exit."
    ]

    tutorial_lines = wrap_tutorial_lines(raw_tutorial_lines, MAX_CHARS_PER_LINE)
    scroll_offset = 0

    while True:
        thumby.display.fill(0)
        for i in range(5):
            line_index = scroll_offset + i
            if line_index < len(tutorial_lines):
                thumby.display.drawText(tutorial_lines[line_index], 0, i*7, 1)
        thumby.display.update()

        if thumby.buttonD.justPressed():
            if scroll_offset < (len(tutorial_lines) - 5):
                scroll_offset += 1
            time.sleep(0.1)
        if thumby.buttonU.justPressed():
            if scroll_offset > 0:
                scroll_offset -= 1
            time.sleep(0.1)
        if thumby.buttonB.justPressed():
            break
        time.sleep(0.05)

#
# --------------------------------------------------------------------
# SCROLLABLE RESULTS SCREEN WITH WEIGHTS
# --------------------------------------------------------------------
def display_results():
    # Displays final predictions and then shows final weights/biases.
    global W1, B1, W2, B2

    result_lines = []
    result_lines.append("TRAINED NN RESULTS")

    # Predict F for each Celsius in c_values
    for c_val in c_values:
        c_norm = [normalize_c(c_val)]
        _, out = forward_pass(c_norm)
        f_pred = denormalize_f(out[0])
        line = f"{c_val}C => {f_pred:.1f}F"
        result_lines.append(line)

    # Show final weights and biases. Round to 2 decimals to fit display space.
    # W1: shape (5,1) since there is 1 input and 5 hidden
    # B1: shape (5,)
    # W2: shape (1,5) since there is 1 output and 5 hidden
    # B2: shape (1,)

    # For W1, gather each row's single value (since input=1)
    w1_values = [round(W1[i][0], 2) for i in range(HIDDEN_SIZE)]
    b1_values = [round(B1[i], 2) for i in range(HIDDEN_SIZE)]
    w2_values = [round(W2[0][i], 2) for i in range(HIDDEN_SIZE)]  # row 0, col i
    b2_value  = round(B2[0], 2)

    result_lines.append("----------")
    result_lines.append("W1:"+str(w1_values))
    result_lines.append("B1:"+str(b1_values))
    result_lines.append("W2:"+str(w2_values))
    result_lines.append("B2:"+str([b2_value]))
    result_lines.append("PRESS B TO EXIT")
    
    scroll_offset = 0
    while True:
        thumby.display.fill(0)
        for i in range(5):
            line_index = scroll_offset + i
            if line_index < len(result_lines):
                thumby.display.drawText(result_lines[line_index], 0, i*7, 1)
        thumby.display.update()

        if thumby.buttonD.justPressed():
            if scroll_offset < (len(result_lines) - 5):
                scroll_offset += 1
            time.sleep(0.1)
        if thumby.buttonU.justPressed():
            if scroll_offset > 0:
                scroll_offset -= 1
            time.sleep(0.1)
        if thumby.buttonB.justPressed():
            break
        time.sleep(0.05)

#
# --------------------------------------------------------------------
# MAIN MENU
# --------------------------------------------------------------------
menu_items = ["Train NN", "Tutorial", "Exit"]
selected_index = 0

def draw_menu():
    thumby.display.fill(0)
    thumby.display.drawText("C->F AI DEMO", 0, 0, 1)
    y = 10
    for i, item in enumerate(menu_items):
        marker = ">" if i == selected_index else " "
        line = marker + " " + item
        thumby.display.drawText(line, 0, y, 1)
        y += 8
    thumby.display.update()

def main_menu():
    global selected_index
    while True:
        draw_menu()
        if thumby.buttonU.justPressed():
            selected_index = max(0, selected_index - 1)
            time.sleep(0.1)
        if thumby.buttonD.justPressed():
            selected_index = min(len(menu_items)-1, selected_index + 1)
            time.sleep(0.1)

        if thumby.buttonA.justPressed():
            choice = menu_items[selected_index]
            if choice == "Train NN":
                init_network()
                display_training_screen()  # Shows TRAINING... in the center
                train_network()
                display_results()
            elif choice == "Tutorial":
                display_tutorial()
            elif choice == "Exit":
                break
        time.sleep(0.1)

#
# --------------------------------------------------------------------
# START PROGRAM
# --------------------------------------------------------------------
main_menu()
