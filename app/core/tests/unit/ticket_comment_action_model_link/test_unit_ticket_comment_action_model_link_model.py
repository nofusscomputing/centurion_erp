import pytest

from django.db import models

from core.models.ticket_comment_action import TicketCommentAction

from core.tests.unit.ticket_comment_action.test_unit_ticket_comment_action_model import (
    TicketCommentActionModelInheritedCases
)



@pytest.mark.model_ticketcommentactionmodellink
class TicketCommentActionModelLinkModelTestCases(
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
            "is_create": {
                'blank': False,
                'default': True,
                'field_type': models.BooleanField,
                'null': False,
                'unique': False,
            },
            "model_id": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.IntegerField,
                'null': False,
                'unique': False,
            },
            "content_type": {
                'blank': False,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.ForeignKey,
                'null': False,
                'unique': False,
            },
        }



class TicketCommentActionModelLinkModelInheritedCases(
    TicketCommentActionModelLinkModelTestCases,
):
    pass


@pytest.mark.module_core
class TicketCommentActionModelLinkModelPyTest(
    TicketCommentActionModelLinkModelTestCases,
):
    pass
