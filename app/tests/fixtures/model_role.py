import datetime
import pytest

from access.models.role import Role
from access.serializers.role import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_role():

    yield Role


@pytest.fixture( scope = 'class')
def kwargs_role(
    kwargs_centurionmodel
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('-', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'r_' + random_str,
        'modified': '2024-06-03T23:00:00Z',
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_role():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
