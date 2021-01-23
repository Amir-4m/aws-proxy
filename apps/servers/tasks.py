import logging
import math

from celery import shared_task
from celery.schedules import crontab
from celery.task import periodic_task
from django.conf import settings
from django.db import transaction

from .models import Server
from .utils import start_server, stop_server, get_server_ip, get_instance_state

logger = logging.getLogger(__name__)


@shared_task
def get_server_ip_async(server_id):
    server = Server.objects.get(id=server_id)
    state = get_instance_state(server)
    logger.info(f'[message: getting IP]-[server_id: {server_id}]-[state: {state}]')
    if state == 'running':
        get_server_ip(server)
        server.aws_status = Server.AWS_STATUS_RUNNING
        server.save()
    elif state == 'pending':
        logger.warning(f'[message: state was not running in starting server]-[server_id: {server_id}]')
        get_server_ip_async.apply_async(args=(server_id,), countdown=60)
    else:
        logger.error(f'[message: invalid state in getting server ip]-[server_id: {server_id}]-[state: {state}]')


@shared_task
def start_server_async(server_id):
    server = Server.objects.get(id=server_id)
    state = get_instance_state(server)
    logger.info(f'[message: starting server]-[server_id: {server.id}]-[state: {state}]')
    if state == Server.AWS_STATUS_STOPPED:
        start_server(server)
        server.aws_status = Server.AWS_STATUS_PENDING
        server.save()
        get_server_ip_async.apply_async(args=(server.id,), countdown=40)
    elif state == Server.AWS_STATUS_STOPPING:
        logger.warning(f'[message: state was in starting server]-[server_id: {server.id}]')
        start_server_async.apply_async(args=(server.id,), countdown=60)


@shared_task
def stop_server_async(server_id):
    server = Server.objects.get(id=server_id)
    logger.info(f'[message: stopping server]-[server_id: {server.id}]')
    stop_server(server)


@shared_task
def restart_server(server_id):
    with transaction.atomic():
        server = Server.objects.select_for_update().get(id=server_id)
        state = get_instance_state(server)
        logger.info(f'[message: restarting server]-[server_id: {server_id}]-[state: {state}]')
        if state == Server.AWS_STATUS_RUNNING:
            stop_server(server)
            server.aws_status = Server.AWS_STATUS_STOPPED
            server.save()
            start_server_async.delay(server.id)
        elif state == Server.AWS_STATUS_STOPPED:
            start_server_async.delay(server.id)
        elif state == Server.AWS_STATUS_STOPPING:
            start_server_async.apply_async(args=(server.id,), countdown=60)
        else:
            logger.warning(
                f'[message: restarting server canceled due to server state]-[server_id: {server_id}]-[state:{state}]'
            )


@periodic_task(run_every=(crontab(minute='*/10')))
def update_servers_to_check():
    servers = Server.objects.live().order_by('updated_time', '-pk')
    servers_range = servers.count() * (settings.UPDATED_SERVER_PERCENTAGE / 100)
    if servers_range < 1:
        servers_range = 1
    for server in servers[:math.ceil(servers_range)]:
        server.connection_status = Server.CONNECTION_STATUS_CHECK
        server.save()
