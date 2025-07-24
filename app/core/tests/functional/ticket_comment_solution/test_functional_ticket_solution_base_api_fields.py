import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_api_fields import (
    TicketCommentBaseAPIFieldsInheritedCases
)



@pytest.mark.model_ticketcommentsolution
class TicketCommentSolutionAPITestCases(
    TicketCommentBaseAPIFieldsInheritedCases,
):

    pass



class TicketCommentSolutionAPIInheritedCases(
    TicketCommentSolutionAPITestCases,
):

    pass



@pytest.mark.module_core
class TicketCommentSolutionAPIPyTest(
    TicketCommentSolutionAPITestCases,
):

    pass
