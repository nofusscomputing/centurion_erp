import datetime
import pytest

from django.db import models

from core.models.ticket_comment_base import TicketCommentBase



@pytest.fixture( scope = 'class')
def model_ticketcommentbase(request):

    yield TicketCommentBase


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentbase(django_db_blocker, kwargs_centurionmodel,
    model_person, kwargs_person, model_ticketcommentbase,
    model_ticketbase, kwargs_ticketbase,
    model_ticketcommentcategory, kwargs_ticketcommentcategory
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        person = model_person.objects.create( **kwargs_person )

        ticket = model_ticketbase.objects.create( **kwargs_ticketbase )

        category = model_ticketcommentcategory.objects.create(
            **kwargs_ticketcommentcategory
        )

    kwargs = kwargs_centurionmodel.copy()
    del kwargs['model_notes']

    kwargs = {
        **kwargs,
        # 'parent': '',
        'ticket': ticket,
        'external_ref': 123,
        'external_system': model_ticketbase.Ticket_ExternalSystem.CUSTOM_1,
        'comment_type': model_ticketcommentbase._meta.sub_model_type,
        'category': category,
        'body': 'a comment body',
        'private': False,
        'duration': 1,
        'estimation': 2,
        # 'template': '',
        'is_template': False,
        'source': model_ticketbase.TicketSource.HELPDESK,
        'user': person,
        'is_closed': True,
        'date_closed': '2025-05-09T19:32Z',


    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        person.delete()

        try:
            category.delete()
        except models.deletion.ProtectedError:
            pass