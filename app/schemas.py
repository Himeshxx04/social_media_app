from pydantic import Field
from typing import Optional
from pydantic import EmailStr
from pydantic.v1 import EmailError
import email
from datetime import datetime
from pydantic import BaseModel
class PostBase(BaseModel):
    
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):

    pass

class Post(PostBase):
    id:int
    created_at:datetime
    user_id:int
    user:UserResponse

    class Config:
        from_attributes=True

class PostOut(BaseModel):
    Post: Post        # capital P — must match
    votes: int
    
    class Config:
        from_attributes=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes=True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

    class Config:
        from_attributes=True

class TokenData(BaseModel):
    id:Optional[int]=None
    

class Vote(BaseModel):
    post_id:int
    vote_dir:int=Field(ge=0,le=1)

