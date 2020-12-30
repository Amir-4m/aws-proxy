from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


class Server(models.Model):
    STATUS_STOPPING = 'stopping'
    STATUS_STOPPED = 'stopped'
    STATUS_RUNNING = 'running'
    STATUS_PENDING = 'pending'

    STATUS_CHOICES = [
        (STATUS_STOPPING, _('Stopping')),
        (STATUS_STOPPED, _('Stopped')),
        (STATUS_RUNNING, _('Running')),
        (STATUS_PENDING, _('Pending')),

    ]
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    name = models.CharField(_('name'), max_length=120)
    properties = JSONField(_('properties'), default=dict)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    is_enable = models.BooleanField(default=True, editable=False)

    def active_ip(self):
        return getattr(
            self.public_ips.all().order_by('-created_time').first(),
            'ip',
            '-'
        )

    def __str__(self):
        return f"server {self.name}"


class PublicIP(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    ip = models.GenericIPAddressField(protocol='IPv4')
    server = models.ForeignKey(Server, on_delete=models.PROTECT, related_name='public_ips')

    def __str__(self):
        return f"{self.server} with public ip {self.ip}"
