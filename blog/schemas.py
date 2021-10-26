from typing import List,Optional
from pydantic import BaseModel

class User(BaseModel):
    name:str
    email:str
    password:str
    
class Blog(BaseModel):
    title:str
    body:str

class BlogBase(Blog):
    class Config:
        orm_mode = True

class Showuser(BaseModel):
    name:str
    email:str
    blogs:List[BlogBase]=[]
    class Config:
        orm_mode = True

class Showblog(BaseModel):
    title:str
    body:str
    creator:Showuser
    class Config:
        orm_mode = True

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
