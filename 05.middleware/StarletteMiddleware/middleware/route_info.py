from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class RouteInfoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"You are on route: {request.url.path} and method: {request.method}")
        
        response = await call_next(request)
        return response
