from prometheus_client import Counter, Histogram, generate_latest

requests_total = Counter(
  'logpie_requests_total',
  'Total number of requests process by LogPie'
)

masked_total = Counter(
  'logpie_masked_total',
  'Total number of sensitive items masked by LogPie',
  ['data_type']
)

mask_latency = Histogram(
    'logpie_mask_latency_seconds', 
    'Latency of data masking operations in seconds',
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, float('inf'))
)
