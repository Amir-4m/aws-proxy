from django.urls import path, include

urlpatterns = [
    path('v1/inspectors/', include("apps.inspectors.api.urls")),
    path('v1/proxies/', include("apps.proxies.api.urls", namespace='v1')),
    path('v2/proxies/', include("apps.proxies.api.urls", namespace='v2')),
]
