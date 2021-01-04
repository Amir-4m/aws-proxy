from django.contrib import admin
from .models import Proxy


@admin.register(Proxy)
class ProxyModelAdmin(admin.ModelAdmin):
    list_display = ('hash_key', 'name_server', 'port', 'status', 'is_enable', 'created_time', 'updated_time')
    list_filter = ('is_enable',)
