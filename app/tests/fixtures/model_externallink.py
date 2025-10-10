import pytest
import random

from settings.models.external_link import ExternalLink
from settings.serializers.external_links import (
    ExternalLinkBaseSerializer,
    ExternalLinkModelSerializer,
    ExternalLinkViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_externallink(clean_model_from_db):

    yield ExternalLink

    clean_model_from_db(ExternalLink)


@pytest.fixture( scope = 'class')
def kwargs_externallink( model_externallink, kwargs_centurionmodel ):

    def factory():

        random_str = str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299))

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'el' + random_str,
            'button_text': 'bt' + random_str,
            'template': 'boo',
            'colour': '#00FF00',
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_externallink():

    yield {
        'base': ExternalLinkBaseSerializer,
        'model': ExternalLinkModelSerializer,
        'view': ExternalLinkViewSerializer
    }
