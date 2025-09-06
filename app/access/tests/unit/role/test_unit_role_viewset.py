import pytest

from access.viewsets.role import (
    Role,
    ViewSet,
)

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    ModelViewSetInheritedCases
)



@pytest.mark.model_role
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
                'value': None
            },
            'back_url': {
                'type': type(None),
            },
            'documentation': {
                'type': type(None),
            },
            'filterset_fields': {
                'value': [
                   'organization',
                   'permissions'
                ]
            },
            'model': {
                'value': Role
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'model_notes',
                    'name'
                ]
            },
            'view_description': {
                'value': 'Available Roles'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class RoleViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class RoleViewsetPyTest(
    ViewsetTestCases,
):
    pass
