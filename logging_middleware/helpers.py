import os
import threading
from typing import Optional
from dotenv import load_dotenv

# Explicitly bind to the correct environment file to prevent thread context loss
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'vehicle_maintenance_scheduler', '.env'))
load_dotenv(dotenv_path=env_path)

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
