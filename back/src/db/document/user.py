from mongoengine import Document, StringField
from ...dto.model import User


class UserDocument(Document):
    fingerprint = StringField(required=True, unique=True)

    def to_dto(self) -> User:
        return User(str(self.id), self.fingerprint)
