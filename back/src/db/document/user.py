from mongoengine import Document, StringField
from ...dto.user import User


class UserDocument(Document):
    fingerprint = StringField(required=True, unique=True)

    def to_dto(self) -> User:
        return User(str(self.id), self.fingerprint)
