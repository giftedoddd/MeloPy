from concurrent.futures import ThreadPoolExecutor
import pathlib
import re
import os

PATTERN = r"\.(flac|wav|mp3|opus|ogg|m4a|aac|wma)$"
PARENT_PATH = pathlib.Path(__file__).parent.parent.parent

def watch_dog(file_path):
    db_path = PARENT_PATH.joinpath("db/.stat")
    try:
        with db_path.open("r") as stat_file:
            path_and_date = stat_file.readlines()

        is_same = path_and_date[0].replace("\n", "") == file_path and path_and_date[1] == str(pathlib.Path(file_path).stat().st_mtime)
        if not is_same:
            raise FileNotFoundError
        return get_files(file_path=file_path, condition=is_same)
    except FileNotFoundError:
        with db_path.open("w") as stat_file:
            stat_file.write(f"{file_path}\n{pathlib.Path(file_path).stat().st_mtime}")
        return get_files(file_path=file_path, condition=False)

def get_files(file_path, condition):
    db_path = PARENT_PATH.joinpath("db/.path")
    paths_list = []

    def execute_workers(path):
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
            exe.submit(execute_workers, file_path)
        return paths_list
    with db_path.open("r") as paths_file:
        return paths_file.read()
