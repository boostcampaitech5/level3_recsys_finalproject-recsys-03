class NotFoundInferenceException(Exception):
    def __init__(self, msg: str = "Can't find inference document"):
        super().__init__(msg)
