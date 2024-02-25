from django.urls import path

from users.views import LogoutView, SignInView, SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
