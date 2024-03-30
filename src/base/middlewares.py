import logging
from typing import Callable, Optional

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)


class ExceptionHandlingMiddleware(MiddlewareMixin):
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request: HttpRequest) -> JsonResponse:
        response = self.get_response(request)
        return response

    @staticmethod
    def process_exception(request: HttpRequest, exception: Exception) -> Optional[JsonResponse]:
        response_data = {}
        status_code = 500

        if isinstance(exception, ValidationError):
            error_details = exception.messages if hasattr(exception, "messages") else [str(exception)]
            response_data["detail"] = "Invalid request parameters."
            response_data["errors"] = error_details
            status_code = 400
        else:
            logger.exception(f"Unhandled exception: {exception}")
            response_data["detail"] = "Internal server error."

        return JsonResponse(response_data, status=status_code, safe=True)
