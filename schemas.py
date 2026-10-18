from pydantic import BaseModel

class UserRegister(BaseModel):
    email: str
    password: str

class UserPublic(BaseModel):
    email:str
    id:int

class NoteCreate(BaseModel):
    text: str

class NotePublic(BaseModel):
    text: str
    id: int

class CreateProduct(BaseModel):
    title: str
    price: int

class ProductPublic(BaseModel):
    title: str
    price: int
    id: int

class Orderpublic(BaseModel):
    id: int

