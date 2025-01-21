_Lung = const(81)
_Hold = const(99)

def _tick_lung(self, t, i):
    x = self.x[i]
    tape = self._tp
    if tape.player.x > x+300:
        self._tids[i] = 0
    if tape.player.x > x-17:
        self.bsync = 1
    data = self.data
    if data[i*5]: return
    self.y[i] = 105
    if self.bsync or self.omons.bsync:
        for j, m in enumerate(self._tids):
            if m == _Hold:
                self._kill(t, j, None, None)
                data[i*5] = 1

mons.ticks = {_Lung: _tick_lung}