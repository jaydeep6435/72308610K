# Allowed Values Definition
ALLOWED_STACKS = {"backend"}

ALLOWED_LEVELS = {"debug", "info", "warn", "error", "fatal"}

ALLOWED_PACKAGES = {
    "cache", "controller", "cron_job", "db", "domain", 
    "handler", "repository", "route", "service", 
    "auth", "config", "middleware", "utils"
}

# API Configuration
LOGGING_ENDPOINT_PATH = "/logs"

# Retry & Network Configuration
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 2
DEFAULT_TIMEOUT_SECONDS = 5.0
