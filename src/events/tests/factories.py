from datetime import timedelta

import factory
from django.db.models import Model
from django.utils import timezone
from factory.django import DjangoModelFactory

from events.constants import EventStatus
from events.models import Event, EventAttendance, EventCategory
from users.models import User
from users.tests.factories import UserFactory


class EventCategoryFactory(DjangoModelFactory):
    class Meta:
        model: Model = EventCategory

    name: str = factory.Faker("word")
    description: str = factory.Faker("paragraph")


class EventFactory(DjangoModelFactory):
    class Meta:
        model: Model = Event

    creator: User = factory.SubFactory(UserFactory)
    category: EventCategory = factory.SubFactory(EventCategoryFactory)
    name: str = factory.Faker("sentence", nb_words=4)
    status: str = factory.Iterator(EventStatus.Created)
    location: str = factory.Faker("address")
    capacity: int = factory.Faker("random_int", min=0, max=10000)
    description: str = factory.Faker("paragraph")
    start_date = factory.LazyFunction(lambda: timezone.now().date() + timedelta(days=1))
    end_date = factory.LazyFunction(lambda: (timezone.now() + timedelta(days=2)).date())


class EventAttendanceFactory(DjangoModelFactory):
    class Meta:
        model = EventAttendance

    user: User = factory.SubFactory(UserFactory)
    event: Event = factory.SubFactory(EventFactory)
    timestamp = factory.LazyFunction(timezone.now)
