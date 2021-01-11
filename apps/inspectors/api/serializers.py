from rest_framework import serializers

from ..models import InspectedServer


class InspectedServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectedServer
        exclude = ('inspector',)

