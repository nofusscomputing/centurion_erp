import pytest
import random

from core.models.model_tickets import ModelTicketMetaModel
from core.serializers.modelticket import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_modelticketmetamodel(clean_model_from_db):

    yield ModelTicketMetaModel

    clean_model_from_db(ModelTicketMetaModel)



@pytest.fixture( scope = 'class')
def kwargs_modelticketmetamodel(django_db_blocker,
    kwargs_modelticket,
    model_device, kwargs_device,
):

    with django_db_blocker.unblock():

        kwargs = kwargs_device.copy()
        kwargs['name'] = 'model-ticket-' + str( random.randint(1, 99999))

        device = model_device.objects.create( **kwargs )

        kwargs = {
            **kwargs_modelticket.copy(),
            'model': device
        }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        device.delete()


@pytest.fixture( scope = 'class')
def serializer_modelticketmetamodel():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
