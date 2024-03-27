import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from base.tests import BaseTest
from users.tests.factories import UserFactory


pytestmark = pytest.mark.django_db


class TestGetUserView(BaseTest):
    def test__get_user__success(self, api_client: APIClient) -> None:
        user = UserFactory()

        # when
        response = api_client.get(
            reverse(
                "user_details",
                args=[str(user.id)],
            ),
        )

        # then
        self._common_check(response, expected_status=200)

        response_data = response.json()
        assert response_data["id"] == str(user.id)
        assert response_data["email"] == user.email
        assert response_data["first_name"] == user.first_name
        assert response_data["last_name"] == user.last_name

    def test__user_not_found__failed(self, api_client: APIClient) -> None:

        # when
        response = api_client.get(
            reverse(
                "user_details",
                args=["d98df0d1-d6c4-43d2-9464-d2981e8f7074"],
            ),
        )

        # then
        self._common_check(response, expected_status=404)

        response_data = response.json()
        assert response_data["detail"] == "No User matches the given query."
