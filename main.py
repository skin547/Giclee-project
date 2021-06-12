from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from app.api.api import api_router

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return { "item_name" : item.name, "item_id": item_id }

@app.get("/clone")
def get_clone_image():
    return 