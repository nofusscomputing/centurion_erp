from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import ContentType
from django.db.models.signals import (
    m2m_changed,
    post_save
)
from django.dispatch import receiver



@receiver(m2m_changed, dispatch_uid="audit_history_save")
@receiver(post_save, dispatch_uid="audit_history_save")
def audit_history(sender, instance, **kwargs):

    if getattr(instance, '_audit_enabled', False):

        if(
            type(instance).context.get(instance._meta.model_name, None) is None
            or (
                kwargs['signal'] is m2m_changed
                and kwargs['action'] not in [ 'post_add', 'post_remove' ]
            )
        ):
            return
        else:
            trace_var_for_testing = instance.context.get('user', None)

        log = settings.CENTURION_LOG.getChild('audit_history')

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

            if kwargs['signal'] is post_save:

                audit_entry = audit_model.objects.create(
                    organization = instance.get_tenant(),
                    content_type = ContentType.objects.get(
                        app_label = instance._meta.app_label,
                        model = instance._meta.model_name,
                    ),
                    action = audit_action,
                    user = type(instance).context.get(instance._meta.model_name, None),
                    model = instance,
                )

                instance.audit_entry = audit_entry

            elif kwargs['signal'] is m2m_changed:

                audit_entry = instance.audit_entry

                instance._after = instance.get_audit_values()

                audit_entry.save()


        except Exception as e:
            log.error(
                msg = str(
                    'unable to save audit log for model '
                    'vars: '
                    f"model={instance._meta.model_name} "
                    f"app_label={instance._meta.app_label} "
                    f"context={instance.context}"
                ),
                exc_info=True
            )
