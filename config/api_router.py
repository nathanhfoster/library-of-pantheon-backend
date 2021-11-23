from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from library_of_pantheon_backend.users.api.views import UserViewSet
from library_of_pantheon_backend.items.api.views import ItemViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("items", ItemViewSet)

router.urls

app_name = "api"
urlpatterns = router.urls + [
    path('', include("library_of_pantheon_backend.items.api.urls")),
    path('auth/', include("library_of_pantheon_backend.users.api.urls")),
]
