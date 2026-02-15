import difflib
from logging import Logger

from django.conf import settings
from django.db import models
from django.db.models.signals import (
    m2m_changed,
    post_delete,
    post_save,
)
from django.dispatch import receiver

from core.models.ticket_base import TicketBase
from core.models.ticket_comment_action import TicketCommentAction



def create_action_comment(ticket, text, user) -> None:

    TicketCommentAction.objects.create(
        organization = ticket.organization,
        ticket = ticket,
        is_closed = True,
        comment_type = TicketCommentAction._meta.sub_model_type,
        body = text,
        user = user,
    )


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


def filter_models(instance, created) -> str | None:
    """Filter Models / Get Comment source

    Not all models should create an action comment. This function filters those
    models out. On the inverse, will return the comment source for the action.

    Args:
        instance (Model): The model to check
        created (bool): was the save action a Creation.

    Returns:
        str: The action source
        None: Dont create an action comment
    """

    action_comment_models: list = []

    base_model = getattr(instance, '_base_model', None)

    if base_model:

        base_model = base_model._meta.model_name

    user = get_action_user(instance = instance)

    if(
        base_model == 'modelticket'
        and user
    ):

        model_field = getattr(instance, 'model', None)

        model_name = getattr(model_field, '_meta', '')
        model_check = False

        if model_name:
            model_name = model_name.model_name

            model_check = (model_name == str(model_name).replace('ticket', ''))

        if(
            (
                model_check
                and not model_field._ticket_linkable
            ) or instance.__class__ == instance._base_model
        ):
            return None

        return 'model'    # Action comment for linking model


    elif(
        base_model == 'ticketbase'
        and not created
        and user
    ):

        return 'ticket'    # Action comment ticket save


    elif(
        instance._meta.model_name not in action_comment_models
        and base_model != 'ticketbase'
    ):
 
        return None


    return None



def ticket(instance) -> None:
    """Create Action comment for editing a ticket field

    Args:
        instance (Model): The ticket that the action comment will be created
            for.
    """


    excluded_fields: list = [
        'created',
        'date_closed',
        'date_solved',
        'is_closed',
        'is_solved',
        'modified'
    ]
    changed_fields: list = []

    fields = [ value.name for value in instance._meta.fields ]

    _after = instance.get_audit_values()

    for field, value in instance._before.items():

        if (
            instance._before[field] != _after[field]
            and field not in excluded_fields
            and (
                field in fields
                or (
                    str( field )[0:len(field)-3] in fields
                    and str( field ).endswith('_id')
                )
            )
        ):

            changed_fields = changed_fields + [ field ]


    for field_name in changed_fields:

        comment_text = None

        field = instance._meta.get_field(field_name)

        value = None

        if(
            field_name not in instance._before
            and field_name in _after
        ):    # Add

            to_value = instance._after[field_name]

        elif(
            field_name in instance._before
            and field_name in _after
            and instance._before != _after
        ):    # Change

            value = instance._before[field_name]
            to_value = _after[field_name]

        elif(
            field_name in instance._before
            and field_name not in _after
        ):    # Remove

            value = instance._before[field_name]

        else:
            continue


        if isinstance(instance._meta.get_field(field_name), models.DateTimeField):

            if value:
                value = str(value.utcfromtimestamp(value.timestamp()))+ '+00:00'


            if to_value:
                to_value = str(to_value.utcfromtimestamp(to_value.timestamp()))+ '+00:00'


        elif isinstance(instance._meta.get_field(field_name), models.ForeignKey):

            if value:
                value = f'${instance._meta.get_field(field_name).related_model.model_tag}-{value.id}'


            if to_value:
                to_value = f'${instance._meta.get_field(field_name).related_model.model_tag}-{to_value.id}'


        elif getattr(instance._meta.get_field(field_name), 'choices', None) is not None:

            choices_class = None

            if field_name == 'impact':

                choices_class = instance.TicketImpact

            elif field_name == 'priority':

                choices_class = instance.TicketPriority

            elif field_name == 'status':

                choices_class = instance.TicketStatus

            elif field_name == 'urgency':

                choices_class = instance.TicketUrgency


            if choices_class:

                if value:
                    value = choices_class(value).label


                if to_value:
                    to_value = choices_class(to_value).label


        elif field_name == 'description':

                comment_field_value = ''.join(
                    str(x) for x in list(
                        difflib.unified_diff(
                            str(value + '\n').splitlines(keepends=True),
                            str(to_value + '\n').splitlines(keepends=True),
                            fromfile = 'before',
                            tofile = 'after',
                            n = 10000,
                            lineterm = '\n'
                        )
                    )
                ) + ''

                comment_text = '<details><summary>Changed the Description</summary>\n\n``` diff \n\n' + comment_field_value + '\n\n```\n\n</details>'


        if not comment_text:

            comment_text = f"Changed {instance._meta.get_field(field_name).verbose_name} from _{value}_ to **{to_value}**"


        create_action_comment(
            ticket = instance,
            user = type(instance).context[instance._meta.model_name].get_entity(),
            text = comment_text
        )



def ticket_m2m(instance, field, model, action:str, ids: list[int] ) -> None:
    """Create an action comment for a ticket m2m field

    Args:
        instance (Model): The ticket instance to create the action comment on.
        field (Field): The m2m field where the edit occured.
        model (Model): The m2m model where the edit occured.
        action (str): What action occured. choice: add | remove.
        ids (list[int]): The model ids that were add/removed.

    Raises:
        ValueError: Unable to determin the models name.
    """
    for id in ids:

        if model._meta.model_name == 'entity':

            if action == 'add':

                comment_text = f'Added REPLACE-ME to {field.verbose_name}'

            elif action == 'remove':

                comment_text = f'Removed REPLACE-ME from {field.verbose_name}'


            comment_text = comment_text.replace('REPLACE-ME', f'${model._meta.model_name}-{id}')


        else:

            raise ValueError(
                    f'Unable to update m2m field {field.verbose_name} '
                    f'on ticket id={instance.id} as the model could not be '
                    f'determined. The action was {action}.'
            )



        create_action_comment(
            ticket = instance,
            user = type(instance).context[instance._meta.model_name].get_entity(),
            text = comment_text
        )



def link_model_ticket(instance, action:str) -> None:
    """Create action comment when model linked

    Args:
        instance (Model): Model that was linked to ticket
        action (str): What action occured. choice: '' | delete.
    """

    text: str = 'Linked model'
    if action == 'delete':

        text: str = 'Un-linked model'


    create_action_comment(
        ticket = instance.ticket,
        user = get_action_user( instance = instance ).get_entity(),
        text = f'{text} ${instance.model.model_tag}-{instance.model.id}'
    )



@receiver(signal=m2m_changed, sender=TicketBase.assigned_to.through, dispatch_uid="ticket_action_comment_save")
@receiver(signal=m2m_changed, sender=TicketBase.subscribed_to.through, dispatch_uid="ticket_action_comment_save")
@receiver(signal=post_delete, dispatch_uid="ticket_action_comment_save")
@receiver(signal=post_save, dispatch_uid="ticket_action_comment_save")
def ticket_action_comment(sender, instance, created = False, **kwargs) -> None:

    action: str = kwargs.get('action', '')

    if kwargs.get('signal') is post_delete:
        action = 'post_delete'

    action_comment_source = filter_models(instance, created)

    try:

        log: Logger = settings.CENTURION_LOG.getChild('ticket_action_comment')

        if(
            action_comment_source is None
            or kwargs.get('created', False)
            or action.startswith('pre_')
        ):

            return

        elif action_comment_source == 'ticket':

            if action in ['post_add', 'post_remove']:    # m2m field edit

                field = None

                for m2m_field in instance._meta.many_to_many:

                    if m2m_field.remote_field.through == sender:

                        field = m2m_field


                ticket_m2m(
                    instance = instance,
                    field = field,
                    model = kwargs['model'],
                    action = str(action)[5:],
                    ids = list(kwargs['pk_set']),
                    
                )

            elif action == '':    # Ticket edit

                ticket( instance )


        elif action_comment_source == 'model':    # Model linked / un-linked

            link_model_ticket(
                instance = instance, 
                action = str(action)[5:],
            )


    except Exception as e:

        log.error(
            msg = str(
                'unable to save action comment for a ticket '
                'vars: '
                f"sender={sender._meta.app_label}.{sender._meta.model_name} "
                f"action_comment_source={action_comment_source} "
                f"model={instance._meta.model_name} "
                f"app_label={instance._meta.app_label} "
                f"context={instance.context} "
                f"context2={type(instance).context} "
            ),
            exc_info = True
        )
