from blog.models import User
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from .token import verifytoken
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if verifytoken(data,credentials_exception):
        user=verifytoken(data,credentials_exception)
        return user
