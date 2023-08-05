import unittest
from src import db
from .common import connect_to_db
from src.db.repository import UserRepository
from src.dto.model import User


class TestUser(unittest.TestCase):
    user_repository = UserRepository()

    @classmethod
    def setUp(cls):
        connect_to_db()

    @classmethod
    def tearDown(cls):
        db.disconnect()

    def test_create_user(self):
        self.__user()

    def test_find_by_geine_id(self):
        user = self.__user()

        found = self.user_repository.find_by_id(user.id)
        assert user == found

    def test_find_all(self):
        users = [
            self.__user(),
            self.__user(),
            self.__user(),
        ]

        found = self.user_repository.find_all()
        for user in users:
            assert user in found

    def __user(self) -> User:
        return self.user_repository.create_user()
