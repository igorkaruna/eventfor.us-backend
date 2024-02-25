from django.db.models import Model, QuerySet

from base.repositories import BaseRepository, ModelType
from events.models import Event, EventCategory


class EventRepository(BaseRepository[Event]):
    model: Model = Event

    @classmethod
    def get_all(cls) -> QuerySet[ModelType]:
        return cls.model.objects.select_related("creator", "category").all()


class EventCategoryRepository(BaseRepository[EventCategory]):
    model: Model = EventCategory

    @classmethod
    def get_all(cls) -> QuerySet[ModelType]:
        return cls.model.objects.all()
