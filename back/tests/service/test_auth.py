import unittest
from unittest.mock import Mock
from datetime import datetime
from src.services.auth import AuthService
from src.config import AppConfig
from src.dto.auth import AccessTokenPayload, RefreshTokenPayload
from src.db import User, Auth, UserRepository, AuthRepository
from src.exceptions.auth import InvalidTokenException


class TestAuthService(unittest.TestCase):
    def setUp(self) -> None:
        self.app_config = AppConfig()
        self.user_repository: UserRepository = Mock()
        self.auth_repository: AuthRepository = Mock()
        self.auth_service = AuthService(self.app_config, self.user_repository, self.auth_repository)

    def test_logged_in_user(self):
        expected_user = User(id="1")
        self.user_repository.find_by_id.return_value = expected_user
        access_token_payload = AccessTokenPayload(user_id=expected_user.id)
        access_token = self.auth_service._AuthService__encode_access_token(access_token_payload)

        user = self.auth_service.logged_in_user(access_token)

        assert user == expected_user

    def test_logged_in_user__if_the_access_token_is_not_valid_then_should_raise_InvalidTokenException(self):
        expected_user = User(id="1")
        self.user_repository.find_by_id.return_value = expected_user
        invalid_access_token = "invalid"

        with self.assertRaises(InvalidTokenException):
            self.auth_service.logged_in_user(invalid_access_token)

    def test_signin(self):
        new_user = User(id="1")
        self.user_repository.create_user.return_value = new_user

        access_token, refresh_token = self.auth_service.signin()

        self.auth_service._AuthService__decode_access_token(access_token)
        self.auth_service._AuthService__decode_refresh_token(refresh_token)

    def test_re_login(self):
        expected_user = User(id="1")
        refresh_token = self.auth_service._AuthService__encode_refresh_token(RefreshTokenPayload(user_id=expected_user.id))
        auth = Auth(id="1", user=expected_user, refresh_token=refresh_token, created_at=datetime.now())
        self.auth_repository.find_by_refresh_token.return_value = auth

        access_token, new_refresh_token = self.auth_service.re_login(refresh_token)

        access_token_payload = self.auth_service._AuthService__decode_access_token(access_token)
        assert access_token_payload.user_id == expected_user.id
        new_refresh_token_payload = self.auth_service._AuthService__decode_refresh_token(new_refresh_token)
        assert new_refresh_token_payload.user_id == expected_user.id

    def test_re_login__if_the_refresh_token_is_not_valid_then_should_raise_InvalidTokenException(self):
        refresh_token = "invalid"

        with self.assertRaises(InvalidTokenException):
            access_token, new_refresh_token = self.auth_service.re_login(refresh_token)
