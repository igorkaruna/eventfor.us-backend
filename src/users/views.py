from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from base.utils import build_response
from events.serializers import EventSerializer
from users.repositories import UserProfileRepository, UserRepository
from users.serializers import LogoutSerializer, SignUpSerializer, UserSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer


class SignInView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data["refresh_token"]
        RefreshToken(token=refresh_token).blacklist()
        return build_response(detail="Refresh token was successfully blacklisted.")


class GetUserView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return UserRepository.get(id=self.kwargs.get("uuid"))


class GetSavedEventsView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        user = UserRepository.get(id=self.kwargs.get("uuid"))
        return UserProfileRepository.get_saved_events(user.profile)
