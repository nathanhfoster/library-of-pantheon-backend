from django.urls import path
from .views import LoginViewSet, RegisterViewSet, UpdateSettingsViewSet

app_name = "users"
urlpatterns = [
    path("login/", LoginViewSet.as_view(), name="api_login"),
    path("register/", RegisterViewSet.as_view(), name="api_register"),
    path("update-settings/<int:pk>/", UpdateSettingsViewSet.as_view(), name="update_settings"),
]
