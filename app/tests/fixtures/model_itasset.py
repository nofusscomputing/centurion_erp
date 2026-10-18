
import pytest
import random

from datetime import datetime

from itam.models import ITAsset

from itam.serializers.assetbase_itasset import (
    BaseSerializer,
    ModelSerializer,
    ViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_itasset(clean_model_from_db):

    yield ITAsset

    clean_model_from_db(ITAsset)



@pytest.fixture( scope = 'class')
def kwargs_itasset( django_db_blocker, kwargs_itamassetbase,
    model_itassetmodel, kwargs_itassetmodel,
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_itassetmodel()
            kwargs['name'] = 'dev_dm' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" )

            device_model = model_itassetmodel.objects.create( **kwargs )


        kwargs = {
            **kwargs_itamassetbase(),
            'name': 'dev-' + str( datetime.now().strftime("%H%M%S"
                ) + f"{datetime.now().microsecond // 100:04d}" ),


            'uuid': '73'+ str( random.randint(10000, 99999)
                ) + 'c-e3e8-4680-a3bf-2' + str( random.randint(10000, 99999)
                ) + 'e' + str( random.randint(10000, 99999) ),

            'device_model': device_model,
            # 'device_type': device_type,
            'config':  { 'a_dev_config_key': 'a_dev_config_value'},
            'inventorydate': (
                f'2025-{random.randint(1, 12):02d}'
                f'-{random.randint(1, 28):02d}'
                f'T{random.randint(0, 23):02d}:'
                f'{random.randint(0, 59):02d}:'
                f'{random.randint(0, 59):02d}Z'
            ),
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_itasset():

    yield {
        'base': BaseSerializer,
        'model': ModelSerializer,
        'view': ViewSerializer
    }
