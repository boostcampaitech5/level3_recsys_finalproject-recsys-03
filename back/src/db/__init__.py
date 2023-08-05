import mongoengine


def connect(db: str, host: str, username: str, password: str, mongo_client_class=None):
    mongoengine.connect(
        db,
        host=host,
        username=username,
        password=password,
        mongo_client_class=mongo_client_class,
    )


def disconnect():
    mongoengine.disconnect()
