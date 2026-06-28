import pytest

from core.tests.functional.ticket_comment_action.test_functional_ticket_comment_action_api_fields import (
    TicketCommentActionAPIInheritedCases
)



@pytest.mark.model_ticketcommentactionmodellink
class TicketCommentActionModelLinkAPITestCases(
    TicketCommentActionAPIInheritedCases,
):
    
    @property
    def parameterized_api_fields(self):

        return {

            'is_create': {
                'expected': bool
            },
            'model_id': {
                'expected': int
            },
            'content_type': {
                'expected': int
            },
        }




class TicketCommentActionModelLinkAPIInheritedCases(
    TicketCommentActionModelLinkAPITestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentActionModelLinkAPIPyTest(
    TicketCommentActionModelLinkAPITestCases,
):
    pass
