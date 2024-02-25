import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from base.tests import BaseTestView
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestSignInView(BaseTestView):
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

        user_data = response_data.get("user")
        assert user_data, "User data was expected in the response"
        assert user_data == {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

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
