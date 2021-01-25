from rest_framework import serializers

from ..models import Server


class ServerSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(source='active_ip')
    port = serializers.CharField(default='80')

    class Meta:
        model = Server
        fields = ('id', 'hash_key', 'ip', 'port', 'connection_status')
