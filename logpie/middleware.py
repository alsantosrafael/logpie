

import time
from fastapi import Request, Response
from logpie.context import generate_request_id, request_id
import logpie.metrics as metrics

async def enrich_log(request: Request, call_next):
  start_time = time.time()
  request_id.set(generate_request_id())
  metrics.requests_total.inc()
  try: 
    response: Response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

  finally:
    request_id.set(None)
