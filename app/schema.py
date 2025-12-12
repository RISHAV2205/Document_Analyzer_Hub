from pydantic import BaseModel

class PostBase(BaseModel):#pydantic model
    title:str
    content:str
    published:bool=True
    
class PostCreate(PostBase):
    pass


    
    