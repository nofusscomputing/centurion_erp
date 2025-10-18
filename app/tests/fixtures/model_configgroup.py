import pytest

from datetime import datetime

from config_management.models.groups import ConfigGroups
from config_management.serializers.config_group import  (
    ConfigGroupBaseSerializer,
    ConfigGroupModelSerializer,
    ConfigGroupViewSerializer,
)



@pytest.fixture( scope = 'class')
def model_configgroups(clean_model_from_db):

    yield ConfigGroups

    clean_model_from_db(ConfigGroups)


@pytest.fixture( scope = 'class')
def kwargs_configgroups(django_db_blocker,
    kwargs_centurionmodel
):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'cg' + str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'config': {"key": "one", "existing": "dont_over_write"},
            'modified': '2024-06-03T23:00:00Z',
            }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_configgroups():

    yield {
        'base': ConfigGroupBaseSerializer,
        'model': ConfigGroupModelSerializer,
        'view': ConfigGroupViewSerializer
    }
