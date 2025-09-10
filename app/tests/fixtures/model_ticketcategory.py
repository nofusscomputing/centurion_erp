import datetime
import pytest

from core.models.ticket.ticket_category import TicketCategory



@pytest.fixture( scope = 'class')
def model_ticketcategory(clean_model_from_db):

    yield TicketCategory

    clean_model_from_db(TicketCategory)


@pytest.fixture( scope = 'class')
def kwargs_ticketcategory(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'tc' + str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', ''),
    }

    yield kwargs.copy()
