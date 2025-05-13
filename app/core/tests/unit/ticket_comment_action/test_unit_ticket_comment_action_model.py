from rest_framework.exceptions import ValidationError

from core.models.ticket_comment_action import TicketCommentAction
from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_model import (
    TicketCommentBaseModelInheritedCases
)


class TicketCommentActionModelTestCases(
    TicketCommentBaseModelInheritedCases,
):

    sub_model_type = 'action'
    """Sub Model Type
    
    sub-models must have this attribute defined in `ModelName.Meta.sub_model_type`
    """

    kwargs_create_item: dict = {
        'comment_type': sub_model_type,
    }


    def test_class_inherits_ticketcommentaction(self):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(self.model, TicketCommentAction)



    def test_function_called_clean_ticketcommentaction(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(TicketCommentAction, 'clean')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        del valid_data['external_system']
        del valid_data['external_ref']

        model.objects.create(
            **valid_data
        )

        assert spy.assert_called_once


    def test_attribute_value_permissions_has_triage(self):
        """Attribute Check

        This test case is a duplicate of a test with the same name.
        This type of ticket comment does not have a triage permission.

        Ensure attribute `Meta.permissions` value contains permission
        `triage`
        """
        pass



    def test_attribute_value_permissions_has_purge(self):
        """Attribute Check

        This test case is a duplicate of a test with the same name.
        This type of ticket comment does not have a triage permission.
    
        Ensure attribute `Meta.permissions` value contains permission
        `purge`
        """
        pass





class TicketCommentActionModelInheritedCases(
    TicketCommentActionModelTestCases,
):
    """Sub-Ticket Test Cases

    Test Cases for Ticket models that inherit from model TicketCommentAction
    """

    kwargs_create_item: dict = {}

    model = None


    sub_model_type = None
    """Ticket Sub Model Type
    
    Ticket sub-models must have this attribute defined in `ModelNam.Meta.sub_model_type`
    """



class TicketCommentActionModelPyTest(
    TicketCommentActionModelTestCases,
):

    pass
