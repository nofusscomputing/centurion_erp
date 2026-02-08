from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import ContentType, Permission
from django.db.models.signals import (
    pre_delete,
    post_migrate,
)
from django.dispatch import receiver

from centurion.logging import CenturionLogger



@receiver(post_migrate, dispatch_uid="remove_non_existent_permissions")
def remove_non_existent_permissions(sender, **kwargs):


    if sender.label != 'core':
        return

    log: CenturionLogger = settings.CENTURION_LOG.getChild( suffix = 'migration' ).getChild( suffix = 'core' )

    Permission = apps.get_model(
        app_label = 'auth',
        model_name = 'permission'
    )

    try:

        permissions_to_remove = []

        for permission in Permission.objects.select_related(
            'content_type'
        ).all():


            name, model_name, *args = str(permission.codename).split('_')

            try:

                PermissionModel = apps.get_model(
                    app_label = permission.content_type.app_label,
                    model_name = model_name
                )

            except LookupError:

                permissions_to_remove += [ permission ]


            if name in [ 'add', 'change', 'delete', 'view' ]:
                continue


            clean = True

            for model_permission, description in PermissionModel._meta.permissions:

                if model_permission == permission.codename:
                    clean = False


            if clean:

                permissions_to_remove += [ permission ]


        for permission in permissions_to_remove:

            permission.delete()


            log.info(
                msg = f'Delete permission {permission.content_type.app_label}.{permission.codename}'
            )

    except Exception as exc:
        log.exception('exception')



@receiver(pre_delete, sender=Permission, dispatch_uid = 'remove_role_permission')
def remove_role_permission(sender, instance, **kwargs):

    Role = apps.get_model(
        app_label = 'access',
        model_name = 'role'
    )

    roles = Role.objects.filter(
        permissions = instance
    )

    log: CenturionLogger = settings.CENTURION_LOG.getChild( suffix = 'signal' ).getChild( suffix = 'core' )

    for role in roles:

        for permission in role.permissions.select_related(
            'content_type'
        ).all():

            if permission == instance:

                log.info(
                    msg = (
                        f'Remove permission {permission.content_type.app_label}.{permission.codename} '
                        f'from role {role}, as the permission is being deleted.'
                    )
                )

                role.permissions.remove(permission)
                break
