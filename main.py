from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel



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


