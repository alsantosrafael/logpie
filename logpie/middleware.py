

from fastapi import Request, Response
from logpie.context import generate_request_id, request_id

async def enrich_log(request: Request, call_next):
  request_id.set(generate_request_id())

  try: 
    response: Response = await call_next(request)
    return response

  finally:
    request_id.set(None)
