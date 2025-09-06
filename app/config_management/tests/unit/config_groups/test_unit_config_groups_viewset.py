import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from config_management.viewsets.config_group import (
    ConfigGroups,
    ViewSet,
)



@pytest.mark.model_configgroups
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
                    'parent'
                ]
            },
            'model': {
                'value': ConfigGroups
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
                    'config'
                ]
            },
            'view_description': {
                'value': 'Configuration Groups'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class KnowledgeBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_config_management
class KnowledgeBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
