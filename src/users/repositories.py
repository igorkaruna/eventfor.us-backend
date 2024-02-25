from typing import Any

from base.repositories import BaseRepository
from users.models import User


class UserRepository(BaseRepository[User]):
    model = User

    @classmethod
    def create_user(cls, **kwargs: Any) -> User:
        return cls.model.objects.create_user(**kwargs)

    @classmethod
    def create_superuser(cls, **kwargs: Any) -> User:
        return cls.model.objects.create_superuser(**kwargs)

    @classmethod
    def get_by_email(cls, email: str) -> User:
        return cls.model.objects.get(email=email)
