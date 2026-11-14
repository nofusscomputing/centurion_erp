import pytest

from datetime import datetime

from itam.models.itam_asset_base import ITAMAssetBase

from itam.serializers.itassetrelationships import (
    ITAssetRelationships,
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itassetrelationships(clean_model_from_db):

    yield ITAssetRelationships



@pytest.fixture( scope = 'class')
def kwargs_itassetrelationships(django_db_blocker,
    model_itasset, kwargs_itasset,
):

    def factory(parent_model = False):

        with django_db_blocker.unblock():


            kwargs = kwargs_itasset()

            parent = model_itasset.objects.create( **kwargs )

            parent_asset_model = parent.device_model

        kwargs = {
            'name': 'dev-' + str( datetime.now().strftime("%H%M%S"
                ) + f"{datetime.now().microsecond // 100:04d}" ),
            'parent_asset_model': parent_asset_model,
            # 'parent_asset_model': parent.device_model,
            # 'parent': parent,

        }

        if parent_model:
            kwargs['parent'] = parent

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itassetrelationships():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
