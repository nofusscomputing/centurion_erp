from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import ContentType, Permission
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.db.models.signals import (
    post_migrate,
)
from django.dispatch import receiver

from core.models.centurion import CenturionModel
from centurion.logging import CenturionLogger



@receiver(signal = post_migrate, dispatch_uid = "migrate_device_model_asset_model")
def migrate_device_model_asset_model(sender, **kwargs):


    if sender.label != 'itam':
        return

    log: CenturionLogger = settings.CENTURION_LOG.getChild(
        suffix = 'migration' ).getChild( suffix = 'itam' )

    try:

        log.info( msg = 'Begin data migration form itam.DeviceModel to itam.ITAssetModel.' )

        system_user = apps.get_model(settings.AUTH_USER_MODEL).objects.filter(
            username = 'system'
        ).first()

        device_model = apps.get_model(
            app_label = 'itam',
            model_name = 'devicemodel'
        )

        device = apps.get_model(
            app_label = 'itam',
            model_name = 'device'
        )


        ticket_comment_model = apps.get_model(
            app_label = 'core',
            model_name = 'ticketcommentbase'
        )


        kb_article_model = apps.get_model(
            app_label = 'assistance',
            model_name = 'knowledgebase'
        )

        device_model.context['logger'] = log

        for old_device_model in device_model.objects.filter(
            migrated_id = None
        ):

            old_device_model.migrate()


            #
            # SoF Model Tag migration
            #


            log.info(
                msg = f'Searching for ticket comments that contain $device_model-{old_device_model.id}'
            )

            ticket_comments = ticket_comment_model.objects.filter(
                body__contains = f'$device_model-{old_device_model.id}'
            )

            if len(ticket_comments) == 0:

                log.info(
                    msg = f'No ticket comment found for $device_model-{old_device_model.id}'
                )


            for comment in ticket_comments:

                log.info(
                    msg = f'Updating ticket comment {comment.id}, replacing model tag ' \
                        f'$device_model-{old_device_model.id} -> $itasset_model-{old_device_model.migrated_id.id}'
                )

                comment.body = str(comment.body).replace(
                    f'$device_model-{old_device_model.id}',
                    f'$itasset_model-{old_device_model.migrated_id.id}'
                )

                comment.save()




            log.info(
                msg = f'Searing for KB articles that contain $device_model-{old_device_model.id}'
            )

            kb_articles = kb_article_model.objects.filter(
                Q( summary__contains = f'$device_model-{old_device_model.id}' ) |
                Q( content__contains = f'$device_model-{old_device_model.id}' )
            )

            if len(kb_articles) == 0:

                log.info(
                    msg = f'No KB articles found for $device_model-{old_device_model.id}'
                )


            for obj in kb_articles:

                obj.__class__.context[obj._meta.model_name] = system_user

                log.info(
                    msg = f'Updating KB article {obj.id} summary field, replacing model tag ' \
                        f'$device_model-{old_device_model.id} -> $itasset_model-{old_device_model.migrated_id.id}'
                )

                obj.summary = str(obj.summary).replace(
                    f'$device_model-{old_device_model.id}',
                    f'$itasset_model-{old_device_model.migrated_id.id}'
                )

                log.info(
                    msg = f'Updating KB article {obj.id} content field, replacing model tag ' \
                        f'$device_model-{old_device_model.id} -> $itasset_model-{old_device_model.migrated_id.id}'
                )

                obj.content = str(obj.content).replace(
                    f'$device_model-{old_device_model.id}',
                    f'$itasset_model-{old_device_model.migrated_id.id}'
                )

                obj.save()


                del obj.__class__.context[obj._meta.model_name]



            log.info(
                msg = f'Searing all models field model_notes that for $device_model-{old_device_model.id}'
            )
            
            for model in apps.get_models():

                if(
                    not issubclass(model, CenturionModel)
                ):
                    continue

                try:

                    model._meta.get_field('model_notes')

                except FieldDoesNotExist:
                    continue

                log.info(
                    msg = f'Searing model {model._meta.model_name} field model_notes that ' \
                        f'for $device_model-{old_device_model.id}'
                )


                model_rows = model.objects.filter(
                    model_notes__contains = f'$device_model-{old_device_model.id}'
                )

                if len(model_rows) == 0:

                    log.info(
                        msg = f'No rows found for model {model._meta.model_name} containing ' \
                            f'$device_model-{old_device_model.id}'
                    )

                for obj in model_rows:

                    obj.__class__.context[obj._meta.model_name] = system_user

                    log.info(
                        msg = f'Updating {model._meta.model_name} {obj.id} model_notes field, '\
                            f'replacing model tag $device_model-{old_device_model.id} -> ' \
                            f'$itasset_model-{old_device_model.migrated_id.id}'
                    )

                    obj.model_notes = str(obj.model_notes).replace(
                        f'$device_model-{old_device_model.id}',
                        f'$itasset_model-{old_device_model.migrated_id.id}'
                    )

                    obj.save()

                    del obj.__class__.context[obj._meta.model_name]


            #
            # EoF Model Tag migration
            #


        log.info( msg = 'End of data migration form itam.DeviceModel to itam.ITAssetModel.' )


        del device_model.context['logger']



        log.info( msg = 'Begin data migration form itam.Device to itam.ITAsset.' )


        device.context['logger'] = log

        for old_device in device.objects.filter(
            migrated_id = None
        ):

            old_device.migrate()


            #
            # SoF Model Tag migration
            #


            log.info(
                msg = f'Searching for ticket comments that contain $device-{old_device.id}'
            )

            ticket_comments = ticket_comment_model.objects.filter(
                body__contains = f'$device-{old_device.id}'
            )

            if len(ticket_comments) == 0:

                log.info(
                    msg = f'No ticket comment found for $device-{old_device.id}'
                )


            for comment in ticket_comments:

                log.info(
                    msg = f'Updating ticket comment {comment.id}, replacing model tag ' \
                        f'$device-{old_device.id} -> $itasset-{old_device.migrated_id.id}'
                )

                comment.body = str(comment.body).replace(
                    f'$device-{old_device.id}',
                    f'$itasset-{old_device.migrated_id.id}'
                )

                comment.save()




            log.info(
                msg = f'Searing for KB articles that contain $device-{old_device.id}'
            )

            kb_articles = kb_article_model.objects.filter(
                Q( summary__contains = f'$device-{old_device.id}' ) |
                Q( content__contains = f'$device-{old_device.id}' )
            )

            if len(kb_articles) == 0:

                log.info(
                    msg = f'No KB articles found for $device-{old_device.id}'
                )


            for obj in kb_articles:

                obj.__class__.context[obj._meta.model_name] = system_user

                log.info(
                    msg = f'Updating KB article {obj.id} summary field, replacing model tag ' \
                        f'$device-{old_device.id} -> $itasset-{old_device.migrated_id.id}'
                )

                obj.summary = str(obj.summary).replace(
                    f'$device-{old_device.id}',
                    f'$itasset-{old_device.migrated_id.id}'
                )

                log.info(
                    msg = f'Updating KB article {obj.id} content field, replacing model tag ' \
                        f'$device-{old_device.id} -> $itasset-{old_device.migrated_id.id}'
                )

                obj.content = str(obj.content).replace(
                    f'$device-{old_device.id}',
                    f'$itasset-{old_device.migrated_id.id}'
                )

                obj.save()


                del obj.__class__.context[obj._meta.model_name]



            log.info(
                msg = f'Searing all models field model_notes that for $device-{old_device.id}'
            )
            
            for model in apps.get_models():

                if(
                    not issubclass(model, CenturionModel)
                ):
                    continue

                try:

                    model._meta.get_field('model_notes')

                except FieldDoesNotExist:
                    continue

                log.info(
                    msg = f'Searing model {model._meta.model_name} field model_notes that ' \
                        f'for $device-{old_device.id}'
                )


                model_rows = model.objects.filter(
                    model_notes__contains = f'$device-{old_device.id}'
                )

                if len(model_rows) == 0:

                    log.info(
                        msg = f'No rows found for model {model._meta.model_name} containing ' \
                            f'$device-{old_device.id}'
                    )

                for obj in model_rows:

                    obj.__class__.context[obj._meta.model_name] = system_user

                    log.info(
                        msg = f'Updating {model._meta.model_name} {obj.id} model_notes field, '\
                            f'replacing model tag $device-{old_device.id} -> ' \
                            f'$itasset-{old_device.migrated_id.id}'
                    )

                    obj.model_notes = str(obj.model_notes).replace(
                        f'$device-{old_device.id}',
                        f'$itasset-{old_device.migrated_id.id}'
                    )

                    obj.save()

                    del obj.__class__.context[obj._meta.model_name]


            #
            # EoF Model Tag migration
            #



        log.info( msg = 'End of data migration form itam.Device to itam.ITAsset.' )

        del device.context['logger']

    except Exception as exc:
        log.exception(msg = exc)

