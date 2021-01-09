import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.dns.models import DomainNameRecord
from apps.servers.models import Server


class Proxy(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    hash_key = models.UUIDField(default=uuid.uuid4)
    name_server = models.ForeignKey(DomainNameRecord, on_delete=models.CASCADE, related_name='proxies')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='proxies', null=True)
    host = models.CharField(_('host'), max_length=32, null=True, blank=True)
    port = models.IntegerField(_('port'))
    secret_key = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    def __str__(self):
        return self.id
