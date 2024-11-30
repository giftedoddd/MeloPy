from concurrent.futures import ThreadPoolExecutor
import pathlib, re, os

PATTERN = r"\.(flac|wav|mp3|opus|ogg|m4a|aac|wma)$"
PARENT_PATH = pathlib.Path(__file__).parent.parent.parent

def watch_dog(dir_path:str) -> list:
    """Gets a directory path as argument that contains audio files and checks if there is any filesystem changes.if it
    does not detect any modification since last run, simply read paths from database by calling get_files function for
    faster loading speed otherwise, it with call get_files function to rewrite database again."""

    db_path = PARENT_PATH.joinpath("db/.stat")
    modify_date = pathlib.Path(dir_path).stat().st_mtime

    if not PARENT_PATH.joinpath("db").exists():
        PARENT_PATH.joinpath("db").mkdir()

    try:

        with db_path.open("r") as stat_file:
            path_and_date = stat_file.readlines()
        is_same = path_and_date[0].replace("\n", "") == dir_path and path_and_date[1] == str(modify_date)
        if not is_same:
            raise FileNotFoundError
        return get_files(dir_path=dir_path, condition=is_same)

    except FileNotFoundError:
        with db_path.open("w") as stat_file:
            stat_file.write(f"{dir_path}\n{modify_date}")
        return get_files(dir_path=dir_path, condition=False)

def get_files(dir_path:str, condition:bool) -> list:
    """Gets a directory path and boolean condition to choose to read from database or read files and rewrite database.
    the writing process uses threading pool to read from files and write to database as fast as possible.
    reading process simply just read from database and return a list that contains abs_path of founded audio files"""

    db_path = PARENT_PATH.joinpath("db/.path")
    paths_list = []

    def execute_workers(path) -> None:
        """Recursive multithreaded deep file scanning function"""
        directories = os.scandir(path)
        with db_path.open("a") as paths_db:
            for directory in directories:
                if directory.is_dir():
                    execute_workers(directory)
                    continue
                if bool(re.search(PATTERN, directory.path, re.IGNORECASE)):
                    paths_list.append(directory.path)
                    paths_db.write(directory.path + "\n")

    if not condition:
        if db_path.exists():
            os.remove(db_path)
        with ThreadPoolExecutor() as exe:
            exe.submit(execute_workers, dir_path)
        return paths_list
    with db_path.open("r") as paths_file:
        return [path.replace("\n", "") for path in paths_file.readlines()]
