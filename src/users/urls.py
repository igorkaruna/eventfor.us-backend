from django.urls import path

from users.views import GetSavedEventsView, GetUserView, LogoutView, SignInView, SignUpView


urlpatterns = [
    # authentication-related urls
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # other urls
    path("<str:uuid>/", GetUserView.as_view(), name="user_details"),
    path("<str:uuid>/saved_events/", GetSavedEventsView.as_view(), name="user_saved_events"),
]
