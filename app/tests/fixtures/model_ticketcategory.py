import pytest

from datetime import datetime

from core.models.ticket.ticket_category import TicketCategory
from core.serializers.ticket_category import (
    TicketCategoryBaseSerializer,
    TicketCategoryModelSerializer,
    TicketCategoryViewSerializer
)



@pytest.fixture( scope = 'class')
def model_ticketcategory(clean_model_from_db):

    yield TicketCategory

    clean_model_from_db(TicketCategory)


@pytest.fixture( scope = 'class')
def kwargs_ticketcategory(kwargs_centurionmodel):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'tc' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_ticketcategory():

    yield {
        'base': TicketCategoryBaseSerializer,
        'model': TicketCategoryModelSerializer,
        'view': TicketCategoryViewSerializer
    }
