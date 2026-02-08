import pytest

from types import NoneType

from access.permissions.super_user import SuperUserPermissions

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.permissions.ticket import TicketPermission
from core.viewsets.ticket import (
    TicketBase,
    ViewSet,
)



@pytest.mark.tickets
@pytest.mark.model_ticketbase
class ViewsetTestCases(
    SubModelViewSetInheritedCases,
):


    @pytest.fixture( scope = 'function' )
    def viewset(self):
        return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            '_has_import': {
                'type': bool,
                'value': False
            },
            '_has_purge': {
                'type': bool,
                'value': False
            },
            '_has_triage': {
                'type': bool,
                'value': False
            },
            '_model_documentation': {
                'type': NoneType,
            },
            'base_model': {
                'value': TicketBase,
            },
            'back_url': {
                'type': NoneType,
            },
            'documentation': {
                'type': NoneType,
            },
            'filterset_fields': {
                'value': [
                    'organization',
                    'is_deleted'
                ]
            },
            'model': {
                'value': TicketBase
            },
            'model_documentation': {
                'type': NoneType,
            },
            'model_kwarg': {
                'value':'ticket_type',
            },
            'model_suffix': {
                'type': NoneType,
            },
            'permission_classes': {
                'type': list,
                'value': [ TicketPermission | SuperUserPermissions ]
            },
            'search_fields': {
                'value': [
                    'title',
                    'description'
                ]
            },
            'serializer_class': {
                'type': NoneType,
            },
            'view_description': {
                'value': 'All Tickets'
            },
            'view_name': {
                'type': NoneType,
            },
            'view_serializer_name': {
                'type': NoneType,
            },
        }



class TicketBaseViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketBaseViewsetPyTest(
    ViewsetTestCases,
):

    pass
