import datetime
import pytest

from django.db.models.deletion import ProtectedError

from itam.models.software import SoftwareCategory
from itam.serializers.software_category import (
    SoftwareCategoryBaseSerializer,
    SoftwareCategoryModelSerializer,
    SoftwareCategoryViewSerializer
)



@pytest.fixture( scope = 'class')
def model_softwarecategory(django_db_blocker):

    yield SoftwareCategory

    with django_db_blocker.unblock():

        for db_obj in SoftwareCategory.objects.all():

            try:
                db_obj.delete()
            except ProtectedError:
                pass


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
