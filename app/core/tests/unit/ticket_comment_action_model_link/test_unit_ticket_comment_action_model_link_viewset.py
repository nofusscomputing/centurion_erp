import pytest

from core.models.ticket_comment_action_model_link import TicketCommentActionModelLink
from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_viewset import (
    TicketCommentActionViewsetInheritedCases
)



@pytest.mark.model_ticketcommentactionmodellink
class ViewsetTestCases(
    TicketCommentActionViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': TicketCommentActionModelLink
            },
        }



class TicketCommentActionModelLinkViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentActionModelLinkViewsetPyTest(
    ViewsetTestCases,
):

    pass
