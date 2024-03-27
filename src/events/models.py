from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models

from events.constants import EventStatus
from users.models import User


class EventCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(EventCategory, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=25, default=EventStatus.Created, choices=EventStatus.choices())
    location = models.CharField(max_length=255, db_index=True)
    capacity = models.BigIntegerField(validators=[MinValueValidator(0)])
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name: str = "event"
        verbose_name_plural: str = "events"

    def __str__(self) -> str:
        return self.name


class EventAttendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attendees")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "attendance"
        verbose_name_plural = "attendances"
        constraints = [models.UniqueConstraint(fields=["user", "event"], name="unique_user_event_attendance")]

    def __str__(self) -> str:
        return f"{self.user} attends {self.event}"
