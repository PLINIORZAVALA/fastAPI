from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

app = FastAPI()

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Esquema Pydantic para manejar las solicitudes
class ItemCreate(BaseModel):
    name: str
    description: str | None = None

class ItemUpdate(BaseModel):
    name: str
    description: str | None = None

# Ruta de ejemplo para la raíz
@app.get("/")
def read_root():
    """Devuelve un mensaje de bienvenida."""
    return {"message": "Bienvenido a la API básica de FastAPI"}

# Ruta GET para leer un ítem por ID
@app.get("/items/{item_id}")
def read_item(item_id: int, db: Session = Depends(get_db)):
    """Devuelve información sobre un ítem por su ID."""
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

# Ruta POST para crear un nuevo elemento
@app.post("/items/")
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """Crea un nuevo ítem en la base de datos."""
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Ruta PUT para actualizar un elemento existente
@app.put("/items/{item_id}")
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """Actualiza un ítem existente en la base de datos."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item

# Ruta DELETE para eliminar un elemento
@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Elimina un ítem de la base de datos por su ID."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    db.delete(db_item)
    db.commit()
    return {"message": f"Item {item_id} eliminado exitosamente"}
