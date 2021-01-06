from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Inspector


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
