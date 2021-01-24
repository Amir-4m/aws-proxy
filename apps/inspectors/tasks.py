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
    with transaction.atomic():
        server_list = Server.objects.select_for_update().filter(connection_status=Server.CONNECTION_STATUS_CHECK,
                                                                is_enable=True)

        op_list = [(_op[0], Inspector.objects.filter(is_enable=True, operator=_op[0]).count()) for _op in
                   Inspector.OPERATOR_CHOICES]

        for server in server_list:
            _restart = []
            for op, inspector_counts in op_list:
                inspected_servers = InspectorLog.objects.filter(hash_key=server.hash_key, inspector__operator=op)
                if inspected_servers.filter(is_active=True).exist():
                    _restart.append(False)
                elif inspected_servers.filter(is_active=False).count() == inspector_counts:
                    _restart.append(True)
                else:
                    _restart.append(None)

            if all([r is False for r in _restart]):
                server.connection_status = Server.CONNECTION_STATUS_ACTIVE
                server.save()
            elif any(_restart):
                restart_server.delay(server.id)
            elif (timezone.now() - server.updated_time).total_seconds() > settings.SERVER_EXPIRY_TIME * 60:
                restart_server.delay(server.id)
