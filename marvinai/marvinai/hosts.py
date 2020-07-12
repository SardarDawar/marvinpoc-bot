from django.conf import settings
from django_hosts import patterns, host
host_patterns = patterns(
    '',
    host(r'^[a-zA-Z0-9]+$', 'main.urls', name='www'),
    host(r'admin', settings.ROOT_URLCONF, name='admin'),
)
