import json
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from data.config import DIR, REFRESH_TOKEN_EXPIRE_MINUTES, FRONTEND_URL
from database.models import User
from loader import bot
from ..exceptions import unauthorized, tokennotprovided
from ..services import generate_tokens, is_telegram, get_current_user

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


def set_cookie(response: Response, value: str):
    response.set_cookie(key='refreshToken', value=value, httponly=True,
                        expires=datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES),
                        samesite='none', secure=True)


def delete_cookie(response: Response):
    response.delete_cookie(key='refreshToken', httponly=True, samesite='none', secure=True)


@router.get('/')
async def _auth(request: Request, state: str = FRONTEND_URL):
    return templates.TemplateResponse("auth.html", {"bot_username": (await bot.get_me()).username,
                                                    "redirect": request.url_for("_auth_redirect").include_query_params(
                                                        state=state), "request": request})


@router.get('/redirect')
async def _auth_redirect(id: int, request: Request, state: str = FRONTEND_URL):
    if is_telegram(dict(request.query_params)):
        user = await User.get(id)

        if not user:
            data = {"detail": unauthorized.detail}
            return RedirectResponse(f'{state}#{json.dumps(data)}')

        access_token, refresh_token = await generate_tokens({'id': id}, {'id': id})
        data = {"user": user.model_dump(), "accessToken": access_token}
        response = RedirectResponse(f'{state}#{json.dumps(data)}') if state else JSONResponse(data)
        set_cookie(response, refresh_token)
        return response
    else:
        data = json.dumps({"error": unauthorized.detail})
        return RedirectResponse(f'{state}#{data}') if state else {"error": unauthorized.detail}


@router.get('/refresh')
async def _refresh(request: Request):
    refresh_token = request.cookies.get('refreshToken')
    if not refresh_token:
        raise tokennotprovided
    user = await get_current_user(refresh_token, True)
    access_token, refresh_token = await generate_tokens({'id': user.id}, {'id': user.id})
    response = JSONResponse({'user': user.model_dump(), 'accessToken': access_token})
    set_cookie(response, refresh_token)
    return response


@router.get('/logout')
async def _logout():
    response = JSONResponse({'message': "ok"})
    delete_cookie(response)
    return response
