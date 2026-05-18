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
    def get_tasks_for_depot(depot_id: int) -> list:
        Log("backend", "info", "repository", f"Fetching vehicle tasks for depot ID {depot_id}")
        
        url = ConfigLoader.get_api_url(f"depots/{depot_id}/vehicles")
        
        try:
            response = http_client.get(url)
            Log("backend", "debug", "repository", "Vehicle API response received")
            
            # Assuming API returns a list under a 'tasks' or 'data' key, or straight list
            tasks = response.get("data", []) if isinstance(response, dict) else response
            return tasks
            
        except Exception as e:
            Log("backend", "error", "repository", f"Failed to fetch vehicle tasks: {e}")
            raise CustomAPIException(f"Vehicle API resolution error: {str(e)}")
