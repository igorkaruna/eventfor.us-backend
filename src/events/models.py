from uuid import uuid4

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from events.constants import EventStatus
from events.managers import EventManager
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
    capacity = models.BigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10_000)])
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    objects = EventManager()

    class Meta:
        verbose_name: str = "event"
        verbose_name_plural: str = "events"

    def clean(self):
        """
        Validates the event dates to ensure the start date precedes the end date.

        This method is particularly important for handling partial updates, such as with PATCH operations,
        where the start and end dates might not be included in the request. It checks that both dates are
        provided and not None before comparing them. This avoids a TypeError that could occur when attempting
        to compare NoneType with a date object and ensures the integrity of the event's date range.

        Raises:
            ValidationError: If the start date is not before the end date.
        """
        if (self.start_date and self.end_date) and self.start_date >= self.end_date:
            raise ValidationError({"start_date": _("The start date must be before the end date.")})

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
