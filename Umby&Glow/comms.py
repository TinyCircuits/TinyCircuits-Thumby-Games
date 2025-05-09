from machine import Pin, UART

_rxPin = Pin(1, Pin.IN)
_uart = UART(0, baudrate=115200, rx=_rxPin, tx=Pin(0, Pin.OUT), timeout=0,
    txbuf=164, rxbuf=328)
Pin(2, Pin.OUT).value(1)

# Read/write buffers (last byte is checksum)
_echobuf = bytearray(0 for x in range(160))
inbuf = bytearray(0 for x in range(160))
outbuf = bytearray(0 for x in range(160))
_echo = _wait = _uanyc = 0 # Listen counters

@micropython.viper
def _prep_checksum():
    chs = 0
    for i in range(159):
        chs ^= int(outbuf[i])
    outbuf[159] = chs
@micropython.viper
def _check_checksum() -> int:
    chs = 0
    for i in range(159):
        chs ^= int(inbuf[i])
    return 1 if int(inbuf[159]) == chs else 0

@micropython.native
def comms():
    global _echo, _wait, _uanyc
    res = 0
    # Discard echo rebounding back on the wire (from half duplex)
    _echo -= _uart.readinto(_echobuf, _echo) or 0
    if _echo == 0 and _wait > 0: # Read
        _wait -= _uart.readinto(memoryview(inbuf)[160-_wait:], _wait) or 0
        if not _wait and _check_checksum():
            res = 1 # Message recieved
    # Check if it is our turn to send
    if _echo == 0 and _wait == 0 and _rxPin.value:
        # Wipe junk or half messages
        while _uart.any():
            _uart.readinto(_echobuf)
        _prep_checksum()
        _uart.write(outbuf) # Send
        # Ready for echo and then reply
        _echo = _wait = 160
    elif _wait != 0 and not _uart.any():
        _uanyc += 1
        # If noreply 60 times, abort and send again
        if _uanyc > 60:
            _echo = _wait = _uanyc = 0
    return res

