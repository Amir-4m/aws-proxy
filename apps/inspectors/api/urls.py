from django.urls import path

from .views import ObtainTokenAPIView, InspectorLogAPIView, InquiryServersAPIView

urlpatterns = [
    path("obtain-token/", ObtainTokenAPIView.as_view(), name="obtain_token"),
    path("inspected-server/", InspectorLogAPIView.as_view(), name="inspected_server"),
    path("inquiry-server/", InquiryServersAPIView.as_view(), name="inquiry_server")

]
