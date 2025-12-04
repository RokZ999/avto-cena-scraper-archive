import asyncio
import time
from functools import wraps

from Backend.logger.log_config import log


def time_it(func):
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        minutes, seconds = divmod(elapsed_time, 60)
        log.info(f"{func.__name__} - Time: {int(minutes)} minutes and {seconds:.2f} seconds")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        minutes, seconds = divmod(elapsed_time, 60)
        log.info(f"{func.__name__} - Time: {int(minutes)} minutes and {seconds:.2f} seconds")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
