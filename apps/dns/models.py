from django.db import models

from django.utils.translation import ugettext_lazy as _


class DomainZone(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    domain_name = models.CharField(max_length=50, unique=True)
    zone_id = models.CharField(max_length=32)
    is_enable = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Domain'

    def __str__(self):
        return self.domain_name


class DomainNameRecord(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    sub_domain_name = models.CharField(max_length=20)
    domain = models.ForeignKey(DomainZone, on_delete=models.PROTECT)
    ip = models.GenericIPAddressField(protocol='IPv4', db_index=True)
    dns_record = models.CharField(max_length=32, blank=True, editable=False)
    is_enable = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sub_domain_name', 'domain'], name='domain_address')
        ]

    def __str__(self):
        return self.domain_full_name

    def has_changed(self):
        if getattr(self.dns_logs.last(), 'ip', None) != self.ip:
            return True, self.ip

        return False, None

    @property
    def domain_full_name(self):
        return f"{self.sub_domain_name}.{self.domain}"


class DNSUpdateLog(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    ip = models.GenericIPAddressField(protocol='IPv4')
    domain_record = models.ForeignKey(DomainNameRecord, on_delete=models.PROTECT, related_name='dns_logs')
    api_response = models.TextField()

    class Meta:
        verbose_name = 'DNS Update Log'

    def __str__(self):
        return f"{self.domain_record} - {self.ip}"
