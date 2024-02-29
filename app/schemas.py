from pydantic import BaseModel, EmailStr, conint
from datetime import datetime   
from typing import Optional

# from pydantic.types import conint


    
# User validation schema   - reqeust  
class UserCreate(BaseModel):
    email: EmailStr
    password: str   
# User validation schema - response
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

# Login Validation schema - request
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Post validation schema   - reqeust  

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Post validation schema   - response  
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(BaseModel):
    Post: Post
    votes: int    


# Token Validation schema - response
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

