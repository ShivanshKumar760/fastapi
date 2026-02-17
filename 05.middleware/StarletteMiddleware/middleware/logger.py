from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        print(f"[LOGGER] Incoming: {request.method} {request.url.path}")

        response = await call_next(request)

        process_time = time.time() - start_time
        print(f"[LOGGER] Completed in {process_time:.4f}s")

        return response
    