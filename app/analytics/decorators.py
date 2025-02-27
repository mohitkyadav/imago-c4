import time
from functools import wraps

from app.analytics.logger import LOG

def log_execution_time(operation_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_time = end_time - start_time

            LOG.info(f"[{operation_name}]: took {execution_time:.4f} seconds to execute")

            return result
        return wrapper
    return decorator
