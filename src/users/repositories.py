from typing import Any

from django.db import transaction

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
    def get_saved_events(cls, profile: UserProfile) -> bool:
        return profile.saved_events.all()

    @classmethod
    def toggle_save_event(cls, profile: UserProfile, event: Event) -> bool:
        already_saved = profile.saved_events.filter(id=event.id).exists()

        if already_saved:
            profile.saved_events.remove(event)
        else:
            profile.saved_events.add(event)

        return not already_saved
