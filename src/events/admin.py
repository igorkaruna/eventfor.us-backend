from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from events.models import Event, EventAttendance, EventCategory
from events.repositories import EventRepository


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return EventRepository.get_events_with_attendees_count()

    def attendees_count(self, obj):
        return obj.attendees_count

    def creator_link(self, obj):
        link = reverse("admin:users_user_change", args=[obj.creator_id])
        return format_html('<a href="{}">{}</a>', link, obj.creator)

    list_display = (
        "id",
        "name",
        "creator_link",
        "category",
        "status",
        "location",
        "start_date",
        "end_date",
        "created_at",
        "attendees_count",
    )

    date_hierarchy = "start_date"

    list_filter = ("status", "category", "location", "start_date", "end_date")
    search_fields = ("id", "name", "creator__username", "location")
    ordering = ("-created_at",)

    attendees_count.admin_order_field = "attendees_count"
    attendees_count.short_description = "Attendees count"
    creator_link.short_description = "Creator"


@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "event", "timestamp")
    search_fields = ("user__username", "event__name")
    list_filter = ("event", "user")


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
    )

    search_fields = ("id", "name")
    ordering = ("name",)
