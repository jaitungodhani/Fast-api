from fastapi.exceptions import HTTPException
from blog import schemas
from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .. import schemas,Database,models
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..token import create_access_token

router=APIRouter(
    tags=['authentication']
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password,hased_password):
    return pwd_context.verify(plain_password,hased_password)

@router.post('/login')
def login_user(request:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(Database.get_db)):
    user= db.query(models.User).filter(models.User.email==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')
    if not verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Password is not Valid')
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}