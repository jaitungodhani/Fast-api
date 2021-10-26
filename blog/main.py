from fastapi import FastAPI
from . import models
from .Database import engine
from .routers import blog,user,authentication

app=FastAPI()

models.Base.metadata.create_all(engine)
app.include_router(blog.router)
app.include_router(user.user_router)
app.include_router(authentication.router)

