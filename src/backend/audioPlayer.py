import time
import sounddevice as sd
import soundfile as sf

class AudioPlayer:
    def __init__(self, playback_speed=1.0):
        self.playback_speed = playback_speed
        self.position = 0
        self.playing = False
        self.remaining = None
        self.samplerate = None
        self.channels = None
        self.audio_data = None
        self.tmp_data = None

    # TODO:OK
    def is_playing(self):
        return self.playing

    # TODO: NOT USING THIS DYNAMICALLY PLAYER NEED TO STOPPED TO CHANGE THE PLAYBACK SPEED!
    def set_playback_speed(self, playback_speed):
        if 0 < playback_speed < 5:
            self.playback_speed = playback_speed
            return
        print("Not valid playback speed!")

    #TODO: NOT USED YET
    def get_remaining(self):
        total = self.remaining / self.samplerate
        minutes = int(total // 60)
        seconds = int(total % 60)

    # TODO:NEED TO BE MORE INFORMATIVE ABOUT EXCEPTION AND HANDLE IT BETTER
    def set_audio_file(self, song):
        if self.playing:
            self.stop()
        try:
            self.audio_data, self.samplerate = sf.read(song.file_path, dtype='float64')
            self.channels = self.audio_data.shape[1] if self.audio_data.ndim > 1 else 1
            self.position = 0
            self.tmp_data = self.audio_data
        except Exception as e:
            raise ValueError(f"Error loading audio file: {e}")

    # TODO:OK
    def callback(self, out_data, frames, time_, status):
        if self.position < len(self.audio_data):
            self.remaining = len(self.audio_data) - self.position
            current_block = min(self.remaining, frames)

            out_data[:current_block, :] = self.tmp_data[self.position:self.position + current_block, :]
            self.position += current_block

        else:
            out_data[:frames, :] = 0

    # TODO:COULD BE BETTER, NEED ANOTHER POLISH!
    def run(self):
        self.playing = True
        block_size = 1024

        with sd.OutputStream(samplerate=self.samplerate * self.playback_speed, channels=self.channels, blocksize=block_size,
                             callback=self.callback, latency='low'):
            while self.position < len(self.audio_data) and self.playing:
                time.sleep(0.1)

    # TODO:OK
    def stop(self):
        if self.playing:
            self.playing = False
            self.position = 0

    # TODO:OK
    def pause(self):
        if self.playing:
            self.playing = False
