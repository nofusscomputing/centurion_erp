import pytest
import random

from accounting.models.asset_base import AssetBase

@pytest.fixture( scope = 'class')
def model_assetbase(clean_model_from_db):

    yield AssetBase

    clean_model_from_db(AssetBase)


@pytest.fixture( scope = 'class')
def kwargs_assetbase( kwargs_centurionmodel, model_assetbase ):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'asset_number': 'ab_' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'serial_number': 'ab_' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            # 'asset_type': (model_assetbase._meta.sub_model_type, model_assetbase._meta.verbose_name),
        }

        return kwargs

    yield factory
