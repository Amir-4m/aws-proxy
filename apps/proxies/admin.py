from django.contrib import admin
from .models import Proxy


@admin.register(Proxy)
class ProxyModelAdmin(admin.ModelAdmin):
    list_display = ('host', 'port', 'is_enable', 'server', 'created_time', 'updated_time')
    list_filter = ('is_enable', 'server')
    search_fields = ('secret_key', 'host')
