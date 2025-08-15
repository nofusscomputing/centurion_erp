import datetime
import pytest

from itam.models.software import Software
from itam.serializers.software import (
    SoftwareBaseSerializer,
    SoftwareModelSerializer,
    SoftwareViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_software(request):

    yield Software


@pytest.fixture( scope = 'class')
def kwargs_software(kwargs_centurionmodel, django_db_blocker,
    model_manufacturer, kwargs_manufacturer,
    model_softwarecategory, kwargs_softwarecategory
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))

    with django_db_blocker.unblock():

        publisher = model_manufacturer.objects.create( **kwargs_manufacturer )

        category = model_softwarecategory.objects.create( **kwargs_softwarecategory )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'publisher': publisher,
        'name': 'software_' + random_str,
        'category': category,
    }

    yield kwargs.copy()

    with django_db_blocker.unblock():

        publisher.delete()

        category.delete()


@pytest.fixture( scope = 'class')
def serializer_software():

    yield {
        'base': SoftwareBaseSerializer,
        'model': SoftwareModelSerializer,
        'view': SoftwareViewSerializer
    }
