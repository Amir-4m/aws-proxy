from celery.schedules import crontab
from celery.task import periodic_task
from django.utils import timezone
from django.conf import settings
from django.db import transaction

from apps.servers.models import Server
from .models import InspectorLog, Inspector
from ..servers.tasks import restart_server


@periodic_task(run_every=(crontab(minute='*')))
def check_server_connection_analyses():
    inspectors_count = Inspector.objects.filter(is_enable=True).count()
    with transaction.atomic():
        server_list = Server.objects.select_for_update().filter(connection_status=Server.CONNECTION_STATUS_CHECK, is_enable=True)
        for server in server_list:
            inspected_servers = InspectorLog.objects.filter(hash_key=server.hash_key)
            if inspectors_count == inspected_servers.count():
                if all(inspected_servers.values_list('is_active', flat=True)):
                    server.connection_status = Server.CONNECTION_STATUS_ACTIVE
                    server.save()
                else:
                    restart_server.delay(server.id)

            else:
                if (timezone.now() - server.updated_time).total_seconds() > settings.SERVER_EXPIRY_TIME * 60:
                    restart_server.delay(server.id)
