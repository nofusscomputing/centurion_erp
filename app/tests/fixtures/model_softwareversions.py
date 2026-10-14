import pytest
import random

from itam.models.software_version import SoftwareVersions
from itam.serializers.software_version import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer
)



@pytest.fixture( scope = 'class')
def model_softwareversions(clean_model_from_db):

    yield SoftwareVersions

    clean_model_from_db(SoftwareVersions)


@pytest.fixture( scope = 'class')
def kwargs_softwareversions(django_db_blocker,
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
def serializer_softwareversions():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
