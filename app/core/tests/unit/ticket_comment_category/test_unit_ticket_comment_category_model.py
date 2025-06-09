import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_ticketcommentcategory
class TicketCommentCategoryModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'ticket_comment_category'
            },
        }


    parameterized_model_fields = {
        'parent': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'max_length': 50,
            'null': False,
            'unique': False,
        },
        'runbook': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'comment': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'notification': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'solution': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'task': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'modified': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': False,
            'unique': False,
        },
    }



class TicketCommentCategoryModelInheritedCases(
    TicketCommentCategoryModelTestCases,
):
    pass



@pytest.mark.module_core
class TicketCommentCategoryModelPyTest(
    TicketCommentCategoryModelTestCases,
):
    pass
