import datetime
import pytest

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

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'sc_' + random_str,
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_softwarecategory():

    yield {
        'base': SoftwareCategoryBaseSerializer,
        'model': SoftwareCategoryModelSerializer,
        'view': SoftwareCategoryViewSerializer
    }
