import random as rd

class Playlist:
    """PlayList class for manage queue and player behaviors."""
    def __init__(self):
        self.songs = []
        self.current_index = 0

    def add_song(self, song_object:object) -> None:
        """Gets a song object as argument per call to add it to the queue."""
        self.songs.append(song_object)

    def play(self) -> object:
        """Returns a song object of current position."""
        if self.songs:
            return self.songs[self.current_index]

    def next(self) -> object:
        """Increase index position by 1 and return song object of that position."""
        if self.songs:
            self.current_index = (self.current_index + 1) % len(self.songs)
            return self.play()

    def previous(self) -> object:
        """Decrease index position by 1 and return song object of that position."""
        if self.songs:
            self.current_index = (self.current_index - 1) % len(self.songs)
            return self.play()
        return None

    def shuffle(self) -> None:
        """Shuffles the queue from current position index to the last, objects before current index will be at same
         position as before"""
        played = self.songs[:self.current_index + 1:]
        in_queue = self.songs[self.current_index + 1::]
        rd.shuffle(in_queue)
        played.extend(in_queue)
        self.songs.clear()
        self.songs = played.copy()
