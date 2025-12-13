from pydantic import BaseModel,EmailStr
from datetime import datetime

class PostBase(BaseModel):#pydantic model to validate post and put request
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
    pass

class Post(BaseModel):#for response sending back to user(response model)
    title:str
    content:str
    published:bool
    class Config:  # to convert sqlalchemy model to pydantic or dictionary
        orm_mode=True
    


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:str
    created_at: datetime
    
    class Config:
        orm_mode=True

    
    
    