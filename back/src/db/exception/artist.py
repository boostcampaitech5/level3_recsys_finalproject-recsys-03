class NotFoundArtistException(Exception):
    def __init__(self, msg: str = "Can't find artist document"):
        super().__init__(msg)
