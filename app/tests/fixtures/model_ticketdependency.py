import pytest

from datetime import datetime

from core.models.ticket_dependencies import TicketDependency
from core.serializers.ticket_dependency import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_ticketdependency(clean_model_from_db):

    yield TicketDependency

    clean_model_from_db(TicketDependency)


@pytest.fixture( scope = 'class')
def kwargs_ticketdependency(django_db_blocker,
    model_ticketbase, kwargs_ticketbase,
    model_ticketdependency,
):


    def factory():

        random_str = str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

        with django_db_blocker.unblock():

            kwargs = kwargs_ticketbase()
            del kwargs['external_system']
            del kwargs['external_ref']

            kwargs['title'] = 'source ' + random_str

            source_ticket = model_ticketbase.objects.create( **kwargs )


            kwargs['title'] = 'dependent ' + random_str

            dependent_ticket = model_ticketbase.objects.create( **kwargs )


        kwargs = {

            'ticket': source_ticket,
            'how_related': model_ticketdependency.Related.RELATED,
            'dependent_ticket': dependent_ticket,
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_ticketdependency():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
