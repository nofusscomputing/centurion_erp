import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_api_fields import (
    TicketCommentBaseAPIFieldsInheritedCases
)



@pytest.mark.model_ticketcommentaction
class TicketCommentActionAPITestCases(
    TicketCommentBaseAPIFieldsInheritedCases,
):

    pass



class TicketCommentActionAPIInheritedCases(
    TicketCommentActionAPITestCases,
):

    pass



@pytest.mark.module_core
class TicketCommentActionAPIPyTest(
    TicketCommentActionAPITestCases,
):

    pass
