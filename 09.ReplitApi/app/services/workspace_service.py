import os
from pathlib import Path 
# BASE_DIR = os.getcwd()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(f"Current working directory: {BASE_DIR}")
WORKSPACES_DIR= os.path.join(BASE_DIR, 'workspaces')
print(f"Workspaces directory: {WORKSPACES_DIR}")
os.makedirs(WORKSPACES_DIR, exist_ok=True)

def create_workspace(user_id,project_name):
    path = os.path.join(WORKSPACES_DIR, f"{user_id}_{project_name}")
    if not os.path.exists(path):
        os.makedirs(path)
        with open(os.path.join(path, "main.py"), "w") as f:
             f.write("""
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Hello World"}
""")
        with open(f"{path}/requirements.txt", "w") as f:
            f.write("fastapi\nuvicorn\n")

    return path

# create_workspace(1,"test_project")
