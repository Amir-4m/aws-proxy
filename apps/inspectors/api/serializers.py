import re

from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ..models import InspectorLog, ISPDetector, RegisterCode, Inspector


class RegisterSerializer(serializers.Serializer):
    code = serializers.SlugRelatedField(queryset=RegisterCode.objects.filter(inspector__isnull=True), slug_field='code')
    name = serializers.CharField()

    def validate_name(self, value):
        if Inspector.objects.filter(name=value).exists():
            raise ValidationError(_('inspector with this name exists!'))
        return value

    def create(self, validated_data):
        with transaction.atomic():
            code = RegisterCode.objects.select_for_update(of=("self",)).get(code=validated_data['code'].code)
            inspector = Inspector.objects.create(name=validated_data['name'])
            code.inspector = inspector
            code.save()
        return inspector

    def update(self, instance, validated_data):
        return instance


class InspectorLogSerializer(serializers.ModelSerializer):
    received_isp = serializers.CharField()

    class Meta:
        model = InspectorLog
        exclude = ('inspector',)

    def validate(self, attrs):
        isp_name = attrs['received_isp'].lower()
        valid_isp = None
        for _i in ISPDetector.objects.filter(is_enable=True):
            if re.search(_i.regex_pattern, isp_name):
                valid_isp = _i
                break
        attrs.update({'detected_isp': valid_isp})
        return attrs
