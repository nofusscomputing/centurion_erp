import pytest

from core.models.ticket_comment_task import TicketCommentTask
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_viewset import (
    TicketCommentBaseViewsetInheritedCases
)



@pytest.mark.model_ticketcommenttask
class ViewsetTestCases(
    TicketCommentBaseViewsetInheritedCases,
):


    @property
    def parameterized_class_attributes(self):
        return {
            'model': {
                'value': TicketCommentTask
            },
        }



class TicketCommentTaskViewsetInheritedCases(
    ViewsetTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentTaskViewsetPyTest(
    ViewsetTestCases,
):

    pass
