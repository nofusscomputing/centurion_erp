import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases


from config_management.viewsets.config_group_software import (
    ConfigGroupSoftware,
    ViewSet,
)



@pytest.mark.model_configgroupsoftware
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
                    'organization',
                    'software'
                ]
            },
            'model': {
                'value': ConfigGroupSoftware
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': []
            },
            'view_description': {
                'value': 'Software for a config group'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class ConfigGroupsViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_config_management
class ConfigGroupsViewsetPyTest(
    ViewsetTestCases,
):

    pass
