from django.contrib import admin
from .models import Proxy


@admin.register(Proxy)
class ProxyModelAdmin(admin.ModelAdmin):
    list_display = ('server', 'host', 'port', 'is_enable', 'created_time', 'updated_time')
    list_filter = ('is_enable', 'server')
    search_fields = ('secret_key', 'host')
