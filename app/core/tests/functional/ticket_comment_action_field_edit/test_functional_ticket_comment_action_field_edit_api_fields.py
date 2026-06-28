import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_api_fields import (
    TicketCommentActionAPIInheritedCases
)



@pytest.mark.model_ticketcommentactionfieldedit
class TicketCommentActionFieldEditAPITestCases(
    TicketCommentActionAPIInheritedCases,
):
    
    @property
    def parameterized_api_fields(self):

        return {

            'field_name': {
                'expected': str
            },
            'previous_value': {
                'expected': str
            },
            'new_value': {
                'expected': str
            },
        }




class TicketCommentActionFieldEditAPIInheritedCases(
    TicketCommentActionFieldEditAPITestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentActionFieldEditAPIPyTest(
    TicketCommentActionFieldEditAPITestCases,
):
    pass
