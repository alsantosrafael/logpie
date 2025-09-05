from fastapi import FastAPI
from logpie.logger import log
from logpie.middleware import enrich_log

app = FastAPI(title="LogPie")

app.middleware("http")(enrich_log)

@app.get("/")
def hello_logpie():
    log.info("Healthcheck init", route="/")
    return {"message": "LogPie service running!"}

