from django.contrib import admin
from django.urls import include, path

from base import settings
from events.urls import router as events_router


urlpatterns = [
    path("admin/", admin.site.urls),
    path("events/", include(events_router.urls)),
    path("users/", include("users.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
