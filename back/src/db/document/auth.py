from mongoengine import Document, DateTimeField, StringField, ReferenceField
from ...dto.model import Auth
from datetime import datetime
from ...config import AppConfig
from .user import UserDocument

config = AppConfig()


class AuthDocument(Document):
    user = ReferenceField(UserDocument, required=True, unique=True)
    refresh_token = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {"indexes": [{"fields": ["created_at"], "expireAfterSeconds": int(config.refresh_token_exp_period.total_seconds())}]}

    def to_dto(self) -> Auth:
        return Auth(id=str(self.id), user=self.user.to_dto(), refresh_token=self.refresh_token, created_at=self.created_at)
