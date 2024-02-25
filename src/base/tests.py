from rest_framework.response import Response


class BaseTestView:
    endpoint: str = None

    @staticmethod
    def _common_check(
        response: Response,
        expected_status: int = 200,
        expected_content_type: str = "application/json",
    ) -> None:
        """
        Check the response's status code and content type.

        Args:
            response: The response object to check.
            expected_status: The expected status code. Defaults to 200.
            expected_content_type: The expected content type. Defaults to "application/json".

        Raises:
            AssertionError: If the response's status code or content type doesn't match the expected values.
        """
        content_type = response.get("content-type")
        assert content_type == expected_content_type, f"Unexpected content-type: {content_type}"

        status_code = response.status_code
        assert status_code == expected_status, f"Unexpected status code: {status_code}"
