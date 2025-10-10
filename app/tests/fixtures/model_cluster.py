import pytest
import random

from itim.models.clusters import Cluster
from itim.serializers.cluster import (
    ClusterBaseSerializer,
    ClusterModelSerializer,
    ClusterViewSerializer
)



@pytest.fixture( scope = 'class')
def model_cluster(clean_model_from_db):

    yield Cluster

    clean_model_from_db(Cluster)


@pytest.fixture( scope = 'class')
def kwargs_cluster(kwargs_centurionmodel, django_db_blocker,
    model_device, kwargs_device,
    model_clustertype, kwargs_clustertype
):

    def factory():

        with django_db_blocker.unblock():

            kwargs = kwargs_device()
            kwargs['serial_number'] = f'clu-{random.randint(100, 999)}-{random.randint(100, 999)}-654'
            kwargs['uuid'] = f'1cf{random.randint(100, 999)}d4-1776-4{random.randint(100, 999)}-8{random.randint(100, 999)}-0{random.randint(100, 999)}4a43d60e'

            node = model_device.objects.create( **kwargs )
            cluster_type = model_clustertype.objects.create( **kwargs_clustertype() )

        kwargs = {
            **kwargs_centurionmodel(),
            'name': 'cluster_' + str( random.randint(1,99)) + str( random.randint(100,199)) + str( random.randint(200,299)),
            'nodes': [ node ],
            'cluster_type': cluster_type,
            'config': { 'config_key_1': 'config_value_1' }
        }

        return kwargs

    yield factory




@pytest.fixture( scope = 'class')
def serializer_cluster():

    yield {
        'base': ClusterBaseSerializer,
        'model': ClusterModelSerializer,
        'view': ClusterViewSerializer
    }
