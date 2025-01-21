class W:
    @micropython.viper
    def pattern_nebula(self, x: int, oY: int) -> int:
        snco = ptr8(sinco)
        v = 0
        for y in range(oY, oY+32):
            v |= (
               1 if snco[((x*x)^((y+100)*(y+100)))%400] < 2 else 0
            ) << (y-oY)
        return v

    @micropython.viper
    def _orbitals_prep(self, x: int, oY: int) -> int:
        buff = ptr32(_buf)
        st = x//128*128
        buff[0] = xs = int(ihash(st))
        # Sub-sector's
        xs |= xs>>16
        sfa = sc = si = 0
        while si < 16:
            ns = sc*sc+16
            if st + ns >= x//128*128+128:
                sfa -= 1
                break
            if xs & (1<<si):
                sfa += 1
                sc += 1
            else:
                if st + ns < x:
                    st += ns + 5
                    sc = 0
                    sfa = 1
                else:
                    break
            si += 1
        buff[1] = int(ihash(st))
        buff[2] = sfa
        buff[3] = st

    @micropython.viper
    def pattern_orbitals(self, x: int, oY: int) -> int:
        snco = ptr8(sinco)
        buff = ptr32(_buf)
        if oY == 0:
            self._orbitals_prep(x, oY)
        rand1 = buff[0] # 128 pixel sector randomizer
        rand2 = buff[1] # sub sector randomizer
        st = buff[3] # Sector position
        sfa = buff[2] # Sector size factor ~(1-15)
        sf = sfa*sfa

        # Vertical position (centered on top row: 0; (-20, 80))
        yh = rand2%(90+sfa*4)-15-sfa*2
        rand2 >>= 1
        cres = rand2%70-11 # Crescenting amoount (11-80)
        gib = rand2%2 # Whether to gibbous (0-1)
        rand2 >>= 1
        lit = rand2%2 # Shadowed or lit (0-1)
        a = x//2 + (200 if lit or gib else 0) # Rotation (0-400)
        rand2 >>= 1
        bl = rand2%16 # Backlighting (0-15)
        sfc = rand2%21 # Curvature (0-20)
        rand2 >>= 1
        sfcs = rand2%17 # Sheer (0-16)
        # Surface pattern parameters
        rand2 >>= 1
        drf = rand2%20+1 # drift (1-20)
        rand2 >>= 1
        srd = rand2%20+1 # spread (1-20)
        rand2 >>= 1
        fld = rand2%20+1 # fold (1-20)

        bl *= sfa
        sfc = (sfc + rand1*sfcs//16)%20
        sz = sf*10 # sector size
        x = x - st - sfa*2-(sfa*100//80 if sfa>6 else +4) # x relative to sector
        sina = (snco[(a+200)%400]-128)
        cosa = (snco[(a-100)%400]-128)

        v = f = 0
        for y in range(oY, oY+32):
            y1 = y-yh
            py = y1 + x + 0-snco[(x*3//2-100)%400]*(y1-sfc)//4
            # Surface pattern
            sp = 1 if (py*(py//srd)//drf)%(fld*2)<fld else 0
            # Rotation
            x1 = cosa*x//128 - sina*y1//128
            y1 = sina*x//128 + cosa*y1//128
            # Shaded orbital
            xx = x1*x1
            y2 = (y1)*cres
            cresgib = xx+y2*y2//100 > sz and y1 < 0
            cresgib = (0 if cresgib else 1) if gib else cresgib
            d = xx+y1*y1
            v |= (1 if d<sz+bl else 0) << (y-oY)
            f |= (
                1 if d>sz else 0 if (sp if d<sz and cresgib else
                    1 if sz<d<sz+bl else lit if d<sz else 0) else 1
            ) << (y-oY)
        buff[4 if oY==0 else 5] = f
        return v
    @micropython.viper
    def pattern_orbitals_fill(self, x: int, oY: int) -> int:
        return ptr32(_buf)[4 if oY==0 else 5]

    @micropython.viper
    def pattern_hull(self, x: int, oY: int) -> int:
        snco = ptr8(sinco)
        xm = 36+(x//36%128)
        x1 = x%xm-xm//2
        v = f = 0
        for y in range(oY, oY+32):
            y1 = y-20
            sp = 1 if int(fsqrt(int(abs(x1*100))))*y1%x1 else 0
            if x1//20%2:
                sp &= 1 if (snco[(x1+200)%400]*y1)%6 else 0
            sp |= 1 if ((y+x)%2 and -4 <= x1 <= 4) else 0
            px = x + snco[(x-100)%400]*y1
            py = y1
            sp |= 1 if x//41%2 and (px+py)%12<6 else 0
            v |= (sp) << (y-oY)
        return v
w = W()