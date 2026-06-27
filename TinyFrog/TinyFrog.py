__version__ = "1.0"

import math
import thumby
import time

FPS = 60
LIVES = 4
TIME = 30

#region General
class Vector2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def copy(self):
        return Vector2(self.x, self.y)

class GameObject:
    def __init__(self, x, y, w, h):
        self.position = Vector2(x, y)
        self.width = w
        self.height = h
    def draw(self, world):
        self.sprite.x = self.position.x - world.camera.position.x
        self.sprite.y = self.position.y - world.camera.position.y
        thumby.display.drawSprite(self.sprite)
    def intersects(self, other, x=0, y=0) -> bool:
        return other.position.x + other.width - x > self.position.x and \
               other.position.x < self.position.x + self.width - x and \
               other.position.y + other.height - y > self.position.y and \
               other.position.y < self.position.y + self.height - y
    def update(self, world):
        pass

class MovingGameObject(GameObject):
    def __init__(self, x, y, w, h, vx):
        GameObject.__init__(self, x, y, w, h)
        self.velocity = Vector2(vx, 0)
    def update(self, world):
        self.position += self.velocity
        if self.velocity.x < 0 and self.position.x < -self.width:
            self.position.x = world.width
        elif self.velocity.x > 0 and self.position.x > world.width:
            self.position.x = -self.width
#endregion

#region Clock
class Counter:
    def __init__(self, n):
        self.n = n
        self.count = 0
    def update(self) -> bool:
        self.count += 1
        if self.count >= self.n:
            self.count = 0
            return True
        return False
    def reset(self):
        self.count = 0

class Timer:
    def __init__(self, milliseconds, function):
        self.milliseconds = milliseconds
        self.function = function
        self._start()
    def _start(self):
        self.started = time.ticks_ms()
        self.updated = self.started
        self.running = True
    def update(self):
        if not self.running:
            return
        self.updated = time.ticks_ms()
        if time.ticks_diff(self.updated, self.started) >= self.milliseconds:
            self.function()
            self.running = False
    def percent_complete(self) -> float:
        p = time.ticks_diff(self.updated, self.started) / self.milliseconds
        return min(p, 1)
    def seconds_remaining(self) -> int:
        ms = self.milliseconds - time.ticks_diff(self.updated, self.started)
        return ms // 1000
    def stop(self):
        self.running = False
#endregion

#region Terrain
class Median(GameObject):
    sprite = thumby.Sprite(16, 16,
        bytearray([2,1,2,2,1,1,2,2,3,4,2,1,1,2,2,2,128,128,128,128,128,64,64,128,64,64,128,64,64,64,64,64]))
    def __init__(self, x, y):
        GameObject.__init__(self, x, y, Median.sprite.width, Median.sprite.height)

class River(GameObject):
    def __init__(self, x, y, w, h):
        GameObject.__init__(self, x, y, w, h)
        self.floating = False
    def draw(self, world):
        pass
    def update(self, world):
        if self.intersects(world.frog):
            if not self.floating and not world.frog.is_jumping():
                world.frog.drown()
            self.floating = False
    def float(self):
        self.floating = True
#endregion

#region Vehicle
class Vehicle(MovingGameObject):
    def update(self, world):
        MovingGameObject.update(self, world)
        if self.intersects(world.frog, 4, 4):
            world.frog.kill()

class Car1(Vehicle):
    sprite = thumby.Sprite(16, 16,
        bytearray([128,192,236,236,252,236,236,224,224,224,238,238,254,238,206,64,1,3,55,55,63,55,55,7,7,7,119,119,127,119,115,2]))
    def __init__(self, x, y):
        Vehicle.__init__(self, x, y, Car1.sprite.width, Car1.sprite.height, -9.74 / FPS)

class Bulldozer(Vehicle):
    sprite = thumby.Sprite(16, 16,
        bytearray([0,204,252,236,236,236,252,236,224,240,16,16,252,252,84,0,0,51,63,55,55,55,63,55,7,15,8,8,63,63,42,0]))
    def __init__(self, x, y):
        Vehicle.__init__(self, x, y, Bulldozer.sprite.width, Bulldozer.sprite.height, 11.2 / FPS)

class Car2(Vehicle):
    sprite = thumby.Sprite(16, 16,
        bytearray([0,224,240,240,248,248,240,240,224,224,240,248,248,248,240,32,0,7,15,15,31,31,15,15,7,7,15,31,31,31,15,4]))
    def __init__(self, x, y):
        Vehicle.__init__(self, x, y, Car2.sprite.width, Car2.sprite.height, -14.9 / FPS)

class Car3(Vehicle):
    sprite = thumby.Sprite(16, 16,
        bytearray([64,110,238,254,238,110,224,224,224,236,236,252,236,236,192,128,2,119,119,127,119,119,7,7,7,55,55,63,55,55,3,1]))
    def __init__(self, x, y):
        Vehicle.__init__(self, x, y, Car3.sprite.width, Car3.sprite.height, 18.7 / FPS)

class Truck(Vehicle):
    sprite = thumby.Sprite(32, 16,
        bytearray([0,0,0,224,240,240,248,248,248,192,240,248,248,248,248,240,240,240,240,240,240,240,240,240,240,240,248,248,248,240,0,0,0,0,0,7,15,15,31,31,31,3,15,31,31,31,15,15,15,15,15,15,15,15,15,15,15,15,31,31,31,15,0,0]))
    def __init__(self, x, y):
        Vehicle.__init__(self, x, y, Truck.sprite.width, Truck.sprite.height, -28.0 / FPS)
#endregion

class Turtles(MovingGameObject):
    sprite = thumby.Sprite(16, 16,
        bytearray([0,0,128,160,112,32,32,32,32,32,112,160,0,0,0,0,0,1,2,10,28,8,8,8,8,8,28,10,1,1,0,0]) +
        bytearray([0,128,144,152,112,32,32,32,32,32,112,152,16,0,128,0,1,2,18,50,28,8,8,8,8,8,28,51,17,1,0,0]) +
        bytearray([0,128,128,128,112,8,16,32,32,32,112,152,16,0,0,0,1,2,2,2,28,32,16,8,8,8,28,50,17,1,2,0]) +
        bytearray([0,0,0,16,136,64,32,32,32,32,64,144,32,0,0,0,0,0,0,8,17,2,4,4,4,4,2,17,8,0,0,0]) +
        bytearray([0,128,0,0,64,32,128,132,132,32,64,0,0,0,128,0,0,1,0,0,4,9,2,66,66,9,4,0,0,0,1,0]) +
        bytearray([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]))
    def __init__(self, x, y, n, dives=False):
        MovingGameObject.__init__(self, x, y, n * Turtles.sprite.width, Turtles.sprite.height, -28.0 / FPS)
        self.n = n
        self.dives = dives
        self.frames = [ 0, 1, 2 ]
        if dives:
            self.frames += [ 3 ]
            if n < 3: self.frames += [ 3, 4, 4, 5, 4, 4, 3 ]
            else: self.frames += [ 4, 5, 4 ]
            self.frames += [ 3, 2, 1 ]
        def cycle(iterable):
            while True:
                for i in iterable:
                    yield(i)
        self.frame_iter = cycle(self.frames)
        self.frame = next(self.frame_iter)
        self.counter = Counter(FPS // 5)
    def draw(self, world):
        Turtles.sprite.setFrame(self.frame)
        Turtles.sprite.x = self.position.x - world.camera.position.x
        Turtles.sprite.y = self.position.y - world.camera.position.y
        for _ in range(self.n):
            thumby.display.drawSprite(Turtles.sprite)
            Turtles.sprite.x += Turtles.sprite.width
    def update(self, world):
        MovingGameObject.update(self, world)
        if self.counter.update():
            self.frame = next(self.frame_iter)
        if self.intersects(world.frog, x=8):
            world.frog.move(self.velocity)
            if self.frame != 5:
                world.river.float()

class Log(MovingGameObject):
    sprite = thumby.Sprite(16, 16,
        bytearray([0,0,0,192,48,16,8,8,8,8,8,8,8,16,8,8,0,0,0,3,4,20,24,16,24,24,24,8,28,24,28,28]) +
        bytearray([8,8,16,8,8,8,8,8,8,8,8,8,16,8,8,8,28,28,28,12,28,28,28,28,28,24,24,8,24,24,24,28]) +
        bytearray([8,8,16,8,8,8,8,8,8,8,8,48,192,0,0,0,28,28,28,28,12,28,28,28,16,16,16,12,3,0,0,0]))
    def __init__(self, x, y, vx, scale=1):
        MovingGameObject.__init__(self, x, y, (2 + scale) * Log.sprite.width, Log.sprite.height, vx)
        self.scale = scale
    def draw(self, world):
        Log.sprite.setFrame(0)
        Log.sprite.x = self.position.x - world.camera.position.x
        Log.sprite.y = self.position.y - world.camera.position.y
        thumby.display.drawSprite(Log.sprite)
        Log.sprite.setFrame(1)
        for _ in range(self.scale):
            Log.sprite.x += Log.sprite.width
            thumby.display.drawSprite(Log.sprite)
        Log.sprite.setFrame(2)
        Log.sprite.x += Log.sprite.width
        thumby.display.drawSprite(Log.sprite)
    def update(self, world):
        MovingGameObject.update(self, world)
        if self.intersects(world.frog, x=8):
            world.frog.move(self.velocity)
            world.river.float()

class Home(GameObject):
    width = 8 + 32 + 8
    height = 24
    sprite_home = thumby.Sprite(32, 24,
        bytearray([81,4,16,50,22,132,64,33,64,36,76,69,32,66,38,66,64,36,76,69,32,66,38,66,32,68,140,5,16,50,20,65,130,22,50,16,0,90,165,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,165,90,0,2,38,100,32,72,66,70,98,16,59,20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,18,45,64,34,70,34,40]))
    sprite_bush = thumby.Sprite(8, 24,
        bytearray([1,72,24,8,64,194,64,17,1,72,24,8,64,194,64,17,64,36,76,69,32,66,38,66]))
    sprite_frog = thumby.Sprite(16, 16,
        bytearray([128,192,134,9,233,254,220,188,188,220,254,233,9,134,192,128,7,159,223,255,124,241,45,45,45,33,241,124,255,223,159,7]))
    def __init__(self, x, y):
        GameObject.__init__(self, x, y, Home.width, Home.height)
        self.occupied = False
    def draw(self, world):
        Home.sprite_bush.x = self.position.x - world.camera.position.x
        Home.sprite_bush.y = self.position.y - world.camera.position.y
        thumby.display.drawSprite(Home.sprite_bush)
        Home.sprite_home.x = Home.sprite_bush.x + Home.sprite_bush.width
        Home.sprite_home.y = Home.sprite_bush.y
        thumby.display.drawSprite(Home.sprite_home)
        Home.sprite_bush.x = Home.sprite_home.x + Home.sprite_home.width
        thumby.display.drawSprite(Home.sprite_bush)
        if self.occupied:
            Home.sprite_frog.x = Home.sprite_home.x + Home.sprite_bush.width
            Home.sprite_frog.y = Home.sprite_home.y + Home.sprite_home.height - Home.sprite_frog.height
            thumby.display.drawSprite(Home.sprite_frog)
    def update(self, world):
        if self.intersects(world.frog, y=8):
            if self.occupied or not self.intersects(world.frog, x=16):
                world.frog.kill()
                return
            self.occupied = True
            world.score += 50 + world.frog.timer.seconds_remaining() * 10
            world.frog.reset(1000)

class Frog(GameObject):
    class State:
        ALIVE = 0
        DYING = 1
        DROWNING = 2
        HIDDEN = 3
    sprite = thumby.Sprite(16, 16,
        bytearray([0,0,16,120,64,240,248,248,248,248,240,64,120,16,0,0,0,0,4,15,1,3,7,7,7,7,3,1,15,4,0,0]) +
        bytearray([0,0,8,60,64,240,248,248,248,248,240,64,60,8,0,0,0,0,32,120,12,7,7,7,7,7,7,12,120,32,0,0]) +
        bytearray([0,0,0,200,236,232,248,224,248,232,204,8,0,0,0,0,0,0,0,19,55,23,31,7,31,23,51,16,0,0,0,0]) +
        bytearray([0,0,8,204,232,232,240,224,224,224,240,24,8,12,8,0,0,0,16,51,23,23,15,7,7,7,15,24,16,48,16,0]) +
        bytearray([0,0,32,240,128,192,224,224,224,224,192,128,240,32,0,0,0,0,8,30,2,15,31,31,31,31,15,2,30,8,0,0]) +
        bytearray([0,0,4,30,48,224,224,224,224,224,224,48,30,4,0,0,0,0,16,60,2,15,31,31,31,31,15,2,60,16,0,0]) +
        bytearray([0,0,0,0,8,204,232,248,224,248,232,236,200,0,0,0,0,0,0,0,16,51,23,31,7,31,23,55,19,0,0,0]) +
        bytearray([0,8,12,8,24,240,224,224,224,240,232,232,204,8,0,0,0,16,48,16,24,15,7,7,7,15,23,23,51,16,0,0]) +
        bytearray([0,0,8,220,254,204,200,248,248,200,204,254,220,8,0,0,0,0,0,16,59,127,63,31,31,31,63,127,59,16,0,0]) +
        bytearray([0,12,238,254,204,236,254,254,254,254,236,204,254,238,12,0,0,24,27,63,63,31,31,31,31,31,31,63,63,27,24,0]) +
        bytearray([12,198,255,31,61,254,254,254,254,254,254,61,31,255,198,12,0,51,255,255,191,127,127,127,127,127,127,191,255,255,51,48]) +
        bytearray([0,0,64,16,136,224,228,240,240,228,224,136,16,64,0,0,0,0,2,8,17,7,39,15,15,39,7,17,8,2,0,0]) +
        bytearray([0,128,40,4,128,162,192,242,242,192,162,128,4,40,128,0,0,1,20,32,1,69,3,79,79,3,69,1,32,20,1,0]) +
        bytearray([64,0,4,0,64,0,17,128,128,17,0,64,0,4,0,64,2,0,32,0,2,0,136,1,1,136,0,2,0,32,0,2]) +
        bytearray([0,48,48,64,156,22,59,127,127,127,59,22,156,64,48,48,0,0,0,0,192,193,34,20,8,20,34,193,192,0,0,0]), key=0)
    def __init__(self, x, y):
        GameObject.__init__(self, x, y, Frog.sprite.width, Frog.sprite.height)
        self.default_position = Vector2(x, y)
        self.velocity = Vector2()
        self.offset = 0
        self.state = Frog.State.ALIVE
        self.lives = LIVES
        self.counter = Counter(FPS // 6)
        self.timer = Timer(TIME * 1000, self.kill)
        self.steps = 0
        self.unit = 60 / FPS
    def _jump(self) -> bool:
        if self.state != Frog.State.ALIVE or self.is_jumping():
            return False
        self.offset = self.height
        return True
    def _kill(self) -> bool:
        if self.state != Frog.State.ALIVE:
            return False
        self.offset = 0
        self.timer.stop()
        return True
    def _sound_drowning(self):
        n = self.offset
        if n > 32:
            return
        start = [ 0, 0, 1000, 0, 0, 0, 0, 2000, 0, 0, 0, 0, 0, 0, 0, 0 ]
        freq = 250 + 250 / 2 * (1 + math.cos(math.pi * n / 8)) if n >= len(start) else start[int(n)]
        if freq < 20:
            return
        thumby.audio.play(int(freq), 50)
    def _sound_dying(self):
        n = 32 - self.offset
        if n < 0:
            return
        freq = 1800 - 1600 / 32 * math.sqrt(32 ** 2 - n ** 2)
        thumby.audio.play(int(freq), 100)
    def _sound_jumping(self):
        n = self.height - self.offset
        freq = 500 + n * 100
        if n % 2:
            freq /= 2
        thumby.audio.play(int(freq), 100)
    def draw(self, world):
        if self.state != Frog.State.HIDDEN:
            GameObject.draw(self, world)
    def update(self, world):
        self.timer.update()
        if self.state == Frog.State.ALIVE:
            if self.is_jumping():
                self._sound_jumping()
                self.position += self.velocity
                self.offset -= self.unit
                if self.offset <= 0:
                    Frog.sprite.setFrame(Frog.sprite.getFrame() - 1)
                    steps = (self.default_position.y - self.position.y) // self.height
                    if steps > self.steps:
                        self.steps = steps
                        world.score += 10
            if self.position.x < 0 or self.position.x > world.width - self.width:
                self.kill()
        elif self.state == Frog.State.DYING or self.state == Frog.State.DROWNING:
            self._sound_dying() if self.state == Frog.State.DYING else self._sound_drowning()
            self.offset += self.unit
            if self.counter.update():
                frame = Frog.sprite.getFrame()
                if frame < 14:
                    Frog.sprite.setFrame(14 if frame == 10 else frame + 1)
                else:
                    self.lives -= 1
                    self.reset()
    def drown(self):
        if self._kill():
            self.state = Frog.State.DROWNING
            Frog.sprite.setFrame(11)
    def is_jumping(self) -> bool:
        return self.offset > 0
    def jump_down(self, world):
        if self.position.y >= world.height - self.height:
            return
        if self._jump():
            Frog.sprite.setFrame(5)
            self.velocity = Vector2(0, self.unit)
    def jump_left(self, world):
        if self.position.x <= 0:
            return
        if self._jump():
            Frog.sprite.setFrame(3)
            self.velocity = Vector2(-self.unit, 0)
    def jump_right(self, world):
        if self.position.x >= world.width - self.width:
            return
        if self._jump():
            Frog.sprite.setFrame(7)
            self.velocity = Vector2(self.unit, 0)
    def jump_up(self, world):
        if self.position.y <= 0:
            return
        if self._jump():
            Frog.sprite.setFrame(1)
            self.velocity = Vector2(0, -self.unit)
    def kill(self):
        if self._kill():
            self.state = Frog.State.DYING
            Frog.sprite.setFrame(8)
    def move(self, velocity):
        if self.state != Frog.State.ALIVE or self.is_jumping() and self.velocity.x == 0:
            return
        self.position += velocity
    def reset(self, delay_ms = 0):
        if delay_ms > 0:
            self.state = Frog.State.HIDDEN
            self.timer = Timer(delay_ms, self.reset)
            return
        Frog.sprite.setFrame(0)
        self.position = self.default_position.copy()
        self.offset = 0
        if self.state == Frog.State.ALIVE:
            self.steps = 0
        else:
            self.state = Frog.State.ALIVE
        self.counter.reset()
        self.timer = Timer(TIME * 1000, self.kill)

class Camera(GameObject):
    width = thumby.display.width
    height = thumby.display.height
    def __init__(self, frog):
        GameObject.__init__(self, 0, 0, Camera.width, Camera.height)
        self._focus(frog)
    def _focus(self, frog):
        self.position.x = frog.position.x - (self.width - frog.width) // 2
        self.position.y = frog.position.y - (self.height - frog.height - 4)
    def update(self, world):
        self._focus(world.frog)
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > world.width - self.width:
            self.position.x = world.width - self.width
        if self.position.y < 0:
            self.position.y = 0

class HUD:
    width = thumby.display.width
    height = thumby.display.height
    def _lives(world):
        for i in range(world.frog.lives - 1):
            thumby.display.setPixel(i * 2, HUD.height - 1, 1)
    def _score(world):
        thumby.display.drawText(str(world.score), 0, 0, 1)
    def _time(world):
        timer_x = (LIVES - 1) * 2
        timer_width = HUD.width - timer_x
        if world.frog.state != Frog.State.HIDDEN:
            timer_width = int((1 - world.frog.timer.percent_complete()) * timer_width)
        if timer_width >= 1:
            thumby.display.drawLine(HUD.width - timer_width, HUD.height - 1, HUD.width - 1, HUD.height - 1, 1)
    def draw(world, score=False):
        thumby.display.drawLine(0, HUD.height - 1, HUD.width - 1, HUD.height - 1, 0)
        HUD._lives(world)
        HUD._time(world)
        if score:
            HUD._score(world)

class World:
    width = 224
    height = 216
    def __init__(self):
        self.score = 0
        self.river = River(0, World.height - 12 * 16, World.width, 5 * 16)
        self.objects = []
        self.frog = Frog(World.width // 2, World.height - 16)
        self.camera = Camera(self.frog)
        for i in range(0, World.width, 16):
            self.objects.append(Median(i, World.height - 16))
        for i in range(3):
            self.objects.append(Car1(5 * 16 + i * 4.5 * 16, World.height - 2 * 16))
        for i in range(3):
            self.objects.append(Bulldozer(6 * 16 + i * 4 * 16, World.height - 3 * 16))
        for i in range(3):
            self.objects.append(Car2(6 * 16 + i * 4 * 16, World.height - 4 * 16))
        self.objects.append(Car3(World.width, World.height - 5 * 16))
        for i in range(2):
            self.objects.append(Truck(7 * 16 + i * 6 * 16, World.height - 6 * 16))
        for i in range(0, World.width, 16):
            self.objects.append(Median(i, World.height - 7 * 16))
        for i in range(4):
            self.objects.append(Turtles(i * 4 * 16, World.height - 8 * 16, 3, i == 0))
        for i in range(3):
            self.objects.append(Log(2 * 16 + i * 5 * 16, World.height - 9 * 16, 9.74 / FPS))
        for i in range(2):
            self.objects.append(Log(2 * 16 + i * 8 * 16, World.height - 10 * 16, 74.7 / FPS, 4))
        for i in range(3):
            self.objects.append(Log(i * 6 * 16, World.height - 11 * 16, 18.7 / FPS, 2))
        for i in range(4):
            self.objects.append(Turtles(2 * 16 + i * 4 * 16, World.height - 12 * 16, 2, i == 0))
        self.homes = []
        for i in range(5):
            home = Home(i * Home.width - 8, World.height - 13.5 * 16)
            self.homes.append(home)
            self.objects.append(home)
    def draw(self):
        for o in self.objects:
            if self.camera.intersects(o):
                o.draw(self)
        self.frog.draw(self)
        HUD.draw(self)
    def update(self):
        self.river.update(self)
        for o in self.objects:
            o.update(self)
        self.frog.update(self)
        self.camera.update(self)
    def active(self) -> bool:
        return self.frog.lives > 0 and (\
               any(not home.occupied for home in self.homes) or \
               self.frog.state == Frog.State.HIDDEN)

class Screen:
    width = thumby.display.width
    height = thumby.display.height
    def _measure_width(string, width=5, space=1):
        n = len(string)
        return n * width + (n - 1) * space
    def _measure_x(string, width=5, space=1):
        return (Screen.width - Screen._measure_width(string, width, space)) // 2
    def _measure_y(height):
        return (Screen.height - height) // 2
    def title():
        thumby.display.fill(0)
        s = "FROG"
        thumby.display.setFont("/lib/font8x8.bin", 8, 8, 2)
        x = Screen._measure_x(s, 8, 2)
        y = Screen._measure_y(8)
        thumby.display.drawText(s, x, y, 1)
        s = "TINY"
        thumby.display.setFont("/lib/font3x5.bin", 3, 5, 2)
        thumby.display.drawText(s, x, y - 7, 1)
        s = "Start"
        x = Screen._measure_x(s, 5) + 1
        y = Screen.height - 7 - 3
        width = Screen._measure_width(s)
        thumby.display.setFont("/lib/font5x7.bin", 5, 7, 1)
        thumby.display.drawText(s, x, y, 1)
        thumby.display.update()
        counter = Counter(FPS // 2)
        arrows = False
        while not thumby.actionJustPressed():
            if counter.update():
                arrows = not arrows
                thumby.display.blit(bytearray([62,28,8] if arrows else [0,0,0]), x - 4, y, 3, 7, -1, 0, 0)
                thumby.display.blit(bytearray([8,28,62] if arrows else [0,0,0]), x + width + 1, y, 3, 7, -1, 0, 0)
            thumby.display.update()
        thumby.buttonD.justPressed()
        thumby.buttonL.justPressed()
        thumby.buttonR.justPressed()
        thumby.buttonU.justPressed()
    def game(world):
        frog = world.frog
        while world.active():
            thumby.display.fill(0)
            world.draw()
            thumby.display.update()
            if thumby.buttonA.justPressed():
                frog.jump_up(world)
            elif thumby.buttonB.justPressed():
                frog.jump_down(world)
            elif thumby.buttonD.justPressed():
                frog.jump_down(world)
            elif thumby.buttonL.justPressed():
                frog.jump_left(world)
            elif thumby.buttonR.justPressed():
                frog.jump_right(world)
            elif thumby.buttonU.justPressed():
                frog.jump_up(world)
            world.update()
    def score(score, high_score):
        thumby.display.fill(0)
        s = "HI-SCORE"
        thumby.display.drawText(s, Screen._measure_x(s), 0, 1)
        s = str(high_score)
        thumby.display.drawText(s, Screen._measure_x(s), 10, 1)
        s = "SCORE"
        thumby.display.drawText(s, Screen._measure_x(s), 23, 1)
        s = str(score)
        thumby.display.drawText(s, Screen._measure_x(s), 33, 1)
        thumby.display.update()
        while not thumby.actionJustPressed():
            pass

thumby.display.setFPS(FPS)
thumby.saveData.setName("TinyFrog")
high_score = 0
if thumby.saveData.hasItem("high_score"):
    high_score = thumby.saveData.getItem("high_score")
while True:
    Screen.title()
    world = World()
    Screen.game(world)
    if all(home.occupied for home in world.homes):
        world.score += 1000
    if world.score > high_score:
        high_score = world.score
        thumby.saveData.setItem("high_score", high_score)
        thumby.saveData.save()
    Screen.score(world.score, high_score)
