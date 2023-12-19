
from datetime import datetime, time, timedelta
from fastapi import FastAPI,Query,Path,Body,Cookie,Header,status,Response,Form,File, UploadFile,HTTPException,Depends,status,Request
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse, RedirectResponse,HTMLResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import *
from fastapi.encoders import jsonable_encoder
from typing import Annotated,Union,List,Dict,Any
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_db = {}
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
fake_users_db = {
    "sanjeev": {
        "username": "sanjeev",
        "full_name": "Sanjeev C",
        "email": "sanjeev@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def main():
    return {"message": "Hello World"}

# Basic
@app.get("/hi")
async def root(response:Response):
    # response.status_code=status.HTTP_201_CREATED
    response.status_code = 404
    return {"message": "Hello World"}

# path parameters
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

# path parameters with type
@app.get("/items/{item_id}")
async def read_item(item_id:int):
    return {"item_id": item_id}

#Predefined values
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

#Path convertor
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

#Query Parameters
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/item/")
async def read_item(skip: int = 0, limit: int = 2): # this is for getting number of data from list
    return fake_items_db[skip : skip + limit]

#Optional parameters
@app.get("/itemspara/{item_id}")
async def read_item(item_id: str, q: str | None = "All"): #change our fixed or our default value as our wish
    print(q)
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}

#Query parameter type conversion
@app.get("/itemspara1/{item_id}")
async def read_item(item_id: str, q: str | None = "ALL", short: bool = True):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#Multiple path and query parameters¶
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: str, q: str | None = "test", short: bool = True):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

#Required query parameters
@app.get("/itemre1/{item_id}")
async def read_user_item(item_id: str, needy: str):
    print("================",item_id,needy)
    item = {"item_id": item_id, "needy": needy}
    return item

#Required query parameters limit
@app.get("/itemsrelimit/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

#Request Body
@app.post("/itemsbase/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Request body + path parameters
@app.put("/itemadd/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

#Request body + path + query parameters
@app.put("/itemsaddapra/{item_id}")
async def create_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

#Query Parameters and String Validations
@app.get("/itemsquery/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Add Query to Annotated in the q parameter
@app.get("/itemsannotated/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#old method instead of annoted Add more validations
@app.get("/itemaddmorevariable/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Add regular expressions
@app.get("/itemsexpressions/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50, pattern="^fixedquery$")] = None,):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Pydantic v1 regex instead of pattern
@app.get("/itemsregex/")
async def read_items(q: Annotated[str | None, Query(min_length=3, max_length=50, regex="^fixedquery$")] = None,):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Default values
@app.get("/itemsdefaultvalues/")
async def read_items(q: Annotated[str, Query(min_length=3)] = "fixedquery"):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Required with Ellipsis (...)
# @app.get("/itemse1/")
# async def read_items(q: Annotated[str, Query(min_length=3)] = ...):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# Query parameter list / multiple values
@app.get("/itemsmultiplevalues/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items

# Query parameter list / multiple values with defaults
@app.get("/itemsmultiplevaluesdefault/")
async def read_items(q: Annotated[list[str], Query()] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items

# Declare more metadata

@app.get("/itemsdeclaremetadata/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Alias parameters
@app.get("/itemsalias/")
async def read_items(q: Annotated[str | None, Query(alias="item-query")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Deprecating parameters
@app.get("/itemsdeprecating/")
async def read_items(
    q: Annotated[
        str | None,
        Query(
            alias="item-query",
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
            max_length=50,
            pattern="^fixedquery$",
            deprecated=True,
        ),
    ] = None,
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Exclude from OpenAPI
@app.get("/itemsexclude/")
async def read_items(
    hidden_query: Annotated[str | None, Query(include_in_schema=False)] = None
):
    if hidden_query:
        return {"hidden_query": hidden_query}
    else:
        return {"hidden_query": "Not found"}
    

# Path Parameters and Numeric Validations
@app.get("/itemsnumeric/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return 

# Order the parameters as you need
@app.get("/itemsorderpara/{item_id}")
async def read_items(
    q: str, item_id: Annotated[int, Path(title="The ID of the item to get")]
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Order the parameters as you need, tricks
@app.get("/itemstricks/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Better with Annotated
@app.get("/itemsbetterannotated/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number validations: greater than or equal
@app.get("/itemsnumbervalidationgraterthan/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=1)], q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number validations: greater than and less than or equal
@app.get("/itemsnumbervalidationgraterthanlessathan/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Number validations: floats, greater than and less than
@app.get("/itemsfloat/{item_id}")
async def read_items(
    *,
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str,
    size: Annotated[float, Query(gt=0, lt=10.5)],
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# Body - Multiple Parameters
# Mix Path, Query and body parameters

@app.put("/itemsmixpath/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Itemm | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# Singular values in body
@app.put("/itemssingular/{item_id}")
async def update_item(
    item_id: int, item: Itemm, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

# Multiple body params and query
@app.put("/itemsmultiplepara/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Itemm,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

# Embed a single body parameter
@app.put("/itemsembed/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=False)):
    results = {"item_id": item_id, "item": item}
    return results

# Body - Fields it verify the data from class so it show error inside json
@app.put("/itemsbodyfield/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

# Body - Nested Models
# List fields
@app.put("/itemsnestedmodel/{item_id}")
async def update_item(item_id: int, item: Item0):
    results = {"item_id": item_id, "item": item}
    return results
# List fields with type parameter    
@app.put("/itemslisttype/{item_id}")
async def update_item(item_id: int, item: Item1):
    results = {"item_id": item_id, "item": item}
    return results

# Declare a list with a type parameter in inside class
@app.put("/itemsparameterinsideclass/{item_id}")
async def update_item(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results

# Set types
@app.put("/itemsset/{item_id}")
async def update_item(item_id: int, item: Item3):
    results = {"item_id": item_id, "item": item}
    return results

# Define a submodel
@app.put("/itemssubmodel/{item_id}")
async def update_item(item_id: int, item: Item4):
    results = {"item_id": item_id, "item": item}
    return results

# Special types and url validation
@app.put("/itemsspecialtype/{item_id}")
async def update_item(item_id: int, item: Item5):
    results = {"item_id": item_id, "item": item}
    return results

# Deeply nested models
@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

# Bodies of pure lists
@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image1]):
    return images

# Bodies of arbitrary dicts
@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights

# Declare Request Example Data
# Extra JSON Schema data in Pydantic models
@app.put("/itemsjsonschema/{item_id}")
async def update_item(item_id: int, item: Item7):
    results = {"item_id": item_id, "item": item}
    return results

# Field additional arguments
@app.put("/itemsadditionalarguments/{item_id}")
async def update_item(item_id: int, item: Item9):
    results = {"item_id": item_id, "item": item}
    return results

# Using the openapi_examples Parameter
@app.put("/itemsopenapiexample/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results

# Extra Data Types
@app.put("/itemsextradatatypes/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
    repeat_at: Annotated[time | None, Body()] = None,
    process_after: Annotated[timedelta | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

# Cookie Parameters
@app.get("/itemscookiepara/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

# Header Parameters
@app.get("/itemsheader/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# Automatic conversion
@app.get("/itemsautomeaticconversion/")
async def read_items(
    user_agent: Annotated[str | None, Header(convert_underscores=False)] = None
):
    return {"strange_header": user_agent}

# Duplicate headers
@app.get("/itemsduplicateheader/")
async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
    return {"X-Token values": x_token}

# Response Model - Return Type
@app.post("/itemsmodel1/")
async def create_item(item: Item10):
    return item

@app.get("/itemsmodel2/")
async def read_items():
    return [
        Item10(name="Portal Gun", price=42.0),
        Item10(name="Plumbus", price=32.0),
    ]

# response_model Parameter
@app.post("/itemsmodel3/", response_model=Item11)
async def create_item(item: Item11):
    return item


@app.get("/itemsmodel4/", response_model=list[Item11])
async def read_items():
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]

# Return the same input data

# Don't do this in production it return password to all client!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.post("/user/")
async def create_user(user: UserIn1):
    return user
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# use this type of production
@app.post("/userproduction/", response_model=UserOut1)
async def create_user(user: UserIn2) -> Any:
    return user

@app.post("/userproductionfilter1/")
async def create_user(user: UserIn3) -> BaseUser1:
    return user

# Other Return Type Annotations
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})

# Annotate a Response Subclass
@app.get("/teleport")
async def get_teleport() -> RedirectResponse:
    return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Disable Response Model
@app.get("/portaldisable", response_model=None)
async def get_portal(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "Here's your interdimensional portal."}

# Response Model encoding parameters
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}
@app.get("/items1/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

# response_model_include and response_model_exclude
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The Bar fighters", "price": 62, "tax": 20.2},
    "baz": {
        "name": "Baz",
        "description": "There goes my baz",
        "price": 50.2,
        "tax": 10.5,
    },
}

@app.get(
    "/items/{item_id}/name",
    response_model=Item,
    response_model_include={"name", "description"},
)
async def read_item_name(item_id: str):
    return items[item_id]
@app.get("/items/{item_id}/public", response_model=Item, response_model_exclude={"tax"})
async def read_item_public_data(item_id: str):
    return items[item_id]

# Using lists instead of sets
@app.get(
    "/items1/{item_id}/name",
    response_model=Item,
    response_model_include=["name", "description"],
)
async def read_item_name(item_id: str):
    return items[item_id]


@app.get("/items1/{item_id}/public", response_model=Item, response_model_exclude=["tax"])
async def read_item_public_data(item_id: str):
    return items[item_id]

# Extra Models
# Multiple models
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserInn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really",user_in_db)
    return user_in_db


@app.post("/usermultimodels/", response_model=UserOutt)
async def create_user(user_in: UserInn):
    user_saved = fake_save_user(user_in)
    return user_saved

# Reduce duplication
def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserInn1):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/userduplication/", response_model=UserOutt1)
async def create_user(user_in: UserInn1):
    user_saved = fake_save_user(user_in)
    return user_saved

# Union or anyOf
items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/itemss/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]

# List of models
items = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]
@app.get("/itemslistofmodel/", response_model=list[Item14])
async def read_items():
    return items

# Response with arbitrary dict
@app.get("/keyword-weights/", response_model=dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.0}

# Response Status Code
@app.post("/itemsstatuscode/", status_code=201)
async def create_item(name: str):
    return {"name": name}

# Shortcut to remember the names
@app.post("/itemsshortcut/", status_code=status.HTTP_404_NOT_FOUND)
async def create_item(name: str):
    return {"name": name}

# Form Data
@app.post("/loginform/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

# Request Files
# File Parameters with UploadFile
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}

# Optional File Upload
@app.post("/filesoptional/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/uploadfileoptional/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}

# UploadFile with Additional Metadata
@app.post("/filesmeta/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@app.post("/uploadfilemeta/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}

# Multiple File Uploads
@app.post("/filesmulti/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfilesmulti/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


@app.get("/multifile/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# Request Forms and Files
# Define File and Form parameters
@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

# Handling Errors
items = {"foo": "The Foo Wrestlers"}
@app.get("/itemserror/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items[item_id]}

# Add custom headers
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

# Path Operation Configuration
@app.post("/itemspathoperation/", response_model=Item15, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item15):
    return item

# Tags
@app.post("/itemstag1/", response_model=Item, tags=["items"])
async def create_item(item: Item):
    return item


@app.get("/itemstag2/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/userstag3/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]

# Tags with Enums
@app.get("/itemsenum/", tags=[Tags.items])
async def get_items():
    return ["Portal gun", "Plumbus"]


@app.get("/usersenum/", tags=[Tags.users])
async def read_users():
    return ["Rick", "Morty"]

# Summary and description
@app.post(
    "/itemssummery/",
    response_model=Item15,
    summary="Create an item",
    description="Create an item with all the information, name, description, price, tax and a set of unique tags",
)
async def create_item(item: Item15):
    return item

# Description from docstring
@app.post("/itemsdocstring/", response_model=Item15, summary="Create an item")
async def create_item(item: Item15):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# Response description
@app.post(
    "/itemsresponsedescriptions/",
    response_model=Item15,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(item: Item15):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

# Deprecate a path operation
@app.get("/itemsdeprication/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]


@app.get("/usersdeprication/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]


@app.get("/elementsdepricaition/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]

# JSON Compatible Encoder
# Using the jsonable_encoder
@app.put("/itemsencoder/{id}")
def update_item(id: str, item: Item17):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return fake_db

# Body - Updates
# Update replacing with PUT
items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/itemsbody1/{item_id}", response_model=Item18)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/itemsbody2/{item_id}", response_model=Item18)
async def update_item(item_id: str, item: Item18):
    update_item_encoded = jsonable_encoder(item)
    print(update_item_encoded)
    items[item_id] = update_item_encoded
    return items

# Classes as Dependencies
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/itemsdepends/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/usersdepends/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

# Shortcut
class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit

@app.get("/itemsshortcut/")
async def read_items(commons: Annotated[CommonQueryParams, Depends()]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response

# Dependencies in path operation decorators
# Add dependencies to the path operation decorator
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


# @app.get("/itemsdepends1/", dependencies=[Depends(verify_token), Depends(verify_key)])
# async def read_items():
#     return [{"item": "Foo"}, {"item": "Bar"}]

# Global Dependencies
@app.get("/itemsglobal/")
async def read_items():
    return [{"item": "Portal Gun"}, {"item": "Plumbus"}]


@app.get("/usersglobal/")
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]

# Security - First Steps
@app.get("/itemstokens1/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}



# Create a user model

def fake_decode_token(token):
    return User(username=token + "fakedecoded", email="john@example.com", full_name="John Doe")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

# Simple OAuth2 with Password and Bearer

# login =================================================================================================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDBs(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenDatas(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Tokens)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users1/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return current_user


@app.get("/users1/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time =datetime.now()
    response = await call_next(request)
    process_time = datetime.now() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response