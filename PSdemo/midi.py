import struct
import gc


#Useful resources:
#http://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html
#https://github.com/colxi/midi-parser-js/wiki/MIDI-File-Format-Specifications
#https://www.csie.ntu.edu.tw/~r92092/ref/midi/
#http://www.shikadi.net/moddingwiki/MID_Format
#http://midi.teragonaudio.com/tech/midispec.htm


def vlq(data): #takes a file-like object, returns an int.
    total = 0
    nextbyte = ord(data.read(1))
    while nextbyte >= 128: #Never had a problem, but not fully compliant as some files may expect this to be signed, and MIDI specifies that these can't be more than 4 bytes.
        total += nextbyte & 127
        total <<= 7
        nextbyte = ord(data.read(1))
    total += nextbyte
    return total


class MidiTrack:
    def __init__(self, data, pos=None):
        if pos == None: pos = data.tell()
        self.data = data
        self.pos = pos
        self.nexttime = 0 #time in ticks of the next event. None if there is no next event.
        self.status = 0 #running status, stores the last event in case it's omitted
        
        data.seek(self.pos)
        if not data.read(4) == b"MTrk":
            print(f"[MIDI] Warning: Track header not found")
        tracksize = struct.unpack(">I", data.read(4))[0]
        print(f"[MIDI] Track at offset {self.pos}, {tracksize} bytes")
        
        self.nexttime += vlq(data)
        self.pos = self.data.tell()
        self.data.seek(pos + tracksize + 8) #seek to the end of the track
        
        self.defaults = (self.nexttime, self.pos)
    
    def reset(self):
        self.status = 0
        self.nexttime = self.defaults[0]
        self.pos = self.defaults[1]
    
    def readevent(self): #returns the next event as ((type, channel, eventData), timestamp). May return None if the next event is irrelevant or nonexistent.
        if self.nexttime == None: return None #just in case
        
        self.data.seek(self.pos)
        event = ord(self.data.read(1))
        if event < 128: #reuses the previous event - this is actually the first byte
            firstbyte = event
            event = self.status
        elif event < 0xf0: #running status is not affected by sysex and meta events
            firstbyte = ord(self.data.read(1)) #don't read the first byte on sysex and meta events because they're structured differently
            self.status = event
        
        finalevent = None
        etype = (event & 0x7f) >> 4
        echan = event & 0b1111
        
        if event == 0xff: #meta event
            metatype = ord(self.data.read(1))
            evlen = vlq(self.data)
            evdata = self.data.read(evlen)
            if metatype == 0x2f: #end of track event
                self.nexttime = None
                return None
            elif metatype == 0x51: #set tempo
                finalevent = ((256, struct.unpack(">I", b"\0" + evdata)[0]), self.nexttime) #reserving illegal event type 256 for tempo change
        
        elif etype == 7: #sysex event
            evlen = vlq(self.data)
            evdata = self.data.read(evlen)
        
        elif etype == 4 or etype == 5: #single byte events
            finalevent = ((etype, echan, firstbyte), self.nexttime)
        
        else: #two-byte events
            secondbyte = ord(self.data.read(1))
            if etype == 1 and secondbyte == 0: etype = 0 #turn "note on at velocity 0" into note off events to simplify processing
            if (etype == 0 or etype == 1) and echan == 9: finalevent = None #since it's not implemented yet, discard percussion for now to lighten resource usage
            else: finalevent = ((etype, echan, firstbyte, secondbyte), self.nexttime)
        
        self.nexttime += vlq(self.data) #get time of next event
        self.pos = self.data.tell()
        return finalevent


class MappedStream:
    def __init__(self, data, mute=None, solo=None, reserve={}, automap=True, callbacks={}):
        self.data = data
        self.mute = mute
        self.solo = solo
        self.reserve = reserve
        self.automap = automap
        self.callbacks = callbacks
        
        if not data.read(4) == b"MThd": #header parsing
            print("[MIDI] Error loading song: MIDI header not found.")
        
        headersize = struct.unpack(">I", data.read(4))[0]
        if not headersize == 6: print("[MIDI] Warning: MIDI Header is abnormally sized")
        fileformat, trackcount, self.tpb = struct.unpack_from(">HHH", data.read(headersize))
        
        print(f"[MIDI] Loading type {fileformat} file with {trackcount} track(s)")
        if self.tpb & 0x8000: print("[MIDI] Error loading song: SMPTE/TPFPS timing is not supported.")
        
        self.tracks = [MidiTrack(data) for i in range(trackcount)]
        
        self.lasttick = 0
        self.realtime = 0.0
        self.tempomul = (500000/1000.0)/self.tpb #500000 microseconds per beat, scaled to milliseconds, divided by ticks per beat, to get the length in milliseconds of each tick.
        
        self.boundinstruments = {} #instrument:channel
        for i in reserve:
            for j in reserve[i]:
                self.boundinstruments[j] = i
        
        self.outputs = [None for i in range(7)] #status of physical channels. None if free, (midiChannel, midiNote, instrument, startTime) if playing anything
        self.instruments = [0 for i in range(16)] #current instrument assigned to each midi channel
        self.maxchannels = 0 #how many channels at most were needed to play the song
        self.notenoughchannels = False
        
        self.nextevent = None
        self.eventqueue = [] #this preloads all events on the same timestamp to reduce latency for real-time streaming
        self.readevent()
    
    def reset(self): #start reading from the beginning again
        for i in self.tracks:
            i.reset()
        self.lasttick = 0
        self.realtime = 0.0
        self.tempomul = (500000/1000.0)/self.tpb
        self.outputs = [None for i in range(7)]
        self.instruments = [0 for i in range(16)]
        self.eventqueue = []
        self.readevent()
        return True
    
    def readevent(self):
        if len(self.eventqueue):
            self.nextevent = self.eventqueue.pop()
            return self.nextevent
        
        timestamp = None
        
        while True:
            selection = None
            nexttime = 0
            for i, track in enumerate(self.tracks):
                if track.nexttime != None and (selection == None or track.nexttime < nexttime): #get the track with the earliest next event
                    selection = i
                    nexttime = track.nexttime
            
            if selection == None: #finished if all tracks have reached the end
                self.eventqueue.append(None)
                break
            
            if timestamp != None and timestamp != nexttime:
                break
            
            event = self.tracks[selection].readevent()
            if event == None: continue #event is irrelevant/nonexistent
            
            self.realtime += (event[1]-self.lasttick) * self.tempomul
            self.lasttick = event[1]
            if event[0][0] == 256: #tempo change event
                self.tempomul = (event[0][1]/1000.0)/self.tpb
                
            elif event[0][0] == 1: #note on event
                if self.solo != None and self.instruments[event[0][1]] not in self.solo: continue #do not play unwanted instruments
                if self.mute != None and self.instruments[event[0][1]] in self.mute: continue #do not play muted instruments
                
                if self.instruments[event[0][1]] in self.callbacks:
                    self.eventqueue.append((int(self.realtime), 3, self.callbacks[self.instruments[event[0][1]]], event[0][2]))
                    if timestamp == None: timestamp = nexttime
                    continue
                
                selection = None
                if not self.automap: #if MIDI channels correspond to physical channels
                    if event[0][1] < 7: selection = event[0][1]
                
                elif self.instruments[event[0][1]] in self.boundinstruments: #if this instrument is bound to a physical channel
                    selection = self.boundinstruments[self.instruments[event[0][1]]]
                
                else: #this note is not bound to a specific channel
                    for i in range(7): #check if this note is already playing (midi channel, pitch)
                        if i in self.reserve: continue #don't touch reserved channels
                        if self.outputs[i] != None and self.outputs[i][0] == event[0][1] and self.outputs[i][1] == event[0][2]: #already playing - keep the same channel
                            selection = i
                            break
                    
                    if selection == None:
                        oldest = None
                        for i in range(7): #check for a free channel
                            if i in self.reserve: continue #don't touch reserved channels
                            if self.outputs[i] == None:
                                selection = i
                                break
                            elif oldest == None or self.outputs[i][3] < self.outputs[oldest][3]:
                                oldest = i
                        else: #there wasn't a free channel - use the channel that's gone the longest without changing
                            selection = oldest
                            self.notenoughchannels = True
                
                if selection == None: continue #there was no suitable channel - this note cannot be played
                
                #at this point, the note is valid and a channel has been selected.
                self.outputs[selection] = (event[0][1], event[0][2], self.instruments[event[0][1]], event[1])
                if selection > self.maxchannels: self.maxchannels = selection
                self.eventqueue.append((int(self.realtime), 1, selection, event[0][2], self.instruments[event[0][1]]))
                if timestamp == None: timestamp = nexttime
                continue
            
            elif event[0][0] == 0: #note off event
                for i in range(7): #check if this note is playing
                    if self.outputs[i] != None and self.outputs[i][0] == event[0][1] and self.outputs[i][1] == event[0][2]: #it's playing - turn it off
                        self.outputs[i] = None
                        self.eventqueue.append((int(self.realtime), 0, i))
                        continue
            
            elif event[0][0] == 4: #instrument change
                self.instruments[event[0][1]] = event[0][2]
        
        if len(self.eventqueue):
            self.eventqueue.reverse()
            self.nextevent = self.eventqueue.pop()
        else:
            print("[MIDI] Event queue is empty. This is probably a bug")
            self.nextevent = None
        return self.nextevent


#mute/solo are iterables of instrument numbers, reserve is a dict of physicalChannelNumber:(bound instrument numbers), callbacks is a dict of {instrumentNum:func} where func is called with the note number while playing
def load(data, mute=None, solo=None, reserve={}, automap=True, callbacks={}): #load an entire song into a list, like the original monolithic loader
    gc.collect()
    gc.threshold(8000) #aggressive garbage collection to prevent memory fragmentation. Anything from 8000-16000 seems like a good balance, nearly as fast while effectively mitigating it.
    events = [(0, 2, 7)] #start with a channel count event
    stream = MappedStream(data, mute=mute, solo=solo, reserve=reserve, automap=automap, callbacks=callbacks)
    while stream.nextevent != None:
        events.append(stream.nextevent)
        stream.readevent()
    events[0] = (0, 2, stream.maxchannels+1) #set the starting channel count to the max needed
    if stream.notenoughchannels: print("[MIDI] Warning: Song uses more channels than are available. Some notes may be cut off.")
    print(f"[MIDI] Song needs {stream.maxchannels+1} channel(s) to play.")
    gc.threshold(-1)
    gc.collect()
    return events


def loadstream(data, mute=None, solo=None, reserve={}, automap=True, callbacks={}):
    return MappedStream(data, mute=mute, solo=solo, reserve=reserve, automap=automap, callbacks=callbacks)

