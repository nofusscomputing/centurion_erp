import datetime
import pytest

from itam.models.operating_system import OperatingSystemVersion
from itam.serializers.operating_system_version import (
    OperatingSystemVersionBaseSerializer,
    OperatingSystemVersionModelSerializer,
    OperatingSystemVersionViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_operatingsystemversion():

    yield OperatingSystemVersion


@pytest.fixture( scope = 'class')
def kwargs_operatingsystemversion(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_operatingsystem, model_operatingsystem,
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        os = model_operatingsystem.objects.create(
            **kwargs_operatingsystem.copy()
        )


    kwargs = {
        **kwargs_centurionmodel.copy(),
        'operating_system': os,
        'name': 'osv' + random_str,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        os.delete()


@pytest.fixture( scope = 'class')
def serializer_operatingsystemversion():

    yield {
        'base': OperatingSystemVersionBaseSerializer,
        'model': OperatingSystemVersionModelSerializer,
        'view': OperatingSystemVersionViewSerializer
    }
