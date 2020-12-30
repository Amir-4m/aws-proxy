import logging

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import DomainNameRecord
from .tasks import cloudflare_create, cloudflare_edit, cloudflare_delete

logger = logging.getLogger(__name__)


@receiver(post_save, sender=DomainNameRecord)
def check_dns_ip(sender, instance, created, **kwargs):
    if created:
        cloudflare_create.delay(
            instance.id,
            instance.domain_full_name,
            instance.ip,
            instance.domain.zone_id
        )
    else:
        if instance.is_enable and instance.domain.is_enable:
            cloudflare_edit.delay(
                instance.id,
                instance.domain_full_name,
                instance.ip,
                instance.dns_record,
                instance.domain.zone_id
            )


@receiver(pre_delete, sender=DomainNameRecord)
def delete_dns_record(sender, instance, **kwargs):
    cloudflare_delete.delay(
        instance.id,
        instance.domain_full_name,
        instance.ip,
        instance.dns_record,
        instance.domain.zone_id
    )
