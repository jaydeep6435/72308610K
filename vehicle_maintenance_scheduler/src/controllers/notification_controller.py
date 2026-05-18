from rest_framework.views import APIView
from src.utils.responses import success_response, error_response
from src.services.notification_priority_service import NotificationPriorityEngine
from src.config.settings import ConfigLoader
from src.utils.http_client import http_client
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class NotificationController(APIView):
    """
    Controller responsible for fetching and ranking Priority Notifications.
    """
    def get(self, request):
        Log("backend", "info", "controller", "Priority notifications fetch request received")
        try:
            # 1. Fetch raw notifications via dynamic URL
            url = ConfigLoader.get_api_url("notifications")
            response_data = http_client.get(url)
            
            # Extract list from potential wrapper
            raw_notifications = response_data.get("notifications", []) if isinstance(response_data, dict) else response_data
            if not isinstance(raw_notifications, list):
                raw_notifications = []
            
            # 2. Rank using O(n log k) Engine
            top_notifications = NotificationPriorityEngine.get_top_notifications(raw_notifications, top_k=10)
            
            # 3. Standardized Production Response
            Log("backend", "debug", "controller", "Priority notifications successfully fetched and ranked")
            return success_response(
                message="Priority notifications fetched successfully", 
                data={"notifications": top_notifications}
            )
            
        except Exception as e:
            Log("backend", "error", "controller", f"Failed to fetch priority notifications: {e}")
            return error_response(message="Failed to fetch priority notifications", data={"detail": str(e)})
