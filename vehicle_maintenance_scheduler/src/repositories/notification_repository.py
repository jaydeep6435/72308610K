from src.utils.http_client import http_client
from src.config.settings import ConfigLoader
from src.handlers.exceptions import CustomAPIException
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from logging_middleware import Log

class NotificationRepository:
    """
    Repository layer for managing Notification delivery via external API.
    """
    @staticmethod
    def send_notification(payload: dict) -> dict:
        Log("backend", "info", "repository", "Sending external notification")
        
        url = ConfigLoader.get_api_url("notifications")
        
        try:
            response = http_client.post(url, json_data=payload)
            Log("backend", "debug", "repository", "Notification sent successfully")
            return response
            
        except Exception as e:
            Log("backend", "error", "repository", f"Failed to fetch notification data: {e}")
            raise CustomAPIException(f"Notification API resolution error: {str(e)}")
