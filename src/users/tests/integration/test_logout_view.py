import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from base.tests import BaseTest
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestLogout(BaseTest):
    endpoint = reverse("logout")

    def test__logout__success(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()
        refresh = RefreshToken.for_user(user)

        # when
        response = api_client.post(
            self.endpoint,
            data={
                "refresh_token": str(refresh),
            },
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

        # then
        self._common_check(response, expected_status=204, expected_content_type=None)

    def test__logout_invalid_refresh_token__failed(self, api_client: APIClient) -> None:
        # when
        response = api_client.post(
            self.endpoint,
            data={
                "refresh_token": "invalid_token",
            },
        )

        # then
        self._common_check(response, expected_status=401)

        response_data = response.json()
        assert response_data["detail"] == "Authentication credentials were not provided."

    def test__logout_empty_request_data__failed(self, api_client: APIClient) -> None:
        # when
        response = api_client.post(self.endpoint)

        # then
        self._common_check(response, expected_status=401)

        response_data = response.json()
        assert response_data["detail"] == "Authentication credentials were not provided."
