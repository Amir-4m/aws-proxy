import logging

from celery.schedules import crontab
from celery.task import periodic_task
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.conf import settings
from django.db import transaction
from django.db.models import Count

from apps.servers.models import Server
from .models import InspectorLog, Inspector, ISPDetector
from ..servers.tasks import restart_server

logger = logging.getLogger(__name__)


@periodic_task(run_every=(crontab(minute='*')))
def check_server_connection_analyses():
    with transaction.atomic():
        server_list = Server.objects.select_for_update().filter(connection_status=Server.CONNECTION_STATUS_CHECK, is_enable=True)

        """
        isp_list = list(ISPDetector.objects.filter(is_enable=True))
        for server in server_list:
            _restart = []
            for isp in isp_list:
                _inspectors = InspectorLog.objects.filter(detected_isp=isp)
                inspected_servers = _inspectors.filter(hash_key=server.hash_key)
                inspector_count = _inspectors.filter(
                    ip=server.active_ip()
                ).aggregate(
                    icount=Coalesce(Count('inspector_id', distinct=True), 0)
                )['icount']
                if inspected_servers.filter(is_active=True).exists():
                    _restart.append(False)
                elif inspector_count > 0 and inspected_servers.count() >= 0.3 * inspector_count:
                    _restart.append(True)
                else:
                    _restart.append(None)
        """

        for server in server_list:
            inspected_servers = InspectorLog.objects.filter(hash_key=server.hash_key)
            if inspected_servers.filter(is_active=False).exists():
                restart_server.delay(server.id)
            elif (timezone.now() - server.updated_time).total_seconds() > settings.SERVER_EXPIRY_TIME * 60:
                restart_server.delay(server.id)
            elif inspected_servers.count() >= 3:
                server.connection_status = Server.CONNECTION_STATUS_ACTIVE
                server.save()

@periodic_task(run_every=(crontab(**settings.CLEAR_INSPECTOR_LOGS_CRONTAB)))
def clear_inspector_logs():
    try:
        InspectorLog.truncate()
    except Exception as e:
        logger.error(f'truncating inspector logs failed due to: {e}')
