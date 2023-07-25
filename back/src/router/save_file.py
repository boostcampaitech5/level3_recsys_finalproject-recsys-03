from fastapi import UploadFile
from src.utils import create_dir

IMG_PATH = "outputs/userImgs/"


def save_file(session_id: str, image: UploadFile) -> str:
    create_dir(IMG_PATH)

    file_path = f"{IMG_PATH}{session_id}.jpg"
    with open(file_path, "wb+") as file_object:
        file_object.write(image.file.read())

    return file_path
