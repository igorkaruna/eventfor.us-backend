from django.contrib import admin
from django.urls import include, path

from base import settings


urlpatterns = [
    path("", include("events.urls")),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
