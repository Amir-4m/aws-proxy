import logging
import requests

from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from .models import DomainNameRecord, DNSUpdateLog

logger = logging.getLogger(__name__)

headers = {
    'X-Auth-Email': settings.CLOUDFLARE_EMAIL,
    'X-Auth-Key': settings.CLOUDFLARE_API_KEY,
    'Content-Type': 'application/json',
}

data = {
    "type": "A",
    "name": None,
    "content": None,
    "ttl": 120,
    "proxied": False,
}

cloudflare_base_url = "https://api.cloudflare.com/client/v4/zones"


@shared_task
def cloudflare_create(record_id, domain, ip, zone_id):
    data['name'] = domain
    data['content'] = ip

    url = f"{cloudflare_base_url}/{zone_id}/dns_records"
    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        response_data = r.json().get('result', {})
        DomainNameRecord.objects.filter(id=record_id).update(dns_record=response_data.get('id', ''))

    except Exception as e:
        logger.error(
            f'[message: create domain error {e}]-[domain: {domain}]-[ip: {ip}]'
        )
        return
    else:
        logger.error(
            f'[message: create domain error]-[domain: {domain}]-[ip: {ip}]'
        )

    DNSUpdateLog.objects.create(
        ip=ip,
        domain_record_id=record_id,
        api_response=response_data
    )


@shared_task
def cloudflare_edit(record_id, domain, ip, dns_record, zone_id):
    data['name'] = domain
    data['content'] = ip

    url = f"{cloudflare_base_url}/{zone_id}/dns_records/{dns_record}"
    try:
        r = requests.put(url, headers=headers, json=data)
        r.raise_for_status()
        response_data = r.json().get('result', {})
    except Exception as e:
        logger.error(
            f'[message: edit domain error {e}]-[domain: {domain}]-[ip: {ip}]'
        )
        return
    else:
        logger.error(
            f'[message: edit domain error]-[domain: {domain}]-[ip: {ip}]'
        )

    DNSUpdateLog.objects.create(
        ip=ip,
        domain_record_id=record_id,
        api_response=response_data,
    )


@shared_task
def cloudflare_delete(objc_id, domain, ip, dns_record, zone_id):
    data['name'] = domain
    data['content'] = ip

    url = f"{cloudflare_base_url}/{zone_id}/dns_records/{dns_record}"
    try:
        r = requests.delete(url, headers=headers)
        r.raise_for_status()
        response_data = r.json().get('result', {})
    except Exception as e:
        logger.error(
            f'[message: delete domain error {e}]-[domain: {domain}]-[ip: {ip}]'
        )
        return
    else:
        logger.error(
            f'[message: delete domain error]-[domain: {domain}]-[ip: {ip}]'
        )
    DNSUpdateLog.objects.create(
        ip=ip,
        domain_record_id=objc_id,
        api_response=response_data
    )


@periodic_task(run_every=(crontab(**settings.CLEAR_DNS_LOGS_CRONTAB)))
def clear_dns_logs():
    try:
        DNSUpdateLog.truncate()
    except Exception as e:
        logger.error(f'truncating dns logs failed due to: {e}')
