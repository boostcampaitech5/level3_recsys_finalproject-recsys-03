from ..document import UserDocument
from ...dto.model import User


class UserRepository:
    def create_user(self) -> User:
        user = UserDocument()
        saved: UserDocument = user.save()
        return saved.to_dto()

    def find_by_id(self, id: str) -> User:
        user: UserDocument = UserDocument.objects(id=id).first()

        if not user:
            return None

        return user.to_dto()

    def find_all(self) -> list[User]:
        users: list[UserDocument] = list(UserDocument.objects)
        return [user.to_dto() for user in users]
