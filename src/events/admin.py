from django.contrib import admin

from events.models import Event, EventCategory


class EventCategoryAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = (
        "id",
        "name",
        "description",
    )

    search_fields: tuple[str, ...] = ("id", "name")
    ordering: tuple[str, ...] = ("name",)


class EventAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = (
        "id",
        "name",
        "creator",
        "category",
        "status",
        "location",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter: tuple[str, ...] = ("status", "category", "location", "start_date", "end_date")
    search_fields: tuple[str, ...] = ("id", "name", "creator__username", "location")
    ordering: tuple[str, ...] = ("-created_at",)
    date_hierarchy: tuple[str, ...] = "start_date"


admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(Event, EventAdmin)
