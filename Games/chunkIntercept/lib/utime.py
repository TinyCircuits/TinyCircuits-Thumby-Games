import time

start_time_ns = time.monotonic_ns()
def ticks_ms():
    return (time.monotonic_ns() - start_time_ns) / 1000000
def ticks_us():
    return (time.monotonic_ns() - start_time_ns) / 1000
def ticks_diff(t0, t1):
    return t1 - t0
def sleep_ms(ms):
    time.sleep(ms / 1000)