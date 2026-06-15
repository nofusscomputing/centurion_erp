import pytest

from core.models.ticket_comment_action import TicketCommentAction

from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_model import (
    TicketCommentActionModelInheritedCases
)



@pytest.mark.model_ticketcommentactionfieldedit
class TicketCommentActionFieldEditModelTestCases(
    TicketCommentActionModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_base_model': {
                'value': TicketCommentAction,
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}



class TicketCommentActionFieldEditModelInheritedCases(
    TicketCommentActionFieldEditModelTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentActionFieldEditModelPyTest(
    TicketCommentActionFieldEditModelTestCases,
):
    pass
