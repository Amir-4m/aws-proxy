from rest_framework import serializers

from ..models import Proxy


class IPProxySerializer(serializers.ModelSerializer):
    ip = serializers.ReadOnlyField(source='host')
    prt = serializers.ReadOnlyField(source='port')
    secret = serializers.ReadOnlyField(source='secret_key')

    class Meta:
        model = Proxy
        fields = ('ip', 'prt', 'user', 'secret', 'sponser')

    def to_representation(self, instance):
        data = super(IPProxySerializer, self).to_representation(instance)
        # as pass is a builtin in python, we create the key in to_representation
        data.update({
            'pass': '',
            'user': '',
            'sponser': True
        })
        return data
