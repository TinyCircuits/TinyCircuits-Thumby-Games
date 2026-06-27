# Generative music player
# Note that this version is tidied up and stripped of comments for the arcade.

# Copyright 2022 David Steinberg <david@sonabuzz.com>


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from machine import PWM, Pin, mem32
import random
import gc
from array import array

PWM_CH6_DIV = const(0x4005007c)
PWM_CH6_CC  = const(0x40050084)
PWM_CH6_TOP = const(0x40050088)

pwm = PWM(Pin(28))
pwm.deinit()

pwm_cfgs = [(0x2c9,0xdf20),(0xd3d,0x2c4e),(0x2b8,0xcba3),(0x4b7,0x6ed5),(0x399,0x8919),(0x4c4,0x61b0),(0x2b2,0xa308),
            (0x939,0x2cf8),(0xbdd,0x20ff),(0x3c7,0x61d2),(0x240,0x9b02),(0x765,0x2c84),(0x4be,0x4185),(0xfdd,0x127c),
            (0x2b8,0x65d1),(0x4b7,0x376a),(0x399,0x448c),(0x37a,0x42f4),(0x159,0xa308),(0x158,0x9a54),(0xbdd,0x107f),
            (0xdb,0xd7f8),(0xe0,0xc74c),(0xdc,0xbf88),(0x4be,0x20c2),(0xf1,0x9bc4),(0x2b8,0x32e8),(0x3b7,0x232a),
            (0x219,0x3ac8),(0x57d,0x1534),(0x38f,0x1ede),(0xac,0x9a54),(0xbdd,0x83f),(0x57d,0x10d4),(0xfc,0x5893),
            (0x6e,0xbf88),(0x25f,0x20c2),(0xfab,0x4ad),(0x57,0xcba3),(0x4c,0xdc07),(0x103,0x3cf0),(0xc1,0x4d30),
            (0xd1,0x4347),(0x56,0x9a54),(0xbdd,0x41f),(0x17b,0x1f32),(0x38,0xc74c),(0x37,0xbf88),(0xa5,0x3c42),
            (0xfab,0x256),(0x3a,0x98ba),(0x26,0xdc07),(0x41,0x7969),(0x2ba,0xaab),(0x26,0xb905),(0x2b,0x9a54),
            (0xbdd,0x20f),(0xc0,0x1eca),(0x1c,0xc74c),(0x29,0x8077)]




@micropython.native
def _mk_array2d(typ, lst):
    a = array('O', [None] * len(lst))
    for  i, r in enumerate(lst):
        a[i] = array(typ, r)
    return a


class vararray(array):
    def __init__(self, typ, maxlen, init=None):
        if hasattr(maxlen, '__iter__') or isinstance(maxlen, array):
            maxlen = max([len(i) for i in maxlen])
        super().__init__(typ, [0] * maxlen)
        self.maxlen = maxlen
        if init is None:
            self.set_len(maxlen)
        else:
            self.set_contents(init)

    def set_len(self, l):
        if l > self.maxlen:
            l = self.maxlen
        self._len = l

    @micropython.native
    def __len__(self):
        return self._len

    @micropython.native
    def set_contents(self, lst):
        self.set_len(len(lst))
        for i, v in enumerate(lst):
            self[i] = v

    @micropython.native
    def sample_into(self, lst):
        lstlen = len(lst)
        self.set_len(lstlen)
        for i in range(lstlen):
            j = random.randrange(lstlen)
            self[i] = lst[j]
        
    #@micropython.native
    def __iter__(self):
        i = 0
        while i < self._len:
            yield self[i]
            i += 1


@micropython.native
def sample_into(dst, src):
    srclen = len(src)
    for i in range(len(dst)):
        j = random.randrange(srclen)
        dst[i] = src[j]


def _make_pat_array(typ):
    arr = array('O', [None] * 3)
    for i in range(3):
        arr[i] = array(typ, [0] * 4)
    return arr

@micropython.native
def _copy_pat_array(dst, src):
    for i in range(4):
        dst[0][i] = src[0][i]
        dst[1][i] = src[1][i]
        dst[2][i] = src[2][i]


class MusicPlayer:

    prima_scale = bytearray([0,2,3,5,7,8,10])
    chord_opts = _mk_array2d('b', [[0,3,7],[0,4,7],[0,3,6],[0,4,8],[0,3,7,10],[0,4,7,11],[0,3,6,10],[0,4,8,11]])
    chord_prog_opts = _mk_array2d('b', [[0,4,5,3], [5,1,4,0], [0,4,6,3]])
    bar_patt_opts = _mk_array2d('b', [
        [ 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 2 ],
        [ 0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2, 1, 0, 1, 2, 1 ],
        [ 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2 ],
        [ 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2, 0, 1, 0, 2 ],
        [ 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 2 ],
        [ 0, 0, 1, 2, 0, 0, 1, 2, 0, 0, 1, 2, 0, 0, 1, 2 ],
        [ 0, 0, 1, 1, 0, 0, 2, 2, 0, 0, 1, 1, 0, 0, 2, 2 ],
        [ 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2 ],
        [ 0, 1, 1, 0, 1, 0, 0, 2, 1, 0, 0, 1, 0, 1, 1, 2 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2 ],
        [ 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2, 0, 1, 2, 2 ],
        [ 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 ],
        [ 0, 1, 0, 1, 0, 1, 0, 1, 0, 2, 0, 2, 0, 2, 0, 2 ],
        [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [ 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2 ],
        [ 0, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2 ],
        [ 0, 1, 1, 1, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 2 ],
    ])

    note_dur_sets = _mk_array2d('l', [
        [65536, 32768, 45875, 26214, 131072],
        [65536, 49152, 131072],
        [65536, 65536, 65536, 65536, 32768],
        [65536],
    ])

    note_delay_sets = _mk_array2d('l', [
        [0, 0, 0, 0, 0, 0, 8192, 16384, 32768, 49152],
        [0, 0, 0, 0, 0, 0, 8192, 16384, 32768, 49152, 65536],
        [0, 0, 0, 32768],
        [0],
        [0, 0, 0, 0, 0, 16384, 49152],
        [0, 0, 0, 0, 0, 16384, 49152, 65536],
    ])

    oct_range_opt = array('b', [0, 1, 2])

    StateDelay = const(0)
    StateNoteOn = const(1)
    StateTailRest = const(2)
    StateNoteTie = const(3)

    def __init__(self, frame_rate, seeds):
        self.frame_rate = frame_rate
        self.is_muted = 0
        try:
            with open("/thumby.cfg", "r") as f:
                conf = f.read().split(',')
            for k in range(len(conf)):
                if(conf[k] == "audioenabled"):
                    if int(conf[k+1]) == 0:
                        is_muted = 1
                        break
        except:
            pass

        if seeds is None:
            self.seeds = []
        else:
            self.seeds = seeds
        self.seeds_ind = 0

        self.root_notes = array('b', [0] * 7)
        self.pwm_widths = array('H', [6553, 58981, 39321, 26214])

        self.chord_prog = array('b', [0,0,0,0])
        self.init_chord_prog = array('b', [0,0,0,0])

        self.note_dur_opts = vararray('b', MusicPlayer.note_dur_sets)
        self.note_delay_opts = vararray('b', MusicPlayer.note_delay_sets)

        self.note_dur_patts = _make_pat_array('H')
        self.note_delay_patts = _make_pat_array('H')
        self.note_chord_patts = _make_pat_array('b')
        self.note_oct_patts = _make_pat_array('b')

        self.init_note_dur_patts = _make_pat_array('H')
        self.init_note_delay_patts = _make_pat_array('H')
        self.init_note_chord_patts = _make_pat_array('b')
        self.init_note_oct_patts = _make_pat_array('b')
        
        self.seedfile = open("/Games/Journey3Dg/last_tune.txt", "w")
        self.seedstr = bytearray(11)
        self.seedstr[10] = 10

        self.init()


    @micropython.viper
    def seed_next(self):
        if int(self.seeds_ind) >= int(len(self.seeds)):
            seed = int(random.randrange(0, 16384)) * int(random.randrange(0, 65536))
        else:
            seed = int(self.seeds[int(self.seeds_ind)])
            ptr32(self.seeds_ind)[0] = int(self.seeds_ind) + 1
        random.seed(seed)
        # Save the last seed to a file. If you want to replay a tune, you can grab the seed
        # from the file and pass a list containing it (and any other seeds) to the MusicPlayer constructor.
        seedstr:ptr8 = ptr8(self.seedstr)
        seedstr[9] = (seed % 10) + 0x30
        v:int = int(seed) // 10
        i:int = 8
        while v != 0:
            seedstr[i] = (v % 10) + 0x30
            v //= 10
            i -= 1
        while i != -1:
            seedstr[i] = 0x20
            i -= 1
        self.seedfile.seek(0, 0)
        self.seedfile.write(self.seedstr)
        print('Seed: ', seed)


    @micropython.native
    def init(self):
        self.want_init = False
        self.seed_next()

        self.bpm = random.randrange(74, 110)
        self.beat_samp_cnt = ((self.frame_rate * 3932160 // (self.bpm * 4)) + 32767) >> 16

        self.key_note = random.randrange(12)
        self.key_scale_off = random.randrange(7)

        for c in range(7):
            self.root_notes[c] = self.get_rootnote(c)

        self.beat_num = 0
        self.bar_num = 0
        self.phrase_num = 0

        self.chord_prog_chords = random.choice(MusicPlayer.chord_prog_opts)
        sample_into(self.chord_prog, self.chord_prog_chords)

        self.chord = random.choice(MusicPlayer.chord_opts)
        nds = random.choice(MusicPlayer.note_dur_sets)
        self.note_dur_opts.set_len(len(nds))
        for i in range(len(nds)):
            self.note_dur_opts[i] = int((self.beat_samp_cnt * nds[i]) >> 16)
        nds = random.choice(MusicPlayer.note_delay_sets)
        self.note_delay_opts.set_len(len(nds))
        for i in range(len(nds)):
            self.note_delay_opts[i] = int((self.beat_samp_cnt * nds[i]) >> 16)
        nds = None

        for i in range(3):
            sample_into(self.note_dur_patts[i], self.note_dur_opts)
            sample_into(self.note_delay_patts[i], self.note_delay_opts)
            sample_into(self.note_chord_patts[i], self.chord)
            sample_into(self.note_oct_patts[i], MusicPlayer.oct_range_opt)

        self.rhythm_seq = random.choice(MusicPlayer.bar_patt_opts)
        self.note_chord_seq = random.choice(MusicPlayer.bar_patt_opts)
        self.note_oct_seq = random.choice(MusicPlayer.bar_patt_opts)

        for i in range(4):
            self.init_chord_prog[i] = self.chord_prog[i]

        _copy_pat_array(self.init_note_dur_patts, self.note_dur_patts)
        _copy_pat_array(self.init_note_delay_patts, self.note_delay_patts)
        _copy_pat_array(self.init_note_chord_patts, self.note_chord_patts)
        _copy_pat_array(self.init_note_oct_patts, self.note_oct_patts)

        self.chord_prog_reord = not random.getrandbits(1)
        self.chord_prog_jump = not random.getrandbits(1)


    @micropython.native
    def get_scalenote(self, ind):
        return (MusicPlayer.prima_scale[(self.key_scale_off + ind) % 7] - MusicPlayer.prima_scale[self.key_scale_off]) % 12

    @micropython.native
    def get_rootnote(self, chord_ind):
        return self.key_note + self.get_scalenote(chord_ind)

    @micropython.native
    def get_current_note(self):
        root_note = self.root_notes[self.chord_prog[self.bar_num % 4]]
        chord_note = self.note_chord_patts[self.note_chord_seq[self.bar_num]][self.beat_num]
        note_oct = self.note_oct_patts[self.note_oct_seq[self.bar_num]][self.beat_num]
        bar_note = root_note + (12 * note_oct) + chord_note
        return bar_note

    def set_first_note(self):
        self.beat_samp_rem = self.beat_samp_cnt
        self.current_note = self.get_current_note()
        if self.note_delay_patts[self.rhythm_seq[0]][0] == 0:
            note_dur = self.note_dur_patts[self.rhythm_seq[0]][0]
            if note_dur != 0:
                self.note_on(self.current_note)
                self.state = MusicPlayer.StateNoteOn
            else:
                self.note_off()
                self.state = MusicPlayer.StateTailRest
            self.state_samp_rem = min(self.beat_samp_rem, note_dur)
            self.note_tie_samps = note_dur - self.state_samp_rem
        else:
            self.note_off()
            self.state_samp_rem = self.note_delay_patts[self.rhythm_seq[0]][0]
            self.note_tie_samps = 0
            self.state = MusicPlayer.StateDelay
        self.set_note_mod(self.pwm_widths[0])


    @micropython.native
    def update_state_notetie(self):
        if self.note_deltm != 0:
            self.note_off()
            self.state = MusicPlayer.StateDelay
            self.state_samp_rem = self.note_deltm
        else:
            self.set_note_mod(self.pwm_widths[self.beat_num])
            self.note_on(self.current_note)
            self.state = MusicPlayer.StateNoteOn
            note_dur = self.note_dur_patts[self.rhythm_seq[self.bar_num]][self.beat_num]
            if note_dur != 0:
                self.note_on(self.current_note)
                self.state = MusicPlayer.StateNoteOn
                self.state_samp_rem = min(self.beat_samp_rem, note_dur)
                self.note_tie_samps = note_dur - self.state_samp_rem
            else:
                self.note_off()
                self.state = MusicPlayer.StateTailRest
                self.state_samp_rem = self.beat_samp_rem
                self.note_tie_samps = 0

    @micropython.native
    def update_state_delay(self):
        self.set_note_mod(self.pwm_widths[self.beat_num])
        note_dur = self.note_dur_patts[self.rhythm_seq[self.bar_num]][self.beat_num]
        if note_dur != 0:
            self.note_on(self.current_note)
            self.state = MusicPlayer.StateNoteOn
            self.state_samp_rem = min(self.beat_samp_rem, note_dur)
            self.note_tie_samps = note_dur - self.state_samp_rem
        else:
            self.note_off()
            self.state = MusicPlayer.StateTailRest
            self.state_samp_rem = self.beat_samp_rem
            self.note_tie_samps = 0

    @micropython.native
    def update_state_phrase_complete(self):
        self.bar_num = 0
        self.note_tie_samps = 0

        self.phrase_num += 1

        if self.chord_prog_reord and random.randrange(3) == 0:
            j = random.randrange(len(self.chord_prog)-1) + 1
            k = random.randrange(len(self.chord_prog)-1) + 1
            self.chord_prog[j], self.chord_prog[k] = self.chord_prog[k], self.chord_prog[j]
        if self.chord_prog_jump and random.randrange(3) == 0:
            j = random.randrange(len(self.chord_prog)-1) + 1
            self.chord_prog[j] = (self.chord_prog[j] + random.choice([-5, 5])) % 7
        for i in range(random.randrange(3)):
            b1 = random.randrange(3)
            b2 = random.randrange(3)
            j = random.randrange(4)
            v = random.choice(self.chord)
            self.note_chord_patts[b1][j] = v
            self.note_chord_patts[b2][j] = v
        for i in range(random.randrange(3)):
            b1 = random.randrange(3)
            b2 = random.randrange(3)
            j = random.randrange(4)
            v = random.randrange(3)
            self.note_oct_patts[b1][j] = v
            self.note_oct_patts[b2][j] = v
        for i in range(random.randrange(3)):
            j = random.randrange(4)
            k = random.randrange(len(self.note_delay_patts))
            v = random.choice(self.note_delay_opts)
            self.note_delay_patts[k][j] = v
            if v != 0:
                if self.note_delay_patts[k][j-1] != 0:
                    self.note_delay_patts[k][j-1] = 0
                if self.note_delay_patts[k][(j+1)%4] != 0:
                    self.note_delay_patts[k][(j+1)%4] = 0

        if self.phrase_num % 2 == 0:
            if random.randrange(3) == 0:
                self.rhythm_seq = random.choice(MusicPlayer.bar_patt_opts)
            if random.randrange(3) == 0:
                self.note_chord_seq = random.choice(MusicPlayer.bar_patt_opts)
            if random.randrange(3) == 0:
                self.note_oct_seq = random.choice(MusicPlayer.bar_patt_opts)
        if self.phrase_num % 4 == 0:
            if random.randrange(3) == 0:
                nds = random.choice(MusicPlayer.note_dur_sets)
                self.note_dur_opts.set_len(len(nds))
                for i in range(len(nds)):
                    self.note_dur_opts[i] = int((self.beat_samp_cnt * nds[i]) >> 16)
                nds = None
            if random.randrange(3) == 0:
                nds = random.choice(MusicPlayer.note_delay_sets)
                self.note_delay_opts.set_len(len(nds))
                for i in range(len(nds)):
                    self.note_delay_opts[i] = int((self.beat_samp_cnt * nds[i]) >> 16)
                nds = None

        if self.phrase_num % 8 == 0:
            if random.randrange(3) != 0:
                _copy_pat_array(self.note_chord_patts, self.init_note_chord_patts)
                _copy_pat_array(self.note_oct_patts, self.init_note_oct_patts)
            if random.randrange(3) != 0:
                _copy_pat_array(self.note_dur_patts, self.init_note_dur_patts)
                _copy_pat_array(self.note_delay_patts, self.init_note_delay_patts)
                for i in range(4):
                    self.chord_prog[i] = self.init_chord_prog[i]
        if self.phrase_num % 16 == 0:
            self.phrase_num = 0
            self.chord = random.choice(MusicPlayer.chord_opts)

    @micropython.native
    def update_state_next_note(self):
        self.current_note = self.get_current_note()
        self.beat_samp_rem = self.beat_samp_cnt
        if self.note_delay_patts[self.rhythm_seq[self.bar_num]][self.beat_num] == 0:
            self.set_note_mod(self.pwm_widths[self.beat_num])
            note_dur = self.note_dur_patts[self.rhythm_seq[self.bar_num]][self.beat_num]
            if note_dur != 0:
                self.note_on(self.current_note)
                self.state = MusicPlayer.StateNoteOn
                self.state_samp_rem = min(self.beat_samp_rem, note_dur)
                self.note_tie_samps = note_dur - self.state_samp_rem
            else:
                self.note_off()
                self.state = MusicPlayer.StateTailRest
                self.state_samp_rem = self.beat_samp_rem
                self.note_tie_samps = 0
        else:
            self.note_deltm = self.note_delay_patts[self.rhythm_seq[self.bar_num]][self.beat_num]
            if self.note_tie_samps != 0:
                self.state_samp_rem = min(self.note_tie_samps, self.note_deltm)
                self.note_deltm -= self.state_samp_rem
                self.state = MusicPlayer.StateNoteTie
            else:
                self.note_off()
                self.state = MusicPlayer.StateDelay
                self.state_samp_rem = self.note_deltm

    @micropython.native
    def update_state(self):
        if self.state == MusicPlayer.StateNoteTie:
            self.update_state_notetie()
            return

        if self.state == MusicPlayer.StateDelay:
            self.update_state_delay()
            return

        if (self.state == MusicPlayer.StateNoteOn) and (self.beat_samp_rem != 0):
            self.note_off()
            self.state = MusicPlayer.StateTailRest
            self.state_samp_rem = self.beat_samp_rem
            self.note_tie_samps = 0
            return

        self.beat_num += 1
        if self.beat_num == 4:
            self.beat_num = 0
            self.bar_num += 1

            if self.want_init:
                self.want_init = False
                self.init()
                self.note_off()
                self.state = MusicPlayer.StateDelay
                self.beat_samp_rem = self.beat_samp_cnt * 3
                self.current_note = self.get_current_note()
                self.state_samp_rem = self.note_delay_patts[self.rhythm_seq[0]][0] + (self.beat_samp_cnt * 2)
                return

            i = random.randrange(len(self.pwm_widths))
            j = random.randrange(len(self.pwm_widths))
            self.pwm_widths[i], self.pwm_widths[j] = self.pwm_widths[j], self.pwm_widths[i]

            if self.bar_num % 8 == 0:
                for i in range(random.randrange(2)):
                    k = random.randrange(len(self.note_dur_patts))
                    j = random.randrange(4)
                    self.note_dur_patts[k][j] = random.choice(self.note_dur_opts)

            if self.bar_num == 16:
                self.update_state_phrase_complete()

        self.update_state_next_note()

    @micropython.native
    def frame(self):
        if self.state_samp_rem != 0:
            self.state_samp_rem -= 1
            self.beat_samp_rem -= 1
        if self.state_samp_rem == 0:
            self.update_state()

    def next_tune(self):
        self.want_init = True

    @micropython.native
    def note_on(self, note):
        self.last_note = note
        if self.is_muted:
            pwm.duty_u16(0)
        else:
            div, top = pwm_cfgs[note]
            mem32[PWM_CH6_DIV] = div
            mem32[PWM_CH6_TOP] = top
            pwm.duty_u16(self.last_duty)

    @micropython.native
    def note_off(self):
        pwm.duty_u16(0)

    @micropython.native
    def set_note_mod(self, val):
        self.last_duty = val
        if self.is_muted:
            pwm.duty_u16(0)
        else:
            pwm.duty_u16(self.last_duty)

    def start(self):
        self.last_duty = 0x7fff
        pwm.duty_u16(0)
        self.set_first_note()

    def stop(self):
        pwm.deinit()

    def toggle_mute(self):
        if self.is_muted:
            self.is_muted = False
            div, top = pwm_cfgs[self.last_note]
            mem32[PWM_CH6_DIV] = div
            mem32[PWM_CH6_TOP] = top
            pwm.duty_u16(self.last_duty)
        else:
            self.is_muted = True
            pwm.duty_u16(0)

