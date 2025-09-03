import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from devops.viewsets.feature_flag import (
    FeatureFlag,
    ViewSet,
)



@pytest.mark.model_featureflag
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
                    'enabled',
                    'organization',
                    'software'
                ]
            },
            'model': {
                'value': FeatureFlag
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'description',
                    'name'
                ]
            },
            'view_description': {
                'value': 'Software Development Feature Flags'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class FeatureFlagViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_devops
class FeatureFlagViewsetPyTest(
    ViewsetTestCases,
):

    pass
