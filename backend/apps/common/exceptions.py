from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error responses."""
    response = exception_handler(exc, context)

    if response is not None:
        response.data = {
            "success": False,
            "message": str(exc.detail) if hasattr(exc, 'detail') else str(exc),
            "status_code": response.status_code,
        }
    else:
        logger.error("Unhandled exception: %s", str(exc), exc_info=True)
        response = Response(
            {
                "success": False,
                "message": "Internal server error",
                "status_code": 500,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
