import logging
import traceback
from .validators import validate_payload
from .api_client import LoggingAPIClient
from .exceptions import LogValidationException
from .helpers import run_in_background

# System fallback logger used for tracking internal middleware errors
fallback_logger = logging.getLogger("afformed_logging_fallback")

class AfformedLogger:
    """
    Core logger class orchestrating validation and dispatch.
    """
    _client = LoggingAPIClient()

    @classmethod
    def process_log(cls, stack: str, level: str, package: str, message: str) -> None:
        """
        Synchronous internal process function.
        Validates the payload and delegates to the API client.
        """
        try:
            validate_payload(stack, level, package, message)
        except LogValidationException as e:
            fallback_logger.error(f"Log validation failed: {e} | Payload: stack='{stack}', level='{level}', package='{package}', message='{message}'")
            return
            
        payload = {
            "stack": stack,
            "level": level,
            "package": package,
            "message": message
        }
        
        # Send to API Client
        try:
            cls._client.send_log(payload)
        except Exception as e:
            # Absolute worst-case safety net
            fallback_logger.error(f"Critical error in logger process. System remains stable. Details: {e}")


def Log(stack: str, level: str, package: str, message: str) -> None:
    """
    Mandatory Reusable Logging Function.
    
    Logs an event to the Afformed Evaluation Service without blocking the main application flow.
    Ensures that failures (validation, network, auth) fail gracefully and do not crash the service.
    
    Args:
        stack (str): e.g., 'backend'
        level (str): e.g., 'debug', 'info', 'warn', 'error', 'fatal'
        package (str): e.g., 'service', 'controller', 'middleware'
        message (str): The log message body.
    """
    try:
        # Run asynchronously to avoid blocking main application thread
        run_in_background(AfformedLogger.process_log, stack, level, package, message)
    except Exception as e:
        fallback_logger.error(f"Failed to dispatch background log task: {e}\n{traceback.format_exc()}")
