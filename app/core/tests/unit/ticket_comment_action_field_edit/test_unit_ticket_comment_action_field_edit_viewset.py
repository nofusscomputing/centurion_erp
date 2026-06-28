import pytest

from core.models.ticket_comment_action_field_edit import TicketCommentActionFieldEdit
from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_viewset import (
    TicketCommentActionViewsetInheritedCases
)



@pytest.mark.model_ticketcommentactionfieldedit
class ViewsetTestCases(
    TicketCommentActionViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': TicketCommentActionFieldEdit
            },
        }



class TicketCommentActionFieldEditViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentActionFieldEditViewsetPyTest(
    ViewsetTestCases,
):

    pass
