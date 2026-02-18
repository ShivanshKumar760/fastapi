from fastapi import APIRouter,Depends, Request

async def route_logger(request: Request):
    print(f"Route middleware -> {request.method} {request.url.path}")
    # We dont need next() in FastAPI, the function will be called before the route handler
    # cause we are using Depends() in the route handler
    # and it's not a global middleware, it's a route middleware
    # more specifically it not a middleware, it's a dependency that will be called before the route handler
    # but it can be used as a middleware if we want to, by using it in the global dependencies of the app

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(route_logger)]
)

@router.get("/dashboard")
async def dashboard():
    return {"msg": "Admin only"}


@router.get("/test")
async def dashboard():
    return {"msg": "Router specific middleware test"}