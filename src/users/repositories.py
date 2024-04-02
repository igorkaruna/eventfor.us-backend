from typing import Any

from django.db import transaction
from django.db.models import QuerySet

from base.repositories import BaseRepository
from events.models import Event
from users.models import User, UserProfile


class UserRepository(BaseRepository[User]):
    model = User

    @classmethod
    def create_user(cls, **kwargs: Any) -> User:
        with transaction.atomic():
            user = cls.model.objects.create_user(**kwargs)
            UserProfileRepository.create(user=user)

        return user

    @classmethod
    def create_superuser(cls, **kwargs: Any) -> User:
        with transaction.atomic():
            super_user = cls.model.objects.create_superuser(**kwargs)
            UserProfileRepository.create(user=super_user)

        return super_user


class UserProfileRepository(BaseRepository[UserProfile]):
    model = UserProfile

    @classmethod
    def get_saved_events(cls, profile: UserProfile) -> QuerySet:
        return profile.saved_events.all()

    @classmethod
    def toggle_save_event(cls, profile: UserProfile, event: Event) -> bool:
        if profile.saved_events.filter(id=event.id).exists():
            profile.saved_events.remove(event)
            return False
        else:
            profile.saved_events.add(event)
            return True
