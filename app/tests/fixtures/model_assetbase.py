import datetime
import pytest

from accounting.models.asset_base import AssetBase

@pytest.fixture( scope = 'class')
def model_assetbase(clean_model_from_db):

    yield AssetBase

    clean_model_from_db(AssetBase)


@pytest.fixture( scope = 'class')
def kwargs_assetbase( kwargs_centurionmodel, model_assetbase ):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'asset_number': 'ab_' + random_str,
        'serial_number': 'ab_' + random_str,
        # 'asset_type': (model_assetbase._meta.sub_model_type, model_assetbase._meta.verbose_name),
    }

    yield kwargs.copy()
