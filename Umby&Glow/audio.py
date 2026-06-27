from machine import PWM, Pin

_OFF = const(0)
_ON = const(32767)
_spkr = PWM(Pin(28))
_audio = _spkr.duty_u16
@micropython.native
def _speaker(freq):
    try:
        _spkr.freq(freq)
    except ValueError:
        pass # ignore out of bound frequencies
_emu = int
try:
    import emulator
    _speaker = _emu = emulator.audio_breakpoint
except ImportError:
    pass
try:
    with open("/thumby.cfg", "r") as f:
        if "audioenabled,0" in f.read():
            _audio = int # Disable audio
except OSError:
    pass
_audio(_OFF)
_signal = None
_duration = _t = 0
_no_interupt = False

@micropython.native
def audio_tick():
    global _t
    if _t == _duration:
        return
    _signal(_t)
    _audio(_ON)
    _t += 1
    if _t == _duration:
        _emu(_OFF)
        _audio(_OFF)

@micropython.native
def play(sound, duration, no_interupt=False):
    global _signal, _duration, _no_interupt, _t
    if _no_interupt and _t != _duration:
        return
    _signal = sound; _duration = duration; _no_interupt = no_interupt; _t = 0
    audio_tick()

@micropython.viper
def rocket_flight(t: int):
    _speaker(1800-t*8)

@micropython.viper
def rocket_bang(t: int):
    _speaker(900 + (t*-155)%1000 if t < 10 else (t*193)%1000)

@micropython.viper
def rocket_kill(t: int):
    _speaker(900+(t*193)%1000)

@micropython.viper
def worm_jump(t: int):
    _speaker(800 if t < 5 else 1500)

@micropython.viper
def grapple_launch(t: int):
    _speaker(1400-t)

@micropython.viper
def death(t: int):
    _speaker(1500 if t < 60 else 1200 if t < 120 else 800)


