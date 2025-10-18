import pytest

from datetime import datetime

from itam.models.operating_system import OperatingSystemVersion
from itam.serializers.operating_system_version import (
    OperatingSystemVersionBaseSerializer,
    OperatingSystemVersionModelSerializer,
    OperatingSystemVersionViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_operatingsystemversion(clean_model_from_db):

    yield OperatingSystemVersion

    clean_model_from_db(OperatingSystemVersion)


@pytest.fixture( scope = 'class')
def kwargs_operatingsystemversion(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_operatingsystem, model_operatingsystem,
):


    def factory():

        with django_db_blocker.unblock():

            os = model_operatingsystem.objects.create(
                **kwargs_operatingsystem()
            )


        kwargs = {
            **kwargs_centurionmodel(),
            'operating_system': os,
            'name': 'osv' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
        }

        return kwargs

    yield factory



@pytest.fixture( scope = 'class')
def serializer_operatingsystemversion():

    yield {
        'base': OperatingSystemVersionBaseSerializer,
        'model': OperatingSystemVersionModelSerializer,
        'view': OperatingSystemVersionViewSerializer
    }
