from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.routes import auth, projects

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(projects.router, prefix="/project")