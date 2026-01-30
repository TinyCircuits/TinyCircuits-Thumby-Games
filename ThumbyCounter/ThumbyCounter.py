import engine_main
import engine
import engine_io
import math
from engine_nodes import CameraNode, Text2DNode, EmptyNode
from engine_math import Vector2
from time import sleep_ms

#ThumbyCounter for Thumby Color
#v1.0
#by Zenghiok Ng

engine.fps_limit(30)
camera = CameraNode()

count = 0

# ----- Display nodes for "COUNT" letters individually -----
count_letters = "COUNT"
letter_spacing = 12
letter_scale = Vector2(2, 2)
label_letters = []
start_x = -(len(count_letters) - 1) * letter_spacing / 2

for i, ch in enumerate(count_letters):
    letter_node = Text2DNode(
        text=ch,
        scale=letter_scale,
        position=Vector2(start_x + i * letter_spacing, -30)
    )
    label_letters.append(letter_node)

# Number value display
value = Text2DNode(
    text="0",
    scale=Vector2(3, 3),
    position=Vector2(0, 10),
    letter_spacing=1
)

# ----- Instructions display -----
instr_scale = Vector2(1.5, 1.5)
instr_start_y = -20
instr_spacing = 20
instr_lines = [
    Text2DNode(text="", scale=instr_scale, position=Vector2(0, instr_start_y), opacity=0.0),
    Text2DNode(text="", scale=instr_scale, position=Vector2(0, instr_start_y + instr_spacing), opacity=0.0),
    Text2DNode(text="", scale=instr_scale, position=Vector2(0, instr_start_y + 2 * instr_spacing), opacity=0.0),
]

# ----- VERSION LABEL and AUTHOR -----
version_label = Text2DNode(
    text="v1.0",
    scale=Vector2(1.2, 1.2),
    position=Vector2(0, 40),
    opacity=0.0
)

author = Text2DNode(
    text="by Zenghiok Ng",
    scale=Vector2(1.2, 1.2),
    position=Vector2(0, 60),
    opacity=0.0
)

# ----- Menu Implementation -----
class Menu(EmptyNode):
    def __init__(self):
        super().__init__()
        self.entries = ["Instructions", "Quit"]
        self.selected = 0
        self.visible = False

        self.text_nodes = [
            Text2DNode(
                text=e,
                scale=Vector2(1.9, 1.9),
                position=Vector2(0, 10 - 20 * i),
                opacity=0.0
            )
            for i, e in enumerate(self.entries)
        ]

        self.arrow = Text2DNode(
            text=">",
            scale=Vector2(1.9, 1.9),
            position=Vector2(-60, 10),
            opacity=0.0
        )

    def show(self):
        self.visible = True

        # Always start on "Quit"
        self.selected = len(self.entries) - 1

        for l in label_letters:
            l.opacity = 0.0
        value.opacity = 0.0

        for node in self.text_nodes:
            node.opacity = 1.0

        self.arrow.opacity = 1.0
        version_label.opacity = 1.0
        author.opacity = 1.0
        self.update_arrow()

    def hide(self):
        self.visible = False

        for node in self.text_nodes:
            node.opacity = 0.0

        self.arrow.opacity = 0.0
        version_label.opacity = 0.0
        author.opacity = 0.0

    def up(self):
        self.selected = (self.selected - 1) % len(self.entries)
        self.update_arrow()

    def down(self):
        self.selected = (self.selected + 1) % len(self.entries)
        self.update_arrow()

    def select(self):
        choice = self.entries[self.selected]

        if choice == "Instructions":
            self.hide()
            instr_lines[0].text = "A/LB/RB: count"
            instr_lines[1].text = "B: reset"
            instr_lines[2].text = "DPad: rotate"
            for line in instr_lines:
                line.opacity = 1.0

        elif choice == "Quit":
            global running
            running = False

    def update_arrow(self):
        target = self.text_nodes[self.selected]
        self.arrow.position = Vector2(target.position.x - 60, target.position.y)

menu = Menu()
running = True
viewing_instructions = False

# ----- Rotation-aware menu input -----
def handle_menu_input(menu):
    rot = camera.rotation.z

    if abs(rot - 0) < 0.1:
        up = engine_io.UP.is_just_pressed
        down = engine_io.DOWN.is_just_pressed

    elif abs(rot - math.pi / 2) < 0.1:
        up = engine_io.RIGHT.is_just_pressed
        down = engine_io.LEFT.is_just_pressed

    elif abs(rot - math.pi) < 0.1:
        up = engine_io.DOWN.is_just_pressed
        down = engine_io.UP.is_just_pressed

    elif abs(rot + math.pi / 2) < 0.1:
        up = engine_io.LEFT.is_just_pressed
        down = engine_io.RIGHT.is_just_pressed

    else:
        return

    if up:
        menu.up()
    if down:
        menu.down()

# ----- Main Loop -----
while running:

    if engine_io.MENU.is_just_pressed:
        if menu.visible:
            menu.hide()
            viewing_instructions = False
            for line in instr_lines:
                line.opacity = 0.0
            for l in label_letters:
                l.opacity = 1.0
            value.opacity = 1.0

        elif viewing_instructions:
            viewing_instructions = False
            for line in instr_lines:
                line.opacity = 0.0
            for l in label_letters:
                l.opacity = 1.0
            value.opacity = 1.0

        else:
            menu.show()

    if menu.visible:
        handle_menu_input(menu)

        if engine_io.A.is_just_pressed or engine_io.B.is_just_pressed:
            menu.select()
            if not menu.visible:
                viewing_instructions = True

    elif viewing_instructions:
        if (engine_io.A.is_just_pressed or engine_io.B.is_just_pressed or
            engine_io.LB.is_just_pressed or engine_io.RB.is_just_pressed or
            engine_io.UP.is_just_pressed or engine_io.DOWN.is_just_pressed or
            engine_io.LEFT.is_just_pressed or engine_io.RIGHT.is_just_pressed):

            viewing_instructions = False
            for line in instr_lines:
                line.opacity = 0.0
            for l in label_letters:
                l.opacity = 1.0
            value.opacity = 1.0

    else:
        if (engine_io.A.is_just_pressed or
            engine_io.LB.is_just_pressed or
            engine_io.RB.is_just_pressed):
            count += 1
            value.text = str(count)

        if engine_io.B.is_just_pressed:
            count = 0
            value.text = "0"

        if engine_io.UP.is_just_pressed:
            camera.rotation.z = 0
        if engine_io.RIGHT.is_just_pressed:
            camera.rotation.z = math.pi / 2
        if engine_io.DOWN.is_just_pressed:
            camera.rotation.z = math.pi
        if engine_io.LEFT.is_just_pressed:
            camera.rotation.z = -math.pi / 2

    while not engine.tick():
        sleep_ms(1)

engine_io.release_all_buttons()

