import sys
import os
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class GlobalExceptionMiddleware(MiddlewareMixin):
    """
    Catches all unhandled exceptions globally and formats them
    into the standardized Error JSON format.
    """
    def process_exception(self, request, exception):
        Log("backend", "fatal", "handler", f"Unhandled Server Exception: {str(exception)}")
        
        return JsonResponse({
            "success": False,
            "message": "Internal server error occurred.",
            "errors": {
                "detail": str(exception)
            }
        }, status=500)
