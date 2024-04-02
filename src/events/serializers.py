from typing import Any, Dict

from django.core.exceptions import ValidationError
from django.db.models import Model
from rest_framework import serializers

from events.models import Event, EventCategory
from events.repositories import EventCategoryRepository
from users.serializers import UserSerializer


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model: Model = EventCategory
        fields = ("id", "name", "description")


class EventSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=EventCategoryRepository.get_all(),
        write_only=True,
    )

    class Meta:
        model: Model = Event
        fields = (
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
        read_only_fields = ("id", "creator", "created_at")

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        instance = Event(**data)

        try:
            instance.clean()
        except ValidationError as ex:
            raise serializers.ValidationError(ex.messages)

        return data

    def to_representation(self, instance: Event) -> Dict[str, Any]:
        representation: Dict[str, Any] = super(EventSerializer, self).to_representation(instance)
        representation.update(category=EventCategorySerializer(instance.category).data)
        return representation
