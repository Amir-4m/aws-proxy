from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.dns.models import DomainNameRecord
from apps.servers.models import Server


class ProxyManager(models.Manager):
    def has_domain(self):
        return self.exclude(host__regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        # return self.filter(host__iregex=r'^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9]\.[a-zA-Z]{2,}$')

    def has_ip(self):
        return self.filter(host__regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")


class Proxy(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='proxies')
    host = models.CharField(_('host'), max_length=250)
    port = models.IntegerField(_('port'))
    secret_key = models.TextField(_('secret'))
    is_enable = models.BooleanField(_('enabled?'))
    objects = ProxyManager()

    class Meta:
        verbose_name = _('Proxy')
        verbose_name_plural = _('Proxies')
        unique_together = ('host', 'port')

    def __str__(self):
        return f'{self.host}:{self.port}'
