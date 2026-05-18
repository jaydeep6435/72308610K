from .environment import env
from .constants import AppConstants

class ConfigLoader:
    @staticmethod
    def get_api_url(endpoint: str) -> str:
        return f"{env.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
