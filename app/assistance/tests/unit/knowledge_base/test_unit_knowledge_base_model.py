import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_knowledgebase
class KnowledgeBaseModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'kb'
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
        'title': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'max_length': 50,
            'null': False,
            'unique': False,
        },
        'summary': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': True,
            'unique': False,
        },
        'content': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.TextField,
            'null': True,
            'unique': False,
        },
        'category': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'release_date': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'expiry_date': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'target_team': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ManyToManyField,
            'null': False,
            'unique': False,
        },
        'target_user': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'responsible_user': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'related_name': 'responsible_user',
            'unique': False,
        },
        'responsible_teams': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ManyToManyField,
            'null': False,
            'related_name': 'responsible_teams',
            'unique': False,
        },
        'public': {
            'blank': False,
            'default': False,
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



class KnowledgeBaseModelInheritedCases(
    KnowledgeBaseModelTestCases,
):
    pass



@pytest.mark.module_assistance
class KnowledgeBaseModelPyTest(
    KnowledgeBaseModelTestCases,
):
    pass
