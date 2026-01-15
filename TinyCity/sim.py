import random

from data import (
    TILE_RESIDENTIAL,
    TILE_COMMERCIAL,
    TILE_INDUSTRIAL,
    TILE_POWERPLANT,
    TILE_PARK,
    TILE_POLICE,
    TILE_FIRE,
    TILE_STADIUM,
    TILE_THEME_PARK,
    TILE_SKYSCRAPER,
    TILE_RUBBLE,
    TILE_TREES,
    TILE_SCHOOL,
    TERRAIN_MAPS,
    DEFAULT_TERRAIN,
)

TILE_SIZE = 8
ROAD_MASK = 1
POWER_MASK = 2
MAX_BUILDINGS = 128
MAX_POPULATION_DENSITY = 15
BUILDING_MAP_EMPTY = 255

STARTING_TAX_RATE = 7
STARTING_FUNDS = 10000

FIRE_AND_POLICE_MAINTENANCE_COST = 100
EDUCATION_MAINTENANCE_COST = 50
ROAD_MAINTENANCE_COST = 10
POPULATION_MULTIPLIER = 17

BUILDING_MAX_FIRE_COUNTER = 3
MIN_FRAMES_BETWEEN_DISASTER = 2500
FRAMES_PER_YEAR = MAX_BUILDINGS * 12
MIN_TIME_BETWEEN_DISASTERS = FRAMES_PER_YEAR * 2  # 50
MAX_TIME_BETWEEN_DISASTERS = FRAMES_PER_YEAR * 6  # 200
DISASTER_MESSAGE_DISPLAY_TIME = 60

SIM_INCREMENT_POP_THRESHOLD = 20
SIM_DECREMENT_POP_THRESHOLD = -30

AVERAGE_POPULATION_DENSITY = 8
SIM_BASE_SCORE = 15
SIM_AVERAGING_STRENGTH = 0
SIM_EMPLOYMENT_BOOST = 10
SIM_UNEMPLOYMENT_PENALTY = 100
SIM_INDUSTRIAL_OPPORTUNITY_BOOST = 10
SIM_COMMERCIAL_OPPORTUNITY_BOOST = 10
SIM_LOCAL_BUILDING_DISTANCE = 32
SIM_LOCAL_BUILDING_INFLUENCE = 4
SIM_STADIUM_BOOST = 100
SIM_PARK_BOOST = 5
SIM_THEME_PARK_BOOST = 15
SIM_TREES_BOOST = 2
SIM_SKYSCRAPER_BOOST = 25
SIM_SCHOOL_BOOST = 8
SIM_MAX_CRIME = 50
SIM_RANDOM_STRENGTH_MASK = 31
SIM_POLLUTION_INFLUENCE = 2
SIM_MAX_POLLUTION = 50
SIM_INDUSTRIAL_BASE_POLLUTION = 8
SIM_TRAFFIC_BASE_POLLUTION = 8
SIM_POWERPLANT_BASE_POLLUTION = 32
SIM_HEAVY_TRAFFIC_THRESHOLD = 12
SIM_IDEAL_TAX_RATE = 6
SIM_TAX_RATE_PENALTY = 10
SIM_FIRE_SPREAD_CHANCE = 64
SIM_FIRE_BURN_CHANCE = 64
SIM_FIRE_DEPT_BASE_INFLUENCE = 64
SIM_FIRE_DEPT_INFLUENCE_MULTIPLIER = 5

SAVE_MAGIC = b"MC2"
SAVE_VERSION = 3
SAVE_FLAG_INCLUDE_TERRAIN = 1 << 0

MILESTONES = {
    1950: ("Revolution", 1000),
    1970: ("Boom", 1500),
    2000: ("Millennium", 2000),
}

UNLOCK_YEAR_THEME_PARK = 1970
UNLOCK_YEAR_SKYSCRAPER = 2000

BULLDOZER_COST = 1
ROAD_COST = 10
POWERLINE_COST = 5

BUILDING_NONE = 0
BUILDING_RESIDENTIAL = 1
BUILDING_COMMERCIAL = 2
BUILDING_INDUSTRIAL = 3
BUILDING_POWERPLANT = 4
BUILDING_PARK = 5
BUILDING_POLICE = 6
BUILDING_FIRE = 7
BUILDING_STADIUM = 8
BUILDING_RUBBLE = 9
BUILDING_THEME_PARK = 11
BUILDING_SKYSCRAPER = 12
BUILDING_TREES = 13
BUILDING_SCHOOL = 14

BUILDING_INFO = {
    BUILDING_NONE: {"cost": 0, "width": 0, "height": 0, "tile": None, "name": "None"},
    BUILDING_RESIDENTIAL: {
        "cost": 100,
        "width": 2,
        "height": 2,
        "tile": TILE_RESIDENTIAL,
        "name": "Residential",
    },
    BUILDING_COMMERCIAL: {
        "cost": 100,
        "width": 2,
        "height": 2,
        "tile": TILE_COMMERCIAL,
        "name": "Commercial",
    },
    BUILDING_INDUSTRIAL: {
        "cost": 100,
        "width": 2,
        "height": 2,
        "tile": TILE_INDUSTRIAL,
        "name": "Industrial",
    },
    BUILDING_POWERPLANT: {
        "cost": 3000,
        "width": 3,
        "height": 3,
        "tile": TILE_POWERPLANT,
        "name": "Power",
    },
    BUILDING_PARK: {
        "cost": 50,
        "width": 2,
        "height": 2,
        "tile": TILE_PARK,
        "name": "Park",
    },
    BUILDING_POLICE: {
        "cost": 500,
        "width": 2,
        "height": 2,
        "tile": TILE_POLICE,
        "name": "Police",
    },
    BUILDING_FIRE: {
        "cost": 500,
        "width": 2,
        "height": 2,
        "tile": TILE_FIRE,
        "name": "Fire",
    },
    BUILDING_STADIUM: {
        "cost": 3000,
        "width": 3,
        "height": 3,
        "tile": TILE_STADIUM,
        "name": "Stadium",
    },
    BUILDING_THEME_PARK: {
        "cost": 5000,
        "width": 3,
        "height": 3,
        "tile": TILE_THEME_PARK,
        "name": "Theme Park",
    },
    BUILDING_SKYSCRAPER: {
        "cost": 8000,
        "width": 3,
        "height": 3,
        "tile": TILE_SKYSCRAPER,
        "name": "Skyscraper",
    },
    BUILDING_TREES: {
        "cost": 10,
        "width": 1,
        "height": 1,
        "tile": TILE_TREES,
        "name": "Trees",
    },
    BUILDING_SCHOOL: {
        "cost": 500,
        "width": 2,
        "height": 2,
        "tile": TILE_SCHOOL,
        "name": "School",
    },
    BUILDING_RUBBLE: {
        "cost": 0,
        "width": 1,
        "height": 1,
        "tile": TILE_RUBBLE,
        "name": "Rubble",
    },
}

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

BUILDING_POPULACE_MAP = [1, 13, 5, 11, 7, 14, 3, 4, 1, 6, 12, 2, 10, 9, 11, 8]

TOOLS = [
    {"id": "road", "name": "Road", "cost": ROAD_COST},
    {"id": "power", "name": "Power", "cost": POWERLINE_COST},
    {"id": "bulldoze", "name": "Bulldoze", "cost": BULLDOZER_COST},
    {"id": BUILDING_RESIDENTIAL, "name": "Residential"},
    {"id": BUILDING_COMMERCIAL, "name": "Commercial"},
    {"id": BUILDING_INDUSTRIAL, "name": "Industrial"},
    {"id": BUILDING_POWERPLANT, "name": "Power Plant"},
    {"id": BUILDING_PARK, "name": "Park"},
    {"id": BUILDING_THEME_PARK, "name": "Theme Park"},
    {"id": BUILDING_TREES, "name": "Trees"},
    {"id": BUILDING_SCHOOL, "name": "School"},
    {"id": BUILDING_POLICE, "name": "Police Station"},
    {"id": BUILDING_FIRE, "name": "Fire Station"},
    {"id": BUILDING_STADIUM, "name": "Stadium"},
    {"id": BUILDING_SKYSCRAPER, "name": "Skyscraper"},
    {"id": "budget", "name": "Budget"},
    {"id": "save", "name": "Save"},
]


def _u16_to_bytes(value):
    return bytearray((value & 0xFF, (value >> 8) & 0xFF))


def _u32_to_bytes(value):
    return bytearray(
        (
            value & 0xFF,
            (value >> 8) & 0xFF,
            (value >> 16) & 0xFF,
            (value >> 24) & 0xFF,
        )
    )


def _i32_to_bytes(value):
    if value < 0:
        value = (1 << 32) + value
    return _u32_to_bytes(value)


def _read_u16(data, index):
    value = data[index] | (data[index + 1] << 8)
    return value, index + 2


def _read_u32(data, index):
    value = (
        data[index]
        | (data[index + 1] << 8)
        | (data[index + 2] << 16)
        | (data[index + 3] << 24)
    )
    return value, index + 4


def _read_i32(data, index):
    value, index = _read_u32(data, index)
    if value & (1 << 31):
        value -= 1 << 32
    return value, index


def _random_in_range(min_val, max_val):
    span = max_val - min_val + 1
    if span <= 0:
        return min_val
    return min_val + (random.getrandbits(16) % span)


class Building:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = BUILDING_NONE
        self.population_density = 0
        self.on_fire = 0
        self.heavy_traffic = False
        self.has_power = False
        self.rubble_width = 1
        self.rubble_height = 1


class Sim:
    def __init__(
        self,
        terrain_map,
        connection_map=None,
        buildings=None,
        year=1900,
        month=0,
        notify_callback=None,
    ):
        if terrain_map and isinstance(terrain_map[0], bytearray):
            self.terrain_map = terrain_map
        else:
            self.terrain_map = [bytearray(row) for row in terrain_map]
        self.map_height = len(self.terrain_map)
        self.map_width = len(self.terrain_map[0])

        if connection_map is None:
            self.connection_map = [
                bytearray(self.map_width) for _ in range(self.map_height)
            ]
        else:
            if connection_map and isinstance(connection_map[0], bytearray):
                self.connection_map = connection_map
            else:
                self.connection_map = [bytearray(row) for row in connection_map]

        if buildings is None:
            self.buildings = [Building() for _ in range(MAX_BUILDINGS)]
        else:
            self.buildings = buildings

        self.building_map = [
            bytearray([BUILDING_MAP_EMPTY] * self.map_width)
            for _ in range(self.map_height)
        ]
        self._rebuild_building_map()

        self.year = year
        self.month = month
        self.simulation_step = 0

        self.money = STARTING_FUNDS
        self.tax_rate = STARTING_TAX_RATE

        self.residential_population = 0
        self.industrial_population = 0
        self.commercial_population = 0

        self.taxes_collected = 0
        self.police_budget = 0
        self.fire_budget = 0
        self.road_budget = 0
        self.school_budget = 0

        self.time_to_next_disaster = MAX_TIME_BETWEEN_DISASTERS
        self.power_grid = [bytearray(self.map_width) for _ in range(self.map_height)]
        self.has_power_plant = False
        self.notify_callback = notify_callback

    def get_building_size(self, building):
        if building.type == BUILDING_RUBBLE:
            return building.rubble_width, building.rubble_height
        info = BUILDING_INFO[building.type]
        return info["width"], info["height"]

    def get_tool_footprint(self, tool):
        if tool and isinstance(tool["id"], int):
            info = BUILDING_INFO[tool["id"]]
            return info["width"], info["height"]
        return 1, 1

    def get_visible_tools(self):
        return [tool for tool in TOOLS if self.is_tool_unlocked(tool["id"])]

    def is_tool_unlocked(self, tool_id):
        if tool_id == BUILDING_THEME_PARK:
            return self.year >= UNLOCK_YEAR_THEME_PARK
        if tool_id == BUILDING_SKYSCRAPER:
            return self.year >= UNLOCK_YEAR_SKYSCRAPER
        return True

    def _rebuild_building_map(self):
        for y in range(self.map_height):
            for x in range(self.map_width):
                self.building_map[y][x] = BUILDING_MAP_EMPTY
        for index, building in enumerate(self.buildings):
            if building.type:
                width, height = self.get_building_size(building)
                for y in range(building.y, building.y + height):
                    for x in range(building.x, building.x + width):
                        if 0 <= x < self.map_width and 0 <= y < self.map_height:
                            self.building_map[y][x] = index

    def get_building_at(self, x, y):
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            index = self.building_map[y][x]
            if index != BUILDING_MAP_EMPTY:
                building = self.buildings[index]
                if building.type:
                    return building
        return None

    def is_terrain_clear(self, x, y):
        return self.terrain_map[y][x] == 0

    def get_connections(self, x, y):
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            return self.connection_map[y][x]
        return 0

    def set_connections(self, x, y, new_val):
        if 0 <= x < self.map_width and 0 <= y < self.map_height:
            self.connection_map[y][x] = new_val

    def add_connection(self, x, y, mask):
        self.set_connections(x, y, self.get_connections(x, y) | mask)

    def clear_connection(self, x, y, mask):
        self.set_connections(x, y, self.get_connections(x, y) & (~mask))

    def get_neighbour_mask(self, x, y, mask):
        neighbours = 0
        if y > 0 and (self.get_connections(x, y - 1) & mask):
            neighbours |= 1
        if x < self.map_width - 1 and (self.get_connections(x + 1, y) & mask):
            neighbours |= 2
        if y < self.map_height - 1 and (self.get_connections(x, y + 1) & mask):
            neighbours |= 4
        if x > 0 and (self.get_connections(x - 1, y) & mask):
            neighbours |= 8
        return neighbours

    def is_suitable_for_bridge(self, x, y, mask):
        neighbours = self.get_neighbour_mask(x, y, mask)
        straight = neighbours in (1, 2, 4, 8, 1 | 4, 2 | 8)
        if not straight:
            return False
        if neighbours & 1 and not self.is_terrain_clear(x, y - 1):
            if self.get_neighbour_mask(x, y - 1, mask) & (2 | 8):
                return False
        if neighbours & 2 and not self.is_terrain_clear(x + 1, y):
            if self.get_neighbour_mask(x + 1, y, mask) & (1 | 4):
                return False
        if neighbours & 4 and not self.is_terrain_clear(x, y + 1):
            if self.get_neighbour_mask(x, y + 1, mask) & (2 | 8):
                return False
        if neighbours & 8 and not self.is_terrain_clear(x - 1, y):
            if self.get_neighbour_mask(x - 1, y, mask) & (1 | 4):
                return False
        return True

    def has_high_traffic(self, map_x, map_y):
        for building in self.buildings:
            if not building.type or not building.heavy_traffic:
                continue
            width, height = self.get_building_size(building)
            if map_x < building.x - 1 or map_y < building.y - 1:
                continue
            if map_x > building.x + width or map_y > building.y + height:
                continue
            return True
        return False

    def can_place_building(self, building_type, x, y):
        info = BUILDING_INFO[building_type]
        width = info["width"]
        height = info["height"]
        if x + width > self.map_width or y + height > self.map_height:
            return False
        for j in range(y, y + height):
            for i in range(x, x + width):
                if not self.is_terrain_clear(i, j):
                    return False
                if self.get_connections(i, j) & ROAD_MASK:
                    return False
                index = self.building_map[j][i]
                if index != BUILDING_MAP_EMPTY:
                    building = self.buildings[index]
                    if building.type != BUILDING_RUBBLE:
                        return False
        return True

    def place_building(self, building_type, x, y):
        if not self.can_place_building(building_type, x, y):
            return False

        rubble_to_clear = []
        info = BUILDING_INFO[building_type]
        for j in range(y, y + info["height"]):
            for i in range(x, x + info["width"]):
                index = self.building_map[j][i]
                if index != BUILDING_MAP_EMPTY:
                    building = self.buildings[index]
                    if (
                        building.type == BUILDING_RUBBLE
                        and building not in rubble_to_clear
                    ):
                        rubble_to_clear.append(building)
        for building in rubble_to_clear:
            self.destroy_building(building, rubble=False)

        slot = -1
        for i, building in enumerate(self.buildings):
            if building.type == BUILDING_NONE:
                slot = i
                break
        if slot < 0:
            for i, building in enumerate(self.buildings):
                if building.type == BUILDING_RUBBLE:
                    slot = i
                    break
        if slot < 0:
            return False

        building = self.buildings[slot]
        building.type = building_type
        building.x = x
        building.y = y
        building.population_density = 0
        building.on_fire = 0
        building.heavy_traffic = False
        building.has_power = False
        building.rubble_width = BUILDING_INFO[building_type]["width"]
        building.rubble_height = BUILDING_INFO[building_type]["height"]

        info = BUILDING_INFO[building_type]
        power_mask = 0 if building_type == BUILDING_PARK else POWER_MASK
        for j in range(y, y + info["height"]):
            for i in range(x, x + info["width"]):
                self.set_connections(i, j, power_mask)
                self.building_map[j][i] = slot

        return True

    def destroy_building(self, building, rubble=True):
        width, height = self.get_building_size(building)
        for j in range(building.y, building.y + height):
            for i in range(building.x, building.x + width):
                self.set_connections(i, j, 0)
                if 0 <= i < self.map_width and 0 <= j < self.map_height:
                    self.building_map[j][i] = BUILDING_MAP_EMPTY

        building.on_fire = 0
        if rubble:
            building.type = BUILDING_RUBBLE
            building.rubble_width = width
            building.rubble_height = height
            for j in range(building.y, building.y + height):
                for i in range(building.x, building.x + width):
                    self.building_map[j][i] = self.buildings.index(building)
        else:
            building.type = BUILDING_NONE
            building.population_density = 0
            building.on_fire = 0
            building.heavy_traffic = False
            building.has_power = False
            building.rubble_width = 1
            building.rubble_height = 1

    def bulldoze_at(self, x, y):
        building = self.get_building_at(x, y)
        if building:
            if building.type == BUILDING_RUBBLE:
                self.destroy_building(building, rubble=False)
                # Defensive rebuild to clear any stale rubble footprints.
                self._rebuild_building_map()
            else:
                self.destroy_building(building, rubble=True)
            return True
        if self.get_connections(x, y):
            self.set_connections(x, y, 0)
            return True
        return False

    def place_road(self, x, y):
        if self.get_building_at(x, y):
            return False
        if self.get_connections(x, y) & ROAD_MASK:
            return False
        if self.is_terrain_clear(x, y) or self.is_suitable_for_bridge(x, y, ROAD_MASK):
            self.add_connection(x, y, ROAD_MASK)
            return True
        return False

    def place_powerline(self, x, y):
        if self.get_building_at(x, y):
            return False
        if self.get_connections(x, y) & POWER_MASK:
            return False
        if self.is_terrain_clear(x, y) or self.is_suitable_for_bridge(x, y, POWER_MASK):
            self.add_connection(x, y, POWER_MASK)
            return True
        return False

    def get_num_road_connections(self, building):
        width, height = self.get_building_size(building)
        count = 0
        if building.y > 0:
            for i in range(width):
                if self.get_connections(building.x + i, building.y - 1) & ROAD_MASK:
                    count += 1
        if building.y + height < self.map_height:
            for i in range(width):
                if (
                    self.get_connections(building.x + i, building.y + height)
                    & ROAD_MASK
                ):
                    count += 1
        if building.x > 0:
            for i in range(height):
                if self.get_connections(building.x - 1, building.y + i) & ROAD_MASK:
                    count += 1
        if building.x + width < self.map_width:
            for i in range(height):
                if self.get_connections(building.x + width, building.y + i) & ROAD_MASK:
                    count += 1
        return count

    def _manhattan_distance(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    def get_month_year(self):
        return "{} {}".format(MONTHS[self.month], self.year)

    def calculate_power_connectivity(self):
        self.power_grid = [bytearray(self.map_width) for _ in range(self.map_height)]
        stack = []
        self.has_power_plant = False
        for building in self.buildings:
            if building.type == BUILDING_POWERPLANT:
                self.has_power_plant = True
                stack.append((building.x, building.y))

        while stack:
            x, y = stack.pop()
            if not (0 <= x < self.map_width and 0 <= y < self.map_height):
                continue
            if self.power_grid[y][x]:
                continue
            if not (self.get_connections(x, y) & POWER_MASK):
                continue
            self.power_grid[y][x] = 1
            stack.append((x + 1, y))
            stack.append((x - 1, y))
            stack.append((x, y + 1))
            stack.append((x, y - 1))

        for building in self.buildings:
            if building.type:
                building.has_power = self.power_grid[building.y][building.x]

    def count_population(self):
        self.residential_population = 0
        self.industrial_population = 0
        self.commercial_population = 0
        for building in self.buildings:
            if building.type == BUILDING_RESIDENTIAL:
                self.residential_population += building.population_density
            elif building.type == BUILDING_INDUSTRIAL:
                self.industrial_population += building.population_density
            elif building.type == BUILDING_COMMERCIAL:
                self.commercial_population += building.population_density

    def do_budget(self):
        total_population = (
            self.residential_population
            + self.commercial_population
            + self.residential_population
        ) * POPULATION_MULTIPLIER
        self.taxes_collected = (total_population * self.tax_rate) // 100
        self.money += self.taxes_collected

        num_police = 0
        num_fire = 0
        num_school = 0
        for building in self.buildings:
            if building.type == BUILDING_POLICE:
                num_police += 1
            elif building.type == BUILDING_FIRE:
                num_fire += 1
            elif building.type == BUILDING_SCHOOL:
                num_school += 1

        self.police_budget = num_police
        self.fire_budget = num_fire
        self.school_budget = num_school
        self.money -= FIRE_AND_POLICE_MAINTENANCE_COST * num_police
        self.money -= FIRE_AND_POLICE_MAINTENANCE_COST * num_fire
        self.money -= EDUCATION_MAINTENANCE_COST * num_school

        num_road_tiles = 0
        for y in range(self.map_height):
            for x in range(self.map_width):
                if self.get_connections(x, y) & ROAD_MASK:
                    num_road_tiles += 1
        self.road_budget = (num_road_tiles * ROAD_MAINTENANCE_COST) // 100
        self.money -= self.road_budget

    def _spread_fire(self, building):
        width, height = self.get_building_size(building)
        x1 = building.x - 2 if building.x > 1 else building.x
        y1 = building.y - 2 if building.y > 1 else building.y
        x2 = building.x + width + 2
        y2 = building.y + height + 2
        spread_dir = random.getrandbits(2)

        if spread_dir & 1:
            for j in range(building.y, building.y + height):
                neighbour = self.get_building_at(x1 if spread_dir & 2 else x2, j)
                if (
                    neighbour
                    and not neighbour.on_fire
                    and neighbour.type not in (BUILDING_PARK, BUILDING_RUBBLE)
                ):
                    neighbour.on_fire = 1
                    return True
        else:
            for i in range(building.x, building.x + width):
                neighbour = self.get_building_at(i, y1 if spread_dir & 2 else y2)
                if (
                    neighbour
                    and not neighbour.on_fire
                    and neighbour.type not in (BUILDING_PARK, BUILDING_RUBBLE)
                ):
                    neighbour.on_fire = 1
                    return True
        return False

    def simulate_building(self, building):
        population_density_change = 0

        if building.on_fire:
            if building.type == BUILDING_RUBBLE:
                building.on_fire = max(0, building.on_fire - 1)
                if random.getrandbits(8) > SIM_FIRE_SPREAD_CHANCE:
                    self._spread_fire(building)
                return

            closest_fire = 255
            for other in self.buildings:
                if other.type == BUILDING_FIRE and other.has_power:
                    distance = self._manhattan_distance(building, other)
                    if distance < closest_fire:
                        closest_fire = distance

            fire_influence = (
                SIM_FIRE_DEPT_BASE_INFLUENCE
                + closest_fire * SIM_FIRE_DEPT_INFLUENCE_MULTIPLIER
            )
            if fire_influence <= 255 and random.getrandbits(8) > fire_influence:
                building.on_fire = max(0, building.on_fire - 1)
            elif random.getrandbits(
                8
            ) > SIM_FIRE_SPREAD_CHANCE or not self._spread_fire(building):
                if random.getrandbits(8) < SIM_FIRE_BURN_CHANCE:
                    if building.on_fire >= BUILDING_MAX_FIRE_COUNTER:
                        self.destroy_building(building)
                        building.on_fire = BUILDING_MAX_FIRE_COUNTER
                    else:
                        building.on_fire += 1
            if building.on_fire == 0:
                self.destroy_building(building)
                return
            building.heavy_traffic = False
            return

        if building.type in (
            BUILDING_RESIDENTIAL,
            BUILDING_COMMERCIAL,
            BUILDING_INDUSTRIAL,
        ):
            if building.has_power:
                score = 0
                random_effect = (random.getrandbits(8) & SIM_RANDOM_STRENGTH_MASK) - (
                    SIM_RANDOM_STRENGTH_MASK // 2
                )
                score += random_effect
                score += (
                    AVERAGE_POPULATION_DENSITY - building.population_density
                ) * SIM_AVERAGING_STRENGTH
                score -= (self.tax_rate - SIM_IDEAL_TAX_RATE) * SIM_TAX_RATE_PENALTY

                population_effect = 0
                if building.type == BUILDING_RESIDENTIAL:
                    if self.residential_population < self.industrial_population:
                        population_effect += SIM_EMPLOYMENT_BOOST
                    elif (
                        self.residential_population
                        > self.industrial_population + self.commercial_population
                    ):
                        population_effect -= SIM_UNEMPLOYMENT_PENALTY
                elif building.type == BUILDING_INDUSTRIAL:
                    if (
                        self.industrial_population < self.residential_population
                        or self.industrial_population < self.commercial_population
                    ):
                        population_effect += SIM_INDUSTRIAL_OPPORTUNITY_BOOST
                elif building.type == BUILDING_COMMERCIAL:
                    if (
                        self.commercial_population < self.residential_population
                        or self.commercial_population < self.industrial_population
                    ):
                        population_effect += SIM_COMMERCIAL_OPPORTUNITY_BOOST
                score += population_effect

                is_road_connected = self.get_num_road_connections(building) >= 3
                closest_police = 24
                pollution = 0
                pollution_reduction = 0
                local_influence = 0

                if is_road_connected:
                    if building.population_density == 0:
                        score += SIM_BASE_SCORE
                    for other in self.buildings:
                        if (
                            other.type
                            and other is not building
                            and (other.has_power or other.type == BUILDING_PARK)
                            and not other.on_fire
                        ):
                            distance = self._manhattan_distance(building, other)
                            if (
                                other.type == BUILDING_POLICE
                                and distance < closest_police
                            ):
                                closest_police = distance

                            building_pollution = 0
                            if other.type == BUILDING_INDUSTRIAL:
                                building_pollution = (
                                    SIM_INDUSTRIAL_BASE_POLLUTION
                                    + other.population_density
                                    - distance
                                )
                            elif other.type == BUILDING_POWERPLANT:
                                building_pollution = (
                                    SIM_POWERPLANT_BASE_POLLUTION - distance
                                )
                            elif other.heavy_traffic:
                                building_pollution = (
                                    SIM_TRAFFIC_BASE_POLLUTION - distance
                                )

                            if building_pollution > 0:
                                pollution += building_pollution

                            if building.type == BUILDING_RESIDENTIAL:
                                if other.type == BUILDING_PARK:
                                    if distance <= SIM_LOCAL_BUILDING_DISTANCE:
                                        pollution_reduction += 2
                                elif other.type == BUILDING_TREES:
                                    if distance <= SIM_LOCAL_BUILDING_DISTANCE:
                                        pollution_reduction += 1

                            if (
                                distance <= SIM_LOCAL_BUILDING_DISTANCE
                                and self.get_num_road_connections(other) >= 3
                            ):
                                if other.type == BUILDING_INDUSTRIAL:
                                    if (
                                        other.population_density
                                        >= building.population_density
                                        and building.type == BUILDING_RESIDENTIAL
                                    ):
                                        local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                                    elif (
                                        other.population_density
                                        > building.population_density
                                        and building.type == BUILDING_COMMERCIAL
                                    ):
                                        local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                                elif other.type == BUILDING_RESIDENTIAL:
                                    if (
                                        other.population_density
                                        > building.population_density
                                        and building.type
                                        in (BUILDING_COMMERCIAL, BUILDING_INDUSTRIAL)
                                    ):
                                        local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                                elif other.type == BUILDING_COMMERCIAL:
                                    if (
                                        other.population_density
                                        >= building.population_density
                                        and building.type == BUILDING_RESIDENTIAL
                                    ):
                                        local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                                elif other.type == BUILDING_STADIUM:
                                    if building.type in (
                                        BUILDING_RESIDENTIAL,
                                        BUILDING_COMMERCIAL,
                                    ):
                                        local_influence += SIM_STADIUM_BOOST
                                elif other.type == BUILDING_SKYSCRAPER:
                                    if building.type == BUILDING_COMMERCIAL:
                                        local_influence += SIM_SKYSCRAPER_BOOST
                                elif other.type == BUILDING_PARK:
                                    if building.type == BUILDING_RESIDENTIAL:
                                        local_influence += SIM_PARK_BOOST
                                elif other.type == BUILDING_THEME_PARK:
                                    if building.type == BUILDING_RESIDENTIAL:
                                        local_influence += SIM_THEME_PARK_BOOST
                                elif other.type == BUILDING_TREES:
                                    if building.type == BUILDING_RESIDENTIAL:
                                        local_influence += SIM_TREES_BOOST
                                elif other.type == BUILDING_SCHOOL:
                                    if building.type == BUILDING_RESIDENTIAL:
                                        local_influence += SIM_SCHOOL_BOOST

                score += local_influence
                if building.type == BUILDING_RESIDENTIAL:
                    if pollution_reduction > 0:
                        pollution = max(0, pollution - pollution_reduction)
                    if pollution > SIM_MAX_POLLUTION:
                        pollution = SIM_MAX_POLLUTION
                    score -= pollution * SIM_POLLUTION_INFLUENCE

                crime = building.population_density * (closest_police - 16)
                if crime > SIM_MAX_CRIME:
                    crime = SIM_MAX_CRIME
                elif crime < 0:
                    crime = 0
                score -= crime

                if (
                    building.population_density < MAX_POPULATION_DENSITY
                    and score >= SIM_INCREMENT_POP_THRESHOLD
                ):
                    population_density_change = 1
                elif (
                    building.population_density > 0
                    and score <= SIM_DECREMENT_POP_THRESHOLD
                ):
                    population_density_change = -1

                building.heavy_traffic = (
                    building.population_density > SIM_HEAVY_TRAFFIC_THRESHOLD
                )
            else:
                building.heavy_traffic = False
                if building.population_density > 0:
                    population_density_change = -1

        if population_density_change:
            building.population_density += population_density_change
            if building.type == BUILDING_RESIDENTIAL:
                self.residential_population += population_density_change
            elif building.type == BUILDING_INDUSTRIAL:
                self.industrial_population += population_density_change
            elif building.type == BUILDING_COMMERCIAL:
                self.commercial_population += population_density_change

    def start_random_fire(self):
        attempts_left = MAX_BUILDINGS
        while attempts_left:
            index = random.getrandbits(8)
            if index < MAX_BUILDINGS:
                building = self.buildings[index]
                if (
                    building.type
                    and not building.on_fire
                    and building.type not in (BUILDING_PARK, BUILDING_RUBBLE)
                ):
                    building.on_fire = 1
                    if self.notify_callback:
                        self.notify_callback(("Fire!", building.x, building.y))
                    return True
            attempts_left -= 1
        return False

    def simulate_step(self):
        if self.simulation_step < MAX_BUILDINGS:
            building = self.buildings[self.simulation_step]
            if building.type:
                self.simulate_building(building)
        elif self.simulation_step == MAX_BUILDINGS:
            self.calculate_power_connectivity()
        elif self.simulation_step == MAX_BUILDINGS + 1:
            self.count_population()
        elif self.simulation_step == MAX_BUILDINGS + 2:
            self.simulation_step = 0
            self.month += 1
            if self.month >= 12:
                self.month = 0
                self.year += 1
                self.do_budget()
                milestone = MILESTONES.get(self.year)
                if milestone:
                    label, bonus = milestone
                    self.money += bonus
                    if self.notify_callback:
                        self.notify_callback(label + " + $" + str(bonus))
            self._tick_disaster_timer()
            return

        self.simulation_step += 1
        self._tick_disaster_timer()

    def _tick_disaster_timer(self):
        self.time_to_next_disaster -= 1
        if self.time_to_next_disaster <= 0:
            self.start_random_fire()
            self.time_to_next_disaster = _random_in_range(
                MIN_TIME_BETWEEN_DISASTERS, MAX_TIME_BETWEEN_DISASTERS
            )

    def to_save_data(self):
        buildings_data = []
        for building in self.buildings:
            buildings_data.append(
                [
                    building.x,
                    building.y,
                    building.type,
                    building.population_density,
                    building.on_fire,
                    1 if building.heavy_traffic else 0,
                    1 if building.has_power else 0,
                    building.rubble_width,
                    building.rubble_height,
                ]
            )
        return {
            "terrain": [list(row) for row in self.terrain_map],
            "connections": [list(row) for row in self.connection_map],
            "buildings": buildings_data,
            "year": self.year,
            "month": self.month,
            "money": self.money,
            "tax_rate": self.tax_rate,
            "time_to_next_disaster": self.time_to_next_disaster,
        }

    def to_save_bytes(self, include_terrain=True, terrain_index=0):
        map_size = self.map_width * self.map_height
        terrain_size = map_size if include_terrain else 0
        header_size = 20
        buildings_size = MAX_BUILDINGS * 9
        total_size = header_size + terrain_size + map_size + buildings_size
        data = bytearray(total_size)
        index = 0

        data[index : index + 3] = SAVE_MAGIC
        index += 3
        data[index] = SAVE_VERSION
        index += 1
        flags = SAVE_FLAG_INCLUDE_TERRAIN if include_terrain else 0
        data[index] = flags
        index += 1
        data[index] = self.map_width
        index += 1
        data[index] = self.map_height
        index += 1
        data[index] = terrain_index & 0xFF
        index += 1
        data[index : index + 2] = _u16_to_bytes(self.year)
        index += 2
        data[index] = self.month
        index += 1
        data[index : index + 4] = _i32_to_bytes(self.money)
        index += 4
        data[index] = self.tax_rate
        index += 1
        data[index : index + 4] = _u32_to_bytes(self.time_to_next_disaster)
        index += 4

        if include_terrain:
            for row in self.terrain_map:
                data[index : index + self.map_width] = row
                index += self.map_width
        for row in self.connection_map:
            data[index : index + self.map_width] = row
            index += self.map_width

        for building in self.buildings:
            data[index] = building.x
            data[index + 1] = building.y
            data[index + 2] = building.type
            data[index + 3] = building.population_density
            data[index + 4] = building.on_fire
            data[index + 5] = 1 if building.heavy_traffic else 0
            data[index + 6] = 1 if building.has_power else 0
            data[index + 7] = building.rubble_width
            data[index + 8] = building.rubble_height
            index += 9

        return data

    @classmethod
    def from_save_data(cls, save_data, notify_callback=None):
        terrain = [bytearray(row) for row in save_data["terrain"]]
        connections = [bytearray(row) for row in save_data["connections"]]
        buildings_data = save_data["buildings"]
        buildings = [Building() for _ in range(MAX_BUILDINGS)]
        for idx, entry in enumerate(buildings_data):
            if idx >= MAX_BUILDINGS:
                break
            building = buildings[idx]
            building.x = entry[0]
            building.y = entry[1]
            building.type = entry[2]
            building.population_density = entry[3]
            building.on_fire = entry[4]
            building.heavy_traffic = bool(entry[5])
            building.has_power = bool(entry[6])
            if len(entry) > 8:
                building.rubble_width = entry[7]
                building.rubble_height = entry[8]
            else:
                if building.type == 10:
                    building.type = BUILDING_RUBBLE
                    building.rubble_width = 4
                    building.rubble_height = 4
                elif building.type == BUILDING_RUBBLE:
                    building.rubble_width = 3
                    building.rubble_height = 3

        sim = cls(
            terrain,
            connections,
            buildings,
            save_data["year"],
            save_data["month"],
            notify_callback=notify_callback,
        )
        sim.money = save_data["money"]
        sim.tax_rate = save_data["tax_rate"]
        sim.time_to_next_disaster = save_data.get(
            "time_to_next_disaster", MAX_TIME_BETWEEN_DISASTERS
        )
        sim._rebuild_building_map()
        sim.calculate_power_connectivity()
        sim.count_population()
        return sim

    @classmethod
    def from_save_bytes(cls, save_bytes, notify_callback=None, terrain_override=None):
        if isinstance(save_bytes, list):
            save_bytes = bytearray(save_bytes)
        data = save_bytes
        if len(data) < 7 or data[0:3] != SAVE_MAGIC:
            raise ValueError("Invalid save header")
        index = 3
        version = data[index]
        index += 1
        if version == 1:
            flags = SAVE_FLAG_INCLUDE_TERRAIN
            width = data[index]
            height = data[index + 1]
            index += 2
            terrain_index = 0
        elif version in (2, SAVE_VERSION):
            flags = data[index]
            index += 1
            width = data[index]
            height = data[index + 1]
            index += 2
            terrain_index = data[index]
            index += 1
        else:
            raise ValueError("Unsupported save version")
        year, index = _read_u16(data, index)
        month = data[index]
        index += 1
        money, index = _read_i32(data, index)
        tax_rate = data[index]
        index += 1
        time_to_next_disaster, index = _read_u32(data, index)

        if terrain_override is not None:
            terrain = terrain_override
        elif flags & SAVE_FLAG_INCLUDE_TERRAIN:
            terrain = []
            for _ in range(height):
                row = bytearray(data[index : index + width])
                terrain.append(row)
                index += width
        else:
            if 0 <= terrain_index < len(TERRAIN_MAPS):
                terrain = TERRAIN_MAPS[terrain_index]
            else:
                terrain = DEFAULT_TERRAIN

        connections = []
        for _ in range(height):
            row = bytearray(data[index : index + width])
            connections.append(row)
            index += width

        buildings = [Building() for _ in range(MAX_BUILDINGS)]
        for i in range(MAX_BUILDINGS):
            if index + 6 >= len(data):
                break
            building = buildings[i]
            building.x = data[index]
            building.y = data[index + 1]
            building.type = data[index + 2]
            building.population_density = data[index + 3]
            building.on_fire = data[index + 4]
            building.heavy_traffic = bool(data[index + 5])
            building.has_power = bool(data[index + 6])
            if version >= 3 and index + 8 < len(data):
                building.rubble_width = data[index + 7]
                building.rubble_height = data[index + 8]
                index += 9
            else:
                index += 7
                if building.type == 10:
                    building.type = BUILDING_RUBBLE
                    building.rubble_width = 4
                    building.rubble_height = 4
                elif building.type == BUILDING_RUBBLE:
                    building.rubble_width = 3
                    building.rubble_height = 3
                else:
                    info = BUILDING_INFO.get(building.type)
                    if info:
                        building.rubble_width = info["width"]
                        building.rubble_height = info["height"]
            if building.type == 10:
                building.type = BUILDING_RUBBLE
                if building.rubble_width == 0:
                    building.rubble_width = 4
                if building.rubble_height == 0:
                    building.rubble_height = 4
            if building.type == BUILDING_RUBBLE:
                if building.rubble_width < 1:
                    building.rubble_width = 1
                if building.rubble_height < 1:
                    building.rubble_height = 1

        sim = cls(
            terrain,
            connections,
            buildings,
            year,
            month,
            notify_callback=notify_callback,
        )
        sim.money = money
        sim.tax_rate = tax_rate
        sim.time_to_next_disaster = time_to_next_disaster
        sim.calculate_power_connectivity()
        sim.count_population()
        sim.do_budget()
        sim.terrain_index = terrain_index
        sim._rebuild_building_map()
        return sim

    def get_growth_debug(self, building):
        info = {
            "density": building.population_density,
            "has_power": building.has_power,
            "road_connections": self.get_num_road_connections(building),
            "score": None,
            "pollution": 0,
            "crime": 0,
            "population_effect": 0,
            "local_influence": 0,
        }

        if building.type not in (
            BUILDING_RESIDENTIAL,
            BUILDING_COMMERCIAL,
            BUILDING_INDUSTRIAL,
        ):
            return info

        if not building.has_power:
            return info

        score = 0
        score += (
            AVERAGE_POPULATION_DENSITY - building.population_density
        ) * SIM_AVERAGING_STRENGTH
        score -= (self.tax_rate - SIM_IDEAL_TAX_RATE) * SIM_TAX_RATE_PENALTY

        population_effect = 0
        if building.type == BUILDING_RESIDENTIAL:
            if self.residential_population < self.industrial_population:
                population_effect += SIM_EMPLOYMENT_BOOST
            elif self.residential_population > (
                self.industrial_population + self.commercial_population
            ):
                population_effect -= SIM_UNEMPLOYMENT_PENALTY
        elif building.type == BUILDING_INDUSTRIAL:
            if (
                self.industrial_population < self.residential_population
                or self.industrial_population < self.commercial_population
            ):
                population_effect += SIM_INDUSTRIAL_OPPORTUNITY_BOOST
        elif building.type == BUILDING_COMMERCIAL:
            if (
                self.commercial_population < self.residential_population
                or self.commercial_population < self.industrial_population
            ):
                population_effect += SIM_COMMERCIAL_OPPORTUNITY_BOOST
        score += population_effect

        is_road_connected = info["road_connections"] >= 3
        closest_police = 24
        pollution = 0
        local_influence = 0

        if is_road_connected:
            for other in self.buildings:
                if (
                    other.type
                    and other is not building
                    and (other.has_power or other.type == BUILDING_PARK)
                    and not other.on_fire
                ):
                    distance = self._manhattan_distance(building, other)
                    if other.type == BUILDING_POLICE and distance < closest_police:
                        closest_police = distance

                    building_pollution = 0
                    if other.type == BUILDING_INDUSTRIAL:
                        building_pollution = (
                            SIM_INDUSTRIAL_BASE_POLLUTION
                            + other.population_density
                            - distance
                        )
                    elif other.type == BUILDING_POWERPLANT:
                        building_pollution = SIM_POWERPLANT_BASE_POLLUTION - distance
                    elif other.heavy_traffic:
                        building_pollution = SIM_TRAFFIC_BASE_POLLUTION - distance

                    if building_pollution > 0:
                        pollution += building_pollution

                    if (
                        distance <= SIM_LOCAL_BUILDING_DISTANCE
                        and self.get_num_road_connections(other) >= 3
                    ):
                        if other.type == BUILDING_INDUSTRIAL:
                            if (
                                other.population_density >= building.population_density
                                and building.type == BUILDING_RESIDENTIAL
                            ):
                                local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                            elif (
                                other.population_density > building.population_density
                                and building.type == BUILDING_COMMERCIAL
                            ):
                                local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                        elif other.type == BUILDING_RESIDENTIAL:
                            if (
                                other.population_density > building.population_density
                                and building.type
                                in (BUILDING_COMMERCIAL, BUILDING_INDUSTRIAL)
                            ):
                                local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                        elif other.type == BUILDING_COMMERCIAL:
                            if (
                                other.population_density >= building.population_density
                                and building.type == BUILDING_RESIDENTIAL
                            ):
                                local_influence += SIM_LOCAL_BUILDING_INFLUENCE
                        elif other.type == BUILDING_STADIUM:
                            if building.type in (
                                BUILDING_RESIDENTIAL,
                                BUILDING_COMMERCIAL,
                            ):
                                local_influence += SIM_STADIUM_BOOST
                        elif other.type == BUILDING_SKYSCRAPER:
                            if building.type == BUILDING_COMMERCIAL:
                                local_influence += SIM_SKYSCRAPER_BOOST
                        elif other.type == BUILDING_PARK:
                            if building.type == BUILDING_RESIDENTIAL:
                                local_influence += SIM_PARK_BOOST
                        elif other.type == BUILDING_THEME_PARK:
                            if building.type == BUILDING_RESIDENTIAL:
                                local_influence += SIM_THEME_PARK_BOOST
                        elif other.type == BUILDING_TREES:
                            if building.type == BUILDING_RESIDENTIAL:
                                local_influence += SIM_TREES_BOOST
                        elif other.type == BUILDING_SCHOOL:
                            if building.type == BUILDING_RESIDENTIAL:
                                local_influence += SIM_SCHOOL_BOOST

        score += local_influence

        if building.type == BUILDING_RESIDENTIAL:
            if pollution > SIM_MAX_POLLUTION:
                pollution = SIM_MAX_POLLUTION
            score -= pollution * SIM_POLLUTION_INFLUENCE

        crime = building.population_density * (closest_police - 16)
        if crime > SIM_MAX_CRIME:
            crime = SIM_MAX_CRIME
        elif crime < 0:
            crime = 0
        score -= crime

        info["score"] = score
        info["pollution"] = pollution
        info["crime"] = crime
        info["population_effect"] = population_effect
        info["local_influence"] = local_influence
        return info
