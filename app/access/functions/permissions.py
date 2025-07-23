from django.apps import apps
from django.contrib.auth.models import (
    ContentType,
    Permission
)
from django.conf import settings


def permission_queryset():
    """Filter Permissions to those used within the application

    Returns:
        list: Filtered queryset that only contains the used permissions
    """

    centurion_apps = [
        'access',
        'accounting',
        'assistance',
        'config_management',
        'core',
        'devops',
        'django_celery_results',
        'human_resources',
        'itam',
        'itim',
        'project_management',
        'settings',
    ]

    exclude_models = [
        'appsettings',
        'chordcounter',
        'comment',
        'groupresult',
        'history',
        'modelnotes',
        'usersettings',
    ]

    exclude_permissions = [
        'add_checkin',
        'add_history',
        'add_organization',
        'add_taskresult',
        'add_ticketcommentaction',
        'change_checkin',
        'change_history',
        'change_organization',
        'change_taskresult',
        'change_ticketcommentaction',
        'delete_checkin',
        'delete_history',
        'delete_organization',
        'delete_taskresult',
        'delete_ticketcommentaction',
        'view_checkin',
        'view_history',
    ]


    if not settings.RUNNING_TESTS:

        models = apps.get_models()

        for model in models:

            if(
                not str(model._meta.object_name).endswith('AuditHistory')
                and not str(model._meta.model_name).lower().endswith('history')
            ):
                # check `endswith('history')` can be removed when the old history models are removed
                continue

            content_type = ContentType.objects.get(
                app_label = model._meta.app_label,
                model = model._meta.model_name
            )

            permissions = Permission.objects.filter(
                content_type = content_type,
            )

            for permission in permissions:

                if(
                    not permission.codename == 'view_' + str(model._meta.model_name)
                    and str(model._meta.object_name).endswith('AuditHistory')
                ):
                    exclude_permissions += [ permission.codename ]

                elif(
                    not str(model._meta.object_name).endswith('AuditHistory')
                    and str(model._meta.model_name).lower().endswith('history')
                ):
                    # This `elif` can be removed when the old history models are removed

                    exclude_permissions += [ permission.codename ]


    return Permission.objects.select_related('content_type').filter(
            content_type__app_label__in = centurion_apps,
        ).exclude(
            content_type__model__in = exclude_models
        ).exclude(
            codename__in = exclude_permissions
        )