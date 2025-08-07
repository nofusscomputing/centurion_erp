import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from devops.viewsets.software_enable_feature_flag import (
    SoftwareEnableFeatureFlag,
    ViewSet,
)



@pytest.mark.model_softwareenablefeatureflag
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
                'value': SoftwareEnableFeatureFlag
            },
            'model_documentation': {
                'type': type(None),
            },
            'queryset': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': []
            },
            'view_description': {
                'value': 'Enabled Software Development Feature Flags'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class SoftwareEnableFeatureFlagViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_devops
class SoftwareEnableFeatureFlagViewsetPyTest(
    ViewsetTestCases,
):

    pass
