import pytest

from django.db import models

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

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
                'type': models.base.ModelBase,
                'value': Software
            },
            'parent_model_pk_kwarg': {
                'type': str,
                'value': 'software_id'
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



    def test_function_get_parent_model(self, mocker, viewset):
        """Test class function

        Ensure that when function `get_parent_model` is called it returns the value
        of `viewset.parent_model`.

        For all models that dont have attribute `viewset.parent_model` set, it should
        return None
        """

        assert viewset().get_parent_model() is not None



class SoftwareEnableFeatureFlagViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_devops
class SoftwareEnableFeatureFlagViewsetPyTest(
    ViewsetTestCases,
):

    pass
