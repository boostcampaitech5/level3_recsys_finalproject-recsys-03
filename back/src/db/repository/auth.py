from mongoengine import QuerySet
from ..document import AuthDocument, UserDocument
from ..exception import NotFoundAuthException
from ...dto.model import Auth, User
from .common import find_user_doc_by_dto


class AuthRepository:
    def create_auth(self, user: User, refresh_token: str) -> Auth:
        user_doc: UserDocument = find_user_doc_by_dto(user)
        auth = AuthDocument(user=user_doc, refresh_token=refresh_token)
        saved: AuthDocument = auth.save()
        return saved.to_dto()

    def find_by_refresh_token(self, refresh_token: str) -> Auth:
        auth: AuthDocument = AuthDocument.objects(refresh_token=refresh_token).first()

        if not auth:
            return None

        return auth.to_dto()

    def delete_by_id(self, id: str) -> None:
        auths: QuerySet[AuthDocument] = AuthDocument.objects(id=id)

        if not auths:
            raise NotFoundAuthException(f"Can't find auth document: id={id}")

        auths.delete()
