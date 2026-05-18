class LoggingMiddlewareException(Exception):
    """Base exception for the logging middleware package."""
    pass

class LogValidationException(LoggingMiddlewareException):
    """Raised when log payload validation against Afformed schema fails."""
    pass

class LogNetworkException(LoggingMiddlewareException):
    """Raised when the logging API network call fails after retries."""
    pass
