import pytest

# from django.db import models
# from types import NoneType

from api.tests.unit.viewset.test_unit_tenancy_viewset import (
    SubModelViewSetInheritedCases
)

from core.models.ticket_comment_solution import TicketCommentSolution
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_viewset import (
    TicketCommentBaseViewsetInheritedCases
)
# from core.viewsets.ticket_comment import (
#     # NoDocsViewSet,
#     TicketBase,
#     TicketCommentSolution,
#     ViewSet
# )


@pytest.mark.model_ticketcommentsolution
class ViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):


    # @pytest.fixture( scope = 'function' )
    # def viewset(self):
    #     return ViewSet


    @property
    def parameterized_class_attributes(self):
        return {
            # '_has_import': {
            #     'type': bool,
            #     'value': False
            # },
            # '_has_purge': {
            #     'type': bool,
            #     'value': False
            # },
            # '_has_triage': {
            #     'type': bool,
            #     'value': False
            # },
            # '_model_documentation': {
            #     'type': NoneType,
            # },
            # 'base_model': {
            #     'value': TicketCommentSolution,
            # },
            # 'back_url': {
            #     'type': NoneType,
            # },
            # 'documentation': {
            #     'type': NoneType,
            # },
            # 'filterset_fields': {
            #     'value': [
            #         'category',
            #         'external_system',
            #         'external_system',
            #         'is_template',
            #         'organization',
            #         'parent',
            #         'source',
            #         'template',
            #     ]
            # },
            'model': {
                'value': TicketCommentSolution
            },
            # 'model_documentation': {
            #     'type': NoneType,
            # },
            # 'model_kwarg': {
            #     'value':'ticket_comment_model',
            # },
            # 'model_suffix': {
            #     'type': NoneType,
            # },
            # 'parent_model': {
            #     'type': models.base.ModelBase,
            #     'value': TicketBase
            # },
            # 'parent_model_pk_kwarg': {
            #     'value': 'ticket_id'
            # },
            # 'search_fields': {
            #     'value': [
            #         'body',
            #     ]
            # },
            # 'serializer_class': {
            #     'type': NoneType,
            # },
            # 'view_description': {
            #     'value': 'Comments made on Ticket'
            # },
            # 'view_name': {
            #     'type': NoneType,
            # },
            # 'view_serializer_name': {
            #     'type': NoneType,
            # },
        }



class TicketCommentSolutionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentSolutionViewsetPyTest(
    ViewsetTestCases,
):

    pass
