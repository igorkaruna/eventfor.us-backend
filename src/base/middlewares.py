import logging
from typing import Callable

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)


class ExceptionHandlingMiddleware(MiddlewareMixin):
    def __init__(self, get_response: Callable) -> None:
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        logger.info(f"Processing request to {request.path}")

        try:
            response = self.get_response(request)
            logger.info(f"Response status: {response.status_code} for request to {request.path}")
        except Exception as ex:
            logger.error(f"Exception encountered during request to {request.path}: {ex}")
            response = self.process_exception(request, ex)

        return response

    @staticmethod
    def process_exception(request: HttpRequest, exception: Exception):
        if isinstance(exception, ValidationError):
            error_details = exception.messages if hasattr(exception, "messages") else [str(exception)]
            response_data = {
                "detail": "Invalid request parameters.",
                "errors": error_details,
            }
            status_code = 400

        else:
            logger.exception(f"Unhandled exception: {exception}")
            response_data = {"detail": "Internal server error."}
            status_code = 500

        return JsonResponse(response_data, status=status_code)
