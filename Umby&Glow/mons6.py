_CPU = const(80)
_Flood = const(96)

@micropython.viper
def pattern_flood(x: int, oY: int) -> int:
    return 15 if oY == 0 else -268435456

@micropython.viper
def _tick_cpu(self, t: int, i: int):
    xs = ptr32(self.x)
    data = ptr32(self.data)
    tape = self._tp
    ii = i*5
    dmg = data[ii]
    odmg = int(self.omons.bsync)-50
    if 0 <= odmg <= 15 and odmg > dmg:
        dmg = data[ii] = odmg
    if data[ii+1] != dmg:
        say = self.reactions.extend
        data[ii+1] = dmg
        self.bsync = (dmg+50) <<1|1
        if dmg%7==1:
            say(["|!! CORE ALERT !! INTEGRITY:"+str(16-dmg)])
        if dmg == 2:
            say(["@: Nice! It's taking damage!"])
        elif dmg == 5:
            say(["@: Keep going!"])
        elif dmg == 9:
            say(["^: This is an absolute blast!"])
        elif dmg == 13:
            tape.cam_shake = 1 <<1|1
        elif dmg == 14:
            say(["@: Just a bit more!"])
            tape.cam_shake = 3 <<1|1
        elif dmg == 15:
            tape.cam_shake = 6 <<1|1
        p1 = tape.players[0]
        pr1 = int(p1.rocket_x) + int(p1.rocket_y) + 1
        tape.blast(t+i,(t^pr1)%72+int(tape.x[0]), (t*pr1)%64)
    if dmg >= 16:
        data[ii+2] += 1
        if data[ii+2] > 60:
            tape.cam_shake = 0 <<1|1
            self._kill(t, i, None, "SEG-FAULT")

def _tick_flood(self, t: int, i: int):
    self._tp.redraw_tape(1, t*10+t//10%300, pattern_fill, pattern_fill)
    self._tp.redraw_tape(2, t*10+t//10%300, self.ticks[9991], None)
    self.data[i*5] += 1
    if self.data[i*5] > 600:
        self._tids[i] = 0

mons.ticks = {_CPU: _tick_cpu, _Flood: _tick_flood, 9991: pattern_flood}