# world.py
# Builds the flight sim's scenery: ground, mountains, a runway, and a
# course of checkpoint gates to fly through.

from engine3d import Model, Entity

# ---- shared models (instanced many times to save memory) ----------------

# One big flat ground quad. Colour 1 = dim grey.
_GROUND_SIZE = 220
GROUND_MODEL = Model(
    verts=[
        (-_GROUND_SIZE, 0, -_GROUND_SIZE),
        (_GROUND_SIZE, 0, -_GROUND_SIZE),
        (_GROUND_SIZE, 0, _GROUND_SIZE),
        (-_GROUND_SIZE, 0, _GROUND_SIZE),
    ],
    faces=[((0, 1, 2, 3), 1, 0)],
)

# A simple 4-sided pyramid "mountain". Two shades so it reads as lit
# from one side even without real lighting.
def _make_mountain(base, height):
    b = base / 2
    verts = [
        (0, height, 0),      # 0 apex
        (-b, 0, -b),         # 1
        (b, 0, -b),          # 2
        (b, 0, b),           # 3
        (-b, 0, b),          # 4
    ]
    faces = [
        ((0, 1, 2), 2, 1),
        ((0, 2, 3), 1, 1),
        ((0, 3, 4), 2, 1),
        ((0, 4, 1), 1, 1),
    ]
    return Model(verts, faces)

MOUNTAIN_SMALL = _make_mountain(10, 14)
MOUNTAIN_BIG = _make_mountain(16, 24)

# Runway: a long grey strip plus a couple of stripe markings.
_RW_HALF_W = 3
_RW_Z0 = -32
_RW_Z1 = 12
RUNWAY_MODEL = Model(
    verts=[
        (-_RW_HALF_W, 0.02, _RW_Z0),
        (_RW_HALF_W, 0.02, _RW_Z0),
        (_RW_HALF_W, 0.02, _RW_Z1),
        (-_RW_HALF_W, 0.02, _RW_Z1),
        # centerline stripe, thin quad
        (-0.3, 0.03, _RW_Z0 + 4),
        (0.3, 0.03, _RW_Z0 + 4),
        (0.3, 0.03, _RW_Z1 - 4),
        (-0.3, 0.03, _RW_Z1 - 4),
    ],
    faces=[
        ((0, 1, 2, 3), 2, 0),
        ((4, 5, 6, 7), 0, 0),
    ],
)

# Checkpoint gate: a square outline (drawn wireframe, never culled/filled)
def _make_gate(size):
    h = size / 2
    verts = [(-h, -h, 0), (h, -h, 0), (h, h, 0), (-h, h, 0)]
    faces = [((0, 1, 2, 3), 3, 0)]
    return Model(verts, faces)

GATE_MODEL = _make_gate(9)


# ---- world layout ---------------------------------------------------------

RUNWAY_HALF_WIDTH = _RW_HALF_W
RUNWAY_Z0 = _RW_Z0
RUNWAY_Z1 = _RW_Z1
START_POS = (0.0, 0.0, -28.0)  # on the runway, ready to take off
START_YAW = 0.0

# (model, pos, base_radius, height) - base_radius/height used for collision
_MOUNTAIN_LAYOUT = [
    (MOUNTAIN_SMALL, (-22, 0, -10), 5, 14),
    (MOUNTAIN_BIG, (-28, 0, 20), 8, 24),
    (MOUNTAIN_SMALL, (-18, 0, 55), 5, 14),
    (MOUNTAIN_BIG, (24, 0, 40), 8, 24),
    (MOUNTAIN_SMALL, (20, 0, 5), 5, 14),
    (MOUNTAIN_BIG, (30, 0, 90), 8, 24),
]
MOUNTAINS = [(pos, radius, height) for (_m, pos, radius, height) in _MOUNTAIN_LAYOUT]


def build_static_entities():
    """Ground, runway and mountains - never change during play."""
    ents = [
        Entity(GROUND_MODEL, (0, 0, 0)),
        Entity(RUNWAY_MODEL, (0, 0, 0)),
    ]
    for model, pos, _radius, _height in _MOUNTAIN_LAYOUT:
        ents.append(Entity(model, pos))
    return ents


def check_mountain_collision(pos):
    """Approximate each mountain as a cone: allowed clearance height falls
    off linearly from the peak at its center to 0 at base_radius away."""
    x, y, z = pos
    for (mx, my, mz), radius, height in MOUNTAINS:
        dx = x - mx
        dz = z - mz
        dist = (dx * dx + dz * dz) ** 0.5
        if dist < radius:
            allowed = height * (1.0 - dist / radius)
            if y < allowed:
                return True
    return False


class Checkpoint:
    __slots__ = ("pos", "radius", "passed")
    def __init__(self, pos, radius=6.0):
        self.pos = pos
        self.radius = radius
        self.passed = False


def build_checkpoints():
    # A simple slalom course climbing away from the runway.
    layout = [
        (-8, 10, 35),
        (10, 16, 65),
        (-10, 22, 95),
        (8, 14, 125),
    ]
    return [Checkpoint(p) for p in layout]


def checkpoint_entities(checkpoints):
    ents = []
    for cp in checkpoints:
        if not cp.passed:
            ents.append(Entity(GATE_MODEL, cp.pos, wire=True))
    return ents
