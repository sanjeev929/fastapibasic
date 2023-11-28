from enum import Enum
from fastapi import FastAPI,Query,Path
from pydantic import BaseModel
from typing import Annotated


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

# Basic
@app.get("/")
async def root():
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