from django.contrib import admin

from .models import DomainZone, DomainNameRecord, DNSUpdateLog


class DomainNameRecordInline(admin.TabularInline):
    model = DomainNameRecord
    extra = 1


@admin.register(DomainZone)
class DomainZoneAdmin(admin.ModelAdmin):
    list_display = ['domain_name', 'zone_id']
    inlines = (DomainNameRecordInline,)


@admin.register(DNSUpdateLog)
class DNSUpdateLogAdmin(admin.ModelAdmin):
    list_display = ['ip', 'domain_record', 'created_time']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
