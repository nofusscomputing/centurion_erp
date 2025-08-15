import pytest

from core.tests.functional.ticket_comment_base.test_functional_ticket_comment_base_model import TicketCommentBaseModelInheritedTestCases


@pytest.mark.model_ticketcommentsolution
class TicketCommentSolutionModelTestCases(
    TicketCommentBaseModelInheritedTestCases
):
    pass


    # check closes ticket

    # check ticket status changes to solved



class TicketCommentSolutionModelInheritedTestCases(
    TicketCommentSolutionModelTestCases
):

    pass



@pytest.mark.module_core
class TicketCommentSolutionModelPyTest(
    TicketCommentSolutionModelTestCases
):

    pass
