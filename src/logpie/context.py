import contextvars
import uuid

request_id = contextvars.ContextVar("request_id")

def generate_request_id():
  return uuid.uuid4().hex
