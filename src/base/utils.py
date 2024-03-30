from rest_framework.response import Response


def build_response(detail: str = "OK", status: int = 200) -> Response:
    response_data = {
        "detail": detail,
    }
    response_data = {key: value for key, value in response_data.items() if value is not None}
    return Response(response_data, status=status)
