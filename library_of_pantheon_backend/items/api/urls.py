from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import ItemViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('items', ItemViewSet)
app_name = "items"

urlpatterns = router.urls
