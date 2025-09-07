import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from logpie.metrics import requests_total, request_errors_total, request_latency

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        request.state.request_id = request_id
        
        response = None
        try:
            response = await call_next(request)
            return response
        except Exception as _:
            request_errors_total.labels(
                method=request.method, 
                path=request.url.path
            ).inc()
            raise
        finally:
            process_time = time.perf_counter() - start_time
            status_code = response.status_code if response else 500
            
            requests_total.labels(
                method=request.method, 
                path=request.url.path,
                status_code=status_code
            ).inc()
            
            if status_code >= 500:
                request_errors_total.labels(
                    method=request.method, 
                    path=request.url.path
                ).inc()
            
            request_latency.labels(
                method=request.method, 
                path=request.url.path
            ).observe(process_time)
            
            if response:
                response.headers["x-request-id"] = request_id
