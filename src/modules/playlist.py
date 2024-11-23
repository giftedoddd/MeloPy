import random as rd

class Playlist:

    def __init__(self):
        self.songs = []
        self.current_index = 0

    def add_song(self, song_object):
        self.songs.append(song_object)

    def play(self):
        if self.songs:
            return self.songs[self.current_index]
        return None

    def next(self):
        if self.songs:
            self.current_index = (self.current_index + 1) % len(self.songs)
            return self.play()
        return None

    def previous(self):
        if self.songs:
            self.current_index = (self.current_index - 1) % len(self.songs)
            return self.play()
        return None

    def shuffle(self):
        played = self.songs[:self.current_index + 1:]
        in_queue = self.songs[self.current_index + 1::]
        rd.shuffle(in_queue)
        played.extend(in_queue)
        self.songs.clear()
        self.songs = played.copy()
