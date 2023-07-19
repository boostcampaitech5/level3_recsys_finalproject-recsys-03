from fastapi import UploadFile
from src.log.CreateDirectory import createDirectory
from logging import Logger

IMG_PATH = "outputs/userImgs/"

def save_file(session_id:str, image: UploadFile, user_logger:Logger) -> None:
    createDirectory(IMG_PATH)

    file_path = f"{IMG_PATH}{session_id}.jpg"
    with open(file_path, "wb+") as file_object:
        file_object.write(image.file.read())

    user_logger.info("Img Path : %s", file_path)


    
