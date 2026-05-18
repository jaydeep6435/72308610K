from .constants import ALLOWED_STACKS, ALLOWED_LEVELS, ALLOWED_PACKAGES
from .exceptions import LogValidationException

def validate_payload(stack: str, level: str, package: str, message: str) -> None:
    """
    Validates log payload against Afformed requirements.
    Raises LogValidationException if constraints are not met.
    """
    if not isinstance(message, str) or not message.strip():
        raise LogValidationException("Message cannot be empty or non-string.")
        
    if stack not in ALLOWED_STACKS:
        raise LogValidationException(f"Invalid stack '{stack}'. Allowed: {ALLOWED_STACKS}")
        
    if level not in ALLOWED_LEVELS:
        raise LogValidationException(f"Invalid level '{level}'. Allowed: {ALLOWED_LEVELS}")
        
    if package not in ALLOWED_PACKAGES:
        raise LogValidationException(f"Invalid package '{package}'. Allowed: {ALLOWED_PACKAGES}")
