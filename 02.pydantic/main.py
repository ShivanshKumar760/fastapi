from fastapi import FastAPI
from dto.RequestDTO import RequestDTO
from models.Products import products as products_db
app = FastAPI()

@app.get("/products")
def get_products():
    return products_db