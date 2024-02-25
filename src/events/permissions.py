from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import View

from events.models import Event


class IsEventCreator(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Event) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.creator == request.user
