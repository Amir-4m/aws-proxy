from django.urls import path

from .views import IPProxyAPIView

urlpatterns = [
    path("ip-proxies/", IPProxyAPIView.as_view(), name="ip_proxies")
]
