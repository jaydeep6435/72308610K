import time
import logging
from typing import Callable, Any
from .constants import DEFAULT_MAX_RETRIES, DEFAULT_BACKOFF_FACTOR
from .exceptions import LogNetworkException

fallback_logger = logging.getLogger("afformed_logging_fallback")

def execute_with_retry(
    func: Callable[..., Any], 
    max_retries: int = DEFAULT_MAX_RETRIES, 
    backoff_factor: int = DEFAULT_BACKOFF_FACTOR,
    *args, 
    **kwargs
) -> Any:
    """
    Executes a given function with exponential backoff retries.
    Gracefully handles exceptions and raises LogNetworkException only after max retries.
    """
    attempt = 0
    last_error = None
    
    while attempt <= max_retries:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_error = e
            attempt += 1
            if attempt > max_retries:
                fallback_logger.error(f"Execution failed after {max_retries} retries. Error: {e}")
                raise LogNetworkException(f"Max retries exceeded: {e}") from e
            
            sleep_time = backoff_factor ** attempt
            fallback_logger.warning(f"Network error: {e}. Retrying in {sleep_time} seconds (Attempt {attempt}/{max_retries})...")
            time.sleep(sleep_time)
