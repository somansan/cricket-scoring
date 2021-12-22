import random

from fastapi import FastAPI
from fastapi import Body
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status
from fastapi import Response
from typing import Optional

app = FastAPI()
my_posts = [{"id": 1, "title": "post1", "content": "this is new post"}]


class Post(BaseModel):
    title: str
    content: str


def find_post_index(post_id):
    for idx, post in enumerate(my_posts):
        if post_id == post["id"]:
            return idx


@app.get("/")
def root():
    return "Hello, World"


@app.get("/posts")
def get_posts():
    return {
        "data": my_posts
    }


@app.post("/posts/create", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_ = post.dict()
    post_["id"] = random.randint(1, 100000000)
    my_posts.append(post_)
    return {
        "message": "post created",
        "data": post_
    }


@app.get("/posts/{id}")
def get_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return {
                "data": post
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find post with id: {id}")


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    idx = find_post_index(id)
    if not idx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find post with id: {id}")
    _ = my_posts.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
