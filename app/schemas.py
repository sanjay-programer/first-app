from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import List,Tuple

class post_control(BaseModel):
    title:str
    content:str
    created_at:datetime
    owner_id:int

    @classmethod
    def from_db_list(cls,posts:List[Tuple]):
        return [cls.from_db(post) for post in posts]

    @classmethod
    def from_db(cls,post_tuple:Tuple):
        return cls(
            title=post_tuple[1],
            content=post_tuple[2],
            created_at=post_tuple[4],
            owner_id=post_tuple[5]
        )

class create_post(BaseModel):
    title:str
    content:str
    is_published:bool=True
    owner_id:int

class POST(BaseModel):
    title: str
    content: str
    is_published: bool = True

class Sample(BaseModel):
    id:int
    title:str
    content:str
    is_published:bool
    created_at:datetime

    class Config:
        from_attributes = True

class New_User(BaseModel):
    user_name:str="Guest"
    email:EmailStr
    password:str
