import pytest

from django.contrib.contenttypes.models import ContentType



@pytest.fixture( scope = 'class')
def model_contenttype():

    yield ContentType


@pytest.fixture( scope = 'class')
def content_type():

    yield ContentType
