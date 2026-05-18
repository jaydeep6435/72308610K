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
        Log("backend", "info", "repository", "Fetching all depots")
        
        # Centralized configuration usage
        url = ConfigLoader.get_api_url("depots")
        
        try:
            response = http_client.get(url)
            
            # The API returns a dictionary like {"depots": [...]}
            depots_list = response.get("depots", []) if isinstance(response, dict) else response
            if not isinstance(depots_list, list):
                depots_list = []
                
            Log("backend", "debug", "repository", f"Searching for depot ID {depot_id}")
            
            # Iterate to find the exact depot ID
            for d in depots_list:
                # We check ID matching dynamically to prevent type coercion bugs
                if str(d.get("ID")) == str(depot_id) or str(d.get("depotId")) == str(depot_id):
                    Log("backend", "info", "repository", "Matching depot found")
                    return d
                    
            Log("backend", "warn", "repository", f"Depot ID {depot_id} not found")
            raise CustomAPIException(f"Depot with ID {depot_id} does not exist.")
            
        except CustomAPIException as ce:
            raise ce
        except Exception as e:
            Log("backend", "error", "repository", f"Failed to fetch depot data: {e}")
            raise CustomAPIException(f"Depot API resolution error: {str(e)}")
