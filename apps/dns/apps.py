from django.apps import AppConfig


class DnsConfig(AppConfig):
    name = 'apps.dns'

    def ready(self):
        import apps.dns.signals  # NOQA
