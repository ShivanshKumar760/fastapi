from fastapi import FastAPI,Request
from functools import wraps
from fastapi.responses import JSONResponse

def route_logger(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if request:
            print(f"Route middleware -> {request.method} {request.url.path}")
        else:
            print("Route middleware -> No request object found")
        response = await func(*args, **kwargs)

        return response
    return wrapper

app = FastAPI()

@app.get("/public")
@route_logger
async def public(request:Request):#remember to add request as a parameter to the route handler, otherwise the middleware will not work
    #as the wraps function will not be able to find the request object in the kwargs and will print "No request object found"
    return JSONResponse(content={"message": "Wraps decorator middleware applied"})

#Not a good way if we have multiple middlewares, we will have to wrap the route handler with multiple decorators, which will make the code messy and hard to read
