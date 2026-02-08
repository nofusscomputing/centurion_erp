import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_api_fields import (
    TicketCommentBaseAPIFieldsInheritedCases
)



@pytest.mark.model_ticketcommenttask
class TicketCommentTaskAPITestCases(
    TicketCommentBaseAPIFieldsInheritedCases,
):

    pass



class TicketCommentTaskAPIInheritedCases(
    TicketCommentTaskAPITestCases,
):

    pass



@pytest.mark.module_core
class TicketCommentTaskAPIPyTest(
    TicketCommentTaskAPITestCases,
):

    pass
