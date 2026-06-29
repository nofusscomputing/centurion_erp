import pytest

from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_serializer import (
    TicketCommentActionSerializerInheritedCases
)



@pytest.mark.model_ticketcommentactionfieldedit
class TicketCommentActionFieldEditSerializerTestCases(
    TicketCommentActionSerializerInheritedCases
):
    pass


class TicketCommentActionFieldEditSerializerInheritedCases(
    TicketCommentActionFieldEditSerializerTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentActionFieldEditSerializerPyTest(
    TicketCommentActionFieldEditSerializerTestCases
):
    pass
