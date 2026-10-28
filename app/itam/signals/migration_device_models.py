from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import ContentType, Permission
from django.db.models.signals import (
    post_migrate,
)
from django.dispatch import receiver

from centurion.logging import CenturionLogger



@receiver(signal = post_migrate, dispatch_uid = "migrate_device_model_asset_model")
def migrate_device_model_asset_model(sender, **kwargs):


    if sender.label != 'itam':
        return

    log: CenturionLogger = settings.CENTURION_LOG.getChild(
        suffix = 'migration' ).getChild( suffix = 'itam' )

    try:

        log.info( msg = 'Begin data migration form itam.DeviceModel to itam.ITAssetModel.' )

        device_model = apps.get_model(
            app_label = 'itam',
            model_name = 'devicemodel'
        )

        device_model.context['logger'] = log

        for old_device_model in device_model.objects.filter(
            migrated_id = None
        ):

            old_device_model.migrate()


        log.info( msg = 'End of data migration form itam.DeviceModel to itam.ITAssetModel.' )

        del device_model.context['logger']

        log.info( msg = 'Begin data migration form itam.Device to itam.ITAsset.' )

        device = apps.get_model(
            app_label = 'itam',
            model_name = 'device'
        )

        device.context['logger'] = log

        for old_device in device.objects.filter(
            migrated_id = None
        ):

            old_device.migrate()


        log.info( msg = 'End of data migration form itam.Device to itam.ITAsset.' )

        del device.context['logger']

    except Exception as exc:
        log.exception(msg = exc)

