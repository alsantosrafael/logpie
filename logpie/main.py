from fastapi import FastAPI
from logpie.logger import log

app = FastAPI(title="LogPie")

@app.get("/")
def hello_logpie():
    log.info("Healthcheck init", route="/")
    return {"message": "LogPie service running!"}

