import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from itim.viewsets.cluster import (
    Cluster,
    ViewSet,
)



@pytest.mark.model_cluster
class ViewsetTestCases(
    ModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_model_documentation': {
                'type': type(None),
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
                'value': None
            },
            'filterset_fields': {
                'value': [
                    'parent_cluster',
                    'cluster_type',
                    'nodes',
                    'devices'
                ]
            },
            'model': {
                'value': Cluster
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name',
                ]
            },
            'view_description': {
                'value': 'Physical Devices'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class ClusterViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_itim
class ClusterViewsetPyTest(
    ViewsetTestCases,
):

    pass
