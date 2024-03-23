from typing import Optional

from django.db.models import Count, F, QuerySet
from django.db.models.functions import TruncMonth
from django.utils import timezone

from base.repositories import BaseRepository, ModelType
from events.models import Event, EventAttendance, EventCategory
from users.models import User


class EventRepository(BaseRepository[Event]):
    model = Event

    @classmethod
    def get_all(cls) -> QuerySet[ModelType]:
        return cls.model.objects.select_related("creator", "category").all()

    @classmethod
    def get_events_with_attendees_count(cls) -> QuerySet:
        return cls.model.objects.annotate(attendees_count=Count("attendees")).select_related("creator", "category")

    @classmethod
    def get_monthly_event_creation_statistics(cls) -> QuerySet:
        return (
            cls.model.objects.annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

    @classmethod
    def get_open_event_for_attendance(cls, event_id: str) -> Optional[Event]:
        return (
            cls.model.objects.annotate(attendees_count=Count("attendees"))
            .filter(id=event_id, start_date__gt=timezone.now(), attendees_count__lt=F("capacity"))
            .select_related("creator", "category")
            .first()
        )

    @classmethod
    def toggle_attendance(cls, user: User, event: Event) -> bool:
        attendance, created = EventAttendance.objects.get_or_create(user=user, event=event)

        if not created:
            attendance.delete()
            return False

        return True


class EventAttendanceRepository(BaseRepository[EventAttendance]):
    model = EventAttendance

    @classmethod
    def is_user_attending_event(cls, user: User, event: Event) -> bool:
        return cls.model.objects.filter(user=user, event=event).exists()


class EventCategoryRepository(BaseRepository[EventCategory]):
    model = EventCategory
