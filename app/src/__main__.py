from models.audioPlayer import AudioPlayer
from models.playlist import Playlist
from models.server import Server
from models.song import Song
from modules import explorer
import threading

def process_commands(audioplayer_ :AudioPlayer, playlist_: Playlist, host_ :Server):
    def get_remaining():
        while True:
            remaining = audioplayer_.get_remaining()
            if remaining == 1:
                host_.set_tmp_command("next")

    while True:
        threading.Thread(target=get_remaining).start()
        command = host_.get_command()
        match command:
            case "play":
                current = playlist_.play()
                print(f"Playing {current}")
                audioplayer_.set_audio_file(current)
                threading.Thread(target=audioplayer_.run).start()

            case "stop":
                print("stopping!")
                audioplayer_.stop()

            case "pause":
                print("paused.")
                audioplayer_.pause()

            case "resume":
                print("resumed.")
                threading.Thread(target=audioplayer_.run).start()

            case "next":
                audioplayer_.stop()
                audioplayer_.set_audio_file(playlist_.next())
                print(f"Playing {playlist_.play()}")
                threading.Thread(target=audioplayer_.run).start()

            case "previous":
                audioplayer_.stop()
                audioplayer_.set_audio_file(playlist_.previous())
                print(f"Playing {playlist_.play()}")
                threading.Thread(target=audioplayer_.run).start()

            case "shuffle":
                print("shuffling...")
                playlist_.shuffle()

            case _:
                pass

if __name__ == '__main__':
    file_paths = explorer.watch_dog("/home/giftedodd/Music/Imagine Dragon - Hits")

    audioplayer = AudioPlayer()
    playlist = Playlist()
    host = Server(ip="127.0.0.1", port=9353)

    for path in file_paths:
        song = Song(path)
        if not song:
            playlist.add_song(song)

    threading.Thread(target=process_commands, args=(audioplayer, playlist, host)).start()
    threading.Thread(target=host.start_server).start()
