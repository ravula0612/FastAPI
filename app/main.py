from typing import Optional
from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import logging
import logging
from logging.handlers import RotatingFileHandler
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import traceback
load_dotenv()
# Create logger
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler(sys.stdout)
file_handler = RotatingFileHandler(
    'app.log', 
    maxBytes=1024 * 1024,  # 1MB
    backupCount=5
)

# Create formatters and add it to handlers
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

#set logging for this app

app = FastAPI()

class Post(BaseModel):
    # string type from the input
    """
    schema for the create post method 
    title and content is required.
    published in not mandatory : defaults to true.
    rating is not mandatory : defaults to none
    """
    title: str 
    content: str
    published: bool=True
while True:
    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres', 
                                password='Anu627',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        logger.info(f'successfully connected to the postgres.........')
        break
    except Exception as ex:
        logger.error(f'Error occured {ex}, {traceback.print_exc()}')
# dynamic list of post will be available here

my_posts = [{'id':1,'title':"1", 'content':'content 1'}]

@app.get("/")
async def root():
    return {"message": "Hello my xapi"}

@app.post("/posts")
async def create_post(new_post: Post):
    cursor.execute("""
                   INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) 
                   RETURNING * """, (new_post.title,new_post.content, new_post.published))
    post_dict = cursor.fetchone()
    conn.commit()
    return {"message":"created a post sucessfully",
            "body":post_dict}

@app.get("/posts")
async def get_post():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"posts":posts}

async def  find_post(id: int):
    try:
        for i in my_posts:
            print(f'=========== {i}')
            if i.get("id", "") == int(id):
                print('========')
                return i
    except Exception as ex:
        logger.error("logger info : ", ex)
        return {'body':'not found'}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"post_details": post}

@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute(f"""SELECT * FROM posts WHERE id={id}""")
    post_details = cursor.fetchone()
    if not post_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_details":post_details}


async def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p.get("id", "") == id:
            print('========')
            return i
    return None

@app.delete("/posts/{id}")
async def delete_post(id: int):
    # deleting the post
    # generate index
    post_index = await find_index_post(id)

    if not post_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} was not found")
    my_posts.pop(post_index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    post_index = await find_index_post(id)

    if not post_index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id : {id} was not found")

    post_dict = post.dict()

    post_dict[id] = id
    my_posts[post_index] = post_dict

    return {"post_details":post_dict}
        