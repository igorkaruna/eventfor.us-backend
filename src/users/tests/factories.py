import factory
from django.db.models import Model
from factory.django import DjangoModelFactory

from users.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model: Model = User

    email: str = factory.Faker("email")
    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    password: str = factory.PostGenerationMethodCall("set_password", "abc123")
