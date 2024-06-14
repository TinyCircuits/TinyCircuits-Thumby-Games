from thumby import audio


class MusicPlayer:
    def __init__(self):
        self.song = [(523, 500, 20), (523, 250, 2), (523, 250, 2), (523, 250, 2), (523, 250, 2), (523, 500, 5), (466, 500, 2), (523, 500, 12),
        (523, 250, 2), (523, 250, 2), (523, 250, 2), (523, 250, 2), (523, 500, 5), (466, 500, 2), (523, 500, 12), 
        (523, 250, 2), (523, 250, 2), (523, 250, 2), (523, 250, 2), (523, 500, 5), 
        (392, 250, 2), (392, 250, 2), (392, 250, 4), (392, 250, 2), (392, 250, 2), (392, 250, 4), (392, 250, 2), (392, 250, 2), (392, 250, 4), (392, 250, 4), 
        (523, 500, 12), (392, 250, 12), (523, 250, 2), (523, 250, 2), (587, 250, 2), (659, 250, 2), (698, 250, 2), (783, 500, 20), 
        (783, 250, 2), (783, 250, 2), (831, 250, 2), (932, 250, 2), (1046, 500, 20), 
        (1046, 250, 2), (1046, 250, 2), (1046, 250, 2), (932, 250, 2), (831, 250, 2), (932, 250, 5), (831, 250, 2), (783, 500, 20)]
        self.note_count = 0


        self.frequency_count = 0
        self.duration_count = 1
        self.frames_to_play = 2


        self.frame_count = 0
        
    def play_song(self):
        try:
            if self.frame_count < self.frames_to_play:
                self.frames_to_play = self.song[self.note_count][2]
                audio.play(self.song[self.note_count][self.frequency_count], self.song[self.note_count][self.duration_count])
                self.frame_count += 1
            else:
                audio.stop()
                self.note_count += 1
                self.frame_count = 0
        except IndexError:
            self.note_count = 0
