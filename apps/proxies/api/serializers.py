from rest_framework import serializers

from ..models import Proxy


class IPProxySerializer(serializers.ModelSerializer):
    ip = serializers.ReadOnlyField(source='host')
    prt = serializers.ReadOnlyField(source='port')
    user = serializers.ReadOnlyField(default='')
    secret = serializers.ReadOnlyField(source='secret_key')
    sponser = serializers.ReadOnlyField(default=True)

    class Meta:
        model = Proxy
        fields = ('ip', 'prt', 'user', 'secret', 'sponser')

    def to_representation(self, instance):
        data = super(IPProxySerializer, self).to_representation(instance)
        data.update({'pass': ''})
        return data
