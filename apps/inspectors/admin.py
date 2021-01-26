from django.contrib import admin

from .models import Inspector, InspectorLog, RegisterCode, ISPDetector


@admin.register(ISPDetector)
class ISPDetectorModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'regex_pattern', 'is_enable')
    search_fields = ('title',)
    list_filter = ('is_enable',)
    list_editable = ('is_enable',)


@admin.register(Inspector)
class InspectorModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enable', 'created_time', 'token')
    list_filter = ('is_enable',)

    # change_form_template = "testers/admin/change-form.html"

    def token(self, obj):
        return obj.get_jwt_token()


@admin.register(InspectorLog)
class InspectedServerModelAdmin(admin.ModelAdmin):
    list_display = ('inspector', 'server', 'received_isp', 'detected_isp', 'hash_key', 'is_active', 'created_time')
    search_fields = ('hash_key', 'received_isp')
    list_filter = ('server', 'is_active', 'inspector')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(RegisterCode)
class RegisterCodeModelAdmin(admin.ModelAdmin):
    list_display = ('code', 'inspector', 'created_time', 'updated_time')
    search_fields = ('code', 'inspector__name')
    list_filter = ('inspector',)
    readonly_fields = ('inspector',)

    change_list_template = "inspectors/admin/register_code_changelist.html"
