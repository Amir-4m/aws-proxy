from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.servers.models import Server
from apps.servers.api.serializers import ServerSerializer

from .authentications import InspectorJWTAuthentication
from .permissions import InspectorPermission
from .serializers import InspectedServerSerializer
from ..models import Inspector, InspectedServer


class ObtainTokenAPIView(APIView):

    def post(self, request, *args, **kwargs):
        """
        API view that returns a token based on request inspector id.
            body:
                service_id: string/inspector id of specific service

        """
        service_id = request.data.get('inspector_id')
        service = get_object_or_404(
            Inspector,
            id=service_id,
            is_enable=True,
        )

        return Response({"token": service.get_jwt_token()})


class InquiryServersAPIView(generics.ListAPIView):
    queryset = Server.objects.filter(connection_status=Server.CONNECTION_STATUS_CHECK)
    authentication_classes = (InspectorJWTAuthentication,)
    permission_classes = (InspectorPermission,)
    serializer_class = ServerSerializer


class InspectedServersAPIView(generics.CreateAPIView):
    queryset = InspectedServer.objects.all()
    authentication_classes = (InspectorJWTAuthentication,)
    permission_classes = (InspectorPermission,)
    serializer_class = InspectedServerSerializer

    def perform_create(self, serializer):
        serializer.save(inspector=self.request.auth['inspector'])
