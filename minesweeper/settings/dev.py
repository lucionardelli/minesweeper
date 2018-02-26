"""Development settings and globals."""
from os.path import join, normpath
from os import environ

from .common import *

from .db import DATABASES

########## DEBUG CONFIGURATION
DEBUG = True
########## END DEBUG CONFIGURATION


########## LOG CONFIGURATION
LOG_LEVEL=logging.DEBUG
########## END LOG CONFIGURATION

########## CACHE CONFIGURATION
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
########## END CACHE CONFIGURATION

INSTALLED_APPS += (
    'rest_framework_swagger',
    'django_extensions',
)

ALLOWED_HOSTS = ('minesweeper-dev', '*')

# vim:expandtab:stmartindent:tabstop=4:softtabstop=4:shiftwidth=4:
