
import pytest

from datetime import datetime

from itam.models import ITAssetSoftware

from itam.serializers.assetbase_itassetsoftware import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetsoftware(clean_model_from_db):

    yield ITAssetSoftware

    clean_model_from_db(ITAssetSoftware)



@pytest.fixture( scope = 'class')
def kwargs_itassetsoftware( kwargs_itamassetbase, django_db_blocker,
    model_company, kwargs_company,
    model_softwarecategory, kwargs_softwarecategory
):

    def factory():

        with django_db_blocker.unblock():

            publisher = model_company.objects.create( **kwargs_company() )

            kwargs = kwargs_softwarecategory()
            kwargs['name'] = 'soft_c_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),

            category = model_softwarecategory.objects.create( **kwargs )

        kwargs = {
            **kwargs_itamassetbase(),
            'publisher': publisher,
            'name': 'software_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'category': category,
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itassetsoftware():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
