import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_cluster
class ClusterModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': str,
                'value': 'cluster'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
        'parent_cluster': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'cluster_type': {
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
            'length': 50,
            'null': False,
            'unique': False,
        },
        'config': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.JSONField,
            'null': True,
            'unique': False,
        },
        'nodes': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ManyToManyField,
            'null': False,
            'unique': False,
        },
        'devices': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ManyToManyField,
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



class ClusterModelInheritedCases(
    ClusterModelTestCases,
):
    pass



@pytest.mark.module_itim
class ClusterModelPyTest(
    ClusterModelTestCases,
):
    pass
