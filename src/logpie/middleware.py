import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from logpie.metrics import requests_total, request_latency

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id
        try:
            response = await call_next(request)
        finally:
            process_time = time.perf_counter() - start_time
            requests_total.labels(method=request.method, path=request.url.path).inc()
            request_latency.labels(method=request.method, path=request.url.path).observe(process_time)
        response.headers["x-request-id"] = request_id
        return response
