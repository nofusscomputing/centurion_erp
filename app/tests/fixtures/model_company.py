import datetime
import pytest

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

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_entity.copy(),
        'name': 'c' + random_str,
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_company():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
