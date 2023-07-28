import os


def create_dir(path: str) -> None:
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        raise Exception(f"Creating {path} is failed !!!")
