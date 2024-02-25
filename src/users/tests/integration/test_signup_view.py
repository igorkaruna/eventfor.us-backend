import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from base.tests import BaseTestView
from users.repositories import UserRepository


pytestmark = pytest.mark.django_db


class TestSignUpView(BaseTestView):
    endpoint = reverse("signup")

    def test__sign_up__success(self, api_client: APIClient) -> None:
        # when
        response = api_client.post(
            self.endpoint,
            data={
                "email": "john@jhondoe.com",
                "first_name": "John",
                "last_name": "Doe",
                "password": "abc123",
            },
        )

        # then
        self._common_check(response, expected_status=201)

        created_user = UserRepository.get_by_email(email="john@jhondoe.com")
        assert created_user, "User was expected to be created"

        response_data = response.json()
        assert response_data["id"] == str(created_user.id)
        assert response_data["email"] == "john@jhondoe.com"
        assert response_data["first_name"] == "John"
        assert response_data["last_name"] == "Doe"

    def test__sign_up_empty_data__failed(self, api_client: APIClient) -> None:
        # when
        response = api_client.post(self.endpoint, data={})

        # then
        self._common_check(response, expected_status=400)

        response_data = response.json()
        assert response_data == {
            "email": ["This field is required."],
            "first_name": ["This field is required."],
            "last_name": ["This field is required."],
            "password": ["This field is required."],
        }

    def test__sign_up_with_existing_email__failed(self, api_client, user):
        # given
        signup_data = {
            "email": user.email,
            "first_name": "John",
            "last_name": "Doe",
            "password": "abc123",
        }

        # when
        response = api_client.post(self.endpoint, data=signup_data)

        # then
        self._common_check(response, expected_status=400)

        response_data = response.json()
        assert response_data == {
            "email": ["user with this email already exists."],
        }
