from fastapi import APIRouter,Response,status,HTTPException,Depends
from .. import models
from .. import schemas, Database
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2


router= APIRouter(
    tags=['blogs']
)

@router.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request:schemas.Blog, db:Session = Depends(Database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=current_user)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id,db:Session = Depends(Database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Alert":f"Blog with {id} is not exist"})
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_item(id ,request:schemas.Blog, db:Session = Depends(Database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog=db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Alert":f"Blog with {id} is not exist"})
    blog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'updated'

@router.get('/blog', status_code=status.HTTP_200_OK)
def get(db:Session = Depends(Database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blogs=db.query(models.Blog).all()
    return blogs

@router.get('/blog/{id}',status_code=status.HTTP_200_OK, response_model=schemas.Showblog)
def parti_get(id,response:Response,db:Session = Depends(Database.get_db), current_user:schemas.User = Depends(oauth2.get_current_user)):
    blog= db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {"Alert":f"Blog with {id} is not aviable"}
    return blog
