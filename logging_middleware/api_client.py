import requests
from typing import Dict, Any
import logging
from .constants import LOGGING_ENDPOINT_PATH, DEFAULT_TIMEOUT_SECONDS
from .exceptions import LogNetworkException
from .helpers import get_env_variable
from .retry_handler import execute_with_retry

fallback_logger = logging.getLogger("afformed_logging_fallback")

class LoggingAPIClient:
    """
    Centralized HTTP Request Utility for Afformed Logging API.
    Utilizes Bearer token authentication and manages network boundaries.
    """
    def __init__(self):
        # Fallback to hardcoded URL if env is missing, but env var is prioritized.
        base_url = get_env_variable("BASE_URL", "http://4.224.186.213/evaluation-service")
        self.endpoint = f"{base_url.rstrip('/')}{LOGGING_ENDPOINT_PATH}"
        
    def _get_token(self) -> str:
        return get_env_variable("ACCESS_TOKEN", "")

    def _make_request(self, payload: Dict[str, Any]) -> None:
        """Core synchronous HTTP request using python-requests"""
        token = self._get_token()
        if not token:
            fallback_logger.error("ACCESS_TOKEN is missing. Cannot send log to Afformed API.")
            raise LogNetworkException("Missing ACCESS_TOKEN in environment variables.")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            self.endpoint, 
            json=payload, 
            headers=headers, 
            timeout=DEFAULT_TIMEOUT_SECONDS
        )
        response.raise_for_status()

    def send_log(self, payload: Dict[str, Any]) -> None:
        """
        Sends the log payload to the external API using the robust retry mechanism.
        Catches all errors internally to ensure absolute application safety.
        """
        try:
            execute_with_retry(self._make_request, payload=payload)
        except LogNetworkException as e:
            # We catch it here to prevent bubble-up crashes
            fallback_logger.error(f"Failed to send log to external API permanently: {e}")
        except Exception as e:
            # Catch-all to guarantee app stability
            fallback_logger.error(f"Unexpected unhandled error during log transmission: {e}")
