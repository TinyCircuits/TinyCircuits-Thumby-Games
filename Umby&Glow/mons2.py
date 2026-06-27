_MegaBones = const(83)
_ChargingBones = const(6)
_BonesBoss = const(3)
_DragonBones = const(4)
_Wyvern = const(5)
_Skittle = const(10)
_Prober = const(32)

@micropython.viper
def _tick_mega_bones(self, t: int, i: int):
    data = ptr32(self.data)
    tape = self._tp
    spawn = self.add
    p = tape.player
    x = ptr32(self.x)[i]+30
    if int(p.x) > x + 30:
        p.die(p.name + " was mind-flayed!")
    # Sync monster damage
    ii = i*5
    dmg = data[ii]
    odmg = int(self.omons.bsync)
    if odmg > dmg:
        dmg = data[ii] = odmg
    self.bsync = dmg <<1|1
    if data[ii+1] != dmg and dmg <= 50:
        data[ii+1] = dmg
        spawn(_ChargingBones, x, 32)
        if dmg == 10 or dmg == 40:
            spawn(_BonesBoss, x, 32)
        if dmg == 20 or dmg == 30:
            spawn(_DragonBones, x, 32)
        if dmg%7==0:
            spawn(_Wyvern, x, 32)
        if dmg%13==0:
            spawn(_Prober, x, 32)
    if t%240==0:
        spawn(_Skittle, x+80, 32)
    # Death with ensured sync
    if dmg >= 50:
        data[ii+2] += 1
        if data[ii+2] > 60:
            self._kill(t, i, None, "_REST_IN_DEFEAT!_")
            for mi in range(int(len(self._tids))):
                self._tids[mi] = 0
                

mons.ticks = {_MegaBones: _tick_mega_bones}