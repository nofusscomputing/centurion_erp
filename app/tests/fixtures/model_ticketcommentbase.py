import datetime
import pytest

from core.models.ticket_comment_base import TicketCommentBase



@pytest.fixture( scope = 'class')
def model_ticketcommentbase(request):

    yield TicketCommentBase


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentbase(django_db_blocker, kwargs_centurionmodel,
    model_person, kwargs_person, model_ticketcommentbase,
    model_ticketbase, kwargs_ticketbase
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        person = model_person.objects.create( **kwargs_person )

        ticket = model_ticketbase.objects.create( **kwargs_ticketbase )

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    kwargs = {
        **kwargs,
        'body': 'a comment body',
        'comment_type': model_ticketcommentbase._meta.sub_model_type,
        'ticket': ticket,
        'user': person,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        person.delete()