import gc


def lcm(nums): #lowest common multiple - only works on positive numbers
    result = 1
    for num in nums:
        a, b = result, num
        while b: #calculate GCD with the Euclidean algorithm
            a, b = b, a % b
        result = num // a * result #convert GCD to LCM
    return result


class Channel:
    def __init__(self, cnum, data, tpb, callback=None):
        self.cnum = cnum #channel number
        self.data = data
        self.tpb = tpb #ticks per beat
        self.callback = callback
        self.reset() #initialize state
    
    def reset(self): #sets up/resets variables used in playback
        self.stack = []
        self.pos = 0
        self.octave = 5
        self.tpn = self.tpb #ticks per note
        self.length = 100
        self.offdelta = self.tpb #note duration in ticks if @length is non-100. May be float.
        self.offtime = 0.0 #time that the prior note turns off
        self.note = None #currently playing note
        self.instrument = None
        
        self.nexttime = 0 #time in ticks of the next event to be processed. Main time source, will always be int for precision.
        self.nextevent = None #currently pending event. Will be [time, event, eventData]. Time is in ticks can be a float. eventData is optional depending on the event type
        self.evtime = 0 #time of the pending event
        self.readevent()
    
    def readevent(self):
        self.nextevent = None
        
        while self.nextevent == None:
            if self.pos >= len(self.data): #end of data
                if self.note != None: #turn off note if it's playing
                    self.nextevent = [self.offtime, 0, self.cnum]
                    self.evtime = self.offtime
                    self.note = None
                    break
                else:
                    return
            
            event = self.data[self.pos]
            if event[0] == b"P": #note on
                if self.note != None and self.length != 100: #the previous note needs to be turned off first
                    self.nextevent = [self.offtime, 0, self.cnum] #insert a note off event
                    self.evtime = self.offtime
                    self.note = None
                    self.pos -= 1 #undo move since the note on wasn't actually processed yet
                else:
                    self.note = self.octave * 12 + event[1]
                    self.offtime = self.nexttime + self.offdelta
                    self.nextevent = [self.nexttime, 1, self.cnum, self.note, self.instrument]
                    self.evtime = self.nexttime
                    self.nexttime += self.tpn
            
            elif event[0] == b"-": #note sustain
                self.offtime = self.nexttime + self.offdelta
                self.nexttime += self.tpn
            
            elif event[0] == b".": #note off/rest
                if self.note != None:
                    self.nextevent = [self.offtime, 0, self.cnum]
                    self.evtime = self.offtime
                    self.note = None
                self.nexttime += self.tpn
            
            elif event[0] == b">": #octave increase
                self.octave += 1
            
            elif event[0] == b"<": #octave decrease
                self.octave -= 1
            
            elif event[0] == b")": #end loop
                if self.stack[-1][1] == 0: #finished looping - will loop infinitely if the starting number was <= 0
                    self.stack.pop()
                else:
                    self.stack[-1][1] -= 1
                    self.pos = self.stack[-1][0]
            
            elif event[0] == b"(": #start loop
                self.stack.append([self.pos, event[1]-1])
                
            elif event[0] == b"o": #octave set
                self.octave = event[1]
            
            elif event[0] == b"n": #notes per beat
                self.tpn = self.tpb // event[1]
                self.offdelta = self.tpn * self.length / 100.0
            
            elif event[0] == b"l": #length
                self.length = event[1]
                self.offdelta = self.tpn * self.length / 100.0
            
            elif event[0] == b"i": #instrument
                self.instrument = event[1]
            
            elif event[0] == b"t": #tempo
                self.nextevent = [self.nexttime, 256, event[1]] #reserving event 256 for tempo change
                self.evtime = self.nexttime
            
            elif event[0] == b"r": #run callback
                if self.callback != None:
                    self.nextevent = [self.nexttime, 3, self.callback, event[1]]
                    self.evtime = self.nexttime
            
            else:
                print(f"[MML] Error - operation \"{chr(ord(self.data[self.pos][0]))}\" is not implemented")
            
            self.pos += 1
        #print(self.nextevent)


def getnum(data, pos):
    num = 0
    while data[pos] not in b"0123456789":
        pos += 1
        if pos >= len(data): return None, pos #EOF
    while data[pos] in b"0123456789":
        num *= 10
        num += int(data[pos])
        pos += 1
        if pos >= len(data): break #EOF
    return num, pos


pitches = {b"c":0,b"d":2,b"e":4,b"f":5,b"g":7,b"a":9,b"b":11}
notenames = ("c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b")

#tokens:
#@something+number - tnilor - "m" also in parsing but not playback
#standalone - <>).-
#note - cdefgabc - "P" is used as a placeholder
#something+number - (

class Stream:
    def __init__(self, raw, callback=None):
        self.channeldata = []
        self.channels = []
        self.tpb = 1
        self.infinite = False #True if the song uses infinite loops
        self.maxchannel = None #highest channel that the song uses
        self._parsemml(raw, callback) #all above variables are populated by this
        self.reset() #initialize state
    
    def reset(self): #sets up/resets variables used in playback
        self.lasttick = 0
        self.realtime = 0.0
        self.tempomul = (60000.0/120.0)/self.tpb #length of each tick in milliseconds - one minute in milliseconds, divided by bpm (default 120), divided by tpb
        self.nextevent = None
        self.eventqueue = [] #this preloads all events on the same timestamp to reduce latency for real-time streaming
        for channel in self.channels:
            channel.reset()
        self.readevent()
        if self.maxchannel != None:
            self.eventqueue.append(self.nextevent) #push back the first event to make room
            self.nextevent = [0, 2, self.maxchannel] #insert a set channel count event at the start
        return True
    
    def readevent(self):
        if len(self.eventqueue):
            self.nextevent = self.eventqueue.pop()
            return self.nextevent
        
        timestamp = None
        
        while True:
            selection = None
            evtime = 0
            for i, channel in enumerate(self.channels):
                if channel.nextevent != None and (selection == None or channel.evtime < evtime): #get the channel with the earliest next event
                    selection = i
                    evtime = channel.evtime
            
            if selection == None: #all channels have reached the end
                endtime = 0
                for channel in self.channels:
                    if channel.nexttime > endtime:
                        endtime = channel.nexttime #get the final time any channel ends
                self.realtime += (endtime-self.lasttick) * self.tempomul
                self.eventqueue.append([self.realtime, None]) #insert dummy event to preserve silence at the end
                self.eventqueue.append(None)
                break
            
            if timestamp != None and evtime != timestamp: #finished processing this tick
                break
            
            if timestamp == None:
                timestamp = evtime
            
            event = self.channels[selection].nextevent
            self.channels[selection].readevent()
            self.realtime += (event[0]-self.lasttick) * self.tempomul
            self.lasttick = event[0]
            
            if event[1] == 256: #tempo change event
                self.tempomul = (60000.0/event[2])/self.tpb
            else:
                event[0] = int(self.realtime) #replace ticks with real time
                self.eventqueue.append(event)
        
        if len(self.eventqueue):
            self.eventqueue.reverse()
            self.nextevent = self.eventqueue.pop()
        else:
            print("[MML] Event queue is empty. This is probably a bug")
            self.nextevent = None
        return self.nextevent
    
    def _parsemml(self, raw, callback): #parse raw mml and create channel objects
        temp = bytes(memoryview(raw)).lower() #convert the input into a common format (bytes). There doesn't seem to be a clean way to do this, but it works. UTF-8 may cause issues as it isn't decoded properly here.
        data = []
        pos = 0
        while pos < len(temp): #first pass - strip out all comments
            if temp[pos] in b";":
                while pos < len(temp) and temp[pos] not in b"\n":
                    pos += 1
            else:
                data.append(bytes(chr(temp[pos]), "ascii")) #for the time being, uPy ignores the encoding and just treats it as UTF-8 anyway
                pos += 1
        
        data.append(b" ") #add padding so looking ahead won't have issues
        del temp
        
        divisions = set()
        tokens = []
        macros = {}
        secnum = None
        sectype = None
        pos = 0
        brackets = 0
        while pos < len(data): #second pass - tokenization
            if data[pos] == b"!": #section start
                if not data[pos+1] in b"cm":
                    print(f"[MML] Syntax error: Unknown command \"!{data[pos+1]}\"")
                    return
                nexttype = data[pos+1]
                num, pos = getnum(data, pos)
                if num == None:
                    print(f"[MML] Syntax error: Missing number after \"!{nexttype}\"")
                    return
                if brackets != 0:
                    print(f"[MML] Syntax error: Mismatched brackets in section !{chr(ord(sectype))}{str(secnum)}")
                    return
                if secnum != None:
                    if sectype == b"c" and len(tokens):
                        self.channeldata.append((secnum, tokens))
                    elif sectype == b"m":
                        macros[secnum] = tokens
                    tokens = []
                secnum = num
                sectype = nexttype
            
            elif data[pos] == b"@":
                command = data[pos+1]
                num, pos = getnum(data, pos)
                if command not in b"tnilomr": #@commands
                    print(f"[MML] Syntax error: Unknown command \"@{chr(ord(command))}\"")
                    return
                if num == None:
                    print(f"[MML] Syntax error: Missing number after \"@{chr(ord(command))}\"")
                    return
                
                if command == b"m": #special handling of macros
                    if not num in macros:
                        print(f"[MML] Syntax error: Macro {str(num)} is used without being defined yet")
                        return
                    tokens += macros[num]
                elif command == b"r" and callback == None:
                    print("[MML] Warning: @r is used but no callback function was provided")
                else:
                    tokens.append((command, num))
                if command == b"n": divisions.add(num)
            
            elif data[pos] in b"<>).-": #standalone symbols
                tokens.append((data[pos],))
                if data[pos] == b")": brackets -= 1
                pos += 1
            
            elif data[pos] in b"cdefgab": #notes
                pitch = pitches[data[pos]]
                pos += 1
                if data[pos] == b"#":
                    pitch += 1
                    pos += 1
                if data[pos] in b"0123456789":
                    tokens.append((b"o", int(data[pos])))
                tokens.append((b"P", pitch))
            
            elif data[pos] == b"(": #loop start
                num, pos = getnum(data, pos)
                if num == None:
                    print("[MML] Syntax error: Missing number after \"(\"")
                    return
                if num == 0:
                    self.infinite = True
                tokens.append((b"(", num))
                brackets += 1
            
            else:
                pos += 1
        
        if brackets != 0:
            print(f"[MML] Syntax error: Mismatched brackets in section !{chr(ord(sectype))}{str(secnum)}")
            return
        if secnum != None:
            if sectype == b"c" and len(tokens):
                self.channeldata.append((secnum, tokens))
            elif sectype == b"m":
                macros[secnum] = tokens
        
        self.tpb = lcm(divisions)
        
        for i in self.channeldata:
            self.channels.append(Channel(i[0], i[1], self.tpb, callback))
            if i[0] > 6:
                print(f"[MML] Warning: Channel {i[0]} won't play audio as it's beyond the valid range of 0-6")
            elif self.maxchannel == None or i[0]+1 > self.maxchannel:
                self.maxchannel = i[0]+1
        
        print(f"[MML] Song needs {self.maxchannel} channel(s) enabled to play properly")


def load(data, callback=None):
    gc.collect()
    oldthreshold = gc.threshold()
    gc.threshold(8000) #aggressive garbage collection to prevent memory fragmentation.
    events = []
    stream = Stream(data, callback=callback)
    if stream.infinite:
        print("[MML] Error: Need to use \"mml.loadstream()\" for infinitely looping songs")
        return events
    while stream.nextevent != None:
        events.append(stream.nextevent)
        stream.readevent()
    gc.collect()
    gc.threshold(oldthreshold) #return gc to previous threshold
    return events


def loadstream(data, callback=None):
    return Stream(data, callback=callback)
