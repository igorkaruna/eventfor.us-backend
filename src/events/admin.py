from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from events.models import Event, EventAttendance, EventCategory
from events.repositories import EventRepository


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    change_list_template = "admin/event_list.html"

    def get_queryset(self, request):
        return EventRepository.get_events_with_attendees_count()

    def attendees_count(self, obj):
        return obj.attendees_count

    def creator_link(self, obj):
        link = reverse("admin:users_user_change", args=[obj.creator_id])
        return format_html('<a href="{}">{}</a>', link, obj.creator)

    @classmethod
    def get_monthly_attendance_statistics(cls):
        stats = EventRepository.get_monthly_attendance_statistics()
        return (
            format_html_join(
                "\n",
                "<li>{}: {} attendees</li>",
                ((stat["month"].strftime("%B %Y"), stat["total_attendees"]) for stat in stats),
            )
            or "No data"
        )

    @classmethod
    def get_event_duration_analysis(cls):
        analysis = EventRepository.get_event_duration_analysis()
        return (
            format_html_join(
                "\n",
                "<li>{}: {} events</li>",
                (
                    (
                        item["duration_category"],
                        item["total"],
                    )
                    for item in analysis
                ),
            )
            or "No data"
        )

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
    list_display = ("id", "name", "description")
    search_fields = ("id", "name")
    ordering = ("name",)
