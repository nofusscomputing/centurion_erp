import datetime
import pytest

from itam.models.itam_asset_base import ITAMAssetBase

@pytest.fixture( scope = 'class')
def model_itamassetbase(clean_model_from_db):

    yield ITAMAssetBase

    clean_model_from_db(ITAMAssetBase)


@pytest.fixture( scope = 'class')
def kwargs_itamassetbase( kwargs_assetbase, model_itamassetbase ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_assetbase.copy(),
        # 'asset_type': (model_itamassetbase._meta.sub_model_type, model_itamassetbase._meta.verbose_name),
        'itam_type': "it_asset"
    }

    yield kwargs.copy()
