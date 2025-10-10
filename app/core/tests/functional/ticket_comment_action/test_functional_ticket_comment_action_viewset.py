
import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_viewset import (
    TicketCommentBaseViewsetInheritedCases
)



@pytest.mark.model_ticketcommentaction
class ViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):
    pass


class TicketCommentActionViewsetInheritedCases(
    ViewsetTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentActionViewsetPyTest(
    ViewsetTestCases,
):

    pass
