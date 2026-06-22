from fastapi import HTTPException , status , Depends , Header
from fastapi.security import OAuth2PasswordBearer

from .jwt import verify_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/Token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token=token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user