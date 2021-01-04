from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.proxies.models import Proxy
from .utils import random_secret_generator


class Inspector(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    name = models.CharField(_('name'), max_length=120)
    secret_key = models.CharField(_('secret key'), max_length=64, default=random_secret_generator, unique=True)
    is_enable = models.BooleanField(_('is enable'), default=True)

    def __str__(self):
        return self.name


class InspectedProxy(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE, related_name='inspector_proxies')
    proxy = models.ForeignKey(Proxy, on_delete=models.CASCADE, related_name='inspector_proxies')
    hash_key = models.UUIDField(_('hash key'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.inspector} - {self.proxy}'
