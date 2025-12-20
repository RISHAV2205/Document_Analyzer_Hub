from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.sql.expression import null,text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class post(Base):
    __tablename__="posts"
    
    id =Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default="True",nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    owner_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    owner = relationship("user", back_populates="posts")

    
class user(Base):
    __tablename__="users"
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    id =Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    posts = relationship("post", back_populates="owner")
        
    