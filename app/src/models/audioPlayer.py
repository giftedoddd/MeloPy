import sounddevice as sd
import soundfile as sf
import time

class AudioPlayer:
    """
    AudioPlayer class to handle audiodata, buffering and playback.
    """
    def __init__(self, playback_speed=1.0):
        self.__playback_speed = playback_speed        # Playback speed default=1.0.
        self.__position = 0                           # Stores current position.
        self.__playing = False                        # Boolean variable for playing state.
        self.__remaining = None                       # Remaining time.
        self.__samplerate = None                      # Stores Audiodata samplerate.
        self.__channels = None                        # Stores channels.
        self.__audio_data = None                      # Stores Audiodata.

    def playing(self) -> bool:
        """
        Returns current state of output stream.\n
        Args:none
        Returns:boolean
        """
        return self.__playing

    def set_playback_speed(self, playback_speed: float) -> None:
        """
        Sets playback speed.\n
        Args:float
        Returns:none
        """
        if 0 < playback_speed < 5:
            self.__playback_speed = playback_speed

    def get_remaining(self) -> int:
        """
        Returns remaining time of audiodata in seconds.\n
        Args: none
        Returns: int
        """
        time.sleep(2)
        if self.playing:
            try:
                total = self.__remaining // self.__samplerate
            except TypeError:
                total = 0
            return total

    def set_audio_file(self, song_path) -> None:
        """
        Gets a song path and extracts the audiodata, samplerate, channel.\n
        Args: str
        Returns: none
        """
        if self.playing:
            self.stop()
        try:
            self.__audio_data, self.__samplerate = sf.read(song_path.file_path, dtype='float64')
            self.__channels = self.__audio_data.shape[1] if self.__audio_data.ndim > 1 else 1
            self.__position = 0
        except Exception as e:
            raise ValueError(f"Error loading audio file: {e}")

    def __callback(self, out_data, frames, time_, status) -> None:
        """
        Handles positioning and remaining data.\n
        Args: none
        Returns: none
        """
        if self.__position < len(self.__audio_data):
            self.__remaining = len(self.__audio_data) - self.__position
            current_block = min(self.__remaining, frames)

            out_data[:current_block, :] = self.__audio_data[self.__position:self.__position + current_block, :]
            self.__position += current_block

        else:
            out_data[:frames, :] = 0

    def run(self) -> None:
        """
        Runs the output stream and sleeps every 0.1 secs to let the thread look for if there is any other commands to do.\n
        Args: none
        Returns: none
        """
        self.__playing = True
        block_size = 1024

        with sd.OutputStream(samplerate=self.__samplerate * self.__playback_speed, channels=self.__channels, blocksize=block_size,
                             callback=self.__callback, latency='low'):
            while self.__position < len(self.__audio_data) and self.__playing:
                time.sleep(0.1)


    def stop(self) -> None:
        """
        Stops output stream and restore the position.\n
        Args: none
        Returns: none
        """
        if self.__playing:
            self.__playing = False
            self.__position = 0


    def pause(self) -> None:
        """
        Stops output stream without restoring the position.\n
        Args: none
        Returns: none
        """
        if self.__playing:
            self.__playing = False
