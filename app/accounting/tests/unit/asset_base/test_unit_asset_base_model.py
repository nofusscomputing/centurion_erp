import pytest

from django.db import models

from accounting.models.asset_base import AssetBase

from core.tests.unit.centurion_abstract.test_unit_centurion_abstract_model import (
    CenturionAbstractModelInheritedCases
)



@pytest.mark.model_assetbase
class AssetBaseModelTestCases(
    CenturionAbstractModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            'app_namespace': {
                'type': str,
                'value': 'accounting'
            },
            'model_tag': {
                'type': str,
                'value': 'asset'
            },
            'url_model_name': {
                'type': str,
                'value': 'asset'
            },
        }


    @property
    def parameterized_model_fields(self):

        return {
        'asset_number': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'max_length': 30,
            'null': True,
            'unique': True,
        },
        'serial_number': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'max_length': 30,
            'null': True,
            'unique': True,
        },
        'asset_type': {
            'blank': True,
            'default': 'asset',
            'field_type': models.CharField,
            'max_length': 30,
            'null': False,
            'unique': False,
        }
    }


    def test_class_inherits_assetbase(self, model):
        """ Class inheritence

        TenancyObject must inherit SaveHistory
        """

        assert issubclass(model, AssetBase)



class AssetBaseModelInheritedCases(
    AssetBaseModelTestCases,
):


    def test_method_get_url_kwargs(self, mocker, model_instance, settings):

        url = model_instance.get_url_kwargs()

        assert model_instance.get_url_kwargs() == {
            'model_name': model_instance._meta.model_name,
            'pk': model_instance.id
        }



@pytest.mark.module_accounting
class AssetBaseModelPyTest(
    AssetBaseModelTestCases,
):
    pass
