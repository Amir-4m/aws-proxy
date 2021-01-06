from django.urls import path, include

urlpatterns = [
    path('inspectors/', include("apps.inspectors.api.urls")),
]
