from fastapi import FastAPI
from router import router

app = FastAPI()
app.include_router(router)

app.get("/public")
async def public():
    return {"message": "No middleware"}