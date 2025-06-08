import pytest

from django.db import models


from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)





@pytest.mark.model_configgrouphosts
class ConfigGroupHostModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED,
            },
        }


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


    @pytest.mark.xfail( reason = 'not required for this model' )
    def test_method_value_not_default___str__(self):
        pass

    @pytest.mark.xfail( reason = 'not required for this model' )
    def test_model_tag_defined(self):
        pass



class ConfigGroupHostModelInheritedCases(
    ConfigGroupHostModelTestCases,
):
    pass



@pytest.mark.module_config_management
@pytest.mark.configgrouphosts
class ConfigGroupHostModelPyTest(
    ConfigGroupHostModelTestCases,
):
    pass
