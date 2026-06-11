"""
WSGI config for itsm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from prometheus_client import multiprocess, REGISTRY
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centurion.settings')


try:

    import prometheus_client
    import uwsgi

    from django.conf import settings


    if getattr(settings, 'METRICS_ENABLED', False) and "PROMETHEUS_MULTIPROC_DIR" in os.environ:

        coordination_dir = Path(os.environ['PROMETHEUS_MULTIPROC_DIR'])
        coordination_dir.mkdir(parents=True, exist_ok=True)

        # must clear existing db files
        for filepath in coordination_dir.glob(f"*.db"):
            try:
                filepath.unlink()
            except FileNotFoundError:
                pass


        registry = REGISTRY

        # Init multiprocess collector using global registry
        multiprocess.MultiProcessCollector( registry = registry )

        # metric filename suffix
        prometheus_client.values.ValueClass = prometheus_client.values.MultiProcessValue(
            process_identifier=uwsgi.worker_id)

except ImportError:
    pass  # not running in uwsgi


#
# Set working directory
# This is required due to src dir mappped to module name `centurion_erp`
# Without this `chdir` code needs to be updated to import from module
# namespace. in addition src dir would also need to be renamed.
os.chdir(path=f'{os.path.dirname(__file__)}/../')

application = get_wsgi_application()
