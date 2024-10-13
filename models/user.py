from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship





class RoleEnum(enum.Enum):
    user = "user"
    admin = "admin"


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    addresses = relationship("Address", back_populates="user")

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postal_code = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="addresses")