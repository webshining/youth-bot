import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import NamedTuple

import jwt
from fastapi import Depends, Request
from fastapi.openapi.models import OAuthFlows
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param

from data.config import TELEGRAM_BOT_TOKEN, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, \
    ACCESS_TOKEN_SECRET_KEY, REFRESH_TOKEN_SECRET_KEY
from database.models import User
from loader import redis
from ..exceptions import unauthorized, tokenexpired, tokennotprovided


class OAuth2AuthorizationCodeBearer(OAuth2):
    def __init__(
            self,
            authorizationUrl: str,
            tokenUrl: str,
            client_id: str = None,
            scheme_name: str = None,
            scopes: dict = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlows(
            authorizationCode={
                "authorizationUrl": authorizationUrl,
                "tokenUrl": tokenUrl,
                "scopes": scopes
            })
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise tokennotprovided
        scheme, param = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            if self.auto_error:
                raise unauthorized
            else:
                return None
        return param


oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='/api/auth/redirect', authorizationUrl='/api/auth')


class JwtService:
    def __init__(self, token: str, refresh: bool = False):
        self.token = token
        self.refresh = refresh
        self.secret_key = REFRESH_TOKEN_SECRET_KEY if refresh else ACCESS_TOKEN_SECRET_KEY

    def __str__(self):
        return self.token

    async def delete(self):
        if self.refresh:
            await redis.delete(self.token)

    @property
    async def payload(self):
        try:
            if self.refresh:
                if not await redis.get(self.token):
                    return None
            return jwt.decode(self.token, self.secret_key, algorithms=['HS256'])
        except:
            return None

    @staticmethod
    async def generate(payload: any, refresh: bool = False):
        secret_key = REFRESH_TOKEN_SECRET_KEY if refresh else ACCESS_TOKEN_SECRET_KEY
        expire_minutes = REFRESH_TOKEN_EXPIRE_MINUTES if refresh else ACCESS_TOKEN_EXPIRE_MINUTES
        payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        if refresh:
            await redis.set(token, 'token', ex=expire_minutes * 60)
        return token


def is_telegram(data: dict) -> bool:
    try:
        hash = data['hash']
        del data['state']
        del data['hash']
        sorted_data = dict(sorted(data.items()))
        data_check_string = '\n'.join('='.join(i) for i in sorted_data.items()).encode()
        secret_key = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()
        return hmac.new(secret_key, data_check_string, hashlib.sha256).hexdigest() == hash
    except:
        return False


class Tokens(NamedTuple):
    access_token: str
    refresh_token: str


async def generate_tokens(access_data: dict, refresh_data: dict) -> Tokens:
    access_token = await JwtService.generate(access_data)
    refresh_token = await JwtService.generate(refresh_data, True)
    return Tokens(access_token=str(access_token), refresh_token=str(refresh_token))


async def get_current_user(token: str, refresh: bool = False):
    token = JwtService(token, refresh)
    if payload := await token.payload:
        if user := await User.get(int(payload['id'])):
            return user
    else:
        raise tokenexpired
    raise unauthorized


async def get_current_user_depends(token: str = Depends(oauth2_scheme)):
    return await get_current_user(token)
