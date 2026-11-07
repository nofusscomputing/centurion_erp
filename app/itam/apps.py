from django.apps import AppConfig


class ItamConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'itam'


    def ready(self):

        from itam.signals import migration_device_models
