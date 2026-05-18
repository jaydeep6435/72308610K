import os
import threading
from typing import Optional

def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """
    Safely fetch an environment variable. 
    This prevents hardcoding credentials in the package.
    """
    return os.environ.get(var_name, default)

def run_in_background(func, *args, **kwargs):
    """
    Run a function in a separate daemon thread to prevent 
    external network calls from blocking the main application thread.
    """
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.daemon = True
    thread.start()
    return thread
