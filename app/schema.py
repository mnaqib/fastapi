from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
    
class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

        
class Post(PostBase):
    owner : UserOut

    class Config:
        orm_mode = True

class PostOut(Post):
    votes: int
    
    class Config:
        orm_mode = True
    

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[str]

class vote(BaseModel):
    post_id: int
    dir: conint(le=1)