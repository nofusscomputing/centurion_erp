
import pytest

from datetime import datetime

from itam.models import ITAssetModel

from itam.serializers.itassetmodel import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetmodel(clean_model_from_db):

    yield ITAssetModel

    clean_model_from_db(ITAssetModel)



@pytest.fixture( scope = 'class')
def kwargs_itassetmodel( django_db_blocker, kwargs_centurionmodel,
    model_company, kwargs_company
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_company()
            kwargs['name'] = 'dm_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )
            manufacturer = model_company.objects.create( **kwargs )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'devmodel' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'manufacturer': manufacturer,
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itassetmodel():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
