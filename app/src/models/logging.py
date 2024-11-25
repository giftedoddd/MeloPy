from pathlib import Path
import logging

LOG_PATH = Path(__file__).parent.parent.parent.joinpath("logs")

class Logging:
    def __init__(self):
        self.log_files = {
            "AudioPlayer":LOG_PATH.joinpath("audioplayer.log"),
            "Server":LOG_PATH.joinpath("host.log"),
            "Song":LOG_PATH.joinpath("audiofile.log"),
            "Explorer":LOG_PATH.joinpath("explorer.log")
        }
        self.loggers ={}
        self.init_logging()

    def init_logging(self):
        if not LOG_PATH.exists():
            LOG_PATH.mkdir()

        for key, value in self.log_files.items():
            logger = logging.getLogger(key)
            file_handler = logging.FileHandler(filename=value, mode="a", encoding="utf-8")
            formatter = logging.Formatter("%(name)s - %(asctime)s - %(threadName)s - %(funcName)s\n%(message)s")

            logger.addHandler(file_handler)


