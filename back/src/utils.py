import os


def create_dir(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        raise Exception(f"Creating {dir} is failed !!!")


def get_first_dir(path: str) -> str:
    dirs = os.listdir(path)
    return dirs[0]
