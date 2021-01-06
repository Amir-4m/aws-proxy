from django.urls import path

from .views import ObtainTokenAPIView

urlpatterns = [
    path("obtain-token/", ObtainTokenAPIView.as_view(), name="obtain_token"),
]
