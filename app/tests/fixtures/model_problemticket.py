import pytest

from itim.models.ticket_problem import ProblemTicket
# from itim.serializers.ticketbase_request import (
#     BaseSerializer,
#     ModelSerializer,
#     ViewSerializer
# )



@pytest.fixture( scope = 'class')
def model_problemticket(clean_model_from_db):

    yield ProblemTicket

    clean_model_from_db(ProblemTicket)


@pytest.fixture( scope = 'class')
def kwargs_problemticket(kwargs_ticketbase,

):

    def factory():

        kwargs = {
            **kwargs_ticketbase(),
        }

        return kwargs

    yield factory



# @pytest.fixture( scope = 'class')
# def serializer_problemticket():

#     yield {
#         'base': BaseSerializer,
#         'model': ModelSerializer,
#         'view': ViewSerializer
#     }
