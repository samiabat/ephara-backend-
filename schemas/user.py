from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    password: str

class UserLogin(BaseModel):
    email_or_phone: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class UserOut(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str

    class Config:
        orm_mode = True

class UserProfileUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None

class AddressCreate(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str

class AddressUpdate(BaseModel):
    street: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None


