# 🍰 LogPie

### Structured Logging + Data Masking Platform (FastAPI + Prometheus)

[![Python](https://img.shields.io/badge/Python-3.11-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-△-009688)]()
[![Docker](https://img.shields.io/badge/Docker-ready-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## 🚀 Overview

**LogPie** é uma plataforma de **logging estruturado** com foco em **compliance (LGPD/GDPR)**,  
**observabilidade empresarial** e **developer experience**.

- ✅ Logs estruturados em JSON
- ✅ Data Masking Engine configurável (emails, CPFs, telefones, cartões)
- ✅ Middleware injetando `request_id`
- ✅ Prometheus Metrics (`/metrics`)
- ✅ Dockerfile multi-stage + Compose cross-OS
- ✅ Pronto pra integração com Loki + Grafana + OpenTelemetry (roadmap)

---

## ✨ Demo Visual

### Antes (sem masking)

```json
{
  "level": "INFO",
  "message": "Usuário logou",
  "context": {
    "email": "fulano@example.com",
    "cpf": "123.456.789-00"
  },
  "request_id": "abc-123"
}
```

### Depois (com LogPie)

```json
{
  "level": "INFO",
  "message": "Usuário logou",
  "context": {
    "email": "[email_masked]",
    "cpf": "[cpf_masked]"
  },
  "request_id": "abc-123"
}
```

---

## 🐳 Quickstart com Docker

```bash
# Clonar o repositório
git clone https://github.com/alsantosrafael/logpie
cd logpie

# Subir a stack
docker compose up --build
```

A API ficará disponível em `http://localhost:8000`

- `GET /health` → Health-check
- `POST /logs` → Enviar log estruturado
- `GET /metrics` → Métricas Prometheus

---

## 📊 Observabilidade

LogPie já exporta métricas nativas via `prometheus_client`.

### Métricas disponíveis:

- `logpie_requests_total` → total de requisições HTTP
- `logpie_masked_total{data_type}` → totais de dados mascarados por tipo
- `logpie_mask_latency_seconds` → histogram de tempo de mascaramento

### Roadmap próximo:

- [ ] Enviar logs pro **Grafana Loki**
- [ ] Dashboard pronto no Grafana
- [ ] OpenTelemetry traces com correlação `request_id`

### 📊 PromQL

#### P99 Latency

```promql
histogram_quantile(0.99, sum(rate(logpie_request_duration_seconds_bucket[5m])) by (le))
```

#### Error Rate (%)

```promql
(
sum(rate(logpie_request_errors_total[5m])) /
sum(rate(logpie_requests_total[5m]))
) \* 100
```

#### Throughput (RPS)

```promql
sum(rate(logpie_requests_total[5m]))
```

#### Masking Performance

```promql
histogram_quantile(0.95, sum(rate(logpie_mask_duration_seconds_bucket[5m])) by (le))
```

---

## ⚙️ Developer Experience

- **Makefile**: encapsula build/run/logs
- **Docker Compose** compatível Linux/macOS
- **README visual** (isso aqui 💎)
- Código **clean** e organizado em `logpie/`

---

## 🎯 Roadmap Sprint Final

1. **README visual** (esse aqui) ✅
2. **Testes sérios** (pytest + masking edge cases)
3. **CI/CD básico** (lint + pytest workflow)
4. **Observabilidade completa** (Loki + OTel)

---

## 📜 License

MIT © Rafael Almeida Santos
