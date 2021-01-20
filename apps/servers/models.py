import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField


class ServerManager(models.Manager):
    def live(self):
        return self.filter(
            aws_status=Server.AWS_STATUS_RUNNING,
            connection_status=Server.CONNECTION_STATUS_ACTIVE,
            is_enable=True
        )


class Server(models.Model):
    AWS_STATUS_STOPPING = 'stopping'
    AWS_STATUS_STOPPED = 'stopped'
    AWS_STATUS_RUNNING = 'running'
    AWS_STATUS_PENDING = 'pending'

    CONNECTION_STATUS_ACTIVE = 'active'
    CONNECTION_STATUS_CHECK = 'check'

    AWS_STATUS_CHOICES = [
        (AWS_STATUS_STOPPING, _('Stopping')),
        (AWS_STATUS_STOPPED, _('Stopped')),
        (AWS_STATUS_RUNNING, _('Running')),
        (AWS_STATUS_PENDING, _('Pending')),
    ]

    CONNECTION_STATUS_CHOICES = [
        (CONNECTION_STATUS_ACTIVE, _('Active')),
        (CONNECTION_STATUS_CHECK, _('Check')),

    ]

    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_time = models.DateTimeField(_("updated time"), auto_now=True)
    name = models.CharField(_('name'), max_length=120)
    aws_status = models.CharField(max_length=10, choices=AWS_STATUS_CHOICES, editable=False)
    connection_status = models.CharField(
        max_length=11,
        choices=CONNECTION_STATUS_CHOICES,
        default=CONNECTION_STATUS_ACTIVE
    )
    is_enable = models.BooleanField(_('enabled?'))
    hash_key = models.UUIDField(default=uuid.uuid4, editable=False)
    properties = JSONField(_('properties'), default=dict)
    objects = ServerManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_connection_status = self.connection_status

    def active_ip(self):
        return getattr(
            self.server_logs.all().order_by('-pk').first(),
            'ip',
            '-'
        )

    def __str__(self):
        return self.name

    def change_hash_key(self):
        self.hash_key = uuid.uuid4()

    def save(self, *args, **kwargs):
        if self.connection_status != self._b_connection_status and self.connection_status == self.CONNECTION_STATUS_CHECK:
            self.change_hash_key()
        super(Server, self).save(*args, **kwargs)


class ServerLog(models.Model):
    created_time = models.DateTimeField(_("created time"), auto_now_add=True)
    server = models.ForeignKey(Server, on_delete=models.PROTECT, related_name='server_logs')
    ip = models.GenericIPAddressField(protocol='IPv4')

    class Meta:
        db_table = 'servers_publicip'
        verbose_name = _('Server Log')
        verbose_name_plural = _('Server Logs')

    def __str__(self):
        return f"{self.ip} > server: {self.server_id}"
