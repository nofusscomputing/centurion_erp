import pytest

from django.test import TestCase

from core.models.ticket_comment_action import TicketCommentAction
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_viewset import TicketCommentBaseViewsetInheritedCases



@pytest.mark.model_ticketcommentaction
class TicketCommentActionViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):


    @classmethod
    def setUpTestData(self):

        self.model = TicketCommentAction

        super().setUpTestData()



class TicketCommentActionViewsetInheritedCases(
    TicketCommentActionViewsetTestCases,
):
    """Test Suite for Sub-Models of TicketBase
    
    Use this Test suit if your sub-model inherits directly from TicketCommentAction.
    """

    model: str = None
    """name of the model to test"""



@pytest.mark.module_core
class TicketCommentActionViewsetTest(
    TicketCommentActionViewsetTestCases,
    TestCase,
):
    pass
