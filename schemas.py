from pydantic import BaseModel, ConfigDict, Field


# INPUT SCHEMA
class BlogCreate(BaseModel):
    title: str
    content: str


# OUTPUT SCHEMA
class BlogResponse(BaseModel):
    id: int
    title: str
    content: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
