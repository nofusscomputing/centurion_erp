import pytest

from datetime import datetime

from itim.models.clusters import ClusterType
from itim.serializers.cluster_type import (
    ClusterTypeBaseSerializer,
    ClusterTypeModelSerializer,
    ClusterTypeViewSerializer
)



@pytest.fixture( scope = 'class')
def model_clustertype(clean_model_from_db):

    yield ClusterType

    clean_model_from_db(ClusterType)


@pytest.fixture( scope = 'class')
def kwargs_clustertype(kwargs_centurionmodel):

    def factory():

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'clustertype_' +  str( datetime.now().strftime("%H%M%S") + f"{datetime.now().microsecond // 100:04d}" ),
            'config': { 'config_key_1': 'config_value_1' }
        }

        return kwargs

    yield factory


@pytest.fixture( scope = 'class')
def serializer_clustertype():

    yield {
        'base': ClusterTypeBaseSerializer,
        'model': ClusterTypeModelSerializer,
        'view': ClusterTypeViewSerializer
    }
