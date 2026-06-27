class W:
    @micropython.viper
    def pattern_cave(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = int(shash(x,32,48)) + int(shash(x,16,24)) + int(shash(x,4,16))
            buff[1] = int(abs(int(shash(x,8,32)) - (buff[0] >> 2)))
            buff[2] = int(x % (buff[0]>>3) == 0)
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(y > buff[0]) | int(y < buff[1]) | int(y <= 5)
             ) << (y-oY)
        return v
    @micropython.viper
    def pattern_cave_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        v = 0
        for y in range(oY, oY+32):
            v |= (
                ((int(y < (buff[0]>>1)*3) | buff[2]) # ground fill
                # ceiling fill
                & (int(y > 10-buff[1]) | int(y > 5) | int(y == 5) | buff[1]%(y+1)))
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_stalagmites(self, x: int, oY: int) -> int:
        buff = ptr32(_buf) # [ceiling-height, fill-shading-offset]
        if oY == 0:
            t1 = (x%256)-128
            t2 = (x%18)-9
            t3 = (x%4)-2
            buff[0] = 50 - (t1*t1>>8) - (t2*t2>>2) - t3*t3*4
            buff[1] = 15*(x%4)
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(y < buff[0]) | int(y > 64 - buff[0])
            ) << (y-oY)
        return v
    @micropython.viper
    def pattern_stalagmites_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(y+20 > buff[0]) & int(y-buff[1] < 64 - buff[0])
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_toplit_wall(self, x: int, oY: int) -> int:
        v = 0
        p = x-500
        for y in range(oY, oY+32):
            v |= (
                1 if (p*p)%(y+1) == 0 else 0
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_tunnel(self, x: int, oY: int) -> int:
        buff = ptr32(_buf) # [ground-height]
        if oY == 0:
            buff[0] = 10 + int(shash(x,32,24))+int(shash(x,24,8))+int(shash(x,7,2))
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(y > buff[0]) | int(y < buff[0]-10)
             ) << (y-oY)
        return v
w = W()