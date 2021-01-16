import logging

from apps.api.aws import AmazonWebServiceAPI
from .models import Server, PublicIP

logger = logging.getLogger(__name__)


def get_instance_state(server):
    server_name = server.properties.get('name')
    server_access_key = server.properties.get('access_key')
    server_secret_key = server.properties.get('secret_key')
    server_region = server.properties.get('region')

    try:
        api = AmazonWebServiceAPI(server_name, server_access_key, server_secret_key, server_region)
        state = api.get_server_state()
    except Exception as e:
        logger.error(f'[message: getting server ip error {e}]-[server_id: {server.id}]')
        raise

    return state


def start_server(server):
    server_name = server.properties.get('name')
    server_access_key = server.properties.get('access_key')
    server_secret_key = server.properties.get('secret_key')
    server_region = server.properties.get('region')

    try:
        api = AmazonWebServiceAPI(server_name, server_access_key, server_secret_key, server_region)
        api.start_server()
    except Exception as e:
        logger.error(f'[message: starting server error {e}]-[server_id: {server.id}]')
        raise


def stop_server(server):
    server_name = server.properties.get('name')
    server_access_key = server.properties.get('access_key')
    server_secret_key = server.properties.get('secret_key')
    server_region = server.properties.get('region')
    try:
        api = AmazonWebServiceAPI(server_name, server_access_key, server_secret_key, server_region)
        api.stop_server()
    except Exception as e:
        logger.error(f'[message: stopping server error {e}]-[server_id: {server.id}]')
        raise


def get_server_ip(server):
    server_name = server.properties.get('name')
    server_access_key = server.properties.get('access_key')
    server_secret_key = server.properties.get('secret_key')
    server_region = server.properties.get('region')

    try:
        api = AmazonWebServiceAPI(server_name, server_access_key, server_secret_key, server_region)
        ip = api.get_server_ip()
        PublicIP.objects.create(ip=ip, server=server)
    except Exception as e:
        logger.error(f'[message: getting server ip error {e}]-[server_id: {server.id}]')
        raise
