import machine
import rp2
import time
import math

unusedpins = [7, 8, 9, 10, 11, 21, 22] #do not change or reorder these - their relative positions are hardcoded in pio_mixer.
commpins = [machine.Pin(i, machine.Pin.OUT) for i in unusedpins] #these pins are for communication between PIO cores. Each one will have one audio channel on it for the main core to mix together.
waitpin = machine.Pin(25, machine.Pin.OUT) #sends inhibit signal to the audio channels. 25 is hardcoded in the wavegens since in_base is already in use. This sadly seems imperfect, but is necessary since the IRQ flags aren't shared between the two PIO blocks.
audiopin = machine.Pin(28, machine.Pin.OUT)

synthcore = None
channels = []
samplerate = 48000
tickfreq = 1 #how many decrements happen per second in the wave generators.
channelcount = 0 #how many channels the mixer is currently outputting
config = [] #which core types are assigned

SQUARE = 0
NOISE = 1
twelveroottwo = 1.059463094
czero = 8.175798916

#This always takes exactly 8 clock cycles to loop no matter what.
#This repeatedly counts down from the given value until it hits 0, then toggles the pin. The pin is toggled every n+1 loops (eg giving a value of 2 means 3 loops on, 3 loops off, repeat)
#X holds the starting value, Y holds the counter. It will generate the next value within 7 cycles of IRQ 7 being cleared.
#Unless a 0 is explicitly given, it will keep the current count/phase to allow for seamless pitch changes.
#Note that pitch changes don't apply until the counter runs out, so absuredly (unusably) low pitches may stop the channel from updating in time unless a 0 is given.
@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW)
def pio_wavegen():
    label("clearcounter")
    set(y, 0) #clear the current count if the channel is disabled
    mov(pins, y) #clear pin to keep phase consistent. Using mov so set_base can be left alone.
    label("nextstep")
    nop() [1] #account for the missing delay when not toggling pins
    wrap_target()
    wait(0, gpio, 25) #stall if inhibit pin is set
    pull(noblock) #read new frequency if necesary
    mov(x, osr) #store in x
    jmp(not_x, "clearcounter") #do nothing if the frequency is 0 - this effectively disables the channel.
    jmp(y_dec, "nextstep") [1] #jump to top if y isn't 0, then unconditionally decrement y
    mov(pins, invert(pins)) #toggle output pin
    mov(y, x) #reset y to given counter value


#this takes 8 cycles to loop while counting, and an additional 6 or 7 on updating the pin. This discrepancy doesn't really affect this since the output is random instead of a pure tone.
#this pretty much functions the same as pio_wavegen, except instead of always toggling the output pin, it uses an LFSR to toggle it randomly.
#X holds the starting value, Y holds the counter, ISR holds the LFSR state. The pin is also used as a temporary value, holding a copy of the lowest bit in the LFSR.
#This is a 22 bit wide LFSR that uses the lowest and highest bits for generating the next value. It takes about 4 million steps before the sequence repeats.
#22 is the largest width that fits while producing an optimal sequence. 15 is also optimal but repeats often enough to hear the pattern.
@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_LEFT, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def pio_lfsr():
    set(isr, 1) #initialize the LFSR. This *could* be done after "clearcounter", but the first little bit of sound is pretty rough so regularly replaying it is undesirable.
    mov(pins, invert(isr)) #set the pin to 0 since it's value is used in updating the LFSR. Using mov/invert so set_base can be left alone.
    label("clearcounter")
    set(y, 0) #clear the current count if the channel is disabled
    label("nextstep")
    wrap_target()
    wait(0, gpio, 25) #stall if inhibit pin is set
    pull(noblock) #read new frequency if necesary
    mov(x, osr) #store in x
    jmp(not_x, "clearcounter") [3] #do nothing if the frequency is 0 - this effectively disables the channel. Delay to keep the main loops 8 cycles.
    jmp(y_dec, "nextstep") #jump to top if y isn't 0, then unconditionally decrement y
    mov(osr, isr) #copy the LFSR state
    out(y, 20) #discard the lower bits. This allows choosing the width of the LFSR, in this case 22. The value in this instruction must be width-2
    out(y, 1) #put the highest bit of the LFSR into y
    jmp(not_y, "noflip")
    mov(pins, invert(pins)) #conditionally toggle the pin. This functionally behaves as "pin = lowestBit ^ highestBit" since the pin still holds the lowest bit from the last round
    label("noflip")
    in_(pins, 1) #shift the new bit into the LFSR
    mov(y, x) #reset y to given counter value


cyclesperchannel = 16
#this outputs one channel every 16 cycles
#it can be reduced to 13 by subtracting 3 from each delay, but a nice round 16 was preferable
#the additional delay was placed on the IRQ to give a little more time to generate the samples. It shouldn't be necessary but it's the most sensible place to put it.
@rp2.asm_pio(out_init=rp2.PIO.OUT_LOW, in_shiftdir=rp2.PIO.SHIFT_LEFT, set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def pio_mixer():
    label("disablewaves")
    set(pins, 1) [12] #set flag to disable wave generators - the delay here isn't really necessary but it makes it take the same length of time even when disabled
    label("nextsample")
    pull(noblock) #read channel count if necesary
    mov(x, osr) #store in x
    jmp(not_x, "disablewaves") #do nothing if the channel count is 0 - this also pauses wave generators allowing setting all frequencies on the same sample
    set(pins, 0) [3] #ensure wave generators are enabled
    mov(osr, pins) #read all channels in from other cores
    out(y, 14) #discard all bits below channel 6
    in_(osr, 2) #move channels 6 and 7 into ISR
    in_(pins, 5) #add the remaining channels into ISR
    mov(osr, isr) #move everything to OSR
    mov(y, x) #copy channel count to y
    jmp(y_dec, "nextchannel") #decrement y
    label("nextchannel")
    out(pins, 1) #output channel
    jmp(not_y, "nextsample") #back to the top if that was the last channel
    jmp(y_dec, "nextchannel") [13] #this delay happens on all but the last channel, leaving time for prep before the next set of channels


def configure(types=None, corecount=7): #set up state machines
    global synthcore, channels, tickfreq, channelcount, config
    
    if types == None: types = []
    config = types[:]
    while len(config) < corecount: config.append(SQUARE) #default unassigned channels to square wave
    pool1 = [1,2,3] #state machines capable of square only
    pool2 = [4,5,6,7] #state machines capable of both
    
    synthcore = rp2.StateMachine(0, pio_mixer, in_base=commpins[0], out_base=audiopin, set_base=waitpin, freq=cyclesperchannel*corecount*samplerate) #the frequency of this isn't particularly important as long as it's high enough to output every channel above audible range
    synthcore.put(0)
    synthcore.active(1)
    channelcount = 0
    
    tickfreq = machine.freq() // 8
    
    channels = []
    for i in range(corecount):
        if config[i] == SQUARE:
            if len(pool1): sm = pool1.pop() #select a free state machine from the square pool if possible
            elif len(pool2): sm = pool2.pop() #otherwise select one from the other pool
            else:
                print("[polysynth] Not enough channels available for requested configuration.")
                break
            channels.append(rp2.StateMachine(sm, pio_wavegen, in_base=commpins[i], out_base=commpins[i]))
            
        elif config[i] == NOISE:
            if len(pool2): sm = pool2.pop() #select a free state machine from the noise pool
            elif len(pool1):
                print("[polysynth] Not enough noise channels available for requested configuration.")
                sm = pool1.pop()
            else:
                print("[polysynth] Not enough channels available for requested configuration.")
                break
            channels.append(rp2.StateMachine(sm, pio_lfsr, in_base=commpins[i], out_base=commpins[i]))
            
        channels[-1].put(0) #disable by default
        channels[-1].active(1)


def enabled(value=None): #returns the channel count. Passing a number will set the channel count
    global channelcount
    if value != None:
        synthcore.put(value)
        channelcount = value
    return channelcount


def stop(mixer=True, chan=True, song=True):
    global channelcount, playing, notes
    if song:
        playing = False
        timer.deinit()
        notes = [None for i in range(7)]
    if chan:
        for i in channels: i.put(0)
    if mixer:
        synthcore.put(0)
        channelcount = 0


def setpitch(chan, pitch): #set a channel's pitch in hertz. Floats are accepted. None to disable the channel.
    if 0 <= chan < len(channels) and channels[chan].tx_fifo() < 4:
        if pitch == 0 or pitch == None:
            channels[chan].put(0)
        else:
            channels[chan].put(int(tickfreq // (2*pitch)) - 1)


def setnote(chan, pitch): #set a channel's pitch to a specific note, according to MIDI numbering (60 is middle C). Floats are accepted. None to disable the channel.
    if 0 <= chan < len(channels) and channels[chan].tx_fifo() < 4:
        if pitch == None:
            channels[chan].put(0)
        else:
            channels[chan].put(int(tickfreq // (2*czero*twelveroottwo**pitch)) - 1)


#everything from this point forward is the sequencer.


timer = machine.Timer()
stream = None
eventstart = 0
playing = False
autoreset = False
setenabled = False
notes = [None for i in range(7)] #what MIDI notes are currently playing
instruments = [None for i in range(7)] #persistently playing instruments. Each is either None or (phaseLocked, pitch, vibratoSpeed, vibratoAmount, startTime, channel, rise, length)

ilist = {} #defined instruments. Each is (phaseLocked, phaseOffset, detune, vibratoSpeed, vibratoAmount, rise, length).
#phaseLocked is a bool
#phaseOffset is a float, halfCycles (0.5 is 90 degrees out of phase, 1.0 is 180, 1.5 is 270, etc.
#detune is a float, midiPitch
#vibratoSpeed is a float, hertz
#vibratoAmount is a float, midiPitch
#rise is a float, midiPitch change per second
#length is a float, duration in milliseconds


def instrument(phaselock=False, phase=None, detune=0, vibspeed=0, vibamount=0, rise=0, length=None):
    return (phaselock, phase, detune, vibspeed, vibamount, rise, length)


def makepersist(chan, pitch, ins, starttime):
    if ins[4] or ins[5] or ins[6]:
        return (True if ins[1] != None or ins[0] else False, pitch + ins[2], ins[3], ins[4], starttime, chan, ins[5], ins[6])
    else:
        return None


#supported events:
#Note off - (timestamp_ms, 0, channel)
#Note on - (timestamp_ms, 1, channel, midiPitch, instrumentNum)
#Set enabled channel count - (timestamp_ms, 2, channelCount)
#Run a callback function - (timestamp_ms, 3, function, data) - data is usually repurposed midiPitch, but can be anything
#@micropython.native
def audiotick(dummy):
    global playing, eventstart, notes, stream
    stop = True
    lockedwrites = [] #phase-locked changes - each is (channel, value). This should probably be changed to have one queue per channel to avoid multiple notes per tick messing up timing.
    
    if stream != None and stream.nextevent != None: #if a song needs playing
        stop = False
        while stream.nextevent != None and stream.nextevent[0] < time.ticks_ms()-eventstart:
            event = stream.nextevent
            #print(event)
            if event[1] == 1: #note on
                notes[event[2]] = event[3]
                instruments[event[2]] = None
                
                if not event[4] in ilist: #no defined instrument
                    setnote(event[2], event[3])
                    
                else:
                    ins = ilist[event[4]]
                    halfcycle = int(tickfreq // (2*czero*twelveroottwo**(event[3] + ins[2])))
                    
                    if ins[4] or ins[5] or ins[6]: #has vibrato, rise, or duration
                        instruments[event[2]] = makepersist(event[2], event[3], ins, event[0]+eventstart)
                    
                    elif ins[1] != None: #has specified phase offset
                        lockedwrites.append((event[2], 0)) #clear current phase
                        lockedwrites.append((event[2], int(halfcycle*(1.0+ins[1])) - 1)) #delay to get intended phase amount
                        lockedwrites.append((event[2], halfcycle - 1)) #set intended pitch
                        
                    elif ins[0]: #phase locked
                        lockedwrites.append((event[2], 0)) #clear current phase
                        lockedwrites.append((event[2], halfcycle - 1)) #set intended pitch
                    
                    elif channels[event[2]].tx_fifo() < 4: #not phase locked
                        channels[event[2]].put(halfcycle-1)
            
            elif event[1] == 0: #note off
                notes[event[2]] = None
                setnote(event[2], None)
                instruments[event[2]] = None
            
            elif event[1] == 2: #set channel count
                if setenabled:
                    enabled(event[2])
            
            elif event[1] == 3: #run callback
                event[2](event[3])
            
            stream.readevent()
        
        if stream.nextevent == None and autoreset:
            if stream.reset():
                eventstart = time.ticks_ms()
    
    for i in range(7):
        if instruments[i] != None: #if an instrument needs updating
            stop = False
            ins = instruments[i]
            
            if ins[7] and (time.ticks_ms() > ins[4]+ins[7]):
                instruments[i] = None
                if channels[ins[5]].tx_fifo() < 4:
                    channels[ins[5]].put(0)
                continue
            
            #if ins[3] == 0 and ins[6] == 0: continue #don't recalculate pitch if not needed
            
            pitch = ins[1]
            if ins[3]: pitch += math.sin((time.ticks_ms()-ins[4])/1000*2*math.pi*ins[2]) * ins[3] #add vibrato if it uses it
            if ins[6]: pitch += (time.ticks_ms()-ins[4])/1000 * ins[6]
            halfcycle = int(tickfreq // (2*czero*twelveroottwo**(pitch)))
            if ins[0]: #phase locked
                lockedwrites.append((ins[5], halfcycle-1))
            elif channels[ins[5]].tx_fifo() < 4: #not phase locked
                channels[ins[5]].put(halfcycle - 1)
    
    if len(lockedwrites):
        fastwrite([(channels[i[0]].tx_fifo, channels[i[0]].put, i[1]) for i in lockedwrites])
    
    if stop:
        timer.deinit()
        notes = [None for i in range(7)]
        stream = None
        playing = False
        #print("Timer stopped")


@micropython.native
def fastwrite(events):
    mixwrite = synthcore.put #cache these in local variables for slightly better speed
    cc = channelcount
    mixwrite(0) #disable wavegens
    for i in events: #each is (core.tx_fifo, core.put, num)
        if i[0]() < 4:
            i[1](i[2])
        else:
            print("[polysynth] Warning: could not write all phase-locked events")
    mixwrite(cc) #enable wavegens


class StreamWrapper: #turn a list of events into a stream
    def __init__(self, data):
        self.data = data
        self.pos = 0
        self.nextevent = None
        self.readevent()
    
    def reset(self):
        self.pos = 0
        self.nextevent = None
        self.readevent()
        return True
    
    def readevent(self):
        if self.pos < len(self.data):
            self.nextevent = self.data[self.pos]
            self.pos += 1
        else:
            self.nextevent = None
        return self.nextevent


def play(song, ins={}, autoenable=True, loop=False): #song events, instruments, whether or not to automatically set/change the channel count
    global stream, eventstart, playing, instruments, ilist, setenabled, autoreset
    stream = StreamWrapper(song)
    playing = True
    autoreset = loop
    instruments = [None for i in range(len(channels))]
    ilist = ins
    setenabled = autoenable
    eventstart = time.ticks_ms()
    timer.init(freq=50, mode=machine.Timer.PERIODIC, callback=audiotick)


def playstream(song, ins={}, autoenable=True, loop=False): #song events, instruments, whether or not to automatically set/change the channel count
    global stream, eventstart, playing, instruments, ilist, setenabled, autoreset
    stream = song
    playing = True
    autoreset = loop
    instruments = [None for i in range(len(channels))]
    ilist = ins
    setenabled = autoenable
    eventstart = time.ticks_ms()
    timer.init(freq=50, mode=machine.Timer.PERIODIC, callback=audiotick)


def playnote(chan, pitch, ins=None):
    global instruments, playing
    if ins == None or pitch == None:
        instruments[chan] = None
        setnote(chan, pitch)
        return
    
    persist = makepersist(chan, pitch, ins, time.ticks_ms())
    if persist == None:
        setnote(chan, pitch+ins[2]) #include detune
        return
    
    instruments[chan] = persist
    if not playing:
        playing = True
        timer.init(freq=50, mode=machine.Timer.PERIODIC, callback=audiotick)

