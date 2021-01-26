from django.utils import timezone

from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.servers.models import Server
from apps.servers.api.serializers import ServerSerializer

from .authentications import InspectorJWTAuthentication
from .permissions import InspectorPermission
from .serializers import InspectorLogSerializer, RegisterSerializer
from ..models import Inspector, InspectorLog


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response({"token": instance.get_jwt_token()})


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
            pk=service_id,
            is_enable=True,
        )

        return Response({"token": service.get_jwt_token()})


class InquiryServersAPIView(generics.ListAPIView):
    queryset = Server.objects.filter(
        connection_status=Server.CONNECTION_STATUS_CHECK,
        aws_status=Server.AWS_STATUS_RUNNING,
    )
    authentication_classes = (InspectorJWTAuthentication,)
    permission_classes = (InspectorPermission,)
    serializer_class = ServerSerializer


class InspectorLogAPIView(generics.CreateAPIView):
    queryset = InspectorLog.objects.all()
    authentication_classes = (InspectorJWTAuthentication,)
    permission_classes = (InspectorPermission,)
    serializer_class = InspectorLogSerializer

    def perform_create(self, serializer):
        inspector = Inspector.objects.get(id=self.request.auth['inspector_id'])
        serializer.save(inspector=inspector)
