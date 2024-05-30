from fastapi import status


class ApiException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


notenoughrights = ApiException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Not enough rights'
)
unauthorized = ApiException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
)
tokenexpired = ApiException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Token expired',
)
tokennotprovided = ApiException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='No token provided',
)
notfound = ApiException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail='Not found'
)
