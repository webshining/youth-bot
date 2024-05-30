import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from api import router as api_router
from api.exceptions import unauthorized, tokenexpired, ApiException

tags_metadata = [
    {'name': "default"},
    {"name": "users"},
    {"name": "groups"},
    {"name": "auth"},
    {"name": "get methods"},
    {"name": "post methods"},
    {"name": "put methods"},
    {"name": "delete methods"},
]
app = FastAPI(openapi_tags=tags_metadata)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content=jsonable_encoder({"detail": exc.errors()[0]['msg']}))


@app.exception_handler(ApiException)
async def api_exception_handler(request: Request, exc: ApiException):
    response = JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    if request.url.path == "/api/auth/refresh" and exc in [unauthorized, tokenexpired]:
        response.delete_cookie(key='refreshToken', secure=True, httponly=True, samesite='none')
    return response


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=80)
