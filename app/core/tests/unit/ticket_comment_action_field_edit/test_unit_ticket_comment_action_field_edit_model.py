import pytest

from django.db import models

from core.models.ticket_comment_action import TicketCommentAction

from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_model import (
    TicketCommentActionModelInheritedCases
)



@pytest.mark.model_ticketcommentactionfieldedit
class TicketCommentActionFieldEditModelTestCases(
    TicketCommentActionModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_base_model': {
                'value': TicketCommentAction,
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
            "field_name": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'null': False,
                'unique': False,
            },
            "previous_value": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'null': True,
                'unique': False,
            },
            "new_value": {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.CharField,
                'null': True,
                'unique': False,
            },
        }



class TicketCommentActionFieldEditModelInheritedCases(
    TicketCommentActionFieldEditModelTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentActionFieldEditModelPyTest(
    TicketCommentActionFieldEditModelTestCases,
):
    pass
