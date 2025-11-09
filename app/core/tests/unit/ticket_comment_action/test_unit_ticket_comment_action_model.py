import pytest

from core.models.ticket_comment_action import TicketCommentAction

from core.tests.unit.ticket_comment_base.test_unit_ticket_comment_base_model import (
    TicketCommentBaseModelInheritedCases
)




@pytest.mark.model_ticketcommentaction
class TicketCommentActionModelTestCases(
    TicketCommentBaseModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_audit_enabled': {
                'value': False
            },
            '_is_submodel': {
                'value': True
            },
            '_notes_enabled': {
                'value': False
            },
            'model_tag': {
                'type': type(None),
                'value': None
            },
            'url_model_name': {
                'type': str,
                'value': 'ticket_comment_base'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {}



    def test_class_inherits_TicketCommentAction(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, TicketCommentAction)



    def test_function_called_clean_ticketcommentaction(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentAction.clean` is called
        """

        spy = mocker.spy(TicketCommentAction, 'clean')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        comment = model.objects.create(
            **valid_data
        )

        comment.delete()

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



    def test_function_save_called_slash_command(self):
        pytest.xfail( reason = 'action comment must not call slash_command. Test is N/A.' )



    def test_function_save_slash_command_not_called(self, model, mocker, ticket):
        """Function Check

        Ensure function `TicketCommentBase.clean` is called
        """

        spy = mocker.spy(model, 'slash_command')

        valid_data = self.kwargs_create_item.copy()

        valid_data['ticket'] = ticket

        item = model.objects.create(
            **valid_data
        )

        spy.assert_not_called



class TicketCommentActionModelInheritedCases(
    TicketCommentActionModelTestCases,
):

    sub_model_type = None



@pytest.mark.module_core
class TicketCommentActionModelPyTest(
    TicketCommentActionModelTestCases,
):

    sub_model_type = 'action'
