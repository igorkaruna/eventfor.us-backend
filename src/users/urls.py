from django.urls import path

from users.views import LogoutView, RetrieveSavedEventsView, SignInView, SignUpView


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("signin/", SignInView.as_view(), name="signin"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("saved_events/", RetrieveSavedEventsView.as_view(), name="saved_events"),
]
