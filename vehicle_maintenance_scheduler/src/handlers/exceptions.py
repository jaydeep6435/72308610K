from rest_framework.views import exception_handler
from src.utils.responses import error_response
from rest_framework.exceptions import APIException
from rest_framework import status

class CustomAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred.'
    default_code = 'error'

class ExternalAPIException(CustomAPIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = 'Failed to communicate with external service.'
    default_code = 'external_api_error'

def global_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return error_response(
            message=str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            data=response.data,
            status_code=response.status_code
        )
        
    return error_response(
        message="Internal Server Error",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
