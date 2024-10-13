from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None

class ProductOut(BaseModel):
    name: str
    description: str
    price: float
    category: str
