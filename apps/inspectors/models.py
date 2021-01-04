from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.servers.models import Server


class Inspector(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('name'), max_length=120)
    is_enable = models.BooleanField(_('is enable'), default=True)

    def __str__(self):
        return self.name


class InspectedServer(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='inspected_servers')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='inspected_servers')
    hash_key = models.UUIDField(_('hash key'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.inspector} - {self.server}'
