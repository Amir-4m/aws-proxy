from rest_framework import serializers

from ..models import Server


class ServerSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(source='active_ip')

    class Meta:
        model = Server
        fields = ('id', 'hash_key', 'ip', 'ports', 'connection_status')
