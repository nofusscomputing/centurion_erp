import pytest

from access.viewsets.organization import (
    Tenant,
    ViewSet,
)

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    ModelViewSetInheritedCases
)



@pytest.mark.model_tenant
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
                    'name',
                    'manager',
                ]
            },
            'model': {
                'value': Tenant
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'name'
                ]
            },
            'view_description': {
                'value': 'Centurion Tenants'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class TenantViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_access
class TenantViewsetPyTest(
    ViewsetTestCases,
):
    pass
