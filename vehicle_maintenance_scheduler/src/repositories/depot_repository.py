from src.utils.http_client import http_client
from src.config.settings import ConfigLoader
from src.handlers.exceptions import CustomAPIException
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class DepotRepository:
    """
    Repository layer for managing Depot external API communications.
    """
    @staticmethod
    def get_depot(depot_id: int) -> dict:
        Log("backend", "info", "repository", f"Fetching depot data for ID {depot_id}")
        
        # Centralized configuration usage
        url = ConfigLoader.get_api_url(f"depots/{depot_id}")
        
        try:
            response = http_client.get(url)
            Log("backend", "debug", "repository", f"Depot {depot_id} API response received")
            return response
        except Exception as e:
            Log("backend", "error", "repository", f"Failed to fetch depot data: {e}")
            raise CustomAPIException(f"Depot API resolution error: {str(e)}")
