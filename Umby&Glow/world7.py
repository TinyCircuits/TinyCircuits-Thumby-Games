class W:
    @micropython.viper
    def pattern_prison(self, x: int, oY: int) -> int:
        return (-16384 if oY else 262143) if x%8>5 or x%60<3 else 245760

    @micropython.viper
    def pattern_cell(self, x: int, oY: int) -> int:
        return (-256 if oY else 3407871) if x%4 and x%40>3 else (
            -1 if oY else -786433)

    @micropython.viper
    def pattern_studding(self, x: int, oY: int) -> int:
        x *= 2
        return 1 << ((((32+oY)*x)^(x))%31)
w = W()