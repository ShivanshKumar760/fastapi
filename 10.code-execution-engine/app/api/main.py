from fastapi import FastAPI
from app.dto.schemas import CodeRequest
from app.service.executor import execute_code

app = FastAPI()


@app.post("/execute")
async def run_code(req: CodeRequest):
    result = execute_code(req.language, req.code, req.input)
    return result