# Audio class, from which the audio namespace is defined.
class AudioClass:
    def __init__(self):
        pass

    # Set the audio to disabled, mid, or high output
    def setEnabled(self, setting = 1):
        pass

    # Stop audio.
    def stop(self, dummy = None): # I have no idea why it needs the second dummy argument. The timer interrupt won't work without it. Shouldn't affect functionality whatsoever.
        pass

    # Set the frequency and duty of the PWM audio if currently enabled.
    def set(self, freq):
        pass

    # Play a given frequency for the duration with a given duty cycle for PWM audio. Returns before audio is done playing.
    def play(self, freq, duration):
        pass

    # Play a given frequency for the duration with a given duty cycle for PWM audio. Returns after audio is done playing.
    def playBlocking(self, freq, duration):
        pass
            
# Audio instantiation
audio = AudioClass()
