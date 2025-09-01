import pytest

from api.tests.unit.test_unit_common_viewset import ModelViewSetInheritedCases

from devops.viewsets.software_enable_feature_flag import (
    Software,
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
            'parent_model': {
                'value': Software
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'software_id'
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
