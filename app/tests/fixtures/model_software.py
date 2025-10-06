import pytest
import random

from itam.models.software import Software
from itam.serializers.software import (
    SoftwareBaseSerializer,
    SoftwareModelSerializer,
    SoftwareViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_software(clean_model_from_db):

    yield Software

    clean_model_from_db(Software)


@pytest.fixture( scope = 'class')
def kwargs_software(kwargs_centurionmodel, django_db_blocker,
    model_manufacturer, kwargs_manufacturer,
    model_softwarecategory, kwargs_softwarecategory
):

    def factory():

        with django_db_blocker.unblock():

            publisher = model_manufacturer.objects.create( **kwargs_manufacturer() )

            kwargs = kwargs_softwarecategory()
            kwargs['name'] = 'soft_c_' + str( random.randint(1,999) ) + str( random.randint(1,999) ) + str( random.randint(1,999) ),

            category = model_softwarecategory.objects.create( **kwargs )

        kwargs = {
            **kwargs_centurionmodel(),
            'publisher': publisher,
            'name': 'software_' + str( random.randint(1,999) ) + str( random.randint(1,999) ) + str( random.randint(1,999) ),
            'category': category,
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_software():

    yield {
        'base': SoftwareBaseSerializer,
        'model': SoftwareModelSerializer,
        'view': SoftwareViewSerializer
    }
