import pytest

from django.test import TestCase

from core.models.ticket_comment_solution import TicketCommentSolution
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_viewset import TicketCommentBaseViewsetInheritedCases



@pytest.mark.model_ticketcommentsolution
class TicketCommentSolutionViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):


    @classmethod
    def setUpTestData(self):

        self.model = TicketCommentSolution

        super().setUpTestData()



class TicketCommentSolutionViewsetInheritedCases(
    TicketCommentSolutionViewsetTestCases,
):
    """Test Suite for Sub-Models of TicketBase
    
    Use this Test suit if your sub-model inherits directly from TicketCommentSolution.
    """

    model: str = None
    """name of the model to test"""



@pytest.mark.module_core
class TicketCommentSolutionViewsetTest(
    TicketCommentSolutionViewsetTestCases,
    TestCase,
):
    pass
