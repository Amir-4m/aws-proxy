import logging

from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.dns.models import DomainNameRecord
from .models import PublicIP

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=PublicIP)
def check_public_ip(sender, instance, **kwargs):
    expired_ip = instance.server.active_ip()
    if expired_ip != '-':
        for dns_record in DomainNameRecord.objects.filter(ip=expired_ip):
            dns_record.ip = instance.ip
            dns_record.save()
