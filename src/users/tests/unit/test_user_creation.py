import pytest

from users.models import User, UserProfile
from users.repositories import UserRepository


pytestmark = pytest.mark.django_db


def test__user_creation():
    # given
    email = "johndoe@eventfor.us"
    first_name = "John"
    last_name = "Doe"
    password = "abc123"

    # when
    user = UserRepository.create_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )

    # then
    assert User.objects.count() == 1, "Only one user should be created"
    assert UserProfile.objects.count() == 1, "Only one user profile should be created"

    created_user = User.objects.get(id=user.id)
    assert created_user, "User with specified id should be created in the database"
    assert created_user.is_active, "User should be active by default"
    assert not created_user.is_verified, "User shouldn't be verified by default"
    assert not created_user.is_superuser, "User shouldn't be superuser by default"


def test__super_user_creation():
    # given
    email = "johndoe@eventfor.us"
    first_name = "John"
    last_name = "Doe"
    password = "abc123"

    # when
    superuser = UserRepository.create_superuser(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )

    # then
    assert User.objects.count() == 1, "There should be only one user created"

    created_superuser = User.objects.get(id=superuser.id)
    assert created_superuser, "User with specified id should be created in the database"
    assert created_superuser.is_active, "Superuser should be active by default"
    assert created_superuser.is_verified, "Superuser should be verified by default"
    assert created_superuser.is_superuser, "Superuser should be superuser by default"
