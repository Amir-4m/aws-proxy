from rest_framework import serializers

from ..models import InspectedServer


class InspectorLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectedServer
        exclude = ('inspector',)

