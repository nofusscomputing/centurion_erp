from django.apps import apps
from django.contrib.auth.models import ContentType
from django.core.exceptions import ValidationError
from django.db.models.signals import (
    # post_delete,
    post_save
)
from django.dispatch import receiver



# @receiver(post_delete, dispatch_uid="audit_history_delete")
@receiver(post_save, dispatch_uid="audit_history_save")
def audit_history(sender, instance, **kwargs):

    if getattr(instance, '_audit_enabled', False):

        audit_model = apps.get_model( instance._meta.app_label, instance._meta.object_name + 'AuditHistory')

        audit_action = audit_model.Actions.UPDATE

        if instance.get_before() == {}:

            audit_action = audit_model.Actions.ADD

        elif instance.get_after() == {}:

            audit_action = audit_model.Actions.DELETE

        if instance.context.get('user', None) is None:

            raise ValidationError(
                code = 'model_missing_user_context',
                message = f'Model {instance._meta.model_name}, is missing user context. ' \
                    'No audit history can be saved'
            )


        history = audit_model.objects.create(
            organization = instance.organization,
            content_type = ContentType.objects.get(
                app_label = instance._meta.app_label,
                model = instance._meta.model_name,
            ),
            action = audit_action,
            user = instance.context['user'],
            model = instance,
        )
