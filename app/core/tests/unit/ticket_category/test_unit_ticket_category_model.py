import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_ticketcategory
class TicketCategoryModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'ticket_category'
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
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
        'change': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'incident': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'problem': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'project_task': {
            'blank': False,
            'default': True,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        },
        'request': {
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



class TicketCategoryModelInheritedCases(
    TicketCategoryModelTestCases,
):
    pass



@pytest.mark.module_core
class TicketCategoryModelPyTest(
    TicketCategoryModelTestCases,
):
    pass
