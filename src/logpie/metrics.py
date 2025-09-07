from prometheus_client import Counter, Histogram, Gauge, Info

# Throughput - requests per second
requests_total = Counter(
    "logpie_requests_total", "Total HTTP requests", ["method", "path", "status_code"]
)

# Error Rate - 5xx responses
request_errors_total = Counter(
    "logpie_request_errors_total",
    "Total HTTP requests with status >= 500",
    ["method", "path"],
)

# Latency P99 - with realistic buckets for logging service
request_latency = Histogram(
    "logpie_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "path"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Masking-specific metrics
mask_latency = Histogram(
    "logpie_mask_duration_seconds",
    "Time spent masking sensitive data",
    buckets=[0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1],
)

mask_operations_total = Counter(
    "logpie_mask_operations_total",
    "Total masking operations by rule type",
    ["rule_name"],
)

# System health
active_rules_total = Gauge(
    "logpie_active_rules_total", "Number of active masking rules"
)

log_entries_total = Counter(
    "logpie_log_entries_total", "Total log entries processed by level", ["level"]
)

# Service info
service_info = Info("logpie_service_info", "LogPie service information")
