import datetime
import pytest

from itim.models.clusters import ClusterType
from itim.serializers.cluster_type import (
    ClusterTypeBaseSerializer,
    ClusterTypeModelSerializer,
    ClusterTypeViewSerializer
)



@pytest.fixture( scope = 'class')
def model_clustertype():

    yield ClusterType


@pytest.fixture( scope = 'class')
def kwargs_clustertype(kwargs_centurionmodel):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'clustertype_' + random_str,
        'config': { 'config_key_1': 'config_value_1' }
    }

    yield kwargs.copy()


@pytest.fixture( scope = 'class')
def serializer_clustertype():

    yield {
        'base': ClusterTypeBaseSerializer,
        'model': ClusterTypeModelSerializer,
        'view': ClusterTypeViewSerializer
    }
