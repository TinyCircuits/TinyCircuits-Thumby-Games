class W:
    @micropython.viper
    def pattern_tree_wall(self, x: int, oY: int) -> int:
        xa = x*x*40//((x%40+20)+1)
        return ((
                int(0x00000FFF)<<((xa+oY)%64-16) |
                uint(0xFFF00000)>>(32-(xa)%32)
            ) if xa%12 > 4 # Tree middle
            else -1 if (xa-1)%12 > 2 # Bark
            else 0 # Gaps
        )

    @micropython.viper
    def pattern_forest_ferns(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY < 32:
            buff[2] = int(shash(x,40,30))+int(shash(x,16,24))+10 # Fern pattern
        v = 0
        for y in range(oY, oY+32):
            v |= (
                (int(y > (32423421^(x*(y-buff[2])))%56) if y > buff[2] + 10 else 0)
             ) << (y-oY)
        return v
    @micropython.viper
    def pattern_forest_ferns_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        v = 0
        oY -= 15
        for y in range(oY, oY+32):
            v |= (
                (int(y > (32423421^(x*(y-buff[2])))%64) if y > buff[2] else 1)
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_tree_branches(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[3] = int(shash(x,32,30)) + int(shash(x,5,6)) - 10
        br = buff[3]
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int((y%(br%20+5) < br-y//6-5 and y < 30) or y == 0)
            ) << (y-oY)
        return v
    @micropython.viper
    def pattern_tree_branches_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        br = buff[3]
        v = 0
        for y in range(oY, oY+32):
            v |= (
               int((y*y)%((y+br+x)%10) < 1) if y%(br%20+5) < br-y//6-8 and y < 30 else 1
            ) << (y-oY)
        return v | int(1431655765)<<(x%2)

    @micropython.viper
    def pattern_forest(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = x+int(shash(x,50,80)) # Tree width / gap variance
            buff[1] = x*x*40//((x%40+20)+1) # Tree patterner
        xb = buff[0]
        return ((-1 if (xb-3)%120 > 94 # Trees
            else 0) # Tree gaps
            | int(self.pattern_forest_ferns(x, oY)) # Gaps and Ferms
            | int(self.pattern_tree_branches(x, oY))) # Branches and vines
    @micropython.viper
    def pattern_forest_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        xb = buff[0]
        xa = buff[1]
        return (((
                int(0x00000FFF)<<((xa+oY)%64-16) |
                uint(0xFFF00000)>>(32-(xa)%32) |
                int(1431655765)<<(x%2)
            ) if xb%120 > 100 # Tree middle
            else -1)
            & int(self.pattern_forest_ferns_fill(x, oY))
            & int(self.pattern_tree_branches_fill(x, oY)))

    @micropython.viper
    def pattern_mid_forest(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        if oY == 0:
            buff[0] = x+int(shash(x,50,80)) # Tree width / gap variance
            buff[1] = x*x*40//((x%40+20)+1) # Tree patterner
        xb = buff[0]
        v = 0
        for y in range(oY, oY+32):
            v |= (
                int(32423421%((y+x-200)%5000+400)<300) # sunlight
             ) << (y-oY)
        return (-1 if (xb-3)%60 > 39 # Trees
            else v
            ) | int(self.pattern_forest_ferns(x, oY+10)) # Gaps and Ferms
    @micropython.viper
    def pattern_mid_forest_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        xb = buff[0]
        xa = buff[1]
        return ((
                int(0x00000FFF)<<((xa+oY)%64-16) |
                uint(0xFFF00000)>>(32-(xa)%32) |
                int(1431655765)<<(x//2%2)
            ) if xb%60 > 45 # Tree middle
            else -1 if (xb-3)%60 > 39 # Tree edge
            else 0 if (xb-5)%60 > 35 # Tree shadow
            else -1) & int(self.pattern_forest_ferns_fill(x, oY+5))
w = W()