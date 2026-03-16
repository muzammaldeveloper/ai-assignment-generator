"""
Gunicorn Production Configuration.

Optimized for AI Assignment Generator deployment.
"""

import multiprocessing

# ── Server Socket ──
bind = "0.0.0.0:5000"
backlog = 2048

# ── Worker Processes ──
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
graceful_timeout = 30
keepalive = 5

# ── Logging ──
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# ── Process Naming ──
proc_name = "ai_assignment_generator"

# ── Security ──
limit_request_line = 8190
limit_request_fields = 100
limit_request_field_size = 8190