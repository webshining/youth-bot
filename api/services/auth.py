import hashlib
import hmac
from datetime import datetime, timedelta
from typing import NamedTuple

import jwt
from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer

from data.config import TELEGRAM_BOT_TOKEN, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, \
    ACCESS_TOKEN_SECRET_KEY, REFRESH_TOKEN_SECRET_KEY
from database.models import User
from loader import redis

not_enough_rights = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Not enough rights'
)
unauthorized = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
)
notfound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Not found'
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl='/api/auth/redirect', authorizationUrl='/api/auth')


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
    access_data['exp'] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_data['exp'] = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = jwt.encode(access_data, ACCESS_TOKEN_SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_data, REFRESH_TOKEN_SECRET_KEY, algorithm='HS256')
    await save_token(refresh_token, REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    return Tokens(access_token=access_token, refresh_token=refresh_token)


async def get_current_user(token: str = Depends(oauth2_scheme), refresh: bool = False):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET_KEY if refresh else ACCESS_TOKEN_SECRET_KEY,
                             algorithms=['HS256'])
        user = await User.get(int(payload['id']))
        if not user:
            await delete_token(token)
            raise unauthorized
        elif user.status not in ("admin", "super_admin"):
            await delete_token(token)
            raise not_enough_rights
        return user
    except:
        await delete_token(token)
        raise unauthorized


async def save_token(token: str, ex: int):
    await redis.set(token, 'token', ex=ex)


async def delete_token(token: str):
    await redis.delete(token)
