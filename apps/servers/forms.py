from django import forms
from django_admin_json_editor import JSONEditorWidget

from apps.servers.models import Server


class ServerModelAdminForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'
        widgets = {
            'properties': JSONEditorWidget({}, collapsed=False),
        }
