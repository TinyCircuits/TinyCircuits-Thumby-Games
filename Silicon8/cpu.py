import random
import thumbyinterface
import types
import time
from display import AccurateDisplay

@micropython.viper
def any(array) -> bool:
    ptr = ptr8(array)
    for i in range(int(len(array))):
        if ptr[i]:
            return True
    return False

# Main Silicon8 class that holds the virtual CPU
# Pretty much a direct port of https://github.com/Timendus/silicon8 to MicroPython
class CPU:

    # Some static constants

    VIP_SCHIP_RAM_SIZE = const(3583 + 512)
    XOCHIP_RAM_SIZE    = const(65023 + 512)
    DEFAULT_STACK_SIZE = const(12)
    SCHIP_STACK_SIZE   = const(16)  # According to http://devernay.free.fr/hacks/chip8/schip.txt: "Subroutine nesting is limited to 16 levels"

    # Font definitions for the interpreter built in fonts

    chip8Font = (
        0b11110000, 0b10010000, 0b10010000, 0b10010000, 0b11110000,
        0b01100000, 0b00100000, 0b00100000, 0b00100000, 0b01110000,
        0b11110000, 0b00010000, 0b11110000, 0b10000000, 0b11110000,
        0b11110000, 0b00010000, 0b01110000, 0b00010000, 0b11110000,
        0b10100000, 0b10100000, 0b11110000, 0b00100000, 0b00100000,
        0b11110000, 0b10000000, 0b11110000, 0b00010000, 0b11110000,
        0b11110000, 0b10000000, 0b11110000, 0b10010000, 0b11110000,
        0b11110000, 0b00010000, 0b00010000, 0b00010000, 0b00010000,
        0b11110000, 0b10010000, 0b11110000, 0b10010000, 0b11110000,
        0b11110000, 0b10010000, 0b11110000, 0b00010000, 0b11110000,
        0b11110000, 0b10010000, 0b11110000, 0b10010000, 0b10010000,
        0b11110000, 0b01010000, 0b01110000, 0b01010000, 0b11110000,
        0b11110000, 0b10000000, 0b10000000, 0b10000000, 0b11110000,
        0b11110000, 0b01010000, 0b01010000, 0b01010000, 0b11110000,
        0b11110000, 0b10000000, 0b11110000, 0b10000000, 0b11110000,
        0b11110000, 0b10000000, 0b11110000, 0b10000000, 0b10000000,

        0b00111100, 0b01111110, 0b11100111, 0b11000011, 0b11000011, 0b11000011, 0b11000011, 0b11100111, 0b01111110, 0b00111100,
        0b00011000, 0b00111000, 0b01011000, 0b00011000, 0b00011000, 0b00011000, 0b00011000, 0b00011000, 0b00011000, 0b00111100,
        0b00111110, 0b01111111, 0b11000011, 0b00000110, 0b00001100, 0b00011000, 0b00110000, 0b01100000, 0b11111111, 0b11111111,
        0b00111100, 0b01111110, 0b11000011, 0b00000011, 0b00001110, 0b00001110, 0b00000011, 0b11000011, 0b01111110, 0b00111100,
        0b00000110, 0b00001110, 0b00011110, 0b00110110, 0b01100110, 0b11000110, 0b11111111, 0b11111111, 0b00000110, 0b00000110,
        0b11111111, 0b11111111, 0b11000000, 0b11000000, 0b11111100, 0b11111110, 0b00000011, 0b11000011, 0b01111110, 0b00111100,
        0b00111110, 0b01111100, 0b11100000, 0b11000000, 0b11111100, 0b11111110, 0b11000011, 0b11000011, 0b01111110, 0b00111100,
        0b11111111, 0b11111111, 0b00000011, 0b00000110, 0b00001100, 0b00011000, 0b00110000, 0b01100000, 0b01100000, 0b01100000,
        0b00111100, 0b01111110, 0b11000011, 0b11000011, 0b01111110, 0b01111110, 0b11000011, 0b11000011, 0b01111110, 0b00111100,
        0b00111100, 0b01111110, 0b11000011, 0b11000011, 0b01111111, 0b00111111, 0b00000011, 0b00000011, 0b00111110, 0b01111100,
    )

    schipFont = (
        0b11110000, 0b10010000, 0b10010000, 0b10010000, 0b11110000,
        0b00100000, 0b01100000, 0b00100000, 0b00100000, 0b01110000,
        0b11110000, 0b00010000, 0b11110000, 0b10000000, 0b11110000,
        0b11110000, 0b00010000, 0b01110000, 0b00010000, 0b11110000,
        0b10010000, 0b10010000, 0b11110000, 0b00010000, 0b00010000,
        0b11110000, 0b10000000, 0b11110000, 0b00010000, 0b11110000,
        0b11110000, 0b10000000, 0b11110000, 0b10010000, 0b11110000,
        0b11110000, 0b00010000, 0b00100000, 0b01000000, 0b01000000,
        0b11110000, 0b10010000, 0b11110000, 0b10010000, 0b11110000,
        0b11110000, 0b10010000, 0b11110000, 0b00010000, 0b11110000,
        0b11110000, 0b10010000, 0b11110000, 0b10010000, 0b10010000,
        0b11100000, 0b10010000, 0b11100000, 0b10010000, 0b11100000,
        0b11110000, 0b10000000, 0b10000000, 0b10000000, 0b11110000,
        0b11100000, 0b10010000, 0b10010000, 0b10010000, 0b11100000,
        0b11110000, 0b10000000, 0b11110000, 0b10000000, 0b11110000,
        0b11110000, 0b10000000, 0b11110000, 0b10000000, 0b10000000,

        0b00111100, 0b01111110, 0b11100111, 0b11000011, 0b11000011, 0b11000011, 0b11000011, 0b11100111, 0b01111110, 0b00111100,
        0b00011000, 0b00111000, 0b01011000, 0b00011000, 0b00011000, 0b00011000, 0b00011000, 0b00011000, 0b00011000, 0b00111100,
        0b00111110, 0b01111111, 0b11000011, 0b00000110, 0b00001100, 0b00011000, 0b00110000, 0b01100000, 0b11111111, 0b11111111,
        0b00111100, 0b01111110, 0b11000011, 0b00000011, 0b00001110, 0b00001110, 0b00000011, 0b11000011, 0b01111110, 0b00111100,
        0b00000110, 0b00001110, 0b00011110, 0b00110110, 0b01100110, 0b11000110, 0b11111111, 0b11111111, 0b00000110, 0b00000110,
        0b11111111, 0b11111111, 0b11000000, 0b11000000, 0b11111100, 0b11111110, 0b00000011, 0b11000011, 0b01111110, 0b00111100,
        0b00111110, 0b01111100, 0b11100000, 0b11000000, 0b11111100, 0b11111110, 0b11000011, 0b11000011, 0b01111110, 0b00111100,
        0b11111111, 0b11111111, 0b00000011, 0b00000110, 0b00001100, 0b00011000, 0b00110000, 0b01100000, 0b01100000, 0b01100000,
        0b00111100, 0b01111110, 0b11000011, 0b11000011, 0b01111110, 0b01111110, 0b11000011, 0b11000011, 0b01111110, 0b00111100,
        0b00111100, 0b01111110, 0b11000011, 0b11000011, 0b01111111, 0b00111111, 0b00000011, 0b00000011, 0b00111110, 0b01111100,
    )

    def __init__(self):
        # CHIP-8 interpreter state that isn't initialized elsewhere
        self.stop()
        self.v = bytearray(16)
        self.i = 0
        self.userFlags = bytearray(16)
        self.display = AccurateDisplay(self)
        self.rendering = False

    def start(self):
    	self.running = True

    def stop(self):
    	self.running = False

    @micropython.native
    def clockTick(self, t):
        if not self.running:
            return

        # Tick timers
        if self.dt > 0:
        	self.dt -= 1

        if self.st > 0:
        	if not self.playing:
        		self.playing = True
        		thumbyinterface.playSound(self.playingPattern, self.pattern, self.pitch)
        		self.audioDirty = False
        	self.st -= 1
        else:
        	if self.playing:
        		self.playing = False
        		self.audioDirty = False
        		thumbyinterface.stopSound()

        # Trigger audio updates if dirty
        if self.audioDirty:
        	thumbyinterface.playSound(self.playingPattern, self.pattern, self.pitch)
        	self.audioDirty = False

        # Render display if dirty (only render half of the interrupts to save a
        # few CPU cycles)
        self.rendering = not self.rendering
        if self.display.dirty and self.rendering:
            thumbyinterface.render(self.display.width, self.display.height, self.display.frameBuffers)
            self.display.dirty = False

        # Register display redraw interrupt for dispQuirk
        self.display.interrupt()

    @micropython.viper
    def run(self, program):
        ram = ptr8(self.ram)
        prog = ptr8(program)
        for i in range(int(len(program))):
            ram[i + 0x200] = prog[i]
        while self.running and not thumbyinterface.breakCombo():
            self.cycle()

    def reset(self, interpreter):
        self.stop()

        if interpreter != types.AUTO:
            self.specType = interpreter
            self.typeFixed = True
        else:
            self.specType = types.VIP
            self.typeFixed = False

        if interpreter == types.VIP:
        	self.RAMSize = CPU.VIP_SCHIP_RAM_SIZE
    		self.stackSize = CPU.DEFAULT_STACK_SIZE
    	elif interpreter == types.SCHIP:
    		self.RAMSize = CPU.VIP_SCHIP_RAM_SIZE
    		self.stackSize = CPU.SCHIP_STACK_SIZE
    	elif interpreter == types.XOCHIP:
    		self.RAMSize = CPU.XOCHIP_RAM_SIZE
    		self.stackSize = CPU.DEFAULT_STACK_SIZE
    	elif interpreter == types.AUTO: # Takes maximum sizes, determines limits at runtime
    		self.RAMSize = CPU.XOCHIP_RAM_SIZE
    		self.stackSize = CPU.SCHIP_STACK_SIZE

        # Initialize registers
        self.pc = 0x200
        self.sp = self.stackSize - 1
        self.dt = 0
        self.st = 0

        # Initialize XO-Chip audio "registers"
        self.pattern = [0] * 16
        self.pitch = 4000
        self.playingPattern = False
        self.audioDirty = False

        # Initialize memory
        self.display.reset()
        self.stack = [0] * self.stackSize
        self.ram = bytearray(self.RAMSize)

        # Initialize internal variables
        self.waitForKey = False
        self.WaitForInt = 0
        self.playing = False
        self.running = True
        self.cyclesPerFrame = 30

        # Determine quirks to use
        self.setQuirks()

        # Load the appropriate font
        self.loadFont()

        self.start()

    def setQuirks(self):
        self.shiftQuirk = self.specType == types.SCHIP
        self.jumpQuirk = self.specType == types.SCHIP
        self.memQuirk = self.specType != types.SCHIP
        self.vfQuirk = self.specType == types.VIP
        self.clipQuirk = self.specType != types.XOCHIP
        self.dispQuirk = self.specType == types.VIP

    @micropython.native
    def bumpSpecType(self, newType):
        if self.typeFixed:
            return
        if newType > self.specType:
            self.specType = newType
            self.setQuirks()
            if newType == types.SCHIP:
                print("Auto-upgraded interpreter to SCHIP")
            elif newType == types.XOCHIP:
                print("Auto-upgraded interpreter to XOCHIP")

    # Run the CPU for one cycle and return control
    @micropython.native
    def cycle(self):
        if not self.running:
            return

        op  = self.ram[self.a(self.pc)]<<8 | self.ram[self.a(self.pc+1)]
        x   = self.ram[self.a(self.pc)] & 0x0F
        y   = (self.ram[self.a(self.pc+1)] & 0xF0) >> 4
        n   = self.ram[self.a(self.pc+1)] & 0x0F
        nn  = self.ram[self.a(self.pc+1)] & 0xFF
        nnn = x<<8 | nn

        self.pc += 2

        check = op & 0xF000
        if check < 0x8000:
            self.opcodes0to7(check, op, x, y, n, nn, nnn)
        elif check == 0x8000:
            self.maths(x, y, n)
        elif check == 0x9000:
            if self.v[x] != self.v[y]:
                self.skipNextInstruction()
        elif check == 0xA000:
            # Set i
            self.i = nnn
        elif check == 0xB000:
            # Jump to i + "v0"
            if self.jumpQuirk:
                self.pc = nnn + self.v[x]
            else:
                self.pc = nnn + self.v[0]
        elif check == 0xC000:
            # Set register to random number
            self.v[x] = random.randint(0, 255) & nn
        elif check == 0xD000:
            self.display.draw(x, y, n)
        elif check == 0xE000:
            if nn == 0x9E:
                if thumbyinterface.getKeys()[self.v[x]]:
                    self.skipNextInstruction()
            elif nn == 0xA1:
                if not thumbyinterface.getKeys()[self.v[x]]:
                    self.skipNextInstruction()
        elif check == 0xF000:
            if nn < 0x29:
                self.opcodesFX1EandBelow(nn, x)
            else:
                self.opcodesFX29andUp(nn, x)

    # @micropython.native
    def opcodes0to7(self, check:int, op:int, x:int, y:int, n:int, nn:int, nnn:int):
        if check == 0x0000:
            self.machineCall(op, n)
        elif check == 0x1000:
            # Jump
            self.pc = nnn
        elif check == 0x2000:
            # Call
            self.stack[self.s(self.sp)] = self.pc
            self.sp -= 1
            self.pc = nnn
        elif check == 0x3000:
            if self.v[x] == nn:
                self.skipNextInstruction()
        elif check == 0x4000:
            if self.v[x] != nn:
                self.skipNextInstruction()
        elif check == 0x5000:
            if x > y:
                n = x
                x = y
                y = n

            if n == 2:
                # Store range of registers to memory
                for i in range(x, y + 1):
                    self.ram[self.a(self.i+(i-x))] = self.v[i]
                self.bumpSpecType(types.XOCHIP)
            elif n == 3:
                # Load range of registers from memory
                for i in range(x, y + 1):
                    self.v[i] = self.ram[self.a(self.i+(i-x))]
                self.bumpSpecType(types.XOCHIP)
            else:
                if self.v[x] == self.v[y]:
                    self.skipNextInstruction()
        elif check == 0x6000:
            # Set register
            self.v[x] = nn
        elif check == 0x7000:
            # Add to register
            self.v[x] += nn

    @micropython.native
    def opcodesFX1EandBelow(self, nn:int, x:int):
        if nn == 0x00:
            # Set i register to 16-bit value
            self.i = self.ram[self.a(self.pc)]<<8 | self.ram[self.a(self.pc+1)]
            self.pc += 2
            self.bumpSpecType(types.XOCHIP)
        elif nn == 0x01:
            # Enable the second plane if it hasn't been enabled yet
            self.display.numPlanes = 2
            # Select plane X
            self.display.selectedPlane = x
            self.bumpSpecType(types.XOCHIP)
        elif nn == 0x02:
            # XO-Chip: Load 16 bytes of audio buffer from (i)
            for i in range(0, 16):
                self.pattern[i] = self.ram[self.a(self.i+i)]
            self.playingPattern = True
            self.audioDirty = True
            self.bumpSpecType(types.XOCHIP)
        elif nn == 0x07:
            # Set register to value of delay timer
            self.v[x] = self.dt
        elif nn == 0x0A:
            # Wait for keypress and return key in vX
            while True:
                keyboard = thumbyinterface.getKeys()
                if not any(keyboard):
                    break
                time.sleep_ms(1)
            while True:
                keyboard = thumbyinterface.getKeys()
                if any(keyboard):
                    break
                time.sleep_ms(1)
            for i in range(len(keyboard)):
                if keyboard[i]:
                    self.v[x] = i
                    return
        elif nn == 0x15:
            # Set delay timer to value in vX
            self.dt = self.v[x]
        elif nn == 0x18:
            # Set sound timer to value in vX
            self.st = self.v[x]
        elif nn == 0x1E:
            # Add vX to i register
            self.i += self.v[x] & 0xFFFF

    @micropython.native
    def opcodesFX29andUp(self, nn:int, x:int):
        if nn == 0x29:
            # Set i register to font data
            self.i = self.v[x] * 5
        elif nn == 0x30:
            # Set i register to large font data
            self.i = self.v[x]*10 + 80
            self.bumpSpecType(types.SCHIP)
        elif nn == 0x33:
            # Binary coded decimal from vX to address in i
            self.ram[self.a(self.i+0)] = int(self.v[x] / 100)
            self.ram[self.a(self.i+1)] = int(self.v[x] % 100 / 10)
            self.ram[self.a(self.i+2)] = self.v[x] % 10
        elif nn == 0x3A:
            # XO-Chip: Change pitch of audio pattern
            self.pitch = 4000 * pow(2, (self.v[x]-64)/48)
            self.playingPattern = True
            self.audioDirty = True
            self.bumpSpecType(types.XOCHIP)
        elif nn == 0x55:
            # Store registers to memory (regular VIP/SCHIP)
            for i in range(0, x + 1):
                self.ram[self.a(self.i + i)] = self.v[i]
            if self.memQuirk:
                self.i = (self.i + x + 1) & 0xFFFF
        elif nn == 0x65:
            # Load registers from memory (regular VIP/SCHIP)
            for i in range(0, x + 1):
                self.v[i] = self.ram[self.a(self.i + i)]
            if self.memQuirk:
                self.i = (self.i + x + 1) & 0xFFFF
        elif nn == 0x75:
            # Store registers to "user flags" (SCHIP)
            for i in range(0, x + 1):
                self.userFlags[i] = self.v[i]
            self.bumpSpecType(types.SCHIP)
        elif nn == 0x85:
            # Load registers from "user flags" (SCHIP)
            for i in range(0, x + 1):
                self.v[i] = self.userFlags[i]
            self.bumpSpecType(types.SCHIP)

    @micropython.native
    def machineCall(self, op:int, n:int):
        check = op & 0xFFF0
    	if check == 0x00C0:
    		self.display.scrollDown(n)
    		self.bumpSpecType(types.SCHIP)
    		return
    	elif check == 0x00D0:
    		self.display.scrollUp(n)
    		self.bumpSpecType(types.XOCHIP)
    		return

        if op == 0x00E0:
            # Clear screen
            self.display.clear()
        elif op == 0x00EE:
            # Return
            self.sp += 1
            self.pc = self.stack[self.s(self.sp)]
        elif op == 0x00FB:
    		self.display.scrollRight()
    		self.bumpSpecType(types.SCHIP)
    	elif op == 0x00FC:
    		self.display.scrollLeft()
    		self.bumpSpecType(types.SCHIP)
    	elif op == 0x00FD:
    		# Exit interpreter
    		self.running = False
    		self.bumpSpecType(types.SCHIP)
    	elif op == 0x00FE:
    		# Set normal screen resolution
    		self.display.setResolution(64, 32)
    		self.bumpSpecType(types.SCHIP)
    	elif op == 0x00FF:
    		# Set extended screen resolution
    		self.display.setResolution(128, 64)
    		self.bumpSpecType(types.SCHIP)
    	else:
            print("RCA 1802 assembly calls not supported at address", self.pc-2, "opcode", op)
            self.running = False

    @micropython.viper
    def maths(self, x:int, y:int, n:int):
        regs = ptr8(self.v)
    	if n == 0x0:
    		regs[x] = regs[y]
    	elif n == 0x1:
    		regs[x] |= regs[y]
    		if self.vfQuirk:
    			regs[0xF] = 0
    	elif n == 0x2:
    		regs[x] &= regs[y]
    		if self.vfQuirk:
    			regs[0xF] = 0
    	elif n == 0x3:
    		regs[x] ^= regs[y]
    		if self.vfQuirk:
    			regs[0xF] = 0
    	elif n == 0x4:
    		# Add register vY to vX
    		# Set VF to 01 if a carry occurs
    		# Set VF to 00 if a carry does not occur
    		flag:bool = (0xFF - regs[x]) < regs[y]
    		regs[x] += regs[y]
    		self.setFlag(flag)
    	elif n == 0x5:
    		# Subtract register vY from vX and store in vX
    		# Set VF to 00 if a borrow occurs
    		# Set VF to 01 if a borrow does not occur
    		flag:bool = regs[x] >= regs[y]
    		regs[x] -= regs[y]
    		self.setFlag(flag)
    	elif n == 0x6:
    		# Shift right
    		if self.shiftQuirk:
    			y = x
    		# Set register VF to the least significant bit prior to the shift
    		flag:bool = regs[y] & 0b00000001 > 0
    		regs[x] = regs[y] >> 1
    		self.setFlag(flag)
    	elif n == 0x7:
    		# Subtract register vX from vY and store in vX
    		# Set VF to 00 if a borrow occurs
    		# Set VF to 01 if a borrow does not occur
    		flag:bool = regs[y] >= regs[x]
    		regs[x] = regs[y] - regs[x]
    		self.setFlag(flag)
    	elif n == 0xE:
    		# Shift left
    		if self.shiftQuirk:
    			y = x
    		# Set register VF to the most significant bit prior to the shift
    		flag:bool = regs[y] & 0b10000000 > 0
    		regs[x] = regs[y] << 1
    		self.setFlag(flag)

    @micropython.native
    def skipNextInstruction(self):
        nextInstruction = self.ram[self.a(self.pc)]<<8 | self.ram[self.a(self.pc+1)]
    	if nextInstruction == 0xF000:
            self.pc += 4
        else:
            self.pc += 2

    @micropython.native
    def a(self, address:int):
        if address >= self.RAMSize:
            print("Program attempted to access RAM outsize of memory")
            return 0
        if address >= CPU.VIP_SCHIP_RAM_SIZE:
            self.bumpSpecType(types.XOCHIP)
        return address

    @micropython.native
    def s(self, address:int):
        if address >= self.stackSize:
            print("Program attempted to access invalid stack memory")
            return 0
        if self.stackSize == CPU.SCHIP_STACK_SIZE and address < (CPU.SCHIP_STACK_SIZE-CPU.DEFAULT_STACK_SIZE):
            self.bumpSpecType(types.SCHIP)
        return address

    @micropython.native
    def setFlag(self, comparison:bool):
        self.v[0xF] = 0
        if comparison:
            self.v[0xF] = 1

    def loadFont(self):
        if self.specType == types.SCHIP or self.specType == types.XOCHIP:
            font = CPU.schipFont
        else:
            font = CPU.chip8Font

        for i in range(len(font)):
            self.ram[i] = font[i];
