import pytest

from project_management.models.ticket_project_task import ProjectTaskTicket
from project_management.serializers.ticketbase_projecttaskticket import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_projecttaskticket(clean_model_from_db):

    yield ProjectTaskTicket

    clean_model_from_db(ProjectTaskTicket)


@pytest.fixture( scope = 'class')
def kwargs_projecttaskticket(kwargs_ticketbase,

):

    def factory():

        kwargs = {
            **kwargs_ticketbase(),
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_projecttaskticket():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
