from fastapi import FastAPI

from enum import Enum

from typing import Any

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
async def read_item(item_id: int):
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
async def read_file(your_file_path_param: str):
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