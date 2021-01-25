import secrets

from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import RegisterCode


def create_codes(request):
    if request.user.is_authenticated:
        objs = []
        for _i in range(settings.MAX_RANDOM_CODE):
            generated_code = secrets.token_hex(5)
            if not RegisterCode.objects.filter(code=generated_code).exists():
                objs.append(RegisterCode(code=generated_code))
        RegisterCode.objects.bulk_create(objs)
        return HttpResponseRedirect(reverse('admin:inspectors_registercode_changelist'))
    return HttpResponseRedirect(reverse('admin:login'))

