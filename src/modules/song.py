from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.oggopus import OggOpus
from mutagen.asf import ASF
from mutagen.wave import WAVE
import mutagen
import os

class Song:
    def __init__(self, file_path):
        self.file_path = file_path
        self.album = None
        self.artist = None
        self.genre = None
        self.title = None
        self.date = None
        self.cover = None
        self.size = None
        self.get_track_info()

    def __repr__(self):
        return f"Album:{self.album} Artist:{self.artist} Title:{self.title}"

    def get_track_info(self):
        try:
            def extract_info(file_format, file):
                if file_format == "aac" or file_format == "m4a":
                    self.artist = file.tags.get("\xa9ART", [None])[0]
                    self.title = file.tags.get("\xa9nam", [None])[0]
                    self.album = file.tags.get("\xa9alb", [None])[0]
                    self.date = file.tags.get("\xa9day", [None])[0]
                    self.genre = file.tags.get("\xa9gen", [None])[0]
                    return

                self.artist = file.tags.get("artist", [None])[0]
                self.title = file.tags.get("title", [None])[0]
                self.album = file.tags.get("album", [None])[0]
                self.date = file.tags.get("date", [None])[0]
                self.genre = file.tags.get("genre", [None])[0]

            file_extension = self.file_path.split(".")[-1].lower()
            self.size = "%.2f" %(os.path.getsize(self.file_path) / 1000000)

            match file_extension:
                case "mp3":
                    mp3_audio_file = MP3(self.file_path)
                    if "APIC:" in mp3_audio_file:
                        self.cover = mp3_audio_file["APIC:"].data

                    self.artist = mp3_audio_file.get("TPE1", [None])[0]
                    self.title = mp3_audio_file.get("TIT2", [None])[0]
                    self.album = mp3_audio_file.get("TALB", [None])[0]
                    self.date = mp3_audio_file.get("TDRC", [None])[0]
                    self.genre = mp3_audio_file.get("TCON", [None])[0]

                case "flac":
                    flac_audio_file = FLAC(self.file_path)
                    covers = flac_audio_file.pictures
                    for cover in covers:
                        if cover.type == 3:
                            self.cover = cover.data
                            break

                    self.artist = flac_audio_file.get("artist", [None])[0]
                    self.title = flac_audio_file.get("title", [None])[0]
                    self.album = flac_audio_file.get("album", [None])[0]
                    self.date = flac_audio_file.get("date", [None])[0]
                    self.genre = flac_audio_file.get("genre", [None])[0]

                case "wav":
                    wav_audio_file = WAVE(self.file_path)
                    if 'APIC:' in wav_audio_file:
                        self.cover = wav_audio_file['APIC:'].data
                    extract_info(file_format="wav", file=wav_audio_file)

                case "m4a":
                    m4a_audio_file = mutagen.File(self.file_path)
                    if m4a_audio_file is not 0 and isinstance(m4a_audio_file.tags, mutagen.mp4.MP4Tags):
                        if 'covr' in m4a_audio_file.tags:
                            self.cover = m4a_audio_file.tags['covr'][0]

                        extract_info(file_format="m4a", file=m4a_audio_file)

                case "ogg":
                    ogg_audio_file = OggVorbis(self.file_path)
                    if 'metadata' in ogg_audio_file:
                        if 'metadata_block_picture' in ogg_audio_file['metadata']:
                            self.cover = ogg_audio_file['metadata']['metadata_block_picture'][0]

                        extract_info(file_format="ogg", file=ogg_audio_file)

                case "opus":
                    opus_audio_file = OggOpus(self.file_path)
                    if 'metadata' in opus_audio_file:
                        if 'metadata_block_picture' in opus_audio_file['metadata']:
                            self.cover = opus_audio_file['metadata']['metadata_block_picture'][0]

                        extract_info(file_format="opus", file=opus_audio_file)

                case "aac":
                    aac_audio_file = mutagen.File(self.file_path)
                    if aac_audio_file is not 0 and isinstance(aac_audio_file.tags, mutagen.mp4.MP4Tags):
                        if 'covr' in aac_audio_file.tags:
                            self.cover = aac_audio_file.tags['covr'][0]

                        extract_info(file_format="aac", file=aac_audio_file)

                case "wma":
                    wma_audio_file = ASF(self.file_path)
                    if 'WM/Picture' in wma_audio_file:
                        self.cover = wma_audio_file['WM/Picture'].value

                    self.artist = wma_audio_file.tags.get("WM/AlbumArtist", [None])[0]
                    self.title = wma_audio_file.tags.get("Title", [None])[0]
                    self.album = wma_audio_file.tags.get("WM/AlbumTitle", [None])[0]
                    self.date = wma_audio_file.tags.get("WM/Year", [None])[0]
                    self.genre = wma_audio_file.tags.get("WM/Genre", [None])[0]
        except Exception:
            return Song