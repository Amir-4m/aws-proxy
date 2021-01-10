from django.utils import timezone
from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from apps.proxies.models import Proxy

from .forms import ServerModelAdminForm
from .models import Server, PublicIP
from .utils import get_instance_state
from .tasks import restart_server


class ProxyInlineAdmin(admin.TabularInline):
    model = Proxy
    extra = 1


@admin.register(PublicIP)
class PublicIPAdmin(admin.ModelAdmin):
    list_display = ('ip', 'server', 'created_time')
    search_fields = ('ip', 'server__name')
    ordering = ('-created_time',)
    date_hierarchy = 'created_time'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'active_ip',
        'is_enable', 'created_time',
        'updated_time', 'aws_status',
        'connection_status', 'server_actions'
    )
    list_filter = ('is_enable',)
    readonly_fields = ('hash_key',)
    search_fields = ('name', 'active_ip')
    form = ServerModelAdminForm
    inlines = (ProxyInlineAdmin,)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:server_id>/restart/', self.admin_site.admin_view(self.restart), name="server-restart"),

        ]
        return custom_urls + urls

    def server_actions(self, obj):
        return format_html(
            '<a class="button" href="{}">Restart</a>',
            reverse('admin:server-restart', args=[obj.pk])
        )

    server_actions.short_description = _('actions')
    server_actions.allow_tags = True

    def restart(self, request, server_id):
        server = Server.objects.get(id=server_id)
        state = get_instance_state(server)
        if state == Server.AWS_STATUS_RUNNING and (timezone.now() - server.updated_time).seconds > 300:
            server.status = Server.AWS_STATUS_PENDING
            server.save()
            restart_server.delay(server_id)
        else:
            messages.error(request, f'server can not be restarted! state: {state}')

        return redirect(f"admin:servers_server_changelist")
