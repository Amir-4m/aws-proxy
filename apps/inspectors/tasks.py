from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from django.conf import settings

from apps.servers.models import Server
from .models import InspectedServer, Inspector
from ..servers.tasks import restart_server


@periodic_task(run_every=(crontab(minute='*/30')))
def check_server_connection_analyses():
    inspectors = Inspector.objects.filter(is_enable=True)
    for server in Server.objects.filter(connection_status=Server.CONNECTION_STATUS_CHECK, is_enable=True).order_by(
            'updated_time'):
        inspected_servers = InspectedServer.objects.filter(hash_key=server.hash_key)
        if inspectors.count() == inspected_servers.count():
            if all(inspected_servers.values_list('is_active', flat=True)):
                server.connection_status = Server.CONNECTION_STATUS_ACTIVE
            else:
                restart_server.delay()

        else:
            if timezone.now() - server.updated_time > settings.SERVER_EXPIRY_TIME:
                restart_server.delay()
