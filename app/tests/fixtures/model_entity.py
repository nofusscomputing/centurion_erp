import datetime
import pytest

from django.db.models.deletion import ProtectedError

from access.models.entity import Entity
from access.serializers.entity import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_entity(django_db_blocker):

    yield Entity

    with django_db_blocker.unblock():

        for db_obj in Entity.objects.all():

            try:
                db_obj.delete()
            except ProtectedError:
                pass


@pytest.fixture( scope = 'class')
def kwargs_entity( kwargs_centurionmodel ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'entity_type': 'entity',
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_entity():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
