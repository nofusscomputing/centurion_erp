import datetime
import pytest

from settings.models.external_link import ExternalLink
from settings.serializers.external_links import (
    ExternalLinkBaseSerializer,
    ExternalLinkModelSerializer,
    ExternalLinkViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_externallink():

    yield ExternalLink


@pytest.fixture( scope = 'class')
def kwargs_externallink( kwargs_centurionmodel ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'el' + random_str,
        'button_text': 'bt' + random_str,
        'template': 'boo',
        'colour': '#00FF00',
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_externallink():

    yield {
        'base': ExternalLinkBaseSerializer,
        'model': ExternalLinkModelSerializer,
        'view': ExternalLinkViewSerializer
    }
