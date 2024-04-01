from django.urls import include, path
from rest_framework.routers import DefaultRouter

from events.views import EventCategoryListView, EventViewSet


router = DefaultRouter()
router.register(r"", EventViewSet)


urlpatterns = [
    path("events/", include(router.urls)),
    path("categories/", EventCategoryListView.as_view(), name="categories_list"),
]
