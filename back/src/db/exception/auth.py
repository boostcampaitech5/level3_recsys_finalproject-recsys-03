class NotFoundAuthException(Exception):
    def __init__(self, msg: str = "Can't find auth document"):
        super().__init__(msg)
