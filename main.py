from fastapi import FastAPI

app = FastAPI()

# Ruta de ejemplo para la raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API básica de FastAPI"}

# Ruta de ejemplo con parámetros
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

# Ruta para crear un nuevo elemento
@app.post("/items/")
def create_item(name: str, description: str = None):
    return {"name": name, "description": description}
