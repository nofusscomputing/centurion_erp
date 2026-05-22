import pytest

from django.db import models

from pytest_simplified import NOT_USED

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)





@pytest.mark.model_configgrouphosts
class ConfigGroupHostModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'model_tag': {
                'type': NOT_USED,
                'value': NOT_USED,
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

    def test_attribute_page_layout_table_fields(self):
        pytest.xfail( reason = 'This model has no endpoint' )

    def test_attribute_page_layout_dataset_columns_fields(self):
        pytest.xfail( reason = 'This model has no endpoint' )
