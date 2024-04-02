import pytest

from events.models import EventCategory
from events.repositories import EventCategoryRepository


pytestmark = pytest.mark.django_db


def test_event_category_creation():
    # given
    name = "Sports"
    description = "A test event category description"

    # when
    event_category = EventCategoryRepository.create(name=name, description=description)

    # then
    assert EventCategory.objects.count() == 1, "There should be only one category created"

    created_category = EventCategory.objects.filter(id=event_category.id)
    assert created_category.exists(), "Category with specified id should be created in the database"
