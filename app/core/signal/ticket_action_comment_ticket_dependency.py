from logging import Logger

from django.conf import settings
from django.db.models.signals import (
    post_delete,
    post_save,
)
from django.dispatch import receiver

from core.models.ticket_comment_action_ticket_dependency import (
    TicketCommentActionTicketDependency
)
from core.models.ticket_dependencies import TicketDependency



def get_action_user(instance):

    user = None

    if hasattr(type(instance), 'context'):

        for k, v in type(instance).context.items():

            if(
                k == 'logger'
                or getattr(v, 'username', '') == 'system'
                or v == None
            ):
                continue

            if v._meta.model_name == 'centurionuser':
                user = v
                break

    return user



@receiver(
    signal=post_delete,
    sender = TicketDependency,
    dispatch_uid="ticket_action_comment_ticket_dependency_save"
)
@receiver(
    signal=post_save,
    sender = TicketDependency,
    dispatch_uid="ticket_action_comment_ticket_dependency_save"
)
def ticket_action_comment_ticket_dependency(
    sender, instance, **kwargs
) -> None:


    try:

        log: Logger = settings.CENTURION_LOG.getChild(
            'ticket_action_comment_ticket_dependency'
        )

        inverse_exists = TicketDependency.objects.filter(
            ticket = instance.dependent_ticket,
            dependent_ticket = instance.ticket
        )

        user = get_action_user( instance = instance ).get_entity()

        if len( inverse_exists ) == 0 and kwargs.get('signal') == post_save :

            inverse_how_related = instance.how_related

            if instance.how_related == TicketDependency.Related.BLOCKS:

                inverse_how_related = TicketDependency.Related.BLOCKED_BY

            elif instance.how_related == TicketDependency.Related.BLOCKED_BY:

                inverse_how_related = TicketDependency.Related.BLOCKS

            TicketDependency.objects.create(
                ticket = instance.dependent_ticket,
                how_related = inverse_how_related,
                dependent_ticket = instance.ticket,
                organization = instance.dependent_ticket.organization,
                user = user
            )

        TicketCommentActionTicketDependency.objects.create(
            organization = instance.organization,

            ticket = instance.ticket,
            is_closed = True,
            body = '',
            user = user,

            is_create = ( kwargs.get('signal') == post_save ),
            link_type = instance.how_related,
            dependent_ticket_id = instance.dependent_ticket,
        )


    except Exception as e:

        log.error(
            msg = str(
                'unable to save action comment for a ticket '
                'vars: '
                f"sender={sender._meta.app_label}.{sender._meta.model_name} "
                # f"action_comment_source={action_comment_source} "
                f"model={instance._meta.model_name} "
                f"app_label={instance._meta.app_label} "
                f"context={instance.context} "
                f"context2={type(instance).context} "
            ),
            exc_info = True
        )
