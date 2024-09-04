from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserInDB(UserSchema):
    id: int

class UserPublic(UserSchema):
    id: int
    username: str
    email: EmailStr


