import pytest

from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_serializer import (
    TicketCommentBaseSerializerInheritedCases
)



@pytest.mark.model_ticketcommenttask
class TicketCommentTaskSerializerTestCases(
    TicketCommentBaseSerializerInheritedCases
):
    pass


class TicketCommentTaskSerializerInheritedCases(
    TicketCommentTaskSerializerTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentTaskSerializerPyTest(
    TicketCommentTaskSerializerTestCases
):
    pass
