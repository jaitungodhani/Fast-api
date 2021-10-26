from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app=FastAPI()

@app.get("/")
def index():
    return {"data":"blog list"}

@app.get("/blog")
def index(limit:int=10):
    return {"data":f"{limit} blogs from all blog list"}

@app.get("/blog/{id}")
def about(id:int):
    return {"about":f"it is your {id} blog"}

class Blog(BaseModel):
    title: str
    body : str
    published: Optional[bool]

@app.post('/blog')
def create_blog(request:Blog):
    return {'data':request}

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port= 2000)