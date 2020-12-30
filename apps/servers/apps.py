from django.apps import AppConfig


class ServerConfig(AppConfig):
    name = 'apps.servers'

    def ready(self):
        import apps.servers.signals  # NOQA
