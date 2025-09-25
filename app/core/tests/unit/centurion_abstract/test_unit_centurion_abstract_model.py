import pytest

from django.db import models

from django.utils.timezone import now

from access.tests.unit.tenancy_abstract.test_unit_tenancy_abstract_model import (
    TenancyAbstractModelInheritedCases
)

from core.tests.unit.mixin_centurion.test_unit_centurion_mixin import CenturionMixnInheritedCases
from core.models.centurion import CenturionModel



@pytest.mark.unit
@pytest.mark.centurion_models
class CenturionAbstractModelTestCases(
    CenturionMixnInheritedCases,
    TenancyAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):
        
        return {
            '_audit_enabled': {
                'type': bool,
                'value': True,
            },
            '_is_submodel': {
                'type': bool,
                'value': False,
            },
            '_notes_enabled': {
                'type': bool,
                'value': True,
            },
            'model_tag': {
                'type': str,
            },
            'url_model_name': {
                'type': type(None),
                'value': None,
            }
        }

    @property
    def parameterized_model_fields(self):
        
        return {
            'id': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.IntegerField,
                'null': False,
                'unique': True,
            },
            'model_notes': {
                'blank': True,
                'default': models.fields.NOT_PROVIDED,
                'field_type': models.TextField,
                'null': True,
                'unique': False,
            },
            'created': {
                'blank': False,
                'default': now,
                'field_type': models.DateTimeField,
                'null': False,
                'unique': False,
            },
        }



    def test_class_inherits_centurion_model(self, model):
        """ Class Check

        Ensure this model inherits from `CenturionModel`
        """

        assert issubclass(model, CenturionModel)



    def test_method_clean_fields_calls_super_centurion_abstract(self, mocker, model, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        if model._meta.abstract:
            pytest.xfail( reason = 'Model is an abstract model. test not required.' )

        super_clean = mocker.patch(
            'core.models.centurion.CenturionModel.clean_fields', return_value = None
        )

        model_instance.clean_fields()


        super_clean.assert_called_once()


    def test_method_clean_calls_super_centurion_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch(
            'core.models.centurion.CenturionModel.clean', return_value = None
        )

        model_instance.clean()


        super_clean.assert_called_once()


    def test_method_validate_constraints_calls_super_centurion_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch(
            'core.models.centurion.CenturionModel.validate_constraints', return_value = None
        )

        model_instance.validate_constraints()


        super_clean.assert_called_once()


    def test_method_validate_unique_calls_super_centurion_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `clean` calls `super().clean`
        """

        super_clean = mocker.patch(
            'core.models.centurion.CenturionModel.validate_unique', return_value = None
        )

        model_instance.validate_unique()


        super_clean.assert_called_once()


    def test_method_full_clean_calls_super_centurion_abstract(self, mocker, model_instance):
        """Test Class Method

        Ensure method `full_clean` calls `super().full_clean`
        """

        super_clean = mocker.patch(
            'core.models.centurion.CenturionModel.full_clean', return_value = None
        )

        model_instance.full_clean()


        super_clean.assert_called_once()




class CenturionAbstractModelInheritedCases(
    CenturionAbstractModelTestCases,
):

    pass



class CenturionAbstractModelPyTest(
    CenturionAbstractModelTestCases,
):

    @property
    def parameterized_class_attributes(self):
        
        return {
            'model_tag': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED,
            },
            'url_model_name': {
                'type': models.NOT_PROVIDED,
            },
            'page_layout': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED,
            },
            'table_fields': {
                'type': models.NOT_PROVIDED,
                'value': models.NOT_PROVIDED,
            }
        }



    def test_model_is_abstract(self, model):

        assert model._meta.abstract


    def test_model_tag_defined(self, model):

        pytest.xfail( reason = 'model is an abstract' )

    def test_manager_tenancy_filter_tenant(self):
        pytest.xfail( reason = 'base model, test is n/a.' )

    def test_manager_tenancy_select_related(self):
        pytest.xfail( reason = 'base model, test is n/a.' )
