from django.contrib import admin

from .models import Inspector, InspectedServer


@admin.register(Inspector)
class InspectorModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enable', 'created_time', 'updated_time', 'token')
    list_filter = ('is_enable',)

    change_form_template = "testers/admin/change-form.html"

    def token(self, obj):
        return obj.get_jwt_token()
