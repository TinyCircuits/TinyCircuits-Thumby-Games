class W:
    @micropython.viper
    def pattern_cloudy_snowy_mountains(self, x: int, oY: int) -> int:
        buff = ptr32(_buf) # [ripple-modifier, snow-capping, cloud-height, cloud-level]
        xa = x*8
        if oY == 0:
            u = int(shash(xa,32,16))
            buff[0] = int(shash(xa,128,40))+u+int(shash(xa,4,4))
            buff[1] = u>>1
            # cloud parameters
            e = (x+10)%64-10
            e = 10+e if e < 0 else 10-e if e<10 else 0
            buff[2] = (int(shash(x,16,32)) + int(shash(x,8,16))-20-e*e)//3+5
            buff[3] = int(ihash(x>>6))%40
        v = 0
        for y in range(oY, oY+32):
            cloud = int(buff[3] > y > buff[3]-buff[2])
            v |= (
                (int(y > (113111^(xa*(y-buff[0])))>>7%386)
                    if y+8 > buff[0]+(16-buff[1])
                    else 1 if y > buff[0] else 0 if y+3 > buff[0] else cloud)
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_cloudy_plains(self, x: int, oY: int) -> int:
        buff = ptr32(_buf) # [cloud-height, cloud-level, ground height]
        if oY == 0:
            e = (x+10)%64-10
            e = 10+e if e < 0 else 10-e if e<10 else 0
            u = int(shash(x,8,16))
            buff[0] = ((int(shash(x,16,8)) + u-20-e*e)>>1)+10
            buff[1] = int(ihash(x>>6))%12+1
            buff[2] = u>>1
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(buff[1] > y > buff[1]-buff[0]) | int(y>58-buff[2])
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_ferns(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = int(shash(x,64,40))+int(shash(x,32,48))+int(shash(x,4,8))-10
        v = 0
        for y in range(oY, oY+32):
            v |= (
                (int(y > (32423421^(x*(y-buff[0])))%128) if y > buff[0] + 5 else 0)
             ) << (y-oY)
        return v
    @micropython.viper
    def pattern_ferns_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        v = 0
        for y in range(oY, oY+32):
            v |= (
                (int(y > (32423421^(x*(y-buff[0])))%64) if y > buff[0] + 5 else 1)
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_fence_top(self, x: int, oY: int) -> int:
        return 0 if oY else -268435456

    @micropython.viper
    def pattern_chain_link_fence(self, x: int, oY: int) -> int:
        if oY==0: # Top bar with post tops
            return -268435456 if x%151>=4 else -16777216
        # Chain mess
        v = 0
        for y in range(oY, oY+32):
            ym = y%10
            v |= (
                1 if ym<=x%10<=ym+1 or ym<=(0-x)%10<=ym+1 or x%151<4 else 0
            ) << (y-oY)
        return v
w = W()