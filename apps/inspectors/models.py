from datetime import timedelta

from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.inspectors.utils.jwt import jwt_payload_handler, jwt_encode_handler
from apps.servers.models import Server


class ISPDetector(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    title = models.CharField(_('ISP title'), max_length=40)
    # proxy_type = models.PositiveSmallIntegerField(_('proxy type'), choices=TelProxy.PROXY_TYPES)
    regex_pattern = models.TextField(_('regex pattern'))
    is_enable = models.BooleanField(_('enabled?'), default=True)

    class Meta:
        verbose_name = _('ISP detector')
        verbose_name_plural = _('ISP detectors')

    def __str__(self):
        return self.title


class Inspector(models.Model):
    # OPERATOR_TCI = 'tci'
    # OPERATOR_MCI = 'mci'
    # OPERATOR_MTN = 'mtn'
    #
    # OPERATOR_CHOICES = [
    #     (OPERATOR_TCI, _('TCI')),
    #     (OPERATOR_MCI, _('MCI')),
    #     (OPERATOR_MTN, _('MTN')),
    # ]
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('name'), max_length=120)
    # operator = models.CharField(_('operator'), max_length=3, choices=OPERATOR_CHOICES, default=OPERATOR_TCI)
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


class InspectorLog(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='inspector_logs')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='inspector_logs')
    ip = models.CharField(_('ip'), max_length=15, null=True, blank=True)
    received_isp = models.CharField(_('received isp'), max_length=120, blank=True, null=True)
    detected_isp = models.ForeignKey(ISPDetector, null=True, blank=True, on_delete=models.CASCADE, related_name='logs')
    hash_key = models.UUIDField(_('hash key'))
    is_active = models.BooleanField(_('active?'))

    class Meta:
        verbose_name = _('Inspector Log')
        verbose_name_plural = _('Inspector Logs')
        db_table = 'inspectors_inspectedserver'

    def __str__(self):
        return f'{self.inspector} - {self.server}'
