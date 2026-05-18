import requests
import time
from typing import Dict, Any, Optional
from src.config.environment import env
from src.handlers.exceptions import ExternalAPIException
import sys
import os

# Ensure logging_middleware is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class BaseHttpClient:
    """
    Centralized HTTP client for repository layers.
    Includes robust retries, Bearer auth, and exception safety.
    """
    def __init__(self, max_retries: int = 3, backoff_factor: int = 2, timeout: float = 5.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        
    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {env.ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        
    def _request_with_retry(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        attempt = 0
        kwargs['headers'] = self._get_headers()
        kwargs['timeout'] = self.timeout
        
        while attempt <= self.max_retries:
            try:
                response = requests.request(method, url, **kwargs)
                response.raise_for_status()
                # Assuming all APIs return JSON data
                return response.json()
            except requests.exceptions.RequestException as e:
                attempt += 1
                Log("backend", "warn", "utils", f"HTTP {method} to {url} failed. Attempt {attempt}/{self.max_retries}. Error: {e}")
                if attempt > self.max_retries:
                    Log("backend", "error", "utils", f"HTTP {method} to {url} permanently failed after {self.max_retries} retries.")
                    raise ExternalAPIException(f"Failed to communicate with {url}") from e
                
                # Exponential backoff
                time.sleep(self.backoff_factor ** attempt)
        
        raise ExternalAPIException(f"Unreachable external API condition for {url}")

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Reusable GET utility"""
        return self._request_with_retry('GET', url, params=params)

    def post(self, url: str, json_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Reusable POST utility"""
        return self._request_with_retry('POST', url, json=json_data)
        
http_client = BaseHttpClient()
