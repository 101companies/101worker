import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'services_temp.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

