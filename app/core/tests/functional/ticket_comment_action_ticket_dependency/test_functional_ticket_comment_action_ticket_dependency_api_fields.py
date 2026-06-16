import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_api_fields import (
    TicketCommentActionAPIInheritedCases
)



@pytest.mark.model_ticketcommentactionticketdependency
class TicketCommentActionTicketDependencyAPITestCases(
    TicketCommentActionAPIInheritedCases,
):
    
    @property
    def parameterized_api_fields(self):

        return {

            'is_create': {
                'expected': bool
            },
            'link_type': {
                'expected': int
            },
            'dependent_ticket_id': {
                'expected': int
            },
        }




class TicketCommentActionTicketDependencyAPIInheritedCases(
    TicketCommentActionTicketDependencyAPITestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentActionTicketDependencyAPIPyTest(
    TicketCommentActionTicketDependencyAPITestCases,
):
    pass
