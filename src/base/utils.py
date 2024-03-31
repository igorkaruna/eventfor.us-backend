from django.http import JsonResponse


def build_response(detail: str = "OK", status: int = 200) -> JsonResponse:
    response_data = {
        "detail": detail,
    }
    response_data = {key: value for key, value in response_data.items() if value is not None}
    return JsonResponse(response_data, status=status)
