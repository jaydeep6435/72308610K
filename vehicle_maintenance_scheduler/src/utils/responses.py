from rest_framework.response import Response
from rest_framework import status

def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "message": message,
        "data": data or {}
    }, status=status_code)

def error_response(message="Error", data=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "message": message,
        "data": data or {}
    }, status=status_code)

def validation_response(errors):
    return Response({
        "success": False,
        "message": "Validation Failed",
        "data": errors
    }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

def paginated_response(data, total_pages, current_page, total_items):
    return Response({
        "success": True,
        "message": "Data fetched successfully",
        "data": {
            "items": data,
            "meta": {
                "total_pages": total_pages,
                "current_page": current_page,
                "total_items": total_items
            }
        }
    }, status=status.HTTP_200_OK)
