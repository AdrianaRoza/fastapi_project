from pydantic import BaseModel
from typing import Optional

class UserSchemas(BaseModel):
    name: str
    email: str
    password: str
    active:Optional[bool]
    admin:Optional[bool]

    class Config:
        from_attributes = True



class OrderSchemas(BaseModel):
    user: int

    class Config:
        from_attributes = True


class LoginSchemas(BaseModel):
    email:str
    password:str

    class Config:
        from_attributes = True