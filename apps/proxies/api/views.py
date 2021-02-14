from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from apps.servers.models import Server

from .serializers import IPProxySerializerV1, IPProxySerializerV2
from ..models import Proxy


class IPProxyViewSet(viewsets.GenericViewSet):
    renderer_classes = [JSONRenderer]
    queryset = Proxy.objects.has_ip().filter(
        is_enable=True,
        server__aws_status=Server.AWS_STATUS_RUNNING,
        server__is_enable=True,
        server__connection_status=Server.CONNECTION_STATUS_ACTIVE
    )
    serializer_class = IPProxySerializerV1

    @action(methods=['get'], detail=False)
    def version1(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def version2(self, request, *args, **kwargs):
        serializer = IPProxySerializerV2(self.get_queryset(), many=True)
        return Response(serializer.data)
