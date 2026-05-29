from django.core.exceptions import ValidationError
from django.db.models.signals import (
    m2m_changed,
)
from django.dispatch import receiver

from access.models.person import Person
from core.models.ticket_base import TicketBase



@receiver(
    signal=m2m_changed,
    sender=TicketBase.assigned_to.through,
    dispatch_uid="ticketbase_validation_m2m_assigned_to"
)
def ticketbase_validation_m2m_assigned_to(
    sender,
    instance,
    action,
    model,
    pk_set,
    **kwargs
) -> None:

    if action != 'pre_add':

        return


    for assigned_to in model.objects.filter(pk__in=list(pk_set)):

        actual_model = assigned_to.get_related_model()

        if not isinstance(actual_model, Person):

            raise ValidationError(
                message = {'assigned_to': 'Ticket must be assigned to a entity of type person.'},
                code = 'assigned_to_must_be_person'
            )
