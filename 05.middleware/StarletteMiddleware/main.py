from fastapi import FastAPI
from middleware.logger import LoggerMiddleware
from middleware.route_info import RouteInfoMiddleware

app = FastAPI()
app.add_middleware(LoggerMiddleware)
app.add_middleware(RouteInfoMiddleware)

@app.get("/")
async def home():
    return {"message": "Home route"}

@app.post("/create")
async def create_item():
    return {"message": "POST route"}

@app.put("/update")
async def update_item():
    return {"message": "PUT route"}

@app.delete("/delete")
async def delete_item():
    return {"message": "DELETE route"}