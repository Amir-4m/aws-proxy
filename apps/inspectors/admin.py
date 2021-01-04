from django.contrib import admin
from django.http import HttpResponseRedirect

from .models import Inspector, InspectedProxy
from .utils import random_secret_generator


@admin.register(Inspector)
class TesterModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enable', 'created_time', 'updated_time')
    list_filter = ('is_enable',)
    readonly_fields = ('secret_key',)

    change_form_template = "testers/admin/change-form.html"

    def response_change(self, request, obj):
        if "change-secret" in request.POST:
            key = random_secret_generator()
            while Inspector.objects.filter(secret_key=key).exists():
                key = random_secret_generator()

            obj.secret_key = key
            obj.save()
            return HttpResponseRedirect(".")  # stay on the same detail page

        return super().response_change(request, obj)


@admin.register(InspectedProxy)
class InspectedProxyModelAdmin(admin.ModelAdmin):
    list_display = ('inspector', 'proxy', 'hash_key', 'is_active', 'created_time')
    list_filter = ('is_active',)
