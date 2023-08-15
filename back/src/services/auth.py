from pydantic_core import ValidationError
from datetime import datetime
from ..config import AppConfig
from .jwt import encode_jwt, decode_jwt
from ..dto.auth import AccessTokenPayload, RefreshTokenPayload
from ..db import Auth, User, UserRepository, AuthRepository
from ..exceptions.auth import InvalidTokenException
from ..exceptions.error_type import ErrorType


class AuthService:
    def __init__(self, config: AppConfig, user_repository: UserRepository, auth_repository: AuthRepository) -> None:
        self.config = config
        self.user_repository = user_repository
        self.auth_repository = auth_repository

    def logged_in_user(self, access_token: str) -> User:
        payload: AccessTokenPayload = self.__decode_access_token(access_token)

        return self.user_repository.find_by_id(payload.user_id)

    def signin(self) -> tuple[str, str]:
        user: User = self.user_repository.create_user()

        access_token = self.__encode_access_token(AccessTokenPayload(user_id=user.id))
        refresh_token = self.__encode_refresh_token(RefreshTokenPayload(user_id=user.id))

        self.auth_repository.create_auth(user, refresh_token)

        return access_token, refresh_token

    def re_login(self, refresh_token: str) -> tuple[str, str]:
        self.__decode_refresh_token(refresh_token)

        auth: Auth = self.auth_repository.find_by_refresh_token(refresh_token)

        access_token = self.__encode_access_token(AccessTokenPayload(user_id=auth.user.id))
        new_refresh_token = self.__encode_refresh_token(RefreshTokenPayload(user_id=auth.user.id))

        self.auth_repository.delete_by_id(auth.id)
        self.auth_repository.create_auth(auth.user, new_refresh_token)

        return access_token, new_refresh_token

    def __decode_access_token(self, token: str) -> AccessTokenPayload:
        payload = decode_jwt(token, secret=self.config.jwt_secret)

        try:
            return AccessTokenPayload(**payload)
        except ValidationError:
            raise InvalidTokenException(ErrorType.INVALID_TOKEN)

    def __decode_refresh_token(self, refresh_token: str) -> RefreshTokenPayload:
        payload = decode_jwt(refresh_token, secret=self.config.jwt_secret)

        try:
            return RefreshTokenPayload(**payload)
        except ValidationError:
            raise InvalidTokenException(ErrorType.INVALID_TOKEN)

    def __encode_access_token(self, payload: AccessTokenPayload) -> str:
        access_token_exp = datetime.now() + self.config.access_token_exp_period
        return encode_jwt(payload.model_dump(), exp=access_token_exp, secret=self.config.jwt_secret)

    def __encode_refresh_token(self, payload: AccessTokenPayload) -> str:
        refresh_token_exp = datetime.now() + self.config.refresh_token_exp_period
        return encode_jwt(payload.model_dump(), exp=refresh_token_exp, secret=self.config.jwt_secret)
