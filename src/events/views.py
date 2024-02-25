from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from events.permissions import IsEventCreator
from events.repositories import EventRepository
from events.serializers import EventSerializer


class EventViewSet(ModelViewSet):
    queryset = EventRepository.get_all()
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsEventCreator)

    def perform_create(self, serializer: EventSerializer) -> None:
        serializer.save(creator=self.request.user)
