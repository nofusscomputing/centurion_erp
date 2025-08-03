import datetime
import pytest

from itim.models.clusters import Cluster
from itim.serializers.cluster import (
    ClusterBaseSerializer,
    ClusterModelSerializer,
    ClusterViewSerializer
)



@pytest.fixture( scope = 'class')
def model_cluster():

    yield Cluster


@pytest.fixture( scope = 'class')
def kwargs_cluster(kwargs_centurionmodel, django_db_blocker,
    model_device, kwargs_device,
    model_clustertype, kwargs_clustertype
):

    random_str = str(datetime.datetime.now(tz=datetime.timezone.utc))
    random_str = str(random_str).replace(
            ' ', '').replace(':', '').replace('+', '').replace('.', '')

    with django_db_blocker.unblock():

        node = model_device.objects.create( **kwargs_device )
        cluster_type = model_clustertype.objects.create( **kwargs_clustertype )

    kwargs = {
        **kwargs_centurionmodel.copy(),
        'name': 'cluster_' + random_str,
        'nodes': [ node ],
        'cluster_type': cluster_type,
        'config': { 'config_key_1': 'config_value_1' }
    }

    yield kwargs.copy()


    with django_db_blocker.unblock():

        node.delete()
        cluster_type.delete()



@pytest.fixture( scope = 'class')
def serializer_cluster():

    yield {
        'base': ClusterBaseSerializer,
        'model': ClusterModelSerializer,
        'view': ClusterViewSerializer
    }
