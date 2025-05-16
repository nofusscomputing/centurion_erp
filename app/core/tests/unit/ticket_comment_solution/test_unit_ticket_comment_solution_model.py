import pytest

from rest_framework.exceptions import ValidationError

from core.models.ticket_comment_solution import TicketCommentSolution
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_model import (
    TicketCommentBaseModelInheritedCases
)


class TicketCommentSolutionModelTestCases(
    TicketCommentBaseModelInheritedCases,
):

    sub_model_type = 'solution'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """

    kwargs_create_item: dict = {
        'comment_type': sub_model_type,
    }


    def test_class_inherits_ticketcommentsolution(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, TicketCommentSolution)



    def test_function_called_clean_ticketcommentsolution(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(TicketCommentSolution, 'clean')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        del valid_data['external_system']
        del valid_data['external_ref']

        comment = model.objects.create(
            **valid_data
        )

        comment.delete()

        assert spy.assert_called_once



class TicketCommentSolutionModelInheritedCases(
    TicketCommentSolutionModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model TicketCommentSolution
    """

    kwargs_create_item: dict = {}

    model = None


    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """



class TicketCommentSolutionModelPyTest(
    TicketCommentSolutionModelTestCases,
):

    pass
