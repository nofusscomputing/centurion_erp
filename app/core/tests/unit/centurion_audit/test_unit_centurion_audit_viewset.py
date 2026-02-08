import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from core.viewsets.audit_history import (
    CenturionAudit,
    ViewSet,
)



@pytest.mark.model_ticketcategory
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
                    'action',
                    'content_type',
                    'organization',
                    'user',
                ]
            },
            'model': {
                'value': CenturionAudit
            },
            'model_documentation': {
                'type': type(None),
            },
            'serializer_class': {
                'type': type(None),
            },
            'search_fields': {
                'value': [
                    'after',
                    'before',
                ]
            },
            'view_description': {
                'value': 'Audit History entries'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class CenturionAuditViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class CenturionAuditViewsetPyTest(
    ViewsetTestCases,
):

    pass
