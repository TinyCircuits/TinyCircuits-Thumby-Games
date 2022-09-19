_Lazer = const(12)
_EFalcon = const(31)

@micropython.viper
def _tick_e_falcon(self, t: int, i: int):
    xs = ptr32(self.x); ys = ptr8(self.y)
    x = xs[i]
    yy = ys[i]-60
    tpx = int(self._tp.x[0])
    ti = t+i*77
    if ti%300==10: # Dual lazers
        self.add(_Lazer, x, ys[i]-68)
        self.add(_Lazer, x, ys[i]-60)
    if ti%300<30:
        return
    x += ti//120*77%32 - 16
    # Shift right/left into firing range
    if x < tpx+50+(i*6)%16 and ti%120>60 and ti%3==0:
        xs[i] += 1
    elif x > tpx+56+(i*6)%16:
        xs[i] -= 1
    if ti%5==0: # Up/Down
        ys[i] = 60 + (yy + (1 if (x+ti%600//300)%2 else -1))%72

mons.ticks = {_EFalcon: _tick_e_falcon}