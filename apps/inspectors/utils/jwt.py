import jwt

from datetime import datetime
from calendar import timegm

from django.conf import settings

JWT_SETIINGS = getattr(settings, 'JWT_AUTH', dict())


def jwt_payload_handler(payload=dict()):
    if payload.get('exp') is None:
        payload['exp'] = datetime.utcnow() + JWT_SETIINGS['JWT_EXPIRATION_DELTA']

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if JWT_SETIINGS.get('JWT_ALLOW_REFRESH'):
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if JWT_SETIINGS.get('JWT_AUDIENCE') is not None:
        payload['aud'] = JWT_SETIINGS['JWT_AUDIENCE']

    if JWT_SETIINGS.get('JWT_ISSUER') is not None:
        payload['iss'] = JWT_SETIINGS['JWT_ISSUER']

    return payload


def jwt_encode_handler(payload):
    return jwt.encode(
        payload,
        JWT_SETIINGS.get('JWT_SECRET_KEY', settings.SECRET_KEY),
        JWT_SETIINGS.get('JWT_ALGORITHM', 'HS256'),
    ).decode('utf-8')


def jwt_decode_handler(token):
    return jwt.decode(
        token,
        settings.SECRET_KEY,
    )
