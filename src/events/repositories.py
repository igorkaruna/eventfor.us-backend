from typing import Optional

from django.db.models import Case, CharField, Count, ExpressionWrapper, F, QuerySet, Value, When, fields
from django.db.models.functions import ExtractDay, TruncMonth
from django.utils import timezone

from base.repositories import BaseRepository, ModelType
from events.models import Event, EventAttendance, EventCategory
from users.models import User


class EventRepository(BaseRepository[Event]):
    model = Event

    @classmethod
    def get_all(cls) -> QuerySet[ModelType]:
        return cls.model.objects.with_related().all()

    @classmethod
    def get_events_with_attendees_count(cls) -> QuerySet:
        return cls.model.objects.with_related().annotate(attendees_count=Count("attendees"))

    @classmethod
    def get_monthly_attendance_statistics(cls) -> QuerySet:
        return (
            EventAttendance.objects.annotate(month=TruncMonth("timestamp"))
            .values("month")
            .annotate(total_attendees=Count("user"))
            .order_by("month")
        )

    @classmethod
    def get_event_duration_analysis(cls) -> QuerySet:
        return (
            cls.model.objects.annotate(
                duration_days=ExpressionWrapper(
                    F("end_date") - F("start_date"),
                    output_field=fields.DurationField(),
                ),
                duration_days_extracted=ExtractDay("duration_days"),
                duration_category=Case(
                    When(duration_days_extracted__lte=1, then=Value("Short")),
                    When(duration_days_extracted__lte=7, then=Value("Medium")),
                    default=Value("Long"),
                    output_field=CharField(),
                ),
            )
            .values("duration_category")
            .annotate(total=Count("id"))
            .order_by("-duration_category")
        )

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
            cls.model.objects.with_related()
            .annotate(attendees_count=Count("attendees"))
            .filter(id=event_id, start_date__gt=timezone.now(), attendees_count__lt=F("capacity"))
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
