import logging
from typing import Callable

from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.response import Response


logger = logging.getLogger(__name__)


class ExceptionHandlingMiddleware(MiddlewareMixin):
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            # Log the incoming request
            logger.info(f"Processing request to {request.path}")
            response = self.get_response(request)
            # Optionally, log successful response status
            logger.info(f"Response status: {response.status_code} for request to {request.path}")
        except Exception as e:
            logger.error(f"Exception encountered during request to {request.path}: {e}")
            response = self.process_exception(request, e)
        return response

    @staticmethod
    def process_exception(request: HttpRequest, exception: Exception):
        if isinstance(exception, ValidationError):
            error_details = exception.messages if hasattr(exception, "messages") else [str(exception)]
            response_data = {
                "detail": "Invalid request parameters.",
                "errors": error_details,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.exception(f"Unhandled exception: {exception}")
            response_data = {"detail": "Internal server error."}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
