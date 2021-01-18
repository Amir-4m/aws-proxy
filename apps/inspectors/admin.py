from django.contrib import admin

from .models import Inspector, InspectorLog


@admin.register(Inspector)
class InspectorModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enable', 'created_time', 'updated_time', 'token')
    list_filter = ('is_enable',)

    change_form_template = "testers/admin/change-form.html"

    def token(self, obj):
        return obj.get_jwt_token()


@admin.register(InspectorLog)
class InspectedServerModelAdmin(admin.ModelAdmin):
    list_display = ('inspector', 'server', 'hash_key', 'is_active', 'created_time')
    search_fields = ('hash_key',)
    list_filter = ('server', 'is_active', 'inspector')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
