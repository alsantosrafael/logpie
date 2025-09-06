# Stage 1 - Builder
FROM python:3.11-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
  curl gcc build-essential && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
  mv /root/.local/bin/uv /usr/local/bin/uv && \
  uv --version
## Cache guaranteed - No changes in libraries, no need to reinstall
COPY pyproject.toml uv.lock ./
RUN uv sync

COPY . .

# Stage 2 - Runtime
FROM python:3.11-slim AS runner
WORKDIR /app

COPY --from=builder /usr/local/bin/uv /usr/local/bin/uv
COPY --from=builder /app /app
ENV PYTHONPATH=/app/src

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "logpie.main:app", "--host", "0.0.0.0", "--port", "8000"]
