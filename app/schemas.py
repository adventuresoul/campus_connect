from pydantic import BaseModel, EmailStr
from datetime import datetime
import enum
from typing import Optional

## Users
class UserBase(BaseModel):
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

# request model
class UserCreate(UserBase):
    password: str

# request model
class UpdateUser(UserBase):
    password: str

# response model
class User(UserBase):
    class Config:
        orm_mode = True

# Login model
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# posts
class PostBase(BaseModel):
    title: str
    content: str

# request model
class PostCreate(PostBase):
    pass

# request model
class PostUpdate(PostBase):
    pass

class Post(BaseModel):
    id: int
    title: str
    content_text: str
    content_file: Optional[str]  # Base64 encoded string
    user_id: int

    class Config:
        from_attributes = True  # Corrected config key for Pydantic v2

class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        orm_mode = True


# Token Model
class Token(BaseModel):
    access_token: str
    token_type: str

# class TokenData(BaseModel):
#     id: str


# # Enum vote
# class Vote_Model(enum.Enum):
#     like = 1
#     dislike = 0

# Vote Model
class Vote(BaseModel):
    post_id: int
    vote_value: int
    
# Normal message format, (message: successful)
class Message(BaseModel):
    message: str