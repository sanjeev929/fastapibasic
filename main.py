from enum import Enum
from datetime import datetime, time, timedelta
from fastapi import FastAPI,Query,Path,Body,Cookie,Header,status,Response
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel,Field,HttpUrl,EmailStr
from typing import Annotated,Union,List,Dict,Any
from uuid import UUID

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

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
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

app = FastAPI()

# Basic
@app.get("/hi")
async def root(response:Response):
    response.status_code=status.HTTP_201_CREATED
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