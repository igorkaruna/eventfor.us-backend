from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserLogoutSerializer, UserSignInSerializer, UserSignUpSerializer


class SignUpView(CreateAPIView):
    serializer_class = UserSignUpSerializer


class SignInView(TokenObtainPairView):
    serializer_class = UserSignInSerializer


class LogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh_token"]
        RefreshToken(token=refresh_token).blacklist()
        return Response(status=204)
