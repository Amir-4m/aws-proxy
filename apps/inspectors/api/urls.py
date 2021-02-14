from django.urls import path

from .views import InspectorLogAPIView, InquiryServersAPIView, RegisterAPIView

app_name = 'inspectors'

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("inspected-server/", InspectorLogAPIView.as_view(), name="inspected_server"),
    path("inquiry-server/", InquiryServersAPIView.as_view(), name="inquiry_server")
]
