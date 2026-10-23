import pytest

from django.db import models

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractTenancyModelInheritedCases
)



@pytest.mark.model_itassetmodel
class ITAssetModelModelTestCases(
    CenturionAbstractTenancyModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': False
            },
            'model_tag': {
                'type': str,
                'value': 'device_model'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
        'name': {
            'blank': False,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'device_type': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'manufacturer': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'imei': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
        },
        'mac_address': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
        },
        'puk': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
        },
        'puk_pin': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
        },
        'serial_number': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
        },
    }



    def test_function__str__has_manufacturer(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if manufacturer exists that it is used in model
        stringify.
        """

        test_model = model( **model_kwargs() )

        assert str(test_model).startswith(test_model.manufacturer.name)



    def test_function__str__no_manufacturer(self,
        model, model_kwargs,
    ):
        """Test model function
        
        Ensure that if there is not manufacturer that it is not used in model
        stringify.
        """

        kwargs = model_kwargs()
        del kwargs['manufacturer']

        test_model = model( **kwargs )

        assert test_model.name == str(test_model)




class ITAssetModelModelInheritedCases(
    ITAssetModelModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelModelPyTest(
    ITAssetModelModelTestCases,
):
    pass
