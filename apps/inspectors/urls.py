from django.urls import path

from apps.inspectors.views import create_codes

urlpatterns = [
    path('generate-codes/', create_codes, name='generate_codes'),

]
