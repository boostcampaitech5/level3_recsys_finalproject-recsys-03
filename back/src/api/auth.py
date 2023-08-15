from fastapi import APIRouter
from ..dto.request import ReLoginRequest
from ..dto.response import SigninResponse, ReLoginResponse
from ..services.auth import AuthService
from ..config import AppConfig
from ..db import UserRepository, AuthRepository

config = AppConfig()
user_repository = UserRepository()
auth_repository = AuthRepository()

authService = AuthService(config=config, user_repository=user_repository, auth_repository=auth_repository)
router = APIRouter()


@router.post("/signin")
async def signin() -> SigninResponse:
    access_token, refresh_token = authService.signin()
    return SigninResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/relogin")
async def relogin(re_login_request: ReLoginRequest) -> ReLoginResponse:
    access_token, refresh_token = authService.re_login(re_login_request.refresh_token)
    return ReLoginResponse(access_token=access_token, refresh_token=refresh_token)
