import re

from rest_framework import serializers

from ..models import InspectorLog, ISPDetector


class InspectorLogSerializer(serializers.ModelSerializer):
    isp = serializers.CharField()

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
