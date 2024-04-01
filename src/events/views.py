from typing import Any, Dict

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet

from base.settings import REDIS_CONFIGURATION
from base.utils import build_response
from events.constants import EventAttendanceIntent, EventSaveAction
from events.filters import EventFilter
from events.permissions import IsEventCreator
from events.repositories import EventCategoryRepository, EventRepository
from events.serializers import EventCategorySerializer, EventSerializer
from users.repositories import UserProfileRepository


class EventCategoryListView(ListAPIView):
    queryset = EventCategoryRepository.get_all()
    serializer_class = EventCategorySerializer


class EventViewSet(ModelViewSet):
    queryset = EventRepository.get_all()
    serializer_class = EventSerializer
    filterset_class = EventFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsEventCreator)

    def perform_create(self, serializer: EventSerializer) -> None:
        serializer.save(creator=self.request.user)

    @method_decorator(cache_page(timeout=REDIS_CONFIGURATION["TIMEOUT"], key_prefix="events_list"))
    def list(self, request: Request, *args: str, **kwargs: Dict[str, Any]):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def attend(self, request: Request, pk: str = None) -> JsonResponse:
        if not (event := EventRepository.get_open_event_for_attendance(event_id=pk)):
            return build_response(detail="The event is not open for attendance.", status=400)

        event_participated = EventRepository.toggle_attendance(user=request.user, event=event)
        attendance_intent = EventAttendanceIntent.Reserved if event_participated else EventAttendanceIntent.Canceled
        return build_response(detail=f"Attendance {attendance_intent.lower()}.")

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def toggle_save(self, request: Request, pk: str) -> JsonResponse:
        event = EventRepository.get(id=pk)
        event_saved = UserProfileRepository.toggle_save_event(profile=request.user.profile, event=event)
        toggle_action = EventSaveAction.Saved if event_saved else EventSaveAction.Removed
        return build_response(detail=f"Event {toggle_action.lower()} successfully.")
