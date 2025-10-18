import pytest

from datetime import datetime

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
            'asset_number': 'ab_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'serial_number': 'ab_' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            # 'asset_type': (model_assetbase._meta.sub_model_type, model_assetbase._meta.verbose_name),
        }

        return kwargs

    yield factory
