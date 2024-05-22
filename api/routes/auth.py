import json

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from data.config import DIR, REFRESH_TOKEN_EXPIRE_MINUTES
from database.models import User
from loader import bot
from ..exceptions import notfound, not_enough_rights, unauthorized
from ..services import delete_token, generate_tokens, get_current_user, is_telegram

router = APIRouter(prefix="/auth")
templates = Jinja2Templates(directory=f"{DIR}/api/templates")


@router.get('/')
async def _auth(request: Request, state: str = ""):
    return templates.TemplateResponse("auth.html", {"bot_username": (await bot.get_me()).username,
                                                    "redirect": request.url_for("_auth_redirect").include_query_params(
                                                        state=state), "request": request})


@router.get('/redirect')
async def _auth_redirect(id: int, request: Request, state: str = ""):
    if is_telegram(dict(request.query_params)):
        user = await User.get(id)

        data = {}
        if not user:
            data = json.dumps({"error": notfound.detail})
        if not user.is_admin() and not data:
            data = json.dumps({"error": not_enough_rights.detail})
        if data:
            return data if not state else RedirectResponse(f'{state}#{data}')

        access_token, refresh_token = await generate_tokens({'id': id}, {'id': id})
        data = {"user": user.model_dump(), "accessToken": access_token}
        response = RedirectResponse(f'{state}#{json.dumps(data)}') if state else JSONResponse(data)
        response.set_cookie(key='refreshToken', value=refresh_token, max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
                            httponly=True, samesite='none', secure=True)
        return response
    else:
        data = json.dumps({"error": unauthorized.detail})
        return RedirectResponse(f'{state}#{data}') if state else {"error": unauthorized.detail}


@router.get('/refresh')
async def _refresh(request: Request):
    refresh_token = request.cookies.get('refreshToken')
    if not refresh_token:
        raise unauthorized
    user = await get_current_user(refresh_token, True)
    await delete_token(refresh_token)
    access_token, refresh_token = await generate_tokens({'id': user.id}, {'id': user.id})
    response = JSONResponse({'user': user.model_dump(), 'accessToken': access_token})
    response.set_cookie(key='refreshToken', value=refresh_token, httponly=True,
                        max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60, samesite='none', secure=True)
    return response


@router.get('/logout')
async def _logout():
    response = JSONResponse({'message': "ok"})
    response.delete_cookie(key='refreshToken', secure=True, httponly=True, samesite='none')
    return response
