from passlib.context import CryptContext
from .. import schemas,models,Database
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

user_router= APIRouter(
    tags=['users']
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@user_router.post('/user', response_model=schemas.Showuser)
def create_user(request:schemas.User,db:Session = Depends(Database.get_db)):
    hash_password=pwd_context.hash(request.password)
    new_user=models.User(name=request.name,email=request.email,password=hash_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@user_router.get('/getuser/{id}', response_model=schemas.Showuser)
def get_user(id:int,db:Session = Depends(Database.get_db)):
    user=db.query(models.User).filter(models.User.id==id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Alert":f"User with {id} id is not exist"})
    user=user.first()
    return user
