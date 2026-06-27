class W:
    @micropython.viper
    def pattern_alien_decay(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = 0-(int(ihash(x//30))%50)
        v = 0
        for y in range(oY, oY+32):
            y1 = y-20 if y>32 else 44-y
            v |= (
                int(y1 > (32423421^(x*x*(y1-buff[0])))%64) if y1 > buff[0] else 0
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_biomechanical_hall_wall(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = int(shash(x,32,48))
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(y > (11313321^(x*(y+buff[0]))) % 64 + 5)
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_biomechanical_lab_wall(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        v = 0
        if oY == 0:
            buff[0] = x-50+int(shash(x,100,120))
            buff[1] = int(shash(x,32,48))
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(y > (11313321^(buff[0]*(y+buff[1]))) % 64 + 5)
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_bimechanical_mainframe(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        x8 = x//10
        v = f = 0
        for y in range(oY, oY+32):
            blk = (((y+2)//5)+3)%13<7
            v |= ( 1 if blk else 0 ) << (y-oY)
            f |= ( 0 if blk and (x+1)%10>1 and (y+3)%5>1 else 1 ) << (y-oY)
        buff[4 if oY==0 else 5] = int(self.pattern_alien_decay(x, oY)) | f
        return v

    @micropython.viper
    def pattern_biomechanical_lab(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        snco = ptr8(sinco)
        x8 = x//10
        v = f = 0
        for y in range(oY, oY+32):
            y4 = (y+2)//5
            blk = snco[((x8*x8)^((y4+100)*(y4+100)))%400] < 10 or (y4+1)%13<2
            v |= ( 1 if blk else 0 ) << (y-oY)
            f |= ( 0 if blk and (x+1)%10>1 and (y+3)%5>1 else 1 ) << (y-oY)
        buff[4 if oY==0 else 5] = int(self.pattern_alien_decay(x, oY)) | f
        return v
    @micropython.viper

    def pattern_biomechanical_fill(self, x: int, oY: int) -> int:
        return ptr32(_buf)[4 if oY==0 else 5]

    @micropython.viper
    def pattern_slim_room(self, x: int, oY: int) -> int:
        return int(-2147483648) if oY else 1

    @micropython.viper
    def pattern_cathedral(self, x: int, oY: int) -> int:
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(y > (32423421^(y-x*y)) % 64)
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_cable(self, x: int, oY: int) -> int:
        rh = int(shash(x,60,80))-8
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(rh-4 <= y <= rh+4)
            ) << (y-oY)
        return v

    @micropython.viper
    def pattern_cabling(self, x: int, oY: int) -> int:
        ptr32(_buf)[5 if oY else 4] = v = int(self.pattern_cable(x, oY)) | \
            int(self.pattern_cable(x+3333, oY)) | \
            int(self.pattern_cable(x+6666, oY))
        return v

    @micropython.viper
    def pattern_cabled_room(self, x: int, oY: int) -> int:
        v = int(self.pattern_cabling(x, oY))
        return v | (-16777216 if oY else 255)

    @micropython.viper
    def pattern_cabling_fill(self, x: int, oY: int) -> int:
        v = ptr32(_buf)[5 if oY else 4]
        return -1^(v&(v<<4)&(v>>1)) | int(self.pattern_alien_decay(x, oY+x%30))

    @micropython.viper
    def pattern_alien_totem_plants(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = int(shash(x,128,40)) + int(shash(x,16,16)) + int(shash(x,4,4)) - 16
        v = 0
        for y in range(oY, oY+32):
            y1 = y-20 if y>32 else 44-y
            v |= (
                int(y1 > (32423421^(x*x*(y1-buff[0])))%64) if y1 > buff[0] else 0
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_alien_totem_floor(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = int(shash(x,128,10)) + int(shash(x,16,8)) + int(shash(x,4,4)) + 40
        v = 0
        for y in range(oY, oY+32):
            y1 = y if y>32 else 64-y
            v |= (
                int(y1 > (32423421^(x*x*(y1-buff[0])))%64) if y1 > buff[0] else 0
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_undertank(self, x: int, oY: int) -> int:
        if x%70<7: return -1
        self.pattern_alien_totem_floor(x, oY)
        if oY: return int(self.pattern_alien_totem_floor(x, oY))
        return 67108863

    def pattern_bio_pillars(self, x: int, oY: int) -> int:
        if x%20<5: return -1
        return int(self.pattern_undertank(x, oY))

    @micropython.viper
    def pattern_vents(self, x: int, oY: int) -> int:
        return 503808511 if oY == 0 else -8265608

    @micropython.viper
    def pattern_flood(self, x: int, oY: int) -> int:
        return (15 if oY == 0 else -268435456
            ) if x//8%2 else (255 if oY == 0 else -16777216)

    @micropython.viper
    def pattern_alien_vent_decay(self, x: int, oY: int) -> int:
        return int(self.pattern_alien_decay(x, oY)) | -1^(201523455 if oY == 0 else -16728016)

    @micropython.viper
    def pattern_quilted_diodes(self, x: int, oY: int) -> int:
        snco = ptr32(int(ptr32(sinco))+4)
        v = 0
        for y in range(oY, oY+32):
            p1 = -1 if snco[(x^y)%90]<128 else 0
            p2 = -1 if snco[(x*2^y*2)%90]<128 else 0
            p3 = -1 if snco[(x*4^y*4)%90]<128 else 0
            p4 = -1 if snco[(x*8^y*8)%90]<128 else 0
            v |= (
               0 if (p1^p2^p3^p4) else 1
            ) << (y-oY)
        return v
w = W()