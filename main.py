from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False


items_db: dict[int, Item] = {}
current_id = 0


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        return {"error": "Item not found"}
    return items_db[item_id]


@app.post("/items/")
def create_item(item: Item):
    global current_id
    current_id += 1
    items_db[current_id] = item
    return {"id": current_id, **item.model_dump()}
