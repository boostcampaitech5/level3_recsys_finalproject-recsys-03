import unittest
from src import db
from .common import connect_to_db
from src.db.repository import AuthRepository, UserRepository
from src.dto.model import Auth, User
from src.db.exception import NotFoundAuthException


class TestAuth(unittest.TestCase):
    auth_repository = AuthRepository()
    user_repository = UserRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_auth(self):
        user = self.__user()
        self.__auth(user, "123")

    def test_find_by_refresh_token(self):
        user = self.__user()
        auth = self.__auth(user, "123")

        found = self.auth_repository.find_by_refresh_token(auth.refresh_token)
        assert auth == found

    def test_delete_by_id(self):
        user = self.__user()
        auth = self.__auth(user, "123")

        self.auth_repository.delete_by_id(auth.id)
        found = self.auth_repository.find_by_refresh_token(auth.refresh_token)
        assert found is None

        # not exists auth
        self.assertRaises(
            NotFoundAuthException,
            lambda: self.auth_repository.delete_by_id(auth.id),
        )

    def __auth(self, user: User, refresh_token: str) -> Auth:
        return self.auth_repository.create_auth(user=user, refresh_token=refresh_token)

    def __user(self) -> User:
        return self.user_repository.create_user()
