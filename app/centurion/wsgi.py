"""
WSGI config for itsm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'centurion.settings')


try:

    import prometheus_client
    import uwsgi
    from pathlib import Path

    from django.conf import settings

    print("************************************* wsgi ********************************************")

    if getattr(settings, 'METRICS_ENABLED', False):

        from prometheus_client import multiprocess, REGISTRY, start_http_server


        def _setup_multiproc_folder():

            coordination_dir = Path(os.environ["PROMETHEUS_MULTIPROC_DIR"])
            coordination_dir.mkdir(parents=True, exist_ok=True)

            for filepath in coordination_dir.glob("*.db"):

                filepath.unlink()

            return coordination_dir


        proc_path = None

        try:
            proc_path = os.environ["PROMETHEUS_MULTIPROC_DIR"]
        except:
            pass


        if not proc_path:

            os.environ["PROMETHEUS_MULTIPROC_DIR"] = settings.METRICS_MULTIPROC_DIR

            proc_path = os.environ["PROMETHEUS_MULTIPROC_DIR"]


        prometheus_dir = Path(os.environ["PROMETHEUS_MULTIPROC_DIR"])
        prometheus_dir.mkdir(parents=True, exist_ok=True)


        # metric filename suffix
        prometheus_client.values.ValueClass = prometheus_client.values.MultiProcessValue(
            process_identifier=uwsgi.worker_id)


        multiproc_folder_path = _setup_multiproc_folder()

        registry = REGISTRY

        multiprocess.MultiProcessCollector(registry, path=multiproc_folder_path)

        start_http_server( settings.METRICS_EXPORT_PORT, registry=registry)


    print("************************************* wsgi ********************************************")

except ImportError:
    pass  # not running in uwsgi


#
# Set working directory
# This is required due to src dir mappped to module name `centurion_erp`
# Without this `chdir` code needs to be updated to import from module
# namespace. in addition src dir would also need to be renamed.
os.chdir(path=f'{os.path.dirname(__file__)}/../')

application = get_wsgi_application()
