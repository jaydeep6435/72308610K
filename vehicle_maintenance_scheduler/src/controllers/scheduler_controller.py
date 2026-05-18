from rest_framework.views import APIView
from src.utils.responses import success_response, error_response
from src.services.scheduler_service import SchedulerService
from src.serializers.optimization_serializer import OptimizationResponseSerializer
from src.handlers.exceptions import CustomAPIException
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class SchedulerController(APIView):
    """
    Controller responsible for triggering the Vehicle Maintenance Optimizer.
    Strictly delegates logic to SchedulerService.
    """
    def get(self, request, depot_id):
        Log("backend", "info", "controller", f"Schedule generation request received for depot {depot_id}")
        try:
            # 1. Controller-level basic validation
            if depot_id <= 0:
                Log("backend", "warn", "controller", f"Invalid depot ID supplied: {depot_id}")
                return error_response(message="Validation failed", data={"depot_id": "Must be greater than 0"})

            # 2. Delegate to Service Layer
            schedule_data = SchedulerService.generate_schedule(depot_id)
            
            # 3. Serialize and strict response validation
            serializer = OptimizationResponseSerializer(data=schedule_data)
            if serializer.is_valid():
                Log("backend", "debug", "controller", "Schedule generation successful and schema validated")
                return success_response(message="Operation completed successfully", data=serializer.data)
            else:
                Log("backend", "error", "controller", "Generated schedule failed schema validation")
                return error_response(message="Validation failed", data=serializer.errors)
                
        except CustomAPIException as e:
            Log("backend", "error", "controller", f"Schedule generation failed due to internal error: {e}")
            return error_response(message=str(e))
        # Any unexpected exceptions will be gracefully caught by the GlobalExceptionMiddleware
