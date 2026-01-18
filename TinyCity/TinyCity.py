import time
import random
import sys

sys.path.insert(1, "/Games/TinyCity")

from interface import get_interface

from data import (
    LOGO,
    TILE_LAND,
    TILE_WATER,
    TILE_FIRE_1,
    TILE_FIRE_2,
    TILE_ROAD_HORIZONTAL,
    TILE_ROAD_VERTICAL,
    TILE_ROAD_CROSS,
    TILE_ROAD_CROSS_E_VERTICAL,
    TILE_ROAD_CROSS_W_VERTICAL,
    TILE_ROAD_CROSS_N_HORIZONTAL,
    TILE_ROAD_CROSS_S_HORIZONTAL,
    TILE_ROAD_N_E,
    TILE_ROAD_S_E,
    TILE_ROAD_N_W,
    TILE_ROAD_S_W,
    TILE_ROAD_BRIDGE_HORIZONTAL,
    TILE_ROAD_BRIDGE_VERTICAL,
    TILE_ICON_RESIDENTIAL_TOOL,
    TILE_ICON_COMMERCIAL_TOOL,
    TILE_ICON_INDUSTRIAL_TOOL,
    TILE_ICON_POWERPLANT_TOOL,
    TILE_ICON_TREES_TOOL,
    TILE_ICON_PARK_TOOL,
    TILE_ICON_POLICE_TOOL,
    TILE_ICON_FIRE_TOOL,
    TILE_ICON_STADIUM_TOOL,
    TILE_ICON_ROAD_TOOL,
    TILE_ICON_POWER_TOOL,
    TILE_ICON_BULLDOZER_TOOL,
    TILE_ICON_BUDGET_TOOL,
    TILE_ICON_SAVE_TOOL,
    TILE_ICON_THEME_PARK_TOOL,
    TILE_ICON_SKYSCRAPER_TOOL,
    TILE_ICON_SCHOOL_TOOL,
    TILE_TREES,
    TILES_BUILDING,
    TILE_RESIDENTIAL_EMPTY,
    TILE_COMMERCIAL_EMPTY,
    TILE_INDUSTRIAL_EMPTY,
    MENU_OPTIONS,
    TERRAIN_MAPS,
    TERRAIN_NAMES,
    DEFAULT_TERRAIN,
    VERSION,
)
from sim import (
    Sim,
    BUILDING_INFO,
    BUILDING_RESIDENTIAL,
    BUILDING_COMMERCIAL,
    BUILDING_INDUSTRIAL,
    BUILDING_POWERPLANT,
    BUILDING_PARK,
    BUILDING_POLICE,
    BUILDING_FIRE,
    BUILDING_STADIUM,
    BUILDING_THEME_PARK,
    BUILDING_SKYSCRAPER,
    BUILDING_TREES,
    BUILDING_SCHOOL,
    BUILDING_RUBBLE,
    EDUCATION_MAINTENANCE_COST,
    FIRE_AND_POLICE_MAINTENANCE_COST,
    MAX_POPULATION_DENSITY,
    ROAD_MAINTENANCE_COST,
    ROAD_MASK,
    POWER_MASK,
    BULLDOZER_COST,
    ROAD_COST,
    POWERLINE_COST,
    BUILDING_POPULACE_MAP,
)

SCREEN_WIDTH = 72
SCREEN_HEIGHT = 40
TILE_SIZE = 8
VISIBLE_WIDTH = SCREEN_WIDTH // TILE_SIZE
VISIBLE_HEIGHT = SCREEN_HEIGHT // TILE_SIZE
BLIT_OPAQUE = -1
MAP_PADDING_TILES = 1
CENTER_CURSOR_X = VISIBLE_WIDTH // 2
CENTER_CURSOR_Y = VISIBLE_HEIGHT // 2

VIEW_MAIN_MENU = 0
VIEW_MAP = 1
VIEW_MENU = 2
VIEW_TERRAIN_SELECT = 3
VIEW_BUDGET = 4

DEBUG_HOVER = False

TOOL_ICONS = {
    "road": TILE_ICON_ROAD_TOOL,
    "power": TILE_ICON_POWER_TOOL,
    "bulldoze": TILE_ICON_BULLDOZER_TOOL,
    "budget": TILE_ICON_BUDGET_TOOL,
    "save": TILE_ICON_SAVE_TOOL,
    BUILDING_RESIDENTIAL: TILE_ICON_RESIDENTIAL_TOOL,
    BUILDING_COMMERCIAL: TILE_ICON_COMMERCIAL_TOOL,
    BUILDING_INDUSTRIAL: TILE_ICON_INDUSTRIAL_TOOL,
    BUILDING_POWERPLANT: TILE_ICON_POWERPLANT_TOOL,
    BUILDING_PARK: TILE_ICON_PARK_TOOL,
    BUILDING_THEME_PARK: TILE_ICON_THEME_PARK_TOOL,
    BUILDING_TREES: TILE_ICON_TREES_TOOL,
    BUILDING_SCHOOL: TILE_ICON_SCHOOL_TOOL,
    BUILDING_POLICE: TILE_ICON_POLICE_TOOL,
    BUILDING_FIRE: TILE_ICON_FIRE_TOOL,
    BUILDING_STADIUM: TILE_ICON_STADIUM_TOOL,
    BUILDING_SKYSCRAPER: TILE_ICON_SKYSCRAPER_TOOL,
}

notification_queue = []
current_notification = ""
notification_start_time = None
NOTIFICATION_LENGTH = 3000

cursor_x = 0
cursor_y = 0
scroll_x = 0
scroll_y = 0
cursor_frame = 0
move_hold_frames = 0
blink_frame = 0

menu_index = 0
view_mode = VIEW_MAIN_MENU
current_tool_index = 0
terrain_index = 0
random_preview_map = None

SIM = None
iface = get_interface("thumby")


def proc_at_tile(x, y):
    return ((y * 359) ^ (x * 431)) & 0xFF


def get_zone_empty_tile(building_type):
    if building_type == BUILDING_RESIDENTIAL:
        return TILE_RESIDENTIAL_EMPTY
    if building_type == BUILDING_COMMERCIAL:
        return TILE_COMMERCIAL_EMPTY
    return TILE_INDUSTRIAL_EMPTY


def get_current_tool():
    visible = SIM.get_visible_tools()
    if not visible:
        return None
    index = current_tool_index % len(visible)
    return visible[index]


def show_notification(text):
    notification_queue.append(text)


def move_cursor_to(map_x, map_y):
    global cursor_x, cursor_y, scroll_x, scroll_y
    max_scroll_x = SIM.map_width - VISIBLE_WIDTH + MAP_PADDING_TILES
    max_scroll_y = SIM.map_height - VISIBLE_HEIGHT + MAP_PADDING_TILES
    scroll_x = map_x - CENTER_CURSOR_X
    scroll_y = map_y - CENTER_CURSOR_Y
    if scroll_x < -MAP_PADDING_TILES:
        scroll_x = -MAP_PADDING_TILES
    elif scroll_x > max_scroll_x:
        scroll_x = max_scroll_x
    if scroll_y < -MAP_PADDING_TILES:
        scroll_y = -MAP_PADDING_TILES
    elif scroll_y > max_scroll_y:
        scroll_y = max_scroll_y
    cursor_x = CENTER_CURSOR_X
    cursor_y = CENTER_CURSOR_Y
    clamp_cursor_to_map()


def handle_sim_notification(message):
    if isinstance(message, tuple) and len(message) >= 3:
        text, map_x, map_y = message[0], message[1], message[2]
        show_notification(text)
        building = SIM.get_building_at(map_x, map_y)
        if building:
            width, height = SIM.get_building_size(building)
            move_cursor_to(building.x + width // 2, building.y + height // 2)
        else:
            move_cursor_to(map_x, map_y)
    else:
        show_notification(message)


def draw_notification():
    global current_notification, notification_start_time, notification_queue

    if len(notification_queue) > 5:
        notification_queue = []
        current_notification = ""
        notification_start_time = None

    if not current_notification and notification_queue:
        current_notification = notification_queue.pop(0)
        notification_start_time = time.ticks_ms()

    if current_notification and notification_start_time is not None:
        elapsed = time.ticks_diff(time.ticks_ms(), notification_start_time)
        if elapsed < NOTIFICATION_LENGTH:
            for y in range(SCREEN_HEIGHT - 8, SCREEN_HEIGHT):
                iface.display.drawLine(0, y, SCREEN_WIDTH, y, 0)
            iface.display.drawText(current_notification, 1, SCREEN_HEIGHT - 6, 1)
        else:
            current_notification = ""
            notification_start_time = None


def draw_terrain_tile(tile_x, tile_y, map_x, map_y):
    terrain = SIM.terrain_map[map_y][map_x]
    tile = TILE_WATER if terrain else TILE_LAND
    iface.display.blit(tile, tile_x, tile_y, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0)


def draw_road(tile_x, tile_y, neighbours, is_bridge):
    if is_bridge:
        if neighbours & 1 or neighbours & 4:
            tile = TILE_ROAD_BRIDGE_VERTICAL
        else:
            tile = TILE_ROAD_BRIDGE_HORIZONTAL
    else:
        if neighbours == (1 | 2 | 4 | 8):
            tile = TILE_ROAD_CROSS
        elif neighbours == (1 | 2 | 4):
            tile = TILE_ROAD_CROSS_W_VERTICAL
        elif neighbours == (1 | 2 | 8):
            tile = TILE_ROAD_CROSS_S_HORIZONTAL
        elif neighbours == (1 | 4 | 8):
            tile = TILE_ROAD_CROSS_E_VERTICAL
        elif neighbours == (2 | 4 | 8):
            tile = TILE_ROAD_CROSS_N_HORIZONTAL
        elif neighbours == (1 | 4):
            tile = TILE_ROAD_VERTICAL
        elif neighbours == (2 | 8):
            tile = TILE_ROAD_HORIZONTAL
        elif neighbours == (1 | 2):
            tile = TILE_ROAD_N_E
        elif neighbours == (2 | 4):
            tile = TILE_ROAD_S_E
        elif neighbours == (4 | 8):
            tile = TILE_ROAD_S_W
        elif neighbours == (8 | 1):
            tile = TILE_ROAD_N_W
        elif neighbours & (1 | 4):
            tile = TILE_ROAD_VERTICAL
        elif neighbours & (2 | 8):
            tile = TILE_ROAD_HORIZONTAL
        else:
            tile = TILE_ROAD_CROSS
    iface.display.blit(tile, tile_x, tile_y, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0)


def draw_traffic_overlay(tile_x, tile_y, neighbours, color):
    horizontal = neighbours & (2 | 8)
    vertical = neighbours & (1 | 4)
    if not horizontal and not vertical:
        return

    phase = (blink_frame // 6) & 1
    offsets = (1, 5) if phase == 0 else (2, 6)

    if horizontal:
        for y in (tile_y + 2, tile_y + 5):
            for x in range(tile_x + offsets[0], tile_x + TILE_SIZE - 1, 4):
                iface.display.drawLine(x, y, x + 1, y, color)
    if vertical:
        for x in (tile_x + 2, tile_x + 5):
            for y in range(tile_y + offsets[0], tile_y + TILE_SIZE - 1, 4):
                iface.display.drawLine(x, y, x, y + 1, color)


def draw_power(tile_x, tile_y, neighbours, color):
    cx = tile_x + 3
    cy = tile_y + 3
    if neighbours & 1:
        iface.display.drawLine(cx, tile_y, cx, cy, color)
    if neighbours & 2:
        iface.display.drawLine(cx, cy, tile_x + 7, cy, color)
    if neighbours & 4:
        iface.display.drawLine(cx, cy, cx, tile_y + 7, color)
    if neighbours & 8:
        iface.display.drawLine(tile_x, cy, cx, cy, color)
    iface.display.setPixel(cx, cy, color)


def draw_building_tile(tile, tile_x, tile_y, map_x, map_y, building, info):
    if not tile:
        return
    if building.type == BUILDING_RUBBLE:
        width = building.rubble_width
        height = building.rubble_height
    else:
        width = info["width"]
        height = info["height"]
    expected_len = width * height * TILE_SIZE * TILE_SIZE // 8
    if len(tile) == TILE_SIZE or len(tile) != expected_len:
        iface.display.blit(
            tile, tile_x, tile_y, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
        )
        return

    local_x = map_x - building.x
    local_y = map_y - building.y
    if not (0 <= local_x < width and 0 <= local_y < height):
        return

    full_width_px = width * TILE_SIZE
    offset_x = local_x * TILE_SIZE
    offset_y = local_y * TILE_SIZE
    sub_tile = bytearray(TILE_SIZE)
    for px in range(TILE_SIZE):
        for py in range(TILE_SIZE):
            index = (offset_x + px) + ((offset_y + py) // 8) * full_width_px
            if 0 <= index < len(tile):
                bit = 1 << ((offset_y + py) % 8)
                if tile[index] & bit:
                    sub_tile[px] |= 1 << (py % 8)

    iface.display.blit(
        sub_tile, tile_x, tile_y, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
    )


def draw_building(tile_x, tile_y, map_x, map_y, building):
    if (
        (not SIM.has_power_plant or not building.has_power)
        and not building.on_fire
        and building.type
        not in (
            BUILDING_POWERPLANT,
            BUILDING_PARK,
            BUILDING_TREES,
            BUILDING_RUBBLE,
        )
        and (blink_frame // 6) % 2 == 0
    ):
        return
    info = BUILDING_INFO[building.type]
    tile = info["tile"]
    if building.type in (
        BUILDING_RESIDENTIAL,
        BUILDING_COMMERCIAL,
        BUILDING_INDUSTRIAL,
    ):
        empty_tile = get_zone_empty_tile(building.type)
        if building.population_density <= 0:
            draw_building_tile(empty_tile, tile_x, tile_y, map_x, map_y, building, info)
        elif building.population_density >= MAX_POPULATION_DENSITY - 1:
            draw_building_tile(tile, tile_x, tile_y, map_x, map_y, building, info)
        else:
            local_x = map_x - building.x
            local_y = map_y - building.y
            index = (
                local_y * info["height"]
                + local_x
                + proc_at_tile(building.x, building.y)
            )
            threshold = BUILDING_POPULACE_MAP[index & 0xF]
            if building.population_density >= threshold and TILES_BUILDING:
                proc_val = proc_at_tile(building.x + local_x, building.y + local_y)
                small_tile = TILES_BUILDING[proc_val & 7]
                iface.display.blit(
                    small_tile,
                    tile_x,
                    tile_y,
                    TILE_SIZE,
                    TILE_SIZE,
                    BLIT_OPAQUE,
                    0,
                    0,
                )
            else:
                draw_building_tile(
                    empty_tile, tile_x, tile_y, map_x, map_y, building, info
                )
    else:
        draw_building_tile(tile, tile_x, tile_y, map_x, map_y, building, info)

    if building.on_fire:
        if (
            building.x <= map_x < building.x + info["width"]
            and building.y <= map_y < building.y + info["height"]
        ):
            phase = (
                (blink_frame // 3) + (map_x - building.x) + (map_y - building.y)
            ) % 2
            fire_tile = TILE_FIRE_1 if phase == 0 else TILE_FIRE_2
            iface.display.blit(
                fire_tile, tile_x, tile_y, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
            )


def draw_map():
    for y in range(VISIBLE_HEIGHT):
        for x in range(VISIBLE_WIDTH):
            map_x = x + scroll_x
            map_y = y + scroll_y
            if 0 <= map_x < SIM.map_width and 0 <= map_y < SIM.map_height:
                tile_x = x * TILE_SIZE
                tile_y = y * TILE_SIZE
                draw_terrain_tile(tile_x, tile_y, map_x, map_y)
                is_land = SIM.terrain_map[map_y][map_x] == 0

                building = SIM.get_building_at(map_x, map_y)
                if building:
                    draw_building(tile_x, tile_y, map_x, map_y, building)
                else:
                    connections = SIM.get_connections(map_x, map_y)
                    if connections & ROAD_MASK:
                        neighbours = SIM.get_neighbour_mask(map_x, map_y, ROAD_MASK)
                        is_bridge = not is_land
                        draw_road(tile_x, tile_y, neighbours, is_bridge)
                        if SIM.has_high_traffic(map_x, map_y):
                            traffic_color = 0 if is_bridge else 1
                            draw_traffic_overlay(
                                tile_x, tile_y, neighbours, traffic_color
                            )
                    if connections & POWER_MASK:
                        neighbours = SIM.get_neighbour_mask(map_x, map_y, POWER_MASK)
                        connection_color = 0 if is_land else 1
                        draw_power(tile_x, tile_y, neighbours, connection_color)


def draw_cursor():
    global SIM, cursor_frame
    cursor_frame = (cursor_frame + 1) % 24

    map_x = cursor_x + scroll_x
    map_y = cursor_y + scroll_y
    if 0 <= map_x < SIM.map_width and 0 <= map_y < SIM.map_height:
        cursor_color = 0 if SIM.terrain_map[map_y][map_x] == 0 else 1
    else:
        cursor_color = 1

    tool = get_current_tool()
    if tool is None:
        return
    width, height = SIM.get_tool_footprint(tool)
    origin_x = map_x - (width // 2)
    origin_y = map_y - (height // 2)
    if height == 2:
        origin_y += 1

    px = (origin_x - scroll_x) * TILE_SIZE
    py = (origin_y - scroll_y) * TILE_SIZE
    width_px = width * TILE_SIZE
    height_px = height * TILE_SIZE

    top_len = width_px
    right_len = height_px - 1
    bottom_len = width_px - 1
    left_len = height_px - 2
    perimeter = top_len + right_len + bottom_len + left_len
    if perimeter <= 0:
        return
    offset = cursor_frame % 6
    step = 6
    pos = offset
    while pos < perimeter:
        for span in range(3):
            p = pos + span
            if p >= perimeter:
                break
            if p < top_len:
                x = px + p
                y = py
            else:
                p -= top_len
                if p < right_len:
                    x = px + width_px - 1
                    y = py + 1 + p
                else:
                    p -= right_len
                    if p < bottom_len:
                        x = px + width_px - 2 - p
                        y = py + height_px - 1
                    else:
                        p -= bottom_len
                        x = px
                        y = py + height_px - 2 - p
            iface.display.setPixel(x, y, cursor_color)
        pos += step


def draw_hud():
    for y in range(0, 8):
        iface.display.drawLine(0, y, SCREEN_WIDTH, y, 0)
    iface.display.drawText("$" + str(SIM.money), 0, 0, 1)
    iface.display.drawText(SIM.get_month_year(), 40, 0, 1)
    if DEBUG_HOVER:
        map_x = cursor_x + scroll_x
        map_y = cursor_y + scroll_y
        building = SIM.get_building_at(map_x, map_y)
        if building and building.type in (
            BUILDING_RESIDENTIAL,
            BUILDING_COMMERCIAL,
            BUILDING_INDUSTRIAL,
        ):
            debug = SIM.get_growth_debug(building)
            for y in range(8, 16):
                iface.display.drawLine(0, y, SCREEN_WIDTH, y, 0)
            for y in range(16, 24):
                iface.display.drawLine(0, y, SCREEN_WIDTH, y, 0)
            line1 = "D{} R{} P{}".format(
                debug["density"], debug["road_connections"], int(debug["has_power"])
            )
            score = debug["score"]
            if score is None:
                line2 = "Sc-- Po{}".format(debug["pollution"])
            else:
                line2 = "Sc{} Po{}".format(score, debug["pollution"])
            iface.display.drawText(line1, 0, 8, 1)
            iface.display.drawText(line2, 0, 16, 1)


def draw_menu():
    for y in range(14, SCREEN_HEIGHT):
        iface.display.drawLine(0, y, SCREEN_WIDTH, y, 0)
    tool = get_current_tool()
    if tool is None:
        iface.display.drawText("No tools", 0, 16, 1)
        iface.display.drawText("B:Exit", 40, 32, 1)
        return
    tool_name = tool["name"]
    cost = tool.get("cost")
    if isinstance(tool["id"], int):
        cost = BUILDING_INFO[tool["id"]]["cost"]

    iface.display.drawText(tool_name, 0, 16, 1)
    if cost is None:
        cost_text = "--"
    else:
        cost_text = "$" + str(cost)
    iface.display.drawText(cost_text, 0, 24, 1)
    if tool["id"] == "budget":
        action_text = "A:Open"
    elif tool["id"] == "save":
        action_text = "A:Save"
    else:
        action_text = "A:Select"
    iface.display.drawText(action_text, 0, 32, 1)
    iface.display.drawText("B:Exit", 40, 32, 1)

    icon = TOOL_ICONS.get(tool["id"])
    if icon:
        iface.display.blit(
            icon, SCREEN_WIDTH - TILE_SIZE, 16, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
        )


def draw_budget_menu():
    taxes = SIM.taxes_collected
    pop_total = (
        SIM.residential_population
        + SIM.commercial_population
        + SIM.industrial_population
    )
    num_police = 0
    num_fire = 0
    num_school = 0
    for building in SIM.buildings:
        if building.type == BUILDING_POLICE:
            num_police += 1
        elif building.type == BUILDING_FIRE:
            num_fire += 1
        elif building.type == BUILDING_SCHOOL:
            num_school += 1
    police_cost = num_police * FIRE_AND_POLICE_MAINTENANCE_COST
    fire_cost = num_fire * FIRE_AND_POLICE_MAINTENANCE_COST
    school_cost = num_school * EDUCATION_MAINTENANCE_COST
    num_road_tiles = 0
    for y in range(SIM.map_height):
        for x in range(SIM.map_width):
            if SIM.get_connections(x, y) & ROAD_MASK:
                num_road_tiles += 1
    road_cost = (num_road_tiles * ROAD_MAINTENANCE_COST) // 100
    cash_flow = taxes - (police_cost + fire_cost + road_cost + school_cost)

    iface.display.drawText("C/F $" + str(cash_flow), 0, 0, 1)
    iface.display.drawText(SIM.get_month_year(), 40, 0, 1)
    iface.display.drawText("Tax " + str(SIM.tax_rate) + "%", 45, 7, 1)
    iface.display.drawText("Tax $" + str(taxes), 0, 7, 1)
    iface.display.drawText("POP " + str(pop_total), 0, 14, 1)

    iface.display.blit(
        TILE_ICON_POLICE_TOOL, 0, 20, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
    )
    iface.display.drawText("$" + str(police_cost), 10, 21, 1)
    iface.display.blit(
        TILE_ICON_FIRE_TOOL, 0, 29, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
    )
    iface.display.drawText("$" + str(fire_cost), 10, 31, 1)

    iface.display.blit(
        TILE_ICON_ROAD_TOOL, 32, 20, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
    )
    iface.display.drawText("$" + str(road_cost), 41, 21, 1)
    iface.display.blit(
        TILE_ICON_SCHOOL_TOOL, 32, 29, TILE_SIZE, TILE_SIZE, BLIT_OPAQUE, 0, 0
    )
    iface.display.drawText("$" + str(school_cost), 41, 31, 1)


def draw_terrain_preview(terrain, x, y, width, height):
    map_h = len(terrain)
    map_w = len(terrain[0])
    for py in range(height):
        map_y = (py * map_h) // height
        for px in range(width):
            map_x = (px * map_w) // width
            is_land = terrain[map_y][map_x] == 0
            iface.display.setPixel(x + px, y + py, 1 if is_land else 0)


def generate_random_terrain(width, height, land_threshold=180, smooth_steps=3):
    terrain = []
    for _ in range(height):
        row = bytearray(width)
        for x in range(width):
            row[x] = 0 if random.getrandbits(8) < land_threshold else 1
        terrain.append(row)

    for _ in range(smooth_steps):
        next_map = []
        for y in range(height):
            row = bytearray(width)
            for x in range(width):
                land_neighbors = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        ny = y + dy
                        nx = x + dx
                        if 0 <= nx < width and 0 <= ny < height:
                            if terrain[ny][nx] == 0:
                                land_neighbors += 1
                row[x] = 0 if land_neighbors >= 5 else 1
            next_map.append(row)
        terrain = next_map
    return terrain


def place_current_tool():
    map_x = cursor_x + scroll_x
    map_y = cursor_y + scroll_y
    if not (0 <= map_x < SIM.map_width and 0 <= map_y < SIM.map_height):
        return

    tool = get_current_tool()
    if tool is None:
        show_notification("No tools")
        return
    tool_id = tool["id"]

    if tool_id == "road":
        if SIM.money < ROAD_COST:
            show_notification("No money")
            return
        if SIM.get_connections(map_x, map_y) & ROAD_MASK:
            show_notification("Already built")
            return
        if SIM.place_road(map_x, map_y):
            SIM.money -= ROAD_COST
        else:
            show_notification("Invalid")
    elif tool_id == "power":
        if SIM.money < POWERLINE_COST:
            show_notification("No money")
            return
        if SIM.get_connections(map_x, map_y) & POWER_MASK:
            show_notification("Already built")
            return
        if SIM.place_powerline(map_x, map_y):
            SIM.money -= POWERLINE_COST
        else:
            show_notification("Invalid")
    elif tool_id == "bulldoze":
        if SIM.money < BULLDOZER_COST:
            show_notification("No money")
            return
        if SIM.bulldoze_at(map_x, map_y):
            SIM.money -= BULLDOZER_COST
        else:
            show_notification("Nothing")
    elif tool_id in ("budget", "save"):
        show_notification("Use menu")
    else:
        width, height = SIM.get_tool_footprint(tool)
        origin_x = map_x - (width // 2)
        origin_y = map_y - (height // 2)
        if height == 2:
            origin_y += 1
        info = BUILDING_INFO[tool_id]
        cost = info["cost"]
        if SIM.money < cost:
            show_notification("No money")
            return
        if SIM.place_building(tool_id, origin_x, origin_y):
            SIM.money -= cost
        else:
            show_notification("Invalid")


def init_game(terrain=None):
    global SIM, cursor_x, cursor_y, scroll_x, scroll_y
    SIM = Sim(
        terrain if terrain is not None else DEFAULT_TERRAIN,
        notify_callback=handle_sim_notification,
    )
    cursor_x = CENTER_CURSOR_X
    cursor_y = CENTER_CURSOR_Y
    scroll_x = 0
    scroll_y = 0
    clamp_cursor_to_map()


def save_game():
    try:
        try:
            iface.saveData.delItem("sim")
        except Exception:
            pass
        if terrain_index >= len(TERRAIN_MAPS):
            terrain_bytes = bytearray()
            for row in SIM.terrain_map:
                terrain_bytes.extend(row)
            iface.saveData.setItem("terrain_random", terrain_bytes)
        else:
            try:
                iface.saveData.delItem("terrain_random")
            except Exception:
                pass
        iface.saveData.setItem(
            "sim",
            SIM.to_save_bytes(include_terrain=False, terrain_index=terrain_index),
        )
        iface.saveData.save()
        show_notification("Saved")
        return True
    except Exception as exc:
        try:
            print("Save error:", exc)
        except Exception:
            pass
        show_notification("Save failed")
        return False


def load_game():
    if not iface.saveData.hasItem("sim"):
        show_notification("No save")
        return False
    try:
        data = iface.saveData.getItem("sim")
        terrain_override = None
        if iface.saveData.hasItem("terrain_random"):
            terrain_bytes = iface.saveData.getItem("terrain_random")
            if isinstance(terrain_bytes, list):
                terrain_bytes = bytearray(terrain_bytes)
            if len(terrain_bytes) == 48 * 48:
                terrain_override = []
                for y in range(48):
                    start = y * 48
                    terrain_override.append(
                        bytearray(terrain_bytes[start : start + 48])
                    )
        sim = Sim.from_save_bytes(
            data,
            notify_callback=handle_sim_notification,
            terrain_override=terrain_override,
        )
    except Exception:
        show_notification("Load error")
        return False

    global SIM, cursor_x, cursor_y, scroll_x, scroll_y
    SIM = sim
    global terrain_index
    terrain_index = getattr(sim, "terrain_index", 0)
    cursor_x = CENTER_CURSOR_X
    cursor_y = CENTER_CURSOR_Y
    scroll_x = 0
    scroll_y = 0
    clamp_cursor_to_map()
    show_notification("Loaded")
    return True


def init_save_data():
    try:
        iface.saveData.setName("TinyCity")
        iface.saveData.hasItem("sim")
        return
    except Exception:
        try:
            iface.saveData.setName("TinyCity2")
            show_notification("Save reset")
        except Exception:
            pass


def clamp_cursor_to_map():
    global SIM, cursor_x, cursor_y, scroll_x, scroll_y
    tool = get_current_tool()
    width, height = SIM.get_tool_footprint(tool)
    x_adjust = width // 2
    y_adjust = (height // 2) - (1 if height == 2 else 0)

    min_x = -scroll_x if scroll_x < 0 else 0
    min_y = -scroll_y if scroll_y < 0 else 0
    max_x = VISIBLE_WIDTH - 1
    max_y = VISIBLE_HEIGHT - 1
    if scroll_x + max_x >= SIM.map_width:
        max_x = SIM.map_width - 1 - scroll_x
    if scroll_y + max_y >= SIM.map_height:
        max_y = SIM.map_height - 1 - scroll_y

    min_x = max(min_x, x_adjust)
    min_y = max(min_y, y_adjust)
    max_x = min(max_x, VISIBLE_WIDTH - width + x_adjust)
    max_y = min(max_y, VISIBLE_HEIGHT - height + y_adjust)

    min_x = max(min_x, x_adjust - scroll_x)
    min_y = max(min_y, y_adjust - scroll_y)
    max_x = min(max_x, SIM.map_width - width + x_adjust - scroll_x)
    max_y = min(max_y, SIM.map_height - height + y_adjust - scroll_y)

    if max_x < min_x:
        max_x = min_x
    if max_y < min_y:
        max_y = min_y
    if cursor_x < min_x:
        cursor_x = min_x
    elif cursor_x > max_x:
        cursor_x = max_x
    if cursor_y < min_y:
        cursor_y = min_y
    elif cursor_y > max_y:
        cursor_y = max_y


def handle_input():
    global cursor_x, cursor_y, scroll_x, scroll_y
    global view_mode, menu_index, current_tool_index, terrain_index, move_hold_frames

    if view_mode == VIEW_MAIN_MENU:
        if iface.buttonU.justPressed():
            menu_index = (menu_index - 1) % len(MENU_OPTIONS)
        if iface.buttonD.justPressed():
            menu_index = (menu_index + 1) % len(MENU_OPTIONS)
        if iface.buttonA.justPressed():
            if MENU_OPTIONS[menu_index] == "New Game":
                terrain_index = 0
                view_mode = VIEW_TERRAIN_SELECT
            elif MENU_OPTIONS[menu_index] == "Load Game":
                if load_game():
                    view_mode = VIEW_MAP
        return

    if view_mode == VIEW_MAP:
        min_scroll_x = -MAP_PADDING_TILES
        min_scroll_y = -MAP_PADDING_TILES
        max_scroll_x = SIM.map_width - VISIBLE_WIDTH + MAP_PADDING_TILES
        max_scroll_y = SIM.map_height - VISIBLE_HEIGHT + MAP_PADDING_TILES
        move_dx = 0
        move_dy = 0
        if iface.buttonU.pressed():
            move_dy = -1
        elif iface.buttonD.pressed():
            move_dy = 1
        if iface.buttonL.pressed():
            move_dx = -1
        elif iface.buttonR.pressed():
            move_dx = 1

        if move_dx or move_dy:
            move_hold_frames += 1
        else:
            move_hold_frames = 0

        can_step = False
        if move_hold_frames == 1:
            can_step = True
        elif move_hold_frames > 10 and (move_hold_frames % 2 == 0):
            can_step = True

        moved = False
        if can_step and move_dy < 0:
            if scroll_y > min_scroll_y and cursor_y <= CENTER_CURSOR_Y:
                scroll_y -= 1
                moved = True
            elif cursor_y > 0:
                cursor_y -= 1
                moved = True
            elif scroll_y > min_scroll_y:
                scroll_y -= 1
                moved = True
        if can_step and move_dy > 0:
            if scroll_y < max_scroll_y and cursor_y >= CENTER_CURSOR_Y:
                scroll_y += 1
                moved = True
            elif cursor_y < VISIBLE_HEIGHT - 1:
                cursor_y += 1
                moved = True
            elif scroll_y < max_scroll_y:
                scroll_y += 1
                moved = True
        if can_step and move_dx < 0:
            if scroll_x > min_scroll_x and cursor_x <= CENTER_CURSOR_X:
                scroll_x -= 1
                moved = True
            elif cursor_x > 0:
                cursor_x -= 1
                moved = True
            elif scroll_x > min_scroll_x:
                scroll_x -= 1
                moved = True
        if can_step and move_dx > 0:
            if scroll_x < max_scroll_x and cursor_x >= CENTER_CURSOR_X:
                scroll_x += 1
                moved = True
            elif cursor_x < VISIBLE_WIDTH - 1:
                cursor_x += 1
                moved = True
            elif scroll_x < max_scroll_x:
                scroll_x += 1
                moved = True
        clamp_cursor_to_map()
        if iface.buttonA.justPressed():
            place_current_tool()
        if moved and iface.buttonA.pressed():
            tool = get_current_tool()
            if tool and tool["id"] == "road":
                place_current_tool()
        if iface.buttonB.justPressed():
            view_mode = VIEW_MENU
            visible_tools = SIM.get_visible_tools()
            if visible_tools:
                current_tool_index = current_tool_index % len(visible_tools)
        return

    if view_mode == VIEW_MENU:
        visible_tools = SIM.get_visible_tools()
        if not visible_tools:
            if iface.buttonB.justPressed():
                view_mode = VIEW_MAP
            return
        if iface.buttonL.justPressed():
            current_tool_index = (current_tool_index - 1) % len(visible_tools)
        if iface.buttonR.justPressed():
            current_tool_index = (current_tool_index + 1) % len(visible_tools)
        if iface.buttonA.justPressed():
            tool_id = visible_tools[current_tool_index]["id"]
            if tool_id == "budget":
                view_mode = VIEW_BUDGET
            elif tool_id == "save":
                if save_game():
                    current_tool_index = 0
                    view_mode = VIEW_MAP
            else:
                view_mode = VIEW_MAP
        if iface.buttonB.justPressed():
            view_mode = VIEW_MAP
        return

    if view_mode == VIEW_BUDGET:
        if iface.buttonU.justPressed():
            SIM.tax_rate = min(30, SIM.tax_rate + 1)
        if iface.buttonD.justPressed():
            SIM.tax_rate = max(0, SIM.tax_rate - 1)
        if iface.buttonA.justPressed() or iface.buttonB.justPressed():
            view_mode = VIEW_MENU
        return
    if view_mode == VIEW_TERRAIN_SELECT:
        total_terrains = len(TERRAIN_MAPS) + 1
        if iface.buttonL.justPressed():
            terrain_index = (terrain_index - 1) % total_terrains
            if terrain_index == len(TERRAIN_MAPS):
                global random_preview_map
                random_preview_map = None
        if iface.buttonR.justPressed():
            terrain_index = (terrain_index + 1) % total_terrains
            if terrain_index == len(TERRAIN_MAPS):
                global random_preview_map
                random_preview_map = None
        if iface.buttonU.justPressed() and terrain_index == len(TERRAIN_MAPS):
            global random_preview_map
            random_preview_map = generate_random_terrain(48, 48)
        if iface.buttonA.justPressed():
            if terrain_index < len(TERRAIN_MAPS):
                init_game(TERRAIN_MAPS[terrain_index])
            else:
                if random_preview_map is None:
                    random_preview_map = generate_random_terrain(48, 48)
                init_game(random_preview_map)
            view_mode = VIEW_MAP
        if iface.buttonB.justPressed():
            view_mode = VIEW_MAIN_MENU
        return


def draw_main_menu():
    iface.display.blit(LOGO, 16, 0, 40, 20, BLIT_OPAQUE, 0, 0)
    for i, option in enumerate(MENU_OPTIONS):
        y = 24 + i * 8
        prefix = ">" if i == menu_index else " "
        iface.display.drawText(prefix + option, 16, y, 1)
    version_text = "v" + VERSION
    version_x = SCREEN_WIDTH - (len(version_text) * 4) - 1
    version_y = 0
    iface.display.drawText(version_text, version_x, version_y, 1)


def draw_terrain_menu():
    iface.display.drawText("TERRAIN", 2, 2, 1)
    if terrain_index < len(TERRAIN_MAPS):
        name = TERRAIN_NAMES[terrain_index]
    else:
        name = "Random"
    iface.display.drawText(name, 5, 12, 1)
    if terrain_index >= len(TERRAIN_MAPS):
        iface.display.drawText("^Generate", 2, 22, 1)
    preview_size = 20
    preview_x = SCREEN_WIDTH - preview_size - 8
    preview_y = 4
    if terrain_index < len(TERRAIN_MAPS):
        draw_terrain_preview(
            TERRAIN_MAPS[terrain_index],
            preview_x,
            preview_y,
            preview_size,
            preview_size,
        )
    else:
        global random_preview_map
        if random_preview_map is not None:
            draw_terrain_preview(
                random_preview_map, preview_x, preview_y, preview_size, preview_size
            )
    iface.display.drawLine(
        preview_x - 1, preview_y - 1, preview_x + preview_size, preview_y - 1, 1
    )
    iface.display.drawLine(
        preview_x - 1,
        preview_y + preview_size,
        preview_x + preview_size,
        preview_y + preview_size,
        1,
    )
    iface.display.drawLine(
        preview_x - 1, preview_y - 1, preview_x - 1, preview_y + preview_size, 1
    )
    iface.display.drawLine(
        preview_x + preview_size,
        preview_y - 1,
        preview_x + preview_size,
        preview_y + preview_size,
        1,
    )
    iface.display.drawText("< > A", 1, 34, 1)
    iface.display.drawText("B:Back", 45, 34, 1)


init_save_data()
iface.display.setFont("/lib/font3x5.bin", 3, 5, 1)

init_game()

while True:
    blink_frame = (blink_frame + 1) % 24
    iface.display.fill(0)

    if view_mode == VIEW_MAIN_MENU:
        draw_main_menu()
    elif view_mode == VIEW_TERRAIN_SELECT:
        draw_terrain_menu()
    elif view_mode == VIEW_BUDGET:
        draw_budget_menu()
    else:
        draw_map()
        draw_cursor()
        draw_hud()
        if view_mode == VIEW_MENU:
            draw_menu()

        SIM.simulate_step()

    draw_notification()
    handle_input()
    iface.display.update()
    time.sleep(0.05)
