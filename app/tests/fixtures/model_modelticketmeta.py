import pytest
import random

from django.db import models

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

    model_objs = []
    def factory(model_objs = model_objs):

        with django_db_blocker.unblock():

            kwargs = kwargs_device()
            kwargs['name'] = 'model-ticket-' + str( random.randint(1, 99999))

            device = model_device.objects.create( **kwargs )

            model_objs += [ device ]

            kwargs = {
                **kwargs_modelticket(),
                'model': device
            }

        return kwargs

    yield factory

    with django_db_blocker.unblock():

        for obj in model_objs:
            try:
                obj.delete()
            except models.deletion.ProtectedError:
                pass


@pytest.fixture( scope = 'class')
def serializer_modelticketmetamodel():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
