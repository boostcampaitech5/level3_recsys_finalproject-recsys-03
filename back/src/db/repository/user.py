from ..document import UserDocument
from ..exception import NotFoundUserException
from ...dto.user import User


class UserRepository:
    def create_user(self, fingerprint: str) -> User:
        user = UserDocument(fingerprint=fingerprint)
        saved: UserDocument = user.save()
        return saved.to_dto()

    def delete_by_fingerprint(self, fingerprint: str) -> None:
        user: UserDocument = UserDocument.objects(fingerprint=fingerprint)

        if not user:
            raise NotFoundUserException(f"Can't find user document: fingerprint={fingerprint}")

        user.delete()

    def find_by_fingerprint(self, fingerprint: str) -> User:
        user: UserDocument = UserDocument.objects(fingerprint=fingerprint).first()

        if not user:
            return None

        return user.to_dto()

    def find_all(self) -> list[User]:
        users: list[UserDocument] = list(UserDocument.objects)
        return [user.to_dto() for user in users]
