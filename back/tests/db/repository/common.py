import dotenv
import os
import mongomock
import src.db


def connect_to_db():
    dotenv.load_dotenv()
    host = os.environ.get("DB_HOST")
    db = os.environ.get("DB_NAME")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")

    src.db.connect(
        db=db,
        host=host,
        username=username,
        password=password,
        mongo_client_class=mongomock.MongoClient,
    )
