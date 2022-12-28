from pydantic import BaseModel
from typing import Optional

class ProjectBase(BaseModel):
    title:str
    featured_image:str
    description:str
    demo_link:str
    source_link:str
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name:str
    last_name:str
    username:str
    password:str
    is_active:Optional[bool]

class showUser(BaseModel):
    email:str
    is_active:bool
    class Config():
        orm_mode = True

class skillBase(BaseModel):
    name:str
    description:str 

class Login(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


class ProfileBase(BaseModel):
    # user_id
    first_name:str
    last_name:str
    location:str
    short_intro:str
    bio:str
    # profile_image 
    social_github:str
    social_twitter:str
    social_linkedin:str
    social_youtube:str
    social_website:str

class ReviewBase(BaseModel):
    comment :str
    vote_value: str