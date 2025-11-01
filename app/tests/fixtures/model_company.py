import pytest

from datetime import datetime

from access.models.company_base import Company
from access.serializers.entity_company import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_company(clean_model_from_db):

    yield Company

    clean_model_from_db(Company)


@pytest.fixture( scope = 'class')
def kwargs_company( kwargs_entity ):

    def factory():

        kwargs = {
            **kwargs_entity(),
            'entity_type': 'company',
            'name': 'c' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_company():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
