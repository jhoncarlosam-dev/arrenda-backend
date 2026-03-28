from slowapi import Limiter
from slowapi.util import get_remote_address

# Keyed by client IP. Default limits apply to every route unless overridden.
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
