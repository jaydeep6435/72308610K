from rest_framework.views import APIView
from src.utils.responses import success_response, error_response
from src.config.settings import ConfigLoader
from src.utils.http_client import http_client
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class DepotController(APIView):
    """
    Handles HTTP Requests for Depots.
    Remains thin, delegates fetching to standardized HTTP Client.
    """
    def get(self, request):
        Log("backend", "info", "controller", "Depots fetch request received")
        try:
            url = ConfigLoader.get_api_url("depots")
            response_data = http_client.get(url)
            
            Log("backend", "debug", "controller", "Depots fetch request completed successfully")
            return success_response(message="Operation completed successfully", data=response_data)
        except Exception as e:
            Log("backend", "error", "controller", f"Depots fetch failed: {e}")
            return error_response(message="Failed to fetch depots", data={"detail": str(e)})
