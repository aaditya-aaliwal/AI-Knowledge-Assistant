from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    name: str = Field(min_length=3, max_length=20)
    email: EmailStr

    class Config:
        from_attributes = True

