from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.inspectors.utils.jwt import jwt_payload_handler, jwt_encode_handler
from apps.servers.models import Server


class Inspector(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('name'), max_length=120)
    is_enable = models.BooleanField(_('enabled?'), default=True)

    def __str__(self):
        return self.name

    def get_payload(self):
        payload = {
            'inspector_id': self.id,
            'exp': self.created_time.utcnow() + timedelta(days=10 * 365)
        }
        return jwt_payload_handler(payload)

    def get_jwt_token(self):
        return jwt_encode_handler(self.get_payload())


class InspectedServer(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='inspected_servers')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='inspected_servers')
    hash_key = models.UUIDField(_('hash key'))
    is_active = models.BooleanField(_('active?'))

    def __str__(self):
        return f'{self.inspector} - {self.server}'
