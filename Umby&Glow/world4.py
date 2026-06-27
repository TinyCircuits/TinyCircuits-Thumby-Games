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
    def pattern_launch_area(self, x: int, oY: int) -> int:
        buff = ptr32(_buf) # [box-height, platform height, chain pattern]
        if oY == 0:
            bx = int(shash(x//9,8,12))
            br = int(shash(x//9,1,4))
            # Boxes
            buff[0] = (0 if bx < 6 else bx-6)*9 + (0 if br < 2 else br-2)*9
            pr = int(ihash(x//42)) # For 0-3 platforms with 5 pixel gaps
            plnum = pr&3 # Num platforms
            pr >>= 2
            pllvl1 = pr&15 # First platform height
            pr >>= 5
            pnd = 22 if plnum==2 else 14*plnum+1 # length of platfrom
            plse = (x%42)%pnd # position into gap and platform
            # Height of current platform and gaps(-8)
            buff[1] = (-8 if pnd-plse < 8 or plnum==0 else
                pllvl1 + (x%42//pnd)*(int(pr&15)-8))
            # Chain: 1 = middle chain, 2 = chain edge
            buff[2] = (1 if plse==1 or pnd-plse==9 else
                2 if plse<3 or pnd-plse<11 else 0)
        pllvl = buff[1]
        chain = buff[2]
        v = 0
        for y in range(oY, oY+32):
            cy = y-pllvl+1
            v |= (
                1 if y>45-buff[0] else # Ground and boxes
                1 if pllvl < y < pllvl+3 # Platforms
                    or ((0 if chain!=0 and y==0 else chain) # Prevent Molaar traps
                        and y < pllvl and ( # Chains
                            cy%3==0 and chain==1 or cy%3>0 and chain==2))
                else 0
             ) << (y-oY)
        return v
    @micropython.viper
    def pattern_launch_area_fill(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        xb = (x-4)%9
        bsq = x%9==1 or x%9==7
        bedg = (x+1)%9<2
        v = 0
        for y in range(oY, oY+32):
            yb = (y-5)%9
            v |= (
                # Ground and shadow
                0 if y//3%2==0 and ((x+y)//3)%2 and y>45 else # Ground pattern
                1 if y>42+buff[0]-xb//2 else # Shadow containment
                (1 if (x+y)%(y-42) else 0) if y>45+buff[0]//5 # Scatter shadow
                else (x+y)%2 if y>45 else # Main shadow
                # Boxes
                (0 if (xb==yb%9 or xb==(0-yb)%9 # box crosses
                    or bsq or y%9==2 or y%9==8) # Box squares
                    and not (bedg or y%9<2) # edge of boxes
                    else 1)
                if y>45-buff[0]
                else 1 # Sky
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_launch_pad(self, x: int, oY: int) -> int:
        buff = ptr32(_buf) # [box-height, platform height, chain pattern]
        if oY == 0:
            pr = int(ihash(x//42)) # For 0-3 platforms with 5 pixel gaps
            plnum = pr&3 or 1 # Num platforms
            pr >>= 2
            pllvl1 = (pr&7) + 8 # First platform height
            pr >>= 4
            pnd = 22 if plnum==2 else 14*plnum+1 # length of platfrom
            plse = (x%42)%pnd # position into gap and platform
            # Height of current platform and gaps(-8)
            buff[1] = -8 if pnd-plse < 8 else pllvl1
            # Chain: 1 = middle chain, 2 = chain edge
            buff[2] = (1 if plse==1 or pnd-plse==9 else
                2 if plse<3 or pnd-plse<11 else 0)
        pllvl = buff[1]
        chain = buff[2]
        v = 0
        for y in range(oY, oY+32):
            cy = y-pllvl+1
            v |= (
                1 if y>45 else # Ground
                1 if pllvl < y < pllvl+3 # Platforms
                    or ((0 if chain!=0 and y==0 else chain) # Prevent Molaar traps
                        and y < pllvl and ( # Chains
                            cy%3==0 and chain==1 or cy%3>0 and chain==2))
                else 0
             ) << (y-oY)
        return v
    @micropython.viper
    def pattern_launch_pad_fill(self, x: int, oY: int) -> int:
        v = 0
        for y in range(oY, oY+32):
            v |= (
                0 if y//3%2==0 and ((x+y)//3)%2 and y>45 else 1
             ) << (y-oY)
        return v

    @micropython.viper
    def pattern_launch_back(self, x: int, oY: int) -> int:
        buff = ptr32(_buf) # [box height, rocket middle]
        if oY == 0:
            bx = int(shash(x//8,4,12))
            br = int(shash(x//8,1,4))
            buff[0] = (0 if bx < 6 else bx-6)*4 + (0 if br < 2 else br-2)*4
            # Rocket parameters
            rx = x%50-20
            buff[1] = rx+2 if rx > 0 else rx-2
        rx = buff[1]
        v = 0
        for y in range(oY, oY+32):
            ry = y//3-11
            v |= (
                # Rockets in the distance
                1 if rx*rx+ry*ry < 30 or (y<43 and rx*rx//5<y-30) else
                # Boxes in the distance
                int(y>43-buff[0])
             ) << (y-oY)
        return v
w = W()