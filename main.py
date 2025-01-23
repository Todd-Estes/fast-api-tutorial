from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from typing import Any

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

@app.get("/")
async def root():
  return {"message": "Hello World"}

'''
  Path Parameters
'''

@app.get("/items/{item_id}")
async def read_item(item_id: int) -> dict[str, int]:
  return {"item_id": item_id}


# enum path parameters
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName) -> dict[str, str]:
  # compare against eumeration members
  if model_name is ModelName.alexnet:
    return {"model_name": model_name, "message": "Deep Learning FTW!"}
  # compare against acutual value ("lenet"), or:
  if model_name.value == ModelName.lenet.value:
      return {"model_name": model_name, "message": "LeCNN all the images"}

  return {"model_name": model_name, "message": "Have some residuals"}

# file path parameters
@app.get("/files/{your_file_path_param:path}")
async def read_file(your_file_path_param: str) -> dict[str, str]:
  return {"file_path": your_file_path_param}

'''
  Query Parameters

  You can declare multiple path parameters and query parameters at the same time,
  FastAPI knows which is which.

  You don't have to declare them in any specific order.

  They will be detected by name.

  When you declare a default value for non-path parameters (for now, we have only
  seen query parameters), then it is not required.

  If you don't want to add a specific value but just make it optional, set the default as None.

  But when you want to make a query parameter required, you can just not declare any default value.

  item_id => path parameter => required
  needy => required / no defaut value
  skip => not required / has default value
  limit => not required / no default value
'''

@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str,
    needy: str,
    skip: int = 0,
    limit: int | None = None
)-> dict[str, Any]:
    # (Alternate) -> dict[str, str | int | None]:
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item

'''
  Request Body

  You can declare path parameters and request body at the same time.

  FastAPI will recognize that the function parameters that match path
  parameters should be taken from the path, and that function parameters
  that are declared to be Pydantic models should be taken from the request body.
'''
async def create_item(item: Item) -> dict[str, Any]:
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item) -> dict[str, Any]:
    return {"item_id": item_id, **item.model_dump()} #unpack (spread) item key/value pairs into dict

'''
  You can also declare body, path and query parameters, all at the same time.

  FastAPI will recognize each of them and take the data from the correct place.

  The function parameters will be recognized as follows:

  If the parameter is also declared in the path, it will be used as a path parameter.
  If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
  If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
'''
@app.put("/items/{item_id}")
async def update_item_with_query(item_id: int, item: Item, q: str) -> dict[str, Any]:
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result