from pydantic import BaseModel,Field,HttpUrl,EmailStr
from datetime import datetime, time, timedelta
from enum import Enum
from typing import Annotated,Union,List,Dict,Any
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
    
class Image(BaseModel):
    url: str
    name: str 

class User(BaseModel):
    username: str
    full_name: str | None = None

class Item0(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=5
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None 

class Item1(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list = []

class Item2(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: List[str] = [] 

class Item3(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

class Item4(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None

class Image1(BaseModel):
    url: HttpUrl
    name: str


class Item5(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image1 | None = None    

class Itemm(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Image2(BaseModel):
    url: HttpUrl
    name: str


class Item6(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image2] | None = None

class Item7(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }
 
class Item9(BaseModel):
    name: str = Field(examples=["Foo"])
    description: str | None = Field(default=None, examples=["A very nice Item"])
    price: float = Field(examples=[35.4])
    tax: float | None = Field(default=None, examples=[3.29])

class Item10(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

class Item11(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []   

class Item12(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5
    tags: list[str] = []

class Item13(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5

class Item14(BaseModel):
    name: str
    description: str

class Item15(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

class Item16(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

class Item17(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None 

class Item18(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []       

class UserIn1(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserIn2(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut1(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class BaseUser1(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn3(BaseUser1):
    password: str


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]

class UserInn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None


class UserOutt(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

class UserBase3(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserInn1(UserBase3):
    password: str


class UserOutt1(UserBase3):
    pass


class UserInDB1(UserBase3):
    hashed_password: str

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int    

class Tags(Enum):
    items = "items"
    users = "users"

class User1(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None    

class Tokens(BaseModel):
    access_token: str
    token_type: str


class TokenDatas(BaseModel):
    username: str | None = None


class Users(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDBs(User):
    hashed_password: str
    disabled: bool

class Userd(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Itemd", back_populates="owner")


class Itemd(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Userd", back_populates="items")