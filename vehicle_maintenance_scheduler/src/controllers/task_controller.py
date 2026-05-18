from rest_framework.views import APIView
from src.utils.responses import success_response, error_response
from src.config.settings import ConfigLoader
from src.utils.http_client import http_client
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class TaskController(APIView):
    """
    Handles HTTP Requests for Vehicle Tasks.
    """
    def get(self, request):
        Log("backend", "info", "controller", "Tasks fetch request received")
        try:
            # Leverage the repository layer instead of inline HTTP calls
            from src.repositories.vehicle_repository import VehicleRepository
            tasks_data = VehicleRepository.get_all_tasks()
            
            Log("backend", "debug", "controller", "Tasks fetch request completed successfully")
            return success_response(message="Operation completed successfully", data={"vehicles": tasks_data})
        except Exception as e:
            Log("backend", "error", "controller", f"Tasks fetch failed: {e}")
            return error_response(message="Failed to fetch tasks", data={"detail": str(e)})
