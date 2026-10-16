import pytest
import random

from itam.models.software import SoftwareVersion
from itam.serializers.software_version import (
    SoftwareVersionBaseSerializer,
    SoftwareVersionModelSerializer,
    SoftwareVersionViewSerializer
)



@pytest.fixture( scope = 'class')
def model_softwareversion(clean_model_from_db):

    yield SoftwareVersion

    clean_model_from_db(SoftwareVersion)


@pytest.fixture( scope = 'class')
def kwargs_softwareversion(django_db_blocker,
    kwargs_centurionmodel,
    kwargs_software, model_software
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_software()

            software = model_software.objects.create( **kwargs_software() )

        kwargs = {
            **kwargs_centurionmodel(),
            'software': software,
            'name': 'softwareversion_' + str( random.randint(1,999) ) + str( random.randint(1,999) ) + str( random.randint(1,999) ),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_softwareversion():

    yield {
        'base': SoftwareVersionBaseSerializer,
        'model': SoftwareVersionModelSerializer,
        'view': SoftwareVersionViewSerializer
    }
