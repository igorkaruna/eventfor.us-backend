import pytest
from rest_framework.test import APIClient

from users.repositories import UserRepository


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserRepository.create_user(
        email="john@johndoe.com",
        first_name="John",
        last_name="Doe",
        password="abc123",
    )
