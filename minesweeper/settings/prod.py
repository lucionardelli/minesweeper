"""Development settings and globals."""
from os.path import join, normpath
from os import environ

import django_heroku
import dj_database_url

from .db import DATABASES
from .common import *

########## DEBUG CONFIGURATION
DEBUG = False
########## END DEBUG CONFIGURATION


########## LOG CONFIGURATION
LOG_LEVEL=logging.INFO
########## END LOG CONFIGURATION

INSTALLED_APPS += (
    'rest_framework_swagger',
    'django_extensions',
)

ALLOWED_HOSTS = ('minesweeper', '*')

########## DATABASE CONFIGURATION
DATABASES['default'].update(dj_database_url.config(conn_max_age=500))
########## END DATABASE CONFIGURATION

########## HEROKU CONFIGURATION
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

django_heroku.settings(locals())
########## END HEROKU CONFIGURATION

# vim:expandtab:stmartindent:tabstop=4:softtabstop=4:shiftwidth=4:
