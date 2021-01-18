from rest_framework import serializers

from ..models import InspectorLog


class InspectorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectorLog
        exclude = ('inspector',)

