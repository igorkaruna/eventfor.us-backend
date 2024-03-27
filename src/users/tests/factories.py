import factory
from factory.django import DjangoModelFactory

from users.models import User, UserProfile


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email: str = factory.Faker("email")
    first_name: str = factory.Faker("first_name")
    last_name: str = factory.Faker("last_name")
    password: str = factory.PostGenerationMethodCall("set_password", "abc123")

    @factory.post_generation
    def post_create(self, create, extracted, **kwargs):
        if not create:
            return

        UserProfileFactory(user=self)


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user: User = factory.SubFactory(UserFactory)
