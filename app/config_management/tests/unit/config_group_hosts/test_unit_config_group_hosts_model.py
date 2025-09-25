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
            '_notes_enabled': {
                'value': False,
            },
            '_ticket_linkable': {
                'value': False,
            },
        }


    @property
    def parameterized_model_fields(self):
        
        return {
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
class ConfigGroupHostModelPyTest(
    ConfigGroupHostModelTestCases,
):


    def test_method_get_url_returns_str(self, mocker, model_instance):
        
        pytest.xfail( reason = 'This model has no endpoint' )
