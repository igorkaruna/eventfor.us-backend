from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotAllowed
from django.urls import include, path
from django.views.static import serve as serve_static
from rest_framework.request import Request

from base import settings


def get_swagger(request: Request) -> HttpResponse:
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    return serve_static(request, "swagger.json", document_root=settings.BASE_DIR)


urlpatterns = [
    # default urls
    path("admin/", admin.site.urls),
    # api urls
    path("api/", include("events.urls")),
    path("api/swagger/", get_swagger, name="swagger"),
    path("api/users/", include("users.urls")),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
