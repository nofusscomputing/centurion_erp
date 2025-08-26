from django.apps import apps
from django.contrib.auth.models import ContentType
from django.db.models.signals import (
    post_save
)
from django.dispatch import receiver



@receiver(post_save, dispatch_uid="audit_history_save")
def audit_history(sender, instance, **kwargs):

    if getattr(instance, '_audit_enabled', False):

        if instance.context.get('user', None) is None:
            return

        audit_model = apps.get_model( 
            instance._meta.app_label,
            instance._meta.object_name + 'AuditHistory'
        )

        audit_action = audit_model.Actions.UPDATE

        if instance.get_before() == {}:

            audit_action = audit_model.Actions.ADD

        elif instance.get_after() == {}:

            audit_action = audit_model.Actions.DELETE


        try:
            audit_model.objects.create(
                organization = instance.get_tenant(),
                content_type = ContentType.objects.get(
                    app_label = instance._meta.app_label,
                    model = instance._meta.model_name,
                ),
                action = audit_action,
                user = instance.context['user'],
                model = instance,
            )

        except Exception as e:
            instance.context['logging'].error("unable to save audit log for model", exc_info=True)
