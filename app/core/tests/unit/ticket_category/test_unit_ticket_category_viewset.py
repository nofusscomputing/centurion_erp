import pytest

from api.tests.unit.viewset.test_unit_tenancy_viewset import ModelViewSetInheritedCases

from core.viewsets.ticket_category import (
    TicketCategory,
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
                    'change',
                    'incident',
                    'organization',
                    'problem',
                    'project_task',
                    'request',
                ]
            },
            'model': {
                'value': TicketCategory
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
                'value': 'Categories available for tickets'
            },
            'view_name': {
                'type': type(None),
            },
            'view_serializer_name': {
                'type': type(None),
            }
        }



class TicketCategoryViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCategoryViewsetPyTest(
    ViewsetTestCases,
):

    pass
