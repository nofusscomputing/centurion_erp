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

    # clean_model_from_db(ITAssetRelationships)



@pytest.fixture( scope = 'class')
def kwargs_itassetrelationships(
    kwargs_centurionmodel,
    model_itasset, kwargs_itasset,
    model_itassetmodel, kwargs_itassetmodel,
):

    def factory():

        parent_asset_model = model_itassetmodel.objects.create( **kwargs_itassetmodel() )

        kwargs = kwargs_itasset()

        parent = model_itasset.objects.create( **kwargs )

        kwargs = kwargs_centurionmodel()
        del kwargs['organization']

        kwargs = {
            **kwargs,
            'name': 'dev-' + str( datetime.now().strftime("%H%M%S"
                ) + f"{datetime.now().microsecond // 100:04d}" ),
            'parent_asset_model': parent_asset_model,
            # 'parent_asset_model': parent.device_model,
            # 'parent': parent,

        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itassetrelationships():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
