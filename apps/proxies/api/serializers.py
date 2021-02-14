from rest_framework import serializers

from ..models import Proxy


class IPProxySerializerV1(serializers.ModelSerializer):
    ip = serializers.ReadOnlyField(source='host')
    prt = serializers.ReadOnlyField(source='port')
    secret = serializers.ReadOnlyField(source='secret_key')

    class Meta:
        model = Proxy
        fields = ('ip', 'prt', 'secret')

    def to_representation(self, instance):
        data = super(IPProxySerializerV1, self).to_representation(instance)
        # as pass is a builtin in python, we create the key in to_representation
        data.update({
            'pass': '',
            'user': '',
            'sponser': True
        })
        return data


class IPProxySerializerV2(serializers.ModelSerializer):
    proxy = serializers.SerializerMethodField()

    class Meta:
        model = Proxy
        fields = ('id', 'proxy')

    def get_proxy(self, obj):
        return f"https://t.me/proxy?server={obj.host}&port={obj.port}&secret={obj.secret_key}"
