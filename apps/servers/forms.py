from django import forms
from jsoneditor.forms import JSONEditor

from apps.servers.models import Server


class ServerModelAdminForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = '__all__'
        widgets = {
            'properties': JSONEditor,
        }
