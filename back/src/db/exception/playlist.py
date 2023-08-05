class NotFoundPlaylistException(Exception):
    def __init__(self, msg: str = "Can't find playlist document"):
        super().__init__(msg)
