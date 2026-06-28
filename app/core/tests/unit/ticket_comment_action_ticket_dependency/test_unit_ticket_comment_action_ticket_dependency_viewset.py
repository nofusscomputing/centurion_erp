import pytest

from core.models.ticket_comment_action_ticket_dependency import TicketCommentActionTicketDependency
from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_viewset import (
    TicketCommentActionViewsetInheritedCases
)



@pytest.mark.model_ticketcommentactionticketdependency
class ViewsetTestCases(
    TicketCommentActionViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': TicketCommentActionTicketDependency
            },
        }



class TicketCommentActionTicketDependencyViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentActionTicketDependencyViewsetPyTest(
    ViewsetTestCases,
):

    pass
