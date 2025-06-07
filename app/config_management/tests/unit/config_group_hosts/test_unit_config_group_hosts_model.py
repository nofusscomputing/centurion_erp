import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)





@pytest.mark.model_config_group_hosts
class ConfigGroupSoftwareModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {}


    parameterized_model_fields = {
        'host': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': False,
            'unique': False,
        },
        'group': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
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



class ConfigGroupSoftwareModelInheritedCases(
    ConfigGroupSoftwareModelTestCases,
):
    pass



class ConfigGroupSoftwareModelPyTest(
    ConfigGroupSoftwareModelTestCases,
):
    pass
