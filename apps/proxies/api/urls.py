from django.urls import path

from .views import IPProxyAPIView

app_name = 'proxies'

urlpatterns = [
    path("ip-proxies/", IPProxyAPIView.as_view(), name="ip_proxies")
]
