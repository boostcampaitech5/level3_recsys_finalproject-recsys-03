import os


def create_dir(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        Exception("Creating %s is failed !!!", dir)


def get_first_dir(path: str) -> str:
    dirs = os.listdir(path)
    return dirs[0]
