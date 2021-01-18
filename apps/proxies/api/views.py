from rest_framework import generics

from .serializers import IPProxySerializer
from ..models import Proxy


class IPProxyAPIView(generics.ListAPIView):
    queryset = Proxy.objects.has_ip().filter(is_enable=True)
    serializer_class = IPProxySerializer
