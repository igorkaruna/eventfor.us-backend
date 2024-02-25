import pytest
from django.utils import timezone

from events.constants import EventStatus
from events.models import Event
from events.repositories import EventRepository
from events.tests.factories import EventCategoryFactory
from users.tests.factories import UserFactory


@pytest.mark.django_db
def test_event_creation():
    # given
    creator = UserFactory()
    category = EventCategoryFactory()

    name = "Tomorrow land"
    status = EventStatus.Created
    location = "Los Angeles, USA"
    capacity = 100
    description = "A test event description"
    start_date = timezone.now().date()
    end_date = timezone.now().date() + timezone.timedelta(days=1)

    # when
    event = EventRepository.create(
        creator=creator,
        category=category,
        name=name,
        status=status,
        location=location,
        capacity=capacity,
        description=description,
        start_date=start_date,
        end_date=end_date,
    )

    # then
    assert Event.objects.count() == 1, "There should be only one event created"

    created_event = Event.objects.filter(id=event.id)
    assert created_event.exists(), "Event with specified id should be created in the database"
