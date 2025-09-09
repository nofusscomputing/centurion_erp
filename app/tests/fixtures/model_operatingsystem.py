import datetime
import pytest

from django.db.models.deletion import ProtectedError

from itam.models.operating_system import OperatingSystem
from itam.serializers.operating_system import (
    OperatingSystemBaseSerializer,
    OperatingSystemModelSerializer,
    OperatingSystemViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_operatingsystem(django_db_blocker):

    yield OperatingSystem

    with django_db_blocker.unblock():

        for db_obj in OperatingSystem.objects.all():

            try:
                db_obj.delete()
            except ProtectedError:
                pass


@pytest.fixture( scope = 'class')
def kwargs_operatingsystem(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_manufacturer, model_manufacturer,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        publisher = model_manufacturer.objects.create( **kwargs_manufacturer.copy() )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'os' + random_str,
        'publisher': publisher,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        publisher.delete()


@pytest.fixture( scope = 'class')
def serializer_operatingsystem():

    yield {
        'base': OperatingSystemBaseSerializer,
        'model': OperatingSystemModelSerializer,
        'view': OperatingSystemViewSerializer
    }
