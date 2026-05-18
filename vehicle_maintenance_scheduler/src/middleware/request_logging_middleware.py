import time
import sys
import os
from django.utils.deprecation import MiddlewareMixin

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Tracks request paths, execution times, and HTTP statuses.
    Logs to Afformed globally.
    """
    def process_request(self, request):
        request.start_time = time.time()
        Log("backend", "info", "handler", f"Incoming request: {request.method} {request.path}")

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            execution_time = time.time() - request.start_time
            status_code = response.status_code
            
            if status_code >= 500:
                Log("backend", "error", "handler", f"Request failed: {request.method} {request.path} - Status: {status_code} in {execution_time:.3f}s")
            elif status_code >= 400:
                Log("backend", "warn", "handler", f"Request warning: {request.method} {request.path} - Status: {status_code} in {execution_time:.3f}s")
            else:
                Log("backend", "debug", "handler", f"Request completed: {request.method} {request.path} - Status: {status_code} in {execution_time:.3f}s")
                
        return response
