from fastapi import FastAPI, Depends, Request

app = FastAPI()

async def route_logger(request: Request):
    print(f"Route middleware -> {request.method} {request.url.path}")
    # We dont need next() in FastAPI, the function will be called before the route handler
    # cause we are using Depends() in the route handler
    # and it's not a global middleware, it's a route middleware
    # more specifically it not a middleware, it's a dependency that will be called before the route handler
    # but it can be used as a middleware if we want to, by using it in the global dependencies of the app

@app.get("/public")
async def public():
    return {"message": "No middleware"}

@app.get("/private", dependencies=[Depends(route_logger)])
async def private():
    return {"message": "Route middleware applied"}
