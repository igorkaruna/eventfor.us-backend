from typing import Any, Dict

from django.db.models import Model
from rest_framework import serializers

from events.models import Event, EventCategory
from users.serializers import UserSerializer


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = EventCategory
        fields: tuple[str, ...] = ("id", "name", "description")


class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=EventCategory.objects.all(),
        write_only=True,
    )

    class Meta:
        model: Model = Event
        fields: tuple[str, ...] = (
            "id",
            "creator",
            "category",
            "name",
            "status",
            "location",
            "capacity",
            "description",
            "start_date",
            "end_date",
            "created_at",
        )
        read_only_fields: tuple[str, ...] = ("id", "creator", "created_at")

    def to_representation(self, instance: Event) -> Dict[str, Any]:
        representation: Dict[str, Any] = super(EventSerializer, self).to_representation(instance)
        representation.update(category=EventCategorySerializer(instance.category).data)
        return representation
