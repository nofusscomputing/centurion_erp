import pytest
import random

from core.models.model_tickets import ModelTicket
from core.serializers.modelticket import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_modelticket(clean_model_from_db):

    yield ModelTicket

    clean_model_from_db(ModelTicket)



@pytest.fixture( scope = 'class')
def kwargs_modelticket(django_db_blocker,
    kwargs_centurionmodel, model_contenttype,
    model_ticketbase, kwargs_ticketbase,
):

    model_objs = []
    def factory(model_objs = model_objs):

        with django_db_blocker.unblock():

            kwargs = kwargs_ticketbase()
            kwargs['title'] = 'model_ticket _' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            del kwargs['external_system']
            del kwargs['external_ref']

            ticket = model_ticketbase.objects.create( **kwargs )

            model_objs += [ ticket ]

            kwargs = {
                **kwargs_centurionmodel(),
                'content_type': model_contenttype.objects.filter()[0],
                'ticket': ticket
            }
            del kwargs['model_notes']

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_modelticket():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
