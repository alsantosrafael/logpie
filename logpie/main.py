from fastapi import FastAPI, Response
from logpie.logger import log
from logpie.masking.engine import MaskingEngine
from logpie.middleware import enrich_log
from prometheus_client import generate_latest
import logpie.metrics as metrics
from logpie.schemas import LogEntry

app = FastAPI(title="LogPie")
engine = MaskingEngine()

app.middleware("http")(enrich_log)

@app.post("/logs")
async def create_log(entry: LogEntry):
    masked_context = engine.mask_log_entry(entry.context)

    with metrics.mask_latency.time():
        level = entry.level.upper()
    if level == "DEBUG":
        log.debug(entry.message, extra=masked_context)
    elif level == "INFO":
        log.info(entry.message, extra=masked_context)
    elif level == "WARNING":
        log.warning(entry.message, extra=masked_context)
    elif level == "ERROR":
        log.error(entry.message, extra=masked_context)
    elif level == "CRITICAL":
        log.critical(entry.message, extra=masked_context)
    else:
        log.info(entry.message, extra=masked_context)

    return {"status": "ok", "masked_context": masked_context}

@app.get("/metrics")
def get_metrics():
    return Response(generate_latest(), media_type="text/plain; version=0.0.4; charset=utf-8")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
