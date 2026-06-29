import pytest

from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_serializer import (
    TicketCommentActionSerializerInheritedCases
)



@pytest.mark.model_ticketcommentactionmodellink
class TicketCommentActionModelLinkSerializerTestCases(
    TicketCommentActionSerializerInheritedCases
):
    pass


class TicketCommentActionModelLinkSerializerInheritedCases(
    TicketCommentActionModelLinkSerializerTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentActionModelLinkSerializerPyTest(
    TicketCommentActionModelLinkSerializerTestCases
):
    pass
