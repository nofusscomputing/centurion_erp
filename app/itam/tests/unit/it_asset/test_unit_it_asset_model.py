import pytest

from django.db import models

from accounting.tests.unit.asset_base.test_unit_asset_base_model import (
    AssetBaseModelInheritedCases,
    AssetBase
)

from itam.models import ITAsset
from itam.tests.unit.itam_asset_base.test_unit_itam_asset_base_model  import (
    ITAMAssetModelInheritedCases
)



@pytest.mark.model_itasset
class ITAssetModelTestCases(
    ITAMAssetModelInheritedCases
):


    @property
    def parameterized_class_attributes(self):

        return {
            '_is_submodel': {
                'value': True
            },
            'app_namespace': {
                'type': str,
                'value': 'accounting'
            },
            'model_tag': {
                'type': str,
                'value': 'device'
            },
            'url_model_name': {
                'type': str,
                'value': 'asset'
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
            'null': False,
            'unique': True,
        },
        'uuid': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.UUIDField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'imei': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'mac_address': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'puk': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'puk_pin': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.CharField,
            'length': 50,
            'null': True,
            'unique': True,
        },
        'device_model': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.ForeignKey,
            'null': True,
            'unique': False,
        },
        'config': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.JSONField,
            'null': True,
            'unique': False,
        },
        'inventorydate': {
            'blank': True,
            'default': models.fields.NOT_PROVIDED,
            'field_type': models.DateTimeField,
            'null': True,
            'unique': False,
        },
        'is_virtual': {
            'blank': True,
            'default': False,
            'field_type': models.BooleanField,
            'null': False,
            'unique': False,
        }
    }


    def test_class_inherits_itasset(self, model):
        """ Class inheritence

        Model Must Inherit from itasset
        """

        assert issubclass(model, ITAsset)



class ITAssetModelInheritedCases(
    ITAssetModelTestCases,
):
    pass



@pytest.mark.module_itam
class ITAssetModelPyTest(
    ITAssetModelTestCases,
):
    pass
