import re

from rest_framework import serializers

from ..models import InspectorLog, ISPDetector


class InspectorLogSerializer(serializers.ModelSerializer):
    received_isp = serializers.CharField()

    class Meta:
        model = InspectorLog
        exclude = ('inspector',)

    def validate_isp(self, value):
        isp_name = value.lower()
        valid_isp = None
        for _i in ISPDetector.objects.filter(is_enable=True):
            if re.search(_i.regex_pattern, isp_name):
                valid_isp = _i
                break
        return valid_isp

    def validate(self, attrs):
        isp_name = attrs['received_isp'].lower()
        valid_isp = None
        for _i in ISPDetector.objects.filter(is_enable=True):
            if re.search(_i.regex_pattern, isp_name):
                valid_isp = _i
                break
        attrs.update({'detected_isp': valid_isp})
        return attrs
