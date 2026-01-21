"""
WSGI config for itsm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centurion.settings')
#
# Set working directory
# This is required due to src dir mappped to module name `centurion_erp`
# Without this `chdir` code needs to be updated to import from module
# namespace. in addition src dir would also need to be renamed.
os.chdir(path=f'{os.path.dirname(__file__)}/../')

application = get_wsgi_application()
