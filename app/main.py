from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel  # it is used to validate schema coming from user
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from sqlalchemy.orm import Session
from .database import engine,session_local,get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()



class Post(BaseModel):  #pydantic model schema
    title:str
    content:str
    published:bool=True
    # rating:Optional[int]=None
    
    
# connect to database
while True:       
    try:
        conn=psycopg2.connect(host='localhost',database='FastAPI',user='postgres',password=1234,cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("connection was succesfull")
        break
    except Exception as error:
        print("connecting to database failed")
        print("error :", error)
        time.sleep(3)


# my_post=[{"title":"hello","content":"vjfjv","id":1}]

# def find_post(id):  #helpful in retrieving particular post
#     for p in my_post:
#         if p['id']==id:
#             return p
        
# def find_index_post(id):    #helpful in deleting particular post by searching index
#     for i,p in enumerate(my_post):
#         if p["id"]==id:
#             return i

@app.get("/")
def root():
    return {"message": "Hello Everyone"}

@app.get("/posts")
def get_post(db: Session=Depends(get_db)):
    # cursor.execute("""select * from posts""")
    #using sqlalchemy
    posts=db.query(models.post).all()
    # print(posts)
    return {"data": posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(post:Post,db:Session=Depends(get_db)): #it will take the body and convert into pydantic model
    # we cannot use f string here because of sql injection
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    # new_post=cursor.fetchall()
    # conn.commit()
    
    # using sqlalchemy
   
    new_post=models.post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data":new_post}

# return latest post
# @app.get("/posts/latest")
# def get_latest_post():
#     post=my_post[len(my_post)-1]
#     return {"detail":post}

@app.get("/sqlalchemy")
def test_post(db:Session=Depends(get_db)):
    posts=db.query(models.post)
    print(posts)
    return {"status":"success"}

@app.get("/posts/{id}")  #path parameter
def get_post(id:int,db:Session =Depends(get_db)):
    # cursor.execute("""SELECT * from posts where id =%s""",(str(id)))
    # post=cursor.fetchone()
    post=db.query(models.post).filter(models.post.id==id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id :{id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"post_detail":"id not found"}
    return { "post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # cursor.execute("""DELETE FROM posts where id =%s returning *""",(str(id)))
    # deleted_post=cursor.fetchone()
    # conn.commit()
    post=db.query(models.post).filter(models.post.id==id)
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesnot exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int,upd_post:Post,db:Session=Depends(get_db)):
    # cursor.execute("""UPDATE posts set title=%s ,content=%s,published=%s where id =%s RETURNING *""",(post.title,post.content,post.published,str(id))) 
    # updated_post=cursor.fetchone()
    # conn.commit()
    
    post_query=db.query(models.post).filter(models.post.id==id)
    post=post_query.first()


    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} doesnot exist")
    #if index is found
    post_query.update(upd_post.dict(),synchronize_session=False)
    db.commit()

    return {"data":post_query.first()}
    


