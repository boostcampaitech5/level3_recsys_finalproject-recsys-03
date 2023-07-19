import os

def createDirectory(dir: str) -> None:
    try:
        if not os.path.exists(dir):
            os.makedirs(dir)
            print(f">>> {dir} is created !!!")
    except OSError:
        Exception("Creating %s is failed !!!", dir)