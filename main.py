from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple FastAPI Backend")

# -----------------------------
# STEP 1: Inline 'Database'
# -----------------------------
database = {}  # stores all items in memory

# -----------------------------
# STEP 2: Data Model
# -----------------------------
class Item(BaseModel):
    name: str
    description: str
    price: float

# -----------------------------
# STEP 3: API Endpoints
# -----------------------------

# POST - Create an item
@app.post("/items/")
def create_item(item_id: int, item: Item):
    if item_id in database:
        raise HTTPException(status_code=400, detail="Item already exists")
    database[item_id] = item
    return {"message": "Item created", "item": item}

# GET - Retrieve an item
@app.get("/items/{item_id}")
def get_item(item_id: int):
    item = database.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": item}

# PUT - Replace an item completely
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    database[item_id] = updated_item
    return {"message": "Item updated", "item": updated_item}

#PATCH - Partial update (update only given fields)
@app.patch("/items/{item_id}")
def patch_item(item_id: int, partial_item: dict):
    item = database.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    updated_data = item.model_dump()
    updated_data.update(partial_item)
    database[item_id] = Item(**updated_data)
    return {"message": "Item partially updated", "item": database[item_id]}

# DELETE - Delete an item
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in database:
        raise HTTPException(status_code=404, detail="Item not found")
    del database[item_id]
    return {"message": "Item deleted successfully"}

