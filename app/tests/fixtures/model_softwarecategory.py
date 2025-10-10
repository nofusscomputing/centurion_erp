import pytest
import random

from itam.models.software import SoftwareCategory
from itam.serializers.software_category import (
    SoftwareCategoryBaseSerializer,
    SoftwareCategoryModelSerializer,
    SoftwareCategoryViewSerializer
)



@pytest.fixture( scope = 'class')
def model_softwarecategory(clean_model_from_db):

    yield SoftwareCategory

    clean_model_from_db(SoftwareCategory)


@pytest.fixture( scope = 'class')
def kwargs_softwarecategory(kwargs_centurionmodel):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'sc_' + str( random.randint(1,999) ) + str( random.randint(1,999) ) + str( random.randint(1,999) ),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_softwarecategory():

    yield {
        'base': SoftwareCategoryBaseSerializer,
        'model': SoftwareCategoryModelSerializer,
        'view': SoftwareCategoryViewSerializer
    }
