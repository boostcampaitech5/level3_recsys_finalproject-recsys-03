from PIL import Image
from fastapi import UploadFile
from src.utils import create_dir

IMG_PATH = "outputs/userImgs/"


def save_file(session_id: str, image: UploadFile) -> str:
    create_dir(IMG_PATH)

    file_path = f"{IMG_PATH}{session_id}.jpg"
    with open(file_path, "wb+") as file_object:
        file_object.write(image.file.read())

    return file_path


def resize_img(img_path: str, size: int) -> None:
    with Image.open(img_path) as im:
        resized = im.resize((size, size))
        resized.save(img_path)
