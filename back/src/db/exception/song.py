class NotFoundSongException(Exception):
    def __init__(self, msg: str = "Can't find song document"):
        super().__init__(msg)
