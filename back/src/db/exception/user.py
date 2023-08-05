class NotFoundUserException(Exception):
    def __init__(self, msg: str = "Can't find user document"):
        super().__init__(msg)
