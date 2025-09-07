import os
from fastapi import FastAPI, Response
from logpie.config.masking_config import load_masking_config
from logpie.logger import log
from logpie.masking.engine import MaskingEngine
from logpie.middleware import LoggingMiddleware
from prometheus_client import generate_latest
import logpie.metrics as metrics
from logpie.schemas import LogEntry

app = FastAPI(title="LogPie")
engine = MaskingEngine()

metrics.service_info.info(
    {
        "version": os.getenv("APP_VERSION", "dev"),
        "environment": os.getenv("ENVIRONMENT", "local"),
    }
)

app.add_middleware(LoggingMiddleware)


@app.post("/logs")
async def create_log(entry: LogEntry):
    with metrics.mask_latency.time():
        level = entry.level.upper()
        metrics.log_entries_total.labels(level=level).inc()
        if level == "DEBUG":
            log.debug(entry.message)
        elif level == "INFO":
            log.info(entry.message)
        elif level == "WARNING":
            log.warning(entry.message)
        elif level == "ERROR":
            log.error(entry.message)
        elif level == "CRITICAL":
            log.critical(entry.message)
        else:
            log.info(entry.message)

    return {"status": "ok"}


@app.get("/metrics")
def get_metrics():
    return Response(
        generate_latest(), media_type="text/plain; version=0.0.4; charset=utf-8"
    )


@app.get("/health")
async def health_check():
    rules = load_masking_config()
    active_rules_count = len(rules)
    metrics.active_rules_total.set(active_rules_count)

    return {
        "status": "healthy",
        "version": os.getenv("APP_VERSION", "dev"),
        "active_masking_rules": active_rules_count,
        "rules": [rule["name"] for rule in rules],
    }
