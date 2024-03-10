from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from events.constants import SaveEventConstant
from events.filters import EventFilter
from events.permissions import IsEventCreator
from events.repositories import EventRepository
from events.serializers import EventSerializer
from users.repositories import UserProfileRepository


class EventViewSet(ModelViewSet):
    queryset = EventRepository.get_all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsEventCreator)

    def perform_create(self, serializer: EventSerializer) -> None:
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=["POST"], permission_classes=(IsAuthenticated,))
    def toggle_save(self, request: Request, pk: str = None) -> Response:
        event = self.get_object()
        event_saved = UserProfileRepository.toggle_save_event(self.request.user.profile, event)
        toggle_action = SaveEventConstant.Saved if event_saved else SaveEventConstant.Removed
        return Response({"event_id": event.id, "action": toggle_action}, status=200)
