from backend.audioPlayer import AudioPlayer
from modules.playlist import Playlist
from modules.server import Server
from modules.song import Song
from modules import explorer
import threading

def process_commands(audioplayer_ :AudioPlayer, playlist_: Playlist, host_ :Server):
    while True:
        command = host_.get_command()
        match command:
            case "play":
                print("playing: " + playlist_.play().artist + " " + playlist_.play().title)
                audioplayer_.set_audio_file(playlist_.play())
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
                print("playing: " + playlist_.play().artist + " " + playlist_.play().title)
                threading.Thread(target=audioplayer_.run).start()

            case "previous":
                audioplayer_.stop()
                audioplayer_.set_audio_file(playlist_.previous())
                print("playing: " + playlist_.play().artist + " " + playlist_.play().title)
                threading.Thread(target=audioplayer_.run).start()

            case "shuffle":
                print("shuffling...")
                playlist_.shuffle()

            case _:
                pass

    # TODO:NEED ANOTHER WAY TO START BACKEND LIKE SUBPROCESS
if __name__ == '__main__':
    file_paths = explorer.watch_dog("/home/giftedodd/Music")

    audioplayer = AudioPlayer()
    playlist = Playlist()
    host = Server(ip="127.0.0.0", port=9353)

    for path in file_paths:
        song = Song(path)
        playlist.add_song(song)

    playlist.shuffle()

    threading.Thread(target=process_commands, args=(audioplayer, playlist, host)).start()
    threading.Thread(target=host.start_server).start()
