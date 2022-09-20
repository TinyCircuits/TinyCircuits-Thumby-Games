_Bones = const(1)
_BackBones = const(2)
_ChargingBones = const(6)
_Molaar = const(21)
_LeftDoor = const(30)

@micropython.viper
def pattern_door(x: int, oY: int) -> int:
    return -1 if oY else 33554431

@micropython.viper
def pattern_windows(x: int, oY: int) -> int:
    we = (12 if 10 < x%24 < 14 else 5 if 9 < x%24 < 15 else
        3 if 8 < x%24 < 16 else 2 if 7 < x%24 < 17 else
        1 if 5 < x%24 < 19 else 0) # edges
    v = 0
    for y in range(oY, oY+32):
        v |= (
            1 if y < 10+we else 1 if y > 30-we else 0
        ) << (y-oY)
    return v

@micropython.viper
def pattern_inside(x: int, oY: int) -> int:
    return -128 if oY else 7 # High roof and floor

def _left_door_events(self, timer, p1, p1x, p2, p2x, ii, x):
    tape = self._tp
    camshk = -1
    data = self.data
    say = self.reactions.extend
    # Handle countdown finishing
    if timer == 1300:
        if p1x < x or (p2.coop and p2x < x):
            # One of the players failed failed to board
            name = p1.name if p1x < x else p2.name
            msg = name + " failed to board!"
            p1.die(msg, (x-600)*256)
            data[ii] = -9
        else:
            # Players boarded!
            tape.feed = [pattern_none,pattern_fill,pattern_fill,
                pattern_fill,pattern_fill]
            tape.spawner = (bytearray([]), bytearray([]))
            tape.clear_overlay()
            msg = "Ready to Launch!"
            tape.message(0, msg + " \n \n \n \n \n " + msg, 3)
            # Shut the rocket doors
            rdrtp = tape.redraw_tape
            for xi in range(x-80, x):
                rdrtp(2, xi, pattern_fill, pattern_fill)
            for xi in range(x+80, x+160):
                rdrtp(2, xi, pattern_fill, pattern_fill)
            for xi in range(0, 216):
                rdrtp(0, xi, pattern_none, None)
            # Set repawn point to be within rocket
            p1.respawn_loc = x + 40
    # Handle launch stage 1 (cam shaking)
    elif timer == 1400:
        tape.clear_overlay()
        camshk = 3
    elif timer == 1450:
        say(["^: WOAAAH!!", "@: HERE WE GOOOOOO!!",
            "@: Brace yourself, Glow!",
            "^: I'm stuck good to this beam.",
            "^: Brace yourself too, Umby!",
            "@: The G-Force is only increasing. I'm well planted!"])
        # Release background monsters
        for xi in range(20):
            self.add(_BackBones, x+xi*4, 10)
        data[ii+2] = 1 # Start lifting off

    # Lift off acceleration sequence
    elif timer == 1800:
        data[ii+2] = 1
    elif timer == 1900:
        data[ii+1] = 1
    elif timer == 2000:
        data[ii+1] = 2
    elif timer == 2100:
        data[ii+1] = 3
    elif timer == 2200:
        data[ii+1] = 4
    elif timer == 2300:
        data[ii+1] = 5
        say(["^: Monsters!", "@: They're getting in!",
            "^: Let's fight!"])
    elif timer == 2400:
        data[ii+1] = 6
    elif timer == 2600:
        data[ii+1] = 7
    elif timer == 2800:
        data[ii+2] = 2
        camshk = 2
    elif timer == 3000:
        data[ii+2] = 3
        camshk = 1
    elif timer == 3200:
        data[ii+2] = 4
        camshk = 0

    elif timer == 6000:
        say(["@: This ship is taking a beating!",
            "^: It's not going to take much more!"])

    # Reach orbit
    elif timer == 8800:
        data[ii+2] = 3
        say(["@: Looks like we are easing into orbit",
            "^: Finally!"])
    elif timer == 9000:
        data[ii+2] = 2
    elif timer == 9200:
        data[ii+2] = 1
    elif timer == 9400:
        data[ii+1] = 6
    elif timer == 9500:
        data[ii+1] = 5
    elif timer == 9600:
        data[ii+1] = 4
        p1.space = p2.space = 1
        say(["^: Woah!", "@: Low Gravity!", "^: Cool!"])
    elif timer == 9700:
        data[ii+1] = 3
    elif timer == 9800:
        data[ii+1] = 2
    elif timer == 9900:
        data[ii+1] = 1
    elif timer == 10000:
        data[ii+2] = 0

    # Rocket explosions
    elif timer == 10200:
        camshk = 1
        say(["^: Umby?!", "@: Glow... WOW...",
            "^: I think this ship is coming apart!",
            "@: I think so too..."])
    elif timer == 10300:
        camshk = 2
    elif timer == 10400:
        camshk = 3
    elif timer == 10500:
        camshk = 4
        say(["^: What do we do?!", "@: I don't know!",
            "@: Hold on???", "^: I'm trying!"])
        tape.feed = [pattern_none,pattern_none,pattern_fill,
            pattern_none,pattern_fill]
    elif timer == 10600:
        camshk = 5
    elif timer == 10700:
        camshk = 7
        say(["^: AAAAAGGGH!", "@: AAAAAGGGH!"])
    elif timer == 11300:
        camshk = 0
        p1.respawn_loc = 0

    if camshk != -1:
        tape.cam_shake = camshk

@micropython.viper
def _tick_left_door(self, t: int, i: int):
    tape = self._tp
    rx = int(tape.x[0]) + 140
    mx = int(tape.midx[0]) + 140
    plyrs = tape.players
    tids = ptr8(self._tids)
    xs = ptr32(self.x)
    ys = ptr8(self.y)
    data = ptr32(self.data)
    ii = i*5
    x = xs[i]
    p1 = plyrs[0]; p2 = plyrs[1]
    p1x = int(p1.x)
    p2x = int(p2.x)
    timer = data[ii]
    alive = int(plyrs[0].mode) < 200

    # Start the countdown timer when both players close
    if timer < 0 and p1x > x-500 and p2x > x-500 and alive:
        data[ii] = 0
    # Update the countdown timer if player not respawning
    elif 100 <= timer < 1300 and (timer-100)%120 == 0 and alive:
        tape.clear_overlay()
        msg = "T-Minus " + str((1300-timer)//120)
        tape.message(0, msg + " \n \n \n \n \n " + msg, 3)
    else:
        self.ticks[999](self, timer, p1, p1x, p2, p2x, ii, x)

    # Increase the timer if active
    if timer >= 0:
        data[ii] += 1

    # Repair spaceship (until 12000)
    if timer < 9700:
        if timer < 1300:
            if rx > x-20:
                ptrn = (self.ticks[9991] if rx<x else
                    self.ticks[9993] if rx<x+80 else pattern_fill)
                tape.redraw_tape(2, rx, ptrn, pattern_fill)
            x1 = x-20-rx+mx
            if rx > x:
                tape.redraw_tape(1, x1, pattern_fill, pattern_fill)
            if mx-20 > x1:
                tape.redraw_tape(1, mx-20, pattern_fill, pattern_fill)
        else: # Spaceship repairs
            x1 = timer%20
            tape.redraw_tape(2, x-x1-1 if x1<10 else x+x1+70,
                pattern_fill, None)
            if int(p1.mode) > 200:
                tape.redraw_tape(2, x+timer%80, self.ticks[9993], None)
        # Keep redrawing the rocket ship windows when in flight
        if timer >= 1600:
            tape.redraw_tape(1, timer, self.ticks[9992], pattern_fill)

    # Keep background monsters in range and falling
    if timer%(8-data[ii+1])==0:
        for xi in range(48):
            if tids[xi] != _BackBones:
                continue
            if xs[xi] > x+88:
                xs[xi] = x+88
            elif xs[xi] < x-8:
                xs[xi] = x-8
            if ys[xi] > 104:
                ys[xi] = 74
            ys[xi] += data[ii+2]

    # Flying sequence monster spawning
    if 2300 < timer < 10000 and timer%280==0:
        # Random position from edge of screen
        p = (timer^p1x)%448
        x1 = p if p<160 else 0 if p<224 else p-224 if p<384 else 159
        y1 = 0 if p<160 else p-160 if p<224 else 63 if p<384 else p-384
        if x1 <= 35: # No monsters from left of screen
            return
        mon = _Molaar if 50<x1<140 else _Bones if x1<=50 else _ChargingBones
        self.add(mon, x+x1-40, y1+64)

    # Stop monsters hogging the respawn area or charging for too long
    xi = timer//2%48
    if tids[xi] == _ChargingBones:
        if xs[xi] == p1x or ys[xi] == int(p1.y):
            if int(p1.mode) > 200:
                if xs[xi] == p1x:
                    xs[xi] += 30 if xi%2 else -30
                else:
                    ys[xi] += 30 if xi//2%2 else -30
            tids[xi] = _Bones
            data[xi*5+4] = 2
    # Keep monsters in area
    if tids[xi] == _Bones:
        if xs[xi] > x+120:
            xs[xi] == x+120
        elif xs[xi] < x-20:
            xs[xi] == x-20

    # Ship breaking apart
    if 10600 < timer < 11300:
        if timer%5==0:
            play(rocket_bang, 40)
            tape.blast(timer//5,
                (timer^p1x)%216+int(self.x[i])-72, (timer*p1x)%64)
        # Clearing out background monsters
        if tids[timer%48] != _LeftDoor:
            tids[timer%48] = 0
            self.num = int(self.num) - 1 <<1|1
    elif timer == 11300:
        tids[i] = 0
        self.num = int(self.num) - 1 <<1|1

mons.ticks = {
    _LeftDoor: _tick_left_door,
    999: _left_door_events,
    9991: pattern_door,
    9992: pattern_windows,
    9993: pattern_inside,
}