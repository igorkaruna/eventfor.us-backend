from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from events.serializers import EventSerializer
from users.repositories import UserProfileRepository


class RetrieveSavedEventsView(ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserProfileRepository.get_saved_events(self.request.user.profile)
