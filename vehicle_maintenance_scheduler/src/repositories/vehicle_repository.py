from src.utils.http_client import http_client
from src.config.settings import ConfigLoader
from src.handlers.exceptions import CustomAPIException
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class VehicleRepository:
    """
    Repository layer for managing Vehicle external API communications.
    """
    @staticmethod
    def get_all_tasks() -> list:
        Log("backend", "info", "repository", "Fetching vehicle maintenance tasks")
        
        url = ConfigLoader.get_api_url("vehicles")
        
        try:
            response = http_client.get(url)
            Log("backend", "debug", "repository", "Vehicle API response received")
            
            # Afformed vehicles API returns: {"vehicles": [...]}
            tasks = response.get("vehicles", []) if isinstance(response, dict) else response
            return tasks
            
        except Exception as e:
            Log("backend", "error", "repository", f"Failed to fetch vehicle tasks: {e}")
            raise CustomAPIException(f"Vehicle API resolution error: {str(e)}")
