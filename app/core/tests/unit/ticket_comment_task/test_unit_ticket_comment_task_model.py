import pytest

from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_model import (
    TicketCommentBaseModelInheritedCases
)



@pytest.mark.model_ticketcommenttask
class TicketCommentTaskModelTestCases(
    TicketCommentBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_is_submodel': {
                'value': True
            },
            '_notes_enabled': {
                'value': False
            },
            'model_tag': {
                'type': type(None),
                'value': None
            },
            'url_model_name': {
                'type': str,
                'value': 'ticket_comment_base'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}



class TicketCommentTaskModelInheritedCases(
    TicketCommentTaskModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_core
class TicketCommentTaskModelPyTest(
    TicketCommentTaskModelTestCases,
):

    sub_model_type = 'task'
