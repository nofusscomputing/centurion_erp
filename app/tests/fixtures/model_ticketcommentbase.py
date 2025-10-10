import pytest
import random

from core.models.ticket_comment_base import TicketCommentBase
from core.serializers.ticketcommentbase import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_ticketcommentbase(clean_model_from_db):

    yield TicketCommentBase

    clean_model_from_db(TicketCommentBase)


@pytest.fixture( scope = 'class')
def kwargs_ticketcommentbase(django_db_blocker, kwargs_centurionmodel,
    model_person, kwargs_person, model_ticketcommentbase,
    model_ticketbase, kwargs_ticketbase,
    model_ticketcommentcategory, kwargs_ticketcommentcategory
):

    def factory():

        with django_db_blocker.unblock():

            person = model_person.objects.create( **kwargs_person() )

            ticket = model_ticketbase.objects.create( **kwargs_ticketbase() )

            category = model_ticketcommentcategory.objects.create(
                **kwargs_ticketcommentcategory()
            )

        kwargs = kwargs_centurionmodel()
        del kwargs['model_notes']

        kwargs = {
            **kwargs,
            # 'parent': '',
            'ticket': ticket,
            'external_ref': int( random.randint(1,999999)),
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

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_ticketcommentbase():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
