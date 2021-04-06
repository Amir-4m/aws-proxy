from rest_framework.routers import DefaultRouter

from .views import IPProxyViewSet

router = DefaultRouter()
router.register('ip-proxies', IPProxyViewSet)

urlpatterns = router.urls
