from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    # 72 байта: лимит bcrypt, длиннее пароль он не принимает
    password: str = Field(min_length=8, max_length=72)


class UserPublic(BaseModel):
    id: int
    email: str


class NoteCreate(BaseModel):
    text: str


class NotePublic(BaseModel):
    id: int
    text: str


class CreateProduct(BaseModel):
    title: str
    price: int


class ProductPublic(BaseModel):
    id: int
    title: str
    price: int


class OrderPublic(BaseModel):
    id: int
    product_id: int
    user_id: int
