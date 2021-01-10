from django.urls import path

from .views import ObtainTokenAPIView, InspectedServersAPIView, InquiryServersAPIView

urlpatterns = [
    path("obtain-token/", ObtainTokenAPIView.as_view(), name="obtain_token"),
    path("inspected-server/", InspectedServersAPIView.as_view(), name="inspected_server"),
    path("inquiry-server/", InquiryServersAPIView.as_view(), name="inquiry_server")

]
