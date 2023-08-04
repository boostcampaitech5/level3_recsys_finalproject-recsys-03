from mongoengine import Document
from ...dto.model import User


class UserDocument(Document):
    def to_dto(self) -> User:
        return User(str(self.id))
