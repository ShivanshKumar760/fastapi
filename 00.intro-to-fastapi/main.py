from fastapi import FastAPI

app = FastAPI()


@app.get("/") #this is a decorator that tells FastAPI that this function should be called when a GET request is made to the root URL ("/")
# it wraps the function read_root() and adds some additional functionality to it, such as handling the request and response, and making it available as an endpoint in the API.
def read_root():
    return {"Hello": "World"}