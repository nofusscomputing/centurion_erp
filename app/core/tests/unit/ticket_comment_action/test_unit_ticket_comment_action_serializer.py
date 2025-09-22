import pytest

# from centurion.tests.abstract.mock_view import MockView
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_serializer import (
    TicketCommentBaseSerializerInheritedCases
)



@pytest.mark.model_ticketcommentaction
class TicketCommentActionSerializerTestCases(
    TicketCommentBaseSerializerInheritedCases
):
    pass


class TicketCommentActionSerializerInheritedCases(
    TicketCommentActionSerializerTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentActionSerializerPyTest(
    TicketCommentActionSerializerTestCases
):
    pass
