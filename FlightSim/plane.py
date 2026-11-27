# plane.py
# Simple arcade-style flight physics: throttle -> speed -> lift, with a
# stall if you get too slow, and pitch/yaw/roll controlled by the D-pad.

from math import sin, cos, pi

MAX_SPEED = 16.0        # units/sec at full throttle
STALL_SPEED = 4.0       # below this, you fall out of the sky
GRAVITY = 9.0           # fall rate while stalled
MAX_PITCH = 0.85        # ~49 degrees
TURN_RATE = 1.1         # rad/sec
PITCH_RATE = 1.0        # rad/sec
MAX_ROLL = 0.6
ROLL_RATE = 4.5         # how fast bank angle catches up to target
THROTTLE_RATE = 0.6     # per second

LANDING_MAX_SPEED = 6.0
LANDING_MAX_PITCH = 0.18
LANDING_MAX_ROLL = 0.25


class Plane:
    def __init__(self, pos, yaw):
        self.pos = list(pos)
        self.yaw = yaw
        self.pitch = 0.0
        self.roll = 0.0
        self.speed = 0.0
        self.throttle = 0.0
        self.stalling = False
        self.crashed = False
        self.landed = False
        self.airborne = False  # becomes True once you actually leave the ground

    def update(self, dt, buttons):
        if self.crashed or self.landed:
            return

        # --- throttle ---
        if buttons.buttonA.pressed():
            self.throttle += THROTTLE_RATE * dt
        if buttons.buttonB.pressed():
            self.throttle -= THROTTLE_RATE * dt
        if self.throttle < 0.0:
            self.throttle = 0.0
        elif self.throttle > 1.0:
            self.throttle = 1.0

        # --- pitch (climb / dive) ---
        if buttons.buttonU.pressed():
            self.pitch += PITCH_RATE * dt
        if buttons.buttonD.pressed():
            self.pitch -= PITCH_RATE * dt
        if self.pitch > MAX_PITCH:
            self.pitch = MAX_PITCH
        elif self.pitch < -MAX_PITCH:
            self.pitch = -MAX_PITCH

        # --- yaw / turn + banking ---
        target_roll = 0.0
        if buttons.buttonL.pressed():
            self.yaw -= TURN_RATE * dt
            target_roll = -MAX_ROLL
        if buttons.buttonR.pressed():
            self.yaw += TURN_RATE * dt
            target_roll = MAX_ROLL
        self.roll += (target_roll - self.roll) * min(1.0, ROLL_RATE * dt)

        # keep yaw in a sane range
        if self.yaw > pi:
            self.yaw -= 2 * pi
        elif self.yaw < -pi:
            self.yaw += 2 * pi

        # --- speed follows throttle with some inertia ---
        target_speed = self.throttle * MAX_SPEED
        self.speed += (target_speed - self.speed) * min(1.0, 1.5 * dt)

        self.stalling = self.speed < STALL_SPEED

        # --- movement ---
        if self.stalling:
            # not enough airspeed to fly - nose drops and you fall
            self.pitch += (-0.35 - self.pitch) * min(1.0, 2.0 * dt)
            horiz = self.speed * 0.5
            vert = -GRAVITY * dt

        # forward vector (matches the camera's yaw-then-pitch convention
        # in engine3d.py, so movement always matches what's on screen)
        fx = sin(self.yaw) * cos(self.pitch)
        fy = sin(self.pitch)
        fz = cos(self.yaw) * cos(self.pitch)

        if self.stalling:
            self.pos[0] += fx * horiz * dt
            self.pos[2] += fz * horiz * dt
            self.pos[1] += vert
        else:
            self.pos[0] += fx * self.speed * dt
            self.pos[1] += fy * self.speed * dt
            self.pos[2] += fz * self.speed * dt

        # --- ground / terrain check ---
        if self.pos[1] > 0.6:
            self.airborne = True

        if self.pos[1] <= 0.0:
            self.pos[1] = 0.0
            if self.airborne:
                self._check_landing()
        elif self.airborne:
            import world
            if world.check_mountain_collision(self.pos):
                self.crashed = True

    def _check_landing(self):
        import world
        x, z = self.pos[0], self.pos[2]
        on_runway = (
            abs(x) < world.RUNWAY_HALF_WIDTH
            and world.RUNWAY_Z0 < z < world.RUNWAY_Z1
        )
        gentle = (
            self.speed < LANDING_MAX_SPEED
            and abs(self.pitch) < LANDING_MAX_PITCH
            and abs(self.roll) < LANDING_MAX_ROLL
        )
        if on_runway and gentle:
            self.landed = True
            self.speed = 0.0
        else:
            self.crashed = True
