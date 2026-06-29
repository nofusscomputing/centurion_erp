import pytest

from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_serializer import (
    TicketCommentActionSerializerInheritedCases
)



@pytest.mark.model_ticketcommentactionticketdependency
class TicketCommentActionTicketDependencySerializerTestCases(
    TicketCommentActionSerializerInheritedCases
):
    pass


class TicketCommentActionTicketDependencySerializerInheritedCases(
    TicketCommentActionTicketDependencySerializerTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentActionTicketDependencySerializerPyTest(
    TicketCommentActionTicketDependencySerializerTestCases
):
    pass
