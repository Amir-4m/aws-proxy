import jwt

from functools import lru_cache

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_text
from django.contrib.auth.models import AnonymousUser

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header

from ..models import Inspector
from ..utils.jwt import jwt_decode_handler


class InspectorJWTAuthentication(BaseAuthentication):
    """
    Token based authentication using the JSON Web Token standard.
    """
    www_authenticate_realm = 'api'

    def get_jwt_value(self, request):
        auth = get_authorization_header(request).split()
        auth_header_prefix = 'jwt'
        if not auth or smart_text(auth[0].lower()) != auth_header_prefix:
            return None
        print(auth)
        if len(auth) == 1:
            msg = _('Invalid Authorization header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid Authorization header. Credentials string '
                    'should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        return auth[1]

    def authenticate_header(self, request):
        """
        Return a string to be used as the value of the `WWW-Authenticate`
        header in a `401 Unauthenticated` response, or `None` if the
        authentication scheme should return `403 Permission Denied` responses.
        """
        return '{0} realm="{1}"'.format('JWT', self.www_authenticate_realm)

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        try:
            payload = jwt_decode_handler(jwt_value)
        except jwt.ExpiredSignatureError:
            msg = _('Signature has expired.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.DecodeError:
            msg = _('Error decoding signature.')
            raise exceptions.AuthenticationFailed(msg)
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed()
        payload['inspector'] = self.authenticate_credentials(payload.get('inspector_id'))
        return AnonymousUser(), payload

    @staticmethod
    @lru_cache(maxsize=None)
    def authenticate_credentials(inspector_id):
        """
        Returns an user of the existing service
        """
        try:
            inspector = Inspector.objects.values().get(id=inspector_id)
        except Inspector.DoesNotExist:
            msg = _('Invalid signature.')
            raise exceptions.AuthenticationFailed(msg)

        return inspector
