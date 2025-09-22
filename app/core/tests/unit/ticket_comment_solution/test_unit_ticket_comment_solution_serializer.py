import pytest

# from centurion.tests.abstract.mock_view import MockView
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_serializer import (
    TicketCommentBaseSerializerInheritedCases
)



@pytest.mark.model_ticketcommentsolution
class TicketCommentSolutionSerializerTestCases(
    TicketCommentBaseSerializerInheritedCases
):
    pass


class TicketCommentSolutionSerializerInheritedCases(
    TicketCommentSolutionSerializerTestCases
):
    pass



@pytest.mark.module_core
class TicketCommentSolutionSerializerPyTest(
    TicketCommentSolutionSerializerTestCases
):
    pass
