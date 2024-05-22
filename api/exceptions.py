from fastapi import HTTPException, status

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
