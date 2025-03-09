from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, Item

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Docker!"}

@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    try :
        db_item = Item(name=item.name, description=item.description)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        return {"error": str(e)}

@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    try:
        return db.query(Item).all()
    except Exception as e:
        return {"error": str(e)}
