from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from apps.servers.models import Server

from .serializers import IPProxySerializer
from ..models import Proxy


class IPProxyAPIView(generics.ListAPIView):
    renderer_classes = [JSONRenderer]
    queryset = Proxy.objects.has_ip().filter(
        is_enable=True,
        server__aws_status=Server.AWS_STATUS_RUNNING,
        server__is_enable=True,
        server__connection_status=Server.CONNECTION_STATUS_ACTIVE
    )
    serializer_class = IPProxySerializer
