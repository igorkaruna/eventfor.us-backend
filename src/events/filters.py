from django.db.models import Model
from django_filters.rest_framework import CharFilter, DateFilter, FilterSet

from events.models import Event


class EventFilter(FilterSet):
    category = CharFilter(field_name="category__id")
    creator = CharFilter(field_name="creator__id")
    location = CharFilter(field_name="location", lookup_expr="icontains")
    start_date_gte = DateFilter(field_name="start_date", lookup_expr="gte")

    class Meta:
        model: Model = Event
        fields: tuple[str, ...] = ("creator", "category", "location", "start_date_gte")
