import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from base.tests import BaseTest
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestSignIn(BaseTest):
    endpoint = reverse("signin")

    def test__sign_in__success(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()

        # when
        response = api_client.post(
            self.endpoint,
            data={
                "email": user.email,
                "password": "abc123",
            },
        )

        # then
        self._common_check(response, expected_status=200)

        response_data = response.json()
        assert response_data.get("access"), "Access token is missing"
        assert response_data.get("refresh"), "Refresh token is missing"

    def test__sign_in_wrong_password__failed(self, api_client: APIClient) -> None:
        # given
        user = UserFactory()

        # when
        response = api_client.post(
            self.endpoint,
            data={
                "email": user.email,
                "password": "wrongpassword",
            },
        )

        # then
        self._common_check(response, expected_status=401)

        response_data = response.json()
        assert response_data["detail"] == "No active account found with the given credentials"

    def test__sign_in_nonexistent_user__failed(self, api_client: APIClient) -> None:
        # when
        response = api_client.post(
            self.endpoint,
            data={
                "email": "nonexistent@user.com",
                "password": "password123",
            },
        )

        # then
        self._common_check(response, expected_status=401)

        response_data = response.json()
        assert response_data["detail"] == "No active account found with the given credentials"
