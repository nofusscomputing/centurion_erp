from django.contrib.auth.models import Permission

def permission_queryset():
    """Filter Permissions to those used within the application

    Returns:
        list: Filtered queryset that only contains the used permissions
    """

    apps = [
        'access',
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
        'change_checkin',
        'change_history',
        'change_organization',
        'change_taskresult',
        'delete_checkin',
        'delete_history',
        'delete_organization',
        'delete_taskresult',
        'view_checkin',
        'view_history',
    ]

    return Permission.objects.select_related('content_type').filter(
            content_type__app_label__in=apps,
        ).exclude(
            content_type__model__in=exclude_models
        ).exclude(
            codename__in = exclude_permissions
        )